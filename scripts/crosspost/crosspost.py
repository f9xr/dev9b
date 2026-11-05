#!/usr/bin/env python3
"""Syndicate a Dev9b Hugo article to dev.to, Medium and AWS Builder Center.

One source file: content/post/<slug>/index.md (Hugo page bundle, YAML front matter).
Everything below is derived from it, because the destinations disagree:

  dev.to          full REST API, renders tables/code/emoji natively.
  Medium          no API; needs HTML with tables rendered as images. Paste it.
  AWS Builder     no API; needs markdown/HTML without front matter or emoji.

Usage (from the repository root):

    python scripts/crosspost/crosspost.py build <slug>
    python scripts/crosspost/crosspost.py publish <slug>
    python scripts/crosspost/crosspost.py all <slug>
    python scripts/crosspost/crosspost.py latest

`build` writes artifacts only. `publish` creates/updates the dev.to copy (live by
default, drafts with --draft).

Artifacts live in .crosspost/<slug>/ (committed, outside Hugo content).
Table images live in static/crosspost/<slug>/ because Medium fetches them by URL.
Commit and push both before publishing: dev.to and Medium fetch images at render
time, so an unpushed file is a broken image on a live post.

Requires: PyYAML, Pillow, Hugo (for the Medium/Builder HTML), and a dev.to key in
$DEV_TO_API_KEY or ~/.devto.key.
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import os
import posixpath
import re
import shutil
import subprocess
import sys
import unicodedata
import urllib.error
import urllib.request
from datetime import date, datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("Missing PyYAML. Install it with: python -m pip install PyYAML Pillow")

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:  # pragma: no cover
    Image = None


# ---------------------------------------------------------------------------
# Paths and configuration
# ---------------------------------------------------------------------------


def repo_root() -> Path:
    here = Path(__file__).resolve()
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=here.parent,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        if out:
            return Path(out)
    except (OSError, subprocess.CalledProcessError):
        pass
    return here.parents[2]


ROOT = repo_root()


def load_config() -> dict:
    defaults = {
        "site_url": "https://f9xr.org",
        "raw_base": "https://raw.githubusercontent.com/f9xr/dev9b/main",
        "devto_org": "aws-builders",
        "devto_publish": True,
        "author": "F9XR Team",
    }
    path = ROOT / ".crosspost.json"
    if path.exists():
        try:
            defaults.update(json.loads(path.read_text(encoding="utf-8")))
        except json.JSONDecodeError as exc:
            sys.exit(f"Bad JSON in {path}: {exc}")
    return defaults


def post_dir(slug: str) -> Path:
    return ROOT / "content" / "post" / slug


def artifacts_dir(slug: str) -> Path:
    # Deliberately outside content/: Hugo refuses text/html content files in a
    # page bundle, and these artifacts are not pages.
    return ROOT / ".crosspost" / slug


def public_img_dir(slug: str) -> Path:
    return ROOT / "static" / "crosspost" / slug


def rel_posix(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


# ---------------------------------------------------------------------------
# Front matter and markdown helpers
# ---------------------------------------------------------------------------


def parse_post(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8-sig")
    m = re.match(r"^---\s*\r?\n(.*?)\r?\n---\s*\r?\n?", text, flags=re.S)
    if not m:
        sys.exit(f"No YAML front matter found in {path}")
    meta = yaml.safe_load(m.group(1)) or {}
    if not isinstance(meta, dict):
        sys.exit(f"Front matter in {path} is not a mapping")
    return meta, text[m.end():]


def slug_of(meta: dict, path: Path) -> str:
    return str(meta.get("slug") or path.parent.name)


def iso(value) -> str:
    if isinstance(value, (date, datetime)):
        return value.isoformat()[:10]
    return str(value or "")


def raw_url(config: dict, repo_path: str) -> str:
    return f"{config['raw_base'].rstrip('/')}/{repo_path.lstrip('/')}"


def site_url(config: dict, url_path: str) -> str:
    return f"{config['site_url'].rstrip('/')}/{url_path.lstrip('/')}"


def cover_repo_path(meta: dict, slug: str) -> str:
    image = str(meta.get("image") or "cover.jpg").strip().lstrip("/")
    return f"content/post/{slug}/{image}"


def strip_more(body: str) -> str:
    return re.sub(r"(?mi)^\s*<!--\s*more\s*-->\s*$", "", body)


def apply_outside_fences(text: str, transform) -> str:
    """Apply a markdown transform to everything except fenced code blocks.

    Code examples in these articles contain markdown links, shortcodes and
    alert-looking lines. Rewriting them changes the example the reader copies.
    """
    out: list[str] = []
    chunk: list[str] = []
    in_fence = False
    for line in text.splitlines(keepends=True):
        if re.match(r"^\s*(```|~~~)", line):
            if in_fence:
                out.append(line)
                in_fence = False
            else:
                out.append(transform("".join(chunk)))
                chunk = []
                out.append(line)
                in_fence = True
            continue
        if in_fence:
            out.append(line)
        else:
            chunk.append(line)
    out.append(transform("".join(chunk)))
    return "".join(out)


def emoji_re() -> re.Pattern:
    return re.compile(
        "["
        "\U0001F000-\U0001FAFF"
        "\U00002600-\U000027BF"
        "\U0001F1E6-\U0001F1FF"
        "\uFE0F\u200D\u20E3"
        "]",
        flags=re.UNICODE,
    )


def strip_emoji(text: str) -> str:
    return emoji_re().sub("", text)


def mermaid_url(code: str) -> str:
    payload = base64.urlsafe_b64encode(code.encode("utf-8")).decode("ascii").rstrip("=")
    return f"https://mermaid.ink/img/{payload}?bgColor=FFFFFF"


def convert_mermaid(body: str) -> tuple[str, int]:
    count = 0

    def repl(match: re.Match) -> str:
        nonlocal count
        count += 1
        return f"![Diagram]({mermaid_url(match.group(1).strip())})"

    body = re.sub(r"(?ms)^```mermaid\s*\r?\n(.*?)^```\s*$", repl, body)
    return body, count


def convert_shortcodes(body: str) -> str:
    def transform(text: str) -> str:
        # Escaped shortcode examples ({{</* ... */>}}) render as literal text.
        text = text.replace("{{</*", "{{<").replace("*/>}}", ">}}")

        def youtube(match: re.Match) -> str:
            vid = match.group(1) or match.group(2)
            return (
                "\n\n[Watch the video on YouTube]"
                f"(https://www.youtube.com/watch?v={vid})\n\n"
            )

        text = re.sub(
            r"\{\{<\s*youtube\s+(?:id\s*=\s*[\"']?([\w-]+)[\"']?|([\w-]+))\s*>\}\}",
            youtube,
            text,
        )

        def bilibili(match: re.Match) -> str:
            return (
                "\n\n[Watch the video on Bilibili]"
                f"(https://www.bilibili.com/video/{match.group(1)})\n\n"
            )

        text = re.sub(
            r"\{\{<\s*bilibili\s+([A-Za-z0-9]+)(?:\s+\d+)?\s*>\}\}", bilibili, text
        )

        def video(match: re.Match) -> str:
            src = match.group(1)
            if not re.match(r"^https?://", src):
                src = site_url(CONFIG, "/" + src.lstrip("/"))
            return f"\n\n[Watch the video]({src})\n\n"

        text = re.sub(
            r"\{\{<\s*video\s+[^>]*src\s*=\s*[\"']([^\"']+)[\"'][^>]*>\}\}", video, text
        )

        def tencent(match: re.Match) -> str:
            return (
                "\n\n[Watch the video on Tencent Video]"
                f"(https://v.qq.com/x/page/{match.group(1)}.html)\n\n"
            )

        text = re.sub(r"\{\{<\s*tencent\s+([A-Za-z0-9]+)\s*>\}\}", tencent, text)

        # Unknown shortcodes cannot render anywhere else; remove them rather
        # than publishing raw Go template syntax.
        return re.sub(r"\{\{<[^>]*>\}\}", "", text)

    return apply_outside_fences(body, transform)


ALERT_RE = re.compile(r"^>\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*(.*)$")


def convert_alerts(body: str) -> str:
    lines = body.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        match = ALERT_RE.match(lines[i].strip())
        if not match:
            out.append(lines[i])
            i += 1
            continue
        kind, title = match.group(1), match.group(2).strip()
        out.append(f"> **{kind}**" + (f" â€” {title}" if title else ""))
        out.append(">")
        i += 1
        while i < len(lines):
            line = lines[i]
            if line.startswith(">"):
                content = re.sub(r"^>\s?", "", line)
                out.append(f"> {content}".rstrip())
                i += 1
            elif not line.strip():
                out.append(">")
                i += 1
                if i < len(lines) and not lines[i].startswith(">"):
                    break
            else:
                break
        out.append("")
    return "\n".join(out)


def is_plain_paragraph_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    if stripped.startswith(("#", ">", "|", "<", "![", "- ", "* ", "+ ")):
        return False
    if re.match(r"^\d+[.)]\s+", stripped):
        return False
    if re.match(r"^(---+|\*\*\*+|___+)$", stripped):
        return False
    if re.match(r"^\s*([-*_]\s*){3,}$", stripped):
        return False
    if stripped.startswith("{{") or stripped.startswith("```") or stripped.startswith("~~~"):
        return False
    return True


def unwrap_paragraphs(body: str) -> str:
    lines = body.splitlines()
    out: list[str] = []
    paragraph: list[str] = []
    in_fence = False

    def flush() -> None:
        if paragraph:
            joined = ""
            for part in paragraph:
                if not joined:
                    joined = part
                elif part.endswith("  "):
                    joined += "\n" + part
                else:
                    joined += " " + part
            out.append(joined)
            paragraph.clear()

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            flush()
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence or not is_plain_paragraph_line(line):
            flush()
            out.append(line)
            continue
        paragraph.append(line)
    flush()
    return "\n".join(out)


def rewrite_markdown_urls(body: str, config: dict, slug: str) -> str:
    base_site = config["site_url"].rstrip("/")

    def image(match: re.Match) -> str:
        alt, target = match.group(1), match.group(2).strip()
        if re.match(r"^(https?:|data:|#)", target):
            return match.group(0)
        if target.startswith("/"):
            return f"![{alt}]({base_site}{target})"
        clean = posixpath.normpath(target.lstrip("./"))
        return f"![{alt}]({raw_url(config, f'content/post/{slug}/{clean}')})"

    body = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+[\"'][^\"']*[\"'])?\)", image, body)

    def link(match: re.Match) -> str:
        label, target = match.group(1), match.group(2).strip()
        if re.match(r"^(https?:|mailto:|#|tel:)", target):
            return match.group(0)
        if target.startswith("/"):
            return f"[{label}]({base_site}{target})"
        clean = posixpath.normpath(target.lstrip("./"))
        return f"[{label}]({base_site}/p/{slug}/{clean})"

    body = re.sub(r"(?<!!)\[([^\]]+)\]\(([^)\s]+)\)", link, body)
    return body


def devto_tags(meta: dict, limit: int = 4) -> list[str]:
    raw = meta.get("tags") or meta.get("categories") or []
    if isinstance(raw, str):
        raw = [p.strip() for p in raw.split(",")]
    tags: list[str] = []
    for item in raw:
        tag = re.sub(r"[^A-Za-z0-9]", "", str(item))
        if tag and tag.lower() not in [t.lower() for t in tags]:
            tags.append(tag.lower())
    return tags[:limit]


def builder_tags(meta: dict, limit: int = 5) -> list[str]:
    raw = meta.get("tags") or []
    if isinstance(raw, str):
        raw = [p.strip() for p in raw.split(",")]
    return [str(t).strip() for t in raw if str(t).strip()][:limit]


# ---------------------------------------------------------------------------
# Dev.to markdown
# ---------------------------------------------------------------------------


def build_devto(meta: dict, body: str, config: dict, slug: str) -> str:
    if config.get("devto_publish", True):
        published = False  # source stays a draft; the payload flips it when live
    else:
        published = False

    title = str(meta.get("title") or "").strip()
    description = str(meta.get("description") or "").strip()
    cover = raw_url(config, cover_repo_path(meta, slug))

    body = strip_more(body)
    body = convert_shortcodes(body)
    body, _ = convert_mermaid(body)
    body = apply_outside_fences(body, convert_alerts)
    body = apply_outside_fences(body, lambda text: rewrite_markdown_urls(text, config, slug))
    body = unwrap_paragraphs(body)
    body = re.sub(r"\n{3,}", "\n\n", body).strip() + "\n"

    front = {
        "title": title,
        "published": published,
        "description": description,
        "tags": ", ".join(devto_tags(meta)),
        "cover_image": cover,
        "canonical_url": site_url(config, f"/p/{slug}/"),
    }
    fm = yaml.safe_dump(front, allow_unicode=True, sort_keys=False, width=1000).strip()
    return f"---\n{fm}\n---\n\n{body}"


# ---------------------------------------------------------------------------
# Builder Center markdown
# ---------------------------------------------------------------------------


def build_builder(meta: dict, body: str, config: dict, slug: str) -> tuple[str, str, str, str]:
    title = str(meta.get("title") or "").strip()
    description = str(meta.get("description") or "").strip()
    body = strip_more(body)
    body = convert_shortcodes(body)
    body, _ = convert_mermaid(body)
    body = apply_outside_fences(body, convert_alerts)
    body = apply_outside_fences(body, lambda text: rewrite_markdown_urls(text, config, slug))
    body = unwrap_paragraphs(body)
    body = strip_emoji(body)
    body = re.sub(r"\n{3,}", "\n\n", body).strip() + "\n"
    tags = "\n".join(builder_tags(meta)) + "\n"
    return body, title, description, tags


# ---------------------------------------------------------------------------
# HTML extraction from the Hugo build
# ---------------------------------------------------------------------------


def hugo_build(config: dict, slug: str) -> Path:
    existing = ROOT / "public"
    page = existing / "p" / slug / "index.html"
    source = post_dir(slug) / "index.md"
    if page.exists() and source.exists() and page.stat().st_mtime >= source.stat().st_mtime:
        return existing

    out = ROOT / "tmp" / "crosspost-build"
    if out.exists():
        shutil.rmtree(out, ignore_errors=True)
    try:
        proc = subprocess.run(
            [
                "hugo",
                "--quiet",
                "--minify",
                "--cleanDestinationDir",
                "--baseURL",
                config["site_url"].rstrip("/") + "/",
                "-d",
                str(out),
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        existing = ROOT / "public"
        if existing.exists():
            print("! hugo not found; using the existing public/ directory", file=sys.stderr)
            return existing
        sys.exit("hugo is required to build the Medium/Builder HTML")
    if proc.returncode != 0:
        message = (proc.stderr or proc.stdout or "").strip().splitlines()
        print("! hugo build failed: " + (message[-1] if message else "unknown error"), file=sys.stderr)
        existing = ROOT / "public"
        if existing.exists():
            print("! using the existing public/ directory", file=sys.stderr)
            return existing
        raise SystemExit(f"hugo build failed with exit code {proc.returncode}")
    return out


def extract_content(page_html: str) -> str:
    for start_marker in (
        "<div data-article-content-wrap><section class=article-content",
        "<section class=article-content",
    ):
        start = page_html.find(start_marker)
        if start != -1:
            break
    else:
        sys.exit("Could not find the article body in the rendered HTML")

    end = page_html.find("</section></div>", start)
    if end != -1:
        end += len("</section>")
    else:
        end = page_html.find("</section>", start)
        if end == -1:
            sys.exit("Could not find the end of the article body")
        end += len("</section>")

    content = page_html[start:end]
    content = re.sub(r"^<div data-article-content-wrap>\s*", "", content)
    content = re.sub(r"^<section[^>]*>", "", content)
    content = re.sub(r"</section>\s*$", "", content)
    return content


def absolute_html_urls(content: str, config: dict) -> str:
    base = config["site_url"].rstrip("/")

    def repl(match: re.Match) -> str:
        attr, quote, path = match.group(1), match.group(2) or "", match.group(3)
        if path.startswith("//"):
            return match.group(0)
        return f'{attr}={quote}{base}{path}{quote}'

    content = re.sub(r'(src|href|poster)=("?)(/[^"\'\s>]+)\2', repl, content)
    return content


# ---------------------------------------------------------------------------
# Tables to PNG (Medium cannot hold a table)
# ---------------------------------------------------------------------------


class TableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.rows: list[list[dict]] = []
        self.row: list[dict] | None = None
        self.cell: dict | None = None

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag == "tr":
            self.row = []
        elif tag in ("td", "th"):
            if self.row is None:
                self.row = []
            self.cell = {"text": "", "header": tag == "th"}
            self.row.append(self.cell)
        elif tag == "br" and self.cell is not None:
            self.cell["text"] += "\n"

    def handle_data(self, data: str) -> None:
        if self.cell is not None:
            self.cell["text"] += data

    def handle_endtag(self, tag: str) -> None:
        if tag in ("td", "th"):
            self.cell = None
        elif tag == "tr" and self.row is not None:
            if any(cell["text"].strip() for cell in self.row):
                self.rows.append(self.row)
            self.row = None


def _font(size: int, bold: bool = False):
    if Image is None:
        return None
    names = []
    if os.name == "nt":
        names += [
            r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
            r"C:\Windows\Fonts\seguisb.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
            r"C:\Windows\Fonts\calibrib.ttf" if bold else r"C:\Windows\Fonts\calibri.ttf",
        ]
    names += [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for name in names:
        if Path(name).exists():
            try:
                return ImageFont.truetype(name, size)
            except OSError:
                continue
    try:
        return ImageFont.load_default(size=size)
    except TypeError:  # Pillow < 10
        return ImageFont.load_default()


def _wrap(text: str, font, max_width: int) -> list[str]:
    lines: list[str] = []
    for raw_line in text.splitlines() or [""]:
        words = raw_line.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            candidate = current + " " + word
            if font.getlength(candidate) <= max_width:
                current = candidate
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines or [""]


def render_table(rows: list[list[dict]], out: Path) -> bool:
    if Image is None or not rows:
        return False
    scale = 2
    max_col_px = 420
    for font_size in (15, 13, 11, 10):
        font = _font(font_size * scale)
        bold = _font(font_size * scale, bold=True)
        if font is None:
            return False
        pad = int(12 * scale)
        columns = max(len(row) for row in rows)
        widths = [0] * columns
        wrapped: list[list[list[str]]] = []
        for row in rows:
            cells = []
            for idx in range(columns):
                cell = row[idx] if idx < len(row) else {"text": "", "header": False}
                lines = _wrap(cell["text"].strip(), font, max_col_px * scale)
                cells.append(lines)
                widths[idx] = max(
                    widths[idx],
                    max((int(font.getlength(line)) for line in lines), default=0),
                )
            wrapped.append(cells)
        total_width = sum(widths) + pad * (columns + 1)
        if total_width <= 1900 * scale:
            break
    else:
        return False

    line_h = int((font_size * 1.5) * scale)
    row_heights = [
        max(len(cells[idx]) for idx in range(columns)) * line_h + pad * 2
        for cells in wrapped
    ]

    width = sum(widths) + pad * (columns + 1)
    height = sum(row_heights) + pad

    image = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    y = pad
    for r_index, (row, cells) in enumerate(zip(rows, wrapped)):
        x = pad
        is_header = all(cell["header"] for cell in row) or r_index == 0
        bg = (245, 245, 245) if is_header else ((252, 252, 252) if r_index % 2 == 0 else (255, 255, 255))
        draw.rectangle([x, y, width - pad, y + row_heights[r_index]], fill=bg)
        for c_index in range(columns):
            cell_lines = cells[c_index]
            cell_font = bold if is_header else font
            ty = y + pad
            for line in cell_lines:
                draw.text((x + pad, ty), line, font=cell_font, fill=(26, 26, 26))
                ty += line_h
            x += widths[c_index] + pad
            draw.line([(x, y), (x, y + row_heights[r_index])], fill=(212, 212, 212), width=max(1, scale // 2))
        draw.line(
            [(pad, y + row_heights[r_index]), (width - pad, y + row_heights[r_index])],
            fill=(212, 212, 212),
            width=max(1, scale // 2),
        )
        y += row_heights[r_index]

    out.parent.mkdir(parents=True, exist_ok=True)
    image.save(out, format="PNG", optimize=True)
    return True


def tables_to_images(content: str, config: dict, slug: str) -> tuple[str, list[Path]]:
    written: list[Path] = []
    img_dir = public_img_dir(slug)
    counter = 0

    def repl(match: re.Match) -> str:
        nonlocal counter
        parser = TableParser()
        parser.feed(match.group(0))
        if not parser.rows:
            return match.group(0)
        counter += 1
        out = img_dir / f"table-{counter}.png"
        if not render_table(parser.rows, out):
            return match.group(0)
        written.append(out)
        url = raw_url(config, f"static/crosspost/{slug}/{out.name}")
        return f'<figure><img src="{url}" alt="Table {counter}"><figcaption>Table {counter}</figcaption></figure>'

    content = re.sub(
        r"(?s)<table\b(?![^>]*\blntable\b)[^>]*>.*?</table>", repl, content
    )
    return content, written


def strip_line_numbers(content: str) -> str:
    pattern = (
        r"(?s)<table class=lntable><tr><td class=lntd>.*?</td>"
        r"<td class=lntd>(<pre[^>]*>.*?</pre>)</td></tr></table>"
    )
    return re.sub(pattern, r"\1", content)


def mermaid_in_html(content: str, config: dict, slug: str) -> tuple[str, list[Path]]:
    written: list[Path] = []
    img_dir = public_img_dir(slug)
    counter = 0

    def repl(match: re.Match) -> str:
        nonlocal counter
        code = html.unescape(re.sub(r"<[^>]+>", "", match.group(1))).strip()
        if not code:
            return match.group(0)
        counter += 1
        url = mermaid_url(code)
        out = img_dir / f"mermaid-{counter}.png"
        written.append(out)  # recorded for the manifest; the image itself is remote
        return f'<figure><img src="{url}" alt="Diagram"><figcaption>Diagram</figcaption></figure>'

    content = re.sub(
        r'(?s)<pre[^>]*>\s*<code[^>]*class="?[^"]*language-mermaid[^"]*"?[^>]*>(.*?)</code>\s*</pre>',
        repl,
        content,
    )
    content = re.sub(r"<div class=highlight>\s*(<figure>.*?</figure>)\s*</div>", r"\1", content, flags=re.S)
    return content, written


def build_medium_html(page_html: str, meta: dict, config: dict, slug: str) -> str:
    content = extract_content(page_html)
    content = strip_line_numbers(content)
    content, _ = mermaid_in_html(content, config, slug)
    content, _ = tables_to_images(content, config, slug)
    content = absolute_html_urls(content, config)
    content = re.sub(r"(?s)<script\b.*?</script>", "", content)
    cover = raw_url(config, cover_repo_path(meta, slug))
    title = html.escape(str(meta.get("title") or ""))
    return (
        "<!doctype html>\n<html><head><meta charset=\"utf-8\">"
        f"<title>{title}</title></head><body>\n"
        f'<figure><img src="{cover}" alt="{title}"></figure>\n'
        f"{content}\n</body></html>\n"
    )


def build_builder_html(page_html: str, meta: dict, config: dict, slug: str) -> str:
    content = extract_content(page_html)
    content = strip_line_numbers(content)
    content, _ = mermaid_in_html(content, config, slug)
    content = absolute_html_urls(content, config)
    content = re.sub(r"(?s)<script\b.*?</script>", "", content)
    return (
        "<!doctype html>\n<html><head><meta charset=\"utf-8\">"
        f"<title>{html.escape(str(meta.get('title') or ''))}</title></head><body>\n"
        f"{content}\n</body></html>\n"
    )


# ---------------------------------------------------------------------------
# State and build orchestration
# ---------------------------------------------------------------------------


def load_state(slug: str) -> dict:
    path = artifacts_dir(slug) / "state.json"
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {}


def save_state(slug: str, state: dict) -> None:
    path = artifacts_dir(slug) / "state.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_links(slug: str, state: dict, config: dict) -> None:
    lines = [f"site = {site_url(config, f'/p/{slug}/')}"]
    devto = (state.get("devto") or {}).get("url")
    if devto:
        lines.append(f"devto = {devto}")
    (artifacts_dir(slug) / "links.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def build(slug: str, config: dict, quiet: bool = False) -> dict:
    source = post_dir(slug) / "index.md"
    if not source.exists():
        sys.exit(f"Post not found: {source}")
    meta, body = parse_post(source)
    out = artifacts_dir(slug)
    out.mkdir(parents=True, exist_ok=True)
    public_img_dir(slug).mkdir(parents=True, exist_ok=True)

    state = load_state(slug)
    state.update(
        {
            "slug": slug,
            "title": str(meta.get("title") or ""),
            "site_url": site_url(config, f"/p/{slug}/"),
            "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }
    )

    devto = build_devto(meta, body, config, slug)
    (out / "devto.md").write_text(devto, encoding="utf-8")

    builder_md, builder_title, builder_desc, builder_tags_text = build_builder(
        meta, body, config, slug
    )
    (out / "builder.md").write_text(builder_md, encoding="utf-8")
    (out / "builder-title.txt").write_text(builder_title + "\n", encoding="utf-8")
    (out / "builder-description.txt").write_text(builder_desc + "\n", encoding="utf-8")
    (out / "builder-tags.txt").write_text(builder_tags_text, encoding="utf-8")

    build_dir = hugo_build(config, slug)
    page = build_dir / "p" / slug / "index.html"
    if not page.exists():
        sys.exit(
            f"Rendered page not found: {page}. Check the slug and that `hugo` builds."
        )
    page_html = page.read_text(encoding="utf-8", errors="replace")
    medium = build_medium_html(page_html, meta, config, slug)
    (out / "medium.html").write_text(medium, encoding="utf-8")
    builder_html = build_builder_html(page_html, meta, config, slug)
    (out / "builder.html").write_text(builder_html, encoding="utf-8")

    state["cover_url"] = raw_url(config, cover_repo_path(meta, slug))
    state["artifacts"] = {
        name: rel_posix(out / name)
        for name in (
            "devto.md",
            "builder.md",
            "builder.html",
            "medium.html",
        )
        if (out / name).exists()
    }
    save_state(slug, state)
    write_links(slug, state, config)
    write_instructions(slug, meta, state, config)
    if not quiet:
        print(f"built {slug}")
        for name, path in state["artifacts"].items():
            print(f"  {name:<18} {path}")
    return state


def write_instructions(slug: str, meta: dict, state: dict, config: dict) -> None:
    out = artifacts_dir(slug)
    devto = state.get("devto") or {}
    lines = [
        f"Cross-post kit for {slug}",
        "=" * (20 + len(slug)),
        "",
        f"Source: content/post/{slug}/index.md",
        f"Site:   {site_url(config, f'/p/{slug}/')}",
        f"Cover:  {state.get('cover_url')}",
        "",
        f"Commit and push this article, .crosspost/{slug}/ and static/crosspost/{slug}/",
        "before publishing anywhere. dev.to and Medium fetch images by URL.",
        "",
        "DEV.TO",
        "  Published by this tool. Status: "
        + (
            f"{'live' if devto.get('published') else 'draft'} {devto.get('url', '')}".strip()
            if devto
            else "not published yet"
        ),
        f"  File: {rel_posix(out / 'devto.md')} (source stays published: false).",
        "",
        "MEDIUM",
        "  1. Open https://medium.com/new-story",
        "  2. Type the title from the source front matter (Medium never fills it).",
        f"  3. Open {rel_posix(out / 'medium.html')} in a browser, select all, copy,",
        "     and paste into the Medium body. Tables are PNG images hosted on",
        "     raw.githubusercontent.com, and Medium re-hosts them.",
        "  4. Add topics and publish.",
        "",
        "AWS BUILDER CENTER",
        "  1. builder.aws.com -> + -> Article.",
        f"  2. Title: {rel_posix(out / 'builder-title.txt')}",
        f"  3. Description: {rel_posix(out / 'builder-description.txt')}",
        f"  4. Paste the body from {rel_posix(out / 'builder.html')} (tables render natively).",
        f"  5. Tags (max 5): {rel_posix(out / 'builder-tags.txt')}",
        f"  6. Upload the cover: content/post/{slug}/{meta.get('image') or 'cover.jpg'}",
        "     (recommended 1200x675).",
        "",
        "Re-run: python scripts/crosspost/crosspost.py build " + slug,
    ]
    (out / "instructions.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# dev.to API
# ---------------------------------------------------------------------------


def devto_key() -> str:
    key = os.environ.get("DEV_TO_API_KEY", "").strip()
    if key:
        return key
    path = Path.home() / ".devto.key"
    if path.exists():
        return path.read_text(encoding="utf-8").strip()
    sys.exit(
        "No dev.to API key. Set DEV_TO_API_KEY or write the key to ~/.devto.key, "
        "then re-run. Never commit the key."
    )


def devto_call(method: str, path: str, key: str, payload: dict | None = None) -> dict:
    url = "https://dev.to/api" + path
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(
        url,
        method=method,
        data=data,
        headers={
            "api-key": key,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "dev9b-crosspost/1.0",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            body = response.read()
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        sys.exit(f"dev.to {method} {path} failed: {exc.code} {detail}")
    except urllib.error.URLError as exc:
        sys.exit(f"dev.to unreachable: {exc.reason}")


def devto_org_id(slug: str, key: str) -> int | None:
    if not slug:
        return None
    try:
        org = devto_call("GET", f"/organizations/{slug}", key)
    except SystemExit:
        print(f"! dev.to organization '{slug}' not found; publishing under the user", file=sys.stderr)
        return None
    if isinstance(org, dict) and org.get("id"):
        return int(org["id"])
    return None


def devto_listing(key: str) -> list[dict]:
    return devto_call("GET", "/articles/me?per_page=100", key) or []


def find_listing(articles: list[dict], article_id: int) -> dict | None:
    for article in articles:
        if int(article.get("id", 0)) == article_id:
            return article
    return None


def devto_publish_payload(
    meta: dict, devto_markdown: str, config: dict, slug: str, live: bool
) -> dict:
    body = devto_markdown
    if live:
        body = re.sub(
            r"(?m)^published:\s*false\s*$",
            "published: true",
            body,
            count=1,
        )
    return {
        "article": {
            "title": str(meta.get("title") or "").strip(),
            "body_markdown": body,
            "description": str(meta.get("description") or "").strip(),
            "tags": devto_tags(meta),
            "canonical_url": site_url(config, f"/p/{slug}/"),
            "cover_image": raw_url(config, cover_repo_path(meta, slug)),
        }
    }


def check_public_url(url: str) -> bool:
    request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "dev9b-crosspost/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return 200 <= response.status < 400
    except urllib.error.HTTPError:
        return False
    except urllib.error.URLError:
        return False


def publish_devto(slug: str, meta: dict, config: dict, live: bool) -> dict:
    key = devto_key()
    artifacts = artifacts_dir(slug)
    state = load_state(slug)

    cover = raw_url(config, cover_repo_path(meta, slug))
    if live and not check_public_url(cover):
        sys.exit(
            "Cover is not reachable yet:\n  "
            + cover
            + "\nCommit and push the article before publishing live."
        )

    payload = devto_publish_payload(
        meta,
        (artifacts / "devto.md").read_text(encoding="utf-8"),
        config,
        slug,
        live,
    )

    existing = state.get("devto") or {}
    article_id = existing.get("id")
    if article_id:
        response = devto_call("PUT", f"/articles/{article_id}", key, payload)
        action = "updated"
    else:
        response = devto_call("POST", "/articles", key, payload)
        action = "created"
        article_id = response.get("id")
        if not article_id:
            sys.exit(f"dev.to did not return an article id: {response}")

    org_slug = config.get("devto_org")
    org_id = devto_org_id(org_slug, key) if org_slug else None
    if org_id:
        devto_call("PUT", f"/articles/{article_id}", key, {"article": {"organization_id": org_id}})

    articles = devto_listing(key)
    final = find_listing(articles, int(article_id))
    if final is None:
        sys.exit(
            "The article is not in your dev.to listing after "
            f"{action}. Check the API key and the article id {article_id}."
        )

    if live and not final.get("published"):
        # dev.to reads `published` from the front matter in body_markdown. Send it
        # once more if the first request only created a draft, then confirm.
        devto_call("PUT", f"/articles/{article_id}", key, payload)
        articles = devto_listing(key)
        final = find_listing(articles, int(article_id)) or final
        if not final.get("published"):
            sys.exit(
                "dev.to still reports the article as a draft. Open "
                f"{final.get('url', '')} and publish it manually, then re-run."
            )

    state["devto"] = {
        "id": int(article_id),
        "url": final.get("url") or response.get("url"),
        "published": bool(final.get("published")),
        "org": (final.get("organization") or {}).get("slug") or org_slug,
        "updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    save_state(slug, state)
    write_links(slug, state, config)
    write_instructions(slug, meta, state, config)
    return state


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def find_latest() -> str:
    candidates: list[tuple[str, str]] = []
    for directory in (ROOT / "content" / "post").iterdir():
        source = directory / "index.md"
        if not source.exists():
            continue
        meta, _ = parse_post(source)
        candidates.append((iso(meta.get("date")), directory.name))
    if not candidates:
        sys.exit("No posts found under content/post/")
    return max(candidates)[1]


def main(argv: list[str] | None = None) -> int:
    global CONFIG
    parser = argparse.ArgumentParser(description="Syndicate a Dev9b article everywhere.")
    parser.add_argument(
        "command",
        choices=["build", "publish", "all", "latest"],
        help="build artifacts, publish to dev.to, or do both",
    )
    parser.add_argument("slug", nargs="?", help="post slug (defaults to latest for 'latest')")
    parser.add_argument("--draft", action="store_true", help="create a dev.to draft instead of live")
    parser.add_argument("--org-slug", default=None, help="override the dev.to organization")
    args = parser.parse_args(argv)

    CONFIG = load_config()
    if args.org_slug:
        CONFIG["devto_org"] = args.org_slug

    if args.command == "latest":
        slug = args.slug or find_latest()
        args.command = "all"
    else:
        slug = args.slug
    if not slug:
        parser.error("a slug is required")

    if args.command == "build":
        build(slug, CONFIG)
        return 0

    if args.command in ("publish", "all"):
        build(slug, CONFIG)
        meta, _ = parse_post(post_dir(slug) / "index.md")
        live = not args.draft
        state = publish_devto(slug, meta, CONFIG, live)
        devto = state.get("devto") or {}
        print(f"{'published' if devto.get('published') else 'draft'} {slug}")
        print(f"  dev.to  {devto.get('url')}")
        print(f"  medium  {rel_posix(artifacts_dir(slug) / 'medium.html')}")
        print(f"  builder {rel_posix(artifacts_dir(slug) / 'builder.html')}")
        return 0

    return 1


CONFIG: dict = {}


if __name__ == "__main__":
    raise SystemExit(main())
