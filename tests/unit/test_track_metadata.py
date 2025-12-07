"""Unit tests for track_metadata module."""

import sys
from pathlib import Path

import pytest

from track_manager.duplicates import normalize_metadata, normalize_text

# Import from track_manager package
from track_manager.metadata import has_junk_patterns, sanitize_filename


def test_normalize_text_basic():
    """Test basic text normalization."""
    assert normalize_text("Artist Name") == "artist name"
    assert normalize_text("ARTIST NAME") == "artist name"


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
        assert normalize_text(input_text) == expected


def test_normalize_text_feat_variations():
    """Test that featuring variations are normalized."""
    test_cases = [
        ("Artist ft. Guest", "artist feat. guest"),
        ("Artist feat. Guest", "artist feat. guest"),
        ("Artist (ft. Guest)", "artist feat. guest"),
        ("Artist featuring Guest", "artist feat. guest"),
    ]

    for input_text, expected in test_cases:
        assert normalize_text(input_text) == expected


def test_normalize_text_whitespace():
    """Test that extra whitespace is cleaned up."""
    assert normalize_text("Artist   Name") == "artist name"
    assert normalize_text(" Artist Name ") == "artist name"
    assert normalize_text("Artist\nName") == "artist name"


def test_normalize_metadata():
    """Test normalizing artist and title together."""
    artist, title = normalize_metadata("Artist Name", "Track Title")
    assert artist == "artist name"
    assert title == "track title"


def test_normalize_metadata_with_none():
    """Test normalizing with None values."""
    artist, title = normalize_metadata(None, "Track Title")
    assert artist == ""
    assert title == "track title"

    artist, title = normalize_metadata("Artist", None)
    assert artist == "artist"
    assert title == ""


def test_has_junk_patterns():
    """Test junk pattern detection."""
    assert has_junk_patterns("Track [Official Video]")
    assert has_junk_patterns("Track (Official Audio)")
    assert has_junk_patterns("Track [HD]")
    assert has_junk_patterns("Track - Music Video")

    assert not has_junk_patterns("Clean Track Name")
    assert not has_junk_patterns("Artist - Title")


def test_sanitize_filename():
    """Test filename sanitization in apply_metadata_csv."""
    # Use the sanitize_filename function from metadata module
    # (already imported at the top of the file)

    test_cases = [
        ("Artist/Name", "Artist-Name"),
        ("Track:Name", "Track-Name"),
        ("Track*Name", "Track-Name"),
        ("Track?Name", "Track-Name"),
        ('Track"Name', "Track-Name"),
        ("Track<Name>", "Track-Name-"),  # Both < and > get replaced
        ("Track|Name", "Track-Name"),
        (".Track Name.", "Track Name"),
    ]

    for input_text, expected in test_cases:
        assert sanitize_filename(input_text) == expected
