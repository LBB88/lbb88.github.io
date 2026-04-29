---
layout: page
title: "Music"
permalink: /music/
categories: music
card_image: /assets/images/logo.jpg
published: true
type: page
---

Welcome to my music blog! Discover new releases and stories from the world of music.

![Music Banner](/assets/images/logo.jpg)

## Explore Music Posts

{% assign filtered_posts = site.posts | where: "categories", page.categories %}

<ul>
  {% for post in filtered_posts %}
    <li><a href="{{ post.url }}">{{ post.title }}</a> — {{ post.date | date: "%b %-d, %Y" }}</li>
  {% endfor %}
</ul>

[← Back to all topics](/)
