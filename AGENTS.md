# AGENTS.md

This file provides guidance to agentic coding agents operating in this repository.

## Project Overview

This is a Jekyll-powered static website deployed on GitHub Pages using the Minima theme. Content lives in `src/` and is built to `_site/` for deployment.

## Build Commands

```bash
# Preview locally (from src/ directory)
bundle exec jekyll serve

# Build for production (outputs to src/_site/)
bundle exec jekyll build
```

### Deployment

The site deploys automatically via GitHub Actions when pushing to `main`:

```bash
# Push to main — GitHub Actions triggers automatically
git push origin main
```

### GitHub Pages Setup (first time)

If GitHub Pages is not enabled:
1. Go to repository **Settings → Pages**
2. Under **Build and deployment**, select **GitHub Actions** as source
3. Next push to `main` triggers deployment

## Project Structure

All source files live in `src/`:

```
src/
├── _config.yml          # Jekyll configuration (title, theme, plugins)
├── _posts/              # Blog posts — naming format: YYYY-MM-DD-title.md
├── _layouts/           # HTML layout templates (*.html)
├── _includes/          # Reusable Liquid includes (e.g., youtube.html)
├── _templates/          # Content templates for new pages
├── assets/
│   ├── images/         # Image files
│   ├── videos/         # Video files
│   └── main.scss       # Custom styles (imported by Minima)
├── index.md            # Home page front matter (layout: home)
├── about.md            # About page
├── topic-*.md          # Topic/category landing pages
└── *.md               # Other pages
```

## Page Types

### Topic Pages (Category Landing Pages)

Topic pages list all posts for a given category. They use `layout: page` and should include:

- `title` — shown in navigation
- `permalink` — URL path (e.g., `/travel/`)
- `categories` — must match the `categories` field in posts
- `card_image` — background image for the home page topic card

**Example frontmatter:**

```yaml
---
layout: page
title: "Travel"
permalink: /travel/
categories: travel
card_image: /assets/images/img.jpg
---
```

### Blog Posts

Blog posts live in `_posts/` with format `YYYY-MM-DD-title.md`. Use `layout: post` and assign a `categories` value matching a topic page to have it listed there.

### Home Page

The home page (`index.md`) uses `layout: home` and is configured entirely through frontmatter:

```yaml
---
layout: home
hero_title: "Welcome to My Blog"
hero_description: "Exploring topics and sharing knowledge."
hero_image: /assets/images/img.jpg
hero_image_alt: "Blog header image"
topics_title: "Browse by Topic"
posts_title: "Latest Posts"
---
```

## Content Templates

Pre-built topic templates are available in `_templates/`:
- `ageing-template.md`
- `music-template.md`
- `product-template.md`
- `retirement-template.md`
- `travel-template.md`

Copy one to `src/` and rename it to create a new topic page. Then update `title`, `permalink`, `categories`, and `card_image` in the frontmatter.

## Git Workflow

- Branch name: `main`
- Commit changes, push to origin
- GitHub Actions auto-deploys on push to `main`
- **Do not commit `_site/`** — it's generated output

## Code Style Guidelines

### Frontmatter

- Always include frontmatter at the very top of `.md` files
- Required fields: `layout`, `title`
- Posts also need: `date`, `categories`
- Topic pages also need: `permalink`, `categories`
- Dates in filenames and frontmatter must be today or in the past

### Markdown

- Use standard Markdown formatting
- Kramdown attributes for styling: `{: attribute="value"}`
- HTML is allowed inside Markdown content

### CSS

- Custom styles go in `assets/main.scss` (imported by Minima)
- Use CSS custom properties for theming
- Box-sizing reset on `*`

### JavaScript

- Vanilla JS only — no frameworks
- Wrap in `DOMContentLoaded`:

```javascript
document.addEventListener('DOMContentLoaded', () => { ... });
```

## Error Handling

- Posts not showing? Check that the date is today or in the past
- Pages blank? Ensure actual content exists after frontmatter
- Images not loading? Verify path is correct and file exists in `src/assets/images/`
- Build failing? Run `bundle exec jekyll build` locally to see errors

## VS Code Configuration

Project includes `.vscode/settings.json` with basic settings. The Jekyll plugin "JM Lahoda" is recommended for syntax highlighting in Liquid templates.

## Validation

Two validation skills are available to check that posts and topic pages contain all required sections.

### Validate New Pages (Recommended)

The `validate-new-pages` skill automatically discovers all `.md` files in `src/` and validates them:

```bash
# Validate all pages and posts
python3 .opencode/skills/validate-new-pages/validate-new-pages.py

# Validate pages only
python3 .opencode/skills/validate-new-pages/validate-new-pages.py --pages

# Validate posts only
python3 .opencode/skills/validate-new-pages/validate-new-pages.py --posts

# Auto-fix layout mismatches (posts only)
python3 .opencode/skills/validate-new-pages/validate-new-pages.py --apply
```

This wrapper automatically:
- Discovers all `.md` files under `src/` (excluding `_site/`, `.opencode/`, `_templates/`, `about.md`, `index.md`)
- Runs the `validate-templates` validator on each file
- Reports pass/fail status with specific errors

### Validate Templates (Manual)

For targeted validation of specific files or directories:

```bash
# Validate all posts
python3 .opencode/skills/validate-templates/validate-templates.py src/_posts/

# Validate a specific page
python3 .opencode/skills/validate-templates/validate-templates.py src/topic-travel.md

# Validate a specific post
python3 .opencode/skills/validate-templates/validate-templates.py src/_posts/2026-04-25-my-post.md

# Auto-fix layout mismatches
python3 .opencode/skills/validate-templates/validate-templates.py src/_posts/ --apply
```

### What It Checks

**For Posts:**
- Frontmatter with `layout`, `title`, `date`, `categories`
- Related posts Liquid block (`where_exp` with `post.categories contains`)
- `limit: 2` set in the loop
- Dynamic topic page link (`p.categories contains`)
- Content exists before Liquid blocks

**For Pages:**
- Frontmatter with `layout`, `title`, `permalink`, `categories`
- Post listing Liquid block (`where: "categories", page.categories`)
- Content exists before Liquid blocks
