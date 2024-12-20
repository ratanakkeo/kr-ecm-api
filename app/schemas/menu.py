# schemas/menu.py
from typing import Optional, Dict, List
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field, validator


class MenuItemType(str, Enum):
    BEVERAGE = "beverage"
    FOOD = "food"
    DESSERT = "dessert"
    SNACK = "snack"


class BeverageType(str, Enum):
    HOT = "hot"
    COLD = "cold"
    BLENDED = "blended"


class CustomizationType(str, Enum):
    SUGAR_LEVEL = "sugar_level"
    ICE_LEVEL = "ice_level"
    EXTRA_SHOT = "extra_shot"
    SIZE = "size"
    MILK_TYPE = "milk_type"


# Add the missing Category schemas
class CategoryBase(BaseModel):
    """Base schema for menu categories with common fields"""
    name: str = Field(..., min_length=1, max_length=100)
    slug: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    translations: Dict[str, str] = Field(default_factory=dict)
    is_active: bool = Field(True)
    display_order: int = Field(0)
    image_url: Optional[str] = None
    parent_id: Optional[int] = None


class CategoryCreate(CategoryBase):
    """Schema for creating a new menu category"""
    merchant_id: int = Field(..., description="ID of the merchant")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Beverages",
                "slug": "beverages",
                "description": "All types of drinks",
                "translations": {
                    "km": "ភេសជ្ជៈ"
                },
                "display_order": 1,
                "merchant_id": 1
            }
        }


class Category(CategoryBase):
    """Schema for retrieving menu categories"""
    id: int
    merchant_id: int
    created_at: datetime
    updated_at: datetime
    subcategories: Optional[List['Category']] = []
    items_count: Optional[int] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Beverages",
                "slug": "beverages",
                "description": "All types of drinks",
                "translations": {
                    "km": "ភេសជ្ជៈ"
                },
                "is_active": True,
                "display_order": 1,
                "merchant_id": 1,
                "parent_id": None,
                "created_at": "2024-10-25T10:00:00",
                "updated_at": "2024-10-25T10:00:00",
                "subcategories": [],
                "items_count": 0
            }
        }


# Keep existing MenuItemBase, MenuItemCreate, MenuItem, and MenuItemUpdate classes as they are
class MenuItemBase(BaseModel):
    """Base schema for menu items with common fields"""
    name: str = Field(..., min_length=1, max_length=100, description="Item name")
    description: Optional[str] = Field(None, max_length=500, description="Item description")
    price_usd: float = Field(..., ge=0, description="Price in USD")
    price_khr: float = Field(..., ge=0, description="Price in KHR")
    is_active: bool = Field(True, description="Item availability status")
    item_type: MenuItemType = Field(..., description="Type of menu item")
    image_url: Optional[str] = Field(None, description="URL of item image")
    translations: Dict[str, str] = Field(
        default_factory=dict,
        description="Translations for item name and description"
    )
    customizations: Optional[List[CustomizationType]] = Field(
        None,
        description="Available customization options"
    )
    category_id: int = Field(..., description="ID of the category this item belongs to")
    merchant_id: int = Field(..., description="ID of the merchant this item belongs to")

    @validator('price_usd', 'price_khr')
    def validate_price(cls, v):
        if not isinstance(v, (int, float)):
            raise ValueError('Price must be a number')
        return round(float(v), 2)

    @validator('translations')
    def validate_translations(cls, v):
        if not isinstance(v, dict):
            raise ValueError('Translations must be a dictionary')
        for lang, text in v.items():
            if not isinstance(lang, str) or not isinstance(text, str):
                raise ValueError('Translation keys and values must be strings')
            if len(text) > 200:
                raise ValueError(f'Translation text too long for language {lang}')
        return v


class MenuItemCreate(MenuItemBase):
    """Schema for creating a new menu item"""
    category_id: int = Field(..., description="ID of the category")
    merchant_id: int = Field(..., description="ID of the merchant")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Iced Latte",
                "description": "Espresso mixed with cold milk",
                "price_usd": 3.00,
                "price_khr": 12000,
                "item_type": "beverage",
                "translations": {
                    "km": "កាហ្វេទឹកដោះគោត្រជាក់"
                },
                "customizations": [
                    "SUGAR_LEVEL",
                    "ICE_LEVEL",
                    "EXTRA_SHOT"
                ],
                "category_id": 1,
                "merchant_id": 1
            }
        }


class MenuItem(MenuItemBase):
    """Schema for retrieving menu items"""
    id: int
    created_at: datetime
    updated_at: datetime
    sales_rank: Optional[int] = None
    availability: bool = True

    class Config:
        from_attributes = True


class MenuItemUpdate(BaseModel):
    """Schema for updating menu items"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    price_usd: Optional[float] = Field(None, ge=0)
    price_khr: Optional[float] = Field(None, ge=0)
    is_active: Optional[bool] = None
    translations: Optional[Dict[str, str]] = None
    customizations: Optional[List[CustomizationType]] = None
    category_id: Optional[int] = None

    @validator('price_usd', 'price_khr')
    def validate_price(cls, v):
        if v is not None:
            if not isinstance(v, (int, float)):
                raise ValueError('Price must be a number')
            return round(float(v), 2)
        return v


class MenuItemResponse(BaseModel):
    """Schema for menu item list responses"""
    items: List[MenuItem]
    total: int
    page: int
    size: int
    has_more: bool

    class Config:
        json_schema_extra = {
            "example": {
                "items": [
                    {
                        "id": 1,
                        "name": "Iced Latte",
                        "price_usd": 3.00,
                        "price_khr": 12000,
                        "is_active": True
                    }
                ],
                "total": 1,
                "page": 1,
                "size": 10,
                "has_more": False
            }
        }
