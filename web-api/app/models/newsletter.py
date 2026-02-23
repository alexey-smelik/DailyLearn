import uuid
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Newsletter(Base):
    __tablename__ = "newsletters"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id"), nullable=False)
    learning_card_id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(as_uuid=True),
        sa.ForeignKey("learning_cards.id", ondelete="CASCADE"),
        nullable=False,
    )
    send_date: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), nullable=False)

    user: Mapped["User"] = relationship(back_populates="newsletters")  # noqa: F821
    learning_card: Mapped["LearningCard"] = relationship(back_populates="newsletters")  # noqa: F821
