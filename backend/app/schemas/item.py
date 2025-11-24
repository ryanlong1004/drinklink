from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# Category Schemas
class CategoryBase(BaseModel):
    name: str = Field(..., max_length=50)
    slug: str = Field(..., max_length=50)
    description: Optional[str] = None
    icon: Optional[str] = Field(None, max_length=10)
    sort_order: int = 0


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    slug: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    icon: Optional[str] = Field(None, max_length=10)
    sort_order: Optional[int] = None


class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Tag Schemas
class TagBase(BaseModel):
    name: str = Field(..., max_length=50)
    slug: str = Field(..., max_length=50)
    description: Optional[str] = None
    color: str = Field(default="#3B82F6", pattern="^#[0-9A-Fa-f]{6}$")


class TagCreate(TagBase):
    pass


class TagUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    slug: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    color: Optional[str] = Field(None, pattern="^#[0-9A-Fa-f]{6}$")


class TagResponse(TagBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Item Schemas
class ItemBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None
    category_id: Optional[int] = None
    price: float = Field(..., ge=0)
    abv: Optional[float] = Field(None, ge=0, le=100)
    volume: Optional[str] = Field(None, max_length=20)
    origin: Optional[str] = Field(None, max_length=100)
    producer: Optional[str] = Field(None, max_length=100)
    is_published: bool = True
    sort_order: int = 0
    image_url: Optional[str] = Field(None, max_length=500)


class ItemCreate(ItemBase):
    tag_ids: List[int] = []


class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    category_id: Optional[int] = None
    price: Optional[float] = Field(None, ge=0)
    abv: Optional[float] = Field(None, ge=0, le=100)
    volume: Optional[str] = Field(None, max_length=20)
    origin: Optional[str] = Field(None, max_length=100)
    producer: Optional[str] = Field(None, max_length=100)
    is_published: Optional[bool] = None
    sort_order: Optional[int] = None
    image_url: Optional[str] = Field(None, max_length=500)
    tag_ids: Optional[List[int]] = None


class ItemResponse(ItemBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    category: Optional[CategoryResponse] = None
    tags: List[TagResponse] = []

    class Config:
        from_attributes = True


# List response with metadata
class ItemListResponse(BaseModel):
    items: List[ItemResponse]
    total: int
    page: int
    page_size: int
    pages: int
