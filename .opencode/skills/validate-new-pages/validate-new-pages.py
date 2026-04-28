#!/usr/bin/env python3
"""
Wrapper script to discover and validate Jekyll pages and posts.
Activates the validate-templates skill for all markdown files in src/.

Usage:
  python validate-new-pages.py              # Validate all pages and posts
  python validate-new-pages.py --pages      # Validate pages only
  python validate-new-pages.py --posts      # Validate posts only
  python validate-new-pages.py --apply      # Auto-fix layout mismatches
  python validate-new-pages.py --import     # Import media before validation
"""

import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

VALIDATOR = Path(__file__).resolve().parent.parent / "validate-templates" / "validate-templates.py"
SRC_DIR = Path(__file__).resolve().parent.parent.parent.parent / "src"


def load_fix_frontmatter():
    fix_path = Path(__file__).resolve().parent / "fix-frontmatter.py"
    spec = importlib.util.spec_from_file_location("fix_frontmatter", fix_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


FIX_FRONTMATTER = load_fix_frontmatter()


def find_files(pages_only=False, posts_only=False):
    if not SRC_DIR.exists():
        print(f"Error: {SRC_DIR} directory not found. Run from repository root.")
        sys.exit(1)

    files = []
    for md_file in SRC_DIR.rglob("*.md"):
        parts = md_file.parts
        if "_site" in parts or ".opencode" in parts:
            continue
        if "_templates" in parts:
            continue
        if md_file.name in ("about.md", "index.md", "README.md"):
            continue

        is_post = "_posts" in parts

        if posts_only and not is_post:
            continue
        if pages_only and is_post:
            continue

        files.append(md_file)

    return sorted(files)


def run_validator(path, apply_fixes=False):
    cmd = [sys.executable, str(VALIDATOR), str(path)]
    if apply_fixes:
        cmd.append("--apply")
    return subprocess.run(cmd, capture_output=False, text=True)


def is_interactive():
    return sys.stdin.isatty()


def prompt_for_field(field, suggestion):
    if isinstance(suggestion, list):
        print(f"\n  Field: {field}")
        print("  Suggestions:")
        for i, opt in enumerate(suggestion, 1):
            print(f"    {i}. {opt}")
        print("    c. Enter custom value")
        print("    s. Skip this field")
        while True:
            response = input("  Select [1-{}], c, or s: ".format(len(suggestion))).strip().lower()
            if response == "s":
                return None
            if response == "c":
                return input("  Enter custom value: ").strip()
            try:
                idx = int(response) - 1
                if 0 <= idx < len(suggestion):
                    return suggestion[idx]
            except ValueError:
                pass
            print("  Invalid choice, try again.")
    else:
        print(f"\n  Field: {field}")
        print(f"  Suggested: {suggestion}")
        response = input("  Accept [Enter], Edit [e], Skip [s]: ").strip().lower()
        if response == "s":
            return None
        elif response == "e":
            return input(f"  Enter value for {field}: ").strip()
        else:
            return suggestion


def interactive_fix(filepath, file_type, missing, data, content):
    proposal = FIX_FRONTMATTER.generate_fix_proposal(filepath, file_type, missing, data, content)

    print(f"\n{'='*60}")
    print(f"FRONTMATTER FIX NEEDED: {filepath.name}")
    print(f"Type: {file_type}")
    print(f"Missing fields: {', '.join(missing)}")
    print("="*60)

    fixes = {}
    for field in missing:
        suggestion = proposal["suggestions"].get(field)
        if suggestion is None:
            continue
        value = prompt_for_field(field, suggestion)
        if value is not None:
            fixes[field] = value

    if not fixes:
        print("\n  No fixes selected. Skipping.")
        return False

    print(f"\n  Summary of fixes for {filepath.name}:")
    for k, v in fixes.items():
        print(f"    {k}: {v}")

    confirm = input("\n  Apply these fixes? [y/N]: ").strip().lower()
    if confirm != "y":
        print("  Skipped.")
        return False

    success, msg = FIX_FRONTMATTER.apply_fix(filepath, file_type, fixes)
    if success:
        print(f"  ✓ Fixed frontmatter in {filepath}")
        return True
    else:
        print(f"  ✗ Failed: {msg}")
        return False


def report_frontmatter_issues(filepath, file_type, missing, data, content):
    proposal = FIX_FRONTMATTER.generate_fix_proposal(filepath, file_type, missing, data, content)
    print(f"\n  ⚠ Frontmatter issues in {filepath.name}: missing {', '.join(missing)}")
    print("    Suggested fixes:")
    for field in missing:
        sugg = proposal["suggestions"].get(field)
        if isinstance(sugg, list):
            print(f"      {field}: {', '.join(sugg)}")
        else:
            print(f"      {field}: {sugg}")


def backup_import_folders():
    repo_root = Path(__file__).resolve().parent.parent.parent.parent
    import_base = repo_root / "import"
    backup_base = repo_root / "bkup-import"

    backed_up = 0

    for import_dir, backup_dir in [
        (import_base / "pages", backup_base / "pages"),
        (import_base / "_posts", backup_base / "_posts")
    ]:
        if not import_dir.exists():
            continue

        pattern = __import__("re").compile(r'^\d{8}_.+')
        folders = [
            p for p in import_dir.iterdir()
            if p.is_dir() and pattern.match(p.name)
        ]

        for folder in sorted(folders):
            dest = backup_dir / folder.name
            if dest.exists():
                continue
            try:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(str(folder), str(dest), ignore=shutil.ignore_patterns("README.md"))
                print(f"  Backed up: {folder.name} → bkup-import/{backup_dir.name}/")
                backed_up += 1
            except Exception as e:
                print(f"  Warning: Failed to backup {folder.name}: {e}", file=sys.stderr)

    if backed_up > 0:
        print(f"\nBacked up {backed_up} folder(s).")
    return backed_up > 0


def import_media_and_embed():
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import import_media
        import media_placement
    except ImportError as e:
        print(f"Error: Could not import media modules: {e}")
        return False

    processed = 0

    for import_dir, entry_type in [
        (import_media.PAGES_IMPORT, "PAGE"),
        (import_media.POSTS_IMPORT, "POST")
    ]:
        if not import_dir.exists():
            continue

        folders = import_media.discover_import_folders(import_dir)
        for folder in folders:
            image_files, video_files = import_media.identify_media_files(folder)
            all_media = image_files + video_files
            first_image = image_files[0] if image_files else None

            result = import_media.process_folder(folder, entry_type=entry_type)
            markdown_dest = result[0] if result else None
            moved_paths = result[1] if result else []

            if markdown_dest and markdown_dest.exists() and moved_paths:
                with open(markdown_dest, "r", encoding="utf-8") as f:
                    content = f.read()

                media_list = []
                for moved_path in moved_paths:
                    is_video = moved_path.suffix.lower() in import_media.VIDEO_EXTENSIONS
                    media_path = "/" + str(moved_path.relative_to(import_media.SRC_DIR))
                    thumb = None
                    if is_video:
                        if first_image:
                            thumb_sanitized = import_media.sanitize_filename(first_image.name)
                            thumb_path = import_media.IMAGES_DIR / thumb_sanitized
                            thumb = "/" + str(thumb_path.relative_to(import_media.SRC_DIR))
                        else:
                            thumb = media_path
                    media_list.append((media_path, is_video, thumb))

                if media_list:
                    new_content = media_placement.insert_media(content, media_list)
                    with open(markdown_dest, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"  Embedded {len(media_list)} media references")
                    processed += 1

    if processed > 0:
        print(f"\nProcessed and embedded media for {processed} item(s).")
    return processed > 0


def has_import_folders(pages_only=False, posts_only=False):
    repo_root = Path(__file__).resolve().parent.parent.parent.parent
    import_base = repo_root / "import"
    pattern = __import__("re").compile(r'^\d{8}_.+')

    for import_dir in [import_base / "pages", import_base / "_posts"]:
        if not import_dir.exists():
            continue
        if pages_only and import_dir.name == "_posts":
            continue
        if posts_only and import_dir.name == "pages":
            continue
        for item in import_dir.iterdir():
            if item.is_dir() and pattern.match(item.name):
                return True
    return False


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Validate Jekyll pages and posts"
    )
    parser.add_argument(
        "--pages",
        action="store_true",
        help="Validate pages only (skip posts)"
    )
    parser.add_argument(
        "--posts",
        action="store_true",
        help="Validate posts only (skip pages)"
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Auto-apply correct layouts based on category"
    )
    parser.add_argument(
        "--import",
        action="store_true",
        dest="do_import",
        help="Import media from /import/ folders before validation"
    )

    args = parser.parse_args()

    if not VALIDATOR.exists():
        print(f"Error: Validator script not found at {VALIDATOR}")
        sys.exit(1)

    print("=" * 60)
    print("BACKUP PHASE")
    print("=" * 60)
    backup_import_folders()
    print()

    # Auto-detect import folders when no specific flags are given
    auto_import = not args.pages and not args.posts and not args.do_import
    should_import = args.do_import or (auto_import and has_import_folders())

    if should_import:
        print("=" * 60)
        print("IMPORT PHASE")
        print("=" * 60)
        import_media_and_embed()
        print()

    files = find_files(pages_only=args.pages, posts_only=args.posts)

    if not files:
        print("No markdown files found to validate.")
        sys.exit(0)

    print(f"Found {len(files)} markdown file(s) to validate:\n")
    for f in files:
        print(f"  - {f}")
    print()

    all_passed = True
    fixed_files = []
    for filepath in files:
        has_issues, missing, data, content, file_type = FIX_FRONTMATTER.has_frontmatter_issues(filepath)

        if has_issues:
            if is_interactive():
                fixed = interactive_fix(filepath, file_type, missing, data, content)
                if fixed:
                    fixed_files.append(filepath)
            else:
                report_frontmatter_issues(filepath, file_type, missing, data, content)

        result = run_validator(filepath, apply_fixes=args.apply)
        if result.returncode != 0:
            all_passed = False
        print()

    print("=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    if fixed_files:
        print(f"Fixed frontmatter in {len(fixed_files)} file(s):")
        for f in fixed_files:
            print(f"  - {f}")
        print()
    if all_passed:
        print("✓ All files passed validation.")
    else:
        print("✗ Some files failed validation. Review errors above.")

    cleanup_import_folders()

    if not all_passed:
        sys.exit(1)


def cleanup_import_folders():
    import re
    repo_root = Path(__file__).resolve().parent.parent.parent.parent
    import_base = repo_root / "import"
    pattern = re.compile(r'^\d{8}_.+')
    removed = 0

    for import_dir in [import_base / "pages", import_base / "_posts"]:
        if not import_dir.exists():
            continue
        for item in import_dir.iterdir():
            if item.is_dir() and pattern.match(item.name):
                try:
                    shutil.rmtree(str(item))
                    print(f"  Cleaned up: {item.name}")
                    removed += 1
                except Exception as e:
                    print(f"  Warning: Could not remove {item.name}: {e}", file=sys.stderr)

    if removed > 0:
        print(f"\nCleaned up {removed} import folder(s).")


if __name__ == "__main__":
    main()
