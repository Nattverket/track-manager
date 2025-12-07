"""SoundCloud downloader using yt-dlp Python API.

SoundCloud support via yt-dlp - similar to YouTube handler.
"""

from .youtube import YouTubeDownloader


class SoundCloudDownloader(YouTubeDownloader):
    """SoundCloud downloader using yt-dlp.

    Inherits from YouTubeDownloader since yt-dlp handles both similarly.
    """

    # Add SoundCloud-specific handling if needed
    # For now, yt-dlp handles SoundCloud just like YouTube
    pass
