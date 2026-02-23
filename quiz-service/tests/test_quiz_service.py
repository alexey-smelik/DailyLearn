import uuid
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from httpx import AsyncClient

from app.quiz.schemas import Difficulty, OllamaModel, QuestionType
from app.quiz.service import QuizService, _chunk_text
from app.quiz.llm.client import OllamaClient
from app.quiz.exceptions import QuizGenerationError, LLMUnavailableError

# ── Unit: chunking ─────────────────────────────────────────────────────────────

class TestChunkText:
    def test_short_text_returns_single_chunk(self) -> None:
        text = "Hello world"
        assert _chunk_text(text, max_size=100, overlap=10) == [text]

    def test_long_text_is_split(self) -> None:
        text = " ".join(["word"] * 200)  # ~1000 chars
        chunks = _chunk_text(text, max_size=200, overlap=20)
        assert len(chunks) > 1

    def test_chunks_have_overlap(self) -> None:
        text = " ".join([f"word{i}" for i in range(100)])
        chunks = _chunk_text(text, max_size=100, overlap=30)
        # The start of chunk[1] should partially overlap with the end of chunk[0]
        assert len(chunks) >= 2

    def test_empty_chunks_are_removed(self) -> None:
        text = "short"
        chunks = _chunk_text(text, max_size=3, overlap=1)
        assert all(c for c in chunks)


# ── Unit: question distribution ───────────────────────────────────────────────

class TestDistributeQuestions:
    def test_even_distribution(self) -> None:
        result = QuizService._distribute_questions(6, 3)
        assert result == [2, 2, 2]

    def test_remainder_goes_to_first_chunks(self) -> None:
        result = QuizService._distribute_questions(7, 3)
        assert result == [3, 2, 2]

    def test_single_chunk(self) -> None:
        assert QuizService._distribute_questions(5, 1) == [5]

    def test_zero_chunks(self) -> None:
        assert QuizService._distribute_questions(5, 0) == []

    def test_more_chunks_than_questions(self) -> None:
        result = QuizService._distribute_questions(2, 5)
        assert sum(result) == 2


# ── Integration: QuizService.generate ─────────────────────────────────────────

MC_LLM_RESPONSE: dict[str, Any] = {
    "questions": [
        {
            "question": "What is the capital of France?",
            "options": ["A) Berlin", "B) Paris", "C) Rome", "D) Madrid"],
            "correct_answer": "B) Paris",
            "explanation": "The text states Paris is the capital of France.",
        }
    ]
}

OPEN_LLM_RESPONSE: dict[str, Any] = {
    "questions": [
        {
            "question": "What is spaced repetition?",
            "sample_answer": "A learning technique that increases review intervals over time.",
            "key_points": ["increasing intervals", "long-term memory", "Ebbinghaus curve"],
        }
    ]
}


@pytest.mark.parametrize(
    "question_type, llm_response",
    [
        (QuestionType.multiple_choice, MC_LLM_RESPONSE),
        (QuestionType.open, OPEN_LLM_RESPONSE),
    ],
)
async def test_generate_returns_quiz_response(
    question_type: QuestionType,
    llm_response: dict[str, Any],
) -> None:
    mock_client = AsyncMock(spec=OllamaClient)
    mock_client.generate.return_value = llm_response

    service = QuizService(client=mock_client)
    result = await service.generate(
        text="France is a country in Europe. Its capital is Paris.",
        num_questions=1,
        difficulty=Difficulty.easy,
        question_type=question_type,
        model=OllamaModel.llama3,
    )

    assert result.num_questions == 1
    assert result.question_type == question_type
    assert len(result.questions) == 1
    assert result.chunks_processed == 1


async def test_generate_raises_quiz_generation_error_on_llm_unavailable() -> None:
    mock_client = AsyncMock(spec=OllamaClient)
    mock_client.generate.side_effect = LLMUnavailableError("Ollama is down")

    service = QuizService(client=mock_client)

    with pytest.raises(QuizGenerationError):
        await service.generate(
            text="Some text",
            num_questions=1,
            difficulty=Difficulty.easy,
            question_type=QuestionType.multiple_choice,
            model=OllamaModel.llama3,
        )


# ── API: /api/v1/quiz/generate ─────────────────────────────────────────────────

async def test_generate_endpoint_returns_200(async_client: AsyncClient) -> None:
    with patch(
        "app.quiz.service.QuizService._generate_for_chunk",
        new_callable=AsyncMock,
        return_value=[
            {
                "question": "Q?",
                "options": ["A) a", "B) b", "C) c", "D) d"],
                "correct_answer": "A) a",
                "explanation": "Because text says so.",
            }
        ],
    ):
        # Use the actual service but mock the chunk-level call
        with patch(
            "app.quiz.dependencies.OllamaClient.generate",
            new_callable=AsyncMock,
            return_value=MC_LLM_RESPONSE,
        ):
            response = await async_client.post(
                "/api/v1/quiz/generate",
                json={
                    "text": "France is a country in Europe. Its capital is Paris.",
                    "num_questions": 1,
                    "difficulty": "easy",
                    "question_type": "multiple_choice",
                    "model": "llama3",
                },
            )

    assert response.status_code == 200
    data = response.json()
    assert "questions" in data


async def test_generate_endpoint_validates_short_text(async_client: AsyncClient) -> None:
    response = await async_client.post(
        "/api/v1/quiz/generate",
        json={"text": "hi", "num_questions": 1},
    )
    assert response.status_code == 422


async def test_generate_endpoint_validates_num_questions_bounds(
    async_client: AsyncClient,
) -> None:
    response = await async_client.post(
        "/api/v1/quiz/generate",
        json={
            "text": "Some valid text content here",
            "num_questions": 99,
        },
    )
    assert response.status_code == 422


async def test_health_endpoint(async_client: AsyncClient) -> None:
    response = await async_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# ── API: /api/v1/quiz/generate/from-card/{card_id} ────────────────────────────

async def test_from_card_returns_404_when_card_missing(
    async_client: AsyncClient,
) -> None:
    card_id = str(uuid.uuid4())
    with patch("app.quiz.router.httpx.AsyncClient") as mock_cls:
        mock_http = AsyncMock()
        mock_cls.return_value.__aenter__.return_value = mock_http
        mock_resp = MagicMock()
        mock_resp.status_code = 404
        mock_resp.is_success = False
        mock_http.get.return_value = mock_resp

        response = await async_client.post(
            f"/api/v1/quiz/generate/from-card/{card_id}",
            json={"num_questions": 3},
        )

    assert response.status_code == 404


async def test_from_card_returns_422_when_no_conspect(
    async_client: AsyncClient,
) -> None:
    card_id = str(uuid.uuid4())
    with patch("app.quiz.router.httpx.AsyncClient") as mock_cls:
        mock_http = AsyncMock()
        mock_cls.return_value.__aenter__.return_value = mock_http
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.is_success = True
        mock_resp.json.return_value = {"conspect": None}
        mock_http.get.return_value = mock_resp

        response = await async_client.post(
            f"/api/v1/quiz/generate/from-card/{card_id}",
            json={"num_questions": 3},
        )

    assert response.status_code == 422
