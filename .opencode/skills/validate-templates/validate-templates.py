#!/usr/bin/env python3
"""
Validates Jekyll markdown files for required template sections.
Checks posts and pages for proper frontmatter and Liquid code blocks.
Usage: python validate-templates.py <path>
"""

import sys
import re
from pathlib import Path


def validate_frontmatter(content, file_type):
    errors = []
    
    if not content.startswith('---'):
        errors.append("Missing frontmatter block")
        return errors
    
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        errors.append("Invalid frontmatter format")
        return errors
    
    frontmatter = match.group(1)
    
    for field in ['layout', 'title', 'categories']:
        if f'{field}:' not in frontmatter:
            errors.append(f"Missing '{field}' in frontmatter")
    
    if file_type == 'post' and 'date:' not in frontmatter:
        errors.append("Missing 'date' in frontmatter (required for posts)")
    elif file_type == 'page' and 'permalink:' not in frontmatter:
        errors.append("Missing 'permalink' in frontmatter (required for pages)")
    
    return errors


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


def validate_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    file_type = 'post' if '_posts' in str(filepath) else 'page'
    
    print(f"\n{'='*60}")
    print(f"Validating: {filepath}")
    print(f"Type: {file_type}")
    print('='*60)
    
    errors = validate_frontmatter(content, file_type)
    if not errors:
        print("  ✓ Frontmatter valid")
        print("  ✓ Required fields present")
    else:
        for error in errors:
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
    return len(errors) == 0


def main():
    if len(sys.argv) < 2:
        print("Usage: validate-templates.py <path>")
        sys.exit(1)
    
    path = Path(sys.argv[1])
    
    if path.is_file():
        files = [path]
    elif path.is_dir():
        files = list(path.glob('*.md')) + list(path.glob('*.markdown'))
    else:
        print(f"Error: {path} not found")
        sys.exit(1)
    
    if not files:
        print(f"No markdown files found in {path}")
        sys.exit(0)
    
    results = [(f, validate_file(f)) for f in files]
    
    print(f"\n{'='*60}")
    print("SUMMARY")
    print('='*60)
    
    passed = sum(1 for _, v in results if v)
    failed = sum(1 for _, v in results if not v)
    
    for filepath, valid in results:
        status = "✓ PASS" if valid else "✗ FAIL"
        print(f"{status}: {filepath}")
    
    print(f"\nTotal: {len(results)} | Passed: {passed} | Failed: {failed}")
    sys.exit(0 if failed == 0 else 1)


if __name__ == '__main__':
    main()
