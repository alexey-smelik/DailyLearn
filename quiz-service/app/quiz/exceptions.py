from fastapi import HTTPException, status


class LLMUnavailableError(Exception):
    """Raised when Ollama is unreachable or returns a server error."""


class LLMResponseParseError(Exception):
    """Raised when the LLM response cannot be parsed as valid JSON."""


class LLMSchemaValidationError(Exception):
    """Raised when parsed JSON does not match expected schema."""


class CardNotFoundError(HTTPException):
    def __init__(self, card_id: str) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Learning card '{card_id}' not found",
        )


class CardHasNoConspectError(HTTPException):
    def __init__(self, card_id: str) -> None:
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Learning card '{card_id}' has no conspect text",
        )


class QuizGenerationError(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Quiz generation failed: {detail}",
        )
