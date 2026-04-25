# lbb88.github.io

Personal website hosted on GitHub Pages.

## Live Site

**URL:** https://lbb88.github.io

## Setup

This is a Jekyll site deployed via GitHub Pages.

## Project Structure

All Jekyll source files are in the `src/` directory:

```
src/
├── _config.yml          # Jekyll configuration
├── _posts/              # Blog posts
├── assets/              # Static assets
│   ├── images/          # Image files
│   └── videos/          # Video files
├── 404.html             # 404 error page
├── about.markdown       # About page
├── index.markdown       # Home page
└── ...                  # Other pages
```

## Deployment

Push to the `main` branch to trigger automatic deployment via GitHub Actions.

## Commit and Push Changes

After making changes to your content, commit and push them to the `main` branch:

```bash
# Stage all changes
git add -A

# Commit with a descriptive message
git commit -m "feat(content): add new blog post about..."

# Push to main branch
git push origin main
```

**Tip:** Use conventional commit messages like `feat(content):`, `fix(content):`, or `chore(config):` to keep the history clean.

## Enabling GitHub Pages

1. Go to your repository **Settings**.
2. Navigate to **Pages** in the sidebar.
3. Under **Build and deployment**, select **GitHub Actions** as the source.
4. The site will deploy automatically on the next push to `main`.

## Adding Content

### Adding Blog Posts

Create a new file in `src/_posts/` with this naming format:

```
YEAR-MONTH-DAY-title.md
```

Example: `src/_posts/2026-04-25-my-new-post.md`

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

Create a new `.md` file in `src/`:

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

### Customizing the Landing Page

The landing page (home page) is controlled by `src/index.md`. Edit the **front matter** values to change what appears on the home page:

```markdown
---
layout: home
hero_title: "Welcome to My Blog"
hero_description: "Exploring topics and sharing knowledge through posts and articles."
hero_image: /assets/images/img.jpg
hero_image_alt: "Blog header image"
topics_title: "Browse by Topic"
posts_title: "Latest Posts"
---
```

**Front matter fields:**

| Field | Description |
|-------|-------------|
| `layout` | Must be `home` |
| `hero_title` | Main heading displayed in the hero banner |
| `hero_description` | Subtitle text below the hero heading |
| `hero_image` | Path to the hero image (place image in `src/assets/images/`) |
| `hero_image_alt` | Alt text for the hero image (accessibility) |
| `topics_title` | Heading for the topics/categories section |
| `posts_title` | Heading for the latest posts section |

**To update the hero image:**
1. Add your image to `src/assets/images/`
2. Update `hero_image` in `src/index.md` to point to the new file (e.g., `/assets/images/my-hero.jpg`)
3. Update `hero_image_alt` with a descriptive alt text

**To update text content:**
Simply edit the values in the front matter of `src/index.md`.

After making changes, commit and push to `main` to see them live.

### Adding Images to Posts and Pages

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

1. Add your image file to `src/assets/images/`:
   ```bash
   cp my-photo.jpg src/assets/images/
   ```

2. Reference it in your post or page:
   ```markdown
   ![My Photo](/assets/images/my-photo.jpg)
   ```

**Important:**
- Supported formats: `.jpg`, `.jpeg`, `.png`, `.gif`, `.svg`, `.webp`
- Keep images under 1MB for faster loading
- Use descriptive alt text for accessibility

#### Modifying Existing Posts/Pages to Add Images

Open the existing `.md` file in `src/_posts/` or `src/` and add the image reference in the content:

```markdown
---
layout: post
title: "My Existing Post"
date: 2026-04-25 10:00:00 +0800
---

Here's my original content.

![New Image](/assets/images/new-photo.jpg)

More content here...
```

### Adding Videos to Posts and Pages

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

#### Local Videos

1. Add your video file to `src/assets/videos/`:
   ```bash
   cp my-video.mp4 src/assets/videos/
   ```

2. Reference it in your post or page using the HTML embed above.

#### Modifying Existing Posts/Pages to Add Videos

Open the existing `.md` file and add the video embed in the content:

```markdown
---
layout: post
title: "My Existing Post"
date: 2026-04-25 10:00:00 +0800
---

Here's my original content.

<video width="640" height="360" controls>
  <source src="/assets/videos/new-video.mp4" type="video/mp4">
</video>

More content here...
```

### Local Preview (Optional)

To preview changes before pushing:

```bash
cd src
bundle exec jekyll serve
```

Then visit `http://localhost:4000` in your browser.

**Troubleshooting:**

- **New post not showing?** Check that the date is today or in the past, not a future date.
- **New page is blank?** Make sure you wrote actual content after the front matter (`---`).
- **Changes not appearing?** It can take 1-2 minutes after push for the site to rebuild and deploy.
- **Images not loading?** Verify the path is correct. For local images, make sure they're in `src/assets/images/` and pushed to `main`.
- **Videos not playing?** Check that the video URL is accessible and the embed code is correct.

## Content Templates

### Post Template

Use this template for new blog posts. It automatically lists 2 related posts from the same category and provides back navigation to the category page.

**Frontmatter Fields:**

| Field | Required | Description |
|-------|----------|-------------|
| `layout` | Yes | Must be `post` |
| `title` | Yes | The post title |
| `date` | Yes | Publication date (YYYY-MM-DD HH:MM:SS +/-HHMM) |
| `categories` | Yes | Single category (e.g., `topic1`) |

**Template:**

```markdown
---
layout: post
title: "Your Post Title"
date: YYYY-MM-DD HH:MM:SS +0800
categories: topic1
---

Your post content here.

{% capture category %}{{ page.categories | first }}{% endcapture %}
{% assign filtered_posts = site.posts | where_exp: "post", "post.url != page.url" | where_exp: "post", "post.categories contains category" %}

<ul>
{% for post in filtered_posts limit: 2 %}
  <li><a href="{{ post.url }}">{{ post.title }}</a></li>
{% endfor %}
</ul>

{% assign topic_page = site.pages | where_exp: "p", "p.categories contains category" | first %}
{% if topic_page %}
Check out more in the [{{ topic_page.title }}]({{ topic_page.url }}).
{% endif %}
```

### Page Template

Use this template for new topic/category pages. It automatically lists all posts sharing the same category.

**Frontmatter Fields:**

| Field | Required | Description |
|-------|----------|-------------|
| `layout` | Yes | Must be `page` |
| `title` | Yes | Page title (shown in navigation) |
| `permalink` | Yes | URL path (e.g., `/my-topic-1/`) |
| `categories` | Yes | Category matching posts to list |

**Template:**

```markdown
---
layout: page
title: "Your Topic Name"
permalink: /your-topic-path/
categories: topic1
---

Your page content here.

{% assign filtered_posts = site.posts | where: "categories", page.categories %}

<ul>
  {% for post in filtered_posts %}
    <li><a href="{{ post.url }}">{{ post.title }}</a></li>
  {% endfor %}
</ul>
```

### How the Templates Work Together

1. **Post** captures its category and finds other posts with the same category
2. **Post** lists up to 2 recent related posts
3. **Post** dynamically finds the matching topic page and links to it
4. **Page** lists all posts sharing its category
5. The connection is made through matching `categories` values in frontmatter

### Validation

When creating new posts or pages, verify they contain:

- [ ] Correct frontmatter (`layout`, `title`, `date`/`permalink`, `categories`)
- [ ] Liquid code block for related posts (posts) or post listing (pages)
- [ ] Dynamic category link (posts only)
- [ ] Content above the Liquid code block

## Activating the Validation Skill

A validation skill is included in this repository to automatically check that your markdown files contain all required sections.

### Manual Validation

Run the validation script directly:

```bash
# Validate all posts
python3 .opencode/skills/validate-templates/validate-templates.py src/_posts/

# Validate all pages
python3 .opencode/skills/validate-templates/validate-templates.py src/topic1.md

# Validate a specific file
python3 .opencode/skills/validate-templates/validate-templates.py src/_posts/2026-04-25-my-post.md
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

### Example Output

```
============================================================
Validating: src/_posts/2026-04-25-my-new-post.md
Type: post
============================================================
  ✓ Frontmatter valid
  ✓ Required fields present
  ✓ Liquid blocks valid
  ✓ Content before Liquid block

============================================================
SUMMARY
============================================================
✓ PASS: src/_posts/2026-04-25-my-new-post.md

Total: 1 | Passed: 1 | Failed: 0
```
