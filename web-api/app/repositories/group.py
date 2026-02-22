from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.group import Group
from app.services.schemas import GroupCreate, GroupUpdate


class GroupRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, group_id: int) -> Group | None:
        return await self._session.get(Group, group_id)

    async def get_all(self) -> list[Group]:
        result = await self._session.execute(select(Group))
        return list(result.scalars().all())

    async def create(self, data: GroupCreate) -> Group:
        group = Group(**data.model_dump())
        self._session.add(group)
        await self._session.flush()
        await self._session.refresh(group)
        return group

    async def update(self, group: Group, data: GroupUpdate) -> Group:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(group, field, value)
        await self._session.flush()
        await self._session.refresh(group)
        return group

    async def delete(self, group: Group) -> None:
        await self._session.delete(group)
        await self._session.flush()
