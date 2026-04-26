---
layout: page
title: "Topic 2 Page"
permalink: /my-topic-2/
categories: topic2
card_image: /assets/images/thumb3.jpeg
published: true
---

## Ways to Embed Videos

This page demonstrates different methods for displaying videos on your Jekyll site using only the Minima theme.

### 1. Simple URL Link

The simplest way to share a video is with a direct link.

[Watch the video](/assets/videos/media.mp4)

**Code:**

```markdown
[Watch the video](/assets/videos/media.mp4)
```

### 2. Video Thumbnail with Link

You can use a thumbnail image that links to the video. To size the thumbnail, add a Kramdown attribute block after the image syntax using `{: width="..."}` or `{: height="..."}` or both.

[![Video Thumbnail](/assets/images/thumb3.jpeg)](/assets/videos/animate.mp4)

[![Video Thumbnail](/assets/images/thumb9.jpeg){: width="100px"}](/assets/videos/media.mp4)

**Code:**

```markdown
[![Video Thumbnail](/assets/images/thumb3.jpeg)](/assets/videos/animate.mp4)

[![Video Thumbnail](/assets/images/thumb9.jpeg){: width="100px"}](/assets/videos/media.mp4)
```

### 3. Inline Video Player

For videos hosted on your site, use the HTML5 `<video>` element to embed a player directly.

<video width="100%" controls>
  <source src="/assets/videos/media.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

**Code:**

```html
<video width="100%" controls>
  <source src="/assets/videos/media.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>
```

### 4. YouTube Embed via Liquid Include

For YouTube videos, create a reusable include for a responsive iframe embed.

{% include youtube.html id="dQw4w9WgXcQ" %}

**Include file (`_includes/youtube.html`):**

{% raw %}
```html
<div class="video-container">
  <iframe src="https://www.youtube.com/embed/{{ include.id }}" frameborder="0" allowfullscreen></iframe>
</div>
```
{% endraw %}

**Usage in your page:**

{% raw %}
```liquid
{% include youtube.html id="dQw4w9WgXcQ" %}
```
{% endraw %}

---

## Related Posts

{% assign filtered_posts = site.posts | where: "categories", page.categories %}

<ul>
  {% for post in filtered_posts %}
    <li><a href="{{ post.url }}">{{ post.title }}</a> — {{ post.date | date: "%b %-d, %Y" }}</li>
  {% endfor %}
</ul>

[← Back to all topics](/)
