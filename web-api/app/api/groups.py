from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.repositories.group import GroupRepository
from app.services.exceptions import GroupNotFound
from app.services.schemas import GroupCreate, GroupResponse, GroupUpdate

router = APIRouter(prefix="/groups", tags=["groups"])


@router.get("", response_model=list[GroupResponse])
async def list_groups(
    session: AsyncSession = Depends(get_session),
) -> list[GroupResponse]:
    repo = GroupRepository(session)
    return await repo.get_all()  # type: ignore[return-value]


@router.post("", response_model=GroupResponse, status_code=status.HTTP_201_CREATED)
async def create_group(
    data: GroupCreate,
    session: AsyncSession = Depends(get_session),
) -> GroupResponse:
    repo = GroupRepository(session)
    return await repo.create(data)  # type: ignore[return-value]


@router.patch("/{group_id}", response_model=GroupResponse)
async def update_group(
    group_id: int,
    data: GroupUpdate,
    session: AsyncSession = Depends(get_session),
) -> GroupResponse:
    repo = GroupRepository(session)
    group = await repo.get_by_id(group_id)
    if group is None:
        raise GroupNotFound(group_id)
    return await repo.update(group, data)  # type: ignore[return-value]


@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_group(
    group_id: int,
    session: AsyncSession = Depends(get_session),
) -> None:
    repo = GroupRepository(session)
    group = await repo.get_by_id(group_id)
    if group is None:
        raise GroupNotFound(group_id)
    await repo.delete(group)
