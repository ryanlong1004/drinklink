from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from app.core.database import get_db
from app.models import Item, Category, Tag
from app.schemas.item import ItemResponse, ItemCreate, ItemUpdate, ItemListResponse
from app.api.v1.endpoints.auth import get_current_user
from app.services.tag_suggestion import TagSuggestionService
from math import ceil

router = APIRouter()


@router.get("", response_model=ItemListResponse)
async def get_items(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category_id: Optional[int] = None,
    tag_ids: Optional[str] = None,  # Comma-separated tag IDs
    search: Optional[str] = None,
    sort_by: str = Query("name", regex="^(name|price|abv|created_at)$"),
    sort_order: str = Query("asc", regex="^(asc|desc)$"),
    published_only: bool = True,
    db: Session = Depends(get_db),
):
    """
    Get paginated list of menu items with filtering and sorting.
    Public endpoint - only returns published items by default.
    """
    query = db.query(Item)

    # Filter by published status
    if published_only:
        query = query.filter(Item.is_published == True)

    # Filter by category
    if category_id:
        query = query.filter(Item.category_id == category_id)

    # Filter by tags (items must have ALL specified tags)
    if tag_ids:
        tag_id_list = [int(tid) for tid in tag_ids.split(",") if tid.strip()]
        for tag_id in tag_id_list:
            query = query.filter(Item.tags.any(Tag.id == tag_id))

    # Search in name, description, producer
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Item.name.ilike(search_term),
                Item.description.ilike(search_term),
                Item.producer.ilike(search_term),
            )
        )

    # Sorting
    if sort_order == "desc":
        query = query.order_by(getattr(Item, sort_by).desc())
    else:
        query = query.order_by(getattr(Item, sort_by).asc())

    # Get total count before pagination
    total = query.count()

    # Pagination
    offset = (page - 1) * page_size
    items = query.offset(offset).limit(page_size).all()

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": ceil(total / page_size) if total > 0 else 0,
    }


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    """
    Get a single item by ID.
    Public endpoint.
    """
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("", response_model=ItemResponse)
async def create_item(
    item_data: ItemCreate,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a new menu item.
    Admin only.
    """
    # Create item
    item = Item(**item_data.model_dump(exclude={"tag_ids"}))

    # Add tags if provided
    if item_data.tag_ids:
        tags = db.query(Tag).filter(Tag.id.in_(item_data.tag_ids)).all()
        item.tags = tags

    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int,
    item_data: ItemUpdate,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update an existing menu item.
    Admin only.
    """
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Update fields
    update_data = item_data.model_dump(exclude_unset=True, exclude={"tag_ids"})
    for field, value in update_data.items():
        setattr(item, field, value)

    # Update tags if provided
    if item_data.tag_ids is not None:
        tags = db.query(Tag).filter(Tag.id.in_(item_data.tag_ids)).all()
        item.tags = tags

    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}")
async def delete_item(
    item_id: int,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Delete a menu item.
    Admin only.
    """
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()
    return {"message": "Item deleted successfully"}


@router.post("/suggest-tags")
async def suggest_tags(
    name: str = Query(...),
    description: Optional[str] = None,
    abv: Optional[float] = None,
    origin: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Suggest tags based on item attributes.
    Returns matching tags that exist in the database.
    """
    # Get suggested tag names
    suggested_names = TagSuggestionService.suggest_tags_from_item(
        name=name, description=description, abv=abv, origin=origin
    )

    # Find existing tags with these names
    if suggested_names:
        suggested_tags = db.query(Tag).filter(Tag.name.in_(suggested_names)).all()
    else:
        suggested_tags = []

    return {
        "suggested_tag_names": list(suggested_names),
        "existing_tags": suggested_tags,
    }
