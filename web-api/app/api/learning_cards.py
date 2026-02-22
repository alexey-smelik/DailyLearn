import uuid

import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_session
from app.repositories.learning_card import LearningCardRepository
from app.services.exceptions import LearningCardNotFound
from app.services.schemas import LearningCardCreate, LearningCardResponse, LearningCardUpdate

router = APIRouter(prefix="/learning-cards", tags=["learning-cards"])


@router.get("", response_model=list[LearningCardResponse])
async def list_learning_cards(
    session: AsyncSession = Depends(get_session),
) -> list[LearningCardResponse]:
    repo = LearningCardRepository(session)
    return await repo.get_all()  # type: ignore[return-value]


@router.post("", response_model=LearningCardResponse, status_code=status.HTTP_201_CREATED)
async def create_learning_card(
    data: LearningCardCreate,
    session: AsyncSession = Depends(get_session),
) -> LearningCardResponse:
    repo = LearningCardRepository(session)
    return await repo.create(data)  # type: ignore[return-value]


@router.get("/{card_id}", response_model=LearningCardResponse)
async def get_learning_card(
    card_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
) -> LearningCardResponse:
    repo = LearningCardRepository(session)
    card = await repo.get_by_id(card_id)
    if card is None:
        raise LearningCardNotFound(card_id)
    return card  # type: ignore[return-value]


@router.patch("/{card_id}", response_model=LearningCardResponse)
async def update_learning_card(
    card_id: uuid.UUID,
    data: LearningCardUpdate,
    session: AsyncSession = Depends(get_session),
) -> LearningCardResponse:
    repo = LearningCardRepository(session)
    card = await repo.get_by_id(card_id)
    if card is None:
        raise LearningCardNotFound(card_id)
    return await repo.update(card, data)  # type: ignore[return-value]


@router.post("/{card_id}/toggle", response_model=LearningCardResponse)
async def toggle_learning_card(
    card_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
) -> LearningCardResponse:
    repo = LearningCardRepository(session)
    card = await repo.get_by_id(card_id)
    if card is None:
        raise LearningCardNotFound(card_id)
    return await repo.toggle(card)  # type: ignore[return-value]


@router.post("/{card_id}/test-send", status_code=status.HTTP_200_OK)
async def test_send_learning_card(
    card_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
) -> dict[str, bool]:
    repo = LearningCardRepository(session)
    card = await repo.get_by_id(card_id)
    if card is None:
        raise LearningCardNotFound(card_id)
    if not card.tg_chat_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Card has no tg_chat_id configured",
        )
    payload = {
        "tg_chat_id": card.tg_chat_id,
        "tg_topic_id": card.tg_topic_id,
        "card_id": str(card.id),
        "card_name": card.name,
        "source_url": card.source_url,
        "schedule": card.schedule,
        "message_template": card.message_template,
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{settings.tg_tool_url}/send", json=payload, timeout=10)
    if not resp.is_success:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"tg-tool error: {resp.text}",
        )
    return {"ok": True}


@router.delete("/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_learning_card(
    card_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
) -> None:
    repo = LearningCardRepository(session)
    card = await repo.get_by_id(card_id)
    if card is None:
        raise LearningCardNotFound(card_id)
    await repo.delete(card)
