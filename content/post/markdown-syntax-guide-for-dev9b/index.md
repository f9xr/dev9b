---
title: "Markdown Syntax Guide for Dev9b"
description: "The complete Markdown reference for Dev9b articles: headings, links, lists, tables, code blocks, callouts, and the exact syntax the platform renders."
slug: markdown-syntax-guide-for-dev9b
date: 2024-01-15
image: cover.jpg
author: F9XR Team
keywords:
    - dev9b markdown
    - markdown syntax
    - markdown cheat sheet
    - github flavored markdown
    - code blocks
    - markdown tables
    - markdown headings
categories:
    - Tutorials
tags:
    - markdown
    - tutorial
    - writing
    - dev9b
draft: false
math: false
faq:
    - question: "What flavor of Markdown does Dev9b use?"
      answer: "Dev9b renders content with Hugo's Goldmark parser configured for GitHub Flavored Markdown, extended with tables, strikethrough, autolinks, task lists, and footnotes. That means the syntax you already know from a GitHub README works here."
    - question: "Can I use raw HTML in a Dev9b article?"
      answer: "Yes, a limited and safe subset of HTML such as abbreviation, keyboard, subscript, and superscript tags is allowed. Keep it minimal, because plain Markdown is easier to read and maintain."
    - question: "How do I link to another Dev9b article?"
      answer: "Use an inline link with a root-relative path, for example [text](/p/hello-world/). Root-relative links keep readers inside the site and are preferred over absolute URLs."
    - question: "How many spaces should I indent a nested list?"
      answer: "Indent nested items with two spaces and keep the marker style consistent within each level. Four spaces can be read as a code block by some parsers, which is a common cause of broken lists."
    - question: "Why is my table not rendering?"
      answer: "Tables need a blank line before them, a header row, and a separator row of at least three dashes per column, such as | --- |. Missing any of those three turns the table back into plain text."
---

Markdown is the writing format behind every Dev9b article. It is plain text with a few punctuation rules that turn into formatted HTML, which is why it is readable even before it is rendered and why it stays portable across editors, repositories, and years. If you have ever written a GitHub README, you already know most of this page.

This is the reference we keep open when drafting: the syntax that Dev9b actually renders, the handful of rules that catch people out, and how each feature looks once built. For a working example of images inside an article, see our [image gallery guide](/p/image-gallery-in-dev9b-articles/).

<!--more-->

## What Dev9b Uses Under the Hood

Dev9b is built with [Hugo](https://gohugo.io/) and renders Markdown through its Goldmark parser configured for [GitHub Flavored Markdown](https://github.github.com/gfm/). In practice that means you get the [CommonMark](https://commonmark.org/) core plus the extensions developers expect:

- tables
- strikethrough with double tildes
- autolinked URLs
- task lists
- footnotes
- syntax-highlighted code blocks

Because it is GitHub Flavored Markdown, the syntax transfers directly from your README files. Nothing here is Dev9b-specific except the front matter and the shortcodes.

## Headings and Document Structure

Headings are made with hash marks. More hashes mean a smaller heading. Dev9b reserves the page title for the front matter, so your body should start at the second level and never include a top-level heading.

```markdown
## Section heading
### Subsection heading
#### Smaller heading
```

Use `##` for main sections and `###` for subsections. A clean outline helps both readers skimming the page and search engines building a table of contents. Do not skip levels just to change the size: go from `##` to `###`, not straight to `####`.

## Paragraphs and Line Breaks

Separate paragraphs with a blank line. A single line break inside a paragraph is treated as a space, which lets you wrap long lines in your editor without changing the output.

```markdown
This is one paragraph.

This is a second paragraph.
```

If you truly need a line break in the middle of a paragraph, end the line with two trailing spaces or a backslash, but use that sparingly.

## Emphasis, Links, and Images

Emphasis uses asterisks or underscores:

```markdown
*italic*  or  _italic_
**bold**  or  __bold__
***bold and italic***
~~strikethrough~~
```

Links use square brackets for the text and parentheses for the target:

```markdown
[Contributor Guide](/contribute/)
![Alt description](1.jpg)
```

Two rules matter on Dev9b. First, link to other articles with a root-relative path such as `/p/hello-world/` rather than a full `https://f9xr.org/...` address, so the link survives a domain change. Second, always give images descriptive alt text; the [image gallery guide](/p/image-gallery-in-dev9b-articles/) explains why in detail.

## Lists

Ordered and unordered lists both work, and they nest with indentation.

```markdown
1. Fork the repository
2. Create the article
3. Submit a pull request

- Write in Markdown
- Add a cover image
- Include code examples
```

Nested items use two spaces:

```markdown
- Tutorials
  - Beginner
  - Intermediate
- How-To Guides
  - Quick tips
```

Task lists are handy for step-by-step posts:

```markdown
- [x] Draft the outline
- [ ] Add code samples
- [ ] Proofread
```

## Blockquotes and Callouts

A blockquote starts with a greater-than sign. Dev9b also supports GitHub-style alerts, which turn a blockquote into a colored callout with an icon:

```markdown
> A plain blockquote.

> [!NOTE]
> Useful information that readers should notice.

> [!WARNING]
> Something that could break their setup.
```

Use alerts for tips, warnings, and important notes, and reserve plain blockquotes for quotations or example text.

## Code: Inline and Fenced

Wrap a word in single backticks for inline code, and use triple backticks with a language tag for a block. The language tag enables syntax highlighting and adds a copy button by default in the reader toolbar.

```text
`npm install`
```

Then tag the language whenever you write a block:

```javascript
function greet(name) {
  return `Welcome to Dev9b, ${name}!`;
}
```

Diff blocks are useful in changelog and migration posts, because added and removed lines are colored:

```diff
- const oldWay = "verbose";
+ const newWay = "clean";
```

Always name the language. A block without a tag still renders, but it loses highlighting and confuses readers who are scanning for a specific language.

## Tables

Tables need a header row, a separator row, and a blank line before the table:

```markdown
| Feature      | Dev9b | Others  |
| ------------ | ----- | ------- |
| Free         | Yes   | Varies  |
| Open source  | Yes   | No      |
| Developer UX | Yes   | Sometimes |
```

You can put inline formatting inside cells:

| Format | Example |
| ------ | ------- |
| Italic | *renders* |
| Bold | **renders** |
| Code | `renders` |

If a table turns into plain text, the usual cause is a missing separator row or a missing blank line above it.

## Horizontal Rules and Other Elements

A line of three dashes creates a horizontal rule. A small set of inline HTML tags is also allowed for the cases Markdown cannot express:

```markdown
---

<abbr title="HyperText Markup Language">HTML</abbr>
H<sub>2</sub>O
X<sup>n</sup>
<kbd>Ctrl</kbd> + <kbd>C</kbd>
<mark>Highlighted text</mark>
```

Keep this list short. Inline HTML is fine for an abbreviation or a keyboard key, but heavy HTML defeats the point of writing in Markdown.

## Escaping Special Characters

To show a character that would otherwise be interpreted, escape it with a backslash. This is how you write a literal asterisk or hash without triggering formatting:

```markdown
\*not italic\*
\#not a heading
```

The backslash escape works for the punctuation characters Markdown treats as meaningful.

## Putting It Together in a Dev9b Article

A well-formed article follows the same shape every time. It opens with a two or three sentence introduction that states the problem, then a `<!--more-->` divider, and then second-level sections that each make one point. Within a section, a short paragraph leads into a code block, a table, or a list, and the section ends with a sentence that tells the reader what to do next.

That rhythm matters more than any single feature. When a heading promises a topic, the next paragraph should deliver it, and a code block should always sit under a sentence that explains what it does and why. Links go inline where the reader needs them, not in a pile at the bottom. Images get alt text. Code fences name their language. Tables get a blank line above them.

Follow that structure and the formatting fades into the background, which is the entire goal. The reader should notice the explanation, never the syntax. Reviewers on the F9XR Review Board check this shape first, because a consistent structure is what makes a long reference article easy to skim and easy to trust.

## Frequently Asked Questions

### What flavor of Markdown does Dev9b use?

Dev9b renders content with Hugo's Goldmark parser configured for GitHub Flavored Markdown, extended with tables, strikethrough, autolinks, task lists, and footnotes. That means the syntax you already know from a GitHub README works here.

### Can I use raw HTML in a Dev9b article?

Yes, a limited and safe subset of HTML such as abbreviation, keyboard, subscript, and superscript tags is allowed. Keep it minimal, because plain Markdown is easier to read and maintain.

### How do I link to another Dev9b article?

Use an inline link with a root-relative path, for example `[text](/p/hello-world/)`. Root-relative links keep readers inside the site and are preferred over absolute URLs.

### How many spaces should I indent a nested list?

Indent nested items with two spaces and keep the marker style consistent within each level. Four spaces can be read as a code block by some parsers, which is a common cause of broken lists.

### Why is my table not rendering?

Tables need a blank line before them, a header row, and a separator row of at least three dashes per column, such as `| --- |`. Missing any of those three turns the table back into plain text.

## Key Takeaways

- Dev9b uses Hugo's Goldmark with GitHub Flavored Markdown, so README syntax works unchanged.
- Start body headings at `##`; the page title comes from the YAML front matter, never a body heading.
- Link internally with root-relative paths like `/p/hello-world/`, and always add descriptive image alt text.
- Name the language on every code fence to get highlighting and a copy button, and keep a blank line before every table.
- Two spaces indent nested lists; four spaces can be misread as a code block.

## Conclusion

Markdown rewards consistency more than cleverness. If you keep one blank line between blocks, start your headings at the second level, name your code languages, and link internally, your drafts will render correctly the first time and read well in plain text too.

Once the basics are second nature, the natural next step is to learn the platform's [useful shortcodes for Dev9b articles](/p/useful-shortcodes-for-dev9b-articles/), which add embeds and media that Markdown alone cannot express. If your article leans on formulas, the [math typesetting guide](/p/math-typesetting-on-dev9b/) shows how to enable KaTeX.

Want to publish on Dev9b? Read the [Contributor Guide](/contribute/) to submit an article, and check our [Editorial Policy](/editorial-policy/) for the review standards every post is held to.

---

*This guide was drafted with the assistance of an AI coding assistant, then reviewed by the F9XR Review Board before publishing.*
