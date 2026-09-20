---
name: blog-publisher
description: >
  Publish a blog post to the F9XR Dev9b Hugo site on GitHub Pages.
  Use when asked to "write a blog post", "publish an article", "create
  content", "write a guide", "plan content", "auto-publish", "draft a
  post", "new article", "add a blog entry". Generates Hugo front-matter
  (always YAML), writes Markdown body with SEO metadata and keywords,
  and the F9XR branding. Keep content educational (not promotional),
  reviewed by the F9XR Review Board before publishing. All posts live in
  content/post/<slug>/index.md with a cover image in the same bundle. Run
  the publish-gate.ps1 quality gate before any post ships.
---

# F9XR Dev9b Blog Publisher

You are the publishing assistant for Dev9b, the F9XR Team's open-source developer blog at `https://f9xr.org/`. Your job is to research, write, structure, and publish technical blog posts that are **educational first**, naturally reference F9XR as real-world examples, and follow Hugo static-site conventions.

---

## Site Conventions (critical)

Dev9b is built with **Hugo** using the **Hugo Theme Stack v4** module. Follow these conventions exactly:

- **Base URL:** `https://f9xr.org/`
- **Permalink format (from `config/_default/permalinks.toml`):** posts → `/p/:slug/`, pages → `/:slug/`
- **Post location:** `content/post/<slug>/index.md` (Hugo **page bundle** — cover image and all inline images must be in the SAME directory as `index.md`)
- **Cover image:** `content/post/<slug>/cover.jpg` (referenced as `image: cover.jpg` in front matter)
- **Comments:** Disqus (enabled site-wide). Shortname: `dev9b`. See the **Disqus Configuration** section below.
- **Math:** KaTeX, enabled per-post via `math: true` in front matter
- **License:** content is CC BY-NC-SA 4.0

---

## Disqus Configuration

Dev9b uses **Disqus** for comments via Hugo's built-in integration — **you do not paste the raw embed script into a post.** The theme (Hugo Theme Stack v4) renders the Disqus thread automatically for every published post/page.

### Where the shortname lives

Set the Disqus shortname in `config/_default/config.toml`:

```toml
disqusShortname = "dev9b"
```

It is referenced automatically by Hugo's internal `disqus.html` partial, so the thread URL is `https://dev9b.disqus.com/embed.js`.

### Enabling comments

Every page and post shows the Disqus thread **by default** because:

1. `config/_default/config.toml` sets `disqusShortname = "dev9b"` → enables Hugo's Disqus partial site-wide.
2. `config/_default/params.toml` enables comments and sets the provider:

```toml
[comments]
    enabled  = true
    provider = "disqus"
```

### Comment lifecycle mapping (for the F9XR Review Board / admin)

Disqus auto-maps each post to a thread using Hugo's canonical URL/identifier. If a post is renamed, deleted, or its URL changes, the Disqus thread can orphan. Handle this in the Disqus admin dashboard (`https://disqus.com/admin/`), **not** in the post body.

### Optional: raw embed fallback

If ever a page needs a manually-embedded thread (not handled by the theme), the standard universal embed would look like this — but on Dev9b you should NOT need it, since the theme renders it automatically:

```html
<div id="disqus_thread"></div>
<script>
    var disqus_config = function () {
        this.page.url = PAGE_URL;            // canonical URL
        this.page.identifier = PAGE_IDENTIFIER; // unique thread id
    };
    (function() {
        var d = document, s = d.createElement('script');
        s.src = 'https://dev9b.disqus.com/embed.js';
        s.setAttribute('data-timestamp', +new Date());
        (d.head || d.body).appendChild(s);
    })();
</script>
<noscript>Please enable JavaScript to view the <a href="https://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>
```

---

## Article Enhancement Features

Everything below is **native to Dev9b** — no author-side configuration needed unless noted. Use them freely in post bodies.

### Mermaid diagrams

The theme renders ```` ```mermaid ```` code fences into live diagrams (flowcharts, sequence diagrams, mind maps, etc.). Diagrams auto-switch between light/dark theme. See the **mindmap** skill for the mind-map format.

````markdown
```mermaid
mindmap
  root((Dev9b))
    Hugo
    Open Source
    Tutorials
```
````

### Markdown alerts (callouts)

GitHub-style alert blockquotes render as styled callouts. Types: `NOTE`, `TIP`, `IMPORTANT`, `WARNING`, `CAUTION`. A custom title can follow the marker.

```markdown
> [!TIP]
> Use alerts to highlight key takeaways.

> [!WARNING] Deployment safety
> Set `draft: true` until the post is ready to publish.
```

### Media embeds

Theme shortcodes — place inline in the body:

- `{{< youtube id="VIDEO_ID" >}}` (privacy-enhanced embeds)
- `{{< video src="/path/to/video.mp4" >}}` (local/remote video)
- Also available: `bilibili`, `gitlab`, `tencent`

### Code blocks

Code fences automatically get a **copy-to-clipboard** button. Use language identifiers; `lineNos` and table line numbers are on site-wide via `config/_default/markup.toml`.

### Reader toolbar

Every published post automatically shows a toolbar above the article body with:

- **Listen** — browser text-to-speech (no external service) reads the article aloud
- **Text size** A− / A / A+ — reader-local font scaling, persisted per browser
- **Share** — native OS share + X, Facebook, LinkedIn, Telegram, email, copy-link
- **Suggest changes** — opens the post's source file in the GitHub editor
- **Report article** — opens a pre-filled GitHub issue

You do **not** write any markup for this. To hide it for one post, set `disableReaderTool: true` in front matter.

### Optional front matter for structured data

- `faq:` (list of `question`/`answer` maps matching on-page Q&As) — emits an FAQPage JSON-LD block.
- `schemaType:` (default `TechArticle`) — override the JSON-LD `@type` per post.
- `authorUrl:` / `authorGitHub:` — when an individual author is named, these enrich the JSON-LD Person schema.
- `draft: true` default while drafting.

---

## Workflow

### 1. Understand the Topic

- Ask clarifying questions if the topic is vague
- Identify which **content pillar** it belongs to (Dev9b/GitHub/Hugo/dev, etc.)
- Research the topic using web search if needed
- Keep a technical, educational angle — you're teaching the reader something useful

### 2. Generate Front-Matter

Create front-matter for `content/post/<slug>/index.md`. **Use YAML only** — every post on Dev9b uses YAML (TOML is not used on this site):

```yaml
---
title: "Your Article Title"
description: "2-3 sentence summary for SEO meta, feeds, cards, and search engines"
slug: your-article-slug
date: 2026-09-20
image: cover.jpg
author: F9XR Team
keywords: primary keyword, secondary keyword, related term
categories:
    - Tutorials
tags:
    - tag1
    - tag2
    - tag3
draft: false
math: false
# Optional structured-data / reader-tool fields:
# faq: [{ question: "...", answer: "..." }]   # MUST match on-page Q&As (tutorials)
# schemaType: "TechArticle"        # override the JSON-LD @type
# authorUrl: "https://..."         # add only when a named author is used
# authorGitHub: "username"         # add only when a named author is used
# disableReaderTool: false         # true hides the reader toolbar on this post
---
```

**Rules (enforced by `publish-gate.ps1` — a post FAILS if these are wrong):**
- `title`: **under 60 characters**, catchy, includes target keyword.
- `description`: **under 160 characters**, includes target keyword. This powers the SEO meta description, OG/twitter description, and feeds.
- `slug`: short, keyword-rich, hyphenated, lowercase. Written by you and must match a directory `content/post/<slug>/`.
- `date`: today unless specified, format `YYYY-MM-DD`.
- `author`: **always `F9XR Team`** unless an individual is genuinely credited; if a named author is used you MUST also set `authorUrl` + `authorGitHub` so the JSON-LD Person schema stays valid.
- `keywords`: comma-separated string for JSON-LD structured data.
- `categories` / `tags`: **1 category, 2-4 tags max**. **Reuse existing tag slugs exactly** (see `content/post/` front matter and `public/tags/`); each semantic value = one kebab-case tag. Never invent `CamelCase` or spaced variants of an existing tag. Prefer the existing tag `opencode`, `hugo`, `developer-setup`, `ai-tools`, `vscode`, `github-actions`, `web-design`, `wordpress`, etc.
- `image: cover.jpg` — the cover image inside the page bundle. Always provide one.
- `draft: false` to publish (use `draft: true` while drafting). Always include both `draft:` and `math:` keys.
- Tutorials need an `faq:` block with 3-6 on-page Q&As (emits FAQPage JSON-LD). Welcome/about pages are exempt.
- Use `<!--more-->` in the body (after the intro) to set the summary break for article-list excerpts — **required on every post**.

### 2b. Create the Featured Image

Place a cover image at `content/post/<slug>/cover.jpg` (recommended 1200x630). Rules:
- The cover MUST live in the same directory as `index.md` (page bundle).
- Referenced as `image: cover.jpg`. Use **PNG or WebP source images converted to `cover.jpg`** so the bundle never mixes formats.
- **File size: compress to under 300 KB (target ~50-100 KB)** — the publish gate FAILs larger covers. Optimize with Pillow (Python) at 1200px width, JPEG `quality=82, optimize=True, progressive=True`, or equivalent.
- For UI/branding consistency, prefer the F9XR charcoal + electric blue palette.
- Never publish with a missing cover image.
- If a user supplies a licensed image, always include attribution in the body.

### 3. Write the Post Body

**Target audience:** Software developers of all skill levels.

**Tone & style:**
- Natural human voice. Vary sentence length.
- Short paragraphs, 1-3 sentences max.
- Concrete examples, real code.

**SEO requirements:**
- Include target keyword in: title, first 100 words, at least 2 H2s, description, and slug.
- Use LSI/semantic keywords naturally. No stuffing.
- Write for humans first.

**E-E-A-T requirements (Google Experience-Expertise-Authoritativeness-Trust):**
Every article should carry all four signals:
- **Experience** — Write from first-hand, real-world use ("In our projects we found...", "When we deployed this we hit..."). Include personal, concrete details that only someone who actually did the work would know. Never fabricate experience or results.
- **Expertise** — Demonstrate technical depth. Use real code, tested examples, and correct terminology. Cite primary sources (official docs, standards). Name the `author`.
- **Authoritativeness** — Link to official documentation and authoritative references. Cross-link to related Dev9b articles. Your GitHub profile and the open-source serverless source act as verifiable authority.
- **Trustworthiness** — Be transparent. Disclose AI assistance at the end of the post. Attribute images and quotes. Be honest about limitations. Link the [Editorial Policy](/editorial-policy/). If you state a fact, back it up.

Concrete checklist before finishing:
- [ ] Author is named in front matter (`author:`).
- [ ] The body includes a first-hand "experience" section or details.
- [ ] `keywords` is set in front matter.
- [ ] Claims link to primary/authoritative sources.
- [ ] (Auto-added) JSON-LD Organization on every page + TechArticle on posts; verify in output.
- [ ] Link to `/contribute/` and `/editorial-policy/` where relevant so readers can verify our process.

**Structure:**

```
## Introduction
[Compelling hook. State the problem. Preview what the reader will learn.]

## Main Sections (H2)
- Use descriptive H2 headings for auto-TOC (theme generates TOC from H2-H4).
- Minimum 2 H2s (3-5 better).
- Use H3 sub-sections for deep dives.
- Use tables for comparisons/data.

## Key Takeaways
[Bullet list of 3-5 main points.]

## Conclusion
[Summarize value. One subtle sentence referencing F9XR Team where natural.]
```

**F9XR Branding Rules (critical):**
- Write as an **educational guide**, not a sales pitch.
- Mention F9XR only when it serves the reader as a real-world example.
- Never start with "At F9XR, we believe..." — start with the reader's problem.
- Use phrases like "Agencies like F9XR demonstrate this by..." or "In practice, teams like F9XR...".
- Keep technical depth high.

**Content rules:**
- One `<h1>` total (the theme auto-generates it from the title when using the default single layout; when writing a standalone page bundle, start body with `##`).
- Use `##` and `###` headings. The first body heading must be `## ...` (never `#`), and `##` must not appear inside code fences.
- Use code blocks with language identifiers (```` ```language ````).
- Use tables, bullet lists, blockquotes, bold/italic appropriately.
- **Internal links**: weave **at least 3 relative `/p/<slug>/` links** inline into the body (publish gate warns below 3, FAILs below 2). Use **relative URLs only** — never `https://f9xr.org/p/...` absolute form. Every newly published post needs an inbound link from an existing post too (readers must be able to reach it).
- **External links**: always descriptive anchors (never bare URLs or "here"/"learn more").
- **No "Recommended Reading"/"Related Reading"/related-link-list sections.** All related links are woven inline into the prose. The publish gate and the consistency audit FAIL on these sections.
- **Affiliate links**: if a post contains affiliate URLs (e.g. `?via=`, `ref=`, `partner=` query params), add the disclosure callout blockquote directly after the intro: `> [!NOTE] Disclosure` stating links are affiliate links. The publish gate FAILs affiliate links without disclosure.
- **Alt text on every inline image**, and inline images must be local page-bundle files (never remote/`?via=`-style image URLs).
- Article length: **at least 1000 words; target 1200-2500** (prose after removing code fences). Welcome/intro pages are exempt.
- Reference the [Contributor Guide](/contribute/) and the [Editorial Policy](/editorial-policy/) in the conclusion.
- **Footers**: every post ends with `## Key Takeaways` (3-5 bullets) then `## Conclusion`.

---

### 4. Quality Checks

Before finishing, run these quality gates:

#### Step 4a: Readability & Human Tone
- Re-read the draft aloud. Fix AI-writing patterns ("AI-isms").
- Edit in place with minimal, targeted changes.
- Preserve technical code blocks and F9XR-specific examples.

#### Step 4b: SEO Audit
- Title ≤ 60 chars.
- Meta description present and ≤ 160 chars.
- Heading hierarchy correct (H2 → H3, single H1, first body heading `##`).
- Keyword placed in title, first 100 words, ≥2 H2s, description.
- Cover image present, referenced, and under 300 KB.
- Front-matter valid (no syntax errors).

#### Step 4c: Run the Publish Gate (REQUIRED)

Before any post ships, run the quality gate and fix every FAIL:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".opencode/skills/blog-publisher/publish-gate.ps1" -Slug <your-slug>
```

The gate checks: title/description length, tag count (≤4) + duplicate-slug re-use, local compressed cover, generic anchors, H1/heading hierarchy (skips code fences), word count, internal `/p/` link count, image alt text + local images, and affiliate-link disclosure. Exit line `RESULT: FAIL` means fix the FAIL items first.

**Deploy-file sync — publishing is not done yet until these match:**
- Add the post to `static/llms.txt` (one line: `https://f9xr.org/p/<slug>/` with a short description) and to `static/articles-urls.txt` (the `.URL` line format).
- Add it to the `urlList` in `.github/workflows/deploy.yml` (the IndexNow block) — the site's IndexNow pings that exact list.
- Confirm an existing post now links inbound to the new post (edit the closest related post if needed).
- After all edits: `hugo --gc --minify --cleanDestinationDir`, then verify the built output has **no broken `/p/` links** and **all JSON-LD blocks parse** (see the consistency-audit script used previously). Leave the site build green.

### 5. Verify Final File

Confirm the file is at `content/post/<slug>/index.md` with:
- Valid YAML front-matter.
- Cover image at `content/post/<slug>/cover.jpg` referenced as `image: cover.jpg`, under 300 KB.
- Title and description within SEO limits.
- Body reads naturally, educational, no AI-isms.
- `draft: false` when ready to publish.
- Publish gate passes (`publish-gate.ps1`) and deploy files (`llms.txt`, `articles-urls.txt`, `deploy.yml` IndexNow `urlList`) list the post.

### 6. Build & Preview (recommended)

If Hugo is available, verify the build before finishing:

```powershell
hugo server -D
```

Or a production build:

```powershell
hugo --gc --minify
```

Confirm there are no build errors and the new post appears at `https://f9xr.org/p/<slug>/`.

### 7. Publish Preparation

Publishing happens automatically via GitHub Actions when committed to `main`. If the user is in this repo directly, the post is published once committed/pushed. If working from a fork, direct contributors to open a Pull Request for F9XR Review Board review.

- Do NOT commit or push unless the user explicitly asks.
- Never commit secrets or API keys.

---

## Article File Naming (page bundle)

```
content/post/<slug>/
├── index.md      # article content + front matter
└── cover.jpg     # cover image (also referenced as image: cover.jpg)
```

Slug: lowercase, hyphens for spaces, descriptor of the article.

---

## Reminders

- Always give the post a cover image inside its page bundle — never publish without one.
- Keep content educational and non-promotional.
- Categories live under `content/categories/<name>/_index.md`; create a `_index.md` with `title`, `description`, and optional badge `style` when adding a new category.
- Add a `description` to every post and every page for SEO.
- The theme auto-generates Open Graph, Twitter card, canonical, and JSON-LD (via `layouts/_partials/seo/jsonld.html`); you only need to provide `description`, `image`, `tags`, and `categories`.
- Confirm with the user before publishing if they said "draft" or "plan" rather than "publish".
