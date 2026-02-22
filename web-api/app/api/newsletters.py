from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.repositories.newsletter import NewsletterRepository
from app.services.exceptions import NewsletterNotFound
from app.services.schemas import NewsletterCreate, NewsletterResponse, NewsletterUpdate

router = APIRouter(prefix="/newsletters", tags=["newsletters"])


@router.get("", response_model=list[NewsletterResponse])
async def list_newsletters(
    session: AsyncSession = Depends(get_session),
) -> list[NewsletterResponse]:
    repo = NewsletterRepository(session)
    return await repo.get_all()  # type: ignore[return-value]


@router.post("", response_model=NewsletterResponse, status_code=status.HTTP_201_CREATED)
async def create_newsletter(
    data: NewsletterCreate,
    session: AsyncSession = Depends(get_session),
) -> NewsletterResponse:
    repo = NewsletterRepository(session)
    return await repo.create(data)  # type: ignore[return-value]


@router.get("/{newsletter_id}", response_model=NewsletterResponse)
async def get_newsletter(
    newsletter_id: int,
    session: AsyncSession = Depends(get_session),
) -> NewsletterResponse:
    repo = NewsletterRepository(session)
    newsletter = await repo.get_by_id(newsletter_id)
    if newsletter is None:
        raise NewsletterNotFound(newsletter_id)
    return newsletter  # type: ignore[return-value]


@router.patch("/{newsletter_id}", response_model=NewsletterResponse)
async def update_newsletter(
    newsletter_id: int,
    data: NewsletterUpdate,
    session: AsyncSession = Depends(get_session),
) -> NewsletterResponse:
    repo = NewsletterRepository(session)
    newsletter = await repo.get_by_id(newsletter_id)
    if newsletter is None:
        raise NewsletterNotFound(newsletter_id)
    return await repo.update(newsletter, data)  # type: ignore[return-value]


@router.delete("/{newsletter_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_newsletter(
    newsletter_id: int,
    session: AsyncSession = Depends(get_session),
) -> None:
    repo = NewsletterRepository(session)
    newsletter = await repo.get_by_id(newsletter_id)
    if newsletter is None:
        raise NewsletterNotFound(newsletter_id)
    await repo.delete(newsletter)
