import uuid
import logging

import httpx
from fastapi import APIRouter, Depends, status

from app.config import settings
from app.quiz.dependencies import get_quiz_service
from app.quiz.exceptions import CardHasNoConspectError, CardNotFoundError, QuizGenerationError
from app.quiz.schemas import QuizGenerateFromCardRequest, QuizGenerateRequest, QuizResponse
from app.quiz.service import QuizService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/quiz", tags=["quiz"])


@router.post(
    "/generate",
    response_model=QuizResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate a quiz from raw text",
)
async def generate_quiz(
    body: QuizGenerateRequest,
    service: QuizService = Depends(get_quiz_service),
) -> QuizResponse:
    return await service.generate(
        text=body.text,
        num_questions=body.num_questions,
        difficulty=body.difficulty,
        question_type=body.question_type,
        model=body.model,
    )


@router.post(
    "/generate/from-card/{card_id}",
    response_model=QuizResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate a quiz from a card's conspect",
)
async def generate_quiz_from_card(
    card_id: uuid.UUID,
    body: QuizGenerateFromCardRequest,
    service: QuizService = Depends(get_quiz_service),
) -> QuizResponse:
    card_id_str = str(card_id)

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.get(
                f"{settings.web_api_url}/api/v1/learning-cards/{card_id_str}"
            )
        except httpx.TransportError as exc:
            logger.error("web-api unreachable: %s", exc)
            raise QuizGenerationError("web-api is unreachable") from exc

    if resp.status_code == 404:
        raise CardNotFoundError(card_id_str)
    if not resp.is_success:
        raise QuizGenerationError(f"web-api returned HTTP {resp.status_code}")

    card = resp.json()
    conspect: str | None = card.get("conspect")

    if not conspect or not conspect.strip():
        raise CardHasNoConspectError(card_id_str)

    return await service.generate(
        text=conspect,
        num_questions=body.num_questions,
        difficulty=body.difficulty,
        question_type=body.question_type,
        model=body.model,
        card_id=card_id,
    )
