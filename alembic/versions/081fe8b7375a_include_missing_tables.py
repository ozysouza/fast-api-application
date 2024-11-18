"""Include missing tables

Revision ID: 081fe8b7375a
Revises: 50af33d9c532
Create Date: 2024-11-18 11:45:45.385716

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '081fe8b7375a'
down_revision: Union[str, None] = '50af33d9c532'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
                              nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    op.create_table('votes',
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('post_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('user_id', 'post_id')
                    )
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    op.add_column('posts', sa.Column('published', sa.Boolean(), server_default=sa.text('true'), nullable=False))
    op.add_column('posts',
                  sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', 'posts', 'users', ['owner_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('post_users_fk', 'posts', type_='foreignkey')
    op.drop_column('posts', 'owner_id')
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'content')
    op.drop_table('votes')
    op.drop_table('users')
