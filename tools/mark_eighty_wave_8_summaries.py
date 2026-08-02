#!/usr/bin/env python3
"""Mark the eighth 80-book wave as summarized in the reading map."""

import json
from pathlib import Path

from build_static import summary_path
from eighty_summary_manifest import set_stage


ROOT = Path(__file__).resolve().parents[1]
NUMBERS = {56, 54, 125, 116, 188, 168, 210, 259, 129, 150}


if __name__ == "__main__":
    books_path = ROOT / "data" / "books.json"
    books = json.loads(books_path.read_text(encoding="utf-8"))
    found = set()
    for book in books:
        number = int(book["no"])
        if number not in NUMBERS:
            continue
        summary = json.loads((ROOT / "data" / "summaries" / f"{number}.json").read_text(encoding="utf-8"))
        book["hasSummary"] = True
        book["summaryUrl"] = summary_path(summary)
        found.add(number)

    missing = NUMBERS - found
    if missing:
        raise RuntimeError(f"Missing books: {sorted(missing)}")

    books_path.write_text(json.dumps(books, ensure_ascii=False, indent=4) + "\n", encoding="utf-8")
    set_stage(sorted(NUMBERS), "site_ready", {
        "characterGate": True,
        "exactSharedParagraphs": 0,
        "interiorImages": 16,
        "coverIndependentAndColor": True,
        "pageGate": True,
        "allPagesRendered": True,
        "visualInspection": "passed",
        "staticIntegration": True,
    })
    print(f"Marked {len(found)} books as summarized and site-ready")
