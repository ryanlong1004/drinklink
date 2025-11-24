from fastapi import APIRouter

from app.api.v1.endpoints import auth, categories, data, items, tags

api_router = APIRouter()

# Public endpoints
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(tags.router, prefix="/tags", tags=["tags"])

# Auth endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Admin endpoints
api_router.include_router(data.router, prefix="/data", tags=["data"])
