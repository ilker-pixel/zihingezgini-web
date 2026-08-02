#!/usr/bin/env python3
"""Render every page in the eighth 80-book wave for visual QA."""

from pathlib import Path

import render_eighty_wave_3_pdfs as base


base.OUT = Path(__file__).resolve().parents[1] / "tmp" / "rendered" / "eighty-wave-8"
base.BOOKS = (56, 54, 125, 116, 188, 168, 210, 259, 129, 150)


if __name__ == "__main__":
    base.main()
