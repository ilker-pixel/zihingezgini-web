#!/usr/bin/env python3
"""Build the nine visually rich PDFs for final wave one."""

from pathlib import Path

import build_repaired_forty_summary_pdfs as repaired


repaired.builder.BOOK_NUMBERS = (30, 52, 83, 84, 102, 113, 115, 117, 119)
repaired.builder.TMP = Path(__file__).resolve().parents[1] / "tmp" / "pdfs" / "final-wave-1"


if __name__ == "__main__":
    repaired.builder.main()
