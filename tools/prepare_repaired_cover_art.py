#!/usr/bin/env python3
"""Install the twenty independent full-color covers for the repaired batch."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
GENERATED = Path("/Users/ilker/.codex/generated_images/019f9da1-066e-7b33-a57d-6f3ce25d234e")
SOURCE_FILES = {
    12: "exec-3e20749e-2743-470e-bc2b-3aea7ff8bde5.png",
    17: "exec-f3fb5174-ba16-492e-8343-80aa4b2adf6d.png",
    32: "exec-54565791-1846-439b-bd99-c13a3460ef6e.png",
    41: "exec-444784b1-0f65-4a2c-9537-7c58edbcdcd4.png",
    66: "exec-fb44ef1e-8f12-4af2-9e62-784a4feb0261.png",
    72: "exec-af0c4a5b-315f-4a2d-8b81-1b237b88b8e5.png",
    93: "exec-42f45f52-890f-4e08-8316-14f97d1fc749.png",
    103: "exec-0a7d2125-a6e5-4b4e-b852-1b477449abd6.png",
    122: "exec-00dfd49c-9e48-4763-a538-693f0e5d23d5.png",
    124: "exec-825c82b2-bcbe-4cdd-996d-ba282a52f761.png",
    152: "exec-3ae0ec08-d2b9-470c-accb-cd578cc40c96.png",
    156: "exec-1a3c4926-f9dd-417f-bd71-3cde2d236cca.png",
    189: "exec-6be43e0c-da93-43d7-87f3-817a780b68b1.png",
    194: "exec-877be2c8-7bca-4e0b-8e00-64b15532f765.png",
    214: "exec-23d7562f-350c-4aaa-ba98-71ed4d1c459c.png",
    222: "exec-a5fc4d14-44ae-4776-81ba-fa8f0a295045.png",
    241: "exec-144ce491-43d1-494d-8e67-ef5005793973.png",
    253: "exec-e0fa093a-4799-4ecb-b19b-ac6f82394257.png",
    271: "exec-5850ff49-51e6-458a-bf29-8218632de435.png",
    275: "exec-ae223fd2-2755-4b86-aaf3-08eb13db3d45.png",
}


def main() -> None:
    for number, source_name in SOURCE_FILES.items():
        summary_path = ROOT / "data" / "summaries" / f"{number}.json"
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        old_name = Path(summary["coverImage"]).name
        stem = old_name.removeprefix("summary-art-").removesuffix("-v1.webp")
        target_name = f"summary-cover-{stem}-v2.webp"
        target = ROOT / "images" / target_name
        source = GENERATED / source_name
        if not source.exists():
            raise FileNotFoundError(source)
        with Image.open(source) as opened:
            image = ImageOps.fit(opened.convert("RGB"), (900, 1350), method=Image.Resampling.LANCZOS)
            image.save(target, "WEBP", quality=91, method=6)
        summary["coverImage"] = f"/images/{target_name}"
        summary["coverStyle"] = "artwork"
        summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{number:3} {target.relative_to(ROOT)} {target.stat().st_size / 1024:.0f} KiB")


if __name__ == "__main__":
    main()
