#!/usr/bin/env python3
"""Render all pages of final wave eight."""

from render_final_wave_pdfs import ROOT, render


if __name__ == "__main__":
    render(
        (289, 291, 292, 295, 296, 297, 298, 299, 300),
        ROOT / "tmp" / "final-wave-8-pdf-renders",
    )
