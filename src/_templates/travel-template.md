---
layout: travel
title: Your Travel Post Title
date: YYYY-MM-DD HH:MM:SS +0800
categories: travel
type: post
author: Your Name
published: true
---

Write your travel story here. Describe destinations, experiences, and tips for fellow travelers.

![Travel Photo](/assets/images/img.jpg)

## Section Heading

Your content here...

> "A memorable travel quote."

## Travel Tips

- Tip one
- Tip two
- Tip three

![Another Photo](/assets/images/thumb.png)

## Conclusion

Wrap up your travel story here.

{% capture category %}{{ page.categories | first }}{% endcapture %}
{% assign filtered_posts = site.posts | where_exp: "post", "post.url != page.url" | where_exp: "post", "post.categories contains category" %}
<div class="related-posts">
  <h3>More Travel Stories</h3>
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
