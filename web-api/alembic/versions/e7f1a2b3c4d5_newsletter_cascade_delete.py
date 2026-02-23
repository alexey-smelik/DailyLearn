"""newsletter cascade delete on learning_card

Revision ID: e7f1a2b3c4d5
Revises: a1b2c3d4e5f6
Create Date: 2026-02-23

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = 'e7f1a2b3c4d5'
down_revision: Union[str, None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop the existing FK without CASCADE, re-create it with CASCADE
    op.drop_constraint(
        'newsletters_learning_card_id_fkey',
        'newsletters',
        type_='foreignkey',
    )
    op.create_foreign_key(
        'newsletters_learning_card_id_fkey',
        'newsletters',
        'learning_cards',
        ['learning_card_id'],
        ['id'],
        ondelete='CASCADE',
    )


def downgrade() -> None:
    op.drop_constraint(
        'newsletters_learning_card_id_fkey',
        'newsletters',
        type_='foreignkey',
    )
    op.create_foreign_key(
        'newsletters_learning_card_id_fkey',
        'newsletters',
        'learning_cards',
        ['learning_card_id'],
        ['id'],
    )
