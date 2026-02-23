from app.quiz.schemas import Difficulty, QuestionType
from app.quiz.constants import DIFFICULTY_INSTRUCTIONS

_MC_TEMPLATE = """\
You are a strict quiz generator. Your ONLY source of knowledge is the TEXT provided below.
Do NOT use any information outside of the provided TEXT.
Do NOT invent facts, examples, or explanations that are not present in the TEXT.

Generate exactly {num_questions} multiple-choice questions from the TEXT.

Difficulty rules: {difficulty_instruction}

Requirements for each question:
- "question": a clear, specific question answerable from the TEXT
- "options": exactly 4 strings, each prefixed with "A) ", "B) ", "C) ", "D) "
- "correct_answer": must be the FULL string of the correct option (e.g. "A) ...")
- "explanation": one sentence citing where in the TEXT the answer comes from

Respond ONLY with a valid JSON object. No markdown, no extra text.

JSON schema:
{{
  "questions": [
    {{
      "question": "...",
      "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
      "correct_answer": "A) ...",
      "explanation": "..."
    }}
  ]
}}

TEXT:
{text}
"""

_OPEN_TEMPLATE = """\
You are a strict quiz generator. Your ONLY source of knowledge is the TEXT provided below.
Do NOT use any information outside of the provided TEXT.
Do NOT invent facts, examples, or explanations that are not present in the TEXT.

Generate exactly {num_questions} open-ended questions from the TEXT.

Difficulty rules: {difficulty_instruction}

Requirements for each question:
- "question": a clear, specific question answerable from the TEXT
- "sample_answer": a model answer written ONLY using information from the TEXT
- "key_points": 2–5 key points from the TEXT that a good answer must cover

Respond ONLY with a valid JSON object. No markdown, no extra text.

JSON schema:
{{
  "questions": [
    {{
      "question": "...",
      "sample_answer": "...",
      "key_points": ["...", "..."]
    }}
  ]
}}

TEXT:
{text}
"""

_TEMPLATES: dict[str, str] = {
    QuestionType.multiple_choice: _MC_TEMPLATE,
    QuestionType.open: _OPEN_TEMPLATE,
}


def build_prompt(
    text: str,
    num_questions: int,
    difficulty: Difficulty,
    question_type: QuestionType,
) -> str:
    template = _TEMPLATES[question_type]
    return template.format(
        num_questions=num_questions,
        difficulty_instruction=DIFFICULTY_INSTRUCTIONS[difficulty],
        text=text,
    )
