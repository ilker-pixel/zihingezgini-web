#!/usr/bin/env python3
"""Prepare the nine covers and 144 chapter images for final wave one."""

from pathlib import Path

from prepare_final_wave_art import ROOT, prepare


SOURCES = {
    30: ("exec-84d4ef41-84a9-4edd-8b9b-378be75d7aaf.png", "exec-049e51f9-4f80-48f3-8314-c470d795a4a3.png"),
    52: ("exec-5e0ec44e-8f4a-4c15-97aa-2616ce0b2dab.png", "exec-8029ee7d-dc67-4013-9fc3-43aca72b5b37.png"),
    83: ("exec-914c1c70-c29c-4204-8fef-09633e7da678.png", "exec-fe3cd602-9215-4b5b-8319-a64d11c4d82b.png"),
    84: ("exec-ee4120a6-0637-447d-b94e-c887087807d4.png", "exec-ccac3703-8b01-4b94-b885-638779646067.png"),
    102: ("exec-a302c8f0-e581-4637-ba1a-fa1fc389b1e6.png", "exec-102db8e8-5d2a-42b2-a5d8-3c334f17f910.png"),
    113: ("exec-1e5856d1-7d3b-448f-807a-3d80e518c54e.png", "exec-41194960-a2ed-45a6-ae1e-92082815ef88.png"),
    115: ("exec-5ca051fa-f177-47a2-b0b3-e5bf45b20efc.png", "exec-5978b4a3-e83b-4e7b-89fb-c9dab9c7bc63.png"),
    117: ("exec-bf98b437-0d5c-4238-996f-23dced54330d.png", "exec-0f4c5d39-286c-4ee7-bad5-a9e66466e092.png"),
    119: ("exec-4eb1e6cb-c6b9-4a6b-9556-65ac342b0db7.png", "exec-3ace0904-101b-4549-8871-f40a364c3659.png"),
}


if __name__ == "__main__":
    prepare(SOURCES, ROOT / "tmp" / "final-wave-1-art", "final-wave-1")
