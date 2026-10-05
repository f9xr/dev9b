---
title: "Math Typesetting on Dev9b"
description: "Learn how to write mathematical equations in your Dev9b articles using KaTeX. Supports inline and block math."
date: 2024-01-20
math: true
tags:
    - math
    - latex
    - writing
    - dev9b
categories:
    - Tutorials
---

Dev9b supports math typesetting using [KaTeX](https://katex.org/). Write mathematical expressions directly in your articles.

**It's not enabled by default site-wide**, but you can enable it for individual posts by adding `math: true` to the front matter. Or you can enable it site-wide by adding `math = true` to the `params.article` section in `config.toml`.

## Inline math

This is an inline mathematical expression: $\varphi = \dfrac{1+\sqrt5}{2}= 1.6180339887…$

```markdown
$\varphi = \dfrac{1+\sqrt5}{2}= 1.6180339887…$
```

## Block math

$$
    \varphi = 1+\frac{1} {1+\frac{1} {1+\frac{1} {1+\cdots} } } 
$$

```markdown
$$
    \varphi = 1+\frac{1} {1+\frac{1} {1+\frac{1} {1+\cdots} } } 
$$
```

$$
    f(x) = \int_{-\infty}^\infty\hat f(\xi)\,e^{2 \pi i \xi x}\,d\xi
$$

```markdown
$$
    f(x) = \int_{-\infty}^\infty\hat f(\xi)\,e^{2 \pi i \xi x}\,d\xi
$$
```

## Writing Math on Dev9b

When contributing articles with math to Dev9b:

1. Add `math: true` to your front matter
2. Use `$...$` for inline math
3. Use `$$...$$` for block math
4. Test your equations before submitting

> Tip: Check the [Contributor Guide](/contribute) for more writing tips.
