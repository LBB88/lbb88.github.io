# Post Template

This template creates a new blog post that automatically lists 2 related posts
from the same category and provides back navigation to the category page.

## Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `layout` | Yes | Must be `post` for blog posts |
| `title` | Yes | The post title |
| `date` | Yes | Publication date (YYYY-MM-DD HH:MM:SS +/-HHMM) |
| `categories` | Yes | Single category string (e.g., `topic1`, `topic2`, `topic3`) |

## File Naming Convention

Posts must follow Jekyll's naming convention:
```
YYYY-MM-DD-your-post-title.md
```

Example: `2026-04-25-my-new-post.md`

## Template

```markdown
---
layout: post
title: "Your Post Title"
date: YYYY-MM-DD HH:MM:SS +0800
categories: topic1
---

Your post content here. You can use **Markdown** formatting.

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

## How It Works

1. **Capture category**: Extracts the first category from the post's frontmatter as a string variable
2. **Filter posts**: Finds other posts with the same category, excluding the current post
3. **List 2 recent posts**: Displays up to 2 related posts in an unordered list
4. **Dynamic back link**: Automatically finds the topic page with matching categories and links to it using the page's actual title and URL

## Usage Example

1. Copy this template
2. Save as `_posts/2026-04-26-your-title.md`
3. Update `title`, `date`, and `categories` fields
4. Add your content above the Liquid code block
5. Keep the Liquid code block at the bottom of the file
