#!/usr/bin/env python3
"""Render all pages of final wave five."""

from render_final_wave_pdfs import ROOT, render


if __name__ == "__main__":
    render(
        (236, 237, 246, 247, 249, 250, 252, 257, 260),
        ROOT / "tmp" / "final-wave-5-pdf-renders",
    )
