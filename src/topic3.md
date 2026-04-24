---
layout: page
title: "Topic 3 Page"
permalink: /my-topic-3/
categories: topic3
---

{% assign filtered_posts = site.posts | where: "category", page.category_name %}

<ul>
  {% for post in filtered_posts %}
    <li><a href="{{ post.url }}">{{ post.title }}</a></li>
  {% endfor %}
</ul>
