from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.endpoints.auth import get_current_user
from app.core.database import get_db
from app.models import Item, Tag
from app.schemas.item import TagCreate, TagResponse, TagUpdate
from app.services.tag_suggestion import TagSuggestionService

router = APIRouter()


@router.get("", response_model=list[TagResponse])
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
        tag_dict["description"] = TagSuggestionService.get_tag_description(tag_data.name)

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


@router.post("/auto-generate")
async def auto_generate_tags(
    current_user: str = Depends(get_current_user),  # noqa: ARG001
    db: Session = Depends(get_db),
):
    """
    Auto-generate tags from all items in the database.
    Analyzes item names, descriptions, ABV, and origins to suggest tags.
    Creates tags that don't already exist and assigns them to the items
    they were found on.
    Admin only.
    """
    # Get all items
    items = db.query(Item).all()

    # Collect suggested tags per item
    item_suggestions = {}  # {item_id: [tag_names]}
    all_suggested_tags = set()

    for item in items:
        suggested = TagSuggestionService.suggest_tags_from_item(
            name=item.name,
            description=item.description,
            abv=item.abv,
            origin=item.origin,
        )
        item_suggestions[item.id] = suggested
        all_suggested_tags.update(suggested)

    # Get existing tags
    existing_tags_dict = {tag.name.lower(): tag for tag in db.query(Tag).all()}

    # Color mapping for different tag types
    color_map = {
        "hoppy": "#10B981",
        "malty": "#F59E0B",
        "fruity": "#EC4899",
        "citrus": "#FBBF24",
        "sweet": "#F472B6",
        "dry": "#8B5CF6",
        "crisp": "#3B82F6",
        "light": "#60A5FA",
        "rich": "#7C3AED",
        "tart": "#DC2626",
        "oaky": "#92400E",
    }

    # Create new tags
    created_tags = []
    for tag_name in all_suggested_tags:
        if tag_name.lower() not in existing_tags_dict:
            # Generate slug
            slug = tag_name.lower().replace(" ", "-")

            # Get description
            description = TagSuggestionService.get_tag_description(tag_name)

            # Assign color
            color = color_map.get(tag_name.lower(), "#3B82F6")

            tag = Tag(name=tag_name.title(), slug=slug, description=description, color=color)
            db.add(tag)
            db.flush()  # Flush to get the tag ID
            existing_tags_dict[tag_name.lower()] = tag
            created_tags.append(tag_name.title())

    # Now assign tags to items
    items_updated = 0
    for item in items:
        if item.id in item_suggestions:
            suggested_tag_names = item_suggestions[item.id]

            # Get current tag IDs for this item
            current_tag_ids = {tag.id for tag in item.tags}

            # Find tags to add
            tags_to_add = []
            for tag_name in suggested_tag_names:
                tag = existing_tags_dict.get(tag_name.lower())
                if tag and tag.id not in current_tag_ids:
                    tags_to_add.append(tag)

            # Add new tags to item
            if tags_to_add:
                item.tags.extend(tags_to_add)
                items_updated += 1

    db.commit()

    msg = f"Successfully created {len(created_tags)} new tags"
    msg += f" and updated {items_updated} items"

    return {
        "message": msg,
        "created_tags": created_tags,
        "items_updated": items_updated,
        "total_suggested": len(all_suggested_tags),
        "already_existed": len(all_suggested_tags) - len(created_tags),
    }
