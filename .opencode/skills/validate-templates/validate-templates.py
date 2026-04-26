#!/usr/bin/env python3
"""
Validates Jekyll markdown files for required template sections.
Checks posts and pages for proper frontmatter and Liquid code blocks.
Can auto-apply correct layouts based on category.

Usage:
  python validate-templates.py <path>              # Validate only
  python validate-templates.py <path> --apply      # Validate and auto-fix layouts
  python validate-templates.py <path> --pages      # Validate pages only
"""

import sys
import re
import argparse
from pathlib import Path


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


def get_category_from_frontmatter(frontmatter):
    match = re.search(r'categories:\s*(\S+)', frontmatter)
    if match:
        return match.group(1).strip()
    return None


def get_layout_from_frontmatter(frontmatter):
    match = re.search(r'layout:\s*(\S+)', frontmatter)
    if match:
        return match.group(1).strip()
    return None


def validate_frontmatter(content, file_type):
    errors = []
    
    if not content.startswith('---'):
        errors.append("Missing frontmatter block")
        return errors, None
    
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        errors.append("Invalid frontmatter format")
        return errors, None
    
    frontmatter = match.group(1)
    
    for field in ['layout', 'title', 'categories']:
        if f'{field}:' not in frontmatter:
            errors.append(f"Missing '{field}' in frontmatter")
    
    if file_type == 'post' and 'date:' not in frontmatter:
        errors.append("Missing 'date' in frontmatter (required for posts)")
    elif file_type == 'page' and 'permalink:' not in frontmatter:
        errors.append("Missing 'permalink' in frontmatter (required for pages)")
    
    category = get_category_from_frontmatter(frontmatter)
    layout = get_layout_from_frontmatter(frontmatter)
    
    if file_type == 'post' and category and layout and category in CATEGORY_LAYOUT_MAP:
        expected_layout = CATEGORY_LAYOUT_MAP[category]
        if layout != expected_layout:
            errors.append(
                f"Layout mismatch: category '{category}' should use layout '{expected_layout}', "
                f"but found '{layout}'"
            )
    
    return errors, (category, layout)


def validate_post_content(content):
    errors = []
    
    if 'where_exp' not in content or 'post.categories contains' not in content:
        errors.append("Missing related posts Liquid block")
    
    if 'limit: 2' not in content:
        errors.append("Missing 'limit: 2' in related posts loop")
    
    if 'p.categories contains' not in content:
        errors.append("Missing dynamic topic page link")
    
    frontmatter_end = content.find('\n---\n', 4)
    liquid_start = content.find('{% capture category %}')
    
    if frontmatter_end == -1 or liquid_start == -1:
        errors.append("Cannot parse content structure")
        return errors
    
    content_between = content[frontmatter_end + 5:liquid_start].strip()
    if len(content_between) < 10:
        errors.append("Insufficient content before Liquid block")
    
    return errors


def validate_page_content(content):
    errors = []
    
    if 'where: "categories", page.categories' not in content:
        errors.append("Missing post listing Liquid block")
    
    frontmatter_end = content.find('\n---\n', 4)
    liquid_start = content.find('{% assign filtered_posts = site.posts')
    
    if frontmatter_end == -1 or liquid_start == -1:
        errors.append("Cannot parse content structure")
        return errors
    
    content_between = content[frontmatter_end + 5:liquid_start].strip()
    if len(content_between) < 10:
        errors.append("Insufficient content before Liquid block")
    
    return errors


def apply_layout(filepath, category, expected_layout):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = re.sub(
        r'(layout:)\s*\S+',
        f'\\1 {expected_layout}',
        content,
        count=1
    )
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False


def validate_file(filepath, apply_fixes=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    file_type = 'post' if '_posts' in str(filepath) else 'page'
    
    print(f"\n{'='*60}")
    print(f"Validating: {filepath}")
    print(f"Type: {file_type}")
    print('='*60)
    
    errors, layout_info = validate_frontmatter(content, file_type)
    if not errors:
        print("  ✓ Frontmatter valid")
        print("  ✓ Required fields present")
    else:
        for error in errors:
            if 'Layout mismatch' in error:
                print(f"  ⚠ {error}")
            else:
                print(f"  ✗ {error}")
    
    if file_type == 'post':
        content_errors = validate_post_content(content)
    else:
        content_errors = validate_page_content(content)
    
    if not content_errors:
        print("  ✓ Liquid blocks valid")
        print("  ✓ Content before Liquid block")
    else:
        for error in content_errors:
            print(f"  ✗ {error}")
    
    errors.extend(content_errors)
    
    if apply_fixes and layout_info:
        category, layout = layout_info
        if category and category in CATEGORY_LAYOUT_MAP:
            expected_layout = CATEGORY_LAYOUT_MAP[category]
            if layout != expected_layout:
                if apply_layout(filepath, category, expected_layout):
                    print(f"  🔧 Auto-applied layout '{expected_layout}' for category '{category}'")
                    errors = [e for e in errors if 'Layout mismatch' not in e]
    
    return len(errors) == 0


def main():
    parser = argparse.ArgumentParser(
        description='Validate Jekyll markdown templates'
    )
    parser.add_argument('path', help='File or directory to validate')
    parser.add_argument(
        '--apply',
        action='store_true',
        help='Auto-apply correct layouts based on category'
    )
    parser.add_argument(
        '--pages',
        action='store_true',
        help='Validate pages only (skip posts)'
    )
    parser.add_argument(
        '--posts',
        action='store_true',
        help='Validate posts only (skip pages)'
    )
    
    args = parser.parse_args()
    path = Path(args.path)
    
    if path.is_file():
        files = [path]
    elif path.is_dir():
        if args.pages:
            files = [f for f in path.glob('*.md') if '_posts' not in str(f)]
        elif args.posts:
            files = list(path.glob('*.md')) + list(path.glob('*.markdown'))
            files = [f for f in files if '_posts' in str(f)]
        else:
            files = list(path.glob('*.md')) + list(path.glob('*.markdown'))
    else:
        print(f"Error: {path} not found")
        sys.exit(1)
    
    if not files:
        print(f"No markdown files found in {path}")
        sys.exit(0)
    
    results = [(f, validate_file(f, apply_fixes=args.apply)) for f in files]
    
    print(f"\n{'='*60}")
    print("SUMMARY")
    print('='*60)
    
    passed = sum(1 for _, v in results if v)
    failed = sum(1 for _, v in results if not v)
    
    for filepath, valid in results:
        status = "✓ PASS" if valid else "✗ FAIL"
        print(f"{status}: {filepath}")
    
    print(f"\nTotal: {len(results)} | Passed: {passed} | Failed: {failed}")
    
    if args.apply:
        print("\n💡 Tip: Run without --apply to validate without making changes.")
    
    sys.exit(0 if failed == 0 else 1)


if __name__ == '__main__':
    main()
