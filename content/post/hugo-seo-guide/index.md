---
title: "The Hugo SEO Checklist (From a Real Site Audit)"
description: "A working Hugo SEO checklist: metadata, JSON-LD, sitemaps, and Core Web Vitals — every item verified on a live Hugo site."
slug: hugo-seo-guide
date: 2026-09-05
image: cover.png
author: F9XR Team
keywords:
    - Hugo SEO
    - SEO checklist
    - static site SEO
    - structured data
    - technical SEO
categories:
    - Tutorials
tags:
    - seo
    - hugo
    - f9xr
draft: false
math: false
faq:
    - question: "Does Hugo need an SEO plugin?"
      answer: "No. Hugo ships everything needed — metadata templates, sitemap, RSS feeds, robots.txt support — and structured data is a small template partial. A plugin adds convenience, not capability."
    - question: "What is the most impactful single Hugo SEO fix?"
      answer: "A correct title hierarchy. Keep one H1 per page (the page title) and ensure that title contains your target keyword before touching anything else."
    - question: "Are duplicate title and description tags harmful?"
      answer: "Duplicate descriptions across similar pages waste crawl and lower click-through. Generate a unique description per page — terms, sections, and posts should each have their own."
---
Most SEO advice for static sites is recycled from 2010 and wrong for Hugo. Tell someone "install a plugin" and they will spend an hour looking for something that does not exist. The truth is better: Hugo generates most of your technical SEO for free, and the rest fits in a handful of template partials.

This checklist comes straight from a five-pass audit of a live Hugo site — the one you are reading. Every item below is something we verified then fixed, with the exact change that worked.

<!--more-->

## The Minimum Viable Hugo SEO Setup

Run through these before you spend time on anything else. They cover 80% of the outcome.

- [ ] **One H1 per page, holding the keyword.** On posts, the title should render as the page's H1. If your theme prints the article title as an H2, override it — this was the single biggest finding in our audit.
- [ ] **Unique meta description per page.** `description` in front matter. Keep it under 160 characters and include the target keyword.
- [ ] **Canonical tags on.** Hugo emits canonicals automatically from `.Permalink`.
- [ ] **Sitemap present.** Hugo's built-in `sitemap.xml` needs no configuration. Confirm it lists every indexable URL.
- [ ] **RSS feeds present.** `index.xml` ships by default; extra feeds are just output formats in `config.toml`.
- [ ] **robots.txt correct.** Respect the `baseURL` path — a sitemap reference that includes the full path is what allows the sitemap to actually be found.

## Metadata That Google Actually Reads

| Element | Value | How Hugo provides it |
|---|---|---|
| Title | `< 60` chars, keyword near the front | `.Title` per page |
| Description | `< 160` chars, unique per page | `description` front matter |
| Canonical | Absolute URL | built-in |
| Open Graph | title, description, image, type | theme partials |
| Twitter card | summary / summary_large_image | theme partials |
| Author | named person or organization | `author` front matter |

Two gotchas from our run: `og:type` defaults to `article` on every page in many themes — restrict it to actual posts. And `og:image` needs explicit `width`/`height` or social scrapers resize the image on their own.

## Structured Data Without a Plugin

Search engines reward explicit structure. On Hugo you write it once in a partial and it applies to every page:

- **Organization** — name, logo, social `sameAs` links. Every page should emit it.
- **BreadcrumbList** — itemListElement with position + URL. Cheap to emit on every page.
- **TechArticle / Article** — headline, description, image, dates, author, publisher.
- **FAQPage** — only when the questions are visible on the page, or Google flags it as spam. Wire it to front matter so only posts with a real FAQ section emit it.

We verified every `ld+json` block on this site as valid JSON-LD. Hugo's `jsonify` outputs JSON directly; pipe it through `safeJS` when embedding inside a `<script>` tag so the HTML template engine does not escape your quotes.

## Core Web Vitals: The Stuff Nobody Checks

Static sites are fast by default, then themes quietly undo it.

- **LCP image.** If your hero image uses `loading="lazy"`, the largest element on the page waits to load. Set `loading="eager"` and `fetchpriority="high"` on the article hero only — keep lazy loading for everything below the fold.
- **Self-hosted fonts.** Two `<link rel="preconnect">` tags before the stylesheet cost almost nothing and cut font latency.
- **No render-blocking analytics.** Third-party scripts (comment widgets, chat, ad providers) are the main votal leak on an otherwise-light page.
- **Image dimensions always.** Missing `width`/`height` on images causes layout shift and hurts CLS.

## Site-Health Checks That Compound

- **No placeholder links.** We found `example.com` links in a published guide. A single dead domain in an "authoritative" article damages trust. Mine your content for defaults.
- **`enableGitInfo = true`.** Hugo pulls commit dates into `Date`/`Lastmod`, which keeps `dateModified` honest without manual edits.
- **Turn off pagination aliases.** `[pagination] disableAliases = true` removes a dozen duplicate `/page/1/` URLs that dilute your crawl.
- **Unique taxonomy titles.** Raw slugs become titles like "Vscode" or "Ai-Tools". Give tags `_index.md` files with real titles, or override the title partial.

## Key Takeaways

- Hugo needs no SEO plugin; templates and front matter cover everything.
- Fix the H1 hierarchy before adding any other SEO feature.
- Structured data is a handful of `ld+json` partials — keep FAQPage honest or leave it out.
- LCP, fonts, and dimensions matter more on a static site than most guides admit.

## Conclusion

Technical SEO on Hugo is not a plugin — it is a short checklist, verified. The audit that produced this list is the reason this site ships the exact patterns above, from H1 behavior to `fetchpriority`. To stand up your own Hugo site first, start with our [GitHub Pages setup guide](/p/hugo-github-pages-setup/), then reuse this checklist on it. If you find a pattern we should cover next, the [contributor guide](/contribute/) is open, and everything here is reviewed against the [editorial policy](/editorial-policy/).