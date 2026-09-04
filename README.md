<img align="right" width="150" alt="logo" src="assets/img/f9x-logo.webp">

# F9XR's Dev9b

**Dev9b** is an open-source blog article publishing platform by the **F9XR Team**. We share the latest articles, tutorials, coding videos, and developer guides for the open developer community.

Dev9b is a free, open-source online community where software developers share knowledge, write technical articles, and help each other grow. Made by developers, for developers.

**Live site:** https://f9xr.github.io/dev9b/

## Features

- 📄 Latest developer articles & tutorials
- 🎥 Coding videos and guides
- 🚀 Free, open-source, community-driven
- ⚙️ Built with Hugo + Hugo Theme Stack
- 🌐 Auto-deployed to GitHub Pages
- 🔍 SEO-optimized (meta tags, OG tags, JSON-LD structured data, sitemap, robots.txt)

## Local Development

You need **Git**, **Go**, and **Hugo Extended** installed.

```bash
# Install the theme module
hugo mod get

# Run the development server
hugo server -D
```

Visit http://localhost:1313/

## Contribute an Article

Dev9b welcomes contributions! All articles are reviewed by the **F9XR Review Board** before publishing.

1. Fork [the repository](https://github.com/f9xr/dev9b)
2. Create your article under `content/post/your-slug/index.md`
3. Add a cover image and proper front matter
4. Submit a Pull Request

For the full guide, see the live [Contributor Guide](https://f9xr.github.io/dev9b/contribute/).

## Site Structure

```
content/
├── _index.md            # Homepage
├── page/
│   ├── about/           # About Dev9b
│   ├── archives/        # Archive listing
│   ├── contribute/      # Contributor guide
│   ├── links/           # Links page
│   └── search/          # Search page
└── post/                # Articles
```

## SEO & Standards Files

Located in `static/`:
- `llms.txt` / `llms-full.txt` — LLM-readable site summaries
- `humans.txt` — Team & tools credits
- `robots.txt` — Crawler rules
- `articles-urls.txt` — Article URL index

## Theme

- [hugo-theme-stack v4](https://github.com/CaiJimmy/hugo-theme-stack) loaded via Hugo modules
- Theme auto-updates daily via GitHub Actions cron

## License

- Source code: [MIT](LICENSE)
- Content: CC BY-NC-SA 4.0

## Team

F9XR Team — [github.com/f9xr](https://github.com/f9xr)
