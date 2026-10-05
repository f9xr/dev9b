---
title: Markdown Syntax Guide for Dev9b
description: "Learn the Markdown syntax used on Dev9b. A comprehensive guide to formatting your articles with headings, code blocks, tables, and more."
date: 2024-01-15
tags:
 - markdown
 - tutorial
 - writing
 - dev9b
categories:
 - Tutorials
---

This article offers a sample of basic Markdown syntax that can be used in Dev9b content files. Use this as a reference when writing your own articles.

<!--more-->

## Headings

Use `#` symbols to create headings. More `#` means a smaller heading.

# H1
## H2
### H3
#### H4
##### H5
###### H6

## Paragraph

Separate paragraphs with a blank line. This is a regular paragraph in Dev9b.

Write your content naturally. Hugo will handle the spacing and formatting.

## Blockquotes

Use `>` to create blockquotes:

> Dev9b is a free, open - source online community where software developers share knowledge, write technical articles, and help each other grow.

### Blockquote with attribution

> "Talk is cheap. Show me the code."<br>
> - <cite>Linus Torvalds</cite>

## Tables

| Feature | Dev9b | Others |
|---------|-------|--------|
| Free | ✅ | Varies |
| Open Source | ✅ | No |
| Developer - focused | ✅ | Sometimes |

### Inline Markdown within tables

| Italics | Bold | Code |
|---------|------|------|
| *italics* | **bold** | `code` |

## Code Blocks

Use triple backticks with a language identifier:

```javascript
function greetDeveloper(name) {
 return `Welcome to Dev9b, ${name}!`;
}

console.log(greetDeveloper("World"));
```

```python
def greet_developer(name):
 return f"Welcome to Dev9b, {name}!"

print(greet_developer("World"))
```

### Diff code block

```diff
- const oldWay = "verbose";
+ const newWay = "clean";
```

## Lists

### Ordered List

1. Fork the repository
2. Create your article
3. Submit a pull request

### Unordered List

* Write your article in Markdown
* Add a cover image
* Include code examples

### Nested list

* Tutorials
 * Beginner
 * Intermediate
 * Advanced
* How - To Guides
 * Quick tips
 * Step - by - step

## Other Elements

Abbreviations: <abbr title="HyperText Markup Language">HTML</abbr>

Subscript: H<sub>2</sub>O

Superscript: X<sup>n</sup>

Keyboard: <kbd>Ctrl</kbd> + <kbd>C</kbd>

Highlight: <mark>Important</mark>

## Need Help?

Check the [Contributor Guide](/contribute) for more details on writing articles for Dev9b.
