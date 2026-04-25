---
layout: page
title: "Topic 1 Page"
permalink: /my-topic-1/
categories: topic1
---

![My Photo](/assets/images/img.jpg)

This is my topic 1 page content, which is done using **Markdown** formatting:

# How to Create a GitHub Page using Markdown

This guide covers the most common Markdown formatting used to build a clean, readable GitHub Pages site or `README.md`.

## 1. Headers
Use the `#` symbol to create headings. More `#` symbols mean a smaller heading.

# H1 Header (Main Title)
## H2 Header (Section)
### H3 Header (Sub-section)

## 2. Text Formatting
It is easy to emphasize your words:
- **Bold text** using `**text**`
- *Italic text* using `*text*`
- ~~Strikethrough~~ using `~~text~~`

## 3. Lists
### Ordered List
1. First item
2. Second item
3. Third item

### Unordered List
* Item A
* Item B
  * Nested item (indent with two spaces)

## 4. Links and Images
To link to a website: [Google](https://google.com)
To show an image: `![Alt Text](url-to-image.jpg)`

## 5. Code
For inline code, use backticks: `const x = 10;`.

For code blocks, use triple backticks with the language name for syntax highlighting:

```javascript
function helloWorld() {
  console.log("Hello, GitHub Pages!");
}
```

## 6. Blockquotes
> Use the `>` symbol to create blockquotes for callouts or citations.

## 7. Tables

| Feature | Syntax | Result |
| :--- | :---: | ---: |
| Left Align | `:---` | Text |
| Center | `:---:` | Text |
| Right | `---:` | Text |

## 8. Task Lists
- [x] Create repository
- [ ] Enable GitHub Pages
- [ ] Add content


{% assign filtered_posts = site.posts | where: "categories", page.categories %}

<ul>
  {% for post in filtered_posts %}
    <li><a href="{{ post.url }}">{{ post.title }}</a></li>
  {% endfor %}
</ul>
