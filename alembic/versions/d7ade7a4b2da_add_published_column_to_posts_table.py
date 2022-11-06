"""add published column to posts table

Revision ID: d7ade7a4b2da
Revises: c1d23186cdee
Create Date: 2022-11-06 01:28:43.161231

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd7ade7a4b2da'
down_revision = 'c1d23186cdee'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, default=True))


def downgrade() -> None:
    op.drop_column('posts', 'published')
