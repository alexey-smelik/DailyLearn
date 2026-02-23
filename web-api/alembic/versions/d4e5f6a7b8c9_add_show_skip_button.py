"""add show_pause_button and show_skip_button to learning_card

Revision ID: d4e5f6a7b8c9
Revises: c9d3e8f1a042
Create Date: 2026-02-23

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "d4e5f6a7b8c9"
down_revision: str | None = "c9d3e8f1a042"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "learning_cards",
        sa.Column("show_pause_button", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.add_column(
        "learning_cards",
        sa.Column("show_skip_button", sa.Boolean(), nullable=False, server_default=sa.true()),
    )


def downgrade() -> None:
    op.drop_column("learning_cards", "show_skip_button")
    op.drop_column("learning_cards", "show_pause_button")
