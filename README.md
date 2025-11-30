# Track Manager

[![built using gptme](https://img.shields.io/badge/built%20using-gptme%20%F0%9F%A4%96-5151f5?style=flat)](https://github.com/ErikBjare/gptme)

Universal music downloader with smart duplicate detection and metadata management.

Download tracks from **Spotify, YouTube, SoundCloud, or direct URLs** with automatic source detection, duplicate prevention, and professional metadata handling.

## Features

- 🎯 **Universal Source Support** - Spotify, YouTube, SoundCloud, direct URLs
- 🔍 **Smart Duplicate Detection** - Works across formats (M4A vs MP3)
- 📝 **Metadata Management** - CSV-based review and correction workflow
- 🤝 **Interactive Prompts** - Asks what to do when duplicates found
- 📊 **Playlist Support** - Handles playlists/albums with progress tracking
- 🔄 **Error Resilience** - Logs failed downloads, continues on errors
- 🎚️ **Best Quality** - Always downloads best available bitrate
- 🌍 **Cross-Platform** - Works on macOS, Linux, Windows

## Installation

### From Source (Recommended)

```bash
# Clone the repository
git clone https://github.com/Nattverket/track-manager.git
cd track-manager

# Install the package
pip install -e .
```

### Direct from GitHub

```bash
# Install directly from GitHub
pip install git+https://github.com/Nattverket/track-manager.git
```

### Using uv (Fast Alternative)

```bash
# Install uv if not available
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install track-manager
uv pip install git+https://github.com/Nattverket/track-manager.git
```

## Quick Start

### Download Tracks

```bash
# Download from Spotify
track-manager download "https://open.spotify.com/track/..."

# Download from YouTube
track-manager download "https://www.youtube.com/watch?v=..."

# Download from SoundCloud
track-manager download "https://soundcloud.com/artist/track"

# Download from direct URL
track-manager download "https://example.com/audio.mp3"
```

### Manage Your Library

```bash
# Check for duplicate tracks
track-manager check-duplicates

# Verify installation and setup
track-manager check-setup

# Get help
track-manager --help
```

## Configuration

Track Manager uses sensible defaults, but you can customize settings by creating a `config.yaml` file:

```yaml
# Copy from config.example.yaml and customize
output_dir: "~/Documents/projects/DJ/tracks"
failed_log: "~/Documents/projects/DJ/failed-downloads.txt"
```

## Supported Sources

### Spotify

- Tracks: `https://open.spotify.com/track/...`
- Playlists: `https://open.spotify.com/playlist/...`
- Albums: `https://open.spotify.com/album/...`

### YouTube

- Videos: `https://www.youtube.com/watch?v=...`
- Playlists: `https://www.youtube.com/playlist?list=...`

### SoundCloud

- Tracks: `https://soundcloud.com/artist/track`
- Sets: `https://soundcloud.com/artist/sets/playlist`

### Direct Audio URLs

- Any direct audio file URL: `https://example.com/audio.mp3`

## Duplicate Detection

Track Manager intelligently detects duplicates by:

- Comparing artist + title from ID3/M4A tags (not filenames)
- Normalizing metadata (removes "[Official Video]", handles "feat." variations)
- Working across formats (finds M4A duplicates of MP3 files)
- Case-insensitive matching

When a duplicate is found, you'll be prompted to:

- Skip new file (keep existing)
- Keep both files
- Replace existing with new file

## Metadata Management

When metadata is missing or problematic, tracks are flagged for manual review:

1. Download script flags tracks with issues
2. Edit `tracks-metadata-review.csv` to fill in correct metadata
3. Run `track-manager apply-metadata` to update files

## Error Handling

Failed downloads are logged to `failed-downloads.txt` with timestamps and error messages. You can retry failed URLs later.

## Development

For development, install with dev dependencies:

```bash
git clone https://github.com/Nattverket/track-manager.git
cd track-manager
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=track_manager
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
