#!/usr/bin/env python3
"""Mark the sixth twenty-book batch as summarized in the reading map."""

import json
from pathlib import Path

from build_static import summary_path


ROOT = Path(__file__).resolve().parents[1]
NUMBERS = {16, 20, 22, 39, 43, 67, 76, 85, 98, 108, 135, 155, 161, 178, 184, 204, 212, 235, 255, 288}

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
print(f"Marked {len(found)} books as summarized")
