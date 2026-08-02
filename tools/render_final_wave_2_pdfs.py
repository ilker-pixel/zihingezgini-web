#!/usr/bin/env python3
"""Render all pages of final wave two."""

from render_final_wave_pdfs import ROOT, render


if __name__ == "__main__":
    render(
        (128, 131, 132, 133, 134, 144, 148, 170, 174),
        ROOT / "tmp" / "final-wave-2-pdf-renders",
    )
