You built the dashboard. The pricing page looks sharp. The login flow works on your laptop. Now you want to put it online without paying for a server, and GitHub Pages keeps coming up in every search result.

Good news: it works well for React projects. Bad news: most tutorials skip the parts that actually break in real SaaS projects, like client-side routing, environment variables, custom domains, and the fine print in GitHub's terms.

This guide covers all of it. You will deploy a React app built with Vite to GitHub Pages using GitHub Actions, fix the classic "404 on refresh" problem, connect a custom domain with HTTPS, and learn where a static host stops being enough for a SaaS product. Everything here was checked against GitHub's and Vite's current documentation in November 2026.

## Quick answer: how do you host a React app on GitHub Pages?

To host a React app on GitHub Pages, set the correct `base` path in your Vite config, push the project to a GitHub repository, switch the Pages source to **GitHub Actions** in repository settings, and add a workflow file that builds the project and deploys the `dist` folder. Your site goes live at `https://username.github.io/repo-name/` after the first successful run.

That is the short version. Here is the full one.

## Read this first: can you actually run a SaaS on GitHub Pages?

This is the part most guides leave out, so let us be straight about it.

GitHub's own [Pages documentation](https://docs.github.com/en/pages) says the service is not intended to be used as a free hosting service to run your online business, an e-commerce site, or any site primarily directed at facilitating commercial transactions or providing commercial software as a service. That wording matters if you are building a paid SaaS.

So what is a safe, sensible use?

| Use case | Fits GitHub Pages? | Notes |
|---|---|---|
| Landing page and marketing site for your SaaS | Yes | Static content is exactly what Pages is built for |
| Product documentation and changelog | Yes | Great fit |
| Public demo or prototype of the React frontend | Yes | Use mock data or a sandbox backend |
| MVP for validation, shared with testers | Usually fine | Keep it small and temporary |
| The production app that takes payments and serves paying customers | Risky | This is what the terms discourage |
| Anything handling passwords or card numbers directly on Pages | No | GitHub says not to use Pages for sensitive transactions |

**Practical advice:** use GitHub Pages for your frontend demo, docs, and marketing site while you validate the idea. When real revenue starts, move the production app to a host that explicitly allows commercial use, such as Cloudflare Pages, Netlify, or Vercel. Because your React build is just static files, moving later takes minutes, not days.

Also remember that GitHub Pages only serves static files. Your authentication, database, and payment logic must live somewhere else. More on that below.

## What you need before you start

You need a GitHub account, Node.js (an active LTS version) and npm, Git installed and configured, and a React project. A public repository is required because Pages on private repositories needs a paid GitHub plan.

If your project still uses Create React App, it will work too, but CRA is no longer actively developed. Vite is the recommended path for new projects and it is what we use here.

## Step 1: Create or prepare your React project

Starting from scratch? Scaffold a Vite and React app:
```bash
npm create vite@latest my-saas-app -- --template react
cd my-saas-app
npm install
npm run dev
```

Already have a project? Skip ahead. Just confirm that `npm run build` finishes without errors on your machine. If the build fails locally, it will fail in GitHub Actions too, and debugging remote builds is slower.

## Step 2: Set the correct base path in vite.config.js

This single setting causes more blank-page problems than anything else.

When you deploy to `https://username.github.io/my-saas-app/`, your site lives in a subfolder. Vite needs to know that so it generates correct asset URLs.
```js
// vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: '/my-saas-app/', // must match your repository name exactly
})
```

Two quick rules:

- **Project site** (`username.github.io/repo-name`): set `base` to `'/repo-name/'`, with slashes on both sides.
- **User site or custom domain** (`username.github.io` repo, or `app.yourdomain.com`): set `base` to `'/'`.

If you plan to use a custom domain later, you will change this to `'/'`. Keep that in mind.

## Step 3: Fix client-side routing (the "404 on refresh" problem)

Your React app is a single page application. Routes like `/dashboard` or `/settings/billing` only exist inside JavaScript. GitHub Pages has no idea about them, so refreshing on `/dashboard` returns a 404.

You have two reliable fixes.

### Option A: use HashRouter

Swap `BrowserRouter` for `HashRouter` from [React Router](https://reactrouter.com). URLs become `/#/dashboard`, and the server never sees the route part.
```jsx
import { HashRouter } from 'react-router-dom'

<HashRouter>
  <App />
</HashRouter>
```

It is not pretty, but it never breaks. Good for demos and internal tools.

### Option B: BrowserRouter with a 404.html fallback

If you want clean URLs, keep `BrowserRouter`, set its `basename`, and copy `index.html` to `404.html` after every build so GitHub Pages serves your app for unknown paths:
```jsx
<BrowserRouter basename="/my-saas-app/">
  <App />
</BrowserRouter>
```
```json
{
  "scripts": {
    "build": "vite build && cp dist/index.html dist/404.html"
  }
}
```

On Windows, use `copy dist\index.html dist\404.html` or a small Node script instead of `cp`.

**Trade-off to know about:** with Option B the server still responds with a 404 status code before your app loads. Users will not notice, but search engines might treat deep links less favorably. If organic search matters for those pages, consider prerendering them.

## Step 4: Handle environment variables safely

Vite exposes variables that start with `VITE_` to the browser. That means anything you put there is public. Read that again, because it is the most common security mistake in frontend SaaS projects.

Safe to expose in a Vite frontend:

- Public API base URL
- Supabase or Firebase public (anon) keys, which are designed to be public and protected by row level security rules
- Analytics IDs

Never expose secret API keys, database connection strings, Stripe secret keys, webhook secrets, or any admin or service role token.

Create a `.env` file for local development and add it to `.gitignore`:
```bash
# .env
VITE_API_URL=https://api.yourdomain.com
```

For the deployed build, store non-secret values as **repository variables** in GitHub (Settings, then Secrets and variables, then Actions, then Variables) and pass them to the build step, as shown in the workflow below.

## Step 5: Push your project to GitHub

Create a new repository on GitHub, then from your project folder run:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/my-saas-app.git
git push -u origin main
```

Double check that `node_modules` and `dist` are listed in `.gitignore`. Vite's default template already handles this.

## Step 6: Turn on GitHub Pages with GitHub Actions

Open your repository on GitHub. Go to **Settings**, then **Pages**. Under **Build and deployment**, open the **Source** dropdown and select **GitHub Actions**.

That is all you need to do here. GitHub will wait for a workflow to publish your site.

## Step 7: Add the deployment workflow

Create a file at `.github/workflows/deploy.yml`:
```yaml
name: Deploy React app to GitHub Pages

on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Node
        uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: npm

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build
        env:
          VITE_API_URL: ${{ vars.VITE_API_URL }}

      - name: Configure Pages
        uses: actions/configure-pages@v5

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./dist

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

A few notes from experience:

- **Use `npm ci`, not `npm install`.** It installs exactly what your lockfile says, so builds are repeatable.
- **Action versions move.** The versions above work, but newer major versions exist. Check the [official Vite static deploy guide](https://vite.dev/guide/static-deploy.html) for the versions it currently recommends and update when it suits you.
- **Pin carefully.** For extra supply chain safety, many teams pin actions to a full commit SHA instead of a version tag.

## Step 8: Push, watch, and verify

Commit the workflow and push to `main`:
```bash
git add .
git commit -m "Add GitHub Pages deploy workflow"
git push
```

Open the **Actions** tab in your repository and watch the run. When both the build and deploy jobs turn green, visit `https://YOUR-USERNAME.github.io/my-saas-app/`.

Test these before you celebrate:

- Hard refresh the home page
- Open a deep route directly in a new tab
- Open DevTools and check the Network tab for 404 errors on JS and CSS files
- Test on your phone

Every future push to `main` redeploys automatically. That is your whole CI/CD pipeline, for free.

Here is a real GitHub Pages deployment running the same setup. This blog, Dev9b, is a static site served by GitHub Pages from its own Actions workflow:

![The Dev9b blog homepage served from GitHub Pages, showing the sidebar navigation, hero section, and latest article card](https://raw.githubusercontent.com/f9xr/dev9b/master/content/post/host-react-saas-github-pages/github-pages-site.jpg)

## The quick alternative: deploy with the gh-pages package

If you do not want a workflow file, the `gh-pages` npm package pushes your build folder to a `gh-pages` branch:
```bash
npm install --save-dev gh-pages
```

Add these scripts to `package.json`:
```json
{
  "scripts": {
    "predeploy": "npm run build",
    "deploy": "gh-pages -d dist"
  }
}
```

Run `npm run deploy`, then set the Pages source to **Deploy from a branch** and pick `gh-pages`.

It works, but GitHub Actions is the better long term choice. The Actions method deploys on every push, keeps built files out of your git history, and does not count against the soft limit of 10 builds per hour that applies to branch-based Pages builds.

## Connect a custom domain and HTTPS

A `username.github.io/repo` URL does not look like a product. Here is how to use your own domain.

For an apex domain (`yourdomain.com`), create four A records pointing to GitHub's Pages IP addresses:
```
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

For a subdomain such as `app.yourdomain.com` or `www.yourdomain.com`, create a CNAME record that points to `YOUR-USERNAME.github.io`.

Then go to **Settings**, then **Pages**, enter your domain under **Custom domain**, and save it. Wait for the DNS check to pass, then tick **Enforce HTTPS**. GitHub issues the certificate through Let's Encrypt automatically. The [official custom domain guide](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site) has the full DNS table if you need it.

Update your project too:

- Change `base` in `vite.config.js` to `'/'`.
- Remove the `basename` from `BrowserRouter` if you set one.
- Add a file named `CNAME` containing only your domain to the `public/` folder, so it ships with every build.

Want a deeper walkthrough with DNS and proxy settings? Our guide on [connecting a GitHub Pages site to a custom domain with Cloudflare](https://f9xr.org/dev9b/p/github-pages-custom-domain-cloudflare/) covers the tricky parts, and [how to create a Cloudflare subdomain for GitHub Pages](https://f9xr.org/dev9b/p/how-to-create-cloudflare-subdomain-github-pages/) is handy if you only need something like `app.yourdomain.com`. No domain budget yet? Browse our [list of free subdomains for developers](https://f9xr.org/dev9b/p/free-subdomains-for-developers-list/).

## Give your static frontend a real backend

A SaaS needs users, data, and payments. GitHub Pages gives you none of that, so your React app talks to external services through APIs.

![Diagram](https://mermaid.ink/img/Zmxvd2NoYXJ0IExSCiAgICBBW1JlYWN0IGFwcDxici8-Vml0ZSBidWlsZF0gLS0-IEJbZGlzdCBzdGF0aWMgZmlsZXNdCiAgICBCIC0tPiBDW0dpdEh1YiBBY3Rpb25zXQogICAgQyAtLT4gRFtHaXRIdWIgUGFnZXMgQ0ROXQogICAgRCAtLT4gRVtCcm93c2VyXQogICAgRSAtLT4gRltTdXBhYmFzZSBBdXRoIGFuZCBEQl0KICAgIEUgLS0-IEdbU2VydmVybGVzcyBBUEldCiAgICBHIC0tPiBIW1N0cmlwZV0?bgColor=FFFFFF)
| Need | Common options |
|---|---|
| Authentication | Supabase Auth, Firebase Auth, Clerk, Auth0 |
| Database | Supabase (Postgres), Firebase Firestore, PlanetScale, Neon |
| Server logic | Cloudflare Workers, AWS Lambda, Supabase Edge Functions |
| Payments | Stripe Checkout or Payment Links (hosted by Stripe) |
| Email | Resend, Postmark, Amazon SES |

Three rules keep this setup healthy:

1. **Keep secrets on the server side.** Your serverless function holds the Stripe secret key. The React app only calls the function.
2. **Configure CORS.** Allow your Pages origin (for example `https://app.yourdomain.com`) in your API's CORS settings, and nothing broader.
3. **Use row level security** if your database is exposed directly to the browser, as with Supabase.

If you are exploring full stack options beyond a static host, our write-ups on the [Supastarter Next.js SaaS starter kit](https://f9xr.org/dev9b/p/supastarter-nextjs-saas-starter-kit-guide/) and [building a SaaS app with Puter.js](https://f9xr.org/dev9b/p/puter-js-build-saas-app-guide/) show two different approaches.

## SEO and AEO tips for a React single page app on GitHub Pages

Search engines and AI answer engines like ChatGPT, Gemini, Claude, and Perplexity read your HTML. A pure client-side React app ships an almost empty HTML file, which hurts discoverability. Fix that with these steps.

**1. Prerender your public pages.** Landing, pricing, features, and blog pages should be real HTML at build time. Tools like Vike (formerly `vite-plugin-ssr`), `react-snap`, or a framework such as Astro or Next.js static export can do this. Keep the logged in dashboard client-rendered, since it does not need to rank.

**2. Set unique titles and meta descriptions per route.** Use `react-helmet-async` or the head management built into your framework.

**3. Add structured data.** JSON-LD for `Organization`, `SoftwareApplication`, and `FAQPage` helps both search engines and AI systems understand what you offer.

**4. Publish `sitemap.xml` and `robots.txt`.** Put them in `public/` so they are copied into the build output.

**5. Write answer-first content.** For every key page, put a clear, direct answer in the first two sentences, then expand. This is the format AI search tools tend to quote.

**6. Ping search engines after deploys.** IndexNow can notify participating search engines when content changes. See our guide to [setting up and pinging an IndexNow API key](https://f9xr.org/dev9b/p/setup-and-ping-indexnow-api-key/).

For more on search basics, our [Hugo SEO guide](https://f9xr.org/dev9b/p/hugo-seo-guide/) explains techniques that apply to any static site.

## Common errors and how to fix them

| Problem | Likely cause | Fix |
|---|---|---|
| Blank white page | Wrong `base` value | Set `base` to `'/repo-name/'` or `'/'` for custom domains, then redeploy |
| JS and CSS return 404 | Same `base` issue, or wrong case in repo name | Match the repository name exactly, including capitalization |
| 404 when refreshing a route | Client-side routing on a static host | Use `HashRouter`, or add the `404.html` fallback |
| Workflow fails with a permissions error | Missing `pages: write` or `id-token: write` | Confirm the `permissions` block from Step 7 |
| Deploy job never starts | Pages source not set to GitHub Actions | Settings, Pages, Source, GitHub Actions |
| Custom domain disappears after deploy | No `CNAME` file in the build | Add `CNAME` to `public/` |
| Old version still showing | Browser or CDN caching | Hard refresh, then check that the Actions run finished |
| Environment variable is `undefined` | Missing `VITE_` prefix or not passed in the workflow | Rename the variable and add it to the build step `env` |

## GitHub Pages limits worth knowing

According to [GitHub's Pages limits documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits), published Pages sites may be no larger than 1 GB, source repositories have a recommended limit of 1 GB, deployments time out after 10 minutes, and sites have a soft bandwidth limit of 100 GB per month. Rate limits can apply too.

For most React frontends, a build of a few megabytes sits far below all of this. Still, optimize anyway:

- Compress and resize images, and prefer WebP or AVIF
- Lazy load heavy routes with `React.lazy`
- Remove unused dependencies and run a bundle analyzer once in a while
- Use SVG icons instead of large icon fonts. Our comparison of [Lucide vs Font Awesome](https://f9xr.org/dev9b/p/lucide-vs-font-awesome/) can help you choose

## When to move beyond GitHub Pages

GitHub Pages is a great starting line. Plan your move when any of these appear:

- You start charging customers
- You need server side rendering or API routes next to your frontend
- You want preview deployments for every pull request
- You need redirects, headers, or edge rules that Pages does not support
- Traffic approaches the bandwidth guidance

| Platform | Best for | Trade-off |
|---|---|---|
| GitHub Pages | Demos, docs, landing pages, open source projects | Static only, commercial SaaS use discouraged |
| Cloudflare Pages | Fast global static hosting with edge functions | Another dashboard to learn |
| Netlify | Easy Git based deploys, forms, functions | Free tier limits can change |
| Vercel | Next.js and React with server features | Pricing grows with team size and usage |
| Codeberg Pages | Privacy minded, non-profit hosting | Smaller ecosystem |

Curious about alternatives to GitHub? We covered [hosting static websites on Codeberg Pages](https://f9xr.org/dev9b/p/how-to-host-static-websites-codeberg-pages/) separately. And if you work with other static frameworks, see how to [deploy Astro to GitHub Pages](https://f9xr.org/dev9b/p/how-to-deploy-astro-github-pages/) or follow the [Hugo and GitHub Pages setup](https://f9xr.org/dev9b/p/hugo-github-pages-setup/).

## Pre-launch checklist

Run through this list before you share the link:

- [ ] `base` path matches your repository name or custom domain
- [ ] Routing tested with a hard refresh on a deep link
- [ ] No secret keys inside `VITE_` variables
- [ ] `CNAME` file in `public/` (custom domain users)
- [ ] HTTPS enforced in Pages settings
- [ ] Unique title and meta description on every public page
- [ ] `sitemap.xml` and `robots.txt` published
- [ ] Open Graph image set for social sharing
- [ ] Lighthouse score checked on mobile
- [ ] Backend CORS limited to your real domain

## Frequently asked questions

### Can I host a React app on GitHub Pages for free?

Yes. GitHub Pages is free for public repositories on GitHub Free, and it serves static files, which is exactly what a React build produces. Private repositories need a paid GitHub plan to use Pages. Bandwidth and size limits apply, but small and medium frontends stay well within them.

### Is it allowed to run a SaaS product on GitHub Pages?

Not as your primary commercial platform. GitHub's documentation states that Pages is not intended to run an online business or provide commercial software as a service. It is fine for documentation, landing pages, demos, and prototypes. Move production apps that take payments to a host that permits commercial use.

### Why does my React app show a blank page on GitHub Pages?

The most common cause is a wrong `base` setting in `vite.config.js`. If your site lives at `username.github.io/repo-name/`, set `base` to `'/repo-name/'`. For a custom domain or a user site, set it to `'/'`. Rebuild and redeploy after changing it.

### How do I fix the 404 error when I refresh a React Router page on GitHub Pages?

GitHub Pages cannot serve routes that exist only in JavaScript. Either switch to `HashRouter`, or keep `BrowserRouter` and copy `index.html` to `404.html` during the build so Pages loads your app for unknown paths.

### Should I use gh-pages or GitHub Actions to deploy React?

Use GitHub Actions. It deploys automatically on each push, avoids committing build output to a branch, and is the method Vite's documentation recommends. The `gh-pages` package is a quick option for one-off deployments.

### How do I add a custom domain to a React app on GitHub Pages?

Add the domain under Settings, then Pages. At your DNS provider, create four A records for an apex domain pointing to GitHub's Pages IPs, or a CNAME record pointing to `username.github.io` for a subdomain. Add a `CNAME` file to your `public/` folder, set Vite `base` to `'/'`, and enable Enforce HTTPS.

## Key takeaways

- GitHub Pages hosts static React builds for free, and GitHub Actions is the cleanest way to deploy them.
- Set `base` correctly in `vite.config.js`. It fixes most blank page and 404 asset problems.
- Single page apps need a routing fix on Pages. Use `HashRouter` or a `404.html` fallback.
- Anything prefixed with `VITE_` is public. Never put secrets in it.
- GitHub's terms discourage running a commercial SaaS on Pages. Use it for demos, docs, and marketing, and move production to a host that allows commercial use.
- Auth, database, and payments must live in external services your React app calls through APIs.
- Custom domains need DNS records, a `CNAME` file in `public/`, and **Enforce HTTPS** turned on.
- Prerender public pages and add structured data so search engines and AI answer engines can read your content.

## Conclusion

Deploying a React project to GitHub Pages takes about ten minutes once you know the four things that trip people up: the `base` path, client-side routing, public environment variables, and the terms around commercial use. Get those right and you have a free, fast, automatically deployed frontend for your SaaS idea.

Treat it as the launchpad rather than the permanent home. Validate the idea, collect feedback, and when customers start paying, move your build to a commercial friendly host. Your React code will not need to change.

This guide was written by the F9XR Team with AI assistance, then checked against primary documentation and built with our own React projects. If you spot an error, [suggest a change through our contributor guide](https://f9xr.org/dev9b/contribute/) or read how we handle corrections in our [editorial policy](https://f9xr.org/dev9b/editorial-policy/).
