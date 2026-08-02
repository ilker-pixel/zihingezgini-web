#!/usr/bin/env python3
"""Build the nine visually rich PDFs for final wave two."""

from pathlib import Path

import build_repaired_forty_summary_pdfs as repaired


repaired.builder.BOOK_NUMBERS = (128, 131, 132, 133, 134, 144, 148, 170, 174)
repaired.builder.TMP = Path(__file__).resolve().parents[1] / "tmp" / "pdfs" / "final-wave-2"


if __name__ == "__main__":
    repaired.builder.main()
