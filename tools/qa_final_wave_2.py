#!/usr/bin/env python3
"""Run the strict gate for final wave two."""

from qa_final_wave import ROOT, run


if __name__ == "__main__":
    run(
        (128, 131, 132, 133, 134, 144, 148, 170, 174),
        ROOT / "tmp" / "final-wave-2-pdf-renders",
    )
