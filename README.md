# lbb88.github.io

Personal website hosted on GitHub Pages.

## Live Site

**URL:** https://lbb88.github.io

## Setup

No build required. This is a static site deployed via GitHub Pages.

## Deployment

Push to the `main` branch to trigger automatic deployment via GitHub Actions.

## Enabling GitHub Pages

1. Go to your repository **Settings**.
2. Navigate to **Pages** in the sidebar.
3. Under **Build and deployment**, select **GitHub Actions** as the source.
4. The site will deploy automatically on the next push to `main`.

## Adding Content

### Adding Blog Posts

Create a new file in the `_posts/` directory with this naming format:

```
YEAR-MONTH-DAY-title.md
```

Example: `2026-04-25-my-new-post.md`

**Important rules:**
- The date in the filename must be **today or in the past**. Future dates won't appear.
- Use `.md` extension (not `.markdown`).
- The file must include **front matter** at the very top.

```markdown
---
layout: post
title: "My New Post"
date: 2026-04-25 10:00:00 +0800
categories: blog update
---

Your post content goes here. You can use **Markdown** formatting.
```

- `layout: post` — required, uses the blog post layout
- `title` — the title displayed on the site
- `date` — publication date (must be today or past, used for sorting)
- `categories` — optional, comma-separated list

After adding the file, commit and push to `main`. The site will rebuild automatically.

### Adding Pages

Create a new `.md` file in the root directory:

```markdown
---
layout: page
title: "My Page"
permalink: /my-page/
---

Write your actual content here. Don't leave it empty or with just placeholder text.
```

**Important rules:**
- Use `.md` extension (not `.markdown`).
- The file must include **front matter** at the very top.
- Write actual content after the front matter. Empty or placeholder-only pages may not render properly.

- `layout: page` — required, uses the page layout
- `title` — displayed in the navigation
- `permalink` — the URL path (e.g., `/my-page/`)

The page will appear in the site navigation automatically.

### Local Preview (Optional)

To preview changes before pushing:

```bash
bundle exec jekyll serve
```

Then visit `http://localhost:4000` in your browser.

**Troubleshooting:**

- **New post not showing?** Check that the date is today or in the past, not a future date.
- **New page is blank?** Make sure you wrote actual content after the front matter (`---`).
- **Changes not appearing?** It can take 1-2 minutes after push for the site to rebuild and deploy.
