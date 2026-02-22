from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.repositories.user import UserRepository
from app.services.exceptions import UserNotFound
from app.services.schemas import UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserResponse])
async def list_users(session: AsyncSession = Depends(get_session)) -> list[UserResponse]:
    repo = UserRepository(session)
    return await repo.get_all()  # type: ignore[return-value]


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserCreate,
    session: AsyncSession = Depends(get_session),
) -> UserResponse:
    repo = UserRepository(session)
    return await repo.create(data)  # type: ignore[return-value]


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
) -> UserResponse:
    repo = UserRepository(session)
    user = await repo.get_by_id(user_id)
    if user is None:
        raise UserNotFound(user_id)
    return user  # type: ignore[return-value]


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    data: UserUpdate,
    session: AsyncSession = Depends(get_session),
) -> UserResponse:
    repo = UserRepository(session)
    user = await repo.get_by_id(user_id)
    if user is None:
        raise UserNotFound(user_id)
    return await repo.update(user, data)  # type: ignore[return-value]


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
) -> None:
    repo = UserRepository(session)
    user = await repo.get_by_id(user_id)
    if user is None:
        raise UserNotFound(user_id)
    await repo.delete(user)
