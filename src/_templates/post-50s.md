---
layout: post-50s
title: Your 50s-Inspired Post Title
date: YYYY-MM-DD HH:MM:SS +0800
categories: 50s
type: post
author: Your Name
published: true
---

Share stories, reflections, or nostalgic content with a calm and peaceful tone.

![Placeholder Image](/assets/images/img.jpg)

## Section Heading

Your content here. Write in a serene, contemplative style that evokes the gentle pace of earlier times.

> "A quote that captures the spirit of the era."

## Key Points

- A gentle reflection point
- A nostalgic memory
- A calm observation

![Additional Image](/assets/images/thumb.png)

## Closing Thoughts

Wrap up with a peaceful conclusion.

{% capture category %}{{ page.categories | first }}{% endcapture %}
{% assign filtered_posts = site.posts | where_exp: "post", "post.url != page.url" | where_exp: "post", "post.categories contains category" %}
<div class="related-posts">
  <h3>More Reflections</h3>
  <ul>
  {% for post in filtered_posts limit: 2 %}
    <li><a href="{{ post.url }}">{{ post.title }}</a></li>
  {% endfor %}
  </ul>
  {% assign topic_page = site.pages | where_exp: "p", "p.categories contains category" | first %}
  {% if topic_page %}
    <a href="{{ topic_page.url }}" class="category-link">Explore all {{ topic_page.title }} posts →</a>
  {% endif %}
</div>