"""Unit tests for track_metadata module."""

import pytest
from pathlib import Path
import sys

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

# Import after adding to path
import track_metadata


def test_normalize_text_basic():
    """Test basic text normalization."""
    assert track_metadata.normalize_text("Artist Name") == "artist name"
    assert track_metadata.normalize_text("ARTIST NAME") == "artist name"


def test_normalize_text_removes_junk():
    """Test that junk patterns are removed."""
    test_cases = [
        ("Track Name [Official Video]", "track name"),
        ("Track Name (Official Video)", "track name"),
        ("Track Name [Official Audio]", "track name"),
        ("Track Name (Music Video)", "track name"),
        ("Track Name [HD]", "track name"),
        ("Track Name (HD)", "track name"),
    ]
    
    for input_text, expected in test_cases:
        assert track_metadata.normalize_text(input_text) == expected


def test_normalize_text_feat_variations():
    """Test that featuring variations are normalized."""
    test_cases = [
        ("Artist ft. Guest", "artist feat. guest"),
        ("Artist feat. Guest", "artist feat. guest"),
        ("Artist (ft. Guest)", "artist feat. guest"),
        ("Artist featuring Guest", "artist feat. guest"),
    ]
    
    for input_text, expected in test_cases:
        assert track_metadata.normalize_text(input_text) == expected


def test_normalize_text_artist_separators():
    """Test that artist separators are normalized."""
    test_cases = [
        ("Artist x Guest", "artist vs. guest"),
        ("Artist & Guest", "artist vs. guest"),
        ("Artist vs Guest", "artist vs. guest"),
        ("Artist vs. Guest", "artist vs. guest"),
    ]
    
    for input_text, expected in test_cases:
        assert track_metadata.normalize_text(input_text) == expected


def test_normalize_text_whitespace():
    """Test that extra whitespace is cleaned up."""
    assert track_metadata.normalize_text("Artist   Name") == "artist name"
    assert track_metadata.normalize_text(" Artist Name ") == "artist name"
    assert track_metadata.normalize_text("Artist\nName") == "artist name"


def test_normalize_metadata():
    """Test normalizing artist and title together."""
    artist, title = track_metadata.normalize_metadata("Artist Name", "Track Title")
    assert artist == "artist name"
    assert title == "track title"


def test_normalize_metadata_with_none():
    """Test normalizing with None values."""
    artist, title = track_metadata.normalize_metadata(None, "Track Title")
    assert artist == ""
    assert title == "track title"
    
    artist, title = track_metadata.normalize_metadata("Artist", None)
    assert artist == "artist"
    assert title == ""


def test_has_junk_patterns():
    """Test junk pattern detection."""
    assert track_metadata.has_junk_patterns("Track [Official Video]")
    assert track_metadata.has_junk_patterns("Track (Official Audio)")
    assert track_metadata.has_junk_patterns("Track [HD]")
    assert track_metadata.has_junk_patterns("Track - Music Video")
    
    assert not track_metadata.has_junk_patterns("Clean Track Name")
    assert not track_metadata.has_junk_patterns("Artist - Title")


def test_sanitize_filename():
    """Test filename sanitization in apply_metadata_csv."""
    # Import the function from apply_metadata_csv
    sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))
    from apply_metadata_csv import sanitize_filename
    
    test_cases = [
        ("Artist/Name", "Artist-Name"),
        ("Track:Name", "Track-Name"),
        ("Track*Name", "Track-Name"),
        ("Track?Name", "Track-Name"),
        ('Track"Name', "Track-Name"),
        ("Track<Name>", "Track-Name"),
        ("Track|Name", "Track-Name"),
        (".Track Name.", "Track Name"),
    ]
    
    for input_text, expected in test_cases:
        assert sanitize_filename(input_text) == expected
