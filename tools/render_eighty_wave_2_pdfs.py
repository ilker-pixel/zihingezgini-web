#!/usr/bin/env python3
"""Render every page of the second 80-book wave and build visual contact sheets."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOKS = (23, 44, 74, 97, 140, 160, 192, 221, 120, 286)
OUT = ROOT / "tmp" / "eighty-wave-2-pdf-renders"


def main() -> None:
    renderer = shutil.which("pdftoppm")
    if not renderer:
        raise RuntimeError("pdftoppm is required for PDF visual QA")
    for number in BOOKS:
        summary = json.loads(
            (ROOT / "data" / "summaries" / f"{number}.json").read_text(encoding="utf-8")
        )
        pdf = ROOT / summary["pdfUrl"].lstrip("/")
        target = OUT / str(number)
        target.mkdir(parents=True, exist_ok=True)
        for old in target.glob("page-*.png"):
            old.unlink()
        subprocess.run(
            [renderer, "-png", "-r", "96", str(pdf), str(target / "page")],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        subprocess.run(
            ["python3", str(ROOT / "tools" / "make_full_pdf_contact_sheet.py"), str(target)],
            check=True,
        )
        print(f"{number}: rendered {len(list(target.glob('page-*.png')))} pages")


if __name__ == "__main__":
    main()
