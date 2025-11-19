from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    Text,
    DateTime,
    Table,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

# Association table for many-to-many relationship between items and tags
item_tags = Table(
    "item_tags",
    Base.metadata,
    Column(
        "item_id", Integer, ForeignKey("items.id", ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True
    ),
)


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    slug = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text)
    icon = Column(String(10))  # Emoji icon for the category
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    items = relationship(
        "Item", back_populates="category", cascade="all, delete-orphan"
    )


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    slug = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text)
    color = Column(String(7), default="#3B82F6")  # Hex color for UI
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    items = relationship("Item", secondary=item_tags, back_populates="tags")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"))

    # Pricing
    price = Column(Float, nullable=False)

    # Details
    abv = Column(Float)  # Alcohol by volume
    volume = Column(String(20))  # e.g., "12 oz", "750ml"
    origin = Column(String(100))  # Country/region of origin
    producer = Column(String(100))  # Brewery, winery, distillery

    # Metadata
    is_published = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)
    image_url = Column(String(500))

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    category = relationship("Category", back_populates="items")
    tags = relationship("Tag", secondary=item_tags, back_populates="items")
