#!/usr/bin/env python3
"""Render all pages of final wave seven."""

from render_final_wave_pdfs import ROOT, render


if __name__ == "__main__":
    render(
        (273, 274, 276, 278, 279, 280, 281, 282, 283),
        ROOT / "tmp" / "final-wave-7-pdf-renders",
    )
