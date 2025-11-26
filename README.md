# Track Manager

Universal audio track downloader with smart duplicate detection and metadata management.

Download music from **any source** - Spotify, YouTube, SoundCloud, or direct URLs - with a single command.

## Features

- 🎵 **Universal downloads** - Works with Spotify, YouTube, SoundCloud, and direct audio URLs
- 🔍 **Smart duplicate detection** - Finds duplicates across formats (M4A vs MP3)
- 🤝 **Interactive handling** - You choose: skip, keep both, or replace duplicates
- 📝 **Metadata management** - Review and fix problematic metadata via CSV workflow
- 📊 **Playlist support** - Handles large playlists with progress tracking
- 🔄 **Error resilience** - Logs failures, continues downloading
- 🎚️ **Quality preservation** - Best available bitrate, no destructive transcoding
- ⚙️ **Configurable** - Customize output directory, behavior, and preferences

## Installation

### Requirements

- Python 3.8+
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [spotdl](https://github.com/spotDL/spotify-downloader) (for Spotify)
- curl (usually pre-installed)
- ffmpeg (for format conversion)

### Setup

1. **Install system dependencies:**
```bash
# macOS
brew install yt-dlp ffmpeg

# Linux (Debian/Ubuntu)
sudo apt install yt-dlp ffmpeg curl

# Or install yt-dlp via pip
pip install yt-dlp
```

2. **Install spotdl** (for Spotify support):
```bash
pip install spotdl
```

3. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure:**
```bash
cp config.example.yaml config.yaml
# Edit config.yaml with your preferences
```

5. **Verify installation:**
```bash
track-manager check-setup
# Or if not installed:
python -m track_manager check-setup
```

## Configuration

Edit `config.yaml` to customize:

- **Output directory** - Where tracks are saved
- **Failed downloads log** - Where errors are logged
- **Metadata review CSV** - Where problematic metadata is flagged
- **Spotdl path** - Custom spotdl location (or use system PATH)
- **Default format** - M4A (default) or MP3
- **Playlist threshold** - Confirmation for large playlists
- **Duplicate handling** - Interactive (default), skip, or keep

See `config.example.yaml` for all options.

## Usage

### Basic Download

```bash
# Universal command - works with any source
track-manager download "<url>"

# Examples
track-manager download "https://open.spotify.com/track/..."
track-manager download "https://www.youtube.com/watch?v=..."
track-manager download "https://soundcloud.com/artist/track"
track-manager download "https://example.com/audio.mp3"
```

### Format Selection

```bash
# Force M4A
track-manager download "<url>" --format m4a

# Force MP3
track-manager download "<url>" --format mp3

# Auto (default) - prefers M4A, accepts best available
track-manager download "<url>"
```

### Playlists

```bash
# Spotify playlist
track-manager download "https://open.spotify.com/playlist/..."

# YouTube playlist
track-manager download "https://www.youtube.com/playlist?list=..."

# SoundCloud set
track-manager download "https://soundcloud.com/user/sets/..."
```

Playlists >50 tracks will prompt for confirmation.

### Metadata Management

**Check for duplicates:**
```bash
track-manager check-duplicates --file <path>
```

**Scan library for duplicates:**
```bash
track-manager check-duplicates
```

**Verify metadata quality:**
```bash
track-manager verify-metadata
```

**Review problematic metadata:**
```bash
# View pending reviews
track-manager apply-metadata --show

# Edit CSV file to fix metadata
# File location configured in config.yaml

# Apply fixes
track-manager apply-metadata
```

## How It Works

### Source Detection

The main script detects the source from the URL:
- **Spotify** → Uses spotdl to find YouTube URLs, downloads with yt-dlp
- **YouTube** → Direct download with yt-dlp
- **SoundCloud** → Uses yt-dlp (has SoundCloud support)
- **Direct URLs** → Downloads with curl, converts if needed

### Duplicate Detection

- Extracts metadata (artist + title) from audio files
- Normalizes metadata (removes junk patterns, handles variations)
- Compares across formats (finds MP3 duplicate of M4A file)
- Interactive prompt: skip, keep both, or replace

### Metadata Review

When metadata is missing or problematic:
1. Track is flagged to CSV file
2. You edit CSV to provide correct metadata
3. Run apply script to update files
4. Processed rows are removed from CSV

### Error Handling

- Failed downloads are logged with timestamp and error
- Download continues with next track
- Failed URLs can be retried later

## Supported Sources

| Source | Tracks | Playlists | Albums | Notes |
|--------|--------|-----------|--------|-------|
| Spotify | ✅ | ✅ | ✅ | Via spotdl → yt-dlp |
| YouTube | ✅ | ✅ | ❌ | Direct via yt-dlp |
| SoundCloud | ✅ | ✅ | ✅ | Via yt-dlp |
| Direct URLs | ✅ | ❌ | ❌ | Any audio format |

## Architecture

## Testing

### Running Tests

```bash
# Install test dependencies
pip install -r requirements.txt

# Run all tests
./run_tests.sh

# Run with coverage report
./run_tests.sh --cov

# Run specific test file
./run_tests.sh tests/unit/test_config_reader.py

# Run tests matching pattern
./run_tests.sh -k "normalize"
```

### Test Structure

- `tests/unit/` - Unit tests for individual modules
- `tests/integration/` - Integration tests for workflows
- `tests/fixtures/` - Test data and fixtures

### Writing Tests

Tests use pytest. See existing tests in `tests/unit/` for examples.

```python
# Example test
def test_something():
    result = my_function()
    assert result == expected
```

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Write tests for new features
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - See LICENSE file for details.

## Architecture Decisions

### Library Choices

**Why we use yt-dlp for both YouTube and SoundCloud:**

yt-dlp is a universal downloader with **native support** for 1000+ sites, including YouTube and SoundCloud. It's not "forcing through YouTube" - it downloads directly from each source using their respective APIs.

- **YouTube**: yt-dlp with native YouTube support
- **SoundCloud**: yt-dlp with native SoundCloud support  
- **Spotify**: spotdl (native Spotify API)
- **Direct URLs**: requests (HTTP download)

**Key improvement from bash version:**
- ❌ Old: Spotify → find on YouTube → download (unnecessary conversion)
- ✅ New: Spotify → spotdl → direct download (native API)

**Why not dedicated SoundCloud libraries?**
- yt-dlp's SoundCloud support is mature and actively maintained
- Fewer dependencies = easier installation
- Proven reliability with millions of users
- Already required for YouTube anyway

Each source is handled appropriately - we're not forcing conversions or workarounds.
