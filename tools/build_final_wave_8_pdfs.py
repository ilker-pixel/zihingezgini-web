#!/usr/bin/env python3
"""Build the nine visually rich PDFs for final wave eight."""

from pathlib import Path

import build_repaired_forty_summary_pdfs as repaired


repaired.builder.BOOK_NUMBERS = (289, 291, 292, 295, 296, 297, 298, 299, 300)
repaired.builder.TMP = Path(__file__).resolve().parents[1] / "tmp" / "pdfs" / "final-wave-8"


if __name__ == "__main__":
    repaired.builder.main()
