"""add schedule to learning_card

Revision ID: e1f805b42cc6
Revises: bca8253862ce
Create Date: 2026-02-22

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "e1f805b42cc6"
down_revision: Union[str, None] = "bca8253862ce"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("learning_cards", sa.Column("schedule", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("learning_cards", "schedule")
