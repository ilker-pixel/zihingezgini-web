#!/usr/bin/env python3
"""Render all pages of final wave four."""

from render_final_wave_pdfs import ROOT, render


if __name__ == "__main__":
    render(
        (219, 226, 227, 228, 230, 231, 232, 233, 234),
        ROOT / "tmp" / "final-wave-4-pdf-renders",
    )
