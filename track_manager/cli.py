"""Command-line interface for track-manager."""

import sys
from pathlib import Path
from typing import Optional

try:
    import click
except ImportError:
    print("Error: click not installed", file=sys.stderr)
    print("Install with: pip install click", file=sys.stderr)
    sys.exit(1)

from .config import Config
from .downloader import Downloader


@click.group()
@click.version_option()
def cli():
    """Track Manager - Universal music downloader with smart duplicate detection."""
    pass


@cli.command()
@click.argument('url')
@click.option('--format', '-f', 
              type=click.Choice(['auto', 'm4a', 'mp3']),
              default='auto',
              help='Output format (default: auto)')
@click.option('--output', '-o',
              type=click.Path(),
              help='Output directory (overrides config)')
def download(url: str, format: str, output: Optional[str]):
    """Download track(s) from URL.
    
    Supports: Spotify, YouTube, SoundCloud, and direct URLs.
    """
    config = Config()
    
    # Override output directory if specified
    if output:
        output_dir = Path(output)
    else:
        output_dir = config.output_dir
    
    downloader = Downloader(config, output_dir)
    
    try:
        downloader.download(url, format)
    except KeyboardInterrupt:
        click.echo("\n⚠️  Download cancelled by user")
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command('check-duplicates')
@click.option('--file', '-f',
              type=click.Path(exists=True),
              help='Check specific file for duplicates')
def check_duplicates(file: Optional[str]):
    """Check for duplicate tracks in library."""
    from .duplicates import scan_library, check_file
    
    config = Config()
    
    if file:
        check_file(Path(file), config.output_dir)
    else:
        scan_library(config.output_dir)


@cli.command('verify-metadata')
def verify_metadata():
    """Verify metadata quality in library."""
    from .metadata import verify_library
    
    config = Config()
    verify_library(config.output_dir)


@cli.command('apply-metadata')
@click.option('--show', is_flag=True,
              help='Show pending reviews without applying')
def apply_metadata(show: bool):
    """Apply metadata corrections from CSV."""
    from .metadata import show_pending_reviews, apply_metadata_csv
    
    config = Config()
    
    if show:
        show_pending_reviews(config.metadata_csv)
    else:
        apply_metadata_csv(config.metadata_csv)


@cli.command('check-setup')
def check_setup():
    """Verify all dependencies are installed."""
    click.echo("🔍 Checking track-manager dependencies...\n")
    
    all_ok = True
    
    # Check yt-dlp
    try:
        import yt_dlp
        click.echo(f"✅ yt-dlp: {yt_dlp.version.__version__}")
    except ImportError:
        click.echo("❌ yt-dlp: Not installed")
        click.echo("   Install: pip install yt-dlp")
        all_ok = False
    
    # Check spotdl
    try:
        import spotdl
        click.echo("✅ spotdl: Installed")
    except ImportError:
        click.echo("⚠️  spotdl: Not installed (optional, needed for Spotify)")
        click.echo("   Install: pip install spotdl")
    
    # Check requests
    try:
        import requests
        click.echo(f"✅ requests: {requests.__version__}")
    except ImportError:
        click.echo("❌ requests: Not installed")
        click.echo("   Install: pip install requests")
        all_ok = False
    
    # Check mutagen
    try:
        import mutagen
        click.echo(f"✅ mutagen: {mutagen.version_string}")
    except ImportError:
        click.echo("❌ mutagen: Not installed")
        click.echo("   Install: pip install mutagen")
        all_ok = False
    
    # Check PyYAML
    try:
        import yaml
        click.echo("✅ PyYAML: Installed")
    except ImportError:
        click.echo("❌ PyYAML: Not installed")
        click.echo("   Install: pip install pyyaml")
        all_ok = False
    
    # Check click
    try:
        import click as _
        click.echo(f"✅ click: {click.__version__}")
    except ImportError:
        click.echo("❌ click: Not installed")
        click.echo("   Install: pip install click")
        all_ok = False
    
    # Check config
    try:
        config = Config()
        click.echo("✅ Configuration: config.yaml found")
    except SystemExit:
        click.echo("⚠️  Configuration: config.yaml not found")
        click.echo("   Copy config.example.yaml to config.yaml")
    
    click.echo()
    
    if all_ok:
        click.echo("🎉 All required dependencies are installed!")
        click.echo("\nNext steps:")
        click.echo("  1. Ensure config.yaml is set up")
        click.echo("  2. Run: track-manager download <url>")
    else:
        click.echo("⚠️  Some dependencies are missing. Please install them first.")
        sys.exit(1)


def main():
    """Main entry point."""
    cli()


if __name__ == '__main__':
    main()
