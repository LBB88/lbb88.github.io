---
layout: page
title: "Your Topic Name"
permalink: /your-topic-path/
categories: topic1
card_image: /assets/images/your-image.jpg
type: page
published: true
---

Your page content here. This appears above the post listing.

{% assign filtered_posts = site.posts | where: "categories", page.categories %}

<ul>
  {% for post in filtered_posts %}
    <li><a href="{{ post.url }}">{{ post.title }}</a> — {{ post.date | date: "%b %-d, %Y" }}</li>
  {% endfor %}
</ul>

[← Back to all topics](/)
