from fastapi import APIRouter
from app.api.v1.endpoints import auth, menu, protected
from app.api.v1.endpoints import categories

api_router = APIRouter()
api_router.include_router(menu.router, prefix="/menu", tags=["menu"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(protected.router, prefix="/protected", tags=["protected"])

api_router.include_router(
    categories.router,
    prefix="/categories",
    tags=["categories"]
)

