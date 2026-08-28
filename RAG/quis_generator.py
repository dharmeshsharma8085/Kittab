import os
import json

from dotenv import load_dotenv
from google import genai

from retriever import Retriever


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# GEMINI CONFIGURATION
# ============================================================

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.7-flash"
)

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not set in .env"
    )


client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ============================================================
# TEST GENERATOR
# ============================================================

class TestGenerator:
    """
    Generate educational tests from Kittab RAG context.
    """

    def __init__(
        self,
        retriever: Retriever = None,
        top_k: int = 5
    ):

        print(
            "\nInitializing Test Generator..."
        )

        self.retriever = (
            retriever
            if retriever is not None
            else Retriever()
        )

        self.top_k = top_k

        print(
            f"Gemini model: {GEMINI_MODEL}"
        )

        print(
            "Test Generator initialized successfully."
        )

    # ========================================================
    # GET CONTEXT
    # ========================================================

    def _get_context(
        self,
        topic: str
    ) -> str:

        results = self.retriever.retrieve(
            query=topic,
            n_results=self.top_k
        )

        if not results:
            return ""

        context_parts = []

        for i, result in enumerate(
            results,
            start=1
        ):

            context_parts.append(
                f"[Context {i}]\n"
                f"{result['text']}"
            )

        return "\n\n".join(
            context_parts
        )

    # ========================================================
    # GENERATE TEST
    # ========================================================

    def generate_test(
        self,
        topic: str,
        num_mcq: int = 5,
        num_short: int = 3,
        difficulty: str = "medium"
    ) -> dict:

        if not topic.strip():
            raise ValueError(
                "Topic cannot be empty."
            )

        if num_mcq < 0:
            raise ValueError(
                "num_mcq cannot be negative."
            )

        if num_short < 0:
            raise ValueError(
                "num_short cannot be negative."
            )

        if num_mcq == 0 and num_short == 0:
            raise ValueError(
                "At least one question is required."
            )

        allowed_difficulties = {
            "easy",
            "medium",
            "hard"
        }

        difficulty = difficulty.lower().strip()

        if difficulty not in allowed_difficulties:
            raise ValueError(
                "Difficulty must be easy, medium, or hard."
            )

        # ----------------------------------------------------
        # Retrieve context
        # ----------------------------------------------------

        print(
            "\nRetrieving study material..."
        )

        context = self._get_context(
            topic
        )

        if not context:

            return {
                "topic": topic,
                "difficulty": difficulty,
                "mcqs": [],
                "short_questions": [],
                "message": (
                    "I couldn't find enough information "
                    "in the provided material."
                )
            }

        # ----------------------------------------------------
        # Prompt
        # ----------------------------------------------------

        prompt = f"""
You are Kittab, an AI study-test generator.

Create a test ONLY from the provided study material.

Topic:
{topic}

Difficulty:
{difficulty}

Number of MCQs:
{num_mcq}

Number of short-answer questions:
{num_short}

IMPORTANT RULES:

1. Use ONLY information present in the context.
2. Do not invent facts.
3. Do not ask questions unrelated to the topic.
4. MCQs must have exactly 4 options.
5. Every MCQ must have one correct answer.
6. Include a short explanation for every MCQ.
7. Short-answer questions should test understanding.
8. Do not reveal answers inside the question.
9. Keep questions clear and educational.
10. Return ONLY valid JSON.
11. Do not use Markdown code fences.

Return exactly this structure:

{{
    "topic": "{topic}",
    "difficulty": "{difficulty}",
    "mcqs": [
        {{
            "question": "Question text",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "answer": "Correct option",
            "explanation": "Why this answer is correct."
        }}
    ],
    "short_questions": [
        {{
            "question": "Question text",
            "answer": "Expected answer"
        }}
    ]
}}

STUDY MATERIAL:

{context}
"""

        # ----------------------------------------------------
        # Gemini
        # ----------------------------------------------------

        print(
            "\nGenerating test with Gemini..."
        )

        try:

            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )

        except Exception as exc:

            raise RuntimeError(
                f"Gemini test generation failed:\n"
                f"{exc}"
            ) from exc

        if not response.text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        raw_text = response.text.strip()

        # ----------------------------------------------------
        # Remove accidental code fences
        # ----------------------------------------------------

        if raw_text.startswith(
            "```"
        ):

            raw_text = (
                raw_text
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

        # ----------------------------------------------------
        # Parse JSON
        # ----------------------------------------------------

        try:

            test = json.loads(
                raw_text
            )

        except json.JSONDecodeError as exc:

            raise RuntimeError(
                "Gemini returned invalid JSON.\n"
                f"Response:\n{raw_text}"
            ) from exc

        # ----------------------------------------------------
        # Validate structure
        # ----------------------------------------------------

        if "mcqs" not in test:
            test["mcqs"] = []

        if "short_questions" not in test:
            test["short_questions"] = []

        print(
            "\nTest generated successfully."
        )

        return test