"""initial

Revision ID: bca8253862ce
Revises:
Create Date: 2026-02-22

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "bca8253862ce"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("login", sa.String(length=255), nullable=False),
        sa.Column("last_visit", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("login"),
    )

    op.create_table(
        "learning_cards",
        sa.Column("id", sa.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("source_url", sa.Text(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "newsletters",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("learning_card_id", sa.UUID(as_uuid=True), nullable=False),
        sa.Column("message_template", sa.Text(), nullable=False),
        sa.Column("send_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "add_date",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("tg_chat_id", sa.String(length=255), nullable=False),
        sa.Column("tg_topic_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["learning_card_id"], ["learning_cards.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("newsletters")
    op.drop_table("learning_cards")
    op.drop_table("users")
