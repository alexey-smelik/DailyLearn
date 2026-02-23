from app.quiz.llm.client import OllamaClient
from app.quiz.service import QuizService


def get_quiz_service() -> QuizService:
    return QuizService(client=OllamaClient())
