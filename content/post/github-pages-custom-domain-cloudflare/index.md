---
title: "Point a Cloudflare Domain to GitHub Pages in 15 Min"
description: "Connect your Cloudflare domain to GitHub Pages the right way: A records, CNAME flattening, SSL settings, and the redirect loop fix developers keep hitting."
slug: github-pages-custom-domain-cloudflare
date: 2026-09-16
image: cover.jpg
author: dev9b
keywords:
    - github pages custom domain
    - cloudflare dns
    - cname flattening
    - ssl full strict
    - github pages https
categories:
    - Tutorials
tags:
    - github-pages
    - cloudflare
    - custom-domain
    - dns
    - devops
    - hugo
    - ssl-certificate
    - static-site-hosting
    - developer-setup
    - github-actions
draft: false
math: false
faq:
    - question: "Can I use Cloudflare's proxy with GitHub Pages?"
      answer: "Yes, but set up DNS as DNS only (grey cloud) first so GitHub can issue its Let's Encrypt certificate, then switch the records to proxied. Set Cloudflare's SSL/TLS mode to Full (strict); Flexible causes an infinite redirect loop."
    - question: "What A records does GitHub Pages use for an apex domain?"
      answer: "Four IPv4 records on @: 185.199.108.153, 185.199.109.153, 185.199.110.153, and 185.199.111.153. For IPv6, add AAAA records from 2606:50c0:8000::153 through 2606:50c0:8003::153."
    - question: "Why does my GitHub Pages custom domain keep disappearing?"
      answer: "Your build overwrites the CNAME file GitHub places in the published branch. Add it to your source instead: static/CNAME for Hugo, public/CNAME for Node builds, or the repository root for Jekyll. With peaceiris/actions-gh-pages, pass the cname parameter."
    - question: "How long does it take for a GitHub Pages custom domain to work?"
      answer: "DNS propagation through Cloudflare takes minutes to at most 24 hours, then GitHub issues the TLS certificate within minutes to about an hour. If Enforce HTTPS stays greyed out after an hour, the DNS configuration is likely wrong."
    - question: "Why am I getting ERR_TOO_MANY_REDIRECTS on my GitHub Pages site?"
      answer: "Cloudflare's SSL/TLS mode is set to Flexible. Cloudflare connects to GitHub over HTTP, GitHub redirects to HTTPS, and the loop repeats. Change the mode to Full (strict) under SSL/TLS then Overview."
    - question: "Can I use a custom domain with a GitHub Pages project site?"
      answer: "Yes. A project repository can serve at a root domain or subdomain. Add the domain under Settings then Pages and point a DNS CNAME record at yourusername.github.io with no path appended."
    - question: "Do I need to pay Cloudflare to connect a domain to GitHub Pages?"
      answer: "No. Cloudflare's free plan includes DNS hosting, CNAME flattening, universal SSL, and redirect rules. GitHub Pages is free for public repositories. The only cost is the domain registration."
    - question: "Should I use Cloudflare Pages instead of GitHub Pages?"
      answer: "Cloudflare Pages builds from the same GitHub repo, adds preview deployments per pull request, and removes certificate coordination because one vendor handles DNS and hosting. The tradeoffs are build minute limits and different routing conventions."
    - question: "Will switching to a custom domain hurt my SEO?"
      answer: "Expect a short-term dip while search engines recrawl. GitHub 301-redirects the old github.io URLs to your custom domain, passing most link equity. Submit the new domain in Search Console and update baseURL to recover faster."
    - question: "Can I point multiple domains at one GitHub Pages site?"
      answer: "GitHub Pages accepts only one custom domain per repository. To serve additional domains, add them as zones in Cloudflare and create a Redirect Rule issuing a 301 to your canonical hostname."
---
You shipped the site. The build is green, GitHub Actions is humming, and `yourname.github.io/project` loads perfectly. Then you look at that URL and think: nobody is going to type that into a keynote slide.

So you buy a domain. You move DNS to Cloudflare because it is free, fast, and the dashboard does not look like it was designed in 2009. And then you hit the wall that every developer hits at least once: the site loads over HTTP but not HTTPS, or Chrome throws `ERR_TOO_MANY_REDIRECTS`, or GitHub sits there for two days saying "Certificate not yet created."

None of that is a bug. It is the predictable result of two proxies both trying to terminate TLS at the same time, plus one checkbox nobody tells you about.

<!--more-->

This guide walks through the whole path: buying or transferring the domain, wiring up DNS records in Cloudflare, telling GitHub Pages about your domain, forcing HTTPS, and then turning the orange cloud back on safely once the certificate exists. Every command is copy-paste ready, and the troubleshooting table at the end covers the five failures that account for roughly 90 percent of the support threads on this topic.

## Key Takeaways

| Point | What it means for you |
|---|---|
| **Order matters** | Add the domain in GitHub Pages **first**, then create DNS records in Cloudflare. Reversing this opens a subdomain takeover window. |
| **Apex needs four A records** | `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`. Add the four AAAA records too if you want IPv6. |
| **Start with DNS only** | Set the grey cloud (DNS only) until GitHub issues the Let's Encrypt certificate. Proxying too early blocks the ACME challenge. |
| **Never use Flexible SSL** | Flexible mode causes the infinite redirect loop. Use **Full (strict)**. |
| **CNAME file is source of truth** | GitHub writes a `CNAME` file into your repo. If your build wipes it, the domain unsets itself on every deploy. |
| **Propagation is not instant** | DNS can take up to 24 hours, though Cloudflare usually settles in minutes. Certificate issuance takes up to an hour after DNS resolves. |
| **Project sites work too** | A repository like `github.com/you/dev9b` can live at a subdomain or root domain, not just at `/dev9b`. |

## What You Need Before You Start

Nothing exotic, but skipping any of these will cost you time later.

* A GitHub repository with GitHub Pages already enabled and deploying successfully. If you are still setting that part up — including the GitHub Actions workflow and `baseURL` — our [Hugo on GitHub Pages setup guide](/p/hugo-github-pages-setup/) covers it end to end.
* A registered domain name. Any registrar works: Cloudflare Registrar, Namecheap, Porkbun, Squarespace, Hostinger. The registrar just has to let you change nameservers.
* A free Cloudflare account.
* Admin permission on the repository. Repository settings for Pages are admin only.
* `dig` or `nslookup` on your machine for verification. Windows users can use `Resolve-DnsName` in PowerShell.

> [!IMPORTANT]
> Custom domains on GitHub Pages are available for **public** repositories on the free plan. Private repositories need GitHub Pro, Team, or Enterprise Cloud to publish a Pages site at all.

## Step 1: Move Your Nameservers to Cloudflare

If your DNS already lives at Cloudflare, skip ahead.

1. Log in to Cloudflare and click **Add a domain**.
2. Type the apex domain, without `www` and without `https://`. So `example.com`, not `www.example.com`.
3. Choose the **Free** plan. It includes unlimited DNS queries, universal SSL, and CNAME flattening — the feature that makes this whole setup pleasant.
4. Cloudflare scans your existing records and shows you two assigned nameservers, something like `arnold.ns.cloudflare.com` and `pola.ns.cloudflare.com`. These are unique per account, so use the pair Cloudflare gives you.
5. Go to your registrar's control panel, find the nameserver section, delete the existing entries, and paste in the Cloudflare pair. Leave any third and fourth nameserver fields empty.
6. Wait. Registrar nameserver changes usually propagate in 5 to 30 minutes, occasionally up to 24 hours. Cloudflare emails you when the zone goes active.

**Practical tip:** if you bought the domain at Cloudflare Registrar, nameservers are already correct and the zone is active from the moment you buy it. That removes an entire failure category.

## Step 2: Add the Custom Domain in GitHub Pages First

This is the step people do last, and doing it last is a real security problem.

If you point DNS at GitHub's IP addresses before claiming the domain inside your repository, GitHub does not know who the domain belongs to. Someone else can claim it on their Pages site and serve content from your hostname. [GitHub's own documentation](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site) flags this. Claim first, point DNS second.

1. Open your repository on GitHub.
2. Go to **Settings** then **Pages** in the left sidebar.
3. Under **Custom domain**, type the exact hostname you intend to serve from: `example.com` for an apex, or `blog.example.com` for a subdomain.
4. Click **Save**.

GitHub will immediately report a DNS check failure. That is expected. You have not created the records yet.

Behind the scenes, GitHub commits a plain text file named `CNAME` to the root of your publishing branch containing a single line with your domain. Remember this file. It comes back to bite people in Step 6.

## Step 3: Create the DNS Records in Cloudflare

Open your Cloudflare zone and go to the **DNS** tab, then **Records**.

Which records you create depends on where you want the site to live.

### Option A: Apex Domain (example.com)

Create four `A` records, all with the name `@`:

| Type | Name | IPv4 address | Proxy status | TTL |
|---|---|---|---|---|
| A | @ | 185.199.108.153 | DNS only | Auto |
| A | @ | 185.199.109.153 | DNS only | Auto |
| A | @ | 185.199.110.153 | DNS only | Auto |
| A | @ | 185.199.111.153 | DNS only | Auto |

Optionally add IPv6 support with four `AAAA` records, also on `@`:

| Type | Name | IPv6 address | Proxy status |
|---|---|---|---|
| AAAA | @ | 2606:50c0:8000::153 | DNS only |
| AAAA | @ | 2606:50c0:8001::153 | DNS only |
| AAAA | @ | 2606:50c0:8002::153 | DNS only |
| AAAA | @ | 2606:50c0:8003::153 | DNS only |

Then add a `www` record so both versions resolve:

| Type | Name | Target | Proxy status |
|---|---|---|---|
| CNAME | www | yourusername.github.io | DNS only |

Note the target has no trailing path. It is `yourusername.github.io`, not `yourusername.github.io/reponame`. DNS records point at hosts, never at paths. GitHub figures out which repository to serve based on the `CNAME` file inside it.

### Option B: Subdomain (blog.example.com or docs.example.com)

Much simpler. One record:

| Type | Name | Target | Proxy status |
|---|---|---|---|
| CNAME | blog | yourusername.github.io | DNS only |

For an organisation site, the target is `orgname.github.io`.

### Option C: Apex Using CNAME Flattening

Cloudflare supports a CNAME at the zone apex, which the DNS spec technically forbids. Cloudflare resolves it and returns the underlying A records instead. This is [CNAME flattening](https://developers.cloudflare.com/dns/cname-flattening/), and it is genuinely useful because if GitHub ever rotates its IP addresses, you inherit the change automatically.

| Type | Name | Target | Proxy status |
|---|---|---|---|
| CNAME | @ | yourusername.github.io | DNS only |

Both Option A and Option C work. Pick A if you want records that mirror GitHub's documented setup exactly and are easy for a teammate to audit. Pick C if you prefer not to hardcode IP addresses.

### The Proxy Toggle, Explained Properly

That orange cloud versus grey cloud switch is the single biggest source of confusion here.

* **Grey cloud (DNS only):** Cloudflare answers the DNS query and gets out of the way. Traffic goes browser to GitHub directly. GitHub sees the real request and can complete the Let's Encrypt HTTP-01 challenge.
* **Orange cloud (Proxied):** Cloudflare sits in the middle. It terminates TLS with your visitor using a Cloudflare certificate, then makes its own connection to GitHub. GitHub never sees the ACME challenge request, so it cannot issue a certificate.

Start every record as **DNS only**. You can switch to proxied later in Step 7, once the certificate exists.

## Step 4: Verify DNS Propagation Before Touching Anything Else

Do not go back to GitHub yet. Confirm the records actually resolve.

```bash
# Check the apex A records
dig example.com +noall +answer -t A

# Check the www CNAME
dig www.example.com +nostats

# Check a subdomain setup
dig blog.example.com +nostats
```

A healthy apex response looks like this:

```
example.com.    300  IN  A  185.199.108.153
example.com.    300  IN  A  185.199.109.153
example.com.    300  IN  A  185.199.110.153
example.com.    300  IN  A  185.199.111.153
```

On Windows PowerShell:

```powershell
Resolve-DnsName example.com -Type A
Resolve-DnsName www.example.com -Type CNAME
```

If you are seeing Cloudflare IPs instead (typically in the `104.x.x.x` or `172.67.x.x` ranges), your record is still proxied. Flip it to DNS only and wait a minute.

**Tip:** use a public resolver to rule out your ISP or local cache: `dig @1.1.1.1 example.com` or `dig @8.8.8.8 example.com`.

## Step 5: Let GitHub Issue the TLS Certificate

Go back to **Settings** then **Pages** in your repository.

1. Click **Remove** next to the custom domain, then re-enter it and save. This forces GitHub to re-run its DNS check immediately instead of waiting for the next scheduled pass.
2. Watch for a green check mark reading "DNS check successful."
3. Below that you will see "Certificate not yet created." GitHub is requesting a certificate from [Let's Encrypt](https://letsencrypt.org/docs/challenge-types/) using the HTTP-01 challenge. This normally takes a few minutes and occasionally up to an hour.
4. Once the message disappears, the **Enforce HTTPS** checkbox becomes clickable. Tick it.

Enforcing HTTPS makes GitHub issue a 301 redirect from HTTP to HTTPS at the edge. Do not skip it. Search engines treat HTTP and HTTPS as separate URLs, and an unenforced setup will split your link equity across both protocols.

**If the checkbox stays greyed out for more than an hour,** the usual culprits are a still-proxied DNS record, a stale `CNAME` file, or a leftover `AAAA` record pointing at old GitHub infrastructure. Check the troubleshooting table below.

## Step 6: Protect the CNAME File From Your Build Pipeline

Here is the failure that makes people think their DNS is broken when it is not.

GitHub stores your custom domain in a file called `CNAME` at the root of the published site. If your deploy process rebuilds the output directory from scratch and force-pushes it, that file vanishes, and GitHub quietly unsets your custom domain. Your site reverts to `github.io` and the custom domain 404s until you re-add it. Then the next deploy wipes it again.

The fix depends on your generator.

**Hugo:** put the file in `static/CNAME` so it gets copied into `public/` on every build.

```bash
echo "example.com" > static/CNAME
```

**Jekyll:** create `CNAME` at the repository root. Jekyll copies unknown root files into `_site` by default.

**Next.js, Astro, Vite, or any Node build:** put it in the public assets directory.

```bash
echo "example.com" > public/CNAME
```

**GitHub Actions with peaceiris/actions-gh-pages:** the action has a parameter for exactly this.

```yaml
- name: Deploy to GitHub Pages
  uses: peaceiris/actions-gh-pages@v4
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    publish_dir: ./public
    cname: example.com
```

**Using the official Pages deployment action?** `actions/deploy-pages` reads the domain from repository settings rather than the file, so you are generally safe there, but adding the static file costs nothing and removes any ambiguity.

One rule to remember: the `CNAME` file contains exactly one line — the bare hostname, no protocol, no trailing slash, no stray blank second line.

## Step 7: Turn On the Cloudflare Proxy Safely

Now that the certificate exists, you can bring Cloudflare's CDN, caching, WAF, and analytics into play.

### First, Fix Your SSL Mode

Go to **SSL/TLS** then **Overview** in Cloudflare and check the encryption mode. Cloudflare's [documentation on SSL modes](https://developers.cloudflare.com/ssl/origin-configuration/ssl-modes/) explains the tradeoffs; here is how each one behaves with GitHub Pages.

| Cloudflare SSL mode | What happens with GitHub Pages | Verdict |
|---|---|---|
| **Off** | No encryption at all | Never |
| **Flexible** | Cloudflare talks HTTPS to the visitor, HTTP to GitHub. GitHub redirects to HTTPS. Cloudflare requests again over HTTP. Loop. | **Causes ERR_TOO_MANY_REDIRECTS** |
| **Full** | Encrypted to GitHub but the certificate is not validated | Works, but weaker |
| **Full (strict)** | Encrypted and certificate validated against GitHub's real cert | **Use this** |

Flexible is the cause of nearly every redirect loop report involving Cloudflare and GitHub Pages. Set **Full (strict)** and the loop disappears.

### Then Flip the Clouds

Go back to **DNS** then **Records** and switch your A, AAAA, or CNAME records from grey to orange.

Verify the site still loads over HTTPS, then check that the proxy is actually active:

```bash
curl -sI https://example.com | grep -i "server\|cf-ray"
```

A proxied response includes a `cf-ray` header and `server: cloudflare`. An unproxied one shows `server: GitHub.com`.

### One Important Caveat About Certificate Renewal

Let's Encrypt certificates last 90 days. GitHub renews them automatically, but renewal requires the same HTTP-01 challenge that needed DNS-only mode in the first place. With the proxy on permanently, renewal can fail and your certificate can expire.

Two ways to handle this:

1. **Leave it proxied and rely on Cloudflare's edge certificate.** Visitors connect to Cloudflare over Cloudflare's cert, so an expired GitHub cert mostly does not surface to users, but it does break Full (strict) validation. Not ideal.
2. **Create a Cloudflare Configuration Rule or Page Rule** that bypasses the cache and disables optimisation for `/.well-known/acme-challenge/*` so challenge requests pass through cleanly.

The lowest-effort approach for personal projects: keep the records on DNS only. You lose Cloudflare caching, but GitHub Pages already sits behind Fastly's CDN, so the performance delta is smaller than you would expect. Turn the proxy on when you actually need the WAF, bot rules, redirect rules, or Workers.

## Step 8: Handle www and Apex Redirects

You want one canonical hostname. Serving identical content on both `example.com` and `www.example.com` creates duplicate content and splits your SEO signals.

GitHub handles this partially on its own: if your `CNAME` file says `example.com` and a visitor hits `www.example.com`, GitHub redirects them to the apex, and vice versa. That works as long as both hostnames resolve.

For more control, use a Cloudflare **Redirect Rule** (Rules then Redirect Rules), which replaced the old Page Rules workflow:

* **When incoming requests match:** Hostname equals `www.example.com`
* **Then:** Dynamic redirect, expression `concat("https://example.com", http.request.uri.path)`
* **Status code:** 301
* **Preserve query string:** on

Redirect rules only fire on proxied records, so this requires the orange cloud.

Finally, set the canonical tag in your site's `<head>` so crawlers have no doubt:

```html
<link rel="canonical" href="https://example.com/your-page/" />
```

If you are on Hugo, update `baseURL` in `hugo.toml` to the new domain and rebuild. Forgetting this leaves absolute links, your sitemap, and your RSS feed all pointing at `github.io` — the same class of problem we cover in our [Hugo SEO configuration guide](/p/hugo-seo-guide/).

```toml
baseURL = "https://example.com/"
```

## Troubleshooting: The Five Failures You Will Actually Hit

| Symptom | Root cause | Fix |
|---|---|---|
| `ERR_TOO_MANY_REDIRECTS` | Cloudflare SSL set to Flexible | Switch to **Full (strict)** under SSL/TLS then Overview |
| "Certificate not yet created" stuck for hours | Record is proxied, blocking the ACME challenge | Set the record to **DNS only**, remove and re-add the domain in Pages settings |
| Custom domain resets itself after every deploy | Build pipeline overwrites the `CNAME` file | Add `CNAME` to `static/` or `public/`, or pass `cname:` to your deploy action |
| GitHub shows "domain does not resolve to the GitHub Pages server" | Wrong record type, wrong target, or stale cached record | Run `dig example.com +noall +answer`, confirm the four `185.199.x.153` addresses, delete conflicting records |
| Site loads but all CSS and images 404 | `baseURL` still points at `username.github.io/repo` | Update `baseURL` in your site config and rebuild |
| Old GitHub IPs still cached | Legacy records like `192.30.252.153` left in the zone | Delete every old A and AAAA record before adding the current set |

## Apex Versus Subdomain: Which Should You Pick?

| Factor | Apex (example.com) | Subdomain (blog.example.com) |
|---|---|---|
| DNS records needed | 4 A records, plus 4 AAAA for IPv6 | 1 CNAME |
| Survives GitHub IP changes | Only with CNAME flattening | Yes, automatically |
| Brand impact | Strongest | Slightly weaker |
| Setup complexity | Moderate | Trivial |
| Best for | A portfolio or company site that is the primary property | Docs, blogs, changelogs, status pages alongside a main site |

If you run several GitHub Pages projects, the cleanest pattern is one subdomain per project: `docs.example.com`, `blog.example.com`, `api.example.com`. Each is a single CNAME, each is independently removable, and none of them can break the others.

## Actionable Tips From People Who Have Done This a Few Times

* **Lower TTL before you migrate.** If you are moving a live domain, drop TTL to 60 seconds a day beforehand so rollback is fast. Cloudflare's "Auto" TTL on proxied records is 300 seconds anyway.
* **Delete conflicting records first.** A leftover `AAAA` or a wildcard `A` record on `@` will silently override your intent. Audit the whole zone, not just the record you are adding.
* **Do not create an A record and a CNAME on the same name.** DNS forbids it and Cloudflare will reject it.
* **Enable Cloudflare's "Always Use HTTPS"** under SSL/TLS then Edge Certificates, in addition to GitHub's Enforce HTTPS. Belt and braces.
* **Test with a hosts file entry** if you want to preview before flipping DNS: map your domain to `185.199.108.153` locally and load the site. You will get a certificate warning, which is expected, but you can confirm the routing works.
* **Add the new domain to Google Search Console** as a separate property and submit the sitemap. The old `github.io` property will not carry over.
* **Set a calendar reminder for 80 days out** on your first renewal cycle if you are running proxied. Check that the certificate renewed.
* **Version control your DNS** if this is a team project. Terraform's Cloudflare provider handles GitHub Pages records well and keeps the setup auditable in a pull request.

## Frequently Asked Questions

### Can I use Cloudflare's proxy with GitHub Pages?

Yes, but set up DNS as "DNS only" first so GitHub can issue its Let's Encrypt certificate, then switch to proxied. You must also set Cloudflare's SSL/TLS mode to Full (strict). Flexible mode causes an infinite redirect loop.

### What A records does GitHub Pages use for an apex domain?

GitHub Pages uses four IPv4 addresses for apex domains: 185.199.108.153, 185.199.109.153, 185.199.110.153, and 185.199.111.153. Create one A record on `@` for each. IPv6 uses 2606:50c0:8000::153 through 2606:50c0:8003::153.

### Why does my GitHub Pages custom domain keep disappearing?

Your build is overwriting the `CNAME` file that GitHub places in the published branch. Add the file to your source directory instead: `static/CNAME` for Hugo, `public/CNAME` for Next.js or Astro, or repository root for Jekyll. If you use peaceiris/actions-gh-pages, pass the `cname` parameter.

### How long does it take for a GitHub Pages custom domain to work?

DNS propagation typically takes a few minutes with Cloudflare and up to 24 hours in the worst case. After DNS resolves correctly, GitHub issues the TLS certificate within minutes to about an hour. If Enforce HTTPS is still greyed out after an hour, your DNS is probably misconfigured.

### Why am I getting ERR_TOO_MANY_REDIRECTS on my GitHub Pages site?

Cloudflare's SSL/TLS mode is set to Flexible. Cloudflare connects to GitHub over HTTP, GitHub redirects to HTTPS, and the loop repeats. Change the mode to Full (strict) under SSL/TLS then Overview.

### Can I use a custom domain with a GitHub Pages project site?

Yes. A project repository such as `github.com/you/dev9b` can serve at a root domain or a subdomain, not just at `username.github.io/dev9b`. Add the domain under Settings then Pages, and point your DNS `CNAME` at `username.github.io` without any path.

### Do I need to pay Cloudflare for this?

No. Cloudflare's free plan includes DNS hosting, CNAME flattening, universal SSL, redirect rules, and the CDN proxy. GitHub Pages is free for public repositories. The only cost is the domain registration itself.

### Can I use Cloudflare Pages instead of GitHub Pages?

Yes, and if you are already inside Cloudflare it is worth considering. Cloudflare Pages builds from the same GitHub repo, gives you preview deployments per pull request, and removes the certificate coordination problem entirely because one vendor handles both DNS and hosting. The tradeoff is build minute limits on the free tier and a different set of routing conventions.

### Will switching to a custom domain hurt my SEO?

Short term, expect a dip while search engines recrawl. GitHub automatically 301 redirects the old `github.io` URLs to your custom domain, which passes most link equity. Speed recovery up by submitting the new domain in Search Console, updating your sitemap `baseURL`, and adding canonical tags.

### Can I point multiple domains at one GitHub Pages site?

GitHub Pages accepts only one custom domain per repository. To serve additional domains, register them in Cloudflare and use a Redirect Rule to 301 them to your canonical hostname.

## Wrapping Up

The whole process comes down to five things done in the right order: claim the domain in GitHub Pages before touching DNS, create the correct record type for apex versus subdomain, keep the proxy off until the certificate exists, set SSL to Full (strict) before turning the proxy on, and stop your build from eating the `CNAME` file.

Get those right and you have a free, globally distributed, HTTPS-enabled static site on a domain you own, deployed by a `git push`.

Every article on this site goes through the F9XR review board against the standards in our [editorial policy](/editorial-policy/). Spot something off or think a DNS edge case is missing? Open the post from the toolbar above and file a change — suggest a fix on [GitHub](https://github.com/) by hitting the **Suggest changes** button on this page, or read about [contributing](/contribute/). This draft was drafted with AI assistance and verified against the Cloudflare and GitHub documentation linked throughout.