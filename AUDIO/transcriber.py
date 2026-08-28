import os
import shutil
from typing import List

import requests
import whisper
from dotenv import load_dotenv
from pydub import AudioSegment


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# FFMPEG CONFIGURATION
# ============================================================

# Change this ONLY if your FFmpeg is installed somewhere else.
FFMPEG_LOCATION = r"C:\ffmpeg\bin"

FFMPEG_EXE = os.path.join(
    FFMPEG_LOCATION,
    "ffmpeg.exe"
)

FFPROBE_EXE = os.path.join(
    FFMPEG_LOCATION,
    "ffprobe.exe"
)


def configure_ffmpeg():
    """
    Configure FFmpeg and FFprobe for pydub.
    """

    if not os.path.isfile(FFMPEG_EXE):
        raise FileNotFoundError(
            f"FFmpeg not found at:\n{FFMPEG_EXE}\n\n"
            "Please update FFMPEG_LOCATION in transcriber.py."
        )

    if not os.path.isfile(FFPROBE_EXE):
        raise FileNotFoundError(
            f"FFprobe not found at:\n{FFPROBE_EXE}\n\n"
            "Please update FFMPEG_LOCATION in transcriber.py."
        )

    # Add FFmpeg to PATH
    os.environ["PATH"] = (
        FFMPEG_LOCATION
        + os.pathsep
        + os.environ.get("PATH", "")
    )

    # Tell pydub where FFmpeg is
    AudioSegment.converter = FFMPEG_EXE
    AudioSegment.ffprobe = FFPROBE_EXE

    detected_ffmpeg = shutil.which("ffmpeg")
    detected_ffprobe = shutil.which("ffprobe")

    print(f"FFmpeg detected: {detected_ffmpeg}")
    print(f"FFprobe detected: {detected_ffprobe}")


# Configure when module loads
configure_ffmpeg()


# ============================================================
# CONFIGURATION
# ============================================================

# Sarvam REST API supports short audio requests.
# Keeping pieces at 25 seconds gives us some safety margin.
SARVAM_PIECE_SECONDS = 25

WHISPER_MODEL = os.getenv(
    "WHISPER_MODEL",
    "small"
)

SARVAM_API_KEY = os.getenv(
    "SARVAM_API_KEY"
)

SARVAM_STT_URL = (
    "https://api.sarvam.ai/speech-to-text"
)

SARVAM_MODEL = os.getenv(
    "SARVAM_STT_MODEL",
    "saaras:v3"
)


# ============================================================
# WHISPER MODEL
# ============================================================

_model = None


def load_model():
    """
    Load Whisper only once.

    The model is cached globally so we don't
    reload it for every audio chunk.
    """

    global _model

    if _model is None:

        print(
            f"Loading Whisper model: "
            f"{WHISPER_MODEL}..."
        )

        _model = whisper.load_model(
            WHISPER_MODEL
        )

        print(
            "Whisper model loaded successfully."
        )

    return _model


# ============================================================
# WHISPER TRANSCRIPTION
# ============================================================

def transcribe_chunk_whisper(
    chunk_path: str
) -> str:
    """
    Transcribe one audio chunk using local Whisper.
    """

    if not os.path.isfile(chunk_path):
        raise FileNotFoundError(
            f"Audio chunk not found:\n{chunk_path}"
        )

    model = load_model()

    print(
        f"Transcribing with Whisper:\n"
        f"{chunk_path}"
    )

    result = model.transcribe(
        chunk_path,
        task="transcribe",
        fp16=False
    )

    text = result.get(
        "text",
        ""
    ).strip()

    return text


# ============================================================
# SARVAM API
# ============================================================

def _send_to_sarvam(
    piece_path: str,
    mode: str = "transcribe"
) -> str:
    """
    Send one short WAV file to Sarvam.

    mode:
        transcribe -> original language
        translate  -> English translation
        translit   -> Romanized output
        codemix    -> code-mixed output
        verbatim   -> word-for-word output
    """

    if not SARVAM_API_KEY:
        raise RuntimeError(
            "SARVAM_API_KEY is not set in .env"
        )

    if not os.path.isfile(piece_path):
        raise FileNotFoundError(
            f"Sarvam audio file not found:\n{piece_path}"
        )

    headers = {
        "api-subscription-key": SARVAM_API_KEY
    }

    data = {
        "model": SARVAM_MODEL,
        "mode": mode
    }

    print(
        f"Sending to Sarvam | "
        f"model={SARVAM_MODEL} | "
        f"mode={mode}"
    )

    with open(
        piece_path,
        "rb"
    ) as audio_file:

        files = {
            "file": (
                os.path.basename(piece_path),
                audio_file,
                "audio/wav"
            )
        }

        response = requests.post(
            SARVAM_STT_URL,
            headers=headers,
            files=files,
            data=data,
            timeout=120
        )

    # --------------------------------------------------------
    # HTTP ERROR
    # --------------------------------------------------------

    if not response.ok:

        print(
            f"\nSarvam Error: "
            f"{response.status_code}"
        )

        print(
            response.text
        )

        response.raise_for_status()

    # --------------------------------------------------------
    # JSON RESPONSE
    # --------------------------------------------------------

    try:
        result = response.json()

    except ValueError as exc:

        raise RuntimeError(
            "Sarvam returned an invalid JSON response."
        ) from exc

    if "transcript" not in result:

        raise RuntimeError(
            "Unexpected Sarvam response:\n"
            f"{result}"
        )

    return result["transcript"].strip()


# ============================================================
# SARVAM TRANSCRIPTION
# ============================================================

def transcribe_chunk_sarvam(
    chunk_path: str,
    mode: str = "codemix"
) -> str:
    """
    Split a larger WAV chunk into 25-second pieces
    and send them individually to Sarvam.

    Default mode is codemix because it is useful
    for Hinglish/code-mixed speech.
    """

    if not os.path.isfile(chunk_path):
        raise FileNotFoundError(
            f"Audio chunk not found:\n{chunk_path}"
        )

    print(
        f"Loading audio chunk:\n{chunk_path}"
    )

    audio = AudioSegment.from_wav(
        chunk_path
    )

    piece_ms = (
        SARVAM_PIECE_SECONDS * 1000
    )

    transcripts: List[str] = []

    total_pieces = (
        len(audio) + piece_ms - 1
    ) // piece_ms

    print(
        f"Total Sarvam pieces: "
        f"{total_pieces}"
    )

    for i, start in enumerate(
        range(
            0,
            len(audio),
            piece_ms
        )
    ):

        piece = audio[
            start:start + piece_ms
        ]

        piece_path = (
            f"{chunk_path}_sv_{i}.wav"
        )

        piece.export(
            piece_path,
            format="wav"
        )

        try:

            print(
                f"\nSarvam piece "
                f"{i + 1}/{total_pieces}"
            )

            text = _send_to_sarvam(
                piece_path,
                mode=mode
            )

            if text:
                transcripts.append(
                    text
                )

        finally:

            if os.path.exists(
                piece_path
            ):
                os.remove(
                    piece_path
                )

    return " ".join(
        transcripts
    ).strip()


# ============================================================
# ROUTER
# ============================================================

def transcribe_chunk(
    chunk_path: str,
    language: str = "english"
) -> str:
    """
    Select transcription engine.

    english  -> Whisper
    hinglish -> Sarvam
    """

    language = (
        language
        .lower()
        .strip()
    )

    if language == "hinglish":

        return transcribe_chunk_sarvam(
            chunk_path,
            mode="codemix"
        )

    return transcribe_chunk_whisper(
        chunk_path
    )


# ============================================================
# TRANSCRIBE ALL
# ============================================================

def transcribe_all(
    chunks: list,
    language: str = "english"
) -> str:
    """
    Transcribe all audio chunks and
    combine them into one transcript.
    """

    if not chunks:
        raise ValueError(
            "No audio chunks provided."
        )

    language = (
        language
        .lower()
        .strip()
    )

    engine = (
        "Sarvam AI"
        if language == "hinglish"
        else "Whisper"
    )

    print(
        f"\nUsing {engine} "
        f"for transcription."
    )

    transcripts = []

    for i, chunk in enumerate(
        chunks
    ):

        print(
            f"\nTranscribing chunk "
            f"{i + 1}/{len(chunks)}..."
        )

        text = transcribe_chunk(
            chunk,
            language=language
        )

        if text:
            transcripts.append(
                text
            )

    print(
        "\nTranscription complete."
    )

    return " ".join(
        transcripts
    ).strip()