"""Integration tests for duplicate detection."""

from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from track_manager.duplicates import check_file_duplicate, scan_library


class TestDuplicateDetection:
    """Test duplicate detection across formats and scenarios."""

    def test_same_format_duplicate(self, temp_output_dir, create_test_audio_file):
        """Test detecting duplicate in same format."""
        # Create existing file
        existing = temp_output_dir / "Artist - Song.mp3"
        create_test_audio_file(existing, artist="Artist", title="Song", format="mp3")

        # Create new file (duplicate)
        new_file = temp_output_dir / "new_file.mp3"
        create_test_audio_file(new_file, artist="Artist", title="Song", format="mp3")

        # Mock user input to skip
        with patch("builtins.input", return_value="s"):
            result = check_file_duplicate(new_file, temp_output_dir, "interactive")
            assert result is True  # Should skip (is duplicate)

    def test_cross_format_duplicate(self, temp_output_dir, create_test_audio_file):
        """Test detecting duplicate across formats (MP3 vs M4A)."""
        # Create existing MP3
        existing = temp_output_dir / "Artist - Song.mp3"
        create_test_audio_file(existing, artist="Artist", title="Song", format="mp3")

        # Create new M4A (duplicate)
        new_file = temp_output_dir / "new_file.m4a"
        create_test_audio_file(new_file, artist="Artist", title="Song", format="m4a")

        # Mock user input to skip
        with patch("builtins.input", return_value="s"):
            result = check_file_duplicate(new_file, temp_output_dir, "interactive")
            assert result is True  # Should skip (is duplicate)

    def test_normalized_metadata_matching(
        self, temp_output_dir, create_test_audio_file
    ):
        """Test that metadata normalization works for duplicates."""
        # Create existing file with clean metadata
        existing = temp_output_dir / "Artist - Song.mp3"
        create_test_audio_file(existing, artist="Artist", title="Song", format="mp3")

        # Create new file with junk in metadata
        new_file = temp_output_dir / "new_file.mp3"
        create_test_audio_file(
            new_file, artist="Artist", title="Song [Official Video]", format="mp3"
        )

        # Mock user input to skip
        with patch("builtins.input", return_value="s"):
            result = check_file_duplicate(new_file, temp_output_dir, "interactive")
            assert result is True  # Should detect as duplicate despite junk

    def test_feat_variations_matching(self, temp_output_dir, create_test_audio_file):
        """Test that feat. variations are normalized."""
        # Create existing file
        existing = temp_output_dir / "Artist - Song.mp3"
        create_test_audio_file(
            existing, artist="Artist", title="Song (feat. Other)", format="mp3"
        )

        # Create new file with different feat. format
        new_file = temp_output_dir / "new_file.mp3"
        create_test_audio_file(
            new_file, artist="Artist", title="Song ft. Other", format="mp3"
        )

        # Mock user input to skip
        with patch("builtins.input", return_value="s"):
            result = check_file_duplicate(new_file, temp_output_dir, "interactive")
            assert result is True  # Should detect as duplicate

    def test_not_duplicate_different_title(
        self, temp_output_dir, create_test_audio_file
    ):
        """Test that different titles are not flagged as duplicates."""
        # Create existing file
        existing = temp_output_dir / "Artist - Song1.mp3"
        create_test_audio_file(existing, artist="Artist", title="Song1", format="mp3")

        # Create new file with different title
        new_file = temp_output_dir / "new_file.mp3"
        create_test_audio_file(new_file, artist="Artist", title="Song2", format="mp3")

        result = check_file_duplicate(new_file, temp_output_dir, "interactive")
        assert result is False  # Not a duplicate

    def test_not_duplicate_remix(self, temp_output_dir, create_test_audio_file):
        """Test that remixes are not flagged as duplicates."""
        # Create existing file
        existing = temp_output_dir / "Artist - Song.mp3"
        create_test_audio_file(existing, artist="Artist", title="Song", format="mp3")

        # Create remix version
        new_file = temp_output_dir / "new_file.mp3"
        create_test_audio_file(
            new_file, artist="Artist", title="Song (Remix)", format="mp3"
        )

        result = check_file_duplicate(new_file, temp_output_dir, "interactive")
        assert result is False  # Not a duplicate (different version)

    def test_interactive_keep_both(self, temp_output_dir, create_test_audio_file):
        """Test interactive mode - keep both files."""
        # Create existing file
        existing = temp_output_dir / "Artist - Song.mp3"
        create_test_audio_file(existing, artist="Artist", title="Song", format="mp3")

        # Create duplicate
        new_file = temp_output_dir / "new_file.mp3"
        create_test_audio_file(new_file, artist="Artist", title="Song", format="mp3")

        # Mock user input to keep both
        with patch("builtins.input", return_value="k"):
            result = check_file_duplicate(new_file, temp_output_dir, "interactive")
            assert result is False  # Don't skip (keep both)

    def test_interactive_replace(self, temp_output_dir, create_test_audio_file):
        """Test interactive mode - replace existing file."""
        # Create existing file
        existing = temp_output_dir / "Artist - Song.mp3"
        create_test_audio_file(existing, artist="Artist", title="Song", format="mp3")

        # Create new file (better quality)
        new_file = temp_output_dir / "new_file.mp3"
        create_test_audio_file(new_file, artist="Artist", title="Song", format="mp3")

        # Mock user input to replace
        with patch("builtins.input", return_value="r"):
            result = check_file_duplicate(new_file, temp_output_dir, "interactive")
            assert result is False  # Don't skip (will replace)
            assert not existing.exists()  # Old file should be deleted

    def test_skip_mode(self, temp_output_dir, create_test_audio_file):
        """Test skip mode - automatically skip duplicates."""
        # Create existing file
        existing = temp_output_dir / "Artist - Song.mp3"
        create_test_audio_file(existing, artist="Artist", title="Song", format="mp3")

        # Create duplicate
        new_file = temp_output_dir / "new_file.mp3"
        create_test_audio_file(new_file, artist="Artist", title="Song", format="mp3")

        result = check_file_duplicate(new_file, temp_output_dir, "skip")
        assert result is True  # Should skip automatically

    def test_keep_mode(self, temp_output_dir, create_test_audio_file):
        """Test keep mode - automatically keep all duplicates."""
        # Create existing file
        existing = temp_output_dir / "Artist - Song.mp3"
        create_test_audio_file(existing, artist="Artist", title="Song", format="mp3")

        # Create duplicate
        new_file = temp_output_dir / "new_file.mp3"
        create_test_audio_file(new_file, artist="Artist", title="Song", format="mp3")

        result = check_file_duplicate(new_file, temp_output_dir, "keep")
        assert result is False  # Should keep automatically

    def test_scan_library(self, temp_output_dir, create_test_audio_file):
        """Test scanning directory for all duplicates."""
        # Create multiple files with some duplicates
        create_test_audio_file(
            temp_output_dir / "file1.mp3", artist="Artist1", title="Song1", format="mp3"
        )
        create_test_audio_file(
            temp_output_dir / "file2.mp3", artist="Artist1", title="Song1", format="mp3"
        )  # Duplicate
        create_test_audio_file(
            temp_output_dir / "file3.m4a", artist="Artist2", title="Song2", format="m4a"
        )
        create_test_audio_file(
            temp_output_dir / "file4.mp3", artist="Artist2", title="Song2", format="mp3"
        )  # Cross-format duplicate

        duplicates = scan_library(temp_output_dir)

        # Should find 2 duplicate groups
        assert len(duplicates) == 2

    def test_missing_metadata_no_duplicate(
        self, temp_output_dir, create_test_audio_file
    ):
        """Test that files with missing metadata don't cause false positives."""
        # Create existing file with metadata
        existing = temp_output_dir / "Artist - Song.mp3"
        create_test_audio_file(existing, artist="Artist", title="Song", format="mp3")

        # Create new file without metadata
        new_file = temp_output_dir / "new_file.mp3"
        create_test_audio_file(new_file, artist=None, title=None, format="mp3")

        result = check_file_duplicate(new_file, temp_output_dir, "interactive")
        assert result is False  # Can't be duplicate without metadata
