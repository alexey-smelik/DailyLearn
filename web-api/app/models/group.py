import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Group(Base):
    # Avoid SQL reserved word "groups"
    __tablename__ = "card_groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="groups")  # noqa: F821
    learning_cards: Mapped[list["LearningCard"]] = relationship(  # noqa: F821
        back_populates="group"
    )
