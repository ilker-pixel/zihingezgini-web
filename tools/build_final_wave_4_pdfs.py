#!/usr/bin/env python3
"""Build the nine visually rich PDFs for final wave four."""

from pathlib import Path

import build_repaired_forty_summary_pdfs as repaired


repaired.builder.BOOK_NUMBERS = (219, 226, 227, 228, 230, 231, 232, 233, 234)
repaired.builder.TMP = Path(__file__).resolve().parents[1] / "tmp" / "pdfs" / "final-wave-4"


if __name__ == "__main__":
    repaired.builder.main()
