# lbb88.github.io

Personal website hosted on GitHub Pages.

## Live Site

**URL:** https://lbb88.github.io

## Setup

This is a Jekyll site deployed via GitHub Pages.

## Agents & Skills

This project uses an AI orchestration system (Sisyphus) with specialized sub-agents and reusable skills.

### Available Agents

| Agent | Role |
|-------|------|
| **Sisyphus** | Orchestrator — plans, delegates, verifies |
| **Sisyphus-Junior** | Task executor — implements changes |
| **Oracle** | High-IQ consultant — architecture, debugging |
| **Explore** | Contextual grep — finds patterns in the codebase |
| **Librarian** | External reference — docs, OSS examples |
| **Metis** | Pre-planning consultant — clarifies ambiguous requests |
| **Momus** | Plan reviewer — checks work plan quality |

### Available Skills

Skills provide specialized workflows for specific tasks:

| Skill | When to Use |
|-------|-------------|
| `commit-push` | Commit and push changes, update site |
| `validate-new-pages` | Validate newly added pages and posts (recommended) |
| `validate-templates` | Validate specific files or directories (manual) |
| `code-warden` | Initialize code-warden snapshot tracking |
| `github-pages-website` | Scaffold a new GitHub Pages site |
| `skill-creator` | Create or edit skills |
| `frontend-ui-ux` | UI/UX design and implementation |
| `git-master` | Git operations: commits, rebases, history |

### Using Skills

Load a skill when starting a task that matches its description:

```
# In conversation, invoke a skill:
/commit-push         → commits and pushes changes
/validate-new-pages  → validates all pages and posts
/validate-templates  → validates specific files or directories
/skill-creator       → creates new skills
```

### Creating Skills

1. Use the `/skill-creator` skill
2. Define: name, description, trigger phrases, instructions
3. Skills are stored in `.opencode/skills/` or `~/.config/opencode/skills/`

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

### Topic Pages (Category Landing Pages)

Topic pages serve as landing pages for each category/agent. They list all posts in that category and link back to the home page.

**Recommended frontmatter fields:**

| Field | Required | Description |
|-------|----------|-------------|
| `layout` | Yes | Must be `page` |
| `title` | Yes | Page title (shown in navigation) |
| `permalink` | Yes | URL path (e.g., `/travel/`) |
| `categories` | Yes | Category matching posts to list |
| `card_image` | Recommended | Background image for home page topic card |

**Example frontmatter:**

```markdown
---
layout: page
title: "Travel"
permalink: /travel/
categories: travel
card_image: /assets/images/img.jpg
---
```

**Full template (saved in `_templates/travel-template.md`):**

```markdown
---
layout: page
title: "Travel"
permalink: /travel/
categories: travel
card_image: /assets/images/img.jpg
---

Welcome to our travel blog! Discover destinations, tips, and stories from around the world.

![Travel Banner](/assets/images/img.jpg)

## Explore Travel Posts

{% assign filtered_posts = site.posts | where: "categories", page.categories %}

<ul>
  {% for post in filtered_posts %}
    <li><a href="{{ post.url }}">{{ post.title }}</a> — {{ post.date | date: "%b %-d, %Y" }}</li>
  {% endfor %}
</ul>

[← Back to all topics](/)
```

**Pre-built topic templates** (use as starting point):

| Template | File |
|----------|------|
| Ageing | `_templates/ageing-template.md` |
| Music | `_templates/music-template.md` |
| Product | `_templates/product-template.md` |
| Retirement | `_templates/retirement-template.md` |
| Travel | `_templates/travel-template.md` |

### Dynamic Card Background Images

Topic cards on the home page display a background image. The image is set via the `card_image` frontmatter field in each topic page.

**To change a card's background:**
1. Open the topic page (e.g., `src/topic-travel.md`)
2. Update the `card_image` value in frontmatter
3. Commit and push — the home page card updates automatically

**Image recommendations:**
- Use images at least 400px wide
- Keep file size under 500KB for fast loading
- Place images in `src/assets/images/`
- Reference with path relative to site root (e.g., `/assets/images/my-image.jpg`)

**How it works:**
The home page layout (`_layouts/home.html`) reads `topic.card_image` for each topic page and applies it as an inline `style="background-image: url('...')"` on the card element. A dark overlay is applied automatically for text readability.

### Video Embedding Guide

For full video embedding examples with code, see [`topic2.md`](/my-topic-2/) on the live site. Four methods are demonstrated:

#### 1. Simple URL Link

```markdown
[Watch the video](/assets/videos/media.mp4)
```

#### 2. Thumbnail Image Linking to Video

```markdown
[![Video Thumbnail](/assets/images/thumb.png)](/assets/videos/animate.mp4)
```

With size control using Kramdown attributes:

```markdown
[![Video Thumbnail](/assets/images/thumb.png)](/assets/videos/media.mp4){: width="200px"}
```

#### 3. HTML5 Inline Video Player

```html
<video width="100%" controls>
  <source src="/assets/videos/media.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>
```

#### 4. YouTube Embed via Liquid Include

Create `_includes/youtube.html`:
```html
<div class="video-container">
  <iframe src="https://www.youtube.com/embed/{{ include.id }}" frameborder="0" allowfullscreen></iframe>
</div>
```

Use in any page:
```liquid
{% include youtube.html id="dQw4w9WgXcQ" %}
```

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

Two validation skills are available to check that your markdown files contain all required sections.

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
