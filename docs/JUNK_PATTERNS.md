[Use a markdown previewer for a more enjoyable reading experience]: #

# Junk Patterns

This document lists all current and implemented junk patterns for metadata normalization in duplicate detection.

---

## Current Patterns (Already Implemented)

### Official/Video/Audio Patterns

| Pattern           | Example Match           | Result |
| ----------------- | ----------------------- | ------ |
| `\[official.*?\]` | "Song [Official Video]" | "song" |
| `\(official.*?\)` | "Song (Official Audio)" | "song" |
| `\[.*?video.*?\]` | "Song [Music Video]"    | "song" |
| `\(.*?video.*?\)` | "Song (Video)"          | "song" |
| `\[.*?audio.*?\]` | "Song [Audio]"          | "song" |
| `\(.*?audio.*?\)` | "Song (Audio)"          | "song" |
| `\[hd\]`          | "Song [HD]"             | "song" |
| `\(hd\)`          | "Song (HD)"             | "song" |

### Featuring Variations (Normalization)

| Pattern                 | Example Match           | Result              |
| ----------------------- | ----------------------- | ------------------- |
| `\s*\(?\s*ft\.?\s+`     | "Song ft. Artist"       | "song feat. artist" |
| `\s*\(?\s*feat\.?\s+`   | "Song feat Artist"      | "song feat. artist" |
| `\s*\(?\s*featuring\s+` | "Song featuring Artist" | "song feat. artist" |

### Artist Separators (Normalization) - REMOVED

These patterns were removed because they broke artist names like "Excision".

| Pattern           | Example Match            | Result                    |
| ----------------- | ------------------------ | ------------------------- |
| ~~`\s*[x&]\s*`~~  | ~~"Artist1 & Artist2"~~  | ~~"artist1 vs. artist2"~~ |
| ~~`\s+vs\.?\s+`~~ | ~~"Artist1 VS Artist2"~~ | ~~"artist1 vs. artist2"~~ |

---

## New Patterns (Implemented)

### Video/Lyrics Patterns

| Pattern                        | Example Match        | Result |
| ------------------------------ | -------------------- | ------ |
| `[\[\(].*?lyric.*?s?.*?[\]\)]` | "Song [Lyrics]"      | "song" |
| `[\[\(].*?lyric.*?s?.*?[\]\)]` | "Song (Lyric Video)" | "song" |
| `[\[\(]visuali[sz]er.*?[\]\)]` | "Song [Visualizer]"  | "song" |

### Quality/Resolution Patterns

| Pattern                     | Example Match         | Result |
| --------------------------- | --------------------- | ------ |
| `[\[\(]4k[\]\)]`            | "Song [4K]"           | "song" |
| `[\[\(]8k[\]\)]`            | "Song [8K]"           | "song" |
| `[\[\(]uhd[\]\)]`           | "Song [UHD]"          | "song" |
| `[\[\(]hq[\]\)]`            | "Song [HQ]"           | "song" |
| `[\[\(]lq[\]\)]`            | "Song [LQ]"           | "song" |
| `[\[\(].*?quality.*?[\]\)]` | "Song (High Quality)" | "song" |

### Platform/Source Patterns

| Pattern               | Example Match    | Result   |
| --------------------- | ---------------- | -------- |
| `\s*-\s*topic\s*$`    | "Artist - Topic" | "artist" |
| `[\[\(]premium[\]\)]` | "Song [Premium]" | "song"   |

### Misc Patterns

| Pattern                       | Example Match          | Result |
| ----------------------------- | ---------------------- | ------ |
| `[\[\(]free\s*download[\]\)]` | "Song [Free Download]" | "song" |
| `[\[\(]download.*?[\]\)]`     | "Song (Download Link)" | "song" |
| `[\[\(]out\s*now[\]\)]`       | "Song [Out Now]"       | "song" |
| `[\[\(]new[\]\)]`             | "Song [NEW]"           | "song" |

---

## Patterns NOT Implemented

These patterns were considered but NOT implemented because they represent meaningful distinctions for DJ libraries.

### Content Type/Rating Patterns

| Pattern                    | Example Match          | Result              |
| -------------------------- | ---------------------- | ------------------- |
| `[\[\(]explicit[\]\)]`     | "Song (Explicit)"      | "song"              |
| `[\[\(]clean[\]\)]`        | "Song (Clean)"         | "song"              |
| `[\[\(]radio\s*edit[\]\)]` | "Song (Radio Edit)"    | "song (radio edit)" |
| `[\[\(].*?edit[\]\)]`      | "Song [Extended Edit]" | "song"              |
| `[\[\(].*?version[\]\)]`   | "Song (Album Version)" | "song"              |

### Remaster/Release Patterns

| Pattern                         | Example Match             | Result |
| ------------------------------- | ------------------------- | ------ |
| `[\[\(].*?remaster.*?[\]\)]`    | "Song (Remastered)"       | "song" |
| `[\[\(].*?anniversary.*?[\]\)]` | "Song (20th Anniversary)" | "song" |
| `[\[\(].*?deluxe.*?[\]\)]`      | "Song [Deluxe Edition]"   | "song" |

### Year Patterns

| Pattern                           | Example Match          | Result |
| --------------------------------- | ---------------------- | ------ |
| `[\[\(]\d{4}[\]\)]`               | "Song (2024)"          | "song" |
| `[\[\(]\d{4}\s*remaster.*?[\]\)]` | "Song (2024 Remaster)" | "song" |

### Platform/Source Patterns

| Pattern                       | Example Match             | Result |
| ----------------------------- | ------------------------- | ------ |
| `[\[\(]spotify.*?[\]\)]`      | "Song [Spotify Sessions]" | "song" |
| `[\[\(].*?session.*?s?[\]\)]` | "Song (Live Session)"     | "song" |

### Performance Type Patterns

| Pattern                       | Example Match         | Result                |
| ----------------------------- | --------------------- | --------------------- |
| `[\[\(]live[\]\)]`            | "Song (Live)"         | "song (live)"         |
| `[\[\(].*?acoustic.*?[\]\)]`  | "Song (Acoustic)"     | "song (acoustic)"     |
| `[\[\(].*?instrumental[\]\)]` | "Song [Instrumental]" | "song (instrumental)" |
| `[\[\(].*?remix.*?[\]\)]`     | "Song (Remix)"        | "song (remix)"        |
| `[\[\(].*?bootleg.*?[\]\)]`   | "Song (Bootleg)"      | "song (bootleg)"      |
| `[\[\(].*?mashup.*?[\]\)]`    | "Song (Mashup)"       | "song (mashup)"       |

---

## Implementation Notes

### Pattern Grouping

Patterns are organized by category in code:

```python
VIDEO_PATTERNS = [...]
QUALITY_PATTERNS = [...]
VERSION_PATTERNS = [...]  # Be careful with these for DJ use!
```

### Test Cases

Each implemented pattern has corresponding test cases in `tests/test_duplicates.py`.

### DJ Library Considerations

**IMPORTANT**: Many patterns that are "junk" for general music libraries might be **meaningful distinctions** for DJ libraries:

- ⚠️ **Radio Edits** - Different length/structure than original
- ⚠️ **Extended Edits** - Longer versions for mixing
- ⚠️ **Live Versions** - Different feel/energy
- ⚠️ **Acoustic Versions** - Completely different arrangement
- ⚠️ **Instrumentals** - No vocals (useful for mixing)
- ⚠️ **Clean/Explicit** - Different content (venue considerations)
- ⚠️ **Bootlegs/Mashups** - Unique versions
- ⚠️ **Sessions (Spotify/BBC/etc)** - Different recordings

**Recommendation**: Be conservative with removal - when in doubt, keep the distinction!

---

## Filename Sanitization

### Why We Replace "Unsafe" Characters

When creating filenames from metadata, we replace certain characters with `-`. This section explains why.

### Filesystem-Forbidden Characters

Some characters **cannot** be in filenames due to filesystem restrictions:

#### All Operating Systems
| Character | Issue | Systems |
|-----------|-------|---------|
| `/` | Path separator | Unix/Linux/macOS |
| `\` | Path separator | Windows |

**Example:**
```python
filename = "AC/DC - Thunderstruck.m4a"
# OS interprets: /music/AC/DC - Thunderstruck.m4a
# As: /music/AC/DC (directory) / - Thunderstruck.m4a
# Result: File not found error
```

#### Windows-Specific
| Character | Issue | Why |
|-----------|-------|-----|
| `:` | Drive/volume separator | `C:`, `D:` |
| `<` | Redirection operator | Input redirection |
| `>` | Redirection operator | Output redirection |
| `"` | String delimiter | Command parsing |
| `|` | Pipe operator | Command chaining |
| `?` | Wildcard | Single char match |
| `*` | Wildcard | Multiple char match |

**Impact:** Files with these characters **cannot be created** on Windows or FAT32/exFAT drives.

**Example:**
```bash
# macOS - works:
touch "Song: The Title.m4a"  ✓

# Windows - fails:
touch "Song: The Title.m4a"  ✗ Error: Invalid filename

# USB drive (FAT32) - fails:
cp "Song: The Title.m4a" /Volumes/USB/  ✗ Error
```

### Shell Metacharacters

On Unix/macOS, these characters are **allowed in filenames** but cause problems in shell commands:

| Character | Shell Meaning | Problem |
|-----------|---------------|---------|
| `*` | Wildcard (any chars) | Expands to matching files |
| `?` | Wildcard (single char) | Expands to matching files |
| `<` | Input redirection | Redirects stdin |
| `>` | Output redirection | Redirects stdout |
| `|` | Pipe | Chains commands |
| `"` | String delimiter | Quote parsing |

**Example:**
```bash
# File named: "song*.mp3"
touch "song*.mp3"  # Creates file (works with quotes)

# Later, without quotes:
ls song*.mp3       # Shell expands * to all matching files
rm song*.mp3       # Deletes ALL files matching song*.mp3 pattern!

# Must always remember quotes:
ls "song*.mp3"     # Works, but error-prone
```

### The Trade-Off

#### Current Approach: Replace with `-`

**What we do:**
```python
unsafe_chars = ["/", "\\", ":", "*", "?", '"', "<", ">", "|"]
for char in unsafe_chars:
    text = text.replace(char, "-")
```

**Examples:**
"AC/DC - Song" → "AC-DC - Song.m4a"
"Song: The Title" → "Song- The Title.m4a"
"File?.mp3" → "File-.mp3"
"Best > Worst" → "Best - Worst.m4a"
