from app.quiz.schemas import Difficulty, QuestionType

DIFFICULTY_INSTRUCTIONS: dict[str, str] = {
    Difficulty.easy: (
        "Questions must test direct recall of facts explicitly stated in the text. "
        "Use simple, unambiguous language."
    ),
    Difficulty.medium: (
        "Questions must test understanding and ability to connect concepts from the text. "
        "Some inference is allowed if the answer is clearly supported by the text."
    ),
    Difficulty.hard: (
        "Questions must test deep comprehension, analysis, and synthesis of ideas from the text. "
        "Require the reader to compare, contrast, or apply concepts from the text."
    ),
}

MC_JSON_SCHEMA: dict = {
    "type": "object",
    "required": ["questions"],
    "additionalProperties": False,
    "properties": {
        "questions": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["question", "options", "correct_answer", "explanation"],
                "additionalProperties": False,
                "properties": {
                    "question": {"type": "string", "minLength": 10},
                    "options": {
                        "type": "array",
                        "items": {"type": "string"},
                        "minItems": 4,
                        "maxItems": 4,
                    },
                    "correct_answer": {"type": "string"},
                    "explanation": {"type": "string"},
                },
            },
        }
    },
}

OPEN_JSON_SCHEMA: dict = {
    "type": "object",
    "required": ["questions"],
    "additionalProperties": False,
    "properties": {
        "questions": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["question", "sample_answer", "key_points"],
                "additionalProperties": False,
                "properties": {
                    "question": {"type": "string", "minLength": 10},
                    "sample_answer": {"type": "string", "minLength": 10},
                    "key_points": {
                        "type": "array",
                        "items": {"type": "string"},
                        "minItems": 1,
                    },
                },
            },
        }
    },
}

JSON_SCHEMA_BY_TYPE: dict[str, dict] = {
    QuestionType.multiple_choice: MC_JSON_SCHEMA,
    QuestionType.open: OPEN_JSON_SCHEMA,
}
