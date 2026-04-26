---
layout: page
title: "Product"
permalink: /product/
categories: product
card_image: /assets/images/thumb2.png
published: true
---

Welcome to our product blog! Stay updated on the latest launches, reviews, and innovations.

![Product Banner](/assets/images/img.jpg)

## Explore Product Posts

{% assign filtered_posts = site.posts | where: "categories", page.categories %}

<ul>
  {% for post in filtered_posts %}
    <li><a href="{{ post.url }}">{{ post.title }}</a> — {{ post.date | date: "%b %-d, %Y" }}</li>
  {% endfor %}
</ul>

[← Back to all topics](/)
