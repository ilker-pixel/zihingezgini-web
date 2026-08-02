#!/usr/bin/env python3
"""Render every page of wave 4 PDFs and build compact contact sheets."""

import render_eighty_wave_3_pdfs as base


base.OUT = base.ROOT / "tmp" / "eighty-wave-4-pdf-renders"
base.BOOKS = (26, 46, 78, 105, 147, 163, 197, 225, 55, 242)


if __name__ == "__main__":
    base.main()
