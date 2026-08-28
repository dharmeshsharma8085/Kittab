import os

from dotenv import load_dotenv
from google import genai


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# GEMINI CONFIGURATION
# ============================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not set in .env"
    )


GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.7-flash"
)


# Create Gemini client
client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ============================================================
# GEMINI GENERATION
# ============================================================

def generate_response(
    system_prompt: str,
    text: str
) -> str:
    """
    Send text to Gemini with a system instruction
    and return the generated response.
    """

    if not text or not text.strip():
        return ""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=text,
        config={
            "system_instruction": system_prompt,
            "temperature": 0.5,
        }
    )

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return response.text.strip()


# ============================================================
# ACTION ITEMS
# ============================================================

def extract_action_items(
    transcript: str
) -> str:
    """
    Extract action items from a transcript.
    """

    if not transcript or not transcript.strip():
        return "No action items found."

    system_prompt = """
You are an expert meeting analyst.

Analyze the meeting transcript and extract only
the action items that were actually assigned.

For each action item provide:

1. Task description
2. Owner / responsible person
3. Deadline, if mentioned

If the owner is not mentioned, write:
Not specified

If the deadline is not mentioned, write:
Not specified

Do not invent information.

Format the result as a numbered list.

If there are no action items, return exactly:
No action items found.
"""

    return generate_response(
        system_prompt,
        transcript
    )


# ============================================================
# KEY DECISIONS
# ============================================================

def extract_key_decisions(
    transcript: str
) -> str:
    """
    Extract finalized decisions from a transcript.
    """

    if not transcript or not transcript.strip():
        return "No key decisions found."

    system_prompt = """
You are an expert meeting analyst.

Analyze the meeting transcript and extract only
the key decisions that were actually finalized.

Do NOT include:

- Suggestions
- Ideas
- Unresolved discussions
- Possibilities
- Opinions that were not finalized

Do not invent information.

Format the result as a numbered list.

If there are no finalized decisions, return exactly:
No key decisions found.
"""

    return generate_response(
        system_prompt,
        transcript
    )


# ============================================================
# OPEN QUESTIONS
# ============================================================

def extract_questions(
    transcript: str
) -> str:
    """
    Extract unresolved questions and follow-up topics.
    """

    if not transcript or not transcript.strip():
        return "No open questions found."

    system_prompt = """
You are an expert meeting analyst.

Analyze the meeting transcript and identify:

- Unresolved questions
- Topics requiring follow-up
- Information that still needs clarification

Do not invent questions that are not present
in the transcript.

Format the result as a numbered list.

If there are no unresolved questions, return exactly:
No open questions found.
"""

    return generate_response(
        system_prompt,
        transcript
    )