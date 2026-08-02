#!/usr/bin/env python3
"""Build the nine visually rich PDFs for final wave six."""

from pathlib import Path

import build_repaired_forty_summary_pdfs as repaired


repaired.builder.BOOK_NUMBERS = (261, 262, 264, 265, 267, 268, 269, 270, 272)
repaired.builder.TMP = Path(__file__).resolve().parents[1] / "tmp" / "pdfs" / "final-wave-6"


if __name__ == "__main__":
    repaired.builder.main()
