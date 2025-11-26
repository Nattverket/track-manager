"""Integration tests for error handling."""

import pytest
from pathlib import Path
from unittest.mock import patch, Mock

from track_manager.downloader import Downloader


class TestErrorHandling:
    """Test error handling across the system."""
    
    def test_failed_download_logged(self, test_config, temp_output_dir):
        """Test that failed downloads are logged to file."""
        downloader = Downloader(test_config, temp_output_dir)
        
        # Mock a download failure
        with patch('track_manager.sources.spotify.SpotifyDownloader.download') as mock_dl:
            mock_dl.side_effect = Exception("Network error")
            
            # Attempt download (should not raise)
            downloader.download("https://open.spotify.com/track/test", "auto")
        
        # Verify failure was logged
        assert test_config.failed_log.exists()
        log_content = test_config.failed_log.read_text()
        assert "https://open.spotify.com/track/test" in log_content
        assert "Network error" in log_content
    
    def test_continue_after_failure(self, test_config, temp_output_dir):
        """Test that processing continues after a failure."""
        downloader = Downloader(test_config, temp_output_dir)
        
        # Mock downloads - first fails, second succeeds
        call_count = 0
        def mock_download(url, fmt):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise Exception("First download failed")
            # Second call succeeds (no exception)
        
        with patch('track_manager.sources.youtube.YouTubeDownloader.download') as mock_dl:
            mock_dl.side_effect = mock_download
            
            # First download (should fail but not crash)
            downloader.download("https://youtube.com/watch?v=fail", "auto")
            
            # Second download (should succeed)
            downloader.download("https://youtube.com/watch?v=success", "auto")
        
        # Verify both were attempted
        assert call_count == 2
    
    def test_invalid_url_handled(self, test_config, temp_output_dir):
        """Test that invalid URLs are handled gracefully."""
        downloader = Downloader(test_config, temp_output_dir)
        
        with patch('track_manager.sources.direct.DirectDownloader.download') as mock_dl:
            mock_dl.side_effect = Exception("Invalid URL")
            
            # Should not raise
            downloader.download("not-a-url", "auto")
        
        # Verify logged
        assert test_config.failed_log.exists()
    
    def test_missing_metadata_handled(self, temp_output_dir, create_test_audio_file):
        """Test that files with missing metadata are handled properly."""
        from track_manager.sources.base import BaseDownloader
        
        # Create file without metadata
        test_file = temp_output_dir / "no_metadata.mp3"
        create_test_audio_file(test_file, artist=None, title=None, format='mp3')
        
        # Create a base downloader instance
        mock_config = Mock()
        mock_config.metadata_csv = temp_output_dir / "review.csv"
        downloader = BaseDownloader(mock_config, temp_output_dir)
        
        # Extract metadata (should not raise)
        artist, title = downloader.extract_metadata(test_file)
        
        assert artist is None
        assert title is None
    
    def test_corrupt_audio_file_handled(self, temp_output_dir):
        """Test that corrupt audio files are handled gracefully."""
        from track_manager.sources.base import BaseDownloader
        
        # Create corrupt file
        corrupt_file = temp_output_dir / "corrupt.mp3"
        corrupt_file.write_bytes(b"not valid audio data")
        
        mock_config = Mock()
        downloader = BaseDownloader(mock_config, temp_output_dir)
        
        # Should not raise, should return None
        artist, title = downloader.extract_metadata(corrupt_file)
        assert artist is None
        assert title is None
    
    def test_network_timeout_handled(self, test_config, temp_output_dir):
        """Test that network timeouts are handled properly."""
        downloader = Downloader(test_config, temp_output_dir)
        
        with patch('track_manager.sources.direct.DirectDownloader.download') as mock_dl:
            mock_dl.side_effect = TimeoutError("Connection timeout")
            
            # Should not crash
            downloader.download("https://example.com/audio.mp3", "auto")
        
        # Verify logged
        assert test_config.failed_log.exists()
        log_content = test_config.failed_log.read_text()
        assert "timeout" in log_content.lower()
    
    def test_permission_error_handled(self, test_config, temp_output_dir):
        """Test that permission errors are handled gracefully."""
        downloader = Downloader(test_config, temp_output_dir)
        
        with patch('track_manager.sources.spotify.SpotifyDownloader.download') as mock_dl:
            mock_dl.side_effect = PermissionError("Permission denied")
            
            # Should not crash
            downloader.download("https://open.spotify.com/track/test", "auto")
        
        # Verify logged
        assert test_config.failed_log.exists()
    
    def test_disk_full_handled(self, test_config, temp_output_dir):
        """Test that disk full errors are handled properly."""
        downloader = Downloader(test_config, temp_output_dir)
        
        with patch('track_manager.sources.youtube.YouTubeDownloader.download') as mock_dl:
            mock_dl.side_effect = OSError("No space left on device")
            
            # Should not crash
            downloader.download("https://youtube.com/watch?v=test", "auto")
        
        # Verify logged
        assert test_config.failed_log.exists()
        log_content = test_config.failed_log.read_text()
        assert "space" in log_content.lower()
    
    def test_api_rate_limit_handled(self, test_config, temp_output_dir):
        """Test that API rate limits are handled gracefully."""
        downloader = Downloader(test_config, temp_output_dir)
        
        with patch('track_manager.sources.spotify.SpotifyDownloader.download') as mock_dl:
            mock_dl.side_effect = Exception("Rate limit exceeded")
            
            # Should not crash
            downloader.download("https://open.spotify.com/track/test", "auto")
        
        # Verify logged
        assert test_config.failed_log.exists()
        log_content = test_config.failed_log.read_text()
        assert "Rate limit" in log_content
    
    def test_multiple_failures_logged_separately(self, test_config, temp_output_dir):
        """Test that multiple failures are logged as separate entries."""
        downloader = Downloader(test_config, temp_output_dir)
        
        with patch('track_manager.sources.spotify.SpotifyDownloader.download') as mock_dl:
            mock_dl.side_effect = [
                Exception("Error 1"),
                Exception("Error 2"),
                Exception("Error 3")
            ]
            
            # Attempt multiple downloads
            downloader.download("https://open.spotify.com/track/1", "auto")
            downloader.download("https://open.spotify.com/track/2", "auto")
            downloader.download("https://open.spotify.com/track/3", "auto")
        
        # Verify all logged
        log_content = test_config.failed_log.read_text()
        assert "Error 1" in log_content
        assert "Error 2" in log_content
        assert "Error 3" in log_content
        
        # Count lines (should have 3 failure entries)
        lines = [l for l in log_content.split('\n') if l.strip()]
        assert len(lines) == 3
