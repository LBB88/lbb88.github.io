---
layout: page
title: "Topic 3 Page"
permalink: /my-topic-3/
categories: topic3
---

{% assign filtered_posts = site.posts | where: "categories, page.category_name %}

<ul>
  {% for post in filtered_posts %}
    <li><a href="{{ post.url }}">{{ post.title }} - {{ post.date }}</a></li>
  {% endfor %}
</ul>
