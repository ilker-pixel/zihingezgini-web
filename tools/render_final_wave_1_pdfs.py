#!/usr/bin/env python3
"""Render all 243 pages of final wave one."""

from render_final_wave_pdfs import ROOT, render


if __name__ == "__main__":
    render(
        (30, 52, 83, 84, 102, 113, 115, 117, 119),
        ROOT / "tmp" / "final-wave-1-pdf-renders",
    )
