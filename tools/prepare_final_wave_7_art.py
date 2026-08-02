#!/usr/bin/env python3
"""Prepare the nine covers and 144 chapter images for final wave seven."""

from prepare_final_wave_art import ROOT, prepare


SOURCES = {
    273: ("exec-e744ac41-9f51-48ef-9f07-11d7bdaa9fd4.png", "exec-383ba38e-141a-467a-bbbf-d1c8a05c3804.png"),
    274: ("exec-37a0248d-8299-4488-89fd-26107e53361e.png", "exec-984715ec-a4c8-414b-8137-13199c77861b.png"),
    276: ("exec-421bd554-8b55-48a4-812e-f18a06c6eaf3.png", "exec-ac91a99d-aa72-47fa-a836-9b9f9852de25.png"),
    278: ("exec-ed711817-717b-4e1d-a99f-a8277f6e0eea.png", "exec-ce66f25f-bd0a-4aab-965e-3a5114397e5c.png"),
    279: ("exec-0b579477-1493-4224-9ed2-ebc602ce7cf3.png", "exec-8d17522c-997e-42fc-8a3d-ab613bee08a5.png"),
    280: ("exec-ac901785-6b6b-4165-9e1a-bfb68a187e2b.png", "exec-fa3fd8dd-4508-420f-97b2-1f616ff1e372.png"),
    281: ("exec-5efb6fb2-ce11-491b-b58f-b0dfa515a121.png", "exec-a718df2e-be5b-46d7-9caf-3098222e8f87.png"),
    282: ("exec-bcf48d46-29fc-43c1-a000-55809deacd79.png", "exec-979f557b-d2fb-4a1b-a8f5-e15679710cff.png"),
    283: ("exec-e47d0994-2a8a-4f39-ac06-d0d0c1cda67a.png", "exec-b3cb8093-1ea7-4517-9c5e-bc91373176e9.png"),
}


if __name__ == "__main__":
    prepare(SOURCES, ROOT / "tmp" / "final-wave-7-art", "final-wave-7")
