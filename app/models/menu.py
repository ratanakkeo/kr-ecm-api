from enum import Enum
from sqlalchemy import Column, String, Float, Integer, ForeignKey, Boolean, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.db.base import TimeStampedBase


class MenuItemType(str, Enum):
    BEVERAGE = "beverage"
    FOOD = "food"
    DESSERT = "dessert"
    SNACK = "snack"


class BeverageType(str, Enum):
    HOT = "hot"
    COLD = "cold"
    BLENDED = "blended"


class MenuItem(TimeStampedBase):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price_usd = Column(Float)
    price_khr = Column(Float)
    is_active = Column(Boolean, default=True)
    translations = Column(JSON)
    image_url = Column(String)
    item_type = Column(SQLEnum(MenuItemType))
    attributes = Column(JSON)  # Store type-specific attributes
    merchant_id = Column(Integer, ForeignKey("merchants.id"))
    category_id = Column(Integer, ForeignKey("menu_categories.id"))

    merchant = relationship("Merchant", back_populates="menu_items")
    category = relationship("MenuCategory", back_populates="items")


class MenuCategory(TimeStampedBase):
    __tablename__ = "menu_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    slug = Column(String, unique=True, index=True)
    translations = Column(JSON)
    description = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    display_order = Column(Integer, default=0)
    merchant_id = Column(Integer, ForeignKey("merchants.id"))
    parent_id = Column(Integer, ForeignKey("menu_categories.id"), nullable=True)

    items = relationship("MenuItem", back_populates="category")
    merchant = relationship("Merchant", back_populates="categories")
    subcategories = relationship("MenuCategory",
                                 backref=relationship("MenuCategory", remote_side=[id]))
