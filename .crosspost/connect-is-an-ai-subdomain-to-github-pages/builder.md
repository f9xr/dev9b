You shipped the demo. The repo is clean, the README has a screenshot, and your project is live at `yourname.github.io/my-ai-app`. It works, but it does not look like a product. Sharing that URL on X, Reddit or in a hackathon submission feels a little like handing someone a business card written in pencil.

The fix takes about ten minutes and costs nothing. [is-an.ai](https://is-an.ai) gives away free `your-project.is-an.ai` subdomains for AI projects, and GitHub Pages can serve your repo on any custom domain you point at it. Connect the two and `my-ai-app.is-an.ai` loads your repository, with HTTPS, straight from GitHub.

This guide covers the full setup: the exact DNS record, three ways to register it, the GitHub settings that matter, how to check that everything works, and the errors people hit most often. If you have not read how to claim a name in the first place, start with our [guide to getting a free is-an.ai domain](https://f9xr.org/dev9b/p/free-is-an-ai-subdomain-for-ai-saas-cli-guide/) and come back.

## Quick Answer: How Do You Connect an is-an.ai Subdomain to GitHub?

To connect an is-an.ai subdomain to a GitHub repository, do these five things in order:

1. Turn on GitHub Pages for your repo (Settings, then Pages).
2. Enter `my-project.is-an.ai` as the custom domain in the same Pages settings and save.
3. Register `my-project` on is-an.ai with a **CNAME** record pointing to `YOUR-USERNAME.github.io`.
4. Wait a few minutes, then confirm the record with `dig my-project.is-an.ai`.
5. Tick **Enforce HTTPS** in the Pages settings once GitHub allows it.

The value people get wrong most often is the CNAME target. It is your GitHub username or organization plus `.github.io`. It is **not** the repository name and **not** the long `*.pages.github.io` address.

## How the Pieces Fit Together

Three separate systems are involved, and most confusion comes from mixing them up.

| System | What it does | What you configure |
|---|---|---|
| is-an.ai | Owns the `is-an.ai` domain and publishes your DNS record | A CNAME record for your subdomain |
| GitHub Pages | Hosts your static site and decides which repo answers for which hostname | The custom domain field and HTTPS |
| Your repo | Holds the site files (and optionally a `CNAME` file) | Branch or Actions workflow that publishes the site |

The CNAME record on is-an.ai says "traffic for `my-project.is-an.ai` should go to GitHub's Pages servers." The custom domain setting on GitHub says "when a request arrives for `my-project.is-an.ai`, serve this particular repository." You need both halves. One without the other gives you a 404.

If the DNS side still feels abstract, our explainer on [how DNS resolution works](https://f9xr.org/dev9b/p/anycast-dns-what-is-it-setup-guide/) covers what a resolver does with a CNAME and why the answer can differ by location.

## Before You Start

You need:

- A GitHub account and a repository containing a static site (plain HTML, or a build output from Vite, Astro, Next.js static export, Jekyll, Hugo and similar).
- Node.js installed if you want to use the `npx is-an-ai` command line tool.
- A public email address set on your GitHub profile if you plan to register by pull request. The `owner.email` in your record must match it. Set it at github.com/settings/profile.

A small design note: GitHub Pages works from public repositories on the free plan. Check GitHub's current plan details if your repo is private.

If you have never published a Pages site before, our [complete GitHub Pages setup guide](https://f9xr.org/dev9b/p/hugo-github-pages-setup/) walks through the branch and Actions publishing models. The commands below assume the site already loads at its default `username.github.io` address.

We checked the CLI commands in this guide against `is-an-ai` version 0.1.6 on npm and the record format against the project's `records/schema.json` while writing it. Free services move fast, so confirm the current flags with `npx is-an-ai --help` before you script anything.

## Step 1: Publish Your Repo With GitHub Pages

Open your repository on GitHub, go to **Settings**, then choose **Pages** in the sidebar. Pick how the site is published:

| Publishing method | Best for | Custom domain note |
|---|---|---|
| Deploy from a branch | Plain HTML, Jekyll, anything already committed as static files | GitHub adds a `CNAME` file to the branch root when you save a custom domain |
| GitHub Actions workflow | Vite, Astro, Next.js export, Hugo, any build step | No `CNAME` file is created, and an existing one is ignored. The setting in the Pages UI is what counts |

Confirm the site loads at the default `username.github.io/repo-name` address first. If it is broken there, it will be broken on your new domain too, and debugging two layers at once is no fun.

## Step 2: Pick and Check Your Subdomain Name

Choose something short and readable. `contractlens.is-an.ai` beats `my-cool-ai-project-final-v2.is-an.ai`. Then check availability from your terminal:
```bash
npx is-an-ai check my-project
```

The command comes from the [is-an-ai CLI on npm](https://www.npmjs.com/package/is-an-ai), which also supports global installs with `npm install -g is-an-ai`. You can check on the is-an.ai website instead. Reserved system names such as `www`, `api`, `docs` and `ns1` are protected, so pick something distinctive.

## Step 3: Add the Custom Domain on GitHub First

This order matters, and [GitHub's custom domain documentation](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site) says so directly: add the custom domain to your Pages site **before** you create the DNS record. If DNS goes first, there is a window where someone else could claim your subdomain on their own GitHub Pages site.

1. In your repo, go to **Settings**, then **Pages**.
2. Under **Custom domain**, type `my-project.is-an.ai`.
3. Click **Save**.

If you publish from a branch, GitHub commits a `CNAME` file to the root of that branch. If you build locally and push generated files, pull that commit into your local copy so you do not overwrite it on your next push.

You will probably see a "DNS check unsuccessful" message at this point. That is expected, because the record does not exist yet.

## Step 4: Register the CNAME Record on is-an.ai

Now create the DNS record. There are three ways to do it. They all end up in the same place.

### Option A: The is-an.ai Website

Go to is-an.ai, check your name, sign in with GitHub, register it, and set the target in the dashboard. Choose **CNAME** as the record type and use `YOUR-USERNAME.github.io` as the value.

### Option B: The Command Line
```bash
npx is-an-ai register my-project -t CNAME -v YOUR-USERNAME.github.io
```

Replace `YOUR-USERNAME` with your GitHub username (or organization name). Add `-d "My AI demo"` if you want a short description attached. The CLI stores the session after `npx is-an-ai login`, so later commands do not need to repeat the auth step.

### Option C: A Pull Request

If you prefer version control, fork the [is-an.ai records repository](https://github.com/is-an-ai-org/is-an.ai) and add a file named `records/my-project.json`. Based on the format shown in the project's README, a record looks roughly like this:
```json
{
  "description": "My AI demo hosted on GitHub Pages",
  "owner": {
    "email": "you@example.com"
  },
  "record": [
    {
      "type": "CNAME",
      "value": "YOUR-USERNAME.github.io"
    }
  ]
}
```

The required structure lives in `records/schema.json` in that repository, so check it before you open the PR in case fields have changed. Validation runs automatically and a bot merges the PR when the checks pass. If validation fails, the most common cause is an `owner.email` that does not match your public GitHub email.

### What Value Goes in the CNAME?

| Your situation | Correct CNAME value | Common wrong value |
|---|---|---|
| Personal account `jane` | `jane.github.io` | `jane.github.io/my-ai-app` |
| Organization `acme-labs` | `acme-labs.github.io` | `acme-labs.github.io/site` |
| Any account | `USERNAME.github.io` | The `*.pages.github.io` address from the Pages settings |
| Any account | `USERNAME.github.io` | The repository URL on github.com |

A CNAME record points at a hostname, so it cannot contain a path. The repository is selected on the GitHub side, through the custom domain setting from Step 3.

## Step 5: Verify That DNS Is Working

Give it a few minutes, then check the record from your terminal:
```bash
dig my-project.is-an.ai +nostats +nocomments +nocmd
```

You want to see a CNAME pointing at `YOUR-USERNAME.github.io`, followed by GitHub's IP addresses. On Windows, `dig` is not installed by default, so use PowerShell instead:
```powershell
Resolve-DnsName my-project.is-an.ai
```

Then go back to **Settings**, **Pages** in your repo. The DNS check should turn green. GitHub notes that DNS changes can take up to 24 hours to propagate, although it is often far quicker.

A note on timing. The is-an.ai records repository says a full DNS sync runs daily at 2 AM UTC and read-only checks run every 15 minutes, and GitHub can delay scheduled jobs. If you register through the website or CLI it is usually fast, but if you are on the pull request path and nothing resolves right away, give it time before assuming something is broken.

## Step 6: Turn On HTTPS

Back in **Settings**, **Pages**, tick **Enforce HTTPS**. GitHub provisions a certificate for your custom domain once DNS resolves correctly. The checkbox can take up to 24 hours to become clickable, so do not panic if it is greyed out right after setup.

Why bother? Browsers flag plain HTTP sites, many APIs refuse to talk to insecure origins, and OAuth providers often require HTTPS redirect URIs. For an AI project that calls model APIs from the browser, it is not optional. [GitHub's HTTPS documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https) explains the certificate flow if you want the details.

## Optional: Verify the Domain on GitHub

GitHub lets you verify custom domains on your account, which protects against domain takeover if a DNS record is ever left dangling. Verification uses a TXT record. The is-an.ai project supports vendor verification records in the format `_{vendor}.{subdomain}`, which are TXT only and require you to own the base subdomain first.

So the sequence would be: register `my-project` first, then add the TXT record GitHub gives you under the matching vendor name. We have not tested this exact flow against GitHub's verification challenge, so treat it as optional and check the is-an.ai README for the current rules before you rely on it.

## Fixing a Project Site That Looks Broken on the New Domain

Here is a trap that catches a lot of developers. When you serve a project repo on its default address, your site lives under a path, like `username.github.io/my-ai-app/`. On a custom domain, it moves to the root: `my-project.is-an.ai/`.

If your framework was configured with a base path, your CSS, JavaScript and images will 404. Fix it by resetting the base:

| Framework | Setting to change | New value |
|---|---|---|
| Vite | `base` in `vite.config.js` | `'/'` |
| Astro | `base` in `astro.config.mjs` | `'/'` (and set `site` to your new URL) |
| Next.js static export | `basePath` in `next.config.js` | remove it |
| Jekyll | `baseurl` in `_config.yml` | `""` and set `url` to your new URL |
| Create React App | `homepage` in `package.json` | your new URL |

Rebuild, push, and the assets should load. If you use a single-page app router, also add a `404.html` that mirrors `index.html`, since GitHub Pages has no server side rewrite rules.

## Troubleshooting: Common Errors and Fixes

[GitHub's custom domain troubleshooting guide](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/troubleshooting-custom-domains-and-github-pages) covers the error messages in more depth. These are the ones that come up most often with a free subdomain:

| Symptom | Likely cause | Fix |
|---|---|---|
| GitHub 404 page on your domain | Custom domain not saved in Pages settings, or `CNAME` file removed | Re-enter the domain under Settings, Pages. Check the `CNAME` file exists on your publishing branch |
| "DNS check unsuccessful" stays red | Record not created, wrong value, or not propagated yet | Run `dig`, confirm the CNAME points at `USERNAME.github.io`, wait and retry |
| Domain resolves but shows the wrong site | CNAME points at a different account, or another repo claims the domain | Check the value, and make sure only one repo uses that custom domain |
| Enforce HTTPS is greyed out | Certificate still being issued | Wait up to 24 hours. Remove and re-add the custom domain if it stays stuck |
| Site loads without CSS or images | Base path still set for `/repo-name/` | Reset the base path in your framework config (see table above) |
| Custom domain vanishes after each deploy | Workflow overwrites the `CNAME` file | Use the Pages UI setting with an Actions workflow, or include `CNAME` in your build output |
| PR validation fails on is-an.ai | `owner.email` does not match your public GitHub email | Set a public email on your GitHub profile and update the record |
| Record disabled | Suspected abuse or rule violation | Open an issue on the is-an.ai repository to dispute it |

If you put Cloudflare in front of the same setup, the failure mode changes. Our [Cloudflare and GitHub Pages guide](https://f9xr.org/dev9b/p/github-pages-custom-domain-cloudflare/) covers CNAME flattening, the Flexible SSL redirect loop, and the proxy settings that break certificate issuance.

## Security Tips Worth Following

GitHub's documentation is blunt about a few risks, and they apply here.

- **Add the domain to GitHub before creating DNS.** This prevents someone else from hosting a site on your subdomain in the gap.
- **Avoid wildcard DNS records.** A `*.my-project.is-an.ai` style record can open the door to subdomain takeover, even when verification is on.
- **Delete records you no longer use.** A CNAME pointing at GitHub for a repo you deleted is exactly what takeover attackers hunt for. Run `npx is-an-ai delete my-project` when a project dies.
- **Do not point a subdomain at an apex domain.** GitHub warns this can break HTTPS enforcement or stop the subdomain reaching your site.
- **Keep secrets out of the repo.** GitHub Pages is public hosting. Never commit API keys, even for a demo, and call model APIs through a backend you control.

## Is This Setup Right for Your AI Project?

GitHub Pages serves static files only. That suits landing pages, documentation, model demos that call an API, in-browser inference with WebAssembly or WebGPU, and portfolios. It does not run Python, Node servers, or anything that needs a secret on the server.

If you need a backend, a common pattern is the front end on GitHub Pages at `my-project.is-an.ai`, and the API on a serverless platform or a small VPS under a second name such as `api-my-project.is-an.ai`. Remember that a free subdomain is lent to you rather than owned. For prototypes and demos that is perfectly fine. Once money is involved, buy a domain you control and change one config value.

Prefer not to use GitHub at all? The is-an-ai CLI also has a `deploy` command that uploads a static build folder directly to your subdomain, with a 50 MB and 1,000 file limit. If you want another free static host, [Codeberg Pages](https://f9xr.org/dev9b/p/how-to-host-static-websites-codeberg-pages/) is a nonprofit alternative with custom domain support. If you are still building the product itself, our [Next.js SaaS starter kit guide](https://f9xr.org/dev9b/p/supastarter-nextjs-saas-starter-kit-guide/) covers the plumbing before the domain question comes up.

## Key Takeaways

- Connecting is-an.ai to GitHub takes two matching settings: a **custom domain** in GitHub Pages and a **CNAME record** on is-an.ai.
- The CNAME value is `YOUR-USERNAME.github.io`, never the repo name or a path.
- Add the custom domain on GitHub **before** creating the DNS record to avoid takeover risk.
- Register the record with the website, `npx is-an-ai register my-project -t CNAME -v YOUR-USERNAME.github.io`, or a pull request.
- Verify with `dig`, then enable **Enforce HTTPS** once GitHub allows it.
- A project repo moves from a `/repo-name/` path to the root of your domain, so reset your framework's base path.

## Conclusion

The setup is small once the order is clear: GitHub first, DNS second, HTTPS last. The two values that matter are the custom domain in the Pages settings and the CNAME target in the is-an.ai record. Everything else is waiting for DNS and fixing a base path.

For a demo or an early AI product, a free `is-an.ai` name is a cheap way to look finished. If the project grows, keep the migration path short by storing the site URL in one config value, then move to a domain you control when the stakes justify it.

If you find a step that has changed, the [contributor guide](https://f9xr.org/dev9b/contribute/) explains how to submit a fix. Every article here is checked against the standards in our [editorial policy](https://f9xr.org/dev9b/editorial-policy/). This guide was drafted with AI assistance and reviewed by the F9XR Team against GitHub's Pages documentation, the is-an.ai records repository, and the published is-an-ai CLI package.

## Frequently Asked Questions

### How do I connect an is-an.ai domain to GitHub Pages?

Enable GitHub Pages on your repo and enter `my-project.is-an.ai` as the custom domain under Settings, then Pages. Next, register a CNAME record for `my-project` on is-an.ai pointing to `YOUR-USERNAME.github.io`. After DNS propagates, turn on Enforce HTTPS.

### What CNAME value should I use for GitHub Pages?

Use your GitHub username or organization followed by `.github.io`, for example `jane.github.io`. Do not include the repository name or a path, and do not use the `*.pages.github.io` address shown in the Pages settings. The repository is chosen by the custom domain setting on GitHub.

### Can I point an is-an.ai subdomain to a specific repository?

Yes. Each repository with GitHub Pages enabled can have its own custom domain. Set `my-project.is-an.ai` as the custom domain in that repo's Pages settings, and create a CNAME record on is-an.ai pointing to your `USERNAME.github.io` address.

### How long does it take for an is-an.ai subdomain to work with GitHub?

Often a few minutes, but GitHub says DNS changes can take up to 24 hours to propagate. The Enforce HTTPS option can also take up to 24 hours to become available. Use `dig my-project.is-an.ai` to check progress.

### Why does my GitHub Pages site show a 404 on my custom domain?

The usual causes are a missing custom domain setting in the Pages settings, a deleted `CNAME` file on the publishing branch, or a CNAME record pointing at the wrong value. Re-enter the domain in GitHub and confirm the record points to `USERNAME.github.io`.

### Why do my CSS and images break after adding the custom domain?

Your site moved from `username.github.io/repo-name/` to the root of your domain, but your framework may still use `/repo-name/` as its base path. Reset the base path to `/` in your Vite, Astro, Next.js or Jekyll config, then rebuild and redeploy.
