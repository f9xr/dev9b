---
title: "Useful Shortcodes for Dev9b Articles"
description: "Embed videos, quotes, and other media in your Dev9b articles using Hugo shortcodes. A practical guide with examples."
date: 2024-01-25
image: cover.jpg
tags:
    - shortcodes
    - writing
    - tutorial
    - dev9b
categories:
    - Tutorials
---

Dev9b supports Hugo shortcodes for embedding media and special content. Here are the most useful ones for your articles.

For more details, check out the [Hugo Theme Stack documentation](https://stack.jimmycai.com/writing/shortcodes).

## YouTube Video

Embed YouTube videos with the `youtube` shortcode:

```markdown
{{</* youtube "VIDEO_ID" */>}}
```

## Generic Video File

Embed video files directly:

```markdown
{{</* video "https://example.com/video.mp4" */>}}
```

## Quote

Create styled quotes:

```markdown
{{</* quote author="Author Name" source="Book or Article" url="https://example.com">}}
Your quote content here.
{{</* /quote */>}}
```

## Writing Tips for Dev9b

When writing articles for Dev9b:

- Use **shortcodes** to embed rich media
- Keep videos relevant to the article topic
- Add **alt text** to images for accessibility
- Use **code blocks** with language identifiers

> Check the [Contributor Guide](/contribute) to submit your article.

---

> Photo by [Codioful](https://unsplash.com/@codioful) on [Unsplash](https://unsplash.com/photos/WDSN62Qdxuk)
