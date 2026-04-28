---
layout: music
title: "Your Music Post Title"
date: YYYY-MM-DD HH:MM:SS +0800
categories: music
type: post
author: "Your Name"
---

Review an album, share new music discoveries, or discuss the industry.

![Album Art](/assets/images/img.jpg)

## Section Heading

Your content here...

> "A quote about music."

## Key Points

- Point one
- Point two
- Point three

![Studio](/assets/images/thumb.png)

## Conclusion

Wrap up your thoughts here.

{% capture category %}{{ page.categories | first }}{% endcapture %}
{% assign filtered_posts = site.posts | where_exp: "post", "post.url != page.url" | where_exp: "post", "post.categories contains category" %}
<div class="related-posts">
  <h3>More Music Reviews</h3>
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
