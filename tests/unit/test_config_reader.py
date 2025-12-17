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
    Config.reset()
    config = Config(sample_config_file)
    assert config.config is not None


def test_config_expands_home_directory(sample_config_file):
    """Test that ~ is expanded in paths."""
    Config.reset()
    config = Config(sample_config_file)
    output_dir_str = str(config.output_dir)
    assert not output_dir_str.startswith("~")
    # Path should be expanded (contains 'test/tracks' somewhere)
    assert "test/tracks" in output_dir_str


def test_config_get_top_level(sample_config_file):
    """Test getting top-level config values."""
    Config.reset()
    config = Config(sample_config_file)
    output_dir = config.get("output_dir")
    # After expansion, ~ is replaced with home directory
    assert "test/tracks" in str(output_dir)
    assert not str(output_dir).startswith("~")


def test_config_get_nested(sample_config_file):
    """Test getting nested config values."""
    Config.reset()
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
    Config.reset()
    config = Config(sample_config_file)

    assert isinstance(config.output_dir, Path)
    assert "test/tracks" in str(config.output_dir)

    assert isinstance(config.failed_log, Path)
    assert "failed.txt" in str(config.failed_log)

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
