from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import Category, Tag, Item
from app.api.v1.endpoints.auth import get_current_user
from typing import Dict, Any
import json

router = APIRouter()


@router.get("/export")
async def export_data(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Export all database data (categories, tags, items).
    Admin only.
    Returns JSON with all data for backup/migration.
    """
    # Get all categories
    categories = db.query(Category).all()
    categories_data = [
        {
            "id": c.id,
            "name": c.name,
            "slug": c.slug,
            "description": c.description,
            "icon": c.icon,
            "sort_order": c.sort_order,
        }
        for c in categories
    ]

    # Get all tags
    tags = db.query(Tag).all()
    tags_data = [
        {
            "id": t.id,
            "name": t.name,
            "slug": t.slug,
            "description": t.description,
            "color": t.color,
        }
        for t in tags
    ]

    # Get all items with their relationships
    items = db.query(Item).all()
    items_data = [
        {
            "id": i.id,
            "name": i.name,
            "description": i.description,
            "category_id": i.category_id,
            "price": i.price,
            "abv": i.abv,
            "volume": i.volume,
            "origin": i.origin,
            "producer": i.producer,
            "is_published": i.is_published,
            "sort_order": i.sort_order,
            "image_url": i.image_url,
            "tag_ids": [t.id for t in i.tags],
        }
        for i in items
    ]

    return {
        "version": "1.0",
        "export_date": "2025-11-19",
        "categories": categories_data,
        "tags": tags_data,
        "items": items_data,
    }


@router.post("/import")
async def import_data(
    data: Dict[Any, Any],
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
    clear_existing: bool = False,
):
    """
    Import data from export.
    Admin only.

    Set clear_existing=true to delete all existing data first.
    Otherwise, will skip items with duplicate IDs.
    """
    try:
        # Clear existing data if requested
        if clear_existing:
            db.query(Item).delete()
            db.query(Tag).delete()
            db.query(Category).delete()
            db.commit()

        # Import categories
        category_map = {}
        for cat_data in data.get("categories", []):
            existing = db.query(Category).filter(Category.id == cat_data["id"]).first()
            if not existing:
                category = Category(
                    id=cat_data["id"],
                    name=cat_data["name"],
                    slug=cat_data["slug"],
                    description=cat_data.get("description"),
                    icon=cat_data.get("icon"),
                    sort_order=cat_data.get("sort_order", 0),
                )
                db.add(category)
                category_map[cat_data["id"]] = category

        db.commit()

        # Import tags
        tag_map = {}
        for tag_data in data.get("tags", []):
            existing = db.query(Tag).filter(Tag.id == tag_data["id"]).first()
            if not existing:
                tag = Tag(
                    id=tag_data["id"],
                    name=tag_data["name"],
                    slug=tag_data["slug"],
                    description=tag_data.get("description"),
                    color=tag_data.get("color", "#3B82F6"),
                )
                db.add(tag)
                tag_map[tag_data["id"]] = tag

        db.commit()

        # Import items
        items_imported = 0
        for item_data in data.get("items", []):
            existing = db.query(Item).filter(Item.id == item_data["id"]).first()
            if not existing:
                item = Item(
                    id=item_data["id"],
                    name=item_data["name"],
                    description=item_data.get("description"),
                    category_id=item_data.get("category_id"),
                    price=item_data["price"],
                    abv=item_data.get("abv"),
                    volume=item_data.get("volume"),
                    origin=item_data.get("origin"),
                    producer=item_data.get("producer"),
                    is_published=item_data.get("is_published", True),
                    sort_order=item_data.get("sort_order", 0),
                    image_url=item_data.get("image_url"),
                )

                # Add tags
                if "tag_ids" in item_data:
                    tags = db.query(Tag).filter(Tag.id.in_(item_data["tag_ids"])).all()
                    item.tags = tags

                db.add(item)
                items_imported += 1

        db.commit()

        return {
            "success": True,
            "message": "Data imported successfully",
            "categories_imported": len(data.get("categories", [])),
            "tags_imported": len(data.get("tags", [])),
            "items_imported": items_imported,
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")
