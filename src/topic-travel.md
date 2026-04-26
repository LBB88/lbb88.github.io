---
layout: page
title: "Travel"
permalink: /travel/
categories: travel
card_image: /assets/images/thumb8.jpeg
---

Welcome to our travel blog! Discover destinations, tips, and stories from around the world.

![Travel Banner](/assets/images/img.jpg)

## Explore Travel Posts

{% assign filtered_posts = site.posts | where: "categories", page.categories %}

<ul>
  {% for post in filtered_posts %}
    <li><a href="{{ post.url }}">{{ post.title }}</a> — {{ post.date | date: "%b %-d, %Y" }}</li>
  {% endfor %}
</ul>

[← Back to all topics](/)
