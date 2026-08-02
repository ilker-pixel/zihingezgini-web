#!/usr/bin/env python3
"""Build the nine visually rich PDFs for final wave three."""

from pathlib import Path

import build_repaired_forty_summary_pdfs as repaired


repaired.builder.BOOK_NUMBERS = (175, 177, 180, 198, 202, 203, 206, 207, 208)
repaired.builder.TMP = Path(__file__).resolve().parents[1] / "tmp" / "pdfs" / "final-wave-3"


if __name__ == "__main__":
    repaired.builder.main()
