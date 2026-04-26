---
layout: page
title: "Music"
permalink: /music/
categories: music
card_image: /assets/images/thumb.png
published: true
---

Welcome to our music blog! Discover new releases, reviews, and stories from the world of music.

![Music Banner](/assets/images/img.jpg)

## Explore Music Posts

{% assign filtered_posts = site.posts | where: "categories", page.categories %}

<ul>
  {% for post in filtered_posts %}
    <li><a href="{{ post.url }}">{{ post.title }}</a> — {{ post.date | date: "%b %-d, %Y" }}</li>
  {% endfor %}
</ul>

[← Back to all topics](/)
