import uuid
from enum import Enum

from pydantic import BaseModel, Field


class Difficulty(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


class QuestionType(str, Enum):
    multiple_choice = "multiple_choice"
    open = "open"


class OllamaModel(str, Enum):
    llama3 = "llama3"
    phi3_mini = "phi3:mini"
    qwen2_0_5b = "qwen2:0.5b"
    tinyllama = "tinyllama"


# ── Request schemas ────────────────────────────────────────────────────────────


class QuizGenerateRequest(BaseModel):
    text: str = Field(..., min_length=10, description="Conspect text to generate quiz from")
    num_questions: int = Field(default=5, ge=1, le=20)
    difficulty: Difficulty = Difficulty.medium
    question_type: QuestionType = QuestionType.multiple_choice
    model: OllamaModel = OllamaModel.llama3


class QuizGenerateFromCardRequest(BaseModel):
    num_questions: int = Field(default=5, ge=1, le=20)
    difficulty: Difficulty = Difficulty.medium
    question_type: QuestionType = QuestionType.multiple_choice
    model: OllamaModel = OllamaModel.llama3


# ── Question schemas ───────────────────────────────────────────────────────────


class MultipleChoiceQuestion(BaseModel):
    question: str
    options: list[str] = Field(..., min_length=4, max_length=4)
    correct_answer: str
    explanation: str


class OpenQuestion(BaseModel):
    question: str
    sample_answer: str
    key_points: list[str] = []


# ── Response schema ────────────────────────────────────────────────────────────


class QuizResponse(BaseModel):
    card_id: uuid.UUID | None = None
    num_questions: int
    difficulty: Difficulty
    question_type: QuestionType
    model: str
    questions: list[MultipleChoiceQuestion] | list[OpenQuestion]
    chunks_processed: int
