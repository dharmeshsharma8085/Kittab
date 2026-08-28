import os
from pathlib import Path

import yt_dlp


# ============================================================
# CONFIGURATION
# ============================================================

VIDEO_DIR = Path(__file__).resolve().parent

DOWNLOAD_DIR = VIDEO_DIR / "downloads"

DOWNLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# URL VALIDATION
# ============================================================

def validate_youtube_url(
    youtube_url: str
) -> str:
    """
    Validate and clean a YouTube URL.
    """

    if not youtube_url:
        raise ValueError(
            "YouTube URL cannot be empty."
        )

    youtube_url = youtube_url.strip()

    if (
        "youtube.com" not in youtube_url
        and "youtu.be" not in youtube_url
    ):
        raise ValueError(
            "Please provide a valid YouTube URL."
        )

    return youtube_url


# ============================================================
# GET VIDEO INFORMATION
# ============================================================

def get_youtube_info(
    youtube_url: str
) -> dict:
    """
    Get YouTube video metadata
    without downloading the video.
    """

    youtube_url = validate_youtube_url(
        youtube_url
    )

    options = {
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
    }

    try:

        with yt_dlp.YoutubeDL(options) as ydl:

            info = ydl.extract_info(
                youtube_url,
                download=False
            )

    except Exception as exc:

        raise RuntimeError(
            f"Failed to get YouTube information:\n{exc}"
        ) from exc

    return {
        "id": info.get("id"),
        "title": info.get("title"),
        "description": info.get("description"),
        "duration": info.get("duration"),
        "channel": info.get("channel"),
        "uploader": info.get("uploader"),
        "webpage_url": info.get("webpage_url"),
        "thumbnail": info.get("thumbnail"),
    }


# ============================================================
# DOWNLOAD VIDEO
# ============================================================

def download_youtube_video(
    youtube_url: str
) -> str:
    """
    Download a YouTube video locally.

    Returns:
        Path of the downloaded video.
    """

    youtube_url = validate_youtube_url(
        youtube_url
    )

    output_template = str(
        DOWNLOAD_DIR / "%(title)s.%(ext)s"
    )

    options = {
        # Best available video + audio.
        # Falls back to a single format if needed.
        "format": "bv*+ba/b",

        "outtmpl": output_template,

        "noplaylist": True,

        # Try to produce MP4 after merging.
        "merge_output_format": "mp4",

        "quiet": False,

        "no_warnings": False,
    }

    print(
        "\nDownloading YouTube video..."
    )

    print(
        f"URL: {youtube_url}"
    )

    try:

        with yt_dlp.YoutubeDL(options) as ydl:

            info = ydl.extract_info(
                youtube_url,
                download=True
            )

            prepared_path = Path(
                ydl.prepare_filename(info)
            )

    except Exception as exc:

        raise RuntimeError(
            f"Failed to download YouTube video:\n{exc}"
        ) from exc

    # ========================================================
    # FIND FINAL DOWNLOADED FILE
    # ========================================================

    if prepared_path.exists():

        final_path = prepared_path

    else:

        # The final file may have a different extension
        # after video/audio merging.
        candidates = list(
            DOWNLOAD_DIR.glob(
                f"{prepared_path.stem}.*"
            )
        )

        # Ignore temporary/partial files.
        candidates = [
            file
            for file in candidates
            if file.suffix.lower()
            not in {
                ".part",
                ".ytdl",
                ".temp"
            }
        ]

        if not candidates:

            raise FileNotFoundError(
                "Video download completed, "
                "but the final video file "
                "could not be found."
            )

        final_path = max(
            candidates,
            key=os.path.getmtime
        )

    # ========================================================
    # SUCCESS
    # ========================================================

    print(
        "\nDownload complete."
    )

    print(
        f"Saved to:\n{final_path}"
    )

    return str(final_path)


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    url = input(
        "Enter YouTube URL: "
    ).strip()

    # --------------------------------------------------------
    # Get metadata
    # --------------------------------------------------------

    info = get_youtube_info(
        url
    )

    print(
        "\nVIDEO INFORMATION"
    )

    print(
        "=" * 60
    )

    print(
        f"Title: {info['title']}"
    )

    print(
        f"Channel: {info['channel']}"
    )

    print(
        f"Duration: {info['duration']} seconds"
    )

    # --------------------------------------------------------
    # Download
    # --------------------------------------------------------

    video_path = download_youtube_video(
        url
    )

    print(
        "\nVIDEO SAVED"
    )

    print(
        "=" * 60
    )

    print(
        video_path
    )