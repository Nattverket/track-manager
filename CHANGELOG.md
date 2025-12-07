# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Quality is now always best by default - no configuration needed
- Spotify downloads at 320 kbps (was ~128 kbps with "auto" setting)
- YouTube explicitly requests high-quality formats (160 kbps Opus or 128 kbps M4A)
- Removed `best_quality` config option - quality is always best

### Fixed

- Spotify downloader was using "auto" bitrate which defaulted to ~128 kbps
- YouTube downloader was selecting low-quality format 249 (~50 kbps) instead of format 251 (~160 kbps)

### Added

- Comprehensive quality documentation in README
- PyPI publishing checklist
- Quality standards for each source

## [0.1.0] - 2025-11-26

### Added

- Initial release
- Universal download system supporting Spotify, YouTube, SoundCloud, and direct URLs
- Smart duplicate detection across formats
- Metadata management with CSV review workflow
- Interactive prompts for duplicate handling
- Playlist support with progress tracking
- Error resilience with failed download logging
- Professional CLI with click
- Comprehensive test suite

### Technical

- Pure Python implementation using spotdl and yt-dlp as libraries
- Configuration system with YAML
- Cross-platform support (macOS, Linux, Windows)

[Unreleased]: https://github.com/AmalganOpen/track-manager/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/AmalganOpen/track-manager/releases/tag/v0.1.0
