---
title: "Image Gallery in Dev9b Articles"
description: "Build interactive PhotoSwipe image galleries in Dev9b articles. Cover the Markdown syntax, bundle rules, alt text, and the performance tips."
slug: image-gallery-in-dev9b-articles
date: 2024-01-28
image: cover.jpg
author: F9XR Team
keywords:
    - dev9b image gallery
    - photoswipe
    - markdown images
    - page bundle images
    - hugo image gallery
    - alt text
    - responsive images
categories:
    - Tutorials
tags:
    - images
    - gallery
    - writing
    - dev9b
draft: false
math: false
faq:
    - question: "How do I create an image gallery in a Dev9b article?"
      answer: "Place the image files in the same directory as your index.md, then reference several of them on one line with standard Markdown, for example ![alt one](1.jpg) ![alt two](2.jpg). Dev9b groups adjacent images into one PhotoSwipe gallery automatically."
    - question: "Can I use images hosted on another website?"
      answer: "No. Gallery images must be local files inside the page bundle. External and hotlinked images are not supported, because they break when the remote host removes or moves the file and they slow the page down."
    - question: "Does every image need alt text?"
      answer: "Yes. Alt text is required for accessibility and it is good for SEO. Write a short description of what the image shows rather than repeating the file name."
    - question: "What image size and format should I use?"
      answer: "Use JPEG or WebP, keep the long edge around 1200 to 1600 pixels, and compress each file to under 300 KB. Consistent dimensions across a gallery give a smoother lightbox experience."
    - question: "How do readers view the full-size image?"
      answer: "Clicking or tapping a gallery thumbnail opens it in a full-screen PhotoSwipe lightbox. Readers can then use the arrow buttons, the keyboard arrows, or a swipe to move between images, and zoom with a pinch or double tap."
---

Screenshots of a fix, frames from a demo, or a set of diagrams are three of the fastest ways to explain something in a tutorial. The problem is that a wall of full-size images is slow and ugly, and a single inline picture cannot show a sequence. Dev9b solves this with built-in image galleries powered by [PhotoSwipe](https://photoswipe.com/), the same lightbox library used by many documentation sites.

This guide covers the exact syntax, the page-bundle rule that trips people up, and the small habits that keep galleries fast and accessible. It is written for anyone submitting an article to Dev9b, so it pairs naturally with our [contributor guide](/contribute/).

<!--more-->

## What the Dev9b Gallery Actually Is

Sorting your images into a gallery does not require a shortcode, a plugin, or any HTML. You write ordinary Markdown image syntax, and when two or more images sit next to each other the theme wraps them into a [PhotoSwipe](https://photoswipe.com/) gallery. PhotoSwipe is a dependency-free, modular lightbox: it handles the full-screen viewer, pinch and double-tap zoom, keyboard navigation, and smooth transitions between images.

The syntax was originally inspired by [Typlog](https://typlog.com/), which is why it feels so minimal. There is nothing to configure per image beyond the alt text.

## Requirements: Images Must Live in the Page Bundle

This is the one rule that breaks most first attempts. On Dev9b an article is a **page bundle**: a directory named after the slug that contains both `index.md` and every image the article uses.

External images and hotlinked URLs are not supported by the gallery. There are two good reasons:

1. **Reliability.** A remote image disappears the moment the host moves or deletes the file, leaving a broken gallery.
2. **Performance.** Local images are served from the same fast origin as the page, so the gallery opens instantly instead of waiting on a third-party server.

So the layout for an article with a gallery looks like this:

```text
content/post/image-gallery-in-dev9b-articles/
├── index.md      # the article
├── cover.jpg     # the social/cover image
├── 1.jpg         # first gallery image
└── 2.jpg         # second gallery image
```

If you have ever wondered how images and Markdown fit together in a Hugo site, our [Markdown syntax guide for Dev9b](/p/markdown-syntax-guide-for-dev9b/) walks through the full file model.

## The Gallery Syntax

Put two or more images on the same line, each in standard Markdown form:

```markdown
![Image 1](1.jpg) ![Image 2](2.jpg)
```

Adjacent images on one line become one gallery. If you separate them with a blank line, each becomes a standalone image instead. That is the entire API.

Here is what that exact line renders as in this article. Because the files `1.jpg` and `2.jpg` sit beside this `index.md`, the two pictures below form a single browsable gallery:

![A developer reviewing a set of screenshots on a laptop](1.jpg) ![A gallery of product images laid out in a lightbox](2.jpg)

Click either image and the lightbox opens with both, in order.

## Building a Gallery Step by Step

The workflow for a real article is short:

1. Prepare your images: crop, resize, and compress them before you add them to the bundle.
2. Name them predictably, using `1.jpg`, `2.jpg`, `3.jpg` or descriptive names like `before.jpg` and `after.jpg`.
3. Copy them into the same directory as `index.md`.
4. Reference them on one line with `![alt text](filename.jpg)`.
5. Build locally and click a thumbnail to confirm the lightbox opens with every image.

If the gallery does not appear, the cause is almost always a filename or path mismatch, not the syntax.

## Writing Good Alt Text

Alt text is not optional on Dev9b. It is read aloud by screen readers, shown when an image fails to load, and used by search engines to understand the picture. Write a sentence that describes what the image shows, not what the file is called.

| Weak alt text | Better alt text |
|---|---|
| `![screenshot](1.jpg)` | `![GitHub branch protection settings with force pushes blocked](1.jpg)` |
| `![image](2.jpg)` | `![Side-by-side before and after of the redesigned pricing table](2.jpg)` |
| `![photo](3.jpg)` | `![A team pair-programming in a terminal with two agents running](3.jpg)` |

The pattern is simple: name the subject and, when it matters, the specific detail a reader should notice. For a deeper look at how images affect search, our [Hugo SEO checklist](/p/hugo-seo-guide/) covers alt text alongside titles, descriptions, and structured data.

## Sizing, Formatting, and Performance

Gallery images are the heaviest asset on most tutorial pages, so a little discipline pays off.

- **Format:** JPEG or WebP. Avoid PNG for photographs; it is much larger for the same visual quality.
- **Dimensions:** around 1200 to 1600 pixels on the long edge is plenty for a lightbox on most screens.
- **File size:** keep each image under about 300 KB. Several images at multi-megabyte sizes will make the page feel slow on mobile.
- **Consistency:** images in the same gallery look best when they share an aspect ratio.

A quick compression pass is worth more than any code change. Resize to your target width, export at roughly 80 to 85 percent quality, and strip metadata.

## Common Problems and Fixes

Here are the failures we see most often when reviewing galleries, and what actually causes them.

| Symptom | Likely cause | Fix |
|---|---|---|
| Image shows as a broken icon | File is not in the page bundle | Move it next to `index.md` and check the exact filename and extension, including case |
| Two images do not group into a gallery | A blank line sits between them | Put them on the same line |
| Gallery is very slow to open | Files are too large | Compress each image to under 300 KB |
| Image is missing from the built site | The path is external or absolute | Use a relative in-bundle filename such as `1.jpg` |
| Lightbox opens but looks blurry | Image is smaller than the display size | Re-export at a higher resolution |

## Frequently Asked Questions

### How do I create an image gallery in a Dev9b article?

Place the image files in the same directory as your `index.md`, then reference several of them on one line with standard Markdown, for example `![alt one](1.jpg) ![alt two](2.jpg)`. Dev9b groups adjacent images into one PhotoSwipe gallery automatically.

### Can I use images hosted on another website?

No. Gallery images must be local files inside the page bundle. External and hotlinked images are not supported, because they break when the remote host removes or moves the file and they slow the page down.

### Does every image need alt text?

Yes. Alt text is required for accessibility and it is good for SEO. Write a short description of what the image shows rather than repeating the file name.

### What image size and format should I use?

Use JPEG or WebP, keep the long edge around 1200 to 1600 pixels, and compress each file to under 300 KB. Consistent dimensions across a gallery give a smoother lightbox experience.

### How do readers view the full-size image?

Clicking or tapping a gallery thumbnail opens it in a full-screen PhotoSwipe lightbox. Readers can then use the arrow buttons, the keyboard arrows, or a swipe to move between images, and zoom with a pinch or double tap.

## Key Takeaways

- Galleries need no shortcode: put two or more Markdown images on one line and Dev9b turns them into a PhotoSwipe gallery.
- Every image must be a local file inside the same page bundle as `index.md`; external and hotlinked images are not supported.
- Alt text is mandatory, and descriptive alt text helps both screen-reader users and search engines.
- Compress to under 300 KB, keep the long edge near 1200 to 1600 pixels, and use JPEG or WebP for photographs.
- A blank line between images breaks the gallery; a filename mismatch breaks the image. Check those two things first.

## Conclusion

Image galleries are one of the highest-leverage features for a tutorial, because a sequence of annotated screenshots often explains in ten seconds what a paragraph struggles to do in a minute. The syntax is deliberately boring, and that is a feature: once your images live in the page bundle and carry honest alt text, the lightbox takes care of itself.

If you are preparing your first submission and want to see how galleries, headings, and code blocks fit together, read the full [Markdown syntax guide for Dev9b](/p/markdown-syntax-guide-for-dev9b/) next. Teams like F9XR treat a clean bundle and descriptive alt text as part of the review checklist, not an afterthought.

Ready to contribute? The [Contributor Guide](/contribute/) explains how to submit an article to Dev9b, and everything we publish is reviewed against the standards in our [Editorial Policy](/editorial-policy/).

---

*Gallery images in this article are from [Unsplash](https://unsplash.com/): photo by [mymind](https://unsplash.com/@mymind) and [Luke Chesser](https://unsplash.com/@lukechesser). This guide was drafted with the assistance of an AI coding assistant, then reviewed by the F9XR Review Board before publishing.*
