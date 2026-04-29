#!/usr/bin/env python3
"""
Interactive frontmatter fixer for Jekyll pages and posts.
Detects missing frontmatter and provides structured output for agent-driven user interaction.

For PAGES with missing frontmatter:
- Extracts images from content to suggest as card_image
- Asks user for: title, permalink, categories
- Uses first image found as card_image suggestion

For POSTS with missing frontmatter:
- Presents existing layout/categories values from CATEGORY_LAYOUT_MAP
- Asks user for: title, date, categories (with suggestions)

Usage:
  python fix-frontmatter.py --dry-run    # Show what would be fixed without changes
  python fix-frontmatter.py --pages      # Fix pages only
  python fix-frontmatter.py --posts      # Fix posts only
"""

import sys
import re
import json
import argparse
from pathlib import Path
from datetime import datetime

SRC_DIR = Path(__file__).resolve().parent.parent.parent.parent / "src"

AVAILABLE_IMAGES = [
    "/assets/images/img.jpg",
    "/assets/images/thumb.png",
    "/assets/images/thumb2.png",
    "/assets/images/thumb3.jpeg",
    "/assets/images/thumb4.jpeg",
    "/assets/images/thumb5.jpeg",
    "/assets/images/thumb6.jpeg",
    "/assets/images/thumb7.jpeg",
    "/assets/images/thumb8.jpeg",
    "/assets/images/thumb9.jpeg",
]

CATEGORY_LAYOUT_MAP = {
    'travel': 'travel',
    'retirement': 'retirement',
    'ageing': 'ageing',
    'music': 'music',
    'product': 'product',
    'topic1': 'post',
    'topic2': 'post',
    'topic3': 'post',
}

LAYOUTS = ["post", "travel", "retirement", "ageing", "music", "product", "page"]
CATEGORIES = ["travel", "retirement", "ageing", "music", "product", "topic1", "topic2", "topic3"]


def find_files(pages_only=False, posts_only=False):
    if not SRC_DIR.exists():
        return []
    files = []
    for md_file in SRC_DIR.rglob("*.md"):
        parts = md_file.parts
        if "_site" in parts or ".opencode" in parts or "_templates" in parts:
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


def extract_frontmatter(content):
    if not content.startswith('---'):
        return None, None
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return None, None
    return match.group(1), match.end()


def parse_frontmatter(frontmatter):
    data = {}
    if not frontmatter:
        return data
    for line in frontmatter.split('\n'):
        line = line.strip()
        if ':' in line:
            key, value = line.split(':', 1)
            data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def get_missing_fields(frontmatter, file_type):
    data = parse_frontmatter(frontmatter) if frontmatter else {}
    missing = []
    # For type: page files, layout should always be 'page' - don't add it to missing
    # For type: post files, layout may vary by category
    for field in ['title', 'categories']:
        if field not in data:
            missing.append(field)
    if file_type == 'post' and 'date' not in data:
        missing.append('date')
    if file_type == 'post' and 'author' not in data:
        missing.append('author')
    elif file_type == 'page' and 'permalink' not in data:
        missing.append('permalink')
    # card_image is required for pages (topic landing pages)
    if file_type == 'page' and 'card_image' not in data:
        missing.append('card_image')
    # type field is always required
    if 'type' not in data:
        missing.append('type')
    return missing, data


def extract_images_from_content(content):
    images = re.findall(r'!\[.*?\]\(([^)]+)\)', content)
    return [img for img in images if img.startswith('/assets/images/')]


def extract_first_image_from_content(content):
    images = extract_images_from_content(content)
    if images:
        return images[0]
    if AVAILABLE_IMAGES:
        return AVAILABLE_IMAGES[0]
    return None


def build_filename(filepath, file_type):
    if file_type == 'post':
        return filepath.name
    else:
        return filepath.name


def has_frontmatter_issues(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    frontmatter, end_pos = extract_frontmatter(content)
    data = parse_frontmatter(frontmatter) if frontmatter else {}
    file_type = data.get('type', 'post' if '_posts' in str(filepath) else 'page')
    missing, data = get_missing_fields(frontmatter, file_type)
    return len(missing) > 0, missing, data, content, file_type


def generate_fix_proposal(filepath, file_type, missing, data, content):
    proposal = {
        'path': str(filepath),
        'file_type': file_type,
        'missing_fields': missing,
        'current_values': data,
    }

    filename = filepath.name.replace('.md', '').replace('.markdown', '')

    if file_type == 'page':
        proposal['suggestions'] = {}

        if 'title' in missing:
            title_candidate = filename
            if title_candidate.startswith('topic-'):
                title_candidate = title_candidate.replace('topic-', '').replace('-', ' ').title()
            proposal['suggestions']['title'] = title_candidate.title()

        if 'permalink' in missing:
            slug = filename.replace('-', '/')
            if not slug.endswith('/'):
                slug += '/'
            if slug.startswith('/'):
                slug = slug[1:]
            proposal['suggestions']['permalink'] = f'/{slug}'

        if 'categories' in missing:
            proposal['suggestions']['categories'] = CATEGORIES.copy()

        if 'layout' in missing:
            proposal['suggestions']['layout'] = 'page'

        if 'type' in missing:
            proposal['suggestions']['type'] = 'page'

        if 'published' in missing:
            proposal['suggestions']['published'] = 'true'

        # Always suggest card_image from page images if available
        image = extract_first_image_from_content(content)
        if image:
            proposal['suggestions']['card_image'] = image

    else:
        proposal['suggestions'] = {}

        if 'title' in missing:
            title_candidate = filename
            for pattern in [r'^\d{4}-\d{2}-\d{2}-', r'^\d{4}-\d{2}-\d{2}_']:
                match = re.search(pattern, title_candidate)
                if match:
                    title_candidate = title_candidate[match.end():]
                    break
            title_candidate = title_candidate.replace('-', ' ').replace('_', ' ').title()
            proposal['suggestions']['title'] = title_candidate

        if 'date' in missing:
            dates = re.findall(r'\d{4}-\d{2}-\d{2}', filename)
            if dates:
                try:
                    dt = datetime.strptime(dates[0], '%Y-%m-%d')
                    proposal['suggestions']['date'] = dt.strftime('%Y-%m-%d %H:%M:%S +0800')
                except:
                    proposal['suggestions']['date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S +0800')
            else:
                proposal['suggestions']['date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S +0800')

        if 'author' in missing:
            proposal['suggestions']['author'] = 'LBB88'

        if 'categories' in missing:
            proposal['suggestions']['categories'] = CATEGORIES.copy()

        if 'type' in missing:
            proposal['suggestions']['type'] = 'post'

        if 'layout' in missing:
            proposal['suggestions']['layout'] = list(set(CATEGORY_LAYOUT_MAP.values()))

    return proposal


def apply_fix(filepath, file_type, fixes):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    frontmatter, end_pos = extract_frontmatter(content)

    if frontmatter is None:
        data = {}
        data.update(fixes)
        new_frontmatter = "---\n"
        for key, value in data.items():
            new_frontmatter += f'{key}: {value}\n'
        new_frontmatter += "---\n"
        new_content = new_frontmatter + "\n" + content
    else:
        data = parse_frontmatter(frontmatter)
        data.update(fixes)
        new_frontmatter = "---\n"
        for key, value in data.items():
            new_frontmatter += f'{key}: {value}\n'
        new_frontmatter += "---\n"
        new_content = content[end_pos:]
        if not new_content.startswith('\n'):
            new_content = '\n' + new_content
        new_content = new_frontmatter + new_content

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True, "Fixed"


def main():
    parser = argparse.ArgumentParser(description="Fix missing frontmatter interactively")
    parser.add_argument("--pages", action="store_true", help="Fix pages only")
    parser.add_argument("--posts", action="store_true", help="Fix posts only")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be fixed")
    parser.add_argument("--json", action="store_true", help="Output JSON for agent integration")
    args = parser.parse_args()

    files = find_files(pages_only=args.pages, posts_only=args.posts)
    issues = []

    for filepath in files:
        has_issues, missing, data, content, file_type = has_frontmatter_issues(filepath)
        if has_issues:
            proposal = generate_fix_proposal(filepath, file_type, missing, data, content)
            issues.append(proposal)

    if not issues:
        print("No frontmatter issues found.")
        sys.exit(0)

    print(f"Found {len(issues)} file(s) with missing frontmatter:\n")
    for issue in issues:
        print(f"  - {issue['path']} ({issue['file_type']}): missing {', '.join(issue['missing_fields'])}")

    if args.json:
        print("\n" + "="*60)
        print("JSON OUTPUT")
        print("="*60 + "\n")
        print(json.dumps(issues, indent=2))

    if args.dry_run:
        print("\nDry run - no changes made.")
        sys.exit(0)

    print("\n" + "="*60)
    print("To fix these, the agent will:")
    print("- Ask you for the missing values")
    print("- Present existing layout/categories options for posts")
    print("- Use an existing image from the page as card_image for pages")
    print("- Ask you to confirm before making any changes")
    print("="*60)

    sys.exit(0)


if __name__ == "__main__":
    main()
