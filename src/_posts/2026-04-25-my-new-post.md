---
layout: post
title: "My New Post 1 -topic3"
date: 2026-04-23 10:00:00 +0800
categories: topic3
author: "LBB88"
published: false
type: post
---

Your post content goes here. You can use **Markdown** formatting.

![My Photo](/assets/images/img.jpg)



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