---
layout: product
title: "Your Product Post Title"
date: YYYY-MM-DD HH:MM:SS +0800
categories: product
type: post
author: "Your Name"
---

Introduce a new product, review features, or share launch details.

![Product Hero](/assets/images/img.jpg)

## Section Heading

Your content here...

> "A quote about innovation."

## Key Features

| Feature | Specification |
|---------|--------------|
| Feature 1 | Detail 1 |
| Feature 2 | Detail 2 |

![Product Detail](/assets/images/thumb.png)

## Conclusion

Wrap up your thoughts here.

{% capture category %}{{ page.categories | first }}{% endcapture %}
{% assign filtered_posts = site.posts | where_exp: "post", "post.url != page.url" | where_exp: "post", "post.categories contains category" %}
<div class="related-posts">
  <h3>More Product Launches</h3>
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
