import os
import subprocess
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

VIDEO_DIR = Path(__file__).resolve().parent

AUDIO_DIR = VIDEO_DIR / "audio"

AUDIO_DIR.mkdir(
    parents=True,
    exist_ok=True
)

FFMPEG_EXE = r"C:\ffmpeg\bin\ffmpeg.exe"


# ============================================================
# VALIDATE FFMPEG
# ============================================================

def check_ffmpeg():
    """
    Check whether FFmpeg exists.
    """

    if not os.path.isfile(FFMPEG_EXE):
        raise FileNotFoundError(
            f"FFmpeg not found at:\n{FFMPEG_EXE}"
        )


# ============================================================
# EXTRACT AUDIO
# ============================================================

def extract_audio(
    video_path: str
) -> str:
    """
    Extract audio from a video file.

    Output:
        WAV file

    Returns:
        Path to extracted WAV file.
    """

    check_ffmpeg()

    video_path = Path(
        video_path
    )

    if not video_path.exists():
        raise FileNotFoundError(
            f"Video not found:\n{video_path}"
        )

    if not video_path.is_file():
        raise ValueError(
            f"Path is not a file:\n{video_path}"
        )

    # Create output filename
    output_path = (
        AUDIO_DIR
        / f"{video_path.stem}.wav"
    )

    print(
        "\nExtracting audio..."
    )

    print(
        f"Video:\n{video_path}"
    )

    print(
        f"Audio:\n{output_path}"
    )

    command = [
        FFMPEG_EXE,

        "-y",

        "-i",
        str(video_path),

        # Mono audio
        "-ac",
        "1",

        # 16 kHz sample rate
        "-ar",
        "16000",

        # PCM WAV
        "-acodec",
        "pcm_s16le",

        str(output_path),
    ]

    try:

        subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

    except subprocess.CalledProcessError as exc:

        raise RuntimeError(
            "FFmpeg failed to extract audio.\n\n"
            f"{exc.stderr}"
        ) from exc

    if not output_path.exists():

        raise FileNotFoundError(
            "FFmpeg completed, but "
            "the audio file was not created."
        )

    print(
        "\nAudio extraction complete."
    )

    print(
        f"Saved to:\n{output_path}"
    )

    return str(output_path)


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    video_path = input(
        "Enter video path: "
    ).strip()

    audio_path = extract_audio(
        video_path
    )

    print(
        "\nFINAL AUDIO PATH"
    )

    print(
        "=" * 60
    )

    print(
        audio_path
    )