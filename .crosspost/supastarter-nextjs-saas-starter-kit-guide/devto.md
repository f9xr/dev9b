---
title: 'Supastarter Explained: Build Your Next.js SaaS Faster'
published: false
description: What is supastarter? See features, pricing and the stack, then follow a step-by-step guide to set it up and build your Next.js SaaS the smart way.
tags: saastools, indiehackers, javascript, tutorial
cover_image: https://raw.githubusercontent.com/f9xr/dev9b/master/content/post/supastarter-nextjs-saas-starter-kit-guide/cover.jpg
canonical_url: https://f9xr.org/dev9b/p/supastarter-nextjs-saas-starter-kit-guide/
---

Every Next.js SaaS starter kit begins the same way: a sharp idea, a free weekend, and a blank folder. By Sunday night you have a login page that sort of works, a half-finished Stripe webhook, and a growing list of things you still need. Password reset. Team invites. Email templates. A pricing page. An admin panel.

None of that is your product. It is the plumbing every SaaS needs before a customer can use the one feature that matters.

That is the problem a Next.js SaaS starter kit solves, and [supastarter](https://supastarter.dev/?atp=f9xr) is one of the more complete options. This guide covers what is inside, what it costs, where it falls short, and how to go from purchase to a running app.

> **NOTE** â€” Disclosure
>
> Some links in this article are affiliate links. If you buy through them, we may earn a commission at no extra cost to you. The technical details below come from the official documentation and public pricing page.
>

## What supastarter actually gives you

supastarter is a fullstack SaaS boilerplate built by Jonathan Wilke. You buy it once, get access to a private repository, and build your product on top of that code. It is not a hosted service and it does not add a runtime dependency to your app.

The Next.js version uses the App Router and React Server Components. It ships as a Turborepo monorepo with separate apps for the marketing site, the product, the documentation, and email previews.

The commercial license allows unlimited projects. That matters if you run an agency or build several small products, because you are not buying one app. You are buying a foundation you can reuse.

The catch is the usual one with starter kits. You inherit someone else's architecture. better-auth, Hono, oRPC, Prisma or Drizzle, and a specific folder layout are already chosen. If those choices match how you like to build, you save weeks. If you want a different stack, you will spend that time swapping parts.

## What the Next.js SaaS starter kit includes

The docs list a broad feature set. A few areas deserve a closer look before you pay.

| Area | What you get |
|---|---|
| Marketing site | Landing page, pricing, MDX blog with i18n, changelog, contact form, legal pages and SEO metadata |
| Authentication | better-auth with email and password, passkeys, magic links, OAuth, 2FA, password reset and email verification |
| Organizations | Teams, invites, owner and member roles, organization settings and data isolation |
| Payments | Stripe, Lemon Squeezy, Creem, Polar and Dodo Payments, with subscriptions, one-time plans, webhooks and a billing portal |
| Database | Prisma or Drizzle ORM, PostgreSQL by default, plus guides for Neon, Supabase, PlanetScale, Turso and Railway |
| API layer | Hono with oRPC, TanStack Query and generated OpenAPI documentation |
| Storage | S3-compatible storage, including AWS S3, Cloudflare R2, DigitalOcean Spaces, SeaweedFS, MinIO and Supabase Storage |
| Email | React Email with Tailwind styling, plus Resend, Postmark and Nodemailer providers |
| AI | Vercel AI SDK integration, a chatbot with history, and text, image and audio model support |
| Background jobs | trigger.dev, Upstash QStash and BullMQ |
| Deployment | Guides for Vercel, Render, Fly.io, Netlify, Docker, Coolify and Railway |

The monorepo split is worth understanding because it shapes where you work:

| App | Purpose |
|---|---|
| `apps/marketing` | Public site, blog, changelog, legal pages and sitemap |
| `apps/saas` | Authentication, onboarding, organizations, billing, admin and API routes |
| `apps/docs` | Documentation site |
| `apps/mail-preview` | Email previews during development |

Keeping the marketing site separate from the product is a sensible default. The public pages can cache and deploy on their own schedule, while the authenticated app stays focused.

The authentication story has improved since the early versions. better-auth now covers passkeys and two-factor authentication in addition to the usual password and OAuth flows. The organization model is also ready on day one, which is the part most teams underestimate. Adding teams and data isolation after you have paying customers is much harder than starting with them.

On the API side, Hono and oRPC give you typed endpoints and a typed client. If you have used tRPC, the idea will feel familiar. The difference is that oRPC is built around OpenAPI, so you also get a generated API description you can inspect or share.

## What it costs in November 2026

The official pricing page lists three one-time plans. There is no subscription.

| Plan | Price | Seats | What stands out |
|---|---|---|---|
| Solo | $349 | 1 developer | Unlimited personal projects, commercial use, lifetime updates |
| Startup | $799 | 5 developers | Priority support and a 60-minute consulting call |
| Agency | $1,499 | 10 developers | White-label use, client projects, private Discord access and a consulting call |

Prices change, and the site was running a promotion at the time of writing. Treat the table as a snapshot, not a quote. Check the [current pricing](https://supastarter.dev/?atp=f9xr) before you decide.

A fair way to judge the price is to compare it with your own time. If auth, teams, billing and email would take you three weeks, the Solo plan is cheap. If you are building a single-user tool with one login method, it is more than you need.

## Where it fits, and where it does not

supastarter makes the most sense for multi-tenant B2B products. The organizations, roles, invites and billing pieces are already connected, and those are the parts that usually turn a two-week MVP into a two-month project.

It also fits indie developers who want to launch several products without rebuilding the same foundation each time. The unlimited-projects license is the reason.

It fits less well in three cases.

First, a tiny internal tool. You will spend more time deleting unused modules than building.

Second, a team with strong opinions about auth, API design or database access. You can replace any part, but the value comes from keeping the defaults.

Third, a product that needs a stack the kit does not support. Confirm the framework before you buy, because the marketing site, docs and pricing selector have not always listed the same set.

We have not shipped a production app on supastarter ourselves. This guide follows the official documentation and pricing page, and the judgment calls are ours. That is worth saying plainly, because a starter kit review is easy to turn into a sales page.

## How to go from purchase to a running app

The official setup guide is the source of truth. Commands and file locations change between releases, so keep the [supastarter documentation](https://supastarter.dev/docs) open while you work.

### Prerequisites

You need Node.js 20 or newer, Git, pnpm, a code editor, and a database connection string. PostgreSQL is the default, and the docs also cover MySQL and SQLite.

### 1. Create the project

After purchase you get access to the private repository. The quickest start is the CLI:
```bash
npx supastarter new my-awesome-project
```

The command clones the repository, asks for your database details, installs dependencies and sets up the database. If it fails, the manual path is to clone the repository and run `pnpm install`, then copy `.env.local.example` to `.env.local` and fill in `DATABASE_URL`.

Never commit that file. If you have not enabled secret scanning yet, our guide to [GitHub security setup](https://f9xr.org/dev9b/p/what-is-gh-secure-setup-guide/) shows how to catch a leaked key before it reaches a public repo. Your payment and email keys will live in the same file.

### 2. Pick your ORM and database

Prisma is the default in the setup docs. Drizzle is supported through a different export in `packages/database/index.ts` and an adapter change in `packages/auth/auth.ts`.

Choose one before you write models. Switching later is possible, but it touches your schema, your auth adapter and every query in between.

The database provider matters less. PostgreSQL is the safest default, and the docs include provider guides for [Neon, Supabase, PlanetScale, Turso and Railway](https://supastarter.dev/docs/nextjs/database/providers).

### 3. Configure email

Pick a mail provider by changing the export in `packages/mail/provider/index.ts`. Resend needs `RESEND_API_KEY`. Postmark needs `POSTMARK_SERVER_TOKEN`. Nodemailer needs the host, port and credentials.

For local work, the console provider prints emails to your terminal instead of sending them. The mail preview app lets you edit templates without triggering a real signup.

### 4. Connect a payment provider

Choose one of the five supported providers and export it in the payments module. Create your products and plans in the provider dashboard, then add the keys and plan IDs to your environment and plan configuration.

If global tax compliance is a concern, start with one of the merchants of record, such as Creem or Lemon Squeezy. If you want the most familiar developer experience, Stripe is still the default choice for most teams.

Test the full lifecycle in sandbox mode before launch: signup, upgrade, downgrade, cancellation and a failed payment. A broken webhook is the kind of bug that costs real money.

### 5. Push the schema and start the app
```bash
pnpm --filter database push
pnpm --filter database generate
pnpm --filter scripts create:user
pnpm dev
```

The exact scripts can differ if you use Drizzle, so check the database docs for your path. `pnpm dev` can start several apps at once, including the marketing site, the SaaS app and the docs.

### 6. Customize the marketing site

Edit the landing page, pricing page and blog in `apps/marketing`. Replace the sample copy with your own message. Keep the SEO basics tight, and do not ship a generic template with your logo pasted on top. Our guide to [removing AI slop from website design](https://f9xr.org/dev9b/p/how-to-de-ai-slop-website-design/) covers the visual side, and the [Hugo SEO guide](https://f9xr.org/dev9b/p/hugo-seo-guide/) is useful even if you are not using Hugo.

### 7. Build the feature that makes you different

Work inside `apps/saas`. A few habits will keep the codebase manageable:

- Scope every new table by organization so tenant data stays separate.
- Add endpoints through Hono and oRPC, then call them with TanStack Query.
- Gate paid features with the paywall components instead of scattering plan checks through the UI.
- Follow the feedback widget recipe in the docs. It walks from database to UI and is a good template for your first feature.

Here is a small Prisma model that follows the multi-tenant pattern:
```prisma
model Project {
  id             String   @id @default(cuid())
  name           String
  organizationId String
  createdAt      DateTime @default(now())

  @@index([organizationId])
}
```

Adapt the field names to the conventions already in the repo. The important part is the organization index. It keeps tenant queries from scanning every row as you grow.

### 8. Deploy and keep up with updates

Run the included Playwright tests where they apply, then deploy. The docs cover Vercel, Render, Fly.io, Netlify, Docker, Coolify and Railway. If you use a custom domain behind Cloudflare, our [GitHub Pages and Cloudflare guide](https://f9xr.org/dev9b/p/github-pages-custom-domain-cloudflare/) explains the DNS side, and the same ideas apply to most hosts.

Before your first release, set the supastarter repository as an upstream remote. That is how you pull fixes and new features later. Commit small changes, keep customizations in clearly separated files, and read the changelog before merging a large update.

## How it compares with other starter kits

| Kit | Starting price | Stack highlights | Best fit |
|---|---|---|---|
| supastarter | $349 | Next.js, Nuxt and other framework codebases, better-auth, Prisma or Drizzle, Hono, five payment providers | Multi-tenant B2B SaaS and teams that want a broad foundation |
| ShipFast | $199 | Next.js, MongoDB or Supabase, Stripe, Google OAuth | Solo founders who want a lean start |
| MakerKit | $349 | Next.js with Supabase, Drizzle or Prisma variants | Teams that want a kit per database choice |
| TurboStarter | $179 | Web, mobile and browser extension in one repo | Products that need several surfaces |

Prices come from public pages and can change. The useful question is not which kit has the most features. It is which kit matches the parts you do not want to build.

If you are still deciding whether to use a kit at all, our comparison of [vibe coding and vibe engineering](https://f9xr.org/dev9b/p/vibe-coder-vs-vibe-engineer/) looks at the trade-off between speed and understanding. A starter kit tilts the balance toward speed, and you still need to understand the code you ship.

## Launch checklist

| Task | Check |
|---|---|
| Real payment keys and webhooks tested | |
| Email domain verified with SPF, DKIM and DMARC | |
| Legal pages edited for your business | |
| Analytics and Sentry installed | |
| Admin account secured with a strong password | |
| Database backups enabled | |
| Sitemap submitted to Google Search Console | |
| Pricing page tested on mobile | |
| Upgrade, downgrade and cancel flows tested | |
| Environment variables stored in your host's secret manager | |

If you want to stress-test the launch before real users arrive, our walkthrough on [setting up and testing a SaaS launch](https://f9xr.org/dev9b/p/mirofish-repo-setup-test-saas-launch/) covers the rehearsal. If referrals are part of your growth plan, the [guide to affiliate software for SaaS](https://f9xr.org/dev9b/p/affonso-affiliate-software-saas-guide/) explains the moving parts.

One more option deserves a mention. If your product is mostly AI features and you want to avoid backend billing entirely, our [Puter.js SaaS guide](https://f9xr.org/dev9b/p/puter-js-build-saas-app-guide/) describes a keyless, user-pays model. It solves a different problem than supastarter, and the two approaches can even be compared before you commit.

## Key Takeaways

- supastarter is a paid SaaS starter kit with auth, organizations, billing, email, storage, AI features, i18n and admin tools already wired.
- The Next.js version is a Turborepo monorepo with separate apps for marketing, product, docs and mail previews.
- Pricing is one-time: $349 for Solo, $799 for Startup and $1,499 for Agency at the time of writing, with lifetime updates.
- The value is highest for multi-tenant B2B products, where teams and billing are hard to add later.
- It is closed source and opinionated, so check the license and the stack before you build a business on it.

## Frequently asked questions

### What is supastarter?

supastarter is a paid, production-ready SaaS starter kit with authentication, organizations, subscription billing, email, storage, AI features, internationalization and an admin panel. It gives you a working codebase so you can spend your time on the product instead of rebuilding the same foundation.

### Which frameworks does supastarter support?

supastarter ships separate codebases for Next.js, Nuxt, SvelteKit and TanStack Start. The pricing selector currently lists Next.js, Nuxt and TanStack Start, so confirm the framework you need on the official site before buying.

### How much does supastarter cost?

The official site lists a one-time price of $349 for Solo, $799 for Startup and $1,499 for Agency. All plans include lifetime updates, and the license allows unlimited projects. Promotions and prices change, so check the site before you buy.

### Is supastarter open source?

No. supastarter is a premium starter kit under a commercial license. You get the full source code after purchase and can modify it, but it is not open source in the traditional sense.

### Which payment providers does supastarter support?

It supports Stripe, Lemon Squeezy, Creem, Polar and Dodo Payments. The billing layer covers monthly, yearly and one-time plans, upgrades, cancellations, webhooks and a billing portal.

### How do I set up supastarter?

Install Node.js 20 or newer, Git and pnpm, create a database, then run `npx supastarter new my-awesome-project`. Set `DATABASE_URL` and your mail and payment variables in `.env.local`, push the schema with `pnpm --filter database push`, and start the app with `pnpm dev`.

## Conclusion

A starter kit will not build your business. It can remove weeks of repetitive work between your idea and your first paying customer, and that is the only promise worth judging it on.

If you want a Next.js foundation with teams, billing and an admin panel already in place, supastarter is a strong candidate. Try the [live demo](https://demo.supastarter.dev), read the [documentation](https://supastarter.dev/docs), and check the current license and pricing before you buy.

If you want to share your own build notes with the Dev9b community, read the [Contributor Guide](https://f9xr.org/dev9b/contribute/) and our [Editorial Policy](https://f9xr.org/dev9b/editorial-policy/). Both explain how we review submissions.

## Sources

- supastarter official site, pricing and feature pages, accessed November 2026
- supastarter Next.js documentation, introduction, tech stack and setup guides
- supastarter live demo
- Prisma supported databases reference
- Drizzle ORM documentation

*Disclosure: This article was drafted with AI assistance and reviewed and edited by the F9XR Team. Product details, prices and framework availability change often. Verify current facts on the official supastarter site before you buy.*
