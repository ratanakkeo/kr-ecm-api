from typing import List, Optional

from app.api.deps import get_current_user
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.menu import MenuCategory
from app.schemas.menu import Category, CategoryCreate

router = APIRouter()


@router.post("/", response_model=Category)
def create_category(
        category: CategoryCreate,
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db)
):
    # Check if slug is unique
    if db.query(MenuCategory).filter(MenuCategory.slug == category.slug).first():
        raise HTTPException(status_code=400, detail="Category slug already exists")

    db_category = MenuCategory(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@router.get("/", response_model=List[Category])
def get_categories(
        skip: int = 0,
        limit: int = 100,
        merchant_id: Optional[int] = None,
        parent_id: Optional[int] = None,
        lang: Optional[str] = None,
        include_inactive: bool = False,
        db: Session = Depends(get_db)
):
    query = db.query(MenuCategory)

    if merchant_id:
        query = query.filter(MenuCategory.merchant_id == merchant_id)
    if parent_id is not None:
        query = query.filter(MenuCategory.parent_id == parent_id)
    if not include_inactive:
        query = query.filter(MenuCategory.is_active == True)

    query = query.order_by(MenuCategory.display_order)
    categories = query.offset(skip).limit(limit).all()

    # Handle translations
    if lang and lang != "en":
        for category in categories:
            if lang in category.translations:
                category.name = category.translations[lang]

    return categories


@router.get("/{category_id}", response_model=Category)
def get_category(
        category_id: int,
        lang: Optional[str] = None,
        db: Session = Depends(get_db)
):
    category = db.query(MenuCategory).filter(MenuCategory.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    if lang and lang != "en" and lang in category.translations:
        category.name = category.translations[lang]

    return category


@router.put("/{category_id}", response_model=Category)
def update_category(
        category_id: int,
        category: CategoryCreate,
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db)
):
    db_category = db.query(MenuCategory).filter(MenuCategory.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Check slug uniqueness if changed
    if category.slug != db_category.slug:
        if db.query(MenuCategory).filter(MenuCategory.slug == category.slug).first():
            raise HTTPException(status_code=400, detail="Category slug already exists")

    for key, value in category.model_dump(exclude_unset=True).items():
        setattr(db_category, key, value)

    db.commit()
    db.refresh(db_category)
    return db_category


@router.delete("/{category_id}")
def delete_category(
        category_id: int,
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db)
):
    db_category = db.query(MenuCategory).filter(MenuCategory.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Check if category has items
    if db_category.items:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete category with existing items. Move or delete items first."
        )

    db.delete(db_category)
    db.commit()
    return {"message": "Category deleted successfully"}
