import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from app.api.v1.api import api_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.models.products import ProductType
from app.db.init_db import init_db
from app.db.session import SessionLocal

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)
# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.on_event("startup")
async def startup_event():
    logger.info("Application startup complete.")
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Initialize default data if needed
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Welcome to Menu API"}


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown complete.")


@app.exception_handler(HTTPException)
async def http_exception_handler(exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


# Sample product attributes validation
PRODUCT_ATTRIBUTES = {
    "cosmetic": {
        "required": ["brand", "volume", "skin_type"],
        "optional": ["ingredients", "expiration_date"]
    },
    "car_part": {
        "required": ["manufacturer", "model", "year"],
        "optional": ["compatibility", "warranty"]
    },
    "clothing": {
        "required": ["brand", "size", "color"],
        "optional": ["material", "care_instructions"]
    }
}


def validate_product_attributes(product_type: ProductType, attributes: dict):
    required = PRODUCT_ATTRIBUTES[product_type]["required"]
    missing = [attr for attr in required if attr not in attributes]
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required attributes for {product_type}: {missing}"
        )
