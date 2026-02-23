"""add conspect fields to learning_cards

Revision ID: f2a3b4c5d6e7
Revises: d4e5f6a7b8c9
Create Date: 2026-02-23 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'f2a3b4c5d6e7'
down_revision = 'd4e5f6a7b8c9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('learning_cards', sa.Column('time_to_educate', sa.Text(), nullable=True))
    op.add_column('learning_cards', sa.Column('conspect', sa.Text(), nullable=True))
    op.add_column(
        'learning_cards',
        sa.Column(
            'conspect_requested',
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )


def downgrade() -> None:
    op.drop_column('learning_cards', 'conspect_requested')
    op.drop_column('learning_cards', 'conspect')
    op.drop_column('learning_cards', 'time_to_educate')
