#!/usr/bin/env python3
"""Run the strict gate for final wave three."""

from qa_final_wave import ROOT, run


if __name__ == "__main__":
    run(
        (175, 177, 180, 198, 202, 203, 206, 207, 208),
        ROOT / "tmp" / "final-wave-3-pdf-renders",
    )
