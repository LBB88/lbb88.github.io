#!/usr/bin/env python3
"""
Media import module for Jekyll pages and posts.
Discovers import folders, moves media to assets, sanitizes filenames,
deduplicates, generates slugs, and writes log entries.

Usage:
  python import-media.py              # Process all import folders
  python import-media.py --dry-run    # Show what would be moved without changes
  python import-media.py --help       # Show usage
"""

import argparse
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

# Media extensions
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
VIDEO_EXTENSIONS = {'.mp4', '.webm', '.mov'}
MEDIA_EXTENSIONS = IMAGE_EXTENSIONS | VIDEO_EXTENSIONS

# Path resolution following validate-new-pages.py patterns
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
SRC_DIR = REPO_ROOT / "src"
IMPORT_BASE = REPO_ROOT / "import"
PAGES_IMPORT = IMPORT_BASE / "pages"
POSTS_IMPORT = IMPORT_BASE / "_posts"
ASSETS_DIR = SRC_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
VIDEOS_DIR = ASSETS_DIR / "videos"
PROCESSED_LOG = Path(__file__).resolve().parent / "processed.log"


def discover_import_folders(import_base: Path) -> List[Path]:
    """Discover YYYYMMDD_* folders in import directory."""
    if not import_base.exists():
        return []
    pattern = re.compile(r'^\d{8}_.+')
    folders = [
        p for p in import_base.iterdir()
        if p.is_dir() and pattern.match(p.name)
    ]
    return sorted(folders)


def identify_media_files(folder: Path) -> Tuple[List[Path], List[Path]]:
    """Return (image_files, video_files) from folder."""
    image_files = []
    video_files = []
    if not folder.exists():
        return image_files, video_files

    for item in sorted(folder.iterdir()):
        if not item.is_file():
            continue
        ext = item.suffix.lower()
        if ext in IMAGE_EXTENSIONS:
            image_files.append(item)
        elif ext in VIDEO_EXTENSIONS:
            video_files.append(item)
    return image_files, video_files


def find_markdown_file(folder: Path) -> Optional[Path]:
    """Find markdown file in folder: prefers content.md, then any .md file (skips README.md)."""
    content_md = folder / "content.md"
    if content_md.exists():
        return content_md

    for item in sorted(folder.iterdir()):
        if item.is_file() and item.suffix.lower() == '.md' and item.name.lower() != 'readme.md':
            return item
    return None


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for web use."""
    name_part = Path(filename).stem
    ext_part = Path(filename).suffix.lower()

    sanitized = name_part.replace(' ', '-')
    sanitized = re.sub(r'[^a-zA-Z0-9\-\.]', '', sanitized)
    sanitized = re.sub(r'-+', '-', sanitized)
    sanitized = sanitized.strip('-')

    if not sanitized:
        sanitized = 'media'

    return sanitized + ext_part


def get_unique_path(target_dir: Path, filename: str) -> Path:
    """Get deduplicated path (append -1, -2 if exists)."""
    target_path = target_dir / filename
    if not target_path.exists():
        return target_path

    stem = Path(filename).stem
    suffix = Path(filename).suffix
    counter = 1
    while True:
        new_filename = f"{stem}-{counter}{suffix}"
        candidate = target_dir / new_filename
        if not candidate.exists():
            return candidate
        counter += 1


def generate_slug(media_files: List[Path]) -> str:
    """Generate slug from first media filename alphabetically."""
    if not media_files:
        return ''
    first = sorted(media_files, key=lambda p: p.name.lower())[0]
    slug = sanitize_filename(first.name)
    return Path(slug).stem.lower()


def generate_slug_from_markdown(markdown_file: Path) -> str:
    """Generate slug from markdown filename."""
    slug = sanitize_filename(markdown_file.name)
    return Path(slug).stem.lower()


def get_markdown_destination(folder: Path, entry_type: str, slug: str) -> Path:
    """Determine destination path for content.md based on type and slug."""
    if entry_type == "PAGE":
        return SRC_DIR / f"topic-{slug}.md"
    else:
        raw_date = folder.name[:8]
        date = f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:8]}"
        return SRC_DIR / "_posts" / f"{date}-{slug}.md"


def move_media_files(media_files: List[Path], target_dir: Path) -> List[Path]:
    """Move files to target, return new paths."""
    target_dir.mkdir(parents=True, exist_ok=True)
    new_paths = []
    moved = []

    try:
        for media_file in media_files:
            sanitized = sanitize_filename(media_file.name)
            target_path = get_unique_path(target_dir, sanitized)
            shutil.move(str(media_file), str(target_path))
            new_paths.append(target_path)
            moved.append((target_path, media_file))
    except Exception as e:
        for new_path, original_path in moved:
            if new_path.exists():
                try:
                    shutil.move(str(new_path), str(original_path))
                except Exception:
                    pass
        raise RuntimeError(f"Failed to move media files: {e}")

    return new_paths


def write_log_entry(log_path: Path, entry_type: str, folder_name: str,
                    dest_path: Path, media_names: List[str],
                    markdown_dest: Path = None):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    media_list = ', '.join(media_names) if media_names else 'none'
    log_line = (f"[{timestamp}] {entry_type}: {folder_name} → {dest_path} "
                f"| media: {media_list}")
    if markdown_dest:
        log_line += f" | markdown: {markdown_dest}"
    log_line += "\n"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(log_line)


def process_folder(folder: Path, entry_type: str, dry_run: bool = False) -> Tuple[Optional[Path], List[Path]] | None:
    """Process a single import folder."""
    image_files, video_files = identify_media_files(folder)
    all_media = image_files + video_files
    markdown_file = find_markdown_file(folder)

    if not all_media and not markdown_file:
        print(f"  No media or markdown files found in {folder.name}")
        return None

    if all_media:
        slug = generate_slug(all_media)
    elif markdown_file:
        slug = generate_slug_from_markdown(markdown_file)
    else:
        return None

    markdown_dest = None
    if markdown_file and markdown_file.exists():
        markdown_dest = get_markdown_destination(folder, entry_type, slug)

    if dry_run:
        print(f"  Would process: {folder.name}")
        print(f"    Type: {entry_type}")
        print(f"    Slug: {slug}")
        for media in all_media:
            sanitized = sanitize_filename(media.name)
            print(f"    - {media.name} → {sanitized}")
        if markdown_dest:
            print(f"    {markdown_file.name} → {markdown_dest}")
        return markdown_dest, []

    try:
        moved_images = []
        moved_videos = []

        if image_files:
            moved_images = move_media_files(image_files, IMAGES_DIR)
        if video_files:
            moved_videos = move_media_files(video_files, VIDEOS_DIR)

        all_moved = moved_images + moved_videos
        media_names = [p.name for p in all_moved]

        if moved_images:
            dest_path = moved_images[0].parent.relative_to(SRC_DIR)
        elif moved_videos:
            dest_path = moved_videos[0].parent.relative_to(SRC_DIR)
        else:
            dest_path = Path("assets")

        if markdown_dest and markdown_file.exists():
            markdown_dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(markdown_file), str(markdown_dest))

        write_log_entry(PROCESSED_LOG, entry_type, folder.name,
                        dest_path, media_names, markdown_dest)
        print(f"  Processed: {folder.name} → {dest_path} "
              f"({len(media_names)} files, slug: {slug})")

        try:
            shutil.rmtree(str(folder))
            print(f"  Removed source folder: {folder.name}")
        except Exception as e:
            print(f"  Warning: Could not remove source folder {folder.name}: {e}", file=sys.stderr)

        return markdown_dest, all_moved

    except Exception as e:
        print(f"  Error processing {folder.name}: {e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Import media files from import folders to Jekyll assets"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be moved without making changes"
    )
    args = parser.parse_args()

    if not IMPORT_BASE.exists():
        print(f"Error: Import directory not found at {IMPORT_BASE}")
        sys.exit(1)

    processed = 0
    errors = 0

    for import_dir, label, entry_type in [
        (PAGES_IMPORT, "pages", "PAGE"),
        (POSTS_IMPORT, "posts", "POST")
    ]:
        if not import_dir.exists():
            continue

        folders = discover_import_folders(import_dir)
        if not folders:
            continue

        print(f"\nProcessing {label} imports ({len(folders)} folder(s)):")
        for folder in folders:
            result = process_folder(folder, entry_type=entry_type,
                                    dry_run=args.dry_run)
            markdown_dest = result[0] if result else None
            if markdown_dest:
                processed += 1
            else:
                errors += 1

    print(f"\n{'='*60}")
    if args.dry_run:
        print("Dry run complete - no changes made.")
    else:
        print(f"Processed {processed} folder(s).")
    if errors:
        print(f"{errors} folder(s) had errors or no media.")
    print(f"Log: {PROCESSED_LOG}")


if __name__ == "__main__":
    main()
