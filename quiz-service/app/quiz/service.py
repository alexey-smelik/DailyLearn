import logging
import math
import uuid

from app.config import settings
from app.quiz.exceptions import (
    LLMResponseParseError,
    LLMSchemaValidationError,
    LLMUnavailableError,
    QuizGenerationError,
)
from app.quiz.llm.client import OllamaClient
from app.quiz.llm.parser import validate_and_parse
from app.quiz.llm.prompts import build_prompt
from app.quiz.schemas import (
    Difficulty,
    MultipleChoiceQuestion,
    OllamaModel,
    OpenQuestion,
    QuestionType,
    QuizResponse,
)

logger = logging.getLogger(__name__)


def _chunk_text(text: str, max_size: int, overlap: int) -> list[str]:
    """Split text into overlapping chunks without breaking words."""
    if len(text) <= max_size:
        return [text]

    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = start + max_size
        if end < len(text):
            # Walk back to nearest whitespace to avoid splitting mid-word
            boundary = text.rfind(" ", start, end)
            if boundary > start:
                end = boundary
        chunks.append(text[start:end].strip())
        start = end - overlap
    return [c for c in chunks if c]


class QuizService:
    def __init__(self, client: OllamaClient) -> None:
        self._client = client

    async def generate(
        self,
        text: str,
        num_questions: int,
        difficulty: Difficulty,
        question_type: QuestionType,
        model: OllamaModel,
        card_id: uuid.UUID | None = None,
    ) -> QuizResponse:
        chunks = _chunk_text(
            text,
            max_size=settings.max_chunk_size,
            overlap=settings.chunk_overlap,
        )
        logger.info(
            "Generating quiz: chunks=%d total_chars=%d num_questions=%d "
            "difficulty=%s type=%s model=%s",
            len(chunks),
            len(text),
            num_questions,
            difficulty,
            question_type,
            model,
        )

        all_questions: list[MultipleChoiceQuestion | OpenQuestion] = []
        questions_per_chunk = self._distribute_questions(num_questions, len(chunks))

        for idx, (chunk, q_count) in enumerate(zip(chunks, questions_per_chunk)):
            if q_count == 0:
                continue
            logger.debug("Processing chunk %d/%d (%d questions)", idx + 1, len(chunks), q_count)
            questions = await self._generate_for_chunk(
                chunk, q_count, difficulty, question_type, model.value
            )
            all_questions.extend(questions)

        # Trim to exact requested count in case of rounding
        all_questions = all_questions[:num_questions]

        return QuizResponse(
            card_id=card_id,
            num_questions=len(all_questions),
            difficulty=difficulty,
            question_type=question_type,
            model=model.value,
            questions=all_questions,  # type: ignore[arg-type]
            chunks_processed=len(chunks),
        )

    async def _generate_for_chunk(
        self,
        text: str,
        num_questions: int,
        difficulty: Difficulty,
        question_type: QuestionType,
        model: str,
    ) -> list[MultipleChoiceQuestion | OpenQuestion]:
        prompt = build_prompt(text, num_questions, difficulty, question_type)
        try:
            raw = await self._client.generate(model=model, prompt=prompt)
        except LLMUnavailableError as exc:
            raise QuizGenerationError(f"LLM unavailable: {exc}") from exc
        except LLMResponseParseError as exc:
            raise QuizGenerationError(f"LLM returned invalid JSON: {exc}") from exc

        try:
            return validate_and_parse(raw, question_type)  # type: ignore[return-value]
        except LLMSchemaValidationError as exc:
            raise QuizGenerationError(f"LLM output failed schema validation: {exc}") from exc

    @staticmethod
    def _distribute_questions(total: int, num_chunks: int) -> list[int]:
        """Distribute total questions across chunks as evenly as possible."""
        if num_chunks == 0:
            return []
        base = total // num_chunks
        remainder = total % num_chunks
        return [base + (1 if i < remainder else 0) for i in range(num_chunks)]
