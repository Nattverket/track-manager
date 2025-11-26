"""Source-specific downloader modules."""

from . import spotify
from . import youtube
from . import soundcloud
from . import direct

__all__ = ['spotify', 'youtube', 'soundcloud', 'direct']
