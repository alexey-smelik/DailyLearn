import uuid
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.models.base import Base


class LearningCard(Base):
    __tablename__ = "learning_cards"

    id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    source_url: Mapped[str | None] = mapped_column(sa.Text, nullable=True)
    schedule: Mapped[str | None] = mapped_column(sa.Text, nullable=True)
    tg_chat_id: Mapped[str | None] = mapped_column(sa.String(255), nullable=True)
    tg_topic_id: Mapped[int | None] = mapped_column(sa.Integer, nullable=True)
    message_template: Mapped[str | None] = mapped_column(sa.Text, nullable=True)
    add_date: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    group_id: Mapped[int | None] = mapped_column(
        sa.ForeignKey("card_groups.id", ondelete="SET NULL"), nullable=True
    )
    is_active: Mapped[bool] = mapped_column(sa.Boolean, nullable=False, server_default=sa.true())
    show_pause_button: Mapped[bool] = mapped_column(sa.Boolean, nullable=False, server_default=sa.true())
    show_skip_button: Mapped[bool] = mapped_column(sa.Boolean, nullable=False, server_default=sa.true())
    show_quiz_button: Mapped[bool] = mapped_column(sa.Boolean, nullable=False, server_default=sa.false())
    time_to_educate: Mapped[str | None] = mapped_column(sa.Text, nullable=True)
    conspect: Mapped[str | None] = mapped_column(sa.Text, nullable=True)
    conspect_requested: Mapped[bool] = mapped_column(sa.Boolean, nullable=False, server_default=sa.false())
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id"), nullable=False)

    group: Mapped["Group | None"] = relationship(back_populates="learning_cards")  # noqa: F821
    user: Mapped["User"] = relationship(back_populates="learning_cards")  # noqa: F821
    newsletters: Mapped[list["Newsletter"]] = relationship(  # noqa: F821
        back_populates="learning_card",
        passive_deletes=True,
    )
