from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.newsletter import Newsletter
from app.services.schemas import NewsletterCreate, NewsletterUpdate


class NewsletterRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, newsletter_id: int) -> Newsletter | None:
        return await self._session.get(Newsletter, newsletter_id)

    async def get_all(self) -> list[Newsletter]:
        result = await self._session.execute(select(Newsletter))
        return list(result.scalars().all())

    async def create(self, data: NewsletterCreate) -> Newsletter:
        newsletter = Newsletter(**data.model_dump())
        self._session.add(newsletter)
        await self._session.flush()
        await self._session.refresh(newsletter)
        return newsletter

    async def update(self, newsletter: Newsletter, data: NewsletterUpdate) -> Newsletter:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(newsletter, field, value)
        await self._session.flush()
        await self._session.refresh(newsletter)
        return newsletter

    async def delete(self, newsletter: Newsletter) -> None:
        await self._session.delete(newsletter)
        await self._session.flush()
