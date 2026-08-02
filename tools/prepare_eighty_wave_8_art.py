#!/usr/bin/env python3
"""Prepare covers and 16 chapter images for the eighth 80-book wave."""

from pathlib import Path

import prepare_eighty_wave_3_art as base


ROOT = Path(__file__).resolve().parents[1]
base.TMP = ROOT / "tmp" / "eighty-wave-8"
base.SOURCES = {
    56: ("exec-e2b56c99-2c68-46ef-96f7-24a329bc37ca.png", "exec-8bd157fd-dbc3-4365-bf0d-2c5884d31f4b.png"),
    54: ("exec-0ecc97e4-6829-4029-8cf6-0148e829cb87.png", "exec-c1032d0e-4405-42d3-9de7-a6b41beb154c.png"),
    125: ("exec-2df8808a-d2a3-43f2-af11-05b486d05f7d.png", "exec-a3095612-1909-4011-ab27-d74ecc0d6015.png"),
    116: ("exec-72cedd4c-7fa9-4a7b-8025-03c042d3ed47.png", "exec-63496258-7524-480e-a79c-2184003112f0.png"),
    188: ("exec-46b050b9-563c-4c43-a4ed-380a7aa0c76f.png", "exec-42e9c670-0786-480d-a64d-b6fb62a157a0.png"),
    168: ("exec-7c618445-e59f-4ece-a3fb-dbb32071a8e4.png", "exec-9e23e3b9-7592-4db3-87a6-2c16d51b5998.png"),
    210: ("exec-6c3bfde6-2bb9-44b4-8571-4f71796fc389.png", "exec-53c389bf-d3b7-4b8f-bffb-801586e115cb.png"),
    259: ("exec-294225bf-723c-46ae-99a9-6e0168b75f79.png", "exec-a9b208ea-1858-4f3f-a542-acffe4ba2011.png"),
    129: ("exec-d5551cf6-77a9-47e6-8aaf-2ee2121fc026.png", "exec-7ae14cd3-8071-4202-bdda-b85bfe849b53.png"),
    150: ("exec-4669d42e-affd-4586-8fe8-978dee34253d.png", "exec-180daa68-7986-4101-83b4-e889b0c45d69.png"),
}


if __name__ == "__main__":
    base.main()
    for old, new in (
        ("wave-3-covers-contact-sheet.jpg", "wave-8-covers-contact-sheet.jpg"),
        ("wave-3-chapter-art-master-contact-sheet.jpg", "wave-8-chapter-art-master-contact-sheet.jpg"),
    ):
        (base.TMP / old).replace(base.TMP / new)
