from datetime import datetime

from pydantic import BaseModel, Field


# Category Schemas
class CategoryBase(BaseModel):
    name: str = Field(..., max_length=50)
    slug: str = Field(..., max_length=50)
    description: str | None = None
    icon: str | None = Field(None, max_length=10)
    sort_order: int = 0


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str | None = Field(None, max_length=50)
    slug: str | None = Field(None, max_length=50)
    description: str | None = None
    icon: str | None = Field(None, max_length=10)
    sort_order: int | None = None


class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


# Tag Schemas
class TagBase(BaseModel):
    name: str = Field(..., max_length=50)
    slug: str = Field(..., max_length=50)
    description: str | None = None
    color: str = Field(default="#3B82F6", pattern="^#[0-9A-Fa-f]{6}$")


class TagCreate(TagBase):
    pass


class TagUpdate(BaseModel):
    name: str | None = Field(None, max_length=50)
    slug: str | None = Field(None, max_length=50)
    description: str | None = None
    color: str | None = Field(None, pattern="^#[0-9A-Fa-f]{6}$")


class TagResponse(TagBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


# Item Schemas
class ItemBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: str | None = None
    category_id: int | None = None
    price: float = Field(..., ge=0)
    abv: float | None = Field(None, ge=0, le=100)
    volume: str | None = Field(None, max_length=20)
    origin: str | None = Field(None, max_length=100)
    producer: str | None = Field(None, max_length=100)
    is_published: bool = True
    sort_order: int = 0
    image_url: str | None = Field(None, max_length=500)


class ItemCreate(ItemBase):
    tag_ids: list[int] = []


class ItemUpdate(BaseModel):
    name: str | None = Field(None, max_length=100)
    description: str | None = None
    category_id: int | None = None
    price: float | None = Field(None, ge=0)
    abv: float | None = Field(None, ge=0, le=100)
    volume: str | None = Field(None, max_length=20)
    origin: str | None = Field(None, max_length=100)
    producer: str | None = Field(None, max_length=100)
    is_published: bool | None = None
    sort_order: int | None = None
    image_url: str | None = Field(None, max_length=500)
    tag_ids: list[int] | None = None


class ItemResponse(ItemBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None
    category: CategoryResponse | None = None
    tags: list[TagResponse] = []

    class Config:
        from_attributes = True


# List response with metadata
class ItemListResponse(BaseModel):
    items: list[ItemResponse]
    total: int
    page: int
    page_size: int
    pages: int
