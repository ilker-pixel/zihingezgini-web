#!/usr/bin/env python3
"""Run the strict gate for final wave six."""

from qa_final_wave import ROOT, run


if __name__ == "__main__":
    run(
        (261, 262, 264, 265, 267, 268, 269, 270, 272),
        ROOT / "tmp" / "final-wave-6-pdf-renders",
    )
