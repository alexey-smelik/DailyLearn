"""add groups

Revision ID: c9d3e8f1a042
Revises: b7c41e9f2d03
Create Date: 2026-02-23

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "c9d3e8f1a042"
down_revision: str | None = "b7c41e9f2d03"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "card_groups",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.add_column(
        "learning_cards",
        sa.Column("group_id", sa.Integer(), nullable=True),
    )
    op.create_foreign_key(
        "fk_learning_cards_group_id",
        "learning_cards",
        "card_groups",
        ["group_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint("fk_learning_cards_group_id", "learning_cards", type_="foreignkey")
    op.drop_column("learning_cards", "group_id")
    op.drop_table("card_groups")
