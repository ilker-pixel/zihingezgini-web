#!/usr/bin/env python3
"""Render every page in the seventh 80-book wave for visual QA."""

from pathlib import Path

import render_eighty_wave_3_pdfs as base


base.OUT = Path(__file__).resolve().parents[1] / "tmp" / "rendered" / "eighty-wave-7"
base.BOOKS = (29, 53, 123, 114, 187, 167, 209, 258, 57, 245)


if __name__ == "__main__":
    base.main()
