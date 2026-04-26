---
layout: page
title: "Ageing"
permalink: /ageing/
categories: ageing
card_image: /assets/images/thumb5.jpeg
published: true
---

Welcome to our ageing blog! Celebrating wisdom, wellness, and the beauty of growing older.

![Ageing Banner](/assets/images/img.jpg)

## Explore Ageing Posts

{% assign filtered_posts = site.posts | where: "categories", page.categories %}

<ul>
  {% for post in filtered_posts %}
    <li><a href="{{ post.url }}">{{ post.title }}</a> — {{ post.date | date: "%b %-d, %Y" }}</li>
  {% endfor %}
</ul>

[← Back to all topics](/)
