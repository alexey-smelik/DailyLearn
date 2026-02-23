import logging
from typing import Any

import jsonschema

from app.quiz.constants import JSON_SCHEMA_BY_TYPE
from app.quiz.exceptions import LLMSchemaValidationError
from app.quiz.schemas import (
    MultipleChoiceQuestion,
    OpenQuestion,
    QuestionType,
)

logger = logging.getLogger(__name__)

_MC_ITEM_SCHEMA: dict = {
    "type": "object",
    "required": ["question", "options", "correct_answer", "explanation"],
    "properties": {
        "question": {"type": "string"},
        "options": {"type": "array", "minItems": 2},
        "correct_answer": {"type": "string"},
        "explanation": {"type": "string"},
    },
}

_OPEN_ITEM_SCHEMA: dict = {
    "type": "object",
    "required": ["question", "sample_answer"],
    "properties": {
        "question": {"type": "string"},
        "sample_answer": {"type": "string"},
        "key_points": {"type": "array"},
    },
}


def validate_and_parse(
    raw: dict[str, Any],
    question_type: QuestionType,
) -> list[MultipleChoiceQuestion] | list[OpenQuestion]:
    """Validate LLM output against JSON schema and convert to Pydantic models.

    Top-level structure is validated strictly. Individual questions that fail
    validation are skipped with a warning rather than rejecting the whole batch.
    """
    schema = JSON_SCHEMA_BY_TYPE[question_type]
    try:
        jsonschema.validate(instance=raw, schema=schema)
    except jsonschema.ValidationError as exc:
        # Try to recover: if the payload has a 'questions' list at all, attempt
        # item-level parsing below; otherwise re-raise.
        if not isinstance(raw.get("questions"), list) or not raw["questions"]:
            raise LLMSchemaValidationError(
                f"LLM output schema mismatch: {exc.message}"
            ) from exc
        logger.warning("Top-level schema validation failed, attempting item recovery: %s", exc.message)

    questions_raw: list[dict[str, Any]] = raw.get("questions", [])

    if question_type == QuestionType.multiple_choice:
        item_schema = _MC_ITEM_SCHEMA
        parsed: list[MultipleChoiceQuestion] = []
        for idx, item in enumerate(questions_raw):
            try:
                jsonschema.validate(instance=item, schema=item_schema)
            except jsonschema.ValidationError as exc:
                logger.warning("Skipping MC question %d — schema error: %s", idx, exc.message)
                continue
            # Ensure correct_answer is one of the options (exact or substring match)
            opts = item["options"]
            ans = item["correct_answer"]
            if ans not in opts:
                # Try to find a matching option by content (model may omit prefix)
                match = next((o for o in opts if ans in o or o in ans), None)
                if match:
                    item = {**item, "correct_answer": match}
                else:
                    logger.warning(
                        "Skipping MC question %d — correct_answer '%s' not in options %s",
                        idx, ans, opts,
                    )
                    continue
            # Normalise options to exactly 4 (pad or trim)
            while len(item["options"]) < 4:
                item["options"].append("—")
            item["options"] = item["options"][:4]
            parsed.append(MultipleChoiceQuestion(**item))
        if not parsed:
            raise LLMSchemaValidationError("No valid questions could be parsed from LLM output")
        return parsed

    parsed_open: list[OpenQuestion] = []
    item_schema_open = _OPEN_ITEM_SCHEMA
    for idx, item in enumerate(questions_raw):
        try:
            jsonschema.validate(instance=item, schema=item_schema_open)
        except jsonschema.ValidationError as exc:
            logger.warning("Skipping open question %d — schema error: %s", idx, exc.message)
            continue
        if isinstance(item.get("key_points"), str):
            item = {**item, "key_points": [item["key_points"]]}
        elif not item.get("key_points"):
            item = {**item, "key_points": []}
        parsed_open.append(OpenQuestion(**item))
    if not parsed_open:
        raise LLMSchemaValidationError("No valid questions could be parsed from LLM output")
    return parsed_open
