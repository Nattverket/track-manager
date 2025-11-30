"""Unit tests for config_reader module."""

import os
import sys
from pathlib import Path

import pytest

# Import from track_manager package
from track_manager.config import Config


@pytest.fixture
def sample_config_file(tmp_path):
    """Create a sample config file for testing."""
    config_content = """
output_dir: "~/test/tracks"
failed_log: "~/test/failed.txt"
metadata_csv: "~/test/metadata.csv"

spotdl:
  path: "/usr/local/bin/spotdl"

downloads:
  default_format: "m4a"
  playlist_confirmation_threshold: 100
  best_quality: true

duplicates:
  handling: "skip"
"""
    config_file = tmp_path / "config.yaml"
    config_file.write_text(config_content)
    return config_file


def test_config_loads_file(sample_config_file):
    """Test that config loads from file."""
    config = Config(sample_config_file)
    assert config.config is not None


def test_config_expands_home_directory(sample_config_file):
    """Test that ~ is expanded in paths."""
    config = Config(sample_config_file)
    assert not str(config.output_dir).startswith("~")
    assert str(config.output_dir).startswith(os.path.expanduser("~"))


def test_config_get_top_level(sample_config_file):
    """Test getting top-level config values."""
    config = Config(sample_config_file)
    assert "test/tracks" in str(config.get("output_dir"))


def test_config_get_nested(sample_config_file):
    """Test getting nested config values."""
    config = Config(sample_config_file)
    assert config.get("spotdl.path") == "/usr/local/bin/spotdl"
    assert config.get("downloads.default_format") == "m4a"
    assert config.get("downloads.playlist_confirmation_threshold") == 100


def test_config_get_with_default(sample_config_file):
    """Test getting config with default value."""
    config = Config(sample_config_file)
    assert config.get("nonexistent.key", "default") == "default"


def test_config_properties(sample_config_file):
    """Test config property accessors."""
    config = Config(sample_config_file)

    assert isinstance(config.output_dir, Path)
    assert "test/tracks" in str(config.output_dir)

    assert isinstance(config.failed_log, Path)
    assert "failed.txt" in str(config.failed_log)

    assert isinstance(config.metadata_csv, Path)
    assert "metadata.csv" in str(config.metadata_csv)

    assert config.spotdl_path == "/usr/local/bin/spotdl"
    assert config.default_format == "m4a"
    assert config.playlist_threshold == 100
    assert config.duplicate_handling == "skip"


def test_config_missing_file():
    """Test handling of missing config file."""
    Config.reset()  # Reset singleton for this test
    with pytest.raises(SystemExit):
        Config(Path("/nonexistent/config.yaml"))


def test_config_empty_spotdl_path(tmp_path):
    """Test that empty spotdl path returns None."""
    Config.reset()  # Reset singleton for this test
    config_content = """
output_dir: "~/test/tracks"
spotdl:
  path: ""
"""
    config_file = tmp_path / "config.yaml"
    config_file.write_text(config_content)

    config = Config(config_file)
    assert config.spotdl_path is None
