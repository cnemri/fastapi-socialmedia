"""create posts table

Revision ID: c1d23186cdee
Revises:
Create Date: 2022-11-06 01:20:11.140184

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1d23186cdee'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # create the posts table
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(100), nullable=False),
        sa.Column('content', sa.Text, nullable=False))


def downgrade() -> None:
    op.drop_table('posts')
