import os

from dotenv import load_dotenv
from PIL import Image, ImageEnhance

from google import genai


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


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ============================================================
# OCR READER
# ============================================================

class OCRReader:

    def __init__(self):

        print(
            f"Using Gemini Vision: "
            f"{GEMINI_MODEL}"
        )

    # ========================================================
    # IMAGE PREPROCESSING
    # ========================================================

    def preprocess_image(
        self,
        image: Image.Image
    ) -> Image.Image:

        image = image.convert(
            "RGB"
        )

        width, height = image.size

        image = image.resize(
            (
                width * 2,
                height * 2
            ),
            Image.Resampling.LANCZOS
        )

        contrast = ImageEnhance.Contrast(
            image
        )

        image = contrast.enhance(
            1.5
        )

        sharpness = ImageEnhance.Sharpness(
            image
        )

        image = sharpness.enhance(
            1.3
        )

        return image

    # ========================================================
    # READ HANDWRITTEN IMAGE
    # ========================================================

    def read_image(
        self,
        image_path: str
    ) -> str:

        if not os.path.isfile(
            image_path
        ):
            raise FileNotFoundError(
                f"Image not found:\n"
                f"{image_path}"
            )

        print(
            f"\nReading image:\n"
            f"{image_path}"
        )

        # ----------------------------------------------------
        # Open image
        # ----------------------------------------------------

        try:

            image = Image.open(
                image_path
            )

        except Exception as exc:

            raise ValueError(
                f"Could not open image:\n"
                f"{exc}"
            ) from exc

        print(
            f"Original image size: "
            f"{image.size}"
        )

        # ----------------------------------------------------
        # Preprocess
        # ----------------------------------------------------

        processed_image = (
            self.preprocess_image(
                image
            )
        )

        print(
            f"Processed image size: "
            f"{processed_image.size}"
        )

        # ====================================================
        # PROMPT
        # ====================================================

        prompt = """
You are an expert handwritten-notes
transcription system.

Carefully read the handwritten notes
in the provided image.

Your job is ONLY to transcribe the
content of the image.

IMPORTANT RULES:

1. Read the actual handwriting.

2. Do not invent missing words.

3. Do not hallucinate concepts.

4. Preserve headings.

5. Preserve subheadings.

6. Preserve bullet points.

7. Preserve numbered lists.

8. Preserve formulas when readable.

9. Preserve technical terminology.

10. Correct obvious spelling mistakes only
when the intended word is clearly visible.

11. If a word cannot be confidently read,
write [unclear].

12. Never guess an unclear word.

13. Do not summarize.

14. Do not explain the notes.

15. Do not add information that is not
present in the image.

16. Keep the original structure as much
as possible.

Return ONLY the transcription.
"""

        # ====================================================
        # GEMINI VISION
        # ====================================================

        print(
            "\nSending image to Gemini..."
        )

        try:

            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=[
                    prompt,
                    processed_image
                ]
            )

        except Exception as exc:

            raise RuntimeError(
                f"Gemini Vision request failed:\n"
                f"{exc}"
            ) from exc

        # ====================================================
        # RESPONSE
        # ====================================================

        text = response.text

        if not text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        text = text.strip()

        print(
            "\nGemini transcription complete."
        )

        return text