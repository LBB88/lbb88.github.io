---
layout: post
title: "Your Post Title"
date: YYYY-MM-DD HH:MM:SS +0800
categories: topic1
author: "Your Name"
type: post
published: true
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
