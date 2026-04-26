#!/usr/bin/env python3
"""
Wrapper script to discover and validate Jekyll pages and posts.
Activates the validate-templates skill for all markdown files in src/.

Usage:
  python validate-new-pages.py              # Validate all pages and posts
  python validate-new-pages.py --pages      # Validate pages only
  python validate-new-pages.py --posts      # Validate posts only
  python validate-new-pages.py --apply      # Auto-fix layout mismatches
"""

import subprocess
import sys
from pathlib import Path

VALIDATOR = Path(__file__).resolve().parent.parent / "validate-templates" / "validate-templates.py"
SRC_DIR = Path(__file__).resolve().parent.parent.parent.parent / "src"


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
        if md_file.name in ("about.md", "index.md"):
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

    args = parser.parse_args()

    if not VALIDATOR.exists():
        print(f"Error: Validator script not found at {VALIDATOR}")
        sys.exit(1)

    files = find_files(pages_only=args.pages, posts_only=args.posts)

    if not files:
        print("No markdown files found to validate.")
        sys.exit(0)

    print(f"Found {len(files)} markdown file(s) to validate:\n")
    for f in files:
        print(f"  - {f}")
    print()

    all_passed = True
    for filepath in files:
        result = run_validator(filepath, apply_fixes=args.apply)
        if result.returncode != 0:
            all_passed = False
        print()

    print("=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    if all_passed:
        print("✓ All files passed validation.")
    else:
        print("✗ Some files failed validation. Review errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
