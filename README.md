# Track Manager

[![Unit Tests](https://github.com/Nattverket/track-manager/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/Nattverket/track-manager/actions/workflows/unit-tests.yml)

Universal audio track downloader with smart duplicate detection and metadata management.

Download music from **any source** - Spotify, YouTube, SoundCloud, or direct URLs - with a single Python command.

## Features

- 🎵 **Universal downloads** - Works with Spotify, YouTube, SoundCloud, and direct audio URLs
- 🔍 **Smart duplicate detection** - Finds duplicates across formats (M4A vs MP3)
- 🤝 **Interactive handling** - You choose: skip, keep both, or replace duplicates
- 📝 **Metadata management** - Review and fix problematic metadata via CSV workflow
- 📊 **Playlist support** - Handles large playlists with progress tracking
- 🔄 **Error resilience** - Logs failures, continues downloading
- 🎚️ **Quality preservation** - Best available bitrate, no destructive transcoding
- ⚙️ **Configurable** - Customize output directory, behavior, and preferences
- 🐍 **Pure Python** - Single pip install, no external CLI tools to manage

## Installation

### Quick Install

```bash
pip install git+https://github.com/Nattverket/track-manager.git
```

### Development Install

```bash
# Clone repository
git clone https://github.com/Nattverket/track-manager.git
cd track-manager

# Install in development mode
pip install -e .

# Install with dev dependencies
pip install -e ".[dev]"
```

### Requirements

- Python 3.8 or higher
- All other dependencies are installed automatically via pip:
  - `yt-dlp` - YouTube and SoundCloud downloads
  - `spotdl` - Spotify downloads (native API)
  - `requests` - Direct URL downloads
  - `mutagen` - Audio metadata handling
  - `pyyaml` - Configuration management
  - `click` - CLI framework

**Note:** `spotdl` may require `ffmpeg` for audio processing. If you encounter errors:
```bash
# macOS
brew install ffmpeg

# Linux (Debian/Ubuntu)
sudo apt install ffmpeg
```

### Verify Installation

```bash
track-manager check-setup
```

## Configuration

Configuration is **optional**. Track Manager works out of the box with sensible defaults.

To customize behavior, create a `config.yaml` file:

```bash
# Copy example configuration
cp config.example.yaml config.yaml

# Edit to customize
# - Output directory
# - Duplicate handling behavior
# - Metadata review preferences
# - Playlist confirmation threshold
```

See `config.example.yaml` for all available options.

**Default behavior without config:**
- Downloads to `~/Documents/projects/DJ/tracks`
- Interactive duplicate handling (prompts for choice)
- Creates metadata review CSV when needed
- Confirms playlists over 50 tracks

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
# Force M4A (default for most sources)
track-manager download "<url>" --format m4a

# Force MP3
track-manager download "<url>" --format mp3

# Auto (default) - uses best available format
track-manager download "<url>"
```

### Custom Output Directory

```bash
# Override configured output directory
track-manager download "<url>" --output /path/to/directory
```

### Playlists

```bash
# Spotify playlist or album
track-manager download "https://open.spotify.com/playlist/..."
track-manager download "https://open.spotify.com/album/..."

# YouTube playlist
track-manager download "https://www.youtube.com/playlist?list=..."

# SoundCloud set or playlist
track-manager download "https://soundcloud.com/user/sets/..."
```

Playlists with more than 50 tracks will prompt for confirmation (configurable).

### Metadata Management

**Check for duplicates:**
```bash
# Check specific file
track-manager check-duplicates --file <path>

# Scan entire library
track-manager check-duplicates
```

**Verify metadata quality:**
```bash
track-manager verify-metadata
```

**Review and fix problematic metadata:**
```bash
# View pending reviews
track-manager apply-metadata --show

# Edit the CSV file to correct metadata
# Default: ~/Documents/projects/DJ/tracks-metadata-review.csv

# Apply corrections
track-manager apply-metadata
```

## How It Works

### Source Detection

Track Manager automatically detects the source from the URL:

- **Spotify** → Uses spotdl with native Spotify API for direct downloads
- **YouTube** → Uses yt-dlp with native YouTube support
- **SoundCloud** → Uses yt-dlp with native SoundCloud support
- **Direct URLs** → Uses Python requests for HTTP downloads

Each source is handled with its appropriate native API - no unnecessary conversions or workarounds.

### Duplicate Detection

1. Extracts metadata (artist + title) from audio file tags
2. Normalizes metadata:
   - Removes junk patterns like "[Official Video]", "(Audio)", "[HD]"
   - Handles "feat." variations
   - Case-insensitive comparison
3. Compares across formats (detects M4A duplicate of MP3)
4. Interactive prompt when duplicate found:
   - Skip new file (keep existing)
   - Keep both files
   - Replace existing with new file

**Note:** Remixes and versions with different titles won't be flagged as duplicates.

### Metadata Review Workflow

When metadata is missing or contains junk patterns:

1. Track is automatically flagged to CSV file
2. You edit CSV to provide correct metadata
3. Run `track-manager apply-metadata` to update files
4. Processed rows are automatically removed from CSV

The CSV file is created only when needed and removed when empty.

### Error Handling

- Failed downloads logged with timestamp and error message
- Download process continues with next track (doesn't stop on errors)
- Failed URLs can be retried later
- Log file location configurable (default: `~/Documents/projects/DJ/failed-downloads.txt`)

## Supported Sources

| Source | Tracks | Playlists | Albums | Implementation |
|--------|--------|-----------|--------|----------------|
| Spotify | ✅ | ✅ | ✅ | spotdl (native API) |
| YouTube | ✅ | ✅ | N/A | yt-dlp (native) |
| SoundCloud | ✅ | ✅ | ✅ | yt-dlp (native) |
| Direct URLs | ✅ | ❌ | ❌ | requests (HTTP) |

## Architecture

### Package Structure

track_manager/
├── __init__.py          # Package initialization
├── __main__.py          # Entry point for python -m track_manager
├── cli.py               # Click-based CLI commands
├── config.py            # Configuration management
├── downloader.py        # Main orchestration logic
├── duplicates.py        # Duplicate detection system
├── metadata.py          # Metadata extraction and review
└── sources/             # Source-specific handlers
    ├── base.py          # Base downloader class
    ├── spotify.py       # Spotify via spotdl
    ├── youtube.py       # YouTube via yt-dlp
    ├── soundcloud.py    # SoundCloud via yt-dlp
    └── direct.py        # Direct URL downloads

### Design Philosophy

1. **Native APIs First**: Each source uses its appropriate library
   - Spotify → spotdl (native Spotify API)
   - YouTube/SoundCloud → yt-dlp (native support for both)
   - Direct URLs → requests (simple HTTP)

2. **Pure Python**: No external CLI tools to install
   - All functionality via Python packages
   - Single `pip install` command
   - Cross-platform by default

3. **Smart Defaults**: Works without configuration
   - Sensible default paths
   - Interactive mode by default
   - Creates required files/directories automatically

4. **User Control**: Interactive prompts for important decisions
   - Duplicate handling (skip/keep/replace)
   - Large playlist confirmation
   - Metadata review workflow

### Data Flow
URL → Downloader.detect_source()
    ↓
Source Handler (spotify/youtube/soundcloud/direct)
    ↓
Download to temp location
    ↓
Extract metadata
    ↓
Check for duplicates → [Interactive prompt if found]
    ↓
Flag for review if metadata issues
    ↓
Move to final location

## Testing

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=track_manager --cov-report=html

# Run specific test file
pytest tests/unit/test_config_reader.py

# Run tests matching pattern
pytest -k "normalize"
```

### Test Structure
tests/
├── unit/              # Unit tests for individual modules
│   ├── test_config_reader.py
│   └── test_track_metadata.py
├── integration/       # Integration tests (to be added)
└── fixtures/          # Test data and fixtures

### Writing Tests

Tests use pytest. Example:

```python
def test_something():
    result = my_function()
    assert result == expected
```

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature-name`)
3. Write tests for new features
4. Ensure all tests pass (`pytest`)
5. Submit a pull request

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Roadmap

### Current Status (v0.1.0)
- ✅ Core download functionality
- ✅ Duplicate detection
- ✅ Metadata management
- ✅ All source handlers (Spotify, YouTube, SoundCloud, Direct)
- ✅ CLI with commands
- ✅ Configuration system

### Planned Features
- 🔲 Publish to PyPI
- 🔲 Additional source support (Bandcamp, Apple Music)
- 🔲 Playlist organization features
- 🔲 Integration tests
- 🔲 Better progress bars
- 🔲 Batch operations
- 🔲 Web UI (optional)

## FAQ

**Q: Do I need to install ffmpeg?**  
A: Usually no. It's only needed if spotdl requires it for Spotify downloads. If you get errors, install it with `brew install ffmpeg` (macOS) or `apt install ffmpeg` (Linux).

**Q: Can I use this without a Spotify account?**  
A: Yes! Spotify downloads work without authentication for most tracks. Some may require a premium account.

**Q: How does duplicate detection work across formats?**  
A: It compares artist + title from audio metadata tags, not filenames. It normalizes both (removes junk, handles variations) and compares case-insensitively. This works across MP3/M4A/etc.

**Q: What happens if a download fails?**  
A: The error is logged to `failed-downloads.txt` and the process continues with the next track. You can retry failed URLs later.

**Q: Can I customize the output directory per download?**  
A: Yes, use `--output /path/to/dir` with the download command.

## Troubleshooting

**Error: "spotdl not found"**
```bash
pip install spotdl
```

**Error: "yt-dlp not found"**
```bash
pip install yt-dlp
```

**Error: "No module named 'track_manager'"**
```bash
# Reinstall the package
pip install --force-reinstall git+https://github.com/Nattverket/track-manager.git
```

**Downloads fail with encoding errors**
```bash
# Try updating yt-dlp
pip install --upgrade yt-dlp
```

## Credits

Built with:
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Universal media downloader
- [spotdl](https://github.com/spotDL/spotify-downloader) - Spotify downloader
- [mutagen](https://github.com/quodlibet/mutagen) - Audio metadata library
- [click](https://click.palletsprojects.com/) - CLI framework
