"""add_icon_to_category

Revision ID: 57b75b3c85a2
Revises: 5539dbf7cca3
Create Date: 2025-11-19 19:49:55.623438

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "57b75b3c85a2"
down_revision = "5539dbf7cca3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add icon column to categories table
    op.add_column("categories", sa.Column("icon", sa.String(10), nullable=True))

    # Set default icons for existing categories
    op.execute(
        "UPDATE categories SET icon = '🍺' WHERE LOWER(name) LIKE '%draft%' OR LOWER(name) LIKE '%tap%'"
    )
    op.execute("UPDATE categories SET icon = '🍾' WHERE LOWER(name) LIKE '%bottle%'")
    op.execute("UPDATE categories SET icon = '🍷' WHERE LOWER(name) LIKE '%wine%'")
    op.execute("UPDATE categories SET icon = '🥫' WHERE LOWER(name) LIKE '%seltzer%'")
    op.execute("UPDATE categories SET icon = '🍸' WHERE LOWER(name) LIKE '%cocktail%'")
    op.execute(
        "UPDATE categories SET icon = '🥃' WHERE LOWER(name) LIKE '%spirit%' OR LOWER(name) LIKE '%liquor%'"
    )
    # Set default for any remaining null icons
    op.execute("UPDATE categories SET icon = '🍺' WHERE icon IS NULL")


def downgrade() -> None:
    # Remove icon column from categories table
    op.drop_column("categories", "icon")
