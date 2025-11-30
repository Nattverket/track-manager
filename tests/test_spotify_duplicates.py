"""Tests for Spotify downloader duplicate detection."""

import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from track_manager.sources.spotify import SpotifyDownloader
from track_manager.config import Config


class TestSpotifyDuplicateDetection:
    """Test Spotify downloader duplicate detection functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.output_dir = Path(self.temp_dir.name)
        
        # Create a mock config
        self.config = MagicMock(spec=Config)
        self.config.output_dir = self.output_dir
        self.config.duplicate_handling = "skip"

    def teardown_method(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()

    def test_check_existing_duplicates_no_duplicates(self):
        """Test duplicate check when no duplicates exist."""
        downloader = SpotifyDownloader(self.config, self.output_dir)
        
        # Mock song object
        song = MagicMock()
        song.artist = "Test Artist"
        song.name = "Test Title"
        
        with patch("track_manager.duplicates.find_duplicates") as mock_find:
            mock_find.return_value = []
            
            duplicates = downloader._check_existing_duplicates(song, "m4a")
            assert duplicates == []

    def test_check_existing_duplicates_with_duplicates(self):
        """Test duplicate check when duplicates exist."""
        downloader = SpotifyDownloader(self.config, self.output_dir)
        
        # Mock song object
        song = MagicMock()
        song.artist = "Test Artist"
        song.name = "Test Title"
        
        # Create a mock duplicate file
        duplicate_file = self.output_dir / "existing.mp3"
        duplicate_file.touch()
        
        with patch("track_manager.duplicates.find_duplicates") as mock_find:
            mock_find.return_value = [duplicate_file]
            
            duplicates = downloader._check_existing_duplicates(song, "m4a")
            assert duplicates == [duplicate_file]

    def test_check_existing_duplicates_missing_metadata(self):
        """Test duplicate check with missing metadata."""
        downloader = SpotifyDownloader(self.config, self.output_dir)
        
        # Mock song object with missing metadata
        song = MagicMock()
        song.artist = None
        song.name = "Test Title"
        
        duplicates = downloader._check_existing_duplicates(song, "m4a")
        assert duplicates == []

    @patch("track_manager.sources.spotify.SpotifyDownloader._check_existing_duplicates")
    @patch("track_manager.sources.spotify.SpotifyDownloader.spotdl")
    def test_download_skips_existing_track(self, mock_spotdl, mock_check_duplicates):
        """Test that download skips tracks that already exist."""
        downloader = SpotifyDownloader(self.config, self.output_dir)
        
        # Mock song object
        song = MagicMock()
        song.artist = "Test Artist"
        song.name = "Test Title"
        song.url = "https://open.spotify.com/track/test"
        
        # Mock duplicate check to return existing file
        duplicate_file = self.output_dir / "existing.mp3"
        duplicate_file.touch()
        mock_check_duplicates.return_value = [duplicate_file]
        
        # Mock spotdl search
        mock_spotdl.search.return_value = [song]
        
        # Run download
        downloader.download("https://open.spotify.com/track/test")
        
        # Verify spotdl.download was NOT called
        mock_spotdl.download.assert_not_called()

    @patch("track_manager.sources.spotify.SpotifyDownloader._check_existing_duplicates")
    @patch("track_manager.sources.spotify.SpotifyDownloader.spotdl")
    @patch("track_manager.sources.spotify.SpotifyDownloader._find_downloaded_file")
    @patch("track_manager.sources.spotify.SpotifyDownloader._process_download")
    def test_download_proceeds_when_no_duplicates(
        self, mock_process, mock_find, mock_spotdl, mock_check_duplicates
    ):
        """Test that download proceeds when no duplicates exist."""
        downloader = SpotifyDownloader(self.config, self.output_dir)
        
        # Mock song object
        song = MagicMock()
        song.artist = "Test Artist"
        song.name = "Test Title"
        song.url = "https://open.spotify.com/track/test"
        
        # Mock no duplicates
        mock_check_duplicates.return_value = []
        
        # Mock successful download
        mock_spotdl.search.return_value = [song]
        mock_spotdl.download.return_value = (song, self.output_dir / "new.mp3")
        mock_find.return_value = self.output_dir / "new.mp3"
        mock_process.return_value = True
        
        # Run download
        downloader.download("https://open.spotify.com/track/test")
        
        # Verify spotdl.download WAS called
        mock_spotdl.download.assert_called_once_with(song)

    @patch("track_manager.sources.spotify.SpotifyDownloader._check_existing_duplicates")
    @patch("track_manager.sources.spotify.SpotifyDownloader.spotdl")
    def test_download_handles_multiple_tracks_with_duplicates(
        self, mock_spotdl, mock_check_duplicates
    ):
        """Test download with multiple tracks, some duplicates."""
        downloader = SpotifyDownloader(self.config, self.output_dir)
        
        # Mock multiple songs
        song1 = MagicMock()
        song1.artist = "Artist1"
        song1.name = "Title1"
        song1.url = "https://open.spotify.com/track/1"
        
        song2 = MagicMock()
        song2.artist = "Artist2"
        song2.name = "Title2"
        song2.url = "https://open.spotify.com/track/2"
        
        # Mock duplicate check - first song exists, second doesn't
        duplicate_file = self.output_dir / "existing.mp3"
        duplicate_file.touch()
        mock_check_duplicates.side_effect = [
            [duplicate_file],  # First song has duplicate
            [],  # Second song no duplicate
        ]
        
        # Mock spotdl search
        mock_spotdl.search.return_value = [song1, song2]
        
        # Mock successful download for second song
        mock_spotdl.download.return_value = (song2, self.output_dir / "new.mp3")
        
        # Mock file processing
        with patch.object(downloader, "_find_downloaded_file") as mock_find:
            with patch.object(downloader, "_process_download") as mock_process:
                mock_find.return_value = self.output_dir / "new.mp3"
                mock_process.return_value = True
                
                # Run download
                downloader.download("https://open.spotify.com/playlist/test")
                
                # Verify spotdl.download was called only for second song
                mock_spotdl.download.assert_called_once_with(song2)

    @patch("track_manager.sources.spotify.SpotifyDownloader._check_existing_duplicates")
    @patch("track_manager.sources.spotify.SpotifyDownloader.spotdl")
    def test_download_handles_empty_duplicate_check(
        self, mock_spotdl, mock_check_duplicates
    ):
        """Test download when duplicate check returns empty list."""
        downloader = SpotifyDownloader(self.config, self.output_dir)
        
        # Mock song object
        song = MagicMock()
        song.artist = "Test Artist"
        song.name = "Test Title"
        song.url = "https://open.spotify.com/track/test"
        
        # Mock empty duplicate list
        mock_check_duplicates.return_value = []
        
        # Mock successful download
        mock_spotdl.search.return_value = [song]
        mock_spotdl.download.return_value = (song, self.output_dir / "new.mp3")
        
        # Mock file processing
        with patch.object(downloader, "_find_downloaded_file") as mock_find:
            with patch.object(downloader, "_process_download") as mock_process:
                mock_find.return_value = self.output_dir / "new.mp3"
                mock_process.return_value = True
                
                # Run download
                downloader.download("https://open.spotify.com/track/test")
                
                # Verify track was downloaded
                mock_spotdl.download.assert_called_once_with(song)
