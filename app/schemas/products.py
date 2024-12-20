from enum import Enum
from typing import Optional, List, Dict, Union

from pydantic import BaseModel, Field


class ProductType(str, Enum):
    COSMETIC = "cosmetic"
    CAR_PART = "car_part"
    CLOTHING = "clothing"


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    type: ProductType
    attributes: Dict[str, Union[str, int, float, List[str]]]


class ProductCreate(ProductBase):
    category_id: int


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(gt=0)
    stock: Optional[int] = Field(ge=0)
    attributes: Optional[Dict[str, Union[str, int, float, List[str]]]] = None
