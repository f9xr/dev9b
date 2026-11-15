---
title: "AI Loves Purple: Most and Least Used AI Colors"
description: "Which colors does AI use most and least? See the purple problem, what research shows, why it happens and how to fix AI default palettes in your code."
slug: most-least-used-colors-by-ai
date: 2026-11-15
image: most-least-used-ai-colors.webp
imageAlt: "AI robot and paint palette above the headline Most and Least Used AI Colors"
author: F9XR Team
keywords:
    - colors most used by AI
    - AI generated website colors
    - purple gradient problem
    - Tailwind indigo-500
    - AI slop design
    - LLM color palette
    - vibe coding design
    - AI color bias
categories:
    - AI Tools
tags:
    - ai-tools
    - web-design
    - vibe-coding
    - css
draft: false
math: false
faq:
    - question: "What color does AI use most?"
      answer: "AI generated websites most often use blue, indigo and violet, frequently as gradients. A 2026 study found blue was the most common color overall, and designers widely report indigo to purple gradients as the most recognizable AI design tell."
    - question: "Why does AI love purple and indigo?"
      answer: "The best documented explanation is Tailwind CSS, whose demos used bg-indigo-500 as the default button color. Code that copied it likely entered training data. This is a plausible cause, but nobody has measured it directly."
    - question: "What colors does AI use least?"
      answer: "In one 2026 study, pink and black were the least frequent colors reported. Designers also observe that warm and earthy colors such as deep green, ochre, amber and terracotta are rare in default AI output, though that has not been counted."
    - question: "Why do AI generated websites all look the same?"
      answer: "When a prompt gives no specific palette, models fall back on their most common associations, such as indigo buttons, gradients, dark hero sections and Inter style fonts. Giving the model explicit color tokens and an avoid list produces more varied results."
    - question: "Is indigo-500 accessible with white text?"
      answer: "Not quite. Tailwind v3 indigo-500 (#6366f1) with white text has a contrast ratio of about 4.47:1, just below the 4.5:1 WCAG AA requirement for normal text. Indigo-600 passes at about 6.29:1."
    - question: "How do I stop AI from using purple gradients?"
      answer: "Define your brand colors as CSS variables, tell the model to use only those, and add an explicit instruction to avoid Tailwind's indigo, violet and purple scales and gradients. Specific constraints work better than asking it to be unique."
---

Ask any AI coding tool for a landing page and watch what happens. A dark hero section. A glowing card or two. A button that fades from indigo into purple. Ask again with different words and you often get the same thing.

If you have noticed this, you are not imagining it. Developers have been joking about "the purple problem" for more than a year, and the creator of Tailwind CSS publicly apologized for his part in it. But the jokes hide a more useful question: **which colors does AI actually use the most, which does it use the least, and what can you do about it when you ship real products?** This guide breaks down the colors most used by AI, where they come from, and the exact steps to replace them in your own code.

<!--more-->

We answer that with a clear line between three kinds of evidence: what was actually measured, what is well documented history, and what is designer observation. Then we give you code you can use today to find and replace AI default colors in your own projects.

## The Short Answer

**Most used by AI:** Blue, indigo, violet and purple, often as gradients. Stock Tailwind swatches. White or near white backgrounds with slate grays. Dark backgrounds with glowing purple or blue accents.

**Least used by AI:** In the one academic study we found that counted colors, pink and black were the least frequent. Designers also point to warm and earthy colors as rare in AI output, such as deep greens, ochre, amber, terracotta and warm off whites. That second group comes from observation, not a published count.

> [!NOTE] How we graded the evidence
> We could not find a large, independent census of every color AI tools produce. Anyone who gives you exact percentages for "AI's favorite color" is guessing. What exists is a mix of a small study, a well documented origin story and a lot of consistent practitioner experience. Each claim below is labelled.

## Colors Most Used by AI: The Defaults You See Everywhere

| Color pattern | Where it shows up | Evidence strength |
|---|---|---|
| Indigo and violet buttons | Primary buttons, links, focus rings | Strong: documented origin, widely reported |
| Blue to purple or pink to purple gradients | Hero sections, headline text, buttons | Strong: widely reported by designers |
| Blue as the default scheme | Generic sites when no scheme is given | Measured in a 2026 study |
| Dark background with neon purple glow | SaaS and AI product landing pages | Moderate: designer observation |
| Pure white backgrounds and slate grays | Cards, sections, body text | Moderate: appears in AI slop checklists |
| Pure black body text | Paragraphs and headings | Moderate: appears in AI slop checklists |

### 1. Indigo and violet: the signature

The most famous AI color is the indigo to violet range. The origin story is unusually well documented. In August 2025, Tailwind CSS creator Adam Wathan posted on X: "I'd like to formally apologize for making every button in Tailwind UI `bg-indigo-500` five years ago." He acknowledged that this default had led to AI generated interfaces coming out indigo.

The mechanism people describe is simple. Tailwind's examples and templates used indigo as the primary color, and that convention is plain to see in the [Tailwind color palette documentation](https://tailwindcss.com/docs/colors). Developers copied those examples into tutorials and open source projects. Models trained on that code learned that "modern web design" and "indigo button" go together.

A word of caution: that causal chain is **plausible but untested**. Nobody has published an analysis of the training data showing how often indigo appears. The Tailwind history is fact. The idea that it is the main cause is a well supported hypothesis.

### 2. Gradients in the blue to purple range

Several design write-ups call the indigo to purple gradient the loudest tell of AI generated design. Gradient headline text, gradient "Get started" buttons and soft aurora backgrounds behind a dark hero are the usual forms. Pink to purple gradients that trended around 2020 and 2021, and blue to indigo hero looks associated with the Linear aesthetic, also feed into this pool of common patterns.

### 3. Blue as the safe default

When nobody specifies a scheme, blue wins. A 2026 study, [Biased or Personalized? The Impact of Personal Information on AI-driven Development](https://arxiv.org/abs/2607.07480), found blue was the most common color overall in AI generated websites. Participants who gave no color instructions got blue and white from ChatGPT. This is the one place where we can point to measurement instead of impressions. The sample was modest (120 personal websites coded by hand and 400 online shops), so treat it as a data point, not a universal law.

### 4. Dark mode with glow

Dark hero sections with a purple or blue glow are everywhere in AI generated SaaS pages. Part of this overlaps with the Linear style, which many designers copied. Because this pattern comes from observation, we cannot give you a frequency, but it is consistent across the sources we read.

### 5. The boring neutrals

Pure white backgrounds, pure black text and gray scales taken straight from Tailwind's slate palette show up on practitioner checklists of AI slop. They are not exciting colors, which is exactly why they are so common. They are the average of everything.

## Colors Least Used by AI (and What That Tells You)

This is the harder half of the question, because absence is harder to measure than presence. Here is what we can and cannot say.

### What was measured

In the same 2026 study, pink and black were the least frequently reported colors. The authors only reported colors with at least three examples per model, so very rare colors were excluded from the count entirely. That means the real "least used" list is longer than the study shows, and it also means those two colors still appeared, just infrequently.

### What designers observe

Advice for escaping the AI look consistently recommends colors that sit outside the indigo family. Suggested alternatives include:

- Deep greens and petrol blues
- Warm neutrals and off whites with a slight tint
- Amber and ochre
- Rose and terracotta
- Muted, earthy palettes inspired by news, hospitality, fintech or public service brands

If designers keep recommending these as the way out, it suggests they are less common in default output. But that is an inference. **Nobody has counted.**

### The reasonable summary

| Likely underused (observation, not measured) | Likely overused |
|---|---|
| Deep forest and olive greens | Indigo and violet |
| Ochre, amber, mustard | Blue 500 and 600 |
| Terracotta, rust, warm brown | Purple to pink gradients |
| Warm off whites and tinted neutrals | Pure white and slate gray |
| Muted, desaturated mid tones | Neon accents on dark backgrounds |

## When AI Picks Colors Based on Who You Are

The 2026 study added a finding that matters for anyone building products with AI. When the generator was told who the website was for, color choices shifted with the persona:

- Blue, both dark and light, was used more for men.
- Pink and purple appeared only on websites for women, and purple concentrated among young women in one model.
- Green was associated with older women in both models.

The researchers tested whether some of these differences were statistically significant, and not all were (pink, for example, was not significant for either model after correction). But the direction of the pattern is a useful warning. If you let an AI choose a palette from a persona description, you may get stereotypes back. Define your brand colors yourself, and treat persona based color choices as something to review, not accept.

## Why Does AI Pick the Same Colors?

Several explanations circulate. Here they are, graded.

1. **Tailwind defaults in training data.** Documented history, plausible effect, not directly measured.
2. **Models average toward the safe center.** Several writers describe purple gradients as the statistically safest way to look modern. This is opinion, though a reasonable one.
3. **Vague prompts produce average output.** "Make it look modern" has no color information in it, so the model falls back on its most common association. This matches what many developers report.
4. **A feedback loop.** Pages generated by AI get published, copied and eventually become more training data. This is a hypothesis, and it is a hard one to prove.
5. **Few constraints.** If you do not give brand tokens, the model invents them.

The practical lesson is the same whichever explanation is right: **the model fills any gap you leave with its most common answer.** The fix is to leave fewer gaps.

## The Accessibility Angle Nobody Mentions

Here is something we checked ourselves instead of repeating from articles. Contrast ratios for the most common AI default colors, using the [WCAG relative luminance formula](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html):

| Color | Hex (Tailwind v3) | White text contrast | Passes AA for normal text (4.5:1)? |
|---|---|---|---|
| indigo-500 | `#6366f1` | 4.47:1 | No, misses by 0.03 |
| indigo-600 | `#4f46e5` | 6.29:1 | Yes |
| violet-500 | `#8b5cf6` | 4.23:1 | No |
| blue-500 | `#3b82f6` | 3.68:1 | No |
| blue-600 | `#2563eb` | 5.17:1 | Yes |
| pink-500 | `#ec4899` | 3.53:1 | No |

So the single most famous AI button color, white text on indigo-500, sits a hair under the AA threshold for normal sized text. The shade one step darker passes comfortably. Many AI generated pages use the 500 shade, so they quietly ship contrast failures.

Large text (18pt or 14pt bold and up) only needs 3:1, which is why you often get away with it on big buttons and headlines. Body copy on those colors is where problems appear.

## How to Find AI Default Colors in Your Codebase

If you have AI generated code in your repo, this script scans for the usual suspects: stock Tailwind hex values, indigo, violet, purple and fuchsia utility classes, and gradients. We tested it against a small demo project and it flagged each default correctly.

```python
import re
import sys
from pathlib import Path

# Tailwind v3 stock swatches that show up constantly in AI generated UI
TAILWIND_TELLS = {
    "#6366f1": "indigo-500",
    "#4f46e5": "indigo-600",
    "#8b5cf6": "violet-500",
    "#7c3aed": "violet-600",
    "#a855f7": "purple-500",
    "#9333ea": "purple-600",
    "#3b82f6": "blue-500",
    "#2563eb": "blue-600",
    "#ec4899": "pink-500",
    "#db2777": "pink-600",
}

CLASS_PATTERN = re.compile(
    r"\b(?:bg|text|from|via|to|border|ring)-(?:indigo|violet|purple|fuchsia)-\d{2,3}\b"
)
GRADIENT_PATTERN = re.compile(r"\bbg-(?:gradient|linear)-to-[a-z]+\b|linear-gradient\(")
EXTS = {".html", ".css", ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte", ".astro"}


def scan(root):
    hits = {}
    for path in Path(root).rglob("*"):
        if path.suffix not in EXTS or "node_modules" in path.parts:
            continue
        text = path.read_text(errors="ignore")
        found = []
        for hex_code, name in TAILWIND_TELLS.items():
            if hex_code in text.lower():
                found.append(f"{hex_code} ({name})")
        found += sorted(set(CLASS_PATTERN.findall(text)))
        if GRADIENT_PATTERN.search(text):
            found.append("gradient")
        if found:
            hits[str(path)] = found
    return hits


if __name__ == "__main__":
    results = scan(sys.argv[1] if len(sys.argv) > 1 else ".")
    for file, items in results.items():
        print(file)
        for item in items:
            print("  -", item)
    print(f"\n{len(results)} file(s) with default looking colors")
```

Run it with `python scan_ai_colors.py ./src`. A hit is not a bug. Plenty of real brands use indigo on purpose. The point is to make you decide deliberately instead of by default.

> [!TIP] Tailwind v4 note
> Tailwind v4 changed its internal color definitions to a different color space, so a v4 project may use values that do not match these v3 hex codes exactly. Searching for the class names still works.

## How to Fix AI Generated Color Palettes

### Step 1: Define your tokens before you prompt

Write your palette as CSS variables first, then tell the AI to use only those.

```css
:root {
  --color-bg: #f6f3ec;
  --color-text: #1a1a17;
  --color-brand: #1f4d3a;
  --color-accent: #e8b931;
  --color-muted: #6b675d;
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-bg: #14130f;
    --color-text: #efeadd;
    --color-brand: #5fae8a;
    --color-accent: #e8b931;
    --color-muted: #a39f92;
  }
}
```

This sample palette is only an illustration. We checked the contrast on the light version: the text color on the background scores 15.74:1, white text on the forest green scores 9.63:1, and near black text on the amber scores 9.48:1. All pass AA easily. Check your own values before you use them.

### Step 2: Give the model a real palette, not a mood

Compare these two prompts.

**Weak:** "Build a modern SaaS landing page."

**Stronger:**

```text
Build a landing page for a bookkeeping tool for small restaurants.
Use ONLY these CSS variables: --color-bg, --color-text, --color-brand,
--color-accent, --color-muted. Do not use Tailwind's default indigo,
violet, purple or blue scales. No gradients. Solid fills only.
Body text must meet WCAG AA contrast. Keep neutrals warm, not pure
white or pure black.
```

An explicit avoid list works better than hoping the model avoids a color on its own. For a deeper look at writing instructions like this, see our guide to [writing an effective system prompt](/p/what-is-system-prompt-how-to-write-effective/).

### Step 3: Tint your neutrals

Pure gray and pure white feel generic. Add a few percent of your brand hue to your neutrals so the whole page feels like it belongs together. This single change does more for a page than swapping one accent color.

### Step 4: Pick colors from something true

Instead of asking for "a nice palette," start from your logo, your product, your physical storefront, or the feeling of your audience. A bookkeeping tool for restaurants might pull from menu paper, kitchen steel and a single warm accent. That produces a palette no one else has, because it came from your actual context.

### Step 5: Use a perceptual color space for ramps

Generate your light and dark steps in OKLCH or a similar space, so steps look evenly spaced to the eye. The [OKLCH color picker](https://oklch.com) makes this easy, and modern CSS supports `oklch()` directly.

### Step 6: Check contrast automatically

Add a contrast check to your tests or CI so a color change cannot quietly break accessibility. The [WebAIM contrast checker](https://webaim.org/resources/contrastchecker/) is a handy manual option while you design.

### Step 7: Review the full page, not just the buttons

AI defaults hide in places you do not look: focus rings, selection highlights, link hover states, shadows and dark mode variants. Search for them with the script above.

## Is Purple Actually Bad?

No. Purple is a perfectly good brand color. Many strong brands use it. The problem is never the color itself. The problem is **the default**: when your page uses indigo because a model reached for it and not because it fits your product, visitors who have seen a hundred identical pages stop noticing yours.

If purple really is your brand, make it yours. Pick an exact shade, use it as a flat fill, and combine it with warm or unexpected neutrals so it does not look like the stock swatch.

## Models Change

Everything in this article describes patterns that reporters and researchers observed up to late 2026. Models improve, and tools such as v0, Lovable and others keep adjusting their defaults. Some model makers also publish frontend style guidance that tells models to avoid purple gradients on white backgrounds, and we expect that to nudge outputs over time. Test the tool you actually use instead of assuming today's habits are permanent.

## Common Mistakes

- **Asking for "modern" or "clean"** and expecting a unique palette.
- **Accepting the first output** and shipping it unchanged.
- **Removing purple but keeping everything else generic**, such as pure white backgrounds and slate grays.
- **Skipping the contrast check** on default shades.
- **Letting AI pick colors based on a persona** without questioning stereotypes.
- **Treating AI color statistics as facts.** Most of what you read online is observation, including some of this article.
- **Hardcoding hex values everywhere** so a palette change means hunting through files.

If you want to go further on getting less generic results, see our guide on [how to avoid AI slop in website design](/p/how-to-de-ai-slop-website-design/), our explainer on [design system files for AI agents](/p/what-is-getdesign-md-ai-agents-design-system/) and our roundup of [UI and UX design inspiration resources](/p/best-ui-ux-design-inspiration-resources/). If you are also choosing icons, our [Lucide vs Font Awesome comparison](/p/lucide-vs-font-awesome/) covers another place defaults creep in.

## FAQ

### What color does AI use most?

AI generated websites most often use blue, indigo and violet, frequently as gradients. A 2026 study found blue was the most common color overall, and designers widely report indigo to purple gradients as the most recognizable AI design tell.

### Why does AI love purple and indigo?

The best documented explanation is Tailwind CSS, whose demos used `bg-indigo-500` as the default button color. Code that copied it likely entered training data. This is a plausible cause, but nobody has measured it directly.

### What colors does AI use least?

In one 2026 study, pink and black were the least frequent colors reported. Designers also observe that warm and earthy colors such as deep green, ochre, amber and terracotta are rare in default AI output, though that has not been counted.

### Why do AI generated websites all look the same?

When a prompt gives no specific palette, models fall back on their most common associations, such as indigo buttons, gradients, dark hero sections and Inter style fonts. Giving the model explicit color tokens and an avoid list produces more varied results.

### Is indigo-500 accessible with white text?

Not quite. Tailwind v3 indigo-500 (`#6366f1`) with white text has a contrast ratio of about 4.47:1, just below the 4.5:1 WCAG AA requirement for normal text. Indigo-600 passes at about 6.29:1.

### How do I stop AI from using purple gradients?

Define your brand colors as CSS variables, tell the model to use only those, and add an explicit instruction to avoid Tailwind's indigo, violet and purple scales and gradients. Specific constraints work better than asking it to be unique.

## Key Takeaways

- **Blue, indigo, violet and purple** are the colors most associated with AI generated interfaces, especially as gradients.
- The best documented cause is **Tailwind's `bg-indigo-500` default**, which its creator publicly apologized for in August 2025. The idea that it is the main cause is a hypothesis, not a measured result.
- A 2026 study found **blue was the most common color** in AI generated websites and **pink and black were the least frequent** among reported colors.
- Designers observe that **deep greens, ochre, amber, terracotta and warm off whites** are rare in default output, but nobody has published counts.
- White text on **indigo-500 scores 4.47:1**, just under the 4.5:1 WCAG AA threshold. The 600 shade passes.
- AI may **tie colors to persona stereotypes**. Define brand colors yourself.
- The fix is **fewer gaps**: set CSS variable tokens, give an explicit avoid list, tint your neutrals and check contrast automatically.
- Purple is not the enemy. **Unchosen defaults are.**

## Conclusion

If you take one thing from this: the colors most used by AI are not a mystery, and they are not permanent. They are the visible trace of a few defaults, repeated often enough to become a house style. That means you can change them with a handful of decisions, not a redesign.

Start with tokens, write an explicit avoid list, tint your neutrals, and run the contrast check before you ship. Your page does not need to avoid purple. It needs to choose its colors on purpose.

If you want to dig deeper into the surrounding craft, our [Contributor Guide](/contribute/) explains how Dev9b handles sourcing and reviews, and the [Editorial Policy](/editorial-policy/) spells out our standards for evidence like the grades used here. Teams like F9XR treat AI output the same way: a fast first draft, then human decisions about what actually represents the product.

*This guide was researched and drafted with the assistance of an AI coding assistant, then reviewed by the F9XR Review Board before publishing.*

---

*Sources: Adam Wathan's August 2025 apology as reported by [aihola](https://aihola.com/article/vibe-coding-purple-landing-pages) and [925 Studios](https://www.925studios.co/blog/ai-slop-design-tells); the 2026 study "Biased or Personalized? The Impact of Personal Information on AI-driven Development" on [arXiv](https://arxiv.org/pdf/2607.07480); design analysis from [Honello](https://honello.com/blog/why-ai-websites-have-purple-gradients), [Sailop](https://www.sailop.com/blog/ai-slop-encyclopedia), [prg.sh](https://prg.sh/ramblings/Why-Your-AI-Keeps-Building-the-Same-Purple-Gradient-Website) and [DEV Community](https://dev.to/jaainil/ai-purple-problem-make-your-ui-unmistakable-3ono). Contrast ratios were calculated with the WCAG relative luminance formula.*
