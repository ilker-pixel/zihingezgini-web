#!/usr/bin/env python3
"""Fail before the publishable static payload reaches the GitHub Pages ceiling."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIRS = (ROOT / "images", ROOT / "data" / "pdfs", ROOT / "audio", ROOT / "covers")
BUDGET = 900 * 1024 * 1024


def main() -> int:
    total = sum(path.stat().st_size for directory in ASSET_DIRS for path in directory.rglob("*") if path.is_file())
    print(f"Publishable media: {total / 1024 / 1024:.1f} MB / {BUDGET / 1024 / 1024:.0f} MB budget.")
    if total > BUDGET:
        print("Asset budget exceeded. Move PDFs and original-resolution images to object storage before publishing.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
