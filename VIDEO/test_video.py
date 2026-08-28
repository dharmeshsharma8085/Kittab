from video_loader import (
    get_youtube_info,
    download_youtube_video,
)


YOUTUBE_URL = "https://youtu.be/T-D1OfcDW1M"


print("\nVIDEO INFORMATION")
print("=" * 60)

info = get_youtube_info(
    YOUTUBE_URL
)

print(f"Title: {info['title']}")
print(f"Channel: {info['channel']}")
print(f"Duration: {info['duration']} seconds")


print("\nDOWNLOADING VIDEO")
print("=" * 60)

video_path = download_youtube_video(
    YOUTUBE_URL
)

print(f"\nVideo path:\n{video_path}")