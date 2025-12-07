"""Main downloader orchestrator."""

import sys
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

from .config import Config
from .sources import direct, soundcloud, spotify, youtube


class Downloader:
    """Main downloader class that routes to appropriate source handler."""

    def __init__(self, config: Config, output_dir: Optional[Path] = None):
        """Initialize downloader.

        Args:
            config: Configuration object
            output_dir: Override output directory
        """
        self.config = config
        self.output_dir = output_dir or config.output_dir

        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def detect_source(self, url: str) -> str:
        """Detect source type from URL.

        Args:
            url: URL to analyze

        Returns:
            Source type: 'spotify', 'youtube', 'soundcloud', or 'direct'
        """
        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        if "spotify.com" in domain:
            return "spotify"
        elif "youtube.com" in domain or "youtu.be" in domain:
            return "youtube"
        elif "soundcloud.com" in domain:
            return "soundcloud"
        else:
            # Assume direct audio file URL
            return "direct"

    def download(self, url: str, format: str = "auto"):
        """Download track(s) from URL.

        Args:
            url: URL to download from
            format: Output format (auto, m4a, mp3)
        """
        source_type = self.detect_source(url)

        print(f"🎵 Detected source: {source_type.title()}")
        print(f"📁 Output directory: {self.output_dir}")
        print()

        # Route to appropriate handler
        if source_type == "spotify":
            handler = spotify.SpotifyDownloader(self.config, self.output_dir)
        elif source_type == "youtube":
            handler = youtube.YouTubeDownloader(self.config, self.output_dir)
        elif source_type == "soundcloud":
            handler = soundcloud.SoundCloudDownloader(self.config, self.output_dir)
        else:
            handler = direct.DirectDownloader(self.config, self.output_dir)

        # Download
        try:
            handler.download(url, format)
        except Exception as e:
            print(f"❌ Download failed: {e}", file=sys.stderr)

            # Log to failed downloads
            self._log_failure(url, str(e))
            raise

    def _log_failure(self, url: str, error: str):
        """Log failed download.

        Args:
            url: URL that failed
            error: Error message
        """
        from datetime import datetime

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        log_entry = f"{timestamp} | {url} | {error}\n"

        with open(self.config.failed_log, "a") as f:
            f.write(log_entry)
