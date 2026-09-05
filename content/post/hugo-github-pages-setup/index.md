---
title: "Hugo on GitHub Pages: Complete Setup Guide"
description: "Deploy a Hugo site to GitHub Pages with GitHub Actions in minutes. Step-by-step setup, build caching, and a ready-to-use workflow."
slug: hugo-github-pages-setup
date: 2026-09-05
image: cover.png
author: F9XR Team
keywords:
    - Hugo
    - GitHub Pages
    - GitHub Actions
    - static site
    - CI/CD
categories:
    - Tutorials
tags:
    - hugo
    - github-actions
    - developer-setup
draft: false
math: false
faq:
    - question: "Can I host a Hugo site on GitHub Pages for free?"
      answer: "Yes. GitHub Pages gives every GitHub account one free static site per repository (and free sites for any GitHub account). Hugo sites are plain static HTML, so they drop onto Pages exactly as they are."
    - question: "What is the baseURL when Hugo is served from a project subpath?"
      answer: "Set baseURL to the full Pages URL (for example https://user.github.io/project/). Hugo prefixes internal links with that path, so every asset, canonical, and feed URL resolves correctly."
    - question: "Why cache Hugo modules in CI?"
      answer: "Hugo downloads theme modules and Dart Sass on every build. Caching them slices minutes off each deploy and keeps rebuilds fast, which is important during active editing."
---
Running your own static site without paying for hosting or keeping a server online is still one of the most underrated setups in web development. Hugo plus GitHub Pages gives you exactly that: a site that builds in under two seconds, deploys automatically on every commit, and costs nothing to host.

This guide walks through the same setup that runs this site. You will leave with a working Hugo blog on GitHub Pages, an automated deploy pipeline, and a clear picture of how the pieces fit together.

<!--more-->

## How Hugo and GitHub Pages Fit Together

Hugo is a static site generator. It turns Markdown and templates into plain HTML files. GitHub Pages is a static host with a build-and-deploy pipeline built in. The two mix well because there is no server to bolt together — Hugo produces files, Pages serves them.

GitHub Actions is the glue. A workflow runs on every push, installs the exact Hugo version that built the site locally, generates the HTML, and hands it to Pages.

## Prerequisites

- A GitHub account
- Git installed on your machine
- Hugo extended edition installed locally (`hugo version` should show `extended`)
- A text editor

## Step 1: Create the Hugo Site

```bash
hugo new site my-site
cd my-site
```

Add a theme. This site uses the Hugo Theme Stack v4 module, but any theme works. To add a theme as a Hugo module:

```bash
hugo mod init github.com/yourname/my-site
printf '[[module.imports]]\n\tpath = "github.com/CaiJimmy/hugo-theme-stack/v4"\n' >> hugo.toml
```

Then create a first post and test locally:

```bash
hugo new content/post/hello/index.md
hugo server
```

## Step 2: Push to GitHub

Create a repository on GitHub, then:

```bash
git init
git add .
git commit -m "Initial Hugo site"
git remote add origin https://github.com/yourname/my-site.git
git push -u origin main
```

## Step 3: The Deploy Workflow

GitHub Pages has two deployment paths. The modern one uses the `actions/deploy-pages` action, which uploads a built artifact that Pages serves directly. Create `.github/workflows/deploy.yml`:

```yaml
name: Build and deploy
on:
  push:
    branches:
      - main
permissions:
  contents: read
  pages: write
  id-token: write
concurrency:
  group: pages
  cancel-in-progress: false
jobs:
  build:
    runs-on: ubuntu-latest
    env:
      HUGO_VERSION: 0.154.2
    steps:
      - name: Checkout
        uses: actions/checkout@v6
        with:
          submodules: recursive
          fetch-depth: 0
      - name: Setup Pages
        id: pages
        uses: actions/configure-pages@v6
      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v3
        with:
          hugo-version: '${{ env.HUGO_VERSION }}'
          extended: true
      - name: Build
        run: |
          hugo --gc --minify --cleanDestinationDir \
            --baseURL "${{ steps.pages.outputs.base_url }}/"
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v5
        with:
          path: ./public
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v5
```

Then in the repository settings, set Pages to "GitHub Actions" as the source. On the next push, Actions builds the site and Pages publishes it.

## Step 4: Serving From a Project Subpath

If your site lives at `https://yourname.github.io/site-name/` — not the account root — set the baseURL in your Hugo config to the full URL. Hugo then prefixes all internal links with that path. This is the part people forget, and it produces broken assets, misdirected canonicals, and feeds that point to nothing.

```toml
baseURL = "https://yourname.github.io/site-name/"
```

## The Full Pipeline at a Glance

```mermaid
mindmap
  root((Static site pipeline))
    Source
        Hugo site
        Theme module
        Content drafts
    CI: GitHub Actions
        Install Hugo extended
        Install Dart Sass
        Build with minify
        Cache modules
    Deploy
        Upload artifact
        Pages deployment
    Live site
        Static HTML
        sitemap.xml
        RSS feeds
```

Prefer pure Markdown? The same map as a tree:

```
Static site pipeline
  - Source
    - Hugo site
    - Theme module
    - Content drafts
  - CI: GitHub Actions
    - Install Hugo extended
    - Install Dart Sass
    - Build with minify
    - Cache modules
  - Deploy
    - Upload artifact
    - Pages deployment
  - Live site
    - Static HTML
    - sitemap.xml
    - RSS feeds
```

## Speeding Up Builds With Caching

Two things slow fresh Hugo builds down: downloading theme modules and compiling Dart Sass. Cache both in CI and deploys drop from minutes to seconds.

```yaml
- name: Cache restore
  id: cache-restore
  uses: actions/cache/restore@v5
  with:
    path: ${{ runner.temp }}/hugo_cache
    key: hugo-${{ github.run_id }}
    restore-keys:
      hugo-
- name: Build
  run: |
    hugo --cacheDir "${{ runner.temp }}/hugo_cache"
```

Point Hugo at a `--cacheDir` inside the cached folder and restore it before every build.

## Key Takeaways

- Hugo and GitHub Pages combine into a free, fully automated static site setup.
- The `actions/deploy-pages` path is the modern way to publish Pages sites from CI.
- With a subpath site, `baseURL` must match the full Pages URL or links break.
- Caching Hugo modules and Dart Sass keeps deploy times in the single digits.

## Conclusion

A static site that deploys itself frees you to write. This very site runs the pipeline above — the workflow file in this article is a trimmed copy of ours. When you are ready to move past Hugo for this site, check the [contributor guide](/contribute/) or see how we turn the whole process into a [Google-friendly checklist](/p/hugo-seo-guide/). Every change we publish is reviewed against the standards in our [editorial policy](/editorial-policy/).