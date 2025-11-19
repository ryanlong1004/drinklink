from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models import Tag
from app.schemas.item import TagResponse, TagCreate, TagUpdate
from app.api.v1.endpoints.auth import get_current_user
from app.services.tag_suggestion import TagSuggestionService

router = APIRouter()


@router.get("", response_model=List[TagResponse])
async def get_tags(db: Session = Depends(get_db)):
    """
    Get all tags.
    Public endpoint.
    """
    tags = db.query(Tag).order_by(Tag.name).all()
    return tags


@router.get("/{tag_id}", response_model=TagResponse)
async def get_tag(tag_id: int, db: Session = Depends(get_db)):
    """
    Get a single tag by ID.
    Public endpoint.
    """
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@router.post("", response_model=TagResponse)
async def create_tag(
    tag_data: TagCreate,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a new tag.
    Admin only.
    """
    # Check if slug already exists
    existing = db.query(Tag).filter(Tag.slug == tag_data.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Tag slug already exists")

    # Auto-generate description if not provided
    tag_dict = tag_data.model_dump()
    if not tag_dict.get("description"):
        tag_dict["description"] = TagSuggestionService.get_tag_description(
            tag_data.name
        )

    tag = Tag(**tag_dict)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


@router.put("/{tag_id}", response_model=TagResponse)
async def update_tag(
    tag_id: int,
    tag_data: TagUpdate,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update an existing tag.
    Admin only.
    """
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    # Check slug uniqueness if being updated
    if tag_data.slug and tag_data.slug != tag.slug:
        existing = db.query(Tag).filter(Tag.slug == tag_data.slug).first()
        if existing:
            raise HTTPException(status_code=400, detail="Tag slug already exists")

    # Update fields
    update_data = tag_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(tag, field, value)

    db.commit()
    db.refresh(tag)
    return tag


@router.delete("/{tag_id}")
async def delete_tag(
    tag_id: int,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Delete a tag.
    Admin only.
    """
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    db.delete(tag)
    db.commit()
    return {"message": "Tag deleted successfully"}
