"""Pytest fixtures for integration tests."""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
import yaml

from track_manager.config import Config


@pytest.fixture
def temp_output_dir(tmp_path):
    """Create a temporary output directory for tests."""
    output_dir = tmp_path / "downloads"
    output_dir.mkdir()
    return output_dir


@pytest.fixture
def temp_config_file(tmp_path, temp_output_dir):
    """Create a temporary config file."""
    config_path = tmp_path / "config.yaml"
    config_data = {
        'output_dir': str(temp_output_dir),
        'failed_log': str(tmp_path / "failed.txt"),
        'metadata_csv': str(tmp_path / "metadata-review.csv"),
        'duplicate_handling': 'interactive',
        'default_format': 'auto',
        'playlist_threshold': 50,
    }
    with open(config_path, 'w') as f:
        yaml.dump(config_data, f)
    return config_path


@pytest.fixture
def test_config(temp_config_file, temp_output_dir):
    """Create a Config instance for testing."""
    with patch('track_manager.config.Path.home') as mock_home:
        mock_home.return_value = temp_config_file.parent
        config = Config(config_path=temp_config_file)
        return config


@pytest.fixture
def create_test_audio_file():
    """Factory fixture to create test audio files with metadata."""
    def _create(path: Path, artist: str = None, title: str = None, 
                format: str = 'mp3'):
        """Create a minimal valid audio file with metadata.
        
        Args:
            path: Path to create file at
            artist: Artist metadata
            title: Title metadata
            format: File format (mp3 or m4a)
        """
        from mutagen.mp3 import MP3
        from mutagen.id3 import ID3, TIT2, TPE1
        from mutagen.mp4 import MP4
        
        # Ensure parent directory exists
        path.parent.mkdir(parents=True, exist_ok=True)
        
        if format == 'mp3':
            # Create minimal valid MP3 file
            # This is a minimal MP3 frame header
            mp3_data = b'\xff\xfb\x90\x00' + b'\x00' * 100
            path.write_bytes(mp3_data)
            
            # Add ID3 tags
            audio = MP3(str(path), ID3=ID3)
            audio.add_tags()
            if artist:
                audio.tags.add(TPE1(encoding=3, text=artist))
            if title:
                audio.tags.add(TIT2(encoding=3, text=title))
            audio.save()
            
        elif format == 'm4a':
            # Create minimal valid M4A file
            # This is a minimal M4A container
            m4a_data = (
                b'\x00\x00\x00\x20ftypisom\x00\x00\x02\x00'
                b'isomiso2avc1mp41'
                b'\x00\x00\x00\x08free'
            )
            path.write_bytes(m4a_data)
            
            # Add tags
            audio = MP4(str(path))
            if artist:
                audio.tags['\xa9ART'] = [artist]
            if title:
                audio.tags['\xa9nam'] = [title]
            audio.save()
        
        return path
    
    return _create


@pytest.fixture
def mock_spotify_download():
    """Mock spotdl downloads."""
    with patch('track_manager.sources.spotify.spotdl') as mock_spotdl:
        yield mock_spotdl


@pytest.fixture
def mock_ytdlp_download():
    """Mock yt-dlp downloads."""
    with patch('track_manager.sources.youtube.yt_dlp') as mock_ytdlp:
        yield mock_ytdlp


@pytest.fixture
def mock_requests_download():
    """Mock requests downloads."""
    with patch('track_manager.sources.direct.requests') as mock_requests:
        # Create a mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {'content-type': 'audio/mpeg'}
        mock_response.iter_content = Mock(return_value=[b'test data'])
        mock_requests.get.return_value = mock_response
        yield mock_requests
