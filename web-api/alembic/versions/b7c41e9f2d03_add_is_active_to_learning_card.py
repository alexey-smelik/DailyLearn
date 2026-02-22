"""add is_active to learning_card

Revision ID: b7c41e9f2d03
Revises: a3f92c1d5e87
Create Date: 2026-02-23

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "b7c41e9f2d03"
down_revision: str | None = "a3f92c1d5e87"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "learning_cards",
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
    )


def downgrade() -> None:
    op.drop_column("learning_cards", "is_active")
