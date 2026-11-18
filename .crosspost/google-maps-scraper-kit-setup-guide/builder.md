If you have ever tried to pull a clean list of local businesses out of Google Maps, you know how it goes. The official Places API wants a billing account and charges per request. Paid scraping platforms charge per result. The free scripts on GitHub usually hand you a name and an address, then leave you to work out the email part yourself.

**Google Maps Scraper Kit** is an open-source project that tries to close that whole gap in one place. Give it a business type and a city, and you get a CSV with phone numbers, websites, ratings, emails and social profile links. It runs on your own machine, needs no API key, and does not require Docker. We checked the repository at version 2.1.0, the release its maintainer last verified on 2026-11-01; at the time of writing it has about 2.5k stars and 500 forks.

This guide covers what the kit is, how it works under the hood, how to install it, which flags actually matter, and where its limits are. There is also a plain section on the legal side, because scraping Google Maps is not a gray area you should ignore.

## What Google Maps Scraper Kit Actually Does

Google Maps Scraper Kit is a free, MIT-licensed Google Maps scraper for lead generation, written in Python and built around a headless Chrome browser. It collects public business listings from Google Maps, then visits each business website to find contact details. The end product is an outreach-ready CSV.

The short version, for anyone skimming:

- **What it is:** a local Google Maps scraper plus an email and social profile finder
- **Language:** Python 3.9 or newer, standard library by default
- **Cost:** free, MIT license
- **API key required:** no
- **Docker required:** no, though Docker is supported as an option
- **Output:** CSV with name, phone, email, website, category, address, rating, review count and six social columns
- **Extras:** MX email check, ad pixel detection, lead scoring, proxy rotation
- **AI agent support:** a skill for Claude Code, Codex and Cursor, plus four slash commands for Claude Code

The project is built by a developer who goes by Mahan on GitHub, and the repo's own notes describe it as a rewrite from scratch. Version 1.x wrapped another open-source scraper inside Docker. Version 2.0 replaced that with the kit's own engine, which talks to Chrome over the DevTools protocol and exposes a small HTTP API and web UI on `127.0.0.1:8080`.

![Google Maps Scraper Kit banner showing a map pin, a lead list card and the project name](https://raw.githubusercontent.com/f9xr/dev9b/master/content/post/google-maps-scraper-kit-setup-guide/kit-preview.png)

If you are weighing whether a script like this is worth the setup time, the honest test is the email hit rate. A list of 100 businesses with 40 usable emails is far more valuable than 400 rows with zero contact details, and that gap is exactly what the enrichment step is meant to close.

## How the Kit Works Under the Hood

Understanding the architecture saves you an hour of confused debugging later, so it is worth a minute.

The kit has two layers:

1. **The engine** (`engine/serve.py`). It launches headless Chrome, loads Google Maps search results, scrolls the results panel, and parses each listing. It serves a local API and a simple web form on port 8080.
2. **The CLI scripts** (`scripts/scrape.py` and `scripts/engine.py`). These are dependency-free Python scripts. `engine.py` starts and stops the engine. `scrape.py` creates a job, waits for it, crawls the business websites for emails and socials, and writes the CSV.

![Diagram](https://mermaid.ink/img/Zmxvd2NoYXJ0IExSCiAgICBBW3NjcmFwZS5weV0gLS0-fGNyZWF0ZSBqb2J8IEJbRW5naW5lIG9uIDEyNy4wLjAuMTo4MDgwXQogICAgQiAtLT58RGV2VG9vbHMgcHJvdG9jb2x8IENbSGVhZGxlc3MgQ2hyb21lXQogICAgQyAtLT58c2VhcmNoICsgc2Nyb2xsfCBEW0dvb2dsZSBNYXBzIHJlc3VsdHNdCiAgICBEIC0tPiBCCiAgICBCIC0tPnxyb3dzfCBBCiAgICBBIC0tPnxIVFRQLCAxNiBhdCBhIHRpbWV8IEVbQnVzaW5lc3Mgd2Vic2l0ZXNdCiAgICBFIC0tPiBBCiAgICBBIC0tPiBGW3Jlc3VsdHMtam9iLWlkLmNzdl0?bgColor=FFFFFF)
The enrichment step is plain HTTP plus regular expressions. After the Maps job finishes, the script fetches each business homepage 16 at a time, looks for an email, and falls back to the contact and about pages when the homepage shows none. The same fetched page is reused to find Instagram, Facebook, LinkedIn, TikTok, YouTube and X links. Because this is code and not a language model, it costs zero AI tokens even when an agent is driving the run.

## What You Get in the CSV

By default you get eight lead fields: `title`, `phone`, `emails`, `website`, `category`, `address`, `review_rating` and `review_count`. After those come six social columns: `instagram`, `facebook`, `linkedin`, `tiktok`, `youtube` and `x`.

The engine itself writes 36 raw columns plus `categories`. Passing `--full` keeps all of them, including coordinates, place IDs, opening hours, star histograms and photo URLs.

| Feature | What it does | Flag or note |
| --- | --- | --- |
| Lead fields | Name, phone, email, website, category, address, rating, review count | 8 fields by default |
| Social enrichment | Finds Instagram, Facebook, LinkedIn, TikTok, YouTube, X | On by default, `--no-socials` skips it |
| Email extraction | Crawls homepage, then contact and about pages | On by default, `--no-email` skips it |
| Beat the 120 cap | Splits a city into map tiles and dedupes on `place_id` | `--grid N`, `--deep-scan` |
| Email check | MX lookup for each email domain over DNS | `--verify-emails` |
| Ad pixel detection | Spots Meta Pixel, Google Ads tag, analytics, Bing Ads, LinkedIn Insight, TikTok pixel, CMS | `--tech` |
| Lead scoring | Ranks leads by an `intent_score` from 0 to 100 | Added by `--tech` |
| Filters | Rating, reviews, phone, email, no-website, limit | `--min-rating`, `--min-reviews`, `--has-phone`, `--has-email`, `--no-website`, `--limit` |
| Incremental runs | Skips places you already have | `--exclude earlier.csv` |
| Geocoding | Turns a city name into coordinates via OpenStreetMap | `--city` |
| Localisation | Language and country for the search | `--lang`, `--country` |
| Reviews | Up to 5 review texts per place, one page load each | `--reviews N` |
| Proxy support | HTTP, HTTPS, SOCKS5 and SOCKS5H, repeatable | `--proxy URL` |
| Batch jobs | Many keywords, one job, one CSV | `--keywords-file` |

One small defence worth knowing: a cell that a spreadsheet would run as a formula gets a leading apostrophe. It is a quiet guard against CSV injection when you open the file in Excel or Sheets.

## Install and Run It in Four Commands

### Requirements

You need three things:

- Python 3.9 or newer
- Google Chrome, Chromium, Edge or Brave
- A terminal (Terminal on macOS, PowerShell on Windows)

If no browser is installed, the first start downloads Chrome for Testing once, about 100 MB, and checks it against a pinned SHA-256 hash. The basic crawl needs no `pip install`. Only the optional JavaScript website rendering needs Playwright. The kit runs natively on macOS, Windows, and Linux on amd64 and arm64, so Apple Silicon Macs are fine.

### The four-line quick start
```bash
git clone https://github.com/Mahanaicoach/google-maps-scraper-kit.git
cd google-maps-scraper-kit
python3 scripts/engine.py start
python3 scripts/scrape.py "coffee shops in Austin TX" 30.2672 -97.7431 --depth 2
```

On Windows, type `py` in place of `python3`. To stop the engine later, run `python3 scripts/engine.py stop`.

That last command scrapes coffee shops around the coordinates you pass, loads two batches of results (about 40 places), crawls their websites, and writes a file named `results-<short job id>.csv`. Use `--out` if you want to name the file yourself.

### If port 8080 is already taken

Copy the example config, then change the port:
```bash
cp .env.example .env
```

Set `SCRAPER_PORT=8081` (or any free port) inside `.env`, then start the engine again.

### Prefer Docker?

Replace the third line with `docker compose up -d`. If the native engine is running, stop it first, because the two keep separate job lists. The first run builds the image, which takes about a minute. Everything else stays the same.

### Optional: use the web UI

Open `http://localhost:8080` and you get a form. The "What" box offers about 4,100 business types and the "Where" box about 168,000 cities from GeoNames, so you cannot accidentally search for a place or category that does not exist. Each finished job offers a Leads CSV, a Full CSV and JSON. One caveat from the docs: the web UI reads homepages only for emails and socials, so the scripts, which also crawl contact pages, find more emails.

## The Flags That Matter in Practice

### Scrape a city without knowing its coordinates
```bash
python3 scripts/scrape.py "dentists in Denver CO" --city "Denver, CO" --depth 5
```

Each `--depth` step loads roughly 20 more places. Depth 2 returns about 40, and depth 5 returns up to about 100, which is close to Google's ceiling of about 120 per search.

### Go past Google's 120 result cap

Google Maps stops scrolling after roughly 120 listings for a single search. That limit is on Google's side, not the kit's. The workaround is cutting the city into tiles:
```bash
python3 scripts/scrape.py "dentists in Denver CO" --city "Denver, CO" --grid 3
```

`--grid 3` splits the area into a 3 by 3 set of map tiles, runs each tile, and removes duplicates by `place_id`. For denser coverage, `--deep-scan` takes any tile that hit the cap and splits it into four sub-tiles one zoom level in. Tiles run one at a time, so a deep scan is slower and more likely to trip rate limits. Use it only when you genuinely need every listing.

### Add ad pixel detection and email checks
```bash
python3 scripts/scrape.py "roofing contractors in Phoenix AZ" --city "Phoenix, AZ" --depth 3 --tech --verify-emails --min-rating 4.0 --has-phone
```

`--tech` adds columns such as `fb_pixel`, `google_ads_tag`, `analytics`, `bing_ads`, `linkedin_insight`, `tiktok_pixel`, `cms`, `mobile_friendly` and `intent_score`, and sorts the hottest leads first. The logic is simple: a business that already pays for ads is more likely to pay for marketing help. `--verify-emails` adds an `email_host` column with values like `google_workspace`, `microsoft_365`, `other` or `none`, and drops dead domains.

Be precise about what that check proves. It looks up the domain's MX record over DNS, so it tells you the domain can receive mail and which provider runs it. It does not confirm that a specific mailbox exists. You still need a real sending process and a bounce policy.

### Find businesses that need a website
```bash
python3 scripts/scrape.py "plumbers in Portland OR" --city "Portland, OR" --depth 5 --no-website
```

### Run a batch of keywords

Put one keyword per line in a text file, then run:
```bash
python3 scripts/scrape.py --keywords-file examples/queries.example.txt --city "Denver, CO"
```

You get one job and one CSV, and a place found by several keywords is listed once.

### Run weekly and keep only new leads
```bash
python3 scripts/scrape.py "dentists in Denver CO" --city "Denver, CO" --depth 5 --exclude last-week.csv
```

That single flag turns a one-off scrape into a feed of new businesses, which is usually what an outreach workflow actually needs.

### Full flag reference

| Flag | Purpose |
| --- | --- |
| `--city "City, ST"` | Auto-geocode a city (repeat it for several cities) |
| `--depth N` | Load N batches of about 20 places |
| `--grid N` | Split the area into N by N tiles |
| `--deep-scan` | Sub-split tiles that hit Google's cap |
| `--no-email` | Skip the email crawl |
| `--no-socials` | Drop social columns |
| `--tech` | Detect ad pixels, CMS, mobile support, score leads |
| `--verify-emails` | MX lookup and mail host label |
| `--lang`, `--country` | Search language and country |
| `--reviews N` | Pull up to 5 review texts per place |
| `--min-rating`, `--min-reviews` | Quality filters |
| `--has-phone`, `--has-email` | Contactability filters |
| `--no-website` | Only businesses without a site |
| `--exclude file.csv` | Skip places you already have |
| `--limit N` | Cap the number of rows |
| `--browser-sites` | Optional Playwright retry for JavaScript-heavy sites |
| `--proxy URL` | Route traffic through a proxy (repeatable) |
| `--full` | Keep every raw column |

## Running It With Claude Code, Codex and Cursor

This is where the project gets interesting for developers. The repo ships an [Agent Skills](https://agentskills.io) compatible skill, so an AI coding agent can run the scrape for you in plain English.

**Option A: open the folder in Claude Code.**
```bash
cd google-maps-scraper-kit
claude
```

The skill and four slash commands load automatically.

**Option B: install the skill into an agent you already use.**
```bash
npx skills add mahanaicoach/google-maps-scraper-kit
```

This installs only the skill file. The engine and scripts still come from the clone, so the agent will ask you to run the quick start first.

Then you can simply say: "Scrape gyms in Miami and give me phones, emails and websites." The agent checks that the engine is running, starts it if not, runs `scripts/scrape.py` in the background, and returns a clean table plus the CSV file.

| Slash command (Claude Code only) | What it does |
| --- | --- |
| `/scrape <business> in <city, ST> [depth]` | Run one scrape and return a table and CSV |
| `/scrape-batch <keywords-file> [--city "City, ST"]` | Run many queries as one job |
| `/scrape-setup` | Start the engine and run a health check |
| `/scrape-jobs [list or delete <id>]` | List or delete jobs |

If you already follow agent tooling, our guides on [AI coding agents explained](https://f9xr.org/dev9b/p/ai-coding-agents-explained/) and [OpenCode skills](https://f9xr.org/dev9b/p/opencode-skills-guide/) cover the same skill-based pattern from other angles. For a head-to-head view of editors, see [OpenCode vs Cursor](https://f9xr.org/dev9b/p/opencode-vs-cursor/).

The design detail worth copying: the agent is only the operator. Parsing and scraping happen in deterministic Python, so results are repeatable and you are not paying tokens for every row.

## Speed, Measured

The README publishes timings from a fresh v2.1.0 install on a MacBook with home internet, no proxies and no Docker, dated 2026-11-01. These are single runs by the author, so treat them as a reasonable guide rather than a guarantee.

| Command (simplified) | Result | Time |
| --- | --- | --- |
| Coffee shops in Austin, depth 2 | 40 places, 11 emails, 16 with a social profile | 21 s |
| Dentists in Denver, depth 5 | 100 places, 42 emails, 63 with a social profile | 44 s |
| Manhattan restaurants, depth 20, no email crawl | 119 places (Google's cap) | 34 s |
| Manhattan restaurants, `--grid 3`, depth 6, no email crawl | 471 unique places across 9 tiles | 5 min 21 s |
| Phoenix roofers, `--tech --verify-emails` filters | 59 places, 38 emails | 29 s |
| Cafes in Lisbon, `--reviews 3 --full` | 40 places with reviews, hours and photo URLs | 37 s |

The whole documented session was 2,068 places across 27 jobs in 21 minutes from one home IP, with no unusual-traffic page. Note the email hit rate: 42 of 100 in the Denver run. That is normal for this kind of scraping, and it is the number to plan around.

## Where It Stops Working

I like that the project documents its own weak spots instead of hiding them. These are the ones that matter most:

- **About 120 listings per search.** This is Google's cap. `--grid` and `--deep-scan` are the workaround, but tiles run one at a time, so grids are slower and more likely to trigger rate limits.
- **Emails only appear when a business publishes one.** Expect emails on a fraction of rows, not all of them.
- **Wrong websites on listings.** Some listings point at the wrong business site. The script skips a homepage that shows neither the listing's phone number nor a word of its category, and reports how many it skipped.
- **Rate limits are real.** Heavy use from one IP can get you temporarily blocked for minutes to hours. The engine waits and retries twice, then stops the job and keeps the rows it already found. Your Google account is not affected.
- **Review counts need a user agent tweak.** Google serves a limited view to browsers that announce `HeadlessChrome`. The engine replaces that word with `Chrome` so review counts and weekly hours come back. Google can still leave fields out.
- **Service-area businesses often have no address.** Plumbers and cleaners frequently hide theirs, so that cell stays empty.
- **No SOCKS5 login.** Chrome cannot authenticate to a SOCKS5 proxy, so use an `http://user:pass@host:port` address instead.

## How It Compares With Other Google Maps Scrapers

The repo includes a 14-point comparison against gosom, omkarcloud, zohaibbashir, gaspa93, conor, Apify and Outscraper. Those figures come from the project's own research dated 2026-11-02, so read them as the maintainer's view and verify anything that decides a purchase. The condensed version:

| Tool type | Typical trade-off |
| --- | --- |
| This kit | Free, local, emails and socials on by default, Python and Chrome only |
| gosom/google-maps-scraper | Free and fast, but needs Docker or a binary, and emails are off by default |
| omkarcloud | Free tier, with enrichment features behind a paid plan |
| Apify and Outscraper | Hosted and scalable, but you pay per result and data leaves your machine |
| Google Places API | Official and stable, but billed per request and limited in fields |

If you want a broader look at scraping approaches, our write-ups on [Scrapling web scraping setup](https://f9xr.org/dev9b/p/scrapling-web-scraping-setup-guide/) and the [Apify MCP workflow guide](https://f9xr.org/dev9b/p/apify-mcp-guide-ai-automation-workflow/) are good companions. The [full comparison document](https://github.com/Mahanaicoach/google-maps-scraper-kit/blob/master/docs/best-google-maps-scrapers.md) lists the sources and dates behind each row.

## Scraping Google Maps and the Law

This part deserves plain talk. The project's own FAQ says scraping Google Maps is against [Google's Terms of Service](https://policies.google.com/terms), and that phone numbers and emails count as personal data. That is not legal advice, and neither is this article.

Here is a sensible baseline:

- **Check the law where the data is used.** GDPR in Europe, CCPA in California, LGPD in Brazil, and [CAN-SPAM](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business) for commercial email in the United States.
- **Have a lawful basis and an opt-out** before you send any outreach.
- **Treat the output as leads to verify**, not a dataset to resell.
- **Go slowly.** Run one job at a time and start at depth 5.
- **Use proxies for large or repeated runs.** The kit rotates several, and retries a refused keyword through the next one.
- **Watch for block signals**: failed jobs, empty results, or far fewer rows than an identical earlier run.

> **WARNING** â€” Terms of service
>
> A successful scrape is not permission to use the data. Check the terms of the source, the privacy law that applies to your recipients, and your own sending rules before the first email goes out.
>

The kit also has safe defaults worth mentioning: the API binds to `127.0.0.1`, it rejects cross-site requests from your browser, it sends no telemetry, and it checks GitHub once a day for a new release (you can disable that with `SCRAPER_NO_UPDATE_CHECK=1` in `.env`). Nothing updates itself.

## Field Notes From Running Lead Scrapers

If you have built lead lists before, a few patterns from that work apply directly here, regardless of which tool you pick.

Start with one small job. A depth-2 run on a city you know well tells you whether your setup works, whether the email crawl reaches the sites it should, and roughly what hit rate to expect. Launching a 3 by 3 grid first only makes a failure slower and noisier.

Filter before you enrich. Crawling a thousand websites to discover you only wanted businesses rated above 4.0 with a phone number wastes an afternoon. The cheap filters run on the Maps rows, so apply them before the crawl.

Keep email hygiene separate from scraping. An MX check tells you a domain accepts mail; it says nothing about bounces, spam traps or consent. If you are building the sending side yourself, our guide on [programmatic transactional SMTP with Node.js](https://f9xr.org/dev9b/p/programmatic-transactional-smtp-nodejs-setup/) covers the transactional side, and the rules for cold outreach are stricter.

Finally, version your outputs. `--exclude last-week.csv` is only useful if last week's file is still where the script expects it. Keep lead lists out of git, and the repo's default `.gitignore` already helps.

## Updating the Kit

The web UI shows a line under its title when a newer release is out, and `python3 scripts/engine.py status` prints one too. Neither updates anything by itself. To pull the latest fixes:
```bash
bash scripts/update.sh
python3 scripts/engine.py restart
```

With Docker, the update script rebuilds and restarts the container for you. On Windows without Git Bash, the maintainer's manual equivalent is a `git pull` followed by `py scripts/engine.py restart`.

## Key Takeaways

- Google Maps Scraper Kit is a free, MIT-licensed, local Python scraper that turns a business type and city into a lead CSV.
- It needs Python 3.9 or newer and a Chrome-based browser. No API key and no Docker are required.
- Emails and six social profile links are collected by default, with zero AI tokens, using HTTP and regex.
- `--grid` and `--deep-scan` get past Google's roughly 120 results per search by tiling the map.
- `--tech` detects ad pixels and ranks leads, while `--verify-emails` runs an MX check on each domain.
- The maintainer measured 100 places with emails in 44 seconds on one test run. Your results will vary with city, hour and IP.
- It includes a skill for Claude Code, Codex and Cursor, plus four Claude Code slash commands.
- Scraping Google Maps breaks Google's Terms of Service, and contact data is personal data. Follow the laws that apply to you.

## Conclusion

The kit earns its stars by solving the boring part of lead generation properly: one command, local execution, emails and socials attached, and an escape hatch when Google's 120-result cap gets in the way. It is not a magic list generator, and the honest limits section in its own README should be required reading before you plan a campaign around the output.

If you spot something outdated in this guide, the [contributor guide](https://f9xr.org/dev9b/contribute/) explains how to suggest a fix, and the [editorial policy](https://f9xr.org/dev9b/editorial-policy/) covers how we verify and correct articles. The [GitHub repository](https://github.com/Mahanaicoach/google-maps-scraper-kit) and its [full setup guide](https://github.com/Mahanaicoach/google-maps-scraper-kit/blob/master/SETUP.md) remain the authoritative source for commands and version-specific details.

## Frequently Asked Questions

### What is Google Maps Scraper Kit?

Google Maps Scraper Kit is a free, open-source Python tool that scrapes Google Maps business listings and enriches them with emails and social profile links. It exports the results to a CSV file and runs entirely on your own computer.

### Is Google Maps Scraper Kit free?

Yes. The kit and its engine are MIT licensed, with no credits, subscriptions or API keys. You only need Python and a Chrome-based browser, or Docker if you prefer it.

### Do I need a Google Maps API key or Docker?

No. The kit drives a headless Chrome browser against Google Maps directly, so there is no API quota or billing. Docker is optional and only offered as an alternative way to run the engine.

### How do I get more than 120 results from Google Maps?

Use the `--grid` flag, for example `--grid 3`. It splits the city into map tiles, scrapes each one, and removes duplicates using `place_id`. For even denser coverage, add `--deep-scan`, which splits any full tile into four sub-tiles.

### Does the email check confirm an address is real?

No. The `--verify-emails` flag looks up the MX record for the email domain and labels the mail host, such as Google Workspace or Microsoft 365. It filters out dead domains but cannot confirm that a specific mailbox exists.

### Is scraping Google Maps legal?

It violates Google's Terms of Service, and business phone numbers and emails are personal data under laws such as GDPR, CCPA and LGPD. Follow the rules where you use the data, get a lawful basis and offer an opt-out before outreach. This is not legal advice.
