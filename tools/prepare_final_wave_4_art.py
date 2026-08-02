#!/usr/bin/env python3
"""Prepare the nine covers and 144 chapter images for final wave four."""

from prepare_final_wave_art import ROOT, prepare


SOURCES = {
    219: ("exec-cf141d7b-079d-4a56-87e9-a76d3f7ef7b3.png", "exec-d0258b0c-299e-44d9-994f-1675c2c62852.png"),
    226: ("exec-35fbd63d-9404-413b-bdfc-769c9078a56a.png", "exec-910dfb31-2ad8-4776-a988-f47176fdc5a9.png"),
    227: ("exec-2f28d9ca-f550-49c0-ab03-a68e4db50607.png", "exec-aab74e78-b9ee-476f-a698-333381fa49ab.png"),
    228: ("exec-36619c5f-eebb-4692-9897-ec20f056914a.png", "exec-f499c5d9-39c6-4d23-8dd9-6fe6531d770c.png"),
    230: ("exec-c30255f3-bbe9-4654-9711-c5fb716b7364.png", "exec-84f265a0-c790-406a-8f09-4c7b2ae4e691.png"),
    231: ("exec-41290b07-8a78-422c-9481-3c1f5f7e1815.png", "exec-7de38ae6-be4c-4dae-a674-5d02f023ce6e.png"),
    232: ("exec-625e60a2-058d-44b3-95fb-7d8a2f19347a.png", "exec-1771a5c9-b962-4422-970d-395952c954a8.png"),
    233: ("exec-6683b039-9f02-45d7-a357-9fc225fb0363.png", "exec-45d9ddb4-9b0a-4f34-a2ec-47e1b3378f34.png"),
    234: ("exec-dda40f6c-bba8-4d69-90cf-df5e96dfa208.png", "exec-7ea2fb88-5349-47e8-a320-6c2294495503.png"),
}


if __name__ == "__main__":
    prepare(SOURCES, ROOT / "tmp" / "final-wave-4-art", "final-wave-4")
