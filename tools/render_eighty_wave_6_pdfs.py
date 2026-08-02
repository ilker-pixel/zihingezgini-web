#!/usr/bin/env python3
"""Render every page in the sixth 80-book wave for visual QA."""

from pathlib import Path

import render_eighty_wave_3_pdfs as base


base.OUT = Path(__file__).resolve().parents[1] / "tmp" / "rendered" / "eighty-wave-6"
base.BOOKS = (28, 51, 86, 112, 186, 166, 205, 256, 149, 171)


if __name__ == "__main__":
    base.main()
