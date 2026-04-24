---
layout: page
title: "Topic 2 Page"
permalink: /my-topic-2/
categories: topic2
---

[Watch the video](/assets/videos/media.mp4)

[![Video Thumbnail](/assets/images/thumb.png)](/assets/videos/animate.mp4)

[![Video Thumbnail](/assets/images/thumb.png)](/assets/videos/media.mp4){: width="200px"}


{% assign filtered_posts = site.posts | where: "category", page.category_name %}

<ul>
  {% for post in filtered_posts %}
    <li><a href="{{ post.url }}">{{ post.title }}</a></li>
  {% endfor %}
</ul>
