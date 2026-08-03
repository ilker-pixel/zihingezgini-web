#!/usr/bin/env python3
"""Create bounded WebP display copies for images that can appear above the fold."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
IMAGE_ROOT = ROOT / "images"
OUTPUT_ROOT = IMAGE_ROOT / "optimized"
MAX_EDGE = 720


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def collect_assets() -> list[Path]:
    values = {
        "/images/zihin_gezgini_logo_sketch.png",
        "/images/thinking_man_sketch.png",
    }
    for path in (ROOT / "data" / "summaries").glob("*.json"):
        value = load(path).get("coverImage")
        if value:
            values.add(value)
    for path in (ROOT / "data" / "posts").glob("*.json"):
        value = load(path).get("featuredImage")
        if value:
            values.add(value)
    for item in load(ROOT / "data" / "kutuphane_index.json"):
        value = item.get("cover")
        if value:
            values.add("/" + value.lstrip("/"))
    return sorted(
        ROOT / value.lstrip("/") for value in values
        if str(value).startswith("/images/") and (ROOT / str(value).lstrip("/")).is_file()
    )


def output_path(source: Path) -> Path:
    relative = source.relative_to(IMAGE_ROOT)
    return OUTPUT_ROOT / relative.parent / f"{relative.stem}-960.webp"


def optimize(source: Path) -> tuple[Path, int, int]:
    target = output_path(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as opened:
        image = ImageOps.exif_transpose(opened)
        image.thumbnail((MAX_EDGE, MAX_EDGE), Image.Resampling.LANCZOS)
        if image.mode not in {"RGB", "RGBA"}:
            image = image.convert("RGBA" if "transparency" in image.info else "RGB")
        image.save(target, "WEBP", quality=72, method=6, exact=image.mode == "RGBA")
    return target, source.stat().st_size, target.stat().st_size


def main() -> int:
    sources = collect_assets()
    original_bytes = 0
    optimized_bytes = 0
    for source in sources:
        _, original, optimized = optimize(source)
        original_bytes += original
        optimized_bytes += optimized
    saving = 100 * (1 - optimized_bytes / original_bytes) if original_bytes else 0
    print(
        f"Optimized {len(sources)} display images: {original_bytes / 1024 / 1024:.1f} MB -> "
        f"{optimized_bytes / 1024 / 1024:.1f} MB ({saving:.1f}% smaller)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
