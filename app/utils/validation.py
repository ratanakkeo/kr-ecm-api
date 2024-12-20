from typing import Dict, Any

from fastapi import HTTPException

from app.models.products import ProductType


def validate_product_attributes(product_type: ProductType, attributes: Dict[str, Any]) -> None:
    """
    Validate product attributes based on product type.
    """
    if product_type == ProductType.DIGITAL:
        required_attrs = {"download_link", "file_size"}
    elif product_type == ProductType.PHYSICAL:
        required_attrs = {"weight", "dimensions"}
    elif product_type == product_type.COSMETIC:
        required_attrs = {"volume", "weight"}
    elif product_type == product_type.CAR_PART:
        required_attrs = {"weight", "dimensions"}
    elif product_type == product_type.CLOTHING:
        required_attrs = {"size", "color"}
    else:
        required_attrs = set()

    missing_attrs = required_attrs - set(attributes.keys())
    if missing_attrs:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required attributes for {product_type}: {', '.join(missing_attrs)}"
        )
