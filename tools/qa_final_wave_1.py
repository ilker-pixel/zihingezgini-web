#!/usr/bin/env python3
"""Run the strict gate for final wave one."""

from qa_final_wave import ROOT, run


if __name__ == "__main__":
    run(
        (30, 52, 83, 84, 102, 113, 115, 117, 119),
        ROOT / "tmp" / "final-wave-1-pdf-renders",
    )
