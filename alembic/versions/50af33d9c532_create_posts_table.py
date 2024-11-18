"""Create posts table

Revision ID: 50af33d9c532
Revises: 
Create Date: 2024-11-18 11:00:32.568817

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '50af33d9c532'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False)
    )
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
