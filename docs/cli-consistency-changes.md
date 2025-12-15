# CLI Output Consistency Changes

## Summary

This document summarizes the changes made to standardize CLI output across track-manager.

## Changes Made

### 1. Check Mark Standardization (✓ → ✅)

Replaced all instances of `✓` (U+2713) with `✅` (U+2705) for consistency:

**Files updated:**
- `track_manager/cli.py` (2 instances)
- `track_manager/downloader.py` (5 instances)
- `track_manager/sources/direct.py` (2 instances)
- `track_manager/sources/soundcloud.py` (1 instance)
- `track_manager/sources/spotify.py` (2 instances)
- `track_manager/sources/youtube.py` (2 instances)
- `track_manager/duplicates.py` (2 instances)
- `track_manager/metadata.py` (4 instances)
- `track_manager/dabmusic.py` (1 instance)

**Total:** 21 instances updated

### 2. Error Message Stderr Routing

Ensured all ❌ error messages write to stderr:

**Files updated:**
- `track_manager/cli.py` (6 instances)
- `track_manager/downloader.py` (1 instance)
- `track_manager/sources/direct.py` (3 instances)
- `track_manager/sources/soundcloud.py` (2 instances)
- `track_manager/sources/spotify.py` (1 instance)

**Total:** 13 instances updated

### 3. Progress Indicators

Updated progress indicators to use ⬇️ emoji:

**Files updated:**
- `track_manager/downloader.py` (2 instances)
- `track_manager/sources/direct.py` (1 instance)
- `track_manager/sources/soundcloud.py` (1 instance)
- `track_manager/sources/spotify.py` (1 instance)
- `track_manager/sources/youtube.py` (1 instance)

**Total:** 6 instances updated

### 4. Line Break Consistency

Fixed line break patterns to follow the style guide:

**Pattern:**
```python
print("Message")
print()  # Blank line for section separation
```

**Files updated:**
- Multiple files for consistent spacing around sections

### 5. Section Headers

Standardized section separator length to 60 characters:

**Files updated:**
- `track_manager/sources/spotify.py`
- `track_manager/sources/youtube.py`

## Verification

All changes verified with:

```bash
# No more ✓ check marks
git grep "✓" track_manager/  # Returns nothing

# All errors use stderr
git grep "print.*❌" track_manager/ | grep -v "file=sys.stderr"  # Returns nothing

# Emoji spacing consistent
git grep -E "✅  |❌  " track_manager/  # Returns nothing (no double spaces)
```

## Style Guide

See `docs/cli-style-guide.md` for the complete style guide that these changes follow.

## Testing

Before committing:

1. Run the full test suite
2. Manually test key commands:
   - `track-manager check-setup`
   - `track-manager init`
   - `track-manager download <url>`
   - `track-manager check-duplicates`
   - `track-manager check-quality`

## Next Steps

1. Update any documentation to reference the new style guide
2. Add linting rules to catch future inconsistencies
3. Consider adding tests for output formatting
