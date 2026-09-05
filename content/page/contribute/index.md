---
title: Contributor Guide
description: "How to contribute articles to Dev9b. A step-by-step guide for developers."
slug: contribute
date: 2024-01-01
menu:
    main:
        weight: 6
        params:
            icon: messages
---

## How to Contribute to Dev9b

Dev9b is an open-source developer blog. We welcome articles from developers of all skill levels. This guide walks you through the process of submitting your first article.

### Prerequisites

- A [GitHub account](https://github.com/join)
- Basic knowledge of Markdown
- Your article content ready

### Step 1: Fork the Repository

1. Go to the [Dev9b repository](https://github.com/f9xr/dev9b)
2. Click the **Fork** button in the top right
3. Clone your forked repository locally:

```bash
git clone https://github.com/YOUR-USERNAME/dev9b.git
cd dev9b
```

### Step 2: Create Your Article

Create a new directory under `content/post/` with your article slug:

```bash
mkdir content/post/your-article-slug
```

Create an `index.md` file inside with the following front matter:

```markdown
---
title: Your Article Title
description: A brief description of your article (for SEO)
date: 2024-01-15
image: cover.jpg
categories:
    - Your Category
tags:
    - tag1
    - tag2
---

Write your article content here using Markdown.
```

### Step 3: Add a Cover Image

Place a cover image (recommended: 1200x630px) in the same directory as your `index.md`:

```bash
cp /path/to/cover.jpg content/post/your-article-slug/
```

### Step 4: Submit a Pull Request

1. Commit your changes:

```bash
git add .
git commit -m "Add article: Your Article Title"
git push origin main
```

2. Go to the [Dev9b repository](https://github.com/f9xr/dev9b)
3. Click **New Pull Request**
4. Select your fork and branch
5. Fill in the PR template with your article details

### Step 5: Review Process

All submissions go through the **F9XR Review Board** before publishing. Here's what we check:

| Check | Description |
|-------|-------------|
| Content Quality | Clear, accurate, well-written |
| Relevance | Relevant to software development |
| Originality | Not duplicated from other sources |
| Formatting | Proper Markdown, no broken links |
| Images | Properly attributed, open license |

The review typically takes **1-3 business days**. You may receive feedback requesting changes.

### Article Guidelines

#### Writing Style

- Write in **clear, concise English**
- Use **headings** to organize content
- Include **code examples** where applicable
- Add **images** to break up text

#### Technical Requirements

- **Minimum length:** 500 words
- **Code blocks:** Use proper syntax highlighting
- **Images:** Must be open-source or your own (with attribution)
- **Links:** Must be working and relevant

#### Categories

Choose from existing categories or suggest a new one:

- **Tutorials** — Step-by-step guides
- **How-To** — Quick solutions to specific problems
- **Deep Dives** — In-depth technical articles
- **Opinion** — Developer perspectives and experiences
- **News** — Latest trends and updates

### Article Structure Template

```markdown
---
title: "Your Article Title"
description: "A concise description for search engines"
date: 2024-01-15
categories:
    - Tutorials
tags:
    - javascript
    - web-development
---

## Introduction

Briefly introduce the topic and what readers will learn.

## Prerequisites

List what readers need to know or have installed.

## Step 1: First Step

Explain the first step with code examples.

```javascript
const example = "Hello, Dev9b!";
console.log(example);
```

## Step 2: Second Step

Continue with the next step.

## Conclusion

Summarize what was covered and suggest next steps.

## References

- [Dev9b repository](https://github.com/f9xr/dev9b)
- [Open an issue](https://github.com/f9xr/dev9b/issues)
```

### Need Help?

- Open an issue on [GitHub](https://github.com/f9xr/dev9b/issues)
- Comment on an existing PR for feedback
- Join the discussion in GitHub Discussions

### Recognition

All contributors are recognized in the article's byline and in the repository's contributors list. Thank you for helping grow the developer community!
