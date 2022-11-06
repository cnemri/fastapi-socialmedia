"""Add created_at column and foreign key user id to posts

Revision ID: c5ebcac77acf
Revises: b94c87488de0
Create Date: 2022-11-06 01:38:08.662463

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5ebcac77acf'
down_revision = 'b94c87488de0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False))
    # add forein key user id
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts',
                          referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', 'posts')
    op.drop_column('posts', 'owner_id')
    op.drop_column('posts', 'created_at')
