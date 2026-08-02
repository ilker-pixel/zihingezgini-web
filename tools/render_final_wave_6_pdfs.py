#!/usr/bin/env python3
"""Render all pages of final wave six."""

from render_final_wave_pdfs import ROOT, render


if __name__ == "__main__":
    render(
        (261, 262, 264, 265, 267, 268, 269, 270, 272),
        ROOT / "tmp" / "final-wave-6-pdf-renders",
    )
