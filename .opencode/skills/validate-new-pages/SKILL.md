---
name: validate-new-pages
description: >
  Validate newly added or modified Jekyll pages and posts using the
  validate-templates skill. Run this when new topic pages, posts, or content
  files are created or updated. Triggers on: "validate new pages", "check new
  pages", "validate templates for new pages", "run validation on pages", "check
  page templates", "validate posts", "verify new content".
license: MIT
compatibility: opencode
---

# Validate New Pages

## Media Import

This skill can also import media files from `/import/pages/` and `/import/_posts/` folders into your Jekyll site.

### What It Does

When using the `--import` flag, the skill will:

1. **Discover import folders** matching `YYYYMMDD_*` pattern in:
   - `/import/pages/` — for topic pages
   - `/import/_posts/` — for blog posts

2. **Move media files** to appropriate asset directories:
   - Images (`.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`) → `/src/assets/images/`
   - Videos (`.mp4`, `.webm`, `.mov`) → `/src/assets/videos/`

3. **Rename and move markdown files**:
   - Pages: `content.md` → `/src/{slug}.md` (slug from first media filename)
   - Posts: `content.md` → `/src/_posts/YYYY-MM-DD_{slug}.md`

4. **Embed media references** in the markdown body:
   - Images: `![alt](/assets/images/photo.jpg)`
   - Videos: `[![Video Thumbnail](/assets/images/thumb.jpeg)](/assets/videos/video.mp4)`
   - First media appears at the top of the article body
   - Remaining media are evenly spaced throughout the article

5. **Track processed imports** in `.opencode/skills/validate-new-pages/processed.log`

### Usage

```bash
# Import media and validate
python3 .opencode/skills/validate-new-pages/validate-new-pages.py --import

# Import media and validate pages only
python3 .opencode/skills/validate-new-pages/validate-new-pages.py --import --pages

# Import media and validate posts only
python3 .opencode/skills/validate-new-pages/validate-new-pages.py --import --posts
```

### Import Folder Structure

Each import folder should contain:
- `content.md` — the markdown content (with optional frontmatter)
- Media files — images and/or videos to be imported

Example:
```
/import/pages/20260428_my-article/
  ├── content.md
  └── featured-photo.jpg
```

This will create:
- `/src/assets/images/featured-photo.jpg` (moved media)
- `/src/featured-photo.md` (renamed and moved markdown with embedded image)

Validates Jekyll markdown files (pages and posts) against required template
structure using the existing `validate-templates` Python script.

When files are missing required frontmatter, this skill interactively
prompts for the missing values and applies fixes after user confirmation.

## When to Use

- After creating new topic pages or blog posts
- Before committing changes to ensure template compliance
- When reviewing pull requests with new content
- After modifying existing page/post frontmatter or Liquid blocks
- Any time "validate", "check", "verify" is mentioned alongside pages/posts
- When frontmatter is missing and needs to be added

## What It Checks

**Pages (`type: page`):**
- Frontmatter contains `layout: page`, `title`, `permalink`, `categories`, `type: page`
- Post listing Liquid block (`where: "categories", page.categories`)
- Content exists before Liquid blocks
- Layout is always `page` — will NOT be auto-changed by `--apply`

**Posts (`type: post`):**
- Frontmatter contains `layout`, `title`, `date`, `categories`, `type: post`
- Related posts Liquid block (`where_exp` with `post.categories contains`)
- `limit: 2` set in the loop
- Dynamic topic page link (`p.categories contains`)
- Content exists before Liquid blocks
- Layout will be auto-corrected to match category if `--apply` is used

**Type Field:**
- The `type` field differentiates pages from posts
- `type: page` — topic/landing pages; layout stays as `page`
- `type: post` — blog posts; layout maps to category (travel→travel, music→music, etc.)
- If `type` is missing, the skill falls back to path-based detection (`_posts/` → post)

**Automatic Handling:**
- **Missing frontmatter** → Interactive prompts for values (interactive mode) or reports suggestions (non-interactive)
- **Layout mismatches** → Auto-corrected with `--apply` for posts only; pages are skipped

## How to Use

### 1. Validate All New/Modified Pages (Interactive)

Run the wrapper script to find and validate all `.md` files in `src/`:

```bash
python3 .opencode/skills/validate-new-pages/validate-new-pages.py
```

This discovers all `.md` files under `src/` (excluding `_site/` and
`.opencode/`) and runs validation on each file.

**If frontmatter is missing**, you will be prompted interactively to fill in
the missing fields with suggestions. The fixes are applied only after you
confirm.

### 2. Validate Pages Only

```bash
python3 .opencode/skills/validate-new-pages/validate-new-pages.py --pages
```

### 3. Validate Posts Only

```bash
python3 .opencode/skills/validate-new-pages/validate-new-pages.py --posts
```

### 4. Auto-Fix Layout Mismatches

```bash
python3 .opencode/skills/validate-new-pages/validate-new-pages.py --apply
```

⚠️ Review changes before committing when using `--apply`.

## Fixing Missing Frontmatter

When pages or posts are missing required frontmatter fields, the skill detects
them before running the validator and offers to fix them interactively.

### Interactive Mode (Terminal)

When running in a terminal (interactive session), the skill will:

1. **Show missing fields** and suggested values
2. **Prompt for each field** — you can:
   - **Accept** the suggestion (press Enter)
   - **Edit** the value (type `e` then enter your own)
   - **Skip** the field (type `s`)
3. **Show a summary** of all changes
4. **Ask for confirmation** (type `y`) before writing to the file
5. **Run the validator** on the fixed file

### Non-Interactive Mode (Piped/Redirected)

When running in a non-interactive environment (e.g., CI/CD, piped input), the
skill will:
- Report frontmatter issues with suggested values
- Continue with validation without modifying files

### Suggestions Provided

**For Pages (`type: page`):**
- **title**: Derived from filename (e.g., `topic-travel.md` → "Travel")
- **permalink**: Auto-generated from filename (e.g., `topic-travel.md` → `/travel/`)
- **categories**: List of available categories to choose from
- **card_image**: First image found in page content (if any)
- **type**: Always suggests `page`
- **layout**: Always suggests `page` (not auto-changed)

**For Posts (`type: post`):**
- **title**: Derived from filename, stripping the date prefix
- **date**: Extracted from filename if present, otherwise today's date
- **categories**: List of available categories to choose from
- **type**: Always suggests `post`
- **layout**: Suggested based on chosen category (e.g., travel→travel, music→music)

### Available Categories

```
travel, retirement, ageing, music, product, topic1, topic2, topic3
```

### Available Images (for card_image)

```
/assets/images/img.jpg
/assets/images/thumb.png
/assets/images/thumb2.png
/assets/images/thumb3.jpeg
/assets/images/thumb4.jpeg
/assets/images/thumb5.jpeg
/assets/images/thumb6.jpeg
/assets/images/thumb7.jpeg
/assets/images/thumb8.jpeg
/assets/images/thumb9.jpeg
```

## Interpreting Output

### Normal Validation (No Issues)

```
============================================================
Validating: src/topic-travel.md
Type: page
============================================================
  ✓ Frontmatter valid
  ✓ Required fields present
  ✓ Liquid blocks valid
  ✓ Content before Liquid block

============================================================
SUMMARY
============================================================
✓ PASS: src/topic-travel.md

Total: 1 | Passed: 1 | Failed: 0
```

### Interactive Frontmatter Fixing

When frontmatter is missing in an interactive session:

```
============================================================
FRONTMATTER FIX NEEDED: test-page.md
Type: page
Missing fields: layout, title, categories, permalink
============================================================

  Field: title
  Suggested: Test-Page
  Accept [Enter], Edit [e], Skip [s]:

  Field: permalink
  Suggested: /test-page/
  Accept [Enter], Edit [e], Skip [s]:

  Field: categories
  Suggestions:
    1. travel
    2. retirement
    3. ageing
    4. music
    5. product
    6. topic1
    7. topic2
    8. topic3
    c. Enter custom value
    s. Skip this field
  Select [1-8], c, or s: 1

  Summary of fixes for test-page.md:
    layout: page
    title: Test-Page
    categories: travel
    permalink: /test-page/

  Apply these fixes? [y/N]: y
  ✓ Fixed frontmatter in src/test-page.md
```

A failed file shows `✗` with specific errors. Fix them and re-run.

## Underlying Tools

- **validate-new-pages.py** - Main wrapper that discovers files, detects missing frontmatter,
  prompts interactively for fixes, and runs the validator
- **validate-templates.py** - Validates Jekyll markdown templates for required frontmatter
  and Liquid blocks
- **fix-frontmatter.py** - Generates fix proposals and applies frontmatter corrections

The wrapper handles file discovery, frontmatter fixing, and validation orchestration.
