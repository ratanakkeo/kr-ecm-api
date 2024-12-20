from typing import List, Optional

from app.api.deps import get_current_user
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.menu import MenuItem as MenuItemModel
from app.schemas.menu import MenuItem, MenuItemCreate

router = APIRouter()


@router.post("/", response_model=MenuItem)
def create_menu_item(
        item: MenuItemCreate,
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db)
):
    db_item = MenuItemModel(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get("/", response_model=List[MenuItem])
def get_menu_items(
        skip: int = 0,
        limit: int = 100,
        merchant_id: Optional[int] = None,
        category_id: Optional[int] = None,
        lang: Optional[str] = None,
        db: Session = Depends(get_db)
):
    query = db.query(MenuItemModel)

    if merchant_id:
        query = query.filter(MenuItemModel.merchant_id == merchant_id)
    if category_id:
        query = query.filter(MenuItemModel.category_id == category_id)

    items = query.offset(skip).limit(limit).all()

    # Handle translations if language is specified
    if lang and lang != "en":
        for item in items:
            if lang in item.translations:
                item.name = item.translations[lang]

    return items


@router.get("/{item_id}", response_model=MenuItem)
def get_menu_item(
        item_id: int,
        lang: Optional[str] = None,
        db: Session = Depends(get_db)
):
    item = db.query(MenuItemModel).filter(MenuItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")

    # Handle translation if language is specified
    if lang and lang != "en" and lang in item.translations:
        item.name = item.translations[lang]

    return item


@router.put("/{item_id}", response_model=MenuItem)
def update_menu_item(
        item_id: int,
        item: MenuItemCreate,
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db)
):
    db_item = db.query(MenuItemModel).filter(MenuItemModel.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Menu item not found")

    for key, value in item.model_dump(exclude_unset=True).items():
        setattr(db_item, key, value)

    db.commit()
    db.refresh(db_item)
    return db_item


@router.delete("/{item_id}")
def delete_menu_item(
        item_id: int,
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db)
):
    db_item = db.query(MenuItemModel).filter(MenuItemModel.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Menu item not found")

    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted successfully"}
