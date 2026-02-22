"""move tg fields to learning_card

Revision ID: a3f92c1d5e87
Revises: e1f805b42cc6
Create Date: 2026-02-23

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "a3f92c1d5e87"
down_revision: str | None = "e1f805b42cc6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Add Telegram config + creation timestamp to learning_cards
    op.add_column("learning_cards", sa.Column("tg_chat_id", sa.String(255), nullable=True))
    op.add_column("learning_cards", sa.Column("tg_topic_id", sa.Integer(), nullable=True))
    op.add_column("learning_cards", sa.Column("message_template", sa.Text(), nullable=True))
    op.add_column(
        "learning_cards",
        sa.Column(
            "add_date",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )

    # Drop moved columns from newsletters
    op.drop_column("newsletters", "tg_chat_id")
    op.drop_column("newsletters", "tg_topic_id")
    op.drop_column("newsletters", "message_template")
    op.drop_column("newsletters", "add_date")


def downgrade() -> None:
    # Restore newsletters columns
    op.add_column(
        "newsletters",
        sa.Column("add_date", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.add_column("newsletters", sa.Column("message_template", sa.Text(), nullable=False))
    op.add_column("newsletters", sa.Column("tg_topic_id", sa.Integer(), nullable=True))
    op.add_column("newsletters", sa.Column("tg_chat_id", sa.String(255), nullable=False))

    # Remove columns from learning_cards
    op.drop_column("learning_cards", "add_date")
    op.drop_column("learning_cards", "message_template")
    op.drop_column("learning_cards", "tg_topic_id")
    op.drop_column("learning_cards", "tg_chat_id")
