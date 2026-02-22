import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.learning_card import LearningCard
from app.services.schemas import LearningCardCreate, LearningCardUpdate


class LearningCardRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, card_id: uuid.UUID) -> LearningCard | None:
        return await self._session.get(LearningCard, card_id)

    async def get_all(self) -> list[LearningCard]:
        result = await self._session.execute(select(LearningCard))
        return list(result.scalars().all())

    async def create(self, data: LearningCardCreate) -> LearningCard:
        card = LearningCard(**data.model_dump())
        self._session.add(card)
        await self._session.flush()
        await self._session.refresh(card)
        return card

    async def update(self, card: LearningCard, data: LearningCardUpdate) -> LearningCard:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(card, field, value)
        await self._session.flush()
        await self._session.refresh(card)
        return card

    async def toggle(self, card: LearningCard) -> LearningCard:
        card.is_active = not card.is_active
        await self._session.flush()
        await self._session.refresh(card)
        return card

    async def delete(self, card: LearningCard) -> None:
        await self._session.delete(card)
        await self._session.flush()
