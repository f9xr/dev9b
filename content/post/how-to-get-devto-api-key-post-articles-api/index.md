---
title: "Dev.to API Key Guide: Publish Articles From Code"
description: "Learn how to get your Dev.to API key and publish articles with the Forem API using curl, Node.js and Python. Step by step, with working code."
slug: how-to-get-devto-api-key-post-articles-api
date: 2026-11-10
image: cover.jpg
author: F9XR Team
keywords: Dev.to API key, Forem API, post articles on Dev.to using API, Dev.to API tutorial, publish to Dev.to programmatically, api-key header, Dev.to cross-posting
categories:
    - Tutorials
tags:
    - devto
    - api
    - tutorial
    - webdev
draft: false
math: false
faq:
    - question: "How do I get a Dev.to API key?"
      answer: "Sign in to Dev.to, open Settings, choose Extensions, and scroll to the DEV Community API Keys section. Enter a description, click Generate API Key, then expand the new entry and copy the key."
    - question: "Is the Dev.to API free to use?"
      answer: "Yes. The API is free with a regular Dev.to account, and you can generate keys at no cost. Keep an eye on rate limits and the community guidelines when you automate."
    - question: "How do I post an article on Dev.to using the API?"
      answer: "Send a POST request to https://dev.to/api/articles with your api-key header and a JSON body containing an article object with at least a title and body_markdown. Set published to true to go live or false to save a draft."
    - question: "What header does the Dev.to API use for authentication?"
      answer: "It uses a custom header named api-key, not the standard Authorization header. Add accept: application/vnd.forem.api-v1+json as well so the request targets API v1."
    - question: "How many tags can I add to a Dev.to article through the API?"
      answer: "Up to four. Sending more than four tags typically returns a validation error, so trim the list before you post."
    - question: "Can I update or delete an article with the Dev.to API?"
      answer: "You can update an article with PUT /api/articles/{id}. To take a post offline, set published to false to move it back to a draft."
    - question: "Why does the Dev.to API return 401 Unauthorized?"
      answer: "A 401 means the key is missing, wrong or revoked. Check that the api-key header is spelled correctly, the environment variable is loaded, and the key still appears in your Dev.to settings."
    - question: "Can I schedule Dev.to posts with the API?"
      answer: "The API itself focuses on creating and updating articles, so scheduling is something you build around it. Many people save drafts through the API and trigger publishing with a cron job or a GitHub Actions workflow at a later time."
---

If you write on your own blog and then copy and paste every post into Dev.to by hand, you already know how tedious it gets. Open the editor, paste the Markdown, fix the formatting, add tags, set the canonical URL, hit publish. Do that ten times and you start wondering why a developer is doing manual labor.

Dev.to runs on Forem, an open source platform with a documented REST API. With one API key and one HTTP request, you can create an article, save it as a draft, update it later, and wire the whole thing into a CI pipeline. Every new post on your site can show up on Dev.to without you touching a browser.

This guide covers the full process: where to find your **Dev.to API key**, how authentication works, how to publish your first article with curl, Node.js and Python, how to update posts, and how to avoid the mistakes that trip up most people on their first attempt.

<!--more-->

## What Is the Dev.to API?

The Dev.to API is the public REST interface of DEV Community, which is built on the Forem platform. The current stable version is API v1, and it lives at `https://dev.to/api`. The official reference is the [Forem API v1 documentation](https://developers.forem.com/api).

A few things worth knowing up front:

- **Reads are mostly public.** You can list articles, look up tags or fetch a user profile without any key.
- **Writes need authentication.** Creating, updating or unpublishing content requires an `api-key` header.
- **It is plain JSON over HTTPS.** Any language that can send an HTTP request can use it, from a Bash one-liner to a Go service.
- **Other Forem communities use the same API.** If you run your own Forem instance, the same endpoints apply on your domain.

### What can you do with it?

| Use case | Endpoint | Method |
|---|---|---|
| Publish or draft a new article | `/api/articles` | POST |
| Update an existing article | `/api/articles/{id}` | PUT |
| List your own articles | `/api/articles/me` | GET |
| List only published articles | `/api/articles/me/published` | GET |
| List only drafts | `/api/articles/me/unpublished` | GET |
| Get your profile info | `/api/users/me` | GET |
| Browse articles by tag | `/api/articles?tag=python` | GET |

## How to Get Your Dev.to API Key

Generating a key takes about a minute. Here is the exact path.

### Step 1: Sign in to Dev.to

Log in to your account at [dev.to](https://dev.to). You need a regular account, nothing paid or special.

### Step 2: Open the Extensions settings

Click your avatar in the top right corner, choose **Settings**, then pick **Extensions** from the left sidebar. You can also jump straight to the [Dev.to Extensions settings](https://dev.to/settings/extensions).

### Step 3: Scroll to "DEV Community API Keys"

The API key section sits near the bottom of the Extensions page. Scroll all the way down until you see it.

### Step 4: Name the key and generate it

Type a short description that tells you what the key is for, such as `blog-sync` or `github-actions`, then click **Generate API Key**.

### Step 5: Copy the key

Your new key appears under the list of active keys. Expand it and copy the value. Paste it somewhere safe right away, ideally into a password manager or your secrets store.

### Tips for managing API keys

- **Create one key per project.** If a key leaks, you revoke only that one and nothing else breaks.
- **Use clear descriptions.** Six months from now, "key 2" tells you nothing. "devto-crosspost-ci" does.
- **Revoke keys you no longer use.** The same settings page lets you delete any key at any time.
- **Treat the key like a password.** It acts as you. Anyone holding it can publish and edit under your account.

## How Authentication Works

The Dev.to API uses a simple header based scheme. You send two headers on requests that need your identity:

| Header | Value | Required? |
|---|---|---|
| `api-key` | Your generated key | Yes, for writes and private reads |
| `accept` | `application/vnd.forem.api-v1+json` | Recommended, it pins the request to API v1 |

Two details cause a lot of confusion, so here they are plainly:

1. **It is `api-key`, not `Authorization`.** Sending a Bearer token will not work.
2. **Without the versioned `accept` header, requests may be routed to the older v0 behavior.** Always include it so your scripts do not change behavior unexpectedly.

A quick way to confirm your key works is to ask the API who you are:

```bash
curl -s https://dev.to/api/users/me \
  -H "api-key: $DEVTO_API_KEY" \
  -H "accept: application/vnd.forem.api-v1+json"
```

If you get back JSON with your username, the key is good. If you get `{"error":"unauthorized","status":401}`, the key is missing, mistyped or revoked.

### Store the key in an environment variable

Never paste the key into source code. Set it as an environment variable instead:

```bash
# macOS or Linux
export DEVTO_API_KEY="paste-your-key-here"

# Windows PowerShell
$env:DEVTO_API_KEY = "paste-your-key-here"
```

For local projects, a `.env` file that is listed in `.gitignore` works well too. If your repo already has a secrets workflow, the same key slots into GitHub Actions as a repository secret.

## How to Post an Article on Dev.to Using the API

Publishing is a single `POST` request to `/api/articles`. The body is JSON with one top level object called `article`.

### The article fields you will actually use

| Field | Type | What it does |
|---|---|---|
| `title` | string | The article title. Required. |
| `body_markdown` | string | The full post in Markdown. Required for a useful article. |
| `published` | boolean | `true` publishes immediately. `false` saves a draft. |
| `tags` | array of strings | Topic tags. Dev.to allows a maximum of four. |
| `series` | string | Groups posts into a named series. |
| `main_image` | string (URL) | Cover image for the post. |
| `canonical_url` | string (URL) | Points to the original post if you published elsewhere first. |
| `description` | string | A short summary used in previews. |
| `organization_id` | integer | Publish under an organization you belong to. |

### Method 1: Publish with curl

Start with a draft so you can check how it looks before anything goes live:

```bash
curl -X POST https://dev.to/api/articles \
  -H "api-key: $DEVTO_API_KEY" \
  -H "accept: application/vnd.forem.api-v1+json" \
  -H "content-type: application/json" \
  -d '{
    "article": {
      "title": "My First Article Posted With the API",
      "body_markdown": "## Hello from the API\n\nThis post was created with a single curl request.",
      "published": false,
      "tags": ["api", "tutorial", "webdev"],
      "description": "Testing the Dev.to API with curl."
    }
  }'
```

A successful call returns a `201 Created` status and a JSON response that includes the article `id`, its `url` and its `slug`. Save that `id`, because you need it for updates.

### Method 2: Publish with Node.js

Node 18 and newer ship with a built in `fetch`, so no extra packages are needed. The [MDN Fetch API reference](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) is the place to go if you have not used it before.

```javascript
// publish.mjs
const API_KEY = process.env.DEVTO_API_KEY;

if (!API_KEY) {
  throw new Error("Set the DEVTO_API_KEY environment variable first.");
}

const response = await fetch("https://dev.to/api/articles", {
  method: "POST",
  headers: {
    "api-key": API_KEY,
    "accept": "application/vnd.forem.api-v1+json",
    "content-type": "application/json",
  },
  body: JSON.stringify({
    article: {
      title: "Posting to Dev.to With Node.js",
      body_markdown: "## It works\n\nPublished from a Node script.",
      published: false,
      tags: ["node", "javascript", "api"],
    },
  }),
});

const data = await response.json();

if (!response.ok) {
  console.error("Request failed:", response.status, data);
  process.exit(1);
}

console.log("Created:", data.url, "ID:", data.id);
```

Run it with `node publish.mjs`.

### Method 3: Publish with Python

```python
import os
import requests

API_KEY = os.environ["DEVTO_API_KEY"]

headers = {
    "api-key": API_KEY,
    "accept": "application/vnd.forem.api-v1+json",
    "content-type": "application/json",
}

payload = {
    "article": {
        "title": "Posting to Dev.to With Python",
        "body_markdown": "## Hello\n\nPublished from a Python script.",
        "published": False,
        "tags": ["python", "api", "tutorial"],
    }
}

response = requests.post(
    "https://dev.to/api/articles",
    headers=headers,
    json=payload,
    timeout=30,
)
response.raise_for_status()

article = response.json()
print("Created:", article["url"], "ID:", article["id"])
```

### Publish straight from a Markdown file

Most developers already write posts as `.md` files. This Python script reads one and sends it, so you never copy and paste again:

```python
import os
import sys
import pathlib
import requests

API_KEY = os.environ["DEVTO_API_KEY"]
md_path = pathlib.Path(sys.argv[1])

body = md_path.read_text(encoding="utf-8")
title = md_path.stem.replace("-", " ").title()

response = requests.post(
    "https://dev.to/api/articles",
    headers={
        "api-key": API_KEY,
        "accept": "application/vnd.forem.api-v1+json",
    },
    json={
        "article": {
            "title": title,
            "body_markdown": body,
            "published": False,
            "canonical_url": "https://your-site.com/blog/" + md_path.stem,
            "tags": ["webdev", "tutorial"],
        }
    },
    timeout=30,
)
response.raise_for_status()
print(response.json()["url"])
```

Run it as `python publish_md.py my-post.md`. Adjust the title logic and canonical URL pattern to match your own site.

## How to Update or Unpublish an Existing Article

Updating uses `PUT` with the article ID you saved earlier:

```bash
curl -X PUT https://dev.to/api/articles/123456 \
  -H "api-key: $DEVTO_API_KEY" \
  -H "accept: application/vnd.forem.api-v1+json" \
  -H "content-type: application/json" \
  -d '{
    "article": {
      "body_markdown": "## Updated content\n\nFixed a typo and added a new section.",
      "published": true
    }
  }'
```

Flipping `published` to `true` turns a draft into a live post. Setting it back to `false` pulls it down to a draft again. Replace `123456` with your real article ID.

### How to find an article ID you forgot

List your drafts or published posts and read the `id` field:

```bash
curl -s https://dev.to/api/articles/me/unpublished \
  -H "api-key: $DEVTO_API_KEY" \
  -H "accept: application/vnd.forem.api-v1+json"
```

## Automate Cross-Posting With GitHub Actions

If your main blog lives in a Git repository, you can push new posts to Dev.to whenever you merge. Store your key as a repository secret named `DEVTO_API_KEY`, following the [GitHub Actions encrypted secrets documentation](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions), then use a workflow like this:

```yaml
name: Cross-post to Dev.to

on:
  workflow_dispatch:

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Publish draft to Dev.to
        env:
          DEVTO_API_KEY: ${{ secrets.DEVTO_API_KEY }}
        run: |
          jq -n --rawfile body posts/my-post.md \
            '{article: {title: "My Post Title", body_markdown: $body, published: false, tags: ["webdev","tutorial"]}}' \
          | curl -sS -X POST https://dev.to/api/articles \
              -H "api-key: $DEVTO_API_KEY" \
              -H "accept: application/vnd.forem.api-v1+json" \
              -H "content-type: application/json" \
              -d @-
```

Using `jq` to build the JSON body saves you from escaping quotes and newlines by hand, which is where most shell based attempts break. Start with `workflow_dispatch` so you control when it runs, and move to a push trigger only after you trust the output.

If you want a visual alternative to YAML, our guide on [self hosting n8n on your own PC](/p/how-to-install-n8n-locally-on-pc/) shows how to chain HTTP steps into a workflow you can inspect node by node.

## Common Errors and How to Fix Them

| Status | Meaning | Usual cause and fix |
|---|---|---|
| `401 Unauthorized` | Key missing or invalid | Check the `api-key` header spelling, confirm the key was not revoked, and make sure the environment variable is actually set. |
| `422 Unprocessable Entity` | Validation failed | Too many tags, an empty title, or a malformed field. Read the error message in the response body. |
| `429 Too Many Requests` | Rate limited | Slow down. Add a delay between calls and retry with backoff. |
| `404 Not Found` | Wrong ID or path | Check the article ID and the endpoint URL. |
| `400 Bad Request` | Broken JSON | Validate the body. Unescaped quotes and raw newlines inside strings are the usual culprits. |

### Mistakes developers make most often

- **Sending more than four tags.** Dev.to caps tags at four per article.
- **Forgetting the `article` wrapper.** The fields must sit inside `{"article": {...}}`, not at the top level.
- **Calling the API from browser code.** Besides running into cross origin restrictions, it would expose your key to every visitor. Make write calls from a server, a script or a CI job.
- **Publishing before previewing.** Create drafts first, check the rendered page, then flip `published` to `true`.
- **Hardcoding the key.** One accidental commit to a public repo and the key is compromised. Rotate it immediately if that happens.

> [!WARNING] Rotate a leaked key
> Revoke the key in Dev.to settings before you do anything else. A key that reaches a public commit is compromised even if you delete the commit later.

## Best Practices for Posting to Dev.to via API

1. **Set a canonical URL.** If the post first appeared on your own blog, point `canonical_url` at it. This tells search engines which version is the original and protects your rankings. The [Hugo SEO guide](/p/hugo-seo-guide/) covers canonical tags on the source side, and you can [set up and ping an IndexNow API key](/p/setup-and-ping-indexnow-api-key/) so search engines pick up the original fast.
2. **Draft first, publish second.** Treat `published: false` as your safety net.
3. **Mind the community rules.** Automation is fine for your own writing. Spamming, mass posting or low effort republishing breaks the [Dev.to Code of Conduct](https://dev.to/code-of-conduct) and can get an account restricted.
4. **Disclose AI assistance where required.** If your workflow uses generated text, check the current editor and policy options on Dev.to and follow them.
5. **Pick tags deliberately.** Four relevant tags beat four random ones. Look at what top posts in your topic use.
6. **Cache and throttle.** Do not hammer endpoints in a loop. A short pause between requests keeps you well inside limits.
7. **Log the returned ID and URL.** Store them next to your source file so future edits become a simple `PUT`.
8. **Keep one source of truth.** Write in Markdown in your repo, then treat Dev.to as a distribution channel rather than a second editor.

We run this exact flow for Dev9b: every post is a Hugo page bundle in Git, a small Python script POSTs the rendered Markdown to Dev.to, and each syndicated copy carries a canonical URL back to the original. The first version failed twice before it worked, both times because of the request body, never the API itself. That is why the examples above build the JSON with a library instead of string concatenation.

For a broader look at where else to publish, see our roundup of the [best blogging sites for developers](/p/best-blogging-sites-for-developers/). If you also write on Hashnode, the process is similar, and we cover it in [how to set up Hashnode for agents](/p/how-to-setup-hashnode-for-agents/).

## Dev.to API vs Posting Manually

| Factor | Manual editor | API |
|---|---|---|
| Speed for one post | Fast | Slower to set up |
| Speed for many posts | Slow and repetitive | Very fast once scripted |
| Consistency of tags and canonical URLs | Easy to forget | Enforced by code |
| Works in CI/CD | No | Yes |
| Learning curve | None | Basic HTTP knowledge |
| Best for | Occasional posts | Regular cross-posting and automation |

## Security Checklist

- Keep the key in environment variables or a secrets manager.
- Add `.env` to `.gitignore` before your first commit.
- Use a separate key for each tool or pipeline.
- Revoke any key you suspect has leaked, then generate a replacement.
- Never print the key in logs, screenshots or support requests.
- Rotate keys now and then, the same way you would rotate any other credential.

## Frequently Asked Questions

### How do I get a Dev.to API key?

Sign in to Dev.to, open Settings, choose Extensions, and scroll to the "DEV Community API Keys" section. Enter a description, click Generate API Key, then expand the new entry and copy the key.

### Is the Dev.to API free to use?

Yes. The API is free with a regular Dev.to account, and you can generate keys at no cost. Keep an eye on rate limits and the community guidelines when you automate.

### How do I post an article on Dev.to using the API?

Send a POST request to `https://dev.to/api/articles` with your `api-key` header and a JSON body containing an `article` object with at least a `title` and `body_markdown`. Set `published` to `true` to go live or `false` to save a draft.

### What header does the Dev.to API use for authentication?

It uses a custom header named `api-key`, not the standard `Authorization` header. Add `accept: application/vnd.forem.api-v1+json` as well so the request targets API v1.

### How many tags can I add to a Dev.to article through the API?

Up to four. Sending more than four tags typically returns a validation error, so trim the list before you post.

### Can I update or delete an article with the Dev.to API?

You can update an article with `PUT /api/articles/{id}`. To take a post offline, set `published` to `false` to move it back to a draft.

### Why does the Dev.to API return 401 Unauthorized?

A 401 means the key is missing, wrong or revoked. Check that the `api-key` header is spelled correctly, the environment variable is loaded, and the key still appears in your Dev.to settings.

### Can I schedule Dev.to posts with the API?

The API itself focuses on creating and updating articles, so scheduling is something you build around it. Many people save drafts through the API and trigger publishing with a cron job or a GitHub Actions workflow at a later time.

## Key Takeaways

- Get your Dev.to API key from **Settings, then Extensions, then DEV Community API Keys**.
- Authenticate with the **`api-key` header**, and add `accept: application/vnd.forem.api-v1+json` to target API v1.
- Create articles with **`POST /api/articles`**, sending JSON wrapped in an `article` object.
- Use **`PUT /api/articles/{id}`** to edit or publish a draft later.
- Start with **`published: false`** so you can review before going live.
- Dev.to allows **up to four tags** per article.
- Set a **`canonical_url`** when cross-posting from your own site.
- Keep your key in an **environment variable**, never in source code, and use one key per project.
- Make API calls from **servers, scripts or CI**, not from public browser code.
- Expect **401, 422 and 429** errors and handle them with clear checks and retries.

## Conclusion

A Dev.to API key turns a repetitive publishing chore into one HTTP request. Generate the key once, store it safely, send an `article` object to `/api/articles`, and you can keep your own site as the source of truth while Dev.to handles distribution. Start with drafts, add the canonical URL, and only automate the publish step after the output looks right.

If you want to go further, the same pattern works for Hashnode, Medium exports and any other platform with an API. If you build something with this guide, the [contributor guide](/contribute/) explains how to propose a post, and the [editorial policy](/editorial-policy/) shows how we review technical claims before they ship.
