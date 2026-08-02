#!/usr/bin/env python3
"""Render all pages of final wave three."""

from render_final_wave_pdfs import ROOT, render


if __name__ == "__main__":
    render(
        (175, 177, 180, 198, 202, 203, 206, 207, 208),
        ROOT / "tmp" / "final-wave-3-pdf-renders",
    )
