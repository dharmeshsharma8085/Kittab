from pathlib import Path

from video_audio import extract_audio


# ============================================================
# FIND DOWNLOADED VIDEO
# ============================================================

VIDEO_DIR = Path(__file__).resolve().parent
DOWNLOAD_DIR = VIDEO_DIR / "downloads"


videos = list(
    DOWNLOAD_DIR.glob("*.mp4")
)


if not videos:
    raise FileNotFoundError(
        "No MP4 video found in:\n"
        f"{DOWNLOAD_DIR}"
    )


# Use the newest downloaded video
video_path = max(
    videos,
    key=lambda file: file.stat().st_mtime
)


# ============================================================
# TEST
# ============================================================

print("\nVIDEO → AUDIO TEST")
print("=" * 60)

print(
    f"Video found:\n{video_path}"
)


audio_path = extract_audio(
    str(video_path)
)


print("\nSUCCESS")
print("=" * 60)

print(
    f"Audio file:\n{audio_path}"
)