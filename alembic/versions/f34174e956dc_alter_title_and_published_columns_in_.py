"""alter title and published columns in posts table

Revision ID: f34174e956dc
Revises: c5ebcac77acf
Create Date: 2022-11-06 01:48:06.387176

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f34174e956dc'
down_revision = 'c5ebcac77acf'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # change title column type
    op.alter_column('posts', 'title', type_=sa.String(),
                    existing_type=sa.String(length=100))
    # provide server default value for published column
    op.alter_column('posts', 'published', server_default='TRUE',
                    existing_type=sa.Boolean())


def downgrade() -> None:
    op.alter_column('posts', 'title', type_=sa.String(
        length=100), existing_type=sa.String())
    # do not provide server default value for published column
    op.alter_column('posts', 'published', server_default=None,
                    existing_type=sa.Boolean())
