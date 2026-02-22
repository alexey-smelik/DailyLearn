from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.services.schemas import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, user_id: int) -> User | None:
        return await self._session.get(User, user_id)

    async def get_all(self) -> list[User]:
        result = await self._session.execute(select(User))
        return list(result.scalars().all())

    async def create(self, data: UserCreate) -> User:
        user = User(**data.model_dump())
        self._session.add(user)
        await self._session.flush()
        await self._session.refresh(user)
        return user

    async def update(self, user: User, data: UserUpdate) -> User:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)
        await self._session.flush()
        await self._session.refresh(user)
        return user

    async def delete(self, user: User) -> None:
        await self._session.delete(user)
        await self._session.flush()
