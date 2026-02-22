from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    last_visit: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    learning_cards: Mapped[list["LearningCard"]] = relationship(back_populates="user")  # noqa: F821
    newsletters: Mapped[list["Newsletter"]] = relationship(back_populates="user")  # noqa: F821
    groups: Mapped[list["Group"]] = relationship(back_populates="user")  # noqa: F821
