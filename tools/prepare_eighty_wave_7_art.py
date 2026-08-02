#!/usr/bin/env python3
"""Prepare covers and 16 chapter images for the seventh 80-book wave."""

from pathlib import Path

import prepare_eighty_wave_3_art as base


ROOT = Path(__file__).resolve().parents[1]
base.TMP = ROOT / "tmp" / "eighty-wave-7"
base.SOURCES = {
    29: ("exec-a13d4264-bab5-41c4-911e-0db0fe706e33.png", "exec-aff7ed23-7607-42c6-af6d-18189ff20ca8.png"),
    53: ("exec-fac45d56-7299-48b8-ba56-c9ea83cfe7a4.png", "exec-08c389f6-bcab-4414-924e-3fd81572d1a2.png"),
    123: ("exec-2556b7e3-6c98-4ccd-a52a-008d4113b0a7.png", "exec-3a0b4f26-9662-4239-9f23-df95bd3d9316.png"),
    114: ("exec-c08b2b47-13f6-41ea-9e27-0bfd69f7357f.png", "exec-ac6f8751-84bf-4fe8-93c5-2471a7f59932.png"),
    187: ("exec-ef90f9ee-b202-4d9a-ae7c-129b866f3dbc.png", "exec-9b0642c0-4662-4bd9-a618-9e398851aa70.png"),
    167: ("exec-e691755e-f75e-4a95-9481-69c4f3e81c80.png", "exec-866cdad2-6f7c-47c9-8bcd-a8ee8b8e6002.png"),
    209: ("exec-1698d690-31ab-4882-b1ce-f521cac14640.png", "exec-21801f7c-99d3-4ea5-b758-1b4136a80c84.png"),
    258: ("exec-ffca77e6-61a8-4fe0-8ec4-0087c4ac84e4.png", "exec-6bf3c381-3eaa-43ca-839a-f1c7df3891f4.png"),
    57: ("exec-40e65890-a4f0-456d-bffe-0620f6d95977.png", "exec-96a94431-9937-417d-8c06-a32dba915de7.png"),
    245: ("exec-3158ab10-8080-43d4-9cf1-7aa9d68b1772.png", "exec-6da101a6-7282-48d8-a567-4ed46006c7e7.png"),
}


if __name__ == "__main__":
    base.main()
    for old, new in (
        ("wave-3-covers-contact-sheet.jpg", "wave-7-covers-contact-sheet.jpg"),
        ("wave-3-chapter-art-master-contact-sheet.jpg", "wave-7-chapter-art-master-contact-sheet.jpg"),
    ):
        (base.TMP / old).replace(base.TMP / new)
