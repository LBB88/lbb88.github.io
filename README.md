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

### Adding Images

#### External Images (from URL)

Use standard Markdown syntax:

```markdown
![Alt text](https://example.com/image.jpg)
```

Or with a title:

```markdown
![Alt text](https://example.com/image.jpg "Image title")
```

#### Local Images

1. Create an `assets/images/` directory if it doesn't exist:
   ```bash
   mkdir -p assets/images
   ```

2. Add your image file to `assets/images/`:
   ```bash
   cp my-photo.jpg assets/images/
   ```

3. Reference it in your post or page:
   ```markdown
   ![My Photo](/assets/images/my-photo.jpg)
   ```

**Important:**
- Supported formats: `.jpg`, `.jpeg`, `.png`, `.gif`, `.svg`, `.webp`
- Keep images under 1MB for faster loading
- Use descriptive alt text for accessibility

### Adding Videos

#### YouTube Videos

Use an HTML embed (Markdown supports HTML):

```html
<iframe width="560" height="315" src="https://www.youtube.com/embed/VIDEO_ID" frameborder="0" allowfullscreen></iframe>
```

Replace `VIDEO_ID` with the actual YouTube video ID (the part after `v=` in the URL).

#### External Video Files

```markdown
[Download video](https://example.com/video.mp4)
```

Or embed directly:

```html
<video width="640" height="360" controls>
  <source src="/assets/videos/my-video.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>
```

Store local videos in `assets/videos/` similar to images.

**Troubleshooting:**

- **New post not showing?** Check that the date is today or in the past, not a future date.
- **New page is blank?** Make sure you wrote actual content after the front matter (`---`).
- **Changes not appearing?** It can take 1-2 minutes after push for the site to rebuild and deploy.
- **Images not loading?** Verify the path is correct. For local images, make sure they're committed and pushed to `main`.
- **Videos not playing?** Check that the video URL is accessible and the embed code is correct.
