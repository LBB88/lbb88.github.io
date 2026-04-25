---
layout: post
title: "My New Post 1"
date: 2026-04-23 10:00:00 +0800
categories: topic3
---

Your post content goes here. You can use **Markdown** formatting.

![My Photo](/assets/images/img.jpg)



{% assign filtered_posts = site.posts | where_exp: "post", "post.url != page.url" | where: "categories", page.categories | limit: 2 %}
<ul>
{% for post in filtered_posts %}
  <li><a href="{{ post.url }}">{{ post.title }}</a></li>
{% endfor %}
</ul>

Check out more in the [topic category](/my-topic-{{ page.categories[0] | replace: "topic", "" }}/).