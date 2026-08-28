import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from langchain_text_splitters import RecursiveCharacterTextSplitter


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


client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ============================================================
# GEMINI HELPER
# ============================================================

def generate_text(
    system_instruction: str,
    text: str,
    temperature: float = 0.5
) -> str:
    """
    Generate a Gemini response for the supplied text.
    """

    if not text or not text.strip():
        return ""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=text,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=temperature,
        )
    )

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return response.text.strip()


# ============================================================
# TRANSCRIPT SPLITTING
# ============================================================

def split_transcript(
    transcript: str
) -> list[str]:
    """
    Split a long transcript into overlapping chunks.

    This keeps enough context between neighboring chunks
    while preventing very large requests.
    """

    if not transcript or not transcript.strip():
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000,
        chunk_overlap=300,
        separators=[
            "\n\n",
            "\n",
            ". ",
            "? ",
            "! ",
            " ",
        ],
    )

    return splitter.split_text(
        transcript
    )


# ============================================================
# SUMMARIZE
# ============================================================

def summarize(
    transcript: str
) -> str:
    """
    Generate a concise professional summary
    from a long transcript.

    Uses a map-reduce style approach:

        Transcript
             ↓
        Split chunks
             ↓
        Summarize each chunk
             ↓
        Combine summaries
             ↓
        Final summary
    """

    if not transcript or not transcript.strip():
        return "No transcript available to summarize."

    chunks = split_transcript(
        transcript
    )

    if not chunks:
        return "No transcript available to summarize."

    # --------------------------------------------------------
    # MAP: summarize each chunk
    # --------------------------------------------------------

    chunk_summaries = []

    map_instruction = """
You are an expert meeting and lecture summarizer.

Summarize the provided transcript section concisely.

Keep important:
- Topics
- Facts
- Explanations
- Decisions
- Examples
- Action items
- Important conclusions

Do not invent information.

Return only the summary.
"""

    for i, chunk in enumerate(
        chunks,
        start=1
    ):

        print(
            f"Summarizing chunk "
            f"{i}/{len(chunks)}..."
        )

        summary = generate_text(
            system_instruction=map_instruction,
            text=chunk,
            temperature=0.3,
        )

        if summary:
            chunk_summaries.append(
                summary
            )

    if not chunk_summaries:
        return "Unable to generate summary."

    # --------------------------------------------------------
    # REDUCE: combine chunk summaries
    # --------------------------------------------------------

    combined = "\n\n".join(
        chunk_summaries
    )

    reduce_instruction = """
You are an expert meeting and lecture summarizer.

Combine the provided partial summaries into ONE
clear, professional final summary.

Organize the result with useful sections when appropriate:

- Overview
- Key Topics
- Important Points
- Decisions
- Action Items
- Conclusions

Do not repeat information unnecessarily.

Do not invent information.

Return only the final summary.
"""

    print(
        "Generating final summary..."
    )

    final_summary = generate_text(
        system_instruction=reduce_instruction,
        text=combined,
        temperature=0.3,
    )

    return final_summary


# ============================================================
# TITLE GENERATION
# ============================================================

def generate_title(
    transcript: str
) -> str:
    """
    Generate a short professional title
    from the transcript.
    """

    if not transcript or not transcript.strip():
        return "Untitled Meeting"

    instruction = """
Based on the provided transcript, generate a short,
professional and descriptive title.

Rules:
- Maximum 8 words
- Do not use quotation marks
- Do not add explanations
- Return ONLY the title
"""

    title = generate_text(
        system_instruction=instruction,
        text=transcript[:4000],
        temperature=0.3,
    )

    return title.strip()


# ============================================================
# TEST / DEMO
# ============================================================

if __name__ == "__main__":

    sample_transcript = """
    The team discussed the Kittab project.

    The audio transcription pipeline will use Whisper
    for English audio and Sarvam for Hinglish audio.

    The team decided to use Gemini as the main LLM.

    Dharmesh will finish the audio module by Friday.

    The team still needs to decide how the final
    production vector database will be deployed.
    """

    print("\nTITLE")
    print("=" * 60)
    print(generate_title(sample_transcript))

    print("\nSUMMARY")
    print("=" * 60)
    print(summarize(sample_transcript))