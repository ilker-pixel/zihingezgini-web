#!/usr/bin/env python3
"""Render every page of wave 5 PDFs and build compact contact sheets."""

import render_eighty_wave_3_pdfs as base


base.OUT = base.ROOT / "tmp" / "eighty-wave-5-pdf-renders"
base.BOOKS = (27, 49, 80, 106, 181, 164, 201, 251, 126, 293)


if __name__ == "__main__":
    base.main()
