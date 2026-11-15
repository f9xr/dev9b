#!/usr/bin/env python3
"""Submit Dev9b article URLs to IndexNow.

Run this AFTER the post is pushed and deployed, and AFTER the dev.to copy is
published. The deploy workflow also pings all article URLs; this is the
post-syndication ping for the exact URL(s) that just shipped.

Usage (from the repository root):

    python scripts/ping-indexnow.py <slug>
    python scripts/ping-indexnow.py <slug> --dry-run
    python scripts/ping-indexnow.py --all

Site URL is read from .crosspost.json (site_url), falling back to
https://f9xr.org/dev9b. The key file lives in static/ and is served from the
same site root, so keyLocation always resolves on the same host.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
ENDPOINT = "https://api.indexnow.org/indexnow"
KEY = "3FFE8AD1224F6498C1B5162A3A4A4907"
DEFAULT_SITE_URL = "https://f9xr.org/dev9b"
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def site_url() -> str:
    config = ROOT / ".crosspost.json"
    if config.exists():
        try:
            value = str(json.loads(config.read_text(encoding="utf-8")).get("site_url", "")).strip()
            if value:
                return value.rstrip("/")
        except (OSError, ValueError) as exc:
            print(f"! ignoring .crosspost.json: {exc}", file=sys.stderr)
    return DEFAULT_SITE_URL


def article_urls(site: str, slug: str | None) -> list[str]:
    if slug:
        if not SLUG_RE.match(slug):
            sys.exit(f"invalid slug: {slug!r} (lowercase letters, digits and hyphens only)")
        return [f"{site}/p/{slug}/"]

    posts = sorted((ROOT / "public" / "p").glob("*/index.html"))
    if not posts:
        sys.exit("no built posts in public/p; run hugo --gc --minify first")
    return [f"{site}/p/{post.parent.name}/" for post in posts]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Submit Dev9b article URLs to IndexNow.")
    parser.add_argument("slug", nargs="?", help="post slug, e.g. most-least-used-colors-by-ai")
    parser.add_argument("--all", action="store_true", help="submit every built post in public/p")
    parser.add_argument("--dry-run", action="store_true", help="print the payload without sending it")
    args = parser.parse_args(argv)

    if bool(args.slug) == bool(args.all):
        parser.error("pass exactly one of: <slug> or --all")

    site = site_url()
    host = urlparse(site).netloc
    if not host:
        sys.exit(f"invalid site_url in .crosspost.json: {site!r}")

    urls = article_urls(site, None if args.all else args.slug)
    payload = {
        "host": host,
        "key": KEY,
        "keyLocation": f"{site}/{KEY}.txt",
        "urlList": urls,
    }

    if args.dry_run:
        print(json.dumps(payload, indent=2))
        return 0

    request = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            status = response.status
            body = response.read().decode("utf-8", "replace").strip()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace").strip()
        print(f"IndexNow failed: HTTP {exc.code} {detail}", file=sys.stderr)
        return 1
    except Exception as exc:  # noqa: BLE001 - network failure should be visible, not silent
        print(f"IndexNow failed: {exc}", file=sys.stderr)
        return 1

    print(f"IndexNow: HTTP {status} ({len(urls)} URL(s))")
    for url in urls[:10]:
        print(f"  - {url}")
    if len(urls) > 10:
        print(f"  ... and {len(urls) - 10} more")
    if body:
        print(body)
    return 0 if status in (200, 202) else 1


if __name__ == "__main__":
    raise SystemExit(main())
