---
name: crosspost
description: >
  Publish a Dev9b Hugo article to dev.to, Medium, AWS Builder Center and
  LinkedIn. Use after a post passes publish-gate.ps1, or when asked to
  "cross-post", "syndicate", "publish everywhere", "post to dev.to",
  "make a Medium version", "Builder Center version" or "LinkedIn post".
  One source file: content/post/<slug>/index.md.
---

# Cross-post a Dev9b article

One Hugo page bundle becomes four artifacts, because each destination disagrees
about tables, code blocks, cover images and markup.

| Destination | How it is delivered | What the tool writes |
|---|---|---|
| dev.to | REST API, draft first, live on publish | `.crosspost/<slug>/devto.md`, then publishes it |
| Medium | No API, paste HTML | `.crosspost/<slug>/medium.html` (tables become PNGs) |
| AWS Builder Center | No API, paste HTML, upload cover | `.crosspost/<slug>/builder.html`, title, description, tags |
| LinkedIn | Composer only, no API draft | `.crosspost/<slug>/linkedin.txt` + `linkedin-cover.jpg` |

## Commands

Run from the repository root:

```bash
python scripts/crosspost/crosspost.py build <slug>
python scripts/crosspost/crosspost.py publish <slug>      # dev.to live
python scripts/crosspost/crosspost.py publish <slug> --draft
python scripts/crosspost/crosspost.py latest              # newest post, all in
```

`publish` builds, checks that the cover URL is reachable, creates or updates the
dev.to article under the organization in `.crosspost.json`, then rebuilds the
LinkedIn post with the live URL.

## Prerequisites

- The post passed `publish-gate.ps1`.
- `python -m pip install PyYAML Pillow`.
- Hugo is installed (the tool renders the Medium/Builder HTML from Hugo).
- A dev.to key in `$DEV_TO_API_KEY` or `~/.devto.key`. Never commit it.
- The article, cover and `static/crosspost/<slug>/` are committed and pushed
  before publishing, because dev.to and Medium fetch them by URL.

## After the command

1. **Medium:** open https://medium.com/new-story, type the title, open
   `.crosspost/<slug>/medium.html` in a browser, copy all, paste, add topics.
2. **Builder Center:** new Article, paste title, description and
   `builder.html`, pick tags, upload `cover.jpg`.
3. **LinkedIn:** paste `linkedin.txt` into the composer, attach
   `linkedin-cover.jpg`, post.
4. Re-run `build` after the dev.to URL exists so the LinkedIn post carries it.

## Rules

- Do not hand-write a Medium markdown file. Tables vanish and code flattens.
- Keep `published: false` in the dev.to source file. The payload flips it.
- No em dashes, no fake personal anecdotes, no invented numbers.
- The site post is canonical. Every syndicated copy should point back to it.
