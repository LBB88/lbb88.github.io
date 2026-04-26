---
layout: page
title: "Retirement"
permalink: /retirement/
categories: retirement
card_image: /assets/images/thumb7.jpeg
---

Welcome to our retirement blog! Find inspiration, tips, and stories for living your best retired life.

![Retirement Banner](/assets/images/img.jpg)

## Explore Retirement Posts

{% assign filtered_posts = site.posts | where: "categories", page.categories %}

<ul>
  {% for post in filtered_posts %}
    <li><a href="{{ post.url }}">{{ post.title }}</a> — {{ post.date | date: "%b %-d, %Y" }}</li>
  {% endfor %}
</ul>

[← Back to all topics](/)
