#!/usr/bin/env python3
"""Prepare the nine covers and 144 chapter images for final wave eight."""

from prepare_final_wave_art import ROOT, prepare


SOURCES = {
    289: ("exec-fd5789a6-7be6-4b5d-a39b-28229b43fd06.png", "exec-ec310973-ea82-4bde-903a-715a8300cfb8.png"),
    291: ("exec-8b4dcbe6-f62e-4939-a41b-893ed236919a.png", "exec-ccdb92c2-1979-4a75-bb42-69fe936de3ff.png"),
    292: ("exec-8f3f8a8a-3293-4322-bee3-7a5b3dde1aba.png", "exec-ee17cfaf-1a70-4e94-9435-6d5257b0b731.png"),
    295: ("exec-f585db88-c77c-4f03-a704-dc732e1f3f61.png", "exec-504ca3f4-6bd9-4e20-8a50-d833b2bafd24.png"),
    296: ("exec-19a0e55a-f948-44a8-8f42-25a97dfd6e2e.png", "exec-60128044-79cb-416c-85a2-db28bdc1d061.png"),
    297: ("exec-59eec7d5-2b93-405f-928d-6ceebec9900a.png", "exec-a1769c84-0378-4aeb-b07e-5f2a70f18e94.png"),
    298: ("exec-0ccf8993-7110-4ece-b0af-81bc7e37f3eb.png", "exec-9d4b9d71-be52-4e47-b429-779d219d8627.png"),
    299: ("exec-f56ac7df-5257-482a-9c35-b198384ed032.png", "exec-a767018e-2c5e-43d2-8384-3a8d62723a38.png"),
    300: ("exec-6b3efc48-7a37-468e-ba18-7bcd28f88371.png", "exec-e349c87a-9068-4cb8-8df1-99c7993c6a90.png"),
}


if __name__ == "__main__":
    prepare(SOURCES, ROOT / "tmp" / "final-wave-8-art", "final-wave-8")
