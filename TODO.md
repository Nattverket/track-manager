# Track Manager - Status & Next Steps

## Current Status (v0.1.0)

✅ **Implementation Complete**

- ✅ Full Python package structure
- ✅ Configuration system (YAML-based with sensible defaults)
- ✅ Professional CLI with click
- ✅ All source handlers implemented:
  - Spotify (native spotdl API)
  - YouTube (yt-dlp Python API)
  - SoundCloud (yt-dlp Python API)
  - Direct URLs (requests)
- ✅ Metadata management (CSV review workflow)
- ✅ Duplicate detection (cross-format, interactive)
- ✅ Test framework with pytest (basic tests)
- ✅ Comprehensive documentation (README updated)
- ✅ Published to GitHub (https://github.com/AmalganOpen/track-manager)

## Next Steps

### High Priority

- [x] **Quality fixed** - Always download best quality (320kbps MP3, 256kbps M4A)
  - Removed config option - quality is always best by default
  - Spotify: 320kbps for MP3, 256kbps for M4A/AAC
  - YouTube: Explicitly requests format 251 (Opus ~160kbps) or 140 (M4A ~128kbps)
    - Fixed: Was defaulting to format 249 (~50kbps)
  - SoundCloud: Best available quality (inherits YouTube settings)
  - No user configuration needed
- [ ] **Test with real URLs** - Validate all source handlers work correctly at best quality
  - Spotify tracks, playlists, and albums (verify 320kbps)
  - YouTube videos and playlists
  - SoundCloud tracks and sets
  - Direct audio URLs (MP3, M4A, etc.)
- [ ] **Improve Spotify credential setup UX** - Make it easier for new users
  - Add first-run detection (check for credentials on startup)
  - Provide clear error messages with setup instructions
  - Add interactive credential setup wizard
  - Document the process clearly in README
  - Consider: Can we work without credentials? (Spotify API requires them)
- [ ] **Integration tests** - Add tests for complete workflows
- [ ] **Publish to PyPI** - Make it `pip install track-manager`
  - See [PUBLISH_CHECKLIST.md](./PUBLISH_CHECKLIST.md) for detailed steps
  - Suggested version: 0.2.0 (quality improvements)
  - Must complete testing and documentation first

### Medium Priority

- [ ] **Enhanced error handling** - Better error messages and recovery
- [ ] **Progress bars** - Better visual feedback for downloads
- [ ] **Batch operations** - Process multiple URLs from file
- [ ] **Config validation** - Validate config.yaml on load

### Low Priority / Future

- [ ] **Additional sources** - Bandcamp, Apple Music, Tidal
- [ ] **Playlist organization** - Group downloads by playlist/album
- [ ] **Quality selection** - Choose specific bitrate/quality
- [ ] **Automated tagging** - Auto-correct common metadata issues

## Publishing to PyPI

When ready to publish:

```bash
# Install build tools
pip install build twine

# Build distribution
python -m build

# Check the build
twine check dist/*

# Upload to PyPI (requires account and API token)
python -m twine upload dist/*
```

Before publishing, ensure:

- [ ] All tests pass
- [ ] Real-world testing complete
- [ ] Documentation is accurate
- [ ] Version number updated in pyproject.toml
- [ ] PyPI account and API token configured

## Testing Checklist

### Functional Tests

- [ ] Spotify single track
- [ ] Spotify playlist (small, <10 tracks)
- [ ] Spotify playlist (large, >50 tracks)
- [ ] Spotify album
- [ ] YouTube single video
- [ ] YouTube playlist
- [ ] SoundCloud track
- [ ] SoundCloud set/playlist
- [ ] Direct MP3 URL
- [ ] Direct M4A URL
- [ ] Direct audio URL (other formats)

### Feature Tests

- [ ] Duplicate detection (same format)
- [ ] Duplicate detection (cross-format: M4A vs MP3)
- [ ] Interactive duplicate handling (skip/keep/replace)
- [ ] Metadata review workflow
- [ ] Metadata extraction and cleaning
- [ ] Failed download logging
- [ ] Config file loading
- [ ] Default behavior (no config)
- [ ] Custom output directory
- [ ] Format selection (auto/m4a/mp3)

### Edge Cases

- [ ] Invalid URL
- [ ] Private/removed content
- [ ] Geo-restricted content
- [ ] Very long playlist (100+ tracks)
- [ ] Tracks with special characters in names
- [ ] Tracks with missing metadata
- [ ] Network interruption handling

## Known Issues

None currently reported.

## Development Notes

### Architecture Decisions

- **Pure Python**: No external CLI dependencies (yt-dlp, spotdl as Python packages)
- **Native APIs**: Each source uses its appropriate library (no forced conversions)
- **Smart defaults**: Works without configuration
- **Interactive mode**: User control for important decisions

### Migration from Bash Version

The original bash implementation has been replaced with this Python package.
Old bash scripts in `scripts/dj/` have been removed from the Gurt workspace.
This Python version provides:

- Better error handling
- Easier installation (single pip command)
- Cross-platform support
- Professional package structure
- Can be published to PyPI for wider use

### Repository

- **Organization**: Amalgan
- **Repository**: https://github.com/AmalganOpen/track-manager
- **License**: MIT
