# Dev9b SEO, GEO and AI Visibility Audit

Open-source developer blog by the F9XR Team, published at f9xr.org/dev9b. Competitor named by the client: dev.to.

**Audit date** 22 Nov 2026\
**Method** sampled fetch of 12 URLs, not a full crawl\
**Scores** estimated, see Overview

## Executive summary

Dev9b is a well-structured Hugo blog with solid on-page basics: self-canonical pages, answer-ready post layouts (key takeaways, FAQ, tables), a public editorial policy and visible affiliate disclosure. The confirmed problems are mostly consistency problems. The site mixes http and https in the signals search engines read, carries placeholder and thin index-eligible pages, and presents its authorship as an anonymous team.

The headline score covers only the parts that could be tested ( of the weighting). Backlinks, AI platform visibility and Core Web Vitals could not be measured, so they are excluded rather than guessed.

## Issue counts

### Issue severity distribution

Counts come from the confirmed register on the next tab. No critical issue was found in the sampled pages.

### Score by category (estimated)

Percent of category weight earned. Judgement-based, not tool-measured. Hatched categories were not tested.

## Scoring method

Local SEO is not applicable (global developer blog with no location target), so its 5 points are removed and the remaining weights are used as given, totalling 95. Overall = points earned divided by tested weight. Treating every untested area as zero would give .

## Five biggest problems

## Five biggest growth opportunities

## Final error register

Every row was observed in fetched page source or file content. Items marked Potential could not be fully confirmed with the tools available and are listed separately.

## Technical SEO

**Not tested:** Core Web Vitals and Lighthouse (the PageSpeed API request returned a client error), HTTP status codes and headers, X-Robots-Tag, redirect behaviour, a site-wide broken link crawl and mobile rendering. No lab or field performance numbers are reported.

| Check | Result | Evidence |
| --- | --- | --- |
| Robots meta | Pass | Every inspected page declares index, follow with max-snippet:-1 and max-image-preview:large. |
| robots.txt reachable | Pass | Allows all crawlers by default and blocks only named training bots. See E05 for contradictory signals. |
| Sitemap reachable | Pass | `/dev9b/sitemap.xml` returns a valid urlset with posts, pages, tags and categories. |
| Sitemap declared | Gap | Root robots.txt lists three other sitemaps, none for /dev9b. See E02. |
| Canonical tags | Mixed | Homepage and posts canonicalise to https. Tag and category pages canonicalise to http. See E01. |
| RSS feed | Pass | `/dev9b/index.xml` is valid RSS 2.0 with full content, but item links use http. |
| Pagination | Observed | Homepage links pages 2 to 9. Canonical and rel handling on those pages was not inspected. |
| Breadcrumbs | Observed | Visible on posts. On pages the trail includes a "Page" step linking to `/dev9b/page/`, which was not fetched. |
| Structured data | Not validated | JSON-LD exists on at least one post (author, headline, sameAs links seen in a search excerpt). @type values and validity were not verified. |
| JavaScript rendering | Low risk | Static Hugo output; content is in the HTML. Disqus loads only on user action. |

### Sitemap and index-eligible page pattern

The blog sitemap mixes about 90 post URLs with a large set of tag URLs at priority 0.5, plus the placeholder pages `/categories/example-category/` and `/p/hello-world/`. The tag `/tags/seo/` lists four posts and carries no text beyond a one-line description. Whether Google indexes these cannot be stated without Search Console data.

## On-page SEO and content

| Element | Observation | Status |
| --- | --- | --- |
| Title tags | Descriptive, roughly 40 to 50 characters, keyword first ("Deploy Hermes Agent on Hostinger VPS Fast"). | Good |
| Meta descriptions | Unique per page, benefit-led, about 150 to 170 characters on posts. | Good |
| Headings | One H1, clear H2/H3 ladder, question-style H3s in FAQs, table of contents with anchors. | Good |
| Internal links | Contextual links between related posts in the body (for example Hermes to Nod and Freebuff) plus a related-articles block. | Good |
| Images | Cover image per post with descriptive alt text on the homepage cards. Per-image alt inside posts not sampled. | Partial |
| Keywords meta | Present but malformed, with empty entries between split words. Ignored by Google. See E11. | Low |
| Homepage copy | The homepage is a post feed with a tagline and no descriptive text about topics covered. | Opportunity |

### E-E-A-T signals that are observable

**Present**

- Editorial policy with review steps, corrections process and independence statement.
- Affiliate disclosure at the top of the Hermes and Nod posts.
- Public GitHub repository, issue link and "Suggest changes" link on every post.
- Last-updated date shown on posts.
- Code described as tested; the trading-bot post states test scope and limits.

**Gaps**

- Byline is "F9XR Team" on every post. The team page names no individuals or credentials.
- A syndicated copy on dev.to credits a named co-author, which the origin site does not show.
- The editorial policy promises an AI-assistance line on posts; the Hermes post text has none.
- Few first-party screenshots or run logs seen in sampled text.

No E-E-A-T score is assigned. The list above is what a reader or reviewer can see.

## GEO and AEO readiness

Assessment of how easily the content can be extracted and attributed. Nothing here is a prediction of AI Overview or citation placement.

| Factor | Finding | Rating |
| --- | --- | --- |
| Direct answers | Posts open with context, then a Key Takeaways list. The Lucide vs Font Awesome post has a "Quick Answer" block under its first H2. The Hermes post does not. | Inconsistent |
| Question-based headings | FAQ sections with six to nine question headings and one-paragraph answers on both sampled posts. | Strong |
| Tables and steps | Plan comparison tables, troubleshooting tables, numbered steps. | Strong |
| Source attribution | Lucide post links official sites and repositories. Hermes post says its advice matches "official" notes without linking them. | Inconsistent |
| Original evidence | One research-style post (AI colour usage) and an experience claim in the trading-bot post. Most posts summarise third-party tools. | Limited |
| Entity clarity | Brand appears as "Dev9b", "F9XR's Dev9b", "F9XR Team" and "F9XR". Organisation JSON-LD with sameAs links exists on at least one post. | Fixable |
| AI crawler access | Training bots (GPTBot, ClaudeBot, Google-Extended and others) are blocked. Search-oriented bots such as OAI-SearchBot and PerplexityBot are not listed, so default Allow applies. | Search allowed |

### Recommended content patterns

| Weakness | Improvement | Target |
| --- | --- | --- |
| No short answer at the top of how-to posts | Add a two-sentence answer block: what it is, what it needs, how long it takes. | `/p/how-to-set-hermes-agent-on-hostinger-vps/` |
| Claims without a link | Add a "Sources" list linking vendor docs next to each factual claim and a "Tested on" line with date and version. | All tutorials |
| Version-sensitive facts | Show "Verified on" date near plan specs and CLI commands so extractors and readers can judge freshness. | Hermes, Nod, Astro, Hugo posts |
| Anonymous authorship | Named author block with Person schema and a link to profile pages. | Every post |

## AI visibility

**Not tested.** No live access to ChatGPT, Perplexity, Gemini, Google AI Overviews or Microsoft Copilot was available. No mention, citation or competitor result is reported for those platforms.

| Platform | Brand mention | Website citation | Competitor visibility | Status |
| --- | --- | --- | --- | --- |
| ChatGPT | Not verified | None tested | Not tested | Not tested |
| Perplexity | Not verified | None tested | Not tested | Not tested |
| Gemini | Not verified | None tested | Not tested | Not tested |
| Google AI Overviews | Not verified | None tested | Not tested | Not tested |
| Microsoft Copilot | Not verified | None tested | Not tested | Not tested |

### Related observation from classic web search (not an AI platform test)

A web search for the brand returned the GitHub repository, one f9xr.org post, and about seven dev.to pages from the F9XR organisation account. The dev.to copies state "Originally published at f9xr.org" and the one inspected canonicalises to f9xr.org. This is a small sample and says nothing about rankings, but it shows that third-party copies are easy for retrieval systems to find.

### Research plan

Run each prompt monthly on every platform, record whether the brand is named (mention), whether an f9xr.org URL is linked (citation), and which other domains are cited (third-party). Log the date, platform, location and model setting.

| Intent | Prompt |
| --- | --- |
| Informational | How do I deploy Hermes Agent on a Hostinger VPS? |
| Informational | What is the difference between Lucide and Font Awesome? |
| Problem-solving | How do I set up Cloudflare Email Routing to send as Gmail? |
| Problem-solving | How do I point a GitHub Pages site at a custom domain on Cloudflare? |
| Comparison | OpenCode vs Cursor for AI coding |
| Comparison | Hermes Agent vs Nod agent self-hosting |
| Commercial | Best blogging sites for developers |
| Commercial | Free subdomains for developers |
| Brand | What is Dev9b by F9XR? |
| Brand | Is F9XR Dev9b a reliable source for tutorials? |
| Alternatives | Alternatives to dev.to for publishing developer articles |
| Transactional | Where can I submit an open-source developer article? |

Local-intent prompts are omitted because the site has no location target.

## Off-page and backlinks

**Not tested.** No Ahrefs, Semrush, Majestic or Search Console access. Referring domains, anchors, link quality and link gaps are unavailable, so no numbers are shown.

### Link-building direction (no metrics behind it)

- Earn editorial links with original data posts, since the AI colour-usage article is the closest asset the site has to citable research.
- Submit tools and posts to relevant open-source newsletters and curated lists where the covered project is listed. Check each project's contribution rules first.
- Look for unlinked mentions of the projects Dev9b documents (Hermes, Nod, Freebuff, OpenCode) and notify maintainers when a guide could be linked from their docs.
- Do not rely on directory or forum-posting lists for links; they carry little editorial value.

## Competitor intelligence

Only dev.to was named and inspected. dev.to is a user-generated community platform and also a distribution channel for Dev9b, so it is not a like-for-like organic competitor. Other competitors should be chosen from real SERP overlap once Search Console or a rank tracker is available.

| Dimension | Dev9b | dev.to |
| --- | --- | --- |
| Model | Single-brand Hugo blog, open-source repo | Open community on Forem with many authors |
| Content scope | AI agents, dev infrastructure, static sites, tooling guides | Broad across all developer topics |
| Authorship | Team byline only | Named profiles and organisation pages |
| Canonical handling of Dev9b copies | Origin is f9xr.org | Inspected copy canonicalises to f9xr.org |
| Backlink profile | Not measured | Not measured |
| Topical authority | Cluster depth visible in tags, not measured in rankings | Not measured |
| AI citations | Not tested | Not tested |

### What Dev9b can do better than a general platform

- Tested, versioned setup guides with a visible "verified on" date.
- Opinionated comparison pages between tools it has already documented.
- Open-source review trail on GitHub that a platform feed cannot offer.

Candidate organic competitors to validate with SERP data (unverified guesses): Hashnode, freeCodeCamp, DigitalOcean tutorials.

## Keyword and content opportunities

**No keyword tool was available.** Search volume and difficulty are unavailable and none are shown. Opportunities below come from the site's own topic clusters.

| Cluster | Existing evidence | Action | Proposed URL |
| --- | --- | --- | --- |
| Self-hosted AI agents | Hermes, Nod, OpenCode, Freebuff, Grok bot posts | Create a hub and a standalone comparison page | `/dev9b/guides/self-hosted-ai-agents/` |
| Free developer infrastructure | Free subdomains, Hurricane Electric DNS, Anycast DNS, Codeberg Pages, localcert | Hub with a maintained comparison table and update dates | `/dev9b/guides/free-dev-infrastructure/` |
| Static site publishing | Hugo, Astro, Gatsby, GitHub Pages, custom domain posts | Hub plus an SSG decision guide | `/dev9b/guides/static-site-publishing/` |
| Email and domain setup | Cloudflare Email Routing, Gmail send-as, Nodemailer SMTP | Consolidate into a step-by-step series with one index page | `/dev9b/guides/custom-domain-email/` |
| AI design quality | AI colours study, de-slop design, getdesign.md | Extend into an original data series | `/dev9b/guides/ai-design-quality/` |

## Opportunity register

## Priority and effort matrix

Qualitative placement by the auditor, not measured.

## UX and conversion

**Scope:** text-level observation only. The pages were not rendered, so layout, mobile behaviour and visual issues were not assessed. No analytics were available, so no conversion problem is claimed.

- The goal appears to be readership and contributions. The homepage offers "Contribute an Article" and "Browse Archives" buttons, which match that.
- Navigation is clear: Home, Archives, Search, About, Contributor Guide, Editorial Policy, Team.
- Posts carry share links, a copy-link control, "Suggest changes" and "Report article", which support the open-source positioning.
- The affiliate Hostinger link appears mid-post and in the intro disclosure. If affiliate revenue matters, track clicks separately from organic sessions.
- The homepage has no newsletter or follow prompt apart from an RSS feed that is not linked in the visible navigation of the fetched text.

Local SEO: not applicable. Dev9b is a global publication with no physical location, service area or local intent.

## 30/60/90-day roadmap

Bars show task count per phase. No ranking or traffic outcome is guaranteed.

## Measurement framework

- Verify the site in Google Search Console and Bing Webmaster Tools; track indexed versus submitted URLs for the blog sitemap.
- Track impressions, clicks and CTR by page group (posts, tags, hubs) monthly.
- Run the AI visibility prompt set monthly and log mentions, citations and third-party sources.
- Measure Core Web Vitals in field data (CrUX or Search Console) before and after changes.
- Track affiliate link clicks and contribution form submissions as conversions.

## Strategic answers

| Question | Answer |
| --- | --- |
| Optimise first | Homepage, the Hermes and Nod posts, and the three posts that already combine key takeaways with FAQ. |
| New pages | Author profile pages, five topic hubs, a Hermes vs Nod comparison page. |
| Development fix now | Set the Hugo base URL to https, regenerate the sitemap and feed, add the sitemap to robots.txt, remove placeholder pages, review http handling at the host. |
| Content team | Add named authors, answer blocks, sources and verified-on dates; refresh posts about fast-moving tools. |
| Link building team | Pitch the original-data posts and maintainers of documented projects; avoid low-value directories. |
| GEO and AI visibility | Start the monthly prompt log, then standardise answer blocks, sources and entity naming. |
| Local SEO | Not necessary. |
| Highest-impact first action | Make every URL signal https consistently (sitemap, canonicals on all templates, og:url, og:image, feed) and verify the site in Search Console. |

## Data limitations and untested areas

| Area | Status | Reason |
| --- | --- | --- |
| Crawl coverage | Sample | Inspected: homepage, Hermes post, Nod post (via RSS), Lucide post (dev.to copy), editorial policy, team page, tag page, placeholder category page, robots.txt, root sitemap, blog sitemap, RSS feed, GitHub Pages host, GitHub repo snippet. The rest of the 87 posts were not opened. |
| Core Web Vitals | Not tested | PageSpeed API request failed with a client error. |
| HTTP headers and redirects | Not tested | The fetch tool does not expose status codes or headers and may upgrade http to https. |
| Structured data validity | Not tested | Page fetches return converted text, not raw JSON-LD. |
| Indexing status | Not tested | No Search Console data. |
| Backlinks and keyword metrics | Not tested | No third-party SEO tool access. |
| AI platform visibility | Not tested | No live access to the platforms. |
| Mobile and visual UX | Not tested | Pages were not rendered. |
| Post count reconciliation | Not tested | The site says 87 posts in 2026; sitemap entries were not counted one by one. |

Scores are the auditor's estimates from the evidence above. Findings marked Potential are hypotheses to verify.