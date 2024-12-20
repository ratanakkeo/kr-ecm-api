import enum

from sqlalchemy import Column, String, Float, Integer, JSON, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.db.base import TimeStampedBase


class ProductType(str, enum.Enum):
    COSMETIC = "cosmetic"
    CAR_PART = "car_part"
    CLOTHING = "clothing"
    DIGITAL = "digital"
    PHYSICAL = "physical"


class Product(TimeStampedBase):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    stock = Column(Integer)
    type = Column(Enum(ProductType))
    attributes = Column(JSON)  # Store type-specific attributes
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="products")
    images = relationship("ProductImage", back_populates="product")


class Category(TimeStampedBase):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    products = relationship("Product", back_populates="category")
    children = relationship("Category")
