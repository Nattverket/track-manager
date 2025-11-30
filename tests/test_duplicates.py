"""Tests for duplicate detection functionality."""

import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from track_manager.duplicates import (
    normalize_text,
    extract_metadata,
    normalize_metadata,
    find_duplicates,
    check_file_duplicate,
    scan_library,
)


class TestNormalizeText:
    """Test text normalization for duplicate detection."""

    def test_normalize_text_basic(self):
        """Test basic text normalization."""
        assert normalize_text("Hello World") == "hello world"
        assert normalize_text("  HELLO   WORLD  ") == "hello world"

    def test_normalize_text_remove_junk_patterns(self):
        """Test removal of common junk patterns."""
        assert normalize_text("Song [Official Video]") == "song"
        assert normalize_text("Track (Official Audio)") == "track"
        assert normalize_text("Title [HD]") == "title"
        assert normalize_text("Name (HD)") == "name"

    def test_normalize_text_featuring_variations(self):
        """Test normalization of featuring variations."""
        assert normalize_text("Artist ft. Other") == "artist feat. other"
        assert normalize_text("Artist Feat. Other") == "artist feat. other"
        assert normalize_text("Artist featuring Other") == "artist feat. other"
        assert normalize_text("Artist (ft. Other)") == "artist feat. other"

    def test_normalize_text_artist_separators(self):
        """Test normalization of artist separators."""
        assert normalize_text("Artist x Other") == "artist vs. other"
        assert normalize_text("Artist & Other") == "artist vs. other"
        assert normalize_text("Artist vs Other") == "artist vs. other"


class TestExtractMetadata:
    """Test metadata extraction from audio files."""

    def test_extract_metadata_nonexistent_file(self):
        """Test metadata extraction from nonexistent file."""
        artist, title = extract_metadata(Path("/nonexistent/file.mp3"))
        assert artist is None
        assert title is None

    @patch("track_manager.duplicates.MutagenFile")
    def test_extract_metadata_success(self, mock_mutagen):
        """Test successful metadata extraction."""
        # Create a simpler mock that directly returns the values we need
        mock_audio = MagicMock()
        mock_audio.__bool__ = lambda self: True
        
        # Mock the get method to return our test values
        def get_mock(key):
            if key == "artist":
                return ["Test Artist"]
            elif key == "title":
                return ["Test Title"]
            else:
                return [None]
        mock_audio.get = get_mock
        
        # Mock the 'in' operator
        mock_audio.__contains__ = lambda self, key: key in ["artist", "title"]
        
        # Set the mock mutagen to return our mock audio object
        mock_mutagen.return_value = mock_audio

        artist, title = extract_metadata(Path("test.mp3"))
        
        # Verify mutagen was called correctly
        mock_mutagen.assert_called_once_with("test.mp3", easy=True)
        
        assert artist == "Test Artist"
        assert title == "Test Title"

    @patch("track_manager.duplicates.MutagenFile")
    def test_extract_metadata_missing_fields(self, mock_mutagen):
        """Test metadata extraction with missing fields."""
        # Mock mutagen file with missing metadata
        mock_audio = MagicMock()
        mock_audio.get.return_value = [None]
        mock_mutagen.return_value = mock_audio

        artist, title = extract_metadata(Path("test.mp3"))
        assert artist is None
        assert title is None


class TestNormalizeMetadata:
    """Test metadata normalization."""

    def test_normalize_metadata_basic(self):
        """Test basic metadata normalization."""
        artist, title = normalize_metadata("Test Artist", "Test Title")
        assert artist == "test artist"
        assert title == "test title"

    def test_normalize_metadata_with_junk(self):
        """Test metadata normalization with junk patterns."""
        artist, title = normalize_metadata("Artist [Official]", "Title [Video]")
        assert artist == "artist"
        assert title == "title"

    def test_normalize_metadata_none_values(self):
        """Test metadata normalization with None values."""
        artist, title = normalize_metadata(None, "Test Title")
        assert artist == ""
        assert title == "test title"

        artist, title = normalize_metadata("Test Artist", None)
        assert artist == "test artist"
        assert title == ""


class TestFindDuplicates:
    """Test duplicate finding functionality."""

    def test_find_duplicates_no_metadata(self):
        """Test duplicate finding with no metadata."""
        with tempfile.TemporaryDirectory() as tmpdir:
            library_dir = Path(tmpdir)
            duplicates = find_duplicates("", "", library_dir)
            assert duplicates == []

    @patch("track_manager.duplicates.extract_metadata")
    def test_find_duplicates_no_matches(self, mock_extract):
        """Test duplicate finding with no matches."""
        with tempfile.TemporaryDirectory() as tmpdir:
            library_dir = Path(tmpdir)
            
            # Create a test file
            test_file = library_dir / "test.mp3"
            test_file.touch()
            
            # Mock different metadata for existing file
            mock_extract.return_value = ("Different Artist", "Different Title")
            
            duplicates = find_duplicates("Test Artist", "Test Title", library_dir)
            assert duplicates == []

    @patch("track_manager.duplicates.extract_metadata")
    def test_find_duplicates_with_matches(self, mock_extract):
        """Test duplicate finding with matches."""
        with tempfile.TemporaryDirectory() as tmpdir:
            library_dir = Path(tmpdir)
            
            # Create test files
            file1 = library_dir / "file1.mp3"
            file2 = library_dir / "file2.m4a"
            file1.touch()
            file2.touch()
            
            # Mock same metadata for both files
            mock_extract.return_value = ("Test Artist", "Test Title")
            
            duplicates = find_duplicates("Test Artist", "Test Title", library_dir)
            assert len(duplicates) == 2
            assert file1 in duplicates
            assert file2 in duplicates


class TestCheckFileDuplicate:
    """Test file duplicate checking."""

    @patch("track_manager.duplicates.find_duplicates")
    @patch("track_manager.duplicates.extract_metadata")
    def test_check_file_duplicate_no_duplicates(self, mock_extract, mock_find):
        """Test duplicate check with no duplicates."""
        mock_extract.return_value = ("Test Artist", "Test Title")
        mock_find.return_value = []
        
        with tempfile.TemporaryDirectory() as tmpdir:
            library_dir = Path(tmpdir)
            file_path = library_dir / "test.mp3"
            
            should_skip = check_file_duplicate(file_path, library_dir, "skip")
            assert should_skip is False

    @patch("track_manager.duplicates.find_duplicates")
    @patch("track_manager.duplicates.extract_metadata")
    def test_check_file_duplicate_skip_mode(self, mock_extract, mock_find):
        """Test duplicate check in skip mode."""
        with tempfile.TemporaryDirectory() as tmpdir:
            library_dir = Path(tmpdir)
            file_path = library_dir / "test.mp3"
            duplicate_path = library_dir / "duplicate.mp3"
            
            # Mock metadata extraction
            mock_extract.return_value = ("Test Artist", "Test Title")
            mock_find.return_value = [duplicate_path]
            
            should_skip = check_file_duplicate(file_path, library_dir, "skip")
            assert should_skip is True

    @patch("track_manager.duplicates.find_duplicates")
    @patch("track_manager.duplicates.extract_metadata")
    def test_check_file_duplicate_keep_mode(self, mock_extract, mock_find):
        """Test duplicate check in keep mode."""
        with tempfile.TemporaryDirectory() as tmpdir:
            library_dir = Path(tmpdir)
            file_path = library_dir / "test.mp3"
            duplicate_path = library_dir / "duplicate.mp3"
            
            # Mock metadata extraction
            mock_extract.return_value = ("Test Artist", "Test Title")
            mock_find.return_value = [duplicate_path]
            
            should_skip = check_file_duplicate(file_path, library_dir, "keep")
            assert should_skip is False

    @patch("track_manager.duplicates.find_duplicates")
    @patch("track_manager.duplicates.extract_metadata")
    @patch("builtins.input")
    def test_check_file_duplicate_interactive_skip(self, mock_input, mock_extract, mock_find):
        """Test duplicate check in interactive mode with skip choice."""
        with tempfile.TemporaryDirectory() as tmpdir:
            library_dir = Path(tmpdir)
            file_path = library_dir / "test.mp3"
            duplicate_path = library_dir / "duplicate.mp3"
            
            # Mock metadata extraction
            mock_extract.return_value = ("Test Artist", "Test Title")
            mock_find.return_value = [duplicate_path]
            mock_input.return_value = "s"  # Skip
            
            should_skip = check_file_duplicate(file_path, library_dir, "interactive")
            assert should_skip is True

    @patch("track_manager.duplicates.find_duplicates")
    @patch("track_manager.duplicates.extract_metadata")
    @patch("builtins.input")
    def test_check_file_duplicate_interactive_keep(self, mock_input, mock_extract, mock_find):
        """Test duplicate check in interactive mode with keep choice."""
        with tempfile.TemporaryDirectory() as tmpdir:
            library_dir = Path(tmpdir)
            file_path = library_dir / "test.mp3"
            duplicate_path = library_dir / "duplicate.mp3"
            
            # Mock metadata extraction
            mock_extract.return_value = ("Test Artist", "Test Title")
            mock_find.return_value = [duplicate_path]
            mock_input.return_value = "k"  # Keep
            
            should_skip = check_file_duplicate(file_path, library_dir, "interactive")
            assert should_skip is False

    @patch("track_manager.duplicates.find_duplicates")
    @patch("track_manager.duplicates.extract_metadata")
    @patch("builtins.input")
    def test_check_file_duplicate_interactive_replace(self, mock_input, mock_extract, mock_find):
        """Test duplicate check in interactive mode with replace choice."""
        with tempfile.TemporaryDirectory() as tmpdir:
            library_dir = Path(tmpdir)
            file_path = library_dir / "test.mp3"
            duplicate_path = library_dir / "duplicate.mp3"
            
            # Create the duplicate file so it can be deleted
            duplicate_path.touch()
            
            # Mock metadata extraction
            mock_extract.return_value = ("Test Artist", "Test Title")
            mock_find.return_value = [duplicate_path]
            mock_input.return_value = "r"  # Replace
            
            should_skip = check_file_duplicate(file_path, library_dir, "interactive")
            assert should_skip is False


class TestScanLibrary:
    """Test library scanning for duplicates."""

    @patch("track_manager.duplicates.extract_metadata")
    def test_scan_library_no_duplicates(self, mock_extract):
        """Test library scan with no duplicates."""
        with tempfile.TemporaryDirectory() as tmpdir:
            library_dir = Path(tmpdir)
            
            # Create files with different metadata
            file1 = library_dir / "file1.mp3"
            file2 = library_dir / "file2.m4a"
            file1.touch()
            file2.touch()
            
            # Mock different metadata for each file
            mock_extract.side_effect = [
                ("Artist1", "Title1"),
                ("Artist2", "Title2"),
            ]
            
            duplicates = scan_library(library_dir)
            assert duplicates == {}

    @patch("track_manager.duplicates.extract_metadata")
    def test_scan_library_with_duplicates(self, mock_extract):
        """Test library scan with duplicates."""
        with tempfile.TemporaryDirectory() as tmpdir:
            library_dir = Path(tmpdir)
            
            # Create files with same metadata
            file1 = library_dir / "file1.mp3"
            file2 = library_dir / "file2.m4a"
            file1.touch()
            file2.touch()
            
            # Mock same metadata for both files
            mock_extract.return_value = ("Test Artist", "Test Title")
            
            duplicates = scan_library(library_dir)
            assert len(duplicates) == 1
            key = "test artist|||test title"
            assert key in duplicates
            assert len(duplicates[key]) == 2
