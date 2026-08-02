#!/usr/bin/env python3
"""Build the nine visually rich PDFs for final wave seven."""

from pathlib import Path

import build_repaired_forty_summary_pdfs as repaired


repaired.builder.BOOK_NUMBERS = (273, 274, 276, 278, 279, 280, 281, 282, 283)
repaired.builder.TMP = Path(__file__).resolve().parents[1] / "tmp" / "pdfs" / "final-wave-7"


if __name__ == "__main__":
    repaired.builder.main()
