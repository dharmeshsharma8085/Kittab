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
# FLASHCARD GENERATOR
# ============================================================

class FlashcardGenerator:
    """
    Generate study flashcards from Kittab RAG context.
    """

    def __init__(
        self,
        retriever: Retriever = None,
        top_k: int = 5
    ):

        print(
            "\nInitializing Flashcard Generator..."
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
            "Flashcard Generator initialized successfully."
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
    # GENERATE FLASHCARDS
    # ========================================================

    def generate_flashcards(
        self,
        topic: str,
        num_cards: int = 10,
        difficulty: str = "medium"
    ) -> dict:
        """
        Generate flashcards from retrieved study material.
        """

        if not isinstance(
            topic,
            str
        ):
            raise TypeError(
                "Topic must be a string."
            )

        topic = topic.strip()

        if not topic:
            raise ValueError(
                "Topic cannot be empty."
            )

        if num_cards < 1:
            raise ValueError(
                "num_cards must be at least 1."
            )

        allowed_difficulties = {
            "easy",
            "medium",
            "hard"
        }

        difficulty = (
            difficulty
            .lower()
            .strip()
        )

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
                "flashcards": [],
                "message": (
                    "I couldn't find enough information "
                    "in the provided material."
                )
            }

        # ----------------------------------------------------
        # Prompt
        # ----------------------------------------------------

        prompt = f"""
You are Kittab, an AI study flashcard generator.

Create flashcards ONLY from the provided study material.

Topic:
{topic}

Difficulty:
{difficulty}

Number of flashcards:
{num_cards}

IMPORTANT RULES:

1. Use ONLY information present in the context.
2. Do not invent facts or information.
3. Focus on important concepts, definitions,
   processes, formulas, and relationships.
4. Questions should test understanding.
5. Answers should be concise but complete.
6. Avoid duplicate flashcards.
7. Keep each flashcard focused on one concept.
8. Do not include information unrelated to the topic.
9. Return ONLY valid JSON.
10. Do not use Markdown code fences.

Return exactly this structure:

{{
    "topic": "{topic}",
    "difficulty": "{difficulty}",
    "flashcards": [
        {{
            "question": "Question",
            "answer": "Answer"
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
            "\nGenerating flashcards with Gemini..."
        )

        try:

            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )

        except Exception as exc:

            raise RuntimeError(
                "Gemini flashcard generation failed:\n"
                f"{exc}"
            ) from exc

        if not response.text:

            raise RuntimeError(
                "Gemini returned an empty response."
            )

        raw_text = response.text.strip()

        # ----------------------------------------------------
        # Remove accidental Markdown fences
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

            flashcards = json.loads(
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

        if "flashcards" not in flashcards:

            flashcards["flashcards"] = []

        print(
            "\nFlashcards generated successfully."
        )

        return flashcards