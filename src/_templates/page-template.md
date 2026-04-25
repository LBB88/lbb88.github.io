# Page Template

This template creates a new topic/category page that automatically lists all
posts sharing the same category as defined in the page's frontmatter.

## Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `layout` | Yes | Must be `page` for standalone pages |
| `title` | Yes | The page title (displayed in navigation and heading) |
| `permalink` | Yes | The URL path for this page (e.g., `/my-topic-1/`) |
| `categories` | Yes | Single category string matching posts you want to list |

## File Naming Convention

Pages can be named anything but should be descriptive:
```
topic1.md
```

## Template

```markdown
---
layout: page
title: "Your Topic Name"
permalink: /your-topic-path/
categories: topic1
---

Your page content here. This appears above the post listing.

{% assign filtered_posts = site.posts | where: "categories", page.categories %}

<ul>
  {% for post in filtered_posts %}
    <li><a href="{{ post.url }}">{{ post.title }}</a></li>
  {% endfor %}
</ul>
```

## How It Works

1. **Page frontmatter**: Defines the category this page represents
2. **Filter posts**: Uses `where` filter to find all posts with matching category
3. **List all posts**: Displays all matching posts as a linked list
4. **Bidirectional linking**: Posts using the post template will automatically link back to this page

## Usage Example

1. Copy this template
2. Save as `topic1.md` (or your desired topic name)
3. Update `title`, `permalink`, and `categories` fields
4. Add your content above the Liquid code block
5. Keep the Liquid code block at the bottom of the file

## Connecting Pages and Posts

For the dynamic linking to work:

1. **Page `categories`** must match **Post `categories`**
2. Only one page should use a given category (the first match is used for back links)
3. Posts can only belong to one category in this simplified setup

## Example Setup

| File | Type | Categories | Permalink |
|------|------|------------|-----------|
| `topic1.md` | Page | `topic1` | `/my-topic-1/` |
| `topic2.md` | Page | `topic2` | `/my-topic-2/` |
| `_posts/2026-04-25-post.md` | Post | `topic1` | (auto) |

When viewing the post, it will:
- Show 2 recent posts also in `topic1`
- Link back to `topic1.md` with title "Topic 1 Page"
