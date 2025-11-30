"""SoundCloud downloader using yt-dlp Python API.

SoundCloud support via yt-dlp - similar to YouTube handler.
"""

import sys
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    print("Error: yt-dlp not installed", file=sys.stderr)
    print("Install with: pip install yt-dlp", file=sys.stderr)
    sys.exit(1)

from .youtube import YouTubeDownloader


class SoundCloudDownloader(YouTubeDownloader):
    """SoundCloud downloader using yt-dlp.

    Inherits from YouTubeDownloader since yt-dlp handles both similarly.
    """

    # TODO: Add SoundCloud-specific handling if needed
    # For now, yt-dlp handles SoundCloud just like YouTube
    pass
