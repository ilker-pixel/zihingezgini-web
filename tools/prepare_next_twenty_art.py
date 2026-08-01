#!/usr/bin/env python3
"""Prepare independent covers and 16 chapter images for the next twenty books."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps

import prepare_twenty_summary_art as base


ROOT = Path(__file__).resolve().parents[1]
GENERATED = Path("/Users/ilker/.codex/generated_images/019f9da1-066e-7b33-a57d-6f3ce25d234e")
IMAGES = ROOT / "images"
TMP = ROOT / "tmp" / "next-twenty-summaries"

SOURCES = {
    9: ("exec-c6b0b2c3-e55d-41cb-9052-156c68a8291b.png", "exec-f6a0af3d-1978-48bc-9b34-366fe9db5ed9.png"),
    33: ("exec-6cac03ea-f62c-422a-94cc-1546d0bb7b02.png", "exec-fae63d74-381e-4769-a4cb-1775a72c58ce.png"),
    37: ("exec-45268b37-de02-48b3-9f8e-3d07e280165e.png", "exec-c18555a5-d2d9-4c76-8f54-c953dd2f3376.png"),
    50: ("exec-dd4b180f-ddb6-4953-b10a-c982d77fb37b.png", "exec-7888e2fb-945a-4b87-8222-1f24547c1777.png"),
    62: ("exec-20378229-7d45-4c42-9bd5-82ca5c49506a.png", "exec-ddcd604a-cd5d-4c45-8e8b-3d77d633d399.png"),
    63: ("exec-aae09498-3afa-4a15-93e2-cf56ff8b40b9.png", "exec-868f3828-bf3d-4af0-9687-f61791029b30.png"),
    68: ("exec-45849dae-36e8-4664-9741-1294ecc8e376.png", "exec-dbdd9b05-259a-40f8-a098-9f42567f7390.png"),
    75: ("exec-22885732-d329-4df1-bb45-2bdfe4dd61f5.png", "exec-f5c9e055-eaf9-40e7-bbc0-ee7b741a3bae.png"),
    79: ("exec-def16d9f-eee1-46a6-b90a-2bd82af4e85d.png", "exec-a760229d-e25b-47d6-926c-ec3126e31d68.png"),
    87: ("exec-29984e05-d3b7-44df-a5f8-a22af1f980fb.png", "exec-ba0c7cc9-2667-4d94-bbeb-be6df2dd4b1b.png"),
    89: ("exec-ec2313f2-219c-4796-a5e5-340e03d5c748.png", "exec-92656210-4757-4c27-93f0-cd57273fccde.png"),
    100: ("exec-7218ac39-acb9-4d00-b64d-a547be097472.png", "exec-1cdb514b-b801-4fb4-87c0-8e16fc9b356b.png"),
    107: ("exec-325c33a3-0f0d-49fb-9fa9-cf7767748377.png", "exec-4fd1c2e2-088c-4d30-8434-7530fc319f81.png"),
    111: ("exec-19801303-df93-4328-bf8f-69b1ba6b0f40.png", "exec-ef67c4c5-873f-402e-a26b-458ba96f172f.png"),
    145: ("exec-b2bab4a6-f5d0-4b52-a4d1-7b862e4aabb0.png", "exec-45d9fc93-e2b5-4342-a5b2-a4afc769a25b.png"),
    158: ("exec-e081ba92-3b17-4503-9525-4b6a5e64d2e4.png", "exec-dc0d7906-c295-41d3-8684-2c64c93c8377.png"),
    172: ("exec-ecbe8083-2f70-4317-9796-4f4cafcaec05.png", "exec-fc0a0334-9282-4727-ba02-186b7a2b4e9a.png"),
    183: ("exec-4f76f8ff-f3c4-4ad1-ada9-c4e36b4d5b44.png", "exec-eaeb117c-aaea-4b9a-9ae2-d18891ec81cd.png"),
    199: ("exec-5e9cbf67-02cc-4230-9ed9-b6018f540b2e.png", "exec-8dcdeef9-f0fb-4179-9c42-aad8422a51b2.png"),
    239: ("exec-a5f5f636-592c-40a1-b48c-425c76751f8f.png", "exec-28a338ed-1466-440c-9810-478501cac103.png"),
}


def main() -> None:
    IMAGES.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    base.TMP = TMP
    cover_thumbs: list[Image.Image] = []

    for book_no, (sheet_name, cover_name) in SOURCES.items():
        summary = json.loads((ROOT / "data" / "summaries" / f"{book_no}.json").read_text(encoding="utf-8"))
        sheet_path = GENERATED / sheet_name
        cover_path = GENERATED / cover_name
        if not sheet_path.exists() or not cover_path.exists():
            raise FileNotFoundError(f"Missing source art for book {book_no}")

        artwork_paths = [ROOT / item["image"].lstrip("/") for item in summary["chapterArtworks"].values()]
        if len(artwork_paths) != 16:
            raise ValueError(f"Book {book_no} must have exactly 16 artwork paths")

        with Image.open(sheet_path) as sheet:
            cells = base.crop_cells(sheet.convert("RGB"))
        for cell, output in zip(cells, artwork_paths, strict=True):
            output.parent.mkdir(parents=True, exist_ok=True)
            base.monochrome(cell, summary["chapterArtColor"]).save(output, "WEBP", quality=84, method=6)

        cover_output = ROOT / summary["coverImage"].lstrip("/")
        with Image.open(cover_path) as source:
            cover = ImageOps.fit(source.convert("RGB"), (900, 1350), method=Image.Resampling.LANCZOS)
            cover = ImageEnhance.Contrast(cover).enhance(1.03)
            cover.save(cover_output, "WEBP", quality=88, method=6)
            cover_thumbs.append(ImageOps.contain(cover, (162, 243)).copy())

        base.make_art_contact_sheet(book_no, artwork_paths)
        print(f"{book_no}: 16 chapter images + cover")

    cover_canvas = Image.new("RGB", (880, 1032), "#D9D3C6")
    for index, thumb in enumerate(cover_thumbs):
        x = 8 + (index % 5) * 174 + (162 - thumb.width) // 2
        y = 8 + (index // 5) * 256 + (243 - thumb.height) // 2
        cover_canvas.paste(thumb, (x, y))
    cover_canvas.save(TMP / "next-twenty-covers-contact-sheet.jpg", quality=92)


if __name__ == "__main__":
    main()
