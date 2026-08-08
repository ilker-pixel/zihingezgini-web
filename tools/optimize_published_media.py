#!/usr/bin/env python3
"""Archive summary cover masters and optimize published, non-personal media.

The script deliberately limits itself to the 300 AI summary JSON files, the 21
research archive covers, and an explicit set of unreferenced AI summary assets.
Personal posts, philosopher pages, and audio are outside its write surface.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
import os
import tempfile
import zipfile
from pathlib import Path

from PIL import Image, ImageChops


ROOT = Path(__file__).resolve().parents[1]
SUMMARY_DIR = ROOT / "data" / "summaries"
OPTIMIZED_DIR = ROOT / "images" / "optimized"

ORPHAN_AI_ASSETS = (
    "images/summary-11-ucuncu-sempanze-cover.png",
    "images/summary-13-buyuk-tarih-cover.png",
    "images/summary-90-sisifos-soyleni-cover.png",
    "images/summary-130-yargi-gucunun-elestirisi-cover.png",
    "images/summary-179-risk-toplumu-cover.png",
    "images/summary-224-oryantalizm-cover.png",
    "images/summary-277-karisini-sapka-sanan-adam-cover.png",
    "images/summary-art-12-tufek-mikrop-ve-celik-v1.webp",
    "images/summary-art-17-evrenin-yapisi-v1.webp",
    "images/summary-art-32-behave-davranis-v1.webp",
    "images/summary-art-41-beyindeki-hayaletler-v1.webp",
    "images/summary-art-66-devlet-v1.webp",
    "images/summary-art-72-savas-sanati-v1.webp",
    "images/summary-art-93-leviathan-v1.webp",
    "images/summary-art-103-protestan-ahlaki-ve-kapitalizmin-ruhu-v1.webp",
    "images/summary-art-122-etika-v1.webp",
    "images/summary-art-124-dusunceler-pascal-v1.webp",
    "images/summary-art-152-uluslarin-dususu-v1.webp",
    "images/summary-art-156-buyuk-donusum-v1.webp",
    "images/summary-art-189-mitolojiler-v1.webp",
    "images/summary-art-194-arac-mesajdir-v1.webp",
    "images/summary-art-214-teknik-yeniden-uretim-caginda-sanat-eseri-v1.webp",
    "images/summary-art-222-feminizm-herkes-icindir-v1.webp",
    "images/summary-art-241-akiskan-modernite-v1.webp",
    "images/summary-art-253-superzeka-v1.webp",
    "images/summary-art-271-dini-deneyimin-cesitleri-v1.webp",
    "images/summary-art-275-buyuk-resim-v1.webp",
)

TEXT_UPDATE_ROOTS = (
    ROOT / "data" / "summaries",
    ROOT / "tools",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def cover_pairs() -> list[tuple[int, Path, Path]]:
    pairs = []
    for number in range(1, 301):
        summary = json.loads((SUMMARY_DIR / f"{number}.json").read_text(encoding="utf-8"))
        raw = str(summary.get("coverImage", ""))
        if not raw.startswith("/images/"):
            raise RuntimeError(f"#{number}: unexpected cover path {raw!r}")
        source = ROOT / raw.lstrip("/")
        relative = source.relative_to(ROOT / "images")
        optimized = OPTIMIZED_DIR / relative.parent / f"{relative.stem}-960.webp"
        if not source.is_file() or not optimized.is_file():
            raise RuntimeError(f"#{number}: missing source/optimized pair: {source}, {optimized}")
        pairs.append((number, source, optimized))
    if len({source for _, source, _ in pairs}) != 300:
        raise RuntimeError("Summary cover sources must be 300 unique files")
    if len({optimized for _, _, optimized in pairs}) != 300:
        raise RuntimeError("Optimized summary covers must be 300 unique files")
    return pairs


def build_archive(output: Path) -> None:
    pairs = cover_pairs()
    lines = ["book_no\tsource\toptimized\tsource_bytes\tsource_sha256\toptimized_sha256"]
    for number, source, optimized in pairs:
        lines.append(
            "\t".join((
                str(number),
                source.relative_to(ROOT).as_posix(),
                optimized.relative_to(ROOT).as_posix(),
                str(source.stat().st_size),
                sha256(source),
                sha256(optimized),
            ))
        )
    manifest = "\n".join(lines) + "\n"
    readme = (
        "Zihin Gezgini · 300 AI ön okuma rehberi kapak ustaları\n\n"
        "Bu ZIP yalnız yüksek çözünürlüklü kaynak kapakları içerir. Canlı sitede "
        "images/optimized altındaki doğrulanmış ekran kopyaları kullanılmaya devam eder.\n"
        "MANIFEST.tsv her kaynak ve ekran kopyasının SHA-256 değerini içerir.\n"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED, allowZip64=True) as archive:
        archive.writestr("README.txt", readme)
        archive.writestr("MANIFEST.tsv", manifest)
        for _, source, _ in pairs:
            archive.write(source, source.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(output) as archive:
        bad = archive.testzip()
        if bad:
            raise RuntimeError(f"Archive CRC failed: {bad}")
        archived_sources = [name for name in archive.namelist() if name.startswith("images/")]
        if len(archived_sources) != 300:
            raise RuntimeError(f"Archive contains {len(archived_sources)} sources, expected 300")
    print(f"archive={output}")
    print(f"archive_bytes={output.stat().st_size}")
    print(f"archive_sha256={sha256(output)}")
    print(f"source_bytes={sum(source.stat().st_size for _, source, _ in pairs)}")


def replace_text(path: Path, replacements: dict[str, str]) -> int:
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return 0
    updated = text
    for source, target in replacements.items():
        updated = updated.replace(source, target)
    if updated == text:
        return 0
    path.write_text(updated, encoding="utf-8")
    return 1


def update_summary_cover_references(pairs: list[tuple[int, Path, Path]]) -> int:
    replacements: dict[str, str] = {}
    for _, source, optimized in pairs:
        source_rel = source.relative_to(ROOT).as_posix()
        optimized_rel = optimized.relative_to(ROOT).as_posix()
        replacements[f"/{source_rel}"] = f"/{optimized_rel}"
        replacements[source_rel] = optimized_rel
    changed = 0
    for root in TEXT_UPDATE_ROOTS:
        for path in root.rglob("*"):
            if path.is_file() and path.suffix.lower() in {".json", ".py", ".js"}:
                changed += replace_text(path, replacements)
    changed += replace_text(ROOT / "app.js", replacements)
    return changed


def convert_research_covers() -> tuple[list[Path], int, int]:
    index_path = ROOT / "data" / "kutuphane_index.json"
    items = json.loads(index_path.read_text(encoding="utf-8"))
    replacements = {}
    before = 0
    after = 0
    for item in items:
        source_rel = item["cover"]
        source = ROOT / source_rel
        target = source.with_suffix(".webp")
        if not source.is_file():
            raise RuntimeError(f"Missing research cover: {source}")
        before += source.stat().st_size
        with Image.open(source) as original:
            image = original.convert("RGB")
            image.thumbnail((720, 720), Image.Resampling.LANCZOS)
            image.save(target, "WEBP", quality=80, method=6)
        after += target.stat().st_size
        replacements[source_rel] = target.relative_to(ROOT).as_posix()
        item["cover"] = replacements[source_rel]
    index_path.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # The legacy reader constructs cover paths dynamically; keep it aligned.
    replace_text(ROOT / "app.js", {"'covers/' + currentBookData.id + '.png'": "'covers/' + currentBookData.id + '.webp'"})
    replace_text(ROOT / "tools" / "build_static.py", {"f\"/covers/{book['id']}.png\"": "f\"/covers/{book['id']}.webp\""})
    return [ROOT / source for source in replacements], before, after


def verify_orphans() -> None:
    tracked_text = []
    for path in ROOT.rglob("*"):
        if (
            not path.is_file()
            or path.resolve() == Path(__file__).resolve()
            or ".git" in path.parts
            or path.suffix.lower() not in {".html", ".json", ".js", ".css", ".py"}
        ):
            continue
        try:
            tracked_text.append(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, OSError):
            pass
    joined = "\n".join(tracked_text)
    for relative in ORPHAN_AI_ASSETS:
        if relative in joined or f"/{relative}" in joined:
            raise RuntimeError(f"Refusing to remove referenced AI asset: {relative}")


def apply_optimizations() -> None:
    pairs = cover_pairs()
    changed = update_summary_cover_references(pairs)
    research_sources, research_before, research_after = convert_research_covers()
    verify_orphans()
    removed_bytes = 0
    for _, source, _ in pairs:
        removed_bytes += source.stat().st_size
        source.unlink()
    for relative in ORPHAN_AI_ASSETS:
        path = ROOT / relative
        if not path.is_file():
            raise RuntimeError(f"Expected orphan is missing: {path}")
        removed_bytes += path.stat().st_size
        path.unlink()
    for source in research_sources:
        source.unlink()
    print(f"updated_text_files={changed}")
    print(f"removed_source_and_orphan_bytes={removed_bytes}")
    print(f"research_covers={len(research_sources)}")
    print(f"research_before_bytes={research_before}")
    print(f"research_after_bytes={research_after}")


def chapter_art_paths() -> list[Path]:
    paths: set[Path] = set()
    for number in range(1, 301):
        summary = json.loads((SUMMARY_DIR / f"{number}.json").read_text(encoding="utf-8"))
        artworks = summary.get("chapterArtworks", {})
        for chapter in summary.get("chapters", []):
            artwork = artworks.get(chapter.get("id", ""), {})
            raw = chapter.get("image") or artwork.get("image")
            if not raw or not str(raw).startswith("/images/"):
                continue
            path = ROOT / str(raw).lstrip("/")
            if OPTIMIZED_DIR in path.parents:
                continue
            if path.suffix.lower() != ".webp" or not path.is_file():
                continue
            with Image.open(path) as image:
                if image.size == (720, 720):
                    paths.add(path)
    return sorted(paths)


def psnr(original: Image.Image, encoded: Image.Image) -> float:
    difference = ImageChops.difference(original, encoded)
    histogram = difference.histogram()
    squared = sum((index % 256) ** 2 * count for index, count in enumerate(histogram))
    channels = len(original.getbands())
    mse = squared / (original.width * original.height * channels)
    return float("inf") if mse == 0 else 20 * math.log10(255 / math.sqrt(mse))


def optimize_chapter_art() -> None:
    paths = chapter_art_paths()
    if len(paths) < 4700:
        raise RuntimeError(f"Expected at least 4700 active AI chapter artworks, found {len(paths)}")
    before = 0
    after = 0
    scores = []
    skipped = 0
    for index, path in enumerate(paths, 1):
        original_bytes = path.read_bytes()
        before += len(original_bytes)
        with Image.open(io.BytesIO(original_bytes)) as source:
            original = source.convert("RGB")
        output = io.BytesIO()
        original.save(output, "WEBP", quality=76, method=6)
        encoded_bytes = output.getvalue()
        with Image.open(io.BytesIO(encoded_bytes)) as candidate:
            encoded = candidate.convert("RGB")
        score = psnr(original, encoded)
        if score < 34.0 or len(encoded_bytes) >= len(original_bytes):
            after += len(original_bytes)
            skipped += 1
            continue
        descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
        try:
            with os.fdopen(descriptor, "wb") as handle:
                handle.write(encoded_bytes)
            os.replace(temporary_name, path)
        finally:
            if os.path.exists(temporary_name):
                os.unlink(temporary_name)
        after += len(encoded_bytes)
        scores.append(score)
        if index % 250 == 0:
            print(f"chapter_art_progress={index}/{len(paths)}", flush=True)
    print(f"chapter_art_files={len(paths)}")
    print(f"chapter_art_skipped={skipped}")
    print(f"chapter_art_before_bytes={before}")
    print(f"chapter_art_after_bytes={after}")
    print(f"chapter_art_saved_bytes={before - after}")
    print(f"chapter_art_min_psnr={min(scores):.2f}")
    print(f"chapter_art_avg_psnr={sum(scores) / len(scores):.2f}")


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--archive", type=Path, help="write a verified ZIP of 300 source covers")
    group.add_argument("--apply", action="store_true", help="apply the verified, scoped media optimization")
    group.add_argument("--chapter-art", action="store_true", help="re-encode active 720 px AI chapter art")
    args = parser.parse_args()
    if args.archive:
        build_archive(args.archive.resolve())
    elif args.chapter_art:
        optimize_chapter_art()
    else:
        apply_optimizations()


if __name__ == "__main__":
    main()
