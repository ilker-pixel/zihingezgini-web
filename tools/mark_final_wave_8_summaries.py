#!/usr/bin/env python3
"""Mark final wave eight as summarized and site-ready after QA."""

import json

from pypdf import PdfReader

from build_static import summary_path
from final_summary_manifest import ROOT, set_stage


NUMBERS = {289, 291, 292, 295, 296, 297, 298, 299, 300}
books_path = ROOT / "data" / "books.json"
books = json.loads(books_path.read_text(encoding="utf-8"))
found = set()
page_counts = {}
for item in books:
    number = int(item["no"])
    if number not in NUMBERS:
        continue
    summary = json.loads((ROOT / "data" / "summaries" / f"{number}.json").read_text(encoding="utf-8"))
    item["hasSummary"] = True
    item["summaryUrl"] = summary_path(summary)
    pdf_path = ROOT / summary["pdfUrl"].lstrip("/")
    page_counts[number] = len(PdfReader(str(pdf_path)).pages)
    found.add(number)

if found != NUMBERS:
    raise RuntimeError(f"Missing books: {sorted(NUMBERS - found)}")
books_path.write_text(json.dumps(books, ensure_ascii=False, indent=4) + "\n", encoding="utf-8")

set_stage(sorted(NUMBERS), "art_ready", {"chapterImages": 16, "coverIndependent": True})
set_stage(sorted(NUMBERS), "pdf_ready", {"pageCounts": page_counts, "embeddedImages": 17})
set_stage(sorted(NUMBERS), "qa_passed", {
    "characterGate": True,
    "exactSharedParagraphs": 0,
    "nearDuplicateParagraphs": 0,
    "repeatedLongSentences": 0,
    "allPagesRendered": True,
    "visualInspection": "passed",
})
set_stage(sorted(NUMBERS), "site_ready", {"staticIntegration": True})
print(f"Marked {len(found)} final-wave-eight works as site-ready")
