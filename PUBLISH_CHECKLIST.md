# Track Manager - PyPI Publishing Checklist

This checklist ensures track-manager is ready for publishing to PyPI.

## Pre-Publish Requirements

### 1. Quality & Testing ✅

- [x] Spotify quality fix verified (320 kbps)
- [x] YouTube quality fix verified (~160 kbps)
- [x] SoundCloud quality verified
- [x] All unit tests passing (90 passed, 1 skipped)
- [x] All integration tests passing
- [ ] Real-world testing complete:
  - [x] Spotify single track
  - [ ] Spotify playlist (small, <10 tracks)
  - [x] YouTube single video
  - [ ] YouTube playlist
  - [x] SoundCloud track
  - [ ] Direct URL download

### 2. Documentation ✅

- [x] README.md up to date
  - [x] Installation instructions
  - [x] Quality information documented
  - [x] Usage examples
  - [x] Troubleshooting section
- [x] CHANGELOG.md created/updated
- [x] Version number decided: **0.2.0** (quality fixes)
- [ ] All docstrings complete (check before publish)
- [x] Configuration example updated

### 3. Code Quality ✅

- [x] No TODO/FIXME comments in critical code
- [x] Type hints present on public APIs
- [x] Error handling comprehensive
- [x] Logging appropriate (CLI uses print statements for user output)
- [x] No debug prints
- [x] Code formatting (black, isort) verified
- [x] Security scan (bandit) passed

### 4. Package Metadata

- [ ] pyproject.toml complete:
  - [ ] Version number updated
  - [ ] Description accurate
  - [ ] Keywords relevant
  - [ ] Dependencies correct
  - [ ] Python version requirements
  - [ ] License specified
  - [ ] Author info
  - [ ] URLs (homepage, issues, source)
- [ ] README renders correctly as description
- [ ] LICENSE file included

### 5. Dependencies

- [x] All dependencies in pyproject.toml
- [x] Version constraints reasonable
- [x] Optional dependencies marked correctly
- [x] No unnecessary dependencies

## Build Preparation

### 6. Version Management

- [ ] Update version in pyproject.toml
- [ ] Follow semantic versioning (MAJOR.MINOR.PATCH)
  - Suggest: `0.2.0` (MINOR bump for quality improvements)
- [ ] Update CHANGELOG.md with version changes
- [ ] Commit version changes

### 7. Clean Build Environment

```bash
# Remove old builds
rm -rf dist/ build/ *.egg-info/

# Ensure working directory is clean
git status

# Create fresh virtual environment for testing
python -m venv test_env
source test_env/bin/activate
pip install build twine
```

## Building

### 8. Build Distribution

```bash
# Install build tools
pip install build twine

# Build both source and wheel distributions
python -m build

# Verify build
ls -lh dist/
```

Expected files:

- `track_manager-X.Y.Z.tar.gz` (source distribution)
- `track_manager-X.Y.Z-py3-none-any.whl` (wheel)

### 9. Check Build

```bash
# Check package with twine
twine check dist/*

# Should show: "Checking dist/... PASSED"
```

## Testing on TestPyPI

### 10. Upload to TestPyPI

```bash
# Upload to TestPyPI (requires account)
# Sign up at: https://test.pypi.org/account/register/
python -m twine upload --repository testpypi dist/*

# You'll need TestPyPI API token
# Create at: https://test.pypi.org/manage/account/#api-tokens
```

### 11. Test Installation from TestPyPI

```bash
# Create fresh environment
python -m venv test_install
source test_install/bin/activate

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple/ \
    track-manager

# Test basic functionality
track-manager --help
track-manager check-setup
```

### 12. Verify Installation

Test that installed package works:

```bash
# Check version
track-manager --version

# Check dependencies
track-manager check-setup

# Test download (use a short video/track)
track-manager download "https://youtube.com/watch?v=test"
```

## Publishing to PyPI

### 13. Upload to PyPI

⚠️ **Important:** This is permanent! Once uploaded, you cannot modify or delete.

```bash
# Upload to real PyPI (requires account)
# Sign up at: https://pypi.org/account/register/
python -m twine upload dist/*

# You'll need PyPI API token
# Create at: https://pypi.org/manage/account/#api-tokens
```

### 14. Create Git Tag

```bash
# Tag the release
git tag -a v0.2.0 -m "Release v0.2.0: Quality improvements"

# Push tag
git push origin v0.2.0
```

### 15. Create GitHub Release

- Go to https://github.com/AmalganOpen/track-manager/releases
- Click "Create a new release"
- Select the tag (v0.2.0)
- Title: "v0.2.0 - Quality Improvements"
- Description: Copy from CHANGELOG.md
- Attach built distributions (optional)
- Publish release

## Post-Publish Verification

### 16. Verify on PyPI

- [ ] Check package page: https://pypi.org/project/track-manager/
- [ ] Verify README renders correctly
- [ ] Check all metadata is correct
- [ ] Verify links work

### 17. Test Installation from PyPI

```bash
# Fresh environment
python -m venv verify_install
source verify_install/bin/activate

# Install from PyPI
pip install track-manager

# Verify it works
track-manager --version
track-manager check-setup
```

### 18. Update Documentation

- [ ] Update main README to reference PyPI
- [ ] Update installation instructions
- [ ] Update version badges if any
- [ ] Document breaking changes if any

### 19. Announce Release

- [ ] Update project README
- [ ] Post in relevant communities (if applicable)
- [ ] Update any integration docs

## Quick Reference

### Version Numbering

For this release, suggest: **0.2.0**

- 0.2.0 (MINOR): Quality improvements, new default behavior
- Not 1.0.0 yet: Still need credential UX improvements, more testing
- Not 0.1.1 (PATCH): Changes behavior (quality settings)

### Required Accounts

1. **TestPyPI**: https://test.pypi.org/account/register/
2. **PyPI**: https://pypi.org/account/register/
3. **API Tokens**:
   - TestPyPI: https://test.pypi.org/manage/account/#api-tokens
   - PyPI: https://pypi.org/manage/account/#api-tokens

### Useful Commands

```bash
# Build
python -m build

# Check
twine check dist/*

# Upload to test
twine upload --repository testpypi dist/*

# Upload to real PyPI
twine upload dist/*

# Install from test
pip install --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple/ \
    track-manager

# Install from PyPI
pip install track-manager
```

## Notes

- Cannot delete or modify uploads on PyPI (only "yank" them)
- Test thoroughly on TestPyPI first
- Version numbers are permanent
- Package name must be unique on PyPI
- Consider using `python -m build` instead of `setup.py`
- Always use API tokens, not passwords

## Rollback Plan

If something goes wrong after publishing:

1. **Critical bug**: Publish patch version (0.2.1) immediately
2. **Bad package**: Yank the version on PyPI (doesn't delete, just warns users)
3. **Documentation issue**: Fix and publish patch version

Cannot: Delete or modify published versions
