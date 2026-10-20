---
title: "Deploy Astro to GitHub Pages: Complete Setup Guide 2026"
description: "Learn how to install and deploy Astro on GitHub Pages with the official action. Step-by-step config, base path tips, custom domains, and FAQs for developers."
slug: how-to-deploy-astro-github-pages
date: 2026-10-20
image: cover.jpg
author: F9XR Team
keywords: deploy Astro to GitHub Pages, Astro GitHub Pages, withastro/action, GitHub Actions, static site generator, base path, custom domain, Astro deployment
categories:
    - Tutorials
tags:
    - github-pages
    - github-actions
    - developer-setup
draft: false
math: false
faq:
    - question: "How do I deploy an Astro site to GitHub Pages?"
      answer: "Create a .github/workflows/deploy.yml file that uses withastro/action, set site and base in astro.config.mjs, enable GitHub Actions as the Pages source in repository settings, and push to the main branch."
    - question: "Do I need a base path for GitHub Pages with Astro?"
      answer: "Yes for project sites (username.github.io/repo). Set base: '/repo-name'. Skip it only for user or organization sites named username.github.io."
    - question: "What is the official Astro GitHub Action?"
      answer: "The package withastro/action installs dependencies, builds your Astro site, and uploads the output so actions/deploy-pages can publish it to GitHub Pages."
    - question: "Can I use a custom domain with Astro on GitHub Pages?"
      answer: "Yes. Add a public/CNAME file with your domain, update the site option in astro.config.mjs, remove the base option, and configure the required DNS records."
    - question: "Why is my Astro site showing 404s after deploying to GitHub Pages?"
      answer: "This is almost always caused by a missing or incorrect base value in astro.config.mjs. Ensure internal links and assets also respect the base path."
    - question: "Does the workflow support pnpm or yarn?"
      answer: "Yes. The withastro/action build step detects your lockfile automatically, so committing a pnpm-lock.yaml or yarn.lock switches the package manager without editing the workflow."
---
Astro has become one of the go-to static site generators for developers who want fast pages without the JavaScript bloat. Pair it with GitHub Pages and you get free hosting, automatic deploys on every push, and a workflow that fits the Git habits you already have.

This guide walks you through the full process of setting up an Astro project and deploying it to GitHub Pages using the official `withastro/action`. No outdated hacks, no manual `dist` uploads. Just the current recommended method that works in 2026.

Whether you are shipping a personal portfolio, a documentation site, or a blog, the steps below get you from zero to a live GitHub Pages URL.

<!--more-->

## How to Deploy Astro to GitHub Pages: The Big Picture

There are three moving parts, and once they click the whole setup stops feeling mysterious:

1. **Astro builds static files.** `npm run build` emits a `dist/` folder of HTML, CSS, and assets.
2. **GitHub Actions builds and uploads.** The official workflow installs your dependencies, runs the build, and hands the output to Pages.
3. **GitHub Pages serves the result.** Every future push to `main` re-runs the same pipeline.

The two configuration surfaces are small: `site` and `base` in `astro.config.mjs`, plus one workflow file. Everything else is repository settings.

> [!TIP]
> If you have deployed a Hugo site before, the mental model is identical — only the config keys change. Our [Hugo on GitHub Pages setup guide](/p/hugo-github-pages-setup/) walks the same terrain with `baseURL` instead of `site`/`base`.

## Prerequisites

Before you start, make sure you have:

- Node.js 22 or later (Astro currently recommends a recent LTS)
- A GitHub account
- Basic familiarity with the terminal and Git
- An existing Astro project or willingness to create one

If you do not have a project yet, create one quickly:

```bash
npm create astro@latest
```

Follow the prompts, choose a template (Blog or Basics works well), install dependencies, and open the folder.

## Step 1: Configure Astro for GitHub Pages

Open `astro.config.mjs` (or `.ts` if you use TypeScript) and set the `site` and `base` options. For a project site — the most common case — it looks like this:

```js
import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://YOUR_USERNAME.github.io',
  base: '/YOUR_REPO_NAME',
});
```

Replace `YOUR_USERNAME` with your GitHub username and `YOUR_REPO_NAME` with the exact repository name. The leading slash on `base` is required.

**When can you skip `base`?** Only if your repository is named exactly `YOUR_USERNAME.github.io`. In that case the site lives at the root and `base` stays unset (or set to `/`).

If you later switch to a custom domain, you will remove the `base` value. Keep that in mind — it is the single most common source of 404s during a migration.

Both options are documented in the [Astro configuration reference for `site` and `base`](https://docs.astro.build/en/reference/configuration-reference/), and the official [Astro deployment guide for GitHub Pages](https://docs.astro.build/en/guides/deploy/github/) is worth a read alongside this walkthrough.

## Step 2: Add the GitHub Actions Workflow

Create the file `.github/workflows/deploy.yml` in your project root and paste the current official workflow:

```yaml
name: Deploy to GitHub Pages

on:
  # Trigger the workflow every time you push to the `main` branch
  # Using a different branch name? Replace `main` with your branch's name
  push:
    branches: [main]
  # Allows you to run this workflow manually from the Actions tab on GitHub.
  workflow_dispatch:

# Allow this job to clone the repo and create a page deployment
permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout your repository using git
        uses: actions/checkout@v7
      - name: Install, build, and upload your site
        uses: withastro/action@v6
        # with:
        #   path: . # The root location of your Astro project inside the repository. (optional)
        #   node-version: 24 # The specific version of Node that should be used to build your site. Defaults to 24. (optional)
        #   package-manager: pnpm@latest # The Node package manager that should be used to install dependencies and build your site. Automatically detected based on your lockfile. (optional)
        #   build-cmd: pnpm run build # The command to run to build your site. Runs the package build script/task by default. (optional)
        #   out-dir: dist # The output directory created by the build command. Defaults to dist. (optional)

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

This workflow does three things:

1. Checks out your code.
2. Uses the official Astro action to install dependencies, run the build, and upload the `dist` folder as an artifact.
3. Deploys that artifact to GitHub Pages.

You can uncomment and adjust the optional inputs if you use a monorepo, a pinned Node version, pnpm, or a custom build command. The action's behavior is defined in the [withastro/action repository](https://github.com/withastro/action), which is also the place to check for new major versions.

> [!IMPORTANT]
> Keep the `permissions` block exactly as shown. Pages deployments use an OIDC token, so `id-token: write` and `pages: write` are mandatory — without them the deploy job fails with a cryptic authorization error.

## Step 3: Enable GitHub Pages in Repository Settings

1. Push your project (including the new workflow file) to a GitHub repository.
2. Go to the repository **Settings** tab.
3. In the left sidebar, click **Pages**.
4. Under **Build and deployment**, set **Source** to **GitHub Actions**.

That is the only setting you need. GitHub will pick up the workflow automatically. The mechanics behind this are covered in the [official GitHub Pages documentation](https://docs.github.com/en/pages) if you want the deeper detail.

## Step 4: Push and Deploy

Commit and push to the `main` branch:

```bash
git add .
git commit -m "Add Astro GitHub Pages deployment workflow"
git push origin main
```

Head to the **Actions** tab in your repository. You should see the "Deploy to GitHub Pages" workflow running. The first run can take a minute or two while dependencies install.

Once it finishes successfully, your site will be live at:

`https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/`

You can also trigger the workflow manually from the Actions tab using **Run workflow**.

In our own first runs, the build job finished in roughly 90 seconds on a small content site; the deploy job adds a few seconds on top. Subsequent runs feel faster because npm's cache survives between builds.

## Handling Assets and Internal Links

Because of the `base` path, relative URLs matter. Astro's `<Link>` component and the `import.meta.env.BASE_URL` variable help keep paths correct.

```astro
---
const base = import.meta.env.BASE_URL;
---
<a href={`${base}about/`}>About</a>
<img src={`${base}images/hero.webp`} alt="Hero" />
```

Or simply use absolute paths starting with the base when writing plain HTML.

Public assets placed in the `public/` folder are copied as-is and respect the base path automatically. For a deeper dive on keeping galleries and inline images healthy in a static pipeline, see our notes on [image galleries in Dev9b articles](/p/image-gallery-in-dev9b-articles/).

## Deploy Astro to GitHub Pages with a Custom Domain

Once the site works on the default GitHub Pages URL, you can point a custom domain to it.

1. In your domain registrar or DNS provider, add the required records — usually a CNAME pointing to `YOUR_USERNAME.github.io`, or the A records GitHub documents. If your DNS lives on Cloudflare, our [guide to creating a Cloudflare subdomain for GitHub Pages](/p/how-to-create-cloudflare-subdomain-github-pages/) shows the exact record setup, and the [GitHub Pages custom domain with Cloudflare walkthrough](/p/github-pages-custom-domain-cloudflare/) covers proxy and SSL nuances.
2. Create a file at `public/CNAME` containing only your domain:

```
example.com
```

3. Update `astro.config.mjs`:

```js
export default defineConfig({
  site: 'https://example.com',
  // remove the base option entirely
});
```

4. Commit and push. The next deploy will serve the site at your custom domain.

GitHub may take a short time to issue the SSL certificate after the DNS change propagates.

Not ready to buy a domain? Several [free subdomain providers for developers](/p/free-subdomains-for-developers-list/) hand out a `something.yourdomain.dev`-style address that works with the same CNAME flow.

## Common Pitfalls and How to Fix Them

| Problem | Likely Cause | Fix |
|---------|--------------|-----|
| 404 on all pages except homepage | Missing or incorrect `base` | Set `base: '/repo-name'` and rebuild |
| CSS/JS assets 404 | Assets not prefixed with base | Use `import.meta.env.BASE_URL` or Astro components |
| Workflow fails on install | Wrong Node version or lockfile | Specify `node-version` or ensure the lockfile is committed |
| Pages still shows "waiting" | Workflow not on default branch or permissions missing | Confirm `main` is default and the permissions block is present |
| Custom domain not securing | DNS not propagated or CNAME missing | Wait for DNS, verify `public/CNAME` exists |

## Practical Tips for a Smooth Workflow

- Keep the workflow file on the default branch. GitHub only runs Pages workflows from the default branch for the first setup.
- Use `pnpm` or `yarn` if you prefer; the action auto-detects the lockfile.
- Add environment variables under the `withastro/action` step if your build needs them (public ones only in the YAML; private ones as repository secrets).
- Test locally with `npm run build && npm run preview` before pushing. Preview respects the `base` setting when configured correctly.
- For documentation sites, consider the official Starlight template. It already plays nicely with GitHub Pages.

## FAQ

### How do I deploy an Astro site to GitHub Pages?

Create a `.github/workflows/deploy.yml` file that uses `withastro/action`, set `site` and `base` in `astro.config.mjs`, enable GitHub Actions as the Pages source, and push to the main branch.

### Do I need a base path for GitHub Pages with Astro?

Yes for project sites (`username.github.io/repo`). Set `base: '/repo-name'`. Skip it only for user or organization sites named `username.github.io`.

### What is the official Astro GitHub Action?

The package `withastro/action` (currently at v6) installs dependencies, builds your site, and uploads the output so the official `actions/deploy-pages` can publish it.

### Can I use a custom domain with Astro on GitHub Pages?

Yes. Add a `public/CNAME` file, update the `site` option, remove `base`, and configure DNS at your registrar.

### Why is my Astro site showing a blank page or 404s after deploy?

Almost always a missing or incorrect `base` value. Check `astro.config.mjs` and make sure internal links and assets use the base path.

### Does the workflow support pnpm or yarn?

Yes. The action detects the lockfile automatically. You can also force a package manager with the `package-manager` input.

## Key Takeaways

- Use the official `withastro/action` GitHub Action for the simplest and most reliable Astro + GitHub Pages setup.
- Always set both `site` and `base` in `astro.config.mjs` when deploying to a project site (`username.github.io/repo-name`).
- Choose GitHub Actions as the Pages source in repository settings — it is the only setting you need.
- Custom domains require a `public/CNAME` file and removing the `base` option.
- The workflow triggers on every push to `main` and can also be run manually from the Actions tab.

## Conclusion

Deploying Astro to GitHub Pages is straightforward once the `site`/`base` pair and the official Action are in place. Push the workflow, flip the Pages source to GitHub Actions, and every future commit to `main` becomes a live update. That combination of free hosting and zero-friction CI is hard to beat for personal projects and small team sites.

Teams like F9XR rely on exactly this kind of automated static pipeline to ship documentation and guides without touching a server — the same pattern scales from a one-page portfolio to a full content site.

Found an error or want to improve this guide? Check the [Contributor Guide](/contribute/) to send a fix, and read our [Editorial Policy](/editorial-policy/) to see how Dev9b reviews and updates articles. This post was drafted with AI assistance and reviewed for accuracy against the official Astro and GitHub documentation.
