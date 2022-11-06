"""create users table

Revision ID: b94c87488de0
Revises: d7ade7a4b2da
Create Date: 2022-11-06 01:34:22.351987

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b94c87488de0'
down_revision = 'd7ade7a4b2da'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                  server_default=sa.text('now()'), nullable=False),
        sa.UniqueConstraint('email', name='unique_email')
    )


def downgrade() -> None:
    op.drop_table('users')
