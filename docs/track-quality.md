# Track Quality Strategy

This document explains track-manager's quality-first approach using DAB Music and ISRC-based matching.

## Core Principle

**Get the highest quality available, automatically** - Use ISRC codes to find lossless FLAC sources from DAB Music, convert to efficient M4A format, fallback to original sources when needed.

## Quality Hierarchy

track-manager prioritizes sources in order of quality:

1. **DAB Music** (Primary) - FLAC lossless → M4A 256kbps
2. **Original Source** (Fallback) - YouTube/SoundCloud at acceptable quality

## DAB Music Integration

### How It Works

1. Extract ISRC from source (Spotify API or song.link)
2. Search DAB Music by ISRC
3. Download FLAC (lossless, 16-bit 44.1kHz)
4. Convert to M4A at 256kbps AAC
5. Apply metadata (title, artist, album, date, ISRC, cover art)
6. Delete FLAC, keep M4A

### Why DAB Music?

**Quality:**

- FLAC: Lossless compression (no quality loss)
- Source: CD-quality (16-bit, 44.1kHz)
- Full frequency range (20kHz)
- No generation loss

### ISRC-Based Matching

**How We Get ISRC:**

**Tier 1 - Direct from Spotify:**

- User provides Spotify URL
- Query Spotify API for track data
- Extract ISRC from track metadata

**Tier 2 - Via song.link:**

- User provides YouTube/SoundCloud/other URL
- Query song.link to find Spotify match
- Get Spotify URL from song.link (requires Spotify match)
- Query Spotify API for ISRC

**Tier 3 - Fallback:**

- No ISRC found or no Spotify match
- Download from original source
- Lower quality but still works

## FLAC → M4A Conversion

### Why Convert?

**FLAC Advantages:**

- Lossless quality (perfect preservation)
- 16-bit 44.1kHz (CD quality)
- Full frequency range

**FLAC Disadvantages:**

- Large file size (~30-40MB per track)
- Poor compatibility with DJ software
- Slower to load and process

**M4A Advantages:**

- 70% smaller files (~8MB vs 30MB)
- Transparent quality at 256kbps AAC
- Universal compatibility
- Fast loading in DJ software
- Native support on all platforms

### Conversion Quality

**Settings:**

- Codec: AAC (Advanced Audio Coding)
- Bitrate: 256kbps constant
- Sample rate: 44.1kHz (preserved)
- Channels: Stereo

**Quality Analysis:**

- Source: FLAC 1411kbps lossless
- Output: M4A 256kbps AAC
- Quality loss: Transparent (imperceptible to human hearing)
- Frequency range: 20kHz preserved
- Dynamic range: Preserved
- Stereo imaging: Preserved

**Why 256kbps AAC is Transparent:**

- AAC is more efficient than MP3 (256kbps AAC ≈ 320kbps MP3)
- At 256kbps, AAC is considered transparent for most listeners
- Professional listening tests show no perceptible difference
- Much more efficient than keeping FLAC for DJ use

### Metadata Preservation

**Applied to M4A:**

- Title, Artist, Album
- Release date
- ISRC (for tracking)
- Cover art (re-embedded after conversion)
- Label, UPC/EAN (when available)

## YouTube Format Conversion

### Why 192kbps for Format 251?

When downloading YouTube format 251 (Opus ~160kbps), we convert to M4A at 192kbps, not 160kbps. Here's why:

**The Transcoding Problem:**

- Source: Opus 160kbps (already lossy)
- Target: M4A/AAC (also lossy)
- Converting lossy → lossy requires headroom to preserve quality

**Why Not Match Source Bitrate?**

Transcoding at the same bitrate (160 → 160) causes quality degradation:

- Opus artifacts get re-encoded by AAC encoder
- Each codec has different strengths/weaknesses
- Some information is lost in the conversion

**Why 192kbps Works:**

The ~20% overhead (160 → 192) provides:

- Headroom for transcoding artifacts
- Preservation of Opus quality characteristics
- Maintains 20kHz frequency range
- Transparent result (no audible loss)

**Result:**

- Format 251 (160kbps Opus) → M4A 192kbps
- Minimal file size increase (~20%)
- No perceptible degradation

## Quality Comparison

### DAB Music vs Original Sources

| Source        | Format | True Bitrate | Quality | File Size | Notes                            |
| ------------- | ------ | ------------ | ------- | --------- | -------------------------------- |
| **DAB Music** | M4A    | 256kbps      | ★★★★★   | ≈6.3 MB   | Lossless source → M4A            |
| Spotify       | M4A    | ~128-160kbps | ★★★☆☆   | ≈4.0 MB   | Via YouTube, Format 251 else 140 |
| YouTube       | M4A    | ~128-160kbps | ★★★☆☆   | ≈4.0 MB   | Format 251 else 140              |
| SoundCloud    | M4A    | ~128kbps     | ★★★☆☆   | ≈3.2 MB   | Free tier only                   |

### Frequency Range Comparison

**DAB Music (from FLAC):**

- Full 20kHz range
- No cutoff or filtering
- Complete audible spectrum
- Professional quality

**YouTube Format 251:**

- 20kHz range
- Decent quality but lossy source
- Mostly noise above 16khz

**YouTube Format 140:**

- 16kHz cutoff
- Missing high frequencies
- Noticeable on critical listening

**Result:** DAB Music preserves the full frequency range from lossless source.

## Fallback Strategy

### When DAB Music Unavailable

If ISRC not found or track not on DAB Music, system falls back to original source:

**YouTube Fallback:**

- Direct yt-dlp download
- Source preference: 1: 251 (Opus), 2: 140 (M4A)
- Source bitrate: ~160kbps (251) or ~128kbps (140)
- Format: M4A at 128-192kbps
- Quality: Standard streaming quality

**Spotify Fallback:**

- Downloads via spotdl (uses YouTube)
- Source bitrate: ~160kbps (251) or ~128kbps (140)
- Format: M4A at 128-192kbps
- Quality: Good but not lossless
- Automatic metadata from Spotify

**SoundCloud Fallback:**

- Direct yt-dlp download
- Format: M4A ~128kbps
- Quality: Free tier streaming

### Graceful Degradation

**With DAB Music credentials:**

- Primary: DAB Music FLAC → M4A 256kbps
- Fallback: Original source (lower quality)

**Without DAB Music credentials:**

- Info message: "DAB Music credentials not configured"
- Direct fallback to original source
- System still works, just lower quality

## File Naming & Organization

**Format:** `Artist - Title.m4a`

**Benefits:**

- Consistent across all sources
- Clean, professional naming
- Easy to sort and search
- DJ software friendly

**Metadata Handling:**

- Sanitizes unsafe characters
- Preserves artist and title
- Includes full metadata tags
- Cover art embedded

## Quality Verification

**Check Downloaded Quality:**

```bash
track-manager check-quality
```

**Expected Results:**

- DAB Music: 256kbps M4A (from FLAC)
- YouTube: ~128-192kbps M4A (format 251 or 140)
- Spotify: ~128-192kbps M4A (format 251 or 140)
- SoundCloud: ~128kbps M4A

## Best Practices

### Maximizing Quality

1. **Configure DAB Music credentials** - Get best possible quality
2. **Use Spotify URLs when possible** - Better ISRC success rate
3. **Monitor failed downloads** - Check `failed-downloads.txt`
4. **Verify metadata** - Run `track-manager verify-metadata`

## Summary

### What You Get

**Primary Source (DAB Music):**

- ✅ Lossless FLAC source
- ✅ Converted to efficient M4A 256kbps
- ✅ Transparent quality (imperceptible loss)
- ✅ 80% smaller than FLAC
- ✅ Full metadata + cover art
- ✅ Universal compatibility

**Fallback Sources:**

- ✅ Still decent quality (128-160kbps)
- ✅ Automatic when DAB unavailable
- ✅ No manual intervention needed

### Why This Approach

1. **Quality First** - Always try for best source (FLAC)
2. **Efficiency** - Convert to practical format (M4A 256kbps)
3. **Compatibility** - Works everywhere (all DJ software, devices)
4. **Reliability** - ISRC-based matching ensures correct track
5. **Automatic** - System handles everything
6. **Graceful** - Falls back when needed
