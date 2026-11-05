#!/usr/bin/env python3
"""Generate a Dev9b cover image (1200x630) with the F9XR palette.

    python scripts/crosspost/make_cover.py \
        --title "Puter.js Explained" \
        --subtitle "Build a SaaS app with no backend" \
        --kicker "AI TOOLS" \
        --out content/post/<slug>/cover.jpg

The output is progressive JPEG, normally under 100 KB.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:  # pragma: no cover
    sys.exit("Pillow is required: python -m pip install Pillow")

W, H = 1200, 630
BG = (15, 22, 38)
INK = (245, 248, 255)
MUTED = (154, 170, 196)
BLUE = (56, 132, 255)
CYAN = (80, 214, 255)
ORANGE = (255, 138, 64)


def font(size: int, bold: bool = False):
    names = []
    if sys.platform.startswith("win"):
        names += [
            r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
            r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
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
            return ImageFont.truetype(name, size)
    try:
        return ImageFont.load_default(size=size)
    except TypeError:  # pragma: no cover
        return ImageFont.load_default()


def wrap(text: str, face, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if face.getlength(candidate) <= max_width or not current:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True)
    parser.add_argument("--subtitle", default="")
    parser.add_argument("--kicker", default="DEV9B")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    image = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(image)

    for y in range(H):
        t = y / H
        color = (
            int(BG[0] + (18 - BG[0]) * t),
            int(BG[1] + (30 - BG[1]) * t),
            int(BG[2] + (58 - BG[2]) * t),
        )
        draw.line([(0, y), (W, y)], fill=color)

    draw.ellipse([820, -160, 1360, 380], fill=(30, 50, 92))
    draw.ellipse([980, 260, 1320, 600], fill=(20, 36, 66))
    draw.rounded_rectangle([72, 92, 158, 104], radius=6, fill=CYAN)
    draw.ellipse([1048, 92, 1078, 122], fill=ORANGE)

    kicker_face = font(24, bold=True)
    draw.text((72, 58), args.kicker.upper(), font=kicker_face, fill=CYAN)

    title_face = font(58, bold=True)
    y = 150
    for line in wrap(args.title, title_face, 900):
        draw.text((72, y), line, font=title_face, fill=INK)
        y += 72

    if args.subtitle:
        sub_face = font(30)
        y += 14
        for line in wrap(args.subtitle, sub_face, 880):
            draw.text((72, y), line, font=sub_face, fill=MUTED)
            y += 42

    draw.rounded_rectangle([72, H - 112, 330, H - 58], radius=10, outline=(60, 82, 120), width=2)
    draw.text((96, H - 101), "F9XR  /  DEV9B", font=font(22, bold=True), fill=INK)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    image.save(out, format="JPEG", quality=86, optimize=True, progressive=True)
    print(f"wrote {out} {image.width}x{image.height} {out.stat().st_size // 1024} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
