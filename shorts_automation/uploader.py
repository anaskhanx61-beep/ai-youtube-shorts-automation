from pathlib import Path


def upload_video(video_path: str, title: str, description: str = "") -> str:
    """Scaffold a YouTube upload flow.

    This intentionally does not perform uploads automatically because proper OAuth credentials
    and YouTube API setup are required. The function simply documents the expected flow.
    """
    path = Path(video_path)
    if not path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")

    return (
        f"Upload placeholder for {title}. "
        "Implement Google OAuth and the YouTube Data API before enabling this flow."
    )


__all__ = ["upload_video"]
