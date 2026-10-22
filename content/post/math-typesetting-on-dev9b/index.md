---
title: "Math Typesetting on Dev9b"
description: "Write KaTeX equations in Dev9b articles. Enable math per post, use inline and block syntax correctly, and avoid the pitfalls that break rendering."
slug: math-typesetting-on-dev9b
date: 2026-01-20
image: cover.jpg
author: F9XR Team
keywords:
    - dev9b math
    - katex
    - latex in markdown
    - inline math
    - block equations
    - hugo katex
    - typesetting
categories:
    - Tutorials
tags:
    - math
    - latex
    - writing
    - dev9b
draft: false
math: true
faq:
    - question: "How do I enable math in a Dev9b article?"
      answer: "Add math: true to the front matter of the post. Math is off by default because loading KaTeX on every page would slow down articles that never use an equation."
    - question: "What is the difference between inline and block math?"
      answer: "Wrap inline math in single dollar signs, like $E = mc^2$, so it flows inside a sentence. Wrap block math in double dollar signs on their own lines to display a centered equation."
    - question: "Which LaTeX commands does KaTeX support?"
      answer: "KaTeX implements a large but not complete subset of LaTeX math. Most common commands, fractions, integrals, sums, matrices, and alignment environments work; check the KaTeX support table for anything unusual."
    - question: "Why is my equation showing as plain text?"
      answer: "The most common causes are missing math: true in the front matter, a missing closing dollar sign, or a space between the dollar sign and the formula. Dollar delimiters must touch the math with no gap."
    - question: "Can I use math inside a code block?"
      answer: "Yes. Put the LaTeX source inside a fenced code block so readers can copy it, and place the live equation outside the fence where KaTeX will render it."
---

Some articles cannot be written in plain prose. An optimization post needs a loss function, a statistics write-up needs a distribution, and a cryptography explainer needs a little modular arithmetic. Dev9b renders mathematical notation with [KaTeX](https://katex.org/), the fast, self-contained typesetting library, so equations look the way they do in a textbook instead of as a tangle of carets and underscores.

This guide shows how to switch math on for a post, how inline and display math differ, and the small syntax rules that decide whether an equation renders or shows up as literal dollar signs. It assumes you are comfortable with the basics covered in our [Markdown syntax guide for Dev9b](/p/markdown-syntax-guide-for-dev9b/).

<!--more-->

## Why KaTeX Instead of Images or MathJax

There are three common ways to put math on the web, and KaTeX is the one that fits a fast static blog:

- **Images** are crisp but not selectable, not searchable, and impossible to edit.
- **MathJax** is powerful and broad, but heavier to load.
- **[KaTeX](https://katex.org/)** renders synchronously and is much smaller, so an equation appears with the rest of the page instead of popping in later.

KaTeX is not a complete LaTeX distribution, but it covers the notation an article actually needs. The maintainers publish a [support table](https://katex.org/docs/supported.html) listing every command, which is the page to bookmark when you use something unusual.

## Enabling Math for a Post

Math is **not enabled site-wide by default**, because loading KaTeX on every article would add weight to the many posts that never use a formula. You opt in per post by adding a single key to the front matter:

```yaml
---
title: "My Equation-Heavy Article"
math: true
---
```

That is all it takes. Site maintainers can also flip it on globally by setting `math = true` under the `params.article` section of the site configuration, but per-post is the better default and the one Dev9b uses.

## Inline Math

Inline math sits inside a sentence and is wrapped in single dollar signs. It is ideal for a variable or a short expression:

```markdown
The golden ratio is $\varphi = \dfrac{1+\sqrt5}{2}= 1.6180339887\ldots$
```

That source renders as: the golden ratio is $\varphi = \dfrac{1+\sqrt5}{2}= 1.6180339887\ldots$ which lets you weave symbols into running text without breaking the paragraph.

Use inline math for single symbols and short expressions. If an expression is longer than a few terms, promote it to display math so it has room to breathe.

## Display (Block) Math

Display math is centered on its own line and is wrapped in double dollar signs, with the delimiters on separate lines:

```markdown
$$
    \varphi = 1+\frac{1} {1+\frac{1} {1+\frac{1} {1+\cdots} } }
$$
```

It renders as a centered, full-size equation:

$$
    \varphi = 1+\frac{1} {1+\frac{1} {1+\frac{1} {1+\cdots} } }
$$

Use display math for anything a reader needs to study rather than skim. A continued fraction like the one above, or an integral, collapses into an unreadable line if you try to keep it inline.

## A Worked Example

Here is a classic integral, the Gaussian, in display form:

$$
    f(x) = \int_{-\infty}^\infty\hat f(\xi)\,e^{2 \pi i \xi x}\,d\xi
$$

And the same idea inline: the Fourier inversion formula expresses $f(x)$ as an integral over frequencies $\xi$.

The pattern is consistent. Write the LaTeX you already know, choose inline for short expressions and display for substantial ones, and let KaTeX do the layout. Spacing commands such as `\,` and `\quad` give you fine control when the automatic spacing in an integral or a sum is not quite right.

## Aligning Multi-Line Equations

For a derivation with several steps, use an alignment environment so the equals signs line up:

```markdown
$$
\begin{aligned}
(a+b)^2 &= a^2 + 2ab + b^2 \\
(a-b)^2 &= a^2 - 2ab + b^2
\end{aligned}
$$
```

Which produces:

$$
\begin{aligned}
(a+b)^2 &= a^2 + 2ab + b^2 \\
(a-b)^2 &= a^2 - 2ab + b^2
\end{aligned}
$$

The `&` marks the alignment point and `\\` ends each row. Matrices and cases work the same way through the `\begin{matrix}`, `\begin{pmatrix}`, and `\begin{cases}` environments.

## A Small Symbol Cheat Sheet

| Symbol | Source | Symbol | Source |
| ------ | ------ | ------ | ------ |
| $\alpha, \beta, \gamma$ | `\alpha, \beta, \gamma` | $\infty$ | `\infty` |
| $\sum_{i=1}^{n}$ | `\sum_{i=1}^{n}` | $\int_a^b$ | `\int_a^b` |
| $\frac{a}{b}$ | `\frac{a}{b}` | $\sqrt{x}$ | `\sqrt{x}` |
| $\le, \ge, \ne$ | `\le, \ge, \ne` | $\times, \cdot$ | `\times, \cdot` |

Greek letters, sums, integrals, fractions, roots, and comparison operators cover the vast majority of what appears in technical articles.

## Pitfalls That Break Rendering

Almost every "my equation will not render" report comes down to one of these:

- **Missing opt-in.** Without `math: true` in the front matter, dollar signs stay literal.
- **A space after the opening dollar.** `$ x $` and `$x$` are not the same; with math enabled, avoid stray spaces next to the delimiters.
- **An unclosed delimiter.** Every `$` needs a partner, and every `$$` needs a matching `$$`.
- **Markdown eating your underscores.** Inline without math enabled, `a_b` becomes emphasis; enabling math for the post avoids the clash.
- **Escaping problems.** A literal percent sign or backslash that is not part of a command needs care; `\%` and `\backslash` are your friends.

A quick local build is the fastest way to catch these before you submit.

## Frequently Asked Questions

### How do I enable math in a Dev9b article?

Add `math: true` to the front matter of the post. Math is off by default because loading KaTeX on every page would slow down articles that never use an equation.

### What is the difference between inline and block math?

Wrap inline math in single dollar signs, like `$E = mc^2$`, so it flows inside a sentence. Wrap block math in double dollar signs on their own lines to display a centered equation.

### Which LaTeX commands does KaTeX support?

KaTeX implements a large but not complete subset of LaTeX math. Most common commands, fractions, integrals, sums, matrices, and alignment environments work; check the KaTeX support table for anything unusual.

### Why is my equation showing as plain text?

The most common causes are missing `math: true` in the front matter, a missing closing dollar sign, or a space between the dollar sign and the formula. Dollar delimiters must touch the math with no gap.

### Can I use math inside a code block?

Yes. Put the LaTeX source inside a fenced code block so readers can copy it, and place the live equation outside the fence where KaTeX will render it.

## Key Takeaways

- Math is opt-in per post: add `math: true` to the front matter before you write a single dollar sign.
- Use single dollar signs for inline math and double dollar signs on their own lines for centered display math.
- KaTeX covers the common LaTeX subset well; the alignment, matrix, and cases environments handle multi-line work.
- Whitespace matters: delimiters must touch the math, and every opening delimiter needs a partner.
- Show the LaTeX source in a code block next to the live equation so readers can copy it.

## Conclusion

Math on a static site is a solved problem when you keep two rules in mind: opt in per post, and let inline math stay inline while display math gets its own centered line. Everything else is ordinary LaTeX that KaTeX turns into clean, selectable, searchable notation. And if you use LaTeX beyond the browser, the same skills carry straight into an [ATS-friendly LaTeX resume](/p/ats-friendly-latex-resume-guide/) that survives applicant-tracking parsers.

If your equations live alongside code, tables, and diagrams, the [useful shortcodes for Dev9b articles](/p/useful-shortcodes-for-dev9b-articles/) round out the toolbox, and the [image gallery guide](/p/image-gallery-in-dev9b-articles/) shows how to add figures that complement the math.

Want to publish a technical article on Dev9b? The [Contributor Guide](/contribute/) explains how to submit, and the [Editorial Policy](/editorial-policy/) describes how every post is reviewed.

---

*This guide was drafted with the assistance of an AI coding assistant, then reviewed by the F9XR Review Board before publishing.*
