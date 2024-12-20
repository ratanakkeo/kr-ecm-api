from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.products import Product, ProductType
from app.schemas.products import ProductCreate, ProductBase
from app.utils.validation import validate_product_attributes

router = APIRouter()


@router.post("/", response_model=ProductBase)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    # Validate attributes based on product type
    validate_product_attributes(product.type, product.attributes)

    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        type=product.type,
        attributes=product.attributes,
        category_id=product.category_id
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.get("/{product_id}", response_model=ProductBase)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("/", response_model=List[ProductBase])
def get_products(
        skip: int = 0,
        limit: int = 100,
        product_type: Optional[ProductType] = None,
        category_id: Optional[int] = None,
        db: Session = Depends(get_db)
):
    query = db.query(Product)
    if product_type:
        query = query.filter(Product.type == product_type)
    if category_id:
        query = query.filter(Product.category_id == category_id)
    return query.offset(skip).limit(limit).all()
