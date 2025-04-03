"""empty message

Revision ID: 0b0476ca9dfb
Revises: 
Create Date: 2025-04-03 03:37:11.779121

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0b0476ca9dfb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('login', sa.String(length=256), nullable=False),
    sa.Column('password_hash', sa.String(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('avatar', sa.String(), server_default=sa.text("'your_default_user_avatar_name_from_MinIo'"), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('login')
    )
    op.create_table('roadmaps',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=256), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('difficulty', sa.Enum('easy', 'medium', 'hard', name='difficultyenum'), nullable=False),
    sa.Column('edit_permission', sa.Enum('view_only', 'can_edit', name='editpermissionenum'), nullable=False),
    sa.Column('visibility', sa.Enum('public', 'link_only', 'private', name='visibilityenum'), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cards',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('roadmap_id', sa.Integer(), nullable=False),
    sa.Column('order_position', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=256), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['roadmap_id'], ['roadmaps.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('roadmap_id', 'order_position', name='uq_roadmap_card_position')
    )
    op.create_table('user_roadmaps',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('roadmap_id', sa.Integer(), nullable=False),
    sa.Column('background', sa.String(), server_default=sa.text("'your_default_roadmap_background_from_MinIo'"), nullable=False),
    sa.ForeignKeyConstraint(['roadmap_id'], ['roadmaps.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'roadmap_id')
    )
    op.create_table('card_links',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('card_id', sa.Integer(), nullable=False),
    sa.Column('link_title', sa.String(length=256), nullable=True),
    sa.Column('link_content', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['card_id'], ['cards.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_cards',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('card_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('in_progress', 'done', 'to_do', name='statusenum'), server_default=sa.text("'to_do'"), nullable=False),
    sa.ForeignKeyConstraint(['card_id'], ['cards.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'card_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_cards')
    op.drop_table('card_links')
    op.drop_table('user_roadmaps')
    op.drop_table('cards')
    op.drop_table('roadmaps')
    op.drop_table('users')
    op.execute('DROP TYPE IF EXISTS accessabilityenum')
    op.execute('DROP TYPE IF EXISTS difficultyenum')
    op.execute('DROP TYPE IF EXISTS editpermissionenum')
    op.execute('DROP TYPE IF EXISTS roleenum')
    op.execute('DROP TYPE IF EXISTS statusenum')
    op.execute('DROP TYPE IF EXISTS visibilityenum')
    # ### end Alembic commands ###
