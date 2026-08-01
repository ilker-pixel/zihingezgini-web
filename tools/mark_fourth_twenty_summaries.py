#!/usr/bin/env python3
"""Mark the fourth twenty-book batch as summarized in the reading map."""

import json
from pathlib import Path

from build_static import summary_path


ROOT = Path(__file__).resolve().parents[1]
NUMBERS = {10, 14, 35, 47, 58, 64, 71, 91, 104, 110, 139, 153, 165, 176, 191, 200, 218, 229, 254, 285}


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
