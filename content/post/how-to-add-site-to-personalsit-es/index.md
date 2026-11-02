---
title: "Add Your Site to PersonalSit.es Directory"
description: "Step-by-step guide for developers to submit a personal website to PersonalSit.es by forking the repo and opening a pull request."
slug: how-to-add-site-to-personalsit-es
date: 2026-11-02
image: cover.jpg
author: F9XR Team
keywords: personalsit.es, personal website directory, add site to personalsit.es, github pull request directory, indieweb directory
categories:
    - Tutorials
tags:
    - open-source
    - github
    - indieweb
    - developer-tools
draft: false
math: false
faq:
  - question: "How long does it take for a site to appear after the PR is opened?"
    answer: "Most submissions are reviewed within a few days to a couple of weeks, depending on maintainer availability. There is no automated approval."
  - question: "Can I submit a site that is still under construction?"
    answer: "It is better to wait until the site is reasonably complete and publicly accessible. Incomplete or placeholder sites are often declined."
  - question: "What if my domain is a subdomain?"
    answer: "That is fine. Name the YAML file after the full subdomain, for example notes.yoursite.com.yaml."
  - question: "Do I need an RSS feed?"
    answer: "No. The feed field is optional. Including one simply helps the directory surface recent updates."
  - question: "Why was my pull request closed?"
    answer: "Common reasons include AI-generated text, incorrect tags, broken links, or sites that do not feel like genuine personal websites. Read the repository README and open a new PR with corrections if needed."
---
Personal websites still matter. In a world full of social platforms and algorithm-driven feeds, a personal site remains one of the few places on the internet that you fully control. [PersonalSit.es](https://personalsit.es/) is a community-curated directory that celebrates exactly that. It lists hundreds of independent personal sites so people can discover new work, get design inspiration, and support the idea that everyone should own a corner of the web.

If you have a personal site (portfolio, blog, digital garden, or experimental playground), getting it listed is straightforward. You do not fill out a form. You open a pull request on the GitHub repository that powers the directory. This guide walks you through the exact process used by the maintainers.

<!--more-->

## What is PersonalSit.es?

PersonalSit.es is an open directory of personal websites. It was originally created by Andy Bell and is currently maintained by Henry Desroches and Declan Chidlow. The site displays screenshots, tags, and links so visitors can filter by interests such as developer, designer, writer, indieweb, or accessibility.

The entire directory is driven by a [public GitHub repository](https://github.com/xdesro/personalsit.es). Every listing is a simple YAML file. That design keeps the project transparent and lets anyone contribute. For developers looking to build their own web presence, learning how to [host static websites with Codeberg Pages](/p/how-to-host-static-websites-codeberg-pages/) or [deploy Astro on GitHub Pages](/p/how-to-deploy-astro-github-pages/) are great places to start.

## Prerequisites Before You Submit

Make sure these things are ready:

- A live personal website with a proper domain or stable URL
- A GitHub account
- Basic familiarity with forking a repository and opening a pull request
- An optional RSS or Atom feed if you want the directory to surface updates

The maintainers are selective about quality and will close pull requests that look AI-generated. Write the submission yourself in a natural way.

## Step-by-Step: How to Add Your Site

### 1. Fork the Repository

Go to the official repository:

[https://github.com/xdesro/personalsit.es](https://github.com/xdesro/personalsit.es)

Click the **Fork** button in the top-right corner. This creates a copy under your own GitHub account.

### 2. Create a New YAML File

In your fork, navigate to the `sites` folder. Create a new file named after your domain.

Examples:

- `yoursite.com.yaml`
- `blog.example.dev.yaml`
- `name.codes.yaml`

Use the exact domain (without `https://` or trailing slash) as the filename.

### 3. Fill Out the Template

Use this structure:

```yaml
title: "Your Name or Site Name"
url: "https://yoursite.com"
tags: ["developer", "writer"]
feed: "https://yoursite.com/feed.xml"
```

**Required fields:**

- `title` – How the site should appear in the directory
- `url` – Full URL including https
- `tags` – Array of allowed tags from the project schema

**Optional field:**

- `feed` – Link to your RSS or Atom feed

Tags must come from the official list defined in [sites.schema.json](https://github.com/xdesro/personalsit.es/blob/main/sites.schema.json). Common ones include:

| Category       | Example Tags                          |
|----------------|---------------------------------------|
| Roles          | developer, designer, writer, maker    |
| Tech           | javascript, css, html, python, react  |
| Interests      | indieweb, blog, accessibility, privacy|
| Other          | photographer, musician, educator      |

Pick only tags that accurately describe your site. Two to four tags usually work best. If you're building out your developer portfolio, check our guide on [best blogging sites for developers](/p/best-blogging-sites-for-developers/) for ideas.

### 4. Open a Pull Request

Commit the new file and open a pull request against the main repository. Write a short, clear description such as:

> Adding my personal site [yoursite.com]

The maintainers review submissions manually. Once approved, your site appears on personalsit.es along with an automatically generated screenshot.

## Tips for a Smooth Approval

- Keep the YAML clean and correctly indented
- Use real, human-written title and tags
- Make sure the site loads quickly and looks intentional
- Avoid promotional or purely commercial landing pages
- If your site changes significantly later, open an issue to request a screenshot update
- Check the README for any recent changes to submission guidelines
- Make sure your site is accessible and works without JavaScript where possible
- Avoid submitting sites that are mostly affiliate links or lead generation pages

## Updating an Existing Listing

Screenshot updates are currently manual. Open a new issue in the repository and request a refresh. The maintainers usually handle these requests when they can. If your URL changes or you need corrections to your listing, you can also submit a new pull request to update your YAML file.

## Key Takeaways

- PersonalSit.es is a community directory powered by a public GitHub repository
- Adding your site means creating a YAML file and opening a pull request
- Required fields are title, url, and tags
- Tags must match the official schema
- Maintainers prefer authentic, human-written submissions
- Having an RSS feed is optional but helpful
- The process supports the broader idea of owning your own place on the web

## Frequently Asked Questions

### How long does it take for a site to appear after the PR is opened?

Most submissions are reviewed within a few days to a couple of weeks, depending on maintainer availability. There is no automated approval.

### Can I submit a site that is still under construction?

It is better to wait until the site is reasonably complete and publicly accessible. Incomplete or placeholder sites are often declined.

### What if my domain is a subdomain?

That is fine. Name the YAML file after the full subdomain, for example `notes.yoursite.com.yaml`.

### Do I need an RSS feed?

No. The feed field is optional. Including one simply helps the directory surface recent updates.

### Why was my pull request closed?

Common reasons include AI-generated text, incorrect tags, broken links, or sites that do not feel like genuine personal websites. Read the repository README and open a new PR with corrections if needed.

## Why Submit to PersonalSit.es?

Listing your site does more than just add it to a directory. It connects you to a wider community of independent web enthusiasts who care about craftsmanship, accessibility, and digital autonomy. Many people discover new blogs and projects through the directory, leading to meaningful connections across the IndieWeb.

It's also a great way to show support for open-source curation. The entire project runs on GitHub, so the community collectively maintains and improves it over time. By submitting your site, you're participating in keeping the human web visible and discoverable.

## Conclusion

Getting listed on PersonalSit.es is a great way to join the growing community of people who value the open web and digital independence. The process is simple, transparent, and aligned with the IndieWeb values of ownership and autonomy. If you're ready to put your site on the map, fork the repo and submit your PR today.

If you're just getting started, check out our [Contributor Guide](/contribute/) and [Editorial Policy](/editorial-policy/) to learn how we maintain quality across Dev9b.
