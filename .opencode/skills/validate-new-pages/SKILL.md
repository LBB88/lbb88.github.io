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

Validates Jekyll markdown files (pages and posts) against required template
structure using the existing `validate-templates` Python script.

## When to Use

- After creating new topic pages or blog posts
- Before committing changes to ensure template compliance
- When reviewing pull requests with new content
- After modifying existing page/post frontmatter or Liquid blocks
- Any time "validate", "check", "verify" is mentioned alongside pages/posts

## What It Checks

**Pages (`layout: page`):**
- Frontmatter contains `layout`, `title`, `permalink`, `categories`
- Post listing Liquid block (`where: "categories", page.categories`)
- Content exists before Liquid blocks

**Posts (`layout: post`):**
- Frontmatter contains `layout`, `title`, `date`, `categories`
- Related posts Liquid block (`where_exp` with `post.categories contains`)
- `limit: 2` set in the loop
- Dynamic topic page link (`p.categories contains`)
- Content exists before Liquid blocks

**Layout auto-fix (posts only):**
- Maps categories to expected layouts (e.g., `travel` → `travel`)
- Can auto-correct mismatched layouts with `--apply`

## How to Use

### 1. Validate All New/Modified Pages

Run the wrapper script to find and validate all `.md` files in `src/`:

```bash
python3 .opencode/skills/validate-new-pages/validate-new-pages.py
```

This discovers all `.md` files under `src/` (excluding `_site/` and
`.opencode/`) and runs validation on each.

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

## Interpreting Output

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

A failed file shows `✗` with specific errors. Fix them and re-run.

## Underlying Tool

This skill wraps `.opencode/skills/validate-templates/validate-templates.py`.
The wrapper handles file discovery; the validator handles actual checking.
