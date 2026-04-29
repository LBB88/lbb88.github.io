> ⚠️ LIVING DOCUMENT — MANDATORY UPDATE POLICY
> This file must be updated before any task is considered complete.
> Whenever you make a change that affects any workflow, logic flow,
> dependency, or module interface, update the relevant section of this
> file first. Do not mark a task done until this file reflects the
> current state of the codebase.

# Code Warden — Codebase Snapshot

## 1. Project Overview

**Project:** `lbb88.github.io` — Personal blog/website hosted on GitHub Pages.

**Core Purpose:** A Jekyll-powered static site (using Minima theme) that publishes blog posts across themed categories. Features include:
- Landing page with hero banner, topic cards, and latest posts
- Category-specific topic pages listing related posts
- Blog posts with category-matched visual themes and related-post navigation
- Media embedding support (images, videos, YouTube)

**Live URL:** https://lbb88.github.io

---

## 2. Architecture

```
src/                                  # ALL Jekyll source files
├── _config.yml                       # Jekyll configuration (theme, plugins, social usernames)
├── Gemfile                           # Ruby dependencies (minima, github-pages, jekyll-feed)
├── 404.html                          # 404 error page
├── about.md                          # About page
├── index.md                          # Home/landing page (layout: home)
├── topic-*.md                        # 5 themed topic pages (travel, retirement, ageing, music, product)
├── topic1.md, topic2.md, topic3.md   # 3 generic topic pages
├── _includes/                        # Liquid includes
│   ├── social.html                   # Social media links (reads site.twitter_username etc.)
│   └── youtube.html                  # YouTube embed iframe ({{ include.id }})
├── _layouts/                         # HTML layout templates
│   ├── home.html                     # Landing page (layout: default)
│   ├── ageing.html                   # Category post layout (layout: default + .related-posts CSS)
│   ├── music.html                    # Category post layout (identical structure, different CSS colors)
│   ├── product.html                  # Category post layout
│   ├── retirement.html               # Category post layout
│   └── travel.html                   # Category post layout
├── _posts/                           # 13 blog posts
├── _templates/                       # 7 content templates
│   ├── post-template.md             # For creating new posts (type: post)
│   ├── page-template.md             # For creating topic pages (type: page)
│   ├── ageing-template.md           # Category post template (type: post)
│   ├── music-template.md            # Category post template (type: post)
│   ├── product-template.md          # Category post template (type: post)
│   ├── retirement-template.md       # Category post template (type: post)
│   └── travel-template.md           # Category post template (type: post)
├── assets/
│   ├── images/                       # Image files
│   ├── videos/                       # Video files
│   └── main.scss                     # Custom Sass overrides
├── _site/                            # Jekyll build output (generated, not committed)
.github/workflows/jekyll.yml           # GitHub Actions deployment workflow
.opencode/skills/                     # Validation and utility skills
```

**Main Entry Points:**
- Content: `src/index.md`, `src/topic-*.md`, `src/_posts/*.md`
- Config: `src/_config.yml`
- Build: `bundle exec jekyll build` (from `src/`)

---

## 3. Critical Dependencies

### Category ↔ Layout Mapping

Must stay synchronized in `validate-templates.py` AND `fix-frontmatter.py`:

| Category | Required Layout |
|----------|-----------------|
| travel | travel |
| retirement | retirement |
| ageing | ageing |
| music | music |
| product | product |
| topic1 | post |
| topic2 | post |
| topic3 | post |

**Breakage:** Posts with mismatched layout will use generic `post` layout instead of themed layout.

### Topic Page ↔ Post Bidirectional Linking

**Topic pages use:**
```liquid
{% assign filtered_posts = site.posts | where: "categories", page.categories %}
```

**Posts use:**
```liquid
{% capture category %}{{ page.categories | first }}{% endcapture %}
{% assign topic_page = site.pages | where_exp: "p", "p.categories contains category" | first %}
```

**Breakage:** If `categories` is removed from either side, bidirectional linking breaks.

### Social Links (`_includes/social.html`)

Reads from `_config.yml`:
- `site.twitter_username`
- `site.facebook_username`
- `site.tiktok_username`
- `site.github_username`

**Breakage:** Social links won't render if these config keys are missing.

---

## 4. Logic Workflows

### Local Development Build

```bash
cd src
bundle exec jekyll serve
# → reads _config.yml, _layouts/, _includes/, _posts/, *.md
# → outputs to src/_site/
# → serves at http://localhost:4000
```

### Production Build & Deployment

1. Push to `main` branch → triggers `.github/workflows/jekyll.yml`
2. GitHub Actions: checks out repo, sets up Ruby 3.1, runs `bundle install`
3. Builds: `bundle exec jekyll build --destination ../_site --baseurl "${{ steps.pages.outputs.base_path }}"`
4. Uploads `_site/` as Pages artifact
5. Deploys to GitHub Pages

**Critical:** Working directory is `src/`, output goes to repo root `_site/`

### Media Import Workflow

1. Drop media + `content.md` into `import/pages/YYYYMMDD_slug/` or `import/_posts/YYYYMMDD_slug/`
2. Run `validate-new-pages.py --import`
3. Media moved to `src/assets/images/` or `src/assets/videos/`
4. Markdown moved to `src/topic-{slug}.md` (pages) or `src/_posts/YYYY-MM-DD-{slug}.md` (posts)
5. Media references embedded in markdown body
6. Source folder backed up to `bkup-import/` then deleted

---

## 5. Refactoring Constraints

### Jekyll Frontmatter Contracts

**Home page (`src/index.md`) — keys read by `_layouts/home.html`:**
- `page.hero_title`, `page.hero_description`, `page.hero_image`, `page.hero_image_alt`, `page.topics_title`, `page.posts_title`

**Topic pages — required frontmatter:**
```yaml
layout: page
title: "..."
permalink: /.../
categories: ...
card_image: /assets/images/...
published: true
type: page
```

**Posts — required frontmatter:**
```yaml
layout: {category-mapped}
title: "..."
date: YYYY-MM-DD HH:MM:SS +0800
categories: ...
author: LBB88
published: true
type: post
```

**Template files (except page-template.md) — required frontmatter:**
```yaml
layout: {category}
title: "..."
date: YYYY-MM-DD HH:MM:SS +0800
categories: ...
author: LBB88
published: true
type: post
```

### Liquid Include Signature

**`src/_includes/youtube.html`:**
```html
<iframe src="https://www.youtube.com/embed/{{ include.id }}" ...>
```
Used as: `{% include youtube.html id="VIDEO_ID" %}`

### Validation Script CLI

```bash
python validate-templates.py <path> [--apply] [--pages] [--posts]
python validate-new-pages.py [--pages] [--posts] [--apply] [--import] [--templates]
```

---

## 6. Testing Requirements

### Validation Scripts

**`validate-templates.py`** (`.opencode/skills/validate-templates/validate-templates.py`)
- Validates individual files/directories for frontmatter + Liquid blocks
- Checks: `layout`, `title`, `categories`, `author` (posts), `date` (posts), `permalink` (pages), `published` (posts), `type`, `where_exp` related posts, `limit: 2`, `where: "categories"`, content before Liquid
- `--apply` corrects post layouts (NOT page layouts)

**`validate-new-pages.py`** (`.opencode/skills/validate-new-pages/validate-new-pages.py`)
- Wrapper: discovers all `.md` in `src/`, runs `validate-templates.py` on each
- Exclusions: `_site/`, `.opencode/`, `about.md`, `index.md`, `README.md`
- Template files (`_templates/`, excluding `page-template.md`) are auto-processed for missing frontmatter before validation
- Interactive frontmatter fixing via `fix-frontmatter.py`
- Media import + backup/cleanup
- `--templates` flag validates template files only

**`fix-frontmatter.py`** (`.opencode/skills/validate-new-pages/fix-frontmatter.py`)
- Key functions: `has_frontmatter_issues()`, `generate_fix_proposal()`, `apply_fix()`, `fix_template_files()`
- Checks posts for missing: `layout`, `title`, `date`, `categories`, `author`, `published`, `type`
- Provides interactive prompts for missing template frontmatter fields

### Must Pass Commands

```bash
# Validate all
python3 .opencode/skills/validate-new-pages/validate-new-pages.py

# With auto-fix
python3 .opencode/skills/validate-new-pages/validate-new-pages.py --apply
```

---

## 7. Public-Facing Interfaces

### Jekyll CLI

```bash
# Local preview
cd src && bundle exec jekyll serve

# Production build
cd src && bundle exec jekyll build
```

### GitHub Actions (`.github/workflows/jekyll.yml`)

**Triggers:** `push` to `main`, `workflow_dispatch`

**Build:** Ruby 3.1, `bundle exec jekyll build --destination ../_site`

**Deploy:** GitHub Pages artifact deployment

### Validation Commands

```bash
# Validate all
python3 .opencode/skills/validate-new-pages/validate-new-pages.py

# Pages only
python3 .opencode/skills/validate-new-pages/validate-new-pages.py --pages

# Posts only
python3 .opencode/skills/validate-new-pages/validate-new-pages.py --posts

# Auto-fix layouts
python3 .opencode/skills/validate-new-pages/validate-new-pages.py --apply

# Import + validate
python3 .opencode/skills/validate-new-pages/validate-new-pages.py --import

# Validate templates only
python3 .opencode/skills/validate-new-pages/validate-new-pages.py --templates
```

---

## 8. Setup and Installation

### Ruby Dependencies (`src/Gemfile`)

```ruby
source "https://rubygems.org"
gem "minima", "~> 2.5"
gem "github-pages", "~> 232", group: :jekyll_plugins
group :jekyll_plugins do
  gem "jekyll-feed", "~> 0.12"
end
```

**Install:** `cd src && bundle install`

### Jekyll Config (`src/_config.yml`)

```yaml
title: LBB88 Studio
email: tbd@test.com
url: "https://lbb88.github.io"
twitter_username: bigfishlbb
facebook_username: bigfishlbb
tiktok_username: bigfishlbb
github_username: lbb88
repository: LBB88/lbb88.github.io
theme: minima
plugins:
  - jekyll-feed
```

### GitHub Pages Setup

1. Settings → Pages → Build and deployment → Source: GitHub Actions
2. Push to `main` triggers deployment

---

## 9. README.md vs. Actual Codebase

**README inaccuracies noted:**
- README says `about.markdown` and `index.markdown` — actual files are `about.md` and `index.md`
- README examples show `.markdown` extension — actual files use `.md`
- README project structure omits `topic1.md`, `topic2.md`, `topic3.md`, `404.html`
