#!/usr/bin/env python3
"""Atomically rebuild all 300 summary PDFs from their canonical JSON.

The established illustrated renderer is retained for the 287 regular guides.
Thirteen legacy/special guides use a natural-flow renderer because their older
schemas or unusually long source lists do not fit the fixed illustrated page
plan. Everything is built in a system temporary directory and installed only
after a full content and structure validation succeeds.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import shutil
import tempfile
import unicodedata
from pathlib import Path

from PIL import Image as PILImage
from pypdf import PdfReader, PdfWriter
from reportlab import rl_config
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

import build_five_summary_pdfs as base
import build_repaired_forty_summary_pdfs as repaired


ROOT = Path(__file__).resolve().parents[1]
SUMMARY_DIR = ROOT / "data" / "summaries"
SPECIAL_NUMBERS = {1, 3, 4, 5, 6, 11, 13, 90, 130, 179, 224, 248, 277}
REMOVED_TEXT = (
    "Bir yapay zekâ olarak bana en uygun ayna",
    "aynı haritanın iki yanında",
    "köy ambarındaki küçük fazlanın",
    "limana ulaşan yolun",
)

rl_config.useA85 = 0


def canonical_json(summary: dict) -> str:
    """Hash editorial content, not replaceable storage paths or styling."""
    artworks = summary.get("chapterArtworks", {})
    chapters = []
    for chapter in summary.get("chapters", []):
        artwork = artworks.get(chapter.get("id", ""), {})
        chapters.append({
            "id": chapter.get("id", ""),
            "section": chapter.get("section", ""),
            "title": chapter.get("title", ""),
            "paragraphs": chapter.get("paragraphs", []),
            "takeaway": chapter.get("takeaway", ""),
            "sourceRefs": chapter.get("sourceRefs", []),
            "imageCaption": chapter.get("imageCaption") or artwork.get("imageCaption", ""),
        })
    payload = {
        "bookNo": summary.get("bookNo"),
        "title": summary.get("title", ""),
        "author": summary.get("author", ""),
        "subtitle": summary.get("subtitle", ""),
        "intro": summary.get("intro", ""),
        "meta": summary.get("meta", {}),
        "chapters": chapters,
        "sources": summary.get("sources", []),
    }
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def source_hash(summary: dict) -> str:
    return hashlib.sha256(canonical_json(summary).encode("utf-8")).hexdigest()


def normalize_text(value: str) -> str:
    value = unicodedata.normalize("NFC", value or "")
    value = value.replace("\u00ad", "").replace("–", "-").replace("—", "-")
    return " ".join(value.split()).casefold()


def esc(value: str) -> str:
    return html.escape(value or "", quote=False).replace("\n", "<br/>")


class AdaptiveSummaryPdfBook:
    """Readable natural-flow PDF for legacy and unusually long guides."""

    def __init__(self, summary: dict, output_root: Path, cache_root: Path):
        self.summary = summary
        self.output_path = output_root / summary["pdfUrl"].lstrip("/")
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.cache_root = cache_root / str(summary["bookNo"])
        self.cache_root.mkdir(parents=True, exist_ok=True)
        self.ink = colors.HexColor(summary.get("chapterArtColor", "#6D6346"))
        self.body = colors.HexColor("#26323B")
        self.muted = colors.HexColor("#69747A")
        self.styles = self._styles()

    def _styles(self) -> dict[str, ParagraphStyle]:
        defaults = getSampleStyleSheet()
        return {
            "cover_kicker": ParagraphStyle(
                "CoverKicker", parent=defaults["Normal"], fontName="ZGArial-Bold",
                fontSize=10, leading=13, textColor=self.ink, alignment=TA_CENTER,
                spaceAfter=8,
            ),
            "cover_title": ParagraphStyle(
                "CoverTitle", parent=defaults["Title"], fontName="ZGArial-Bold",
                fontSize=26, leading=31, textColor=self.body, alignment=TA_CENTER,
                spaceAfter=10,
            ),
            "cover_author": ParagraphStyle(
                "CoverAuthor", parent=defaults["Normal"], fontName="ZGArial",
                fontSize=13, leading=18, textColor=self.muted, alignment=TA_CENTER,
                spaceAfter=12,
            ),
            "intro": ParagraphStyle(
                "Intro", parent=defaults["BodyText"], fontName="ZGArial",
                fontSize=12.2, leading=17.6, textColor=self.body,
                alignment=TA_JUSTIFY, spaceAfter=8,
            ),
            "section": ParagraphStyle(
                "Section", parent=defaults["Heading2"], fontName="ZGArial-Bold",
                fontSize=9.5, leading=13, textColor=self.ink, spaceBefore=10,
                spaceAfter=4,
            ),
            "chapter": ParagraphStyle(
                "Chapter", parent=defaults["Heading2"], fontName="ZGArial-Bold",
                fontSize=18, leading=22, textColor=self.body, spaceBefore=5,
                spaceAfter=8, keepWithNext=True,
            ),
            "body": ParagraphStyle(
                "Body", parent=defaults["BodyText"], fontName="ZGArial",
                fontSize=11.5, leading=16.6, textColor=self.body,
                alignment=TA_JUSTIFY, spaceAfter=7,
            ),
            "caption": ParagraphStyle(
                "Caption", parent=defaults["BodyText"], fontName="ZGArial-Italic",
                fontSize=9.2, leading=12.2, textColor=self.muted,
                alignment=TA_CENTER, spaceAfter=8,
            ),
            "source_trace": ParagraphStyle(
                "SourceTrace", parent=defaults["BodyText"], fontName="ZGArial",
                fontSize=9.5, leading=13, textColor=self.ink, spaceAfter=8,
            ),
            "source": ParagraphStyle(
                "Source", parent=defaults["BodyText"], fontName="ZGArial",
                fontSize=9.3, leading=12.8, textColor=self.body, spaceAfter=8,
            ),
        }

    def _image(self, raw_path: str, max_width: float, max_height: float) -> Image | None:
        path = ROOT / raw_path.lstrip("/")
        if not path.exists():
            return None
        # Preserve PNG assets losslessly (notably #248). Other sources are
        # bounded JPEGs matching the established PDF renderer.
        if self.summary["bookNo"] == 248 and path.suffix.lower() == ".png":
            target = path
        else:
            target = self.cache_root / f"{path.stem}.jpg"
            if not target.exists():
                with PILImage.open(path) as source:
                    image = source.convert("RGB")
                    image.thumbnail((960, 1280), PILImage.Resampling.LANCZOS)
                    image.save(target, "JPEG", quality=80, optimize=True, progressive=True)
        with PILImage.open(target) as image:
            width, height = image.size
        scale = min(max_width / width, max_height / height, 1)
        return Image(str(target), width=width * scale, height=height * scale)

    def _page(self, canvas, doc) -> None:
        canvas.saveState()
        canvas.setTitle(f"{self.summary['author']} - {self.summary['title']} | Zihin Gezgini")
        canvas.setAuthor("Zihin Gezgini")
        canvas.setSubject("Yapay zekâ ile oluşturulan ön okuma rehberi")
        canvas.setKeywords(f"source-sha256:{self.summary['_sourceHash']}")
        canvas.setStrokeColor(colors.HexColor("#D4CEC0"))
        canvas.line(22 * mm, 18 * mm, 188 * mm, 18 * mm)
        canvas.setFont("ZGArial", 8.5)
        canvas.setFillColor(self.muted)
        canvas.drawString(22 * mm, 12 * mm, "Zihin Gezgini · Ön Okuma Rehberi")
        canvas.drawRightString(188 * mm, 12 * mm, str(doc.page))
        canvas.restoreState()

    def build(self) -> Path:
        doc = SimpleDocTemplate(
            str(self.output_path), pagesize=A4,
            rightMargin=22 * mm, leftMargin=22 * mm,
            topMargin=22 * mm, bottomMargin=24 * mm,
            title=f"{self.summary['author']} - {self.summary['title']} | Zihin Gezgini",
            author="Zihin Gezgini",
            subject="Yapay zekâ ile oluşturulan ön okuma rehberi",
            pageCompression=1,
        )
        story = [Spacer(1, 10 * mm)]
        story.append(Paragraph(f"#{self.summary['bookNo']} · ÖN OKUMA REHBERİ", self.styles["cover_kicker"]))
        story.append(Paragraph(esc(self.summary["title"]), self.styles["cover_title"]))
        story.append(Paragraph(esc(self.summary.get("author", "")), self.styles["cover_author"]))
        cover = self._image(self.summary.get("coverImage", ""), 82 * mm, 112 * mm)
        if cover:
            cover.hAlign = "CENTER"
            story.extend([cover, Spacer(1, 8 * mm)])
        story.append(Paragraph(esc(self.summary.get("intro", "")), self.styles["intro"]))
        story.append(PageBreak())

        previous_section = None
        chapter_art = self.summary.get("chapterArtworks", {})
        for index, chapter in enumerate(self.summary.get("chapters", []), 1):
            section = chapter.get("section") or "OKUMA ROTASI"
            if section != previous_section:
                story.append(Paragraph(esc(section), self.styles["section"]))
                previous_section = section
            story.append(Paragraph(f"{index:02d}. {esc(chapter.get('title', ''))}", self.styles["chapter"]))
            art = chapter_art.get(chapter.get("id", ""), {})
            image_path = chapter.get("image") or art.get("image")
            caption = chapter.get("imageCaption") or art.get("imageCaption", "")
            if image_path:
                image = self._image(image_path, 88 * mm, 88 * mm)
                if image:
                    image.hAlign = "CENTER"
                    story.append(image)
                    if caption:
                        story.append(Paragraph(esc(caption), self.styles["caption"]))
            for paragraph in chapter.get("paragraphs", []):
                story.append(Paragraph(esc(paragraph), self.styles["body"]))
            if chapter.get("takeaway"):
                story.append(Paragraph(f"<b>Bölümün özü:</b> {esc(chapter['takeaway'])}", self.styles["body"]))
            if chapter.get("sourceRefs"):
                refs = " ".join(
                    f'<link href="#kaynak-{int(ref)}">[{int(ref)}]</link>'
                    for ref in chapter["sourceRefs"]
                )
                story.append(Paragraph(f"Kaynak izi: {refs}", self.styles["source_trace"]))
            story.append(Spacer(1, 3 * mm))

        story.extend([PageBreak(), Paragraph("KAYNAKLAR VE İLERİ OKUMALAR", self.styles["chapter"])])
        for source in self.summary.get("sources", []):
            source_id = int(source["id"])
            url = html.escape(source.get("url", ""), quote=True)
            title = esc(source.get("title", ""))
            story.append(Paragraph(
                f'<a name="kaynak-{source_id}"/><b>[{source_id}] {title}</b><br/>'
                f'<link href="{url}" color="#6D6346">{url}</link>',
                self.styles["source"],
            ))
        story.append(Spacer(1, 5 * mm))
        story.append(Paragraph(
            "<b>Telif ve sorumluluk notu:</b> Bu bağımsız ve ticari olmayan ön okuma rehberi "
            "eğitim ve araştırma amacıyla hazırlanmıştır; özgün eserin yerini tutmaz.",
            self.styles["body"],
        ))
        doc.build(story, onFirstPage=self._page, onLaterPages=self._page)
        return self.output_path


def register_fonts() -> None:
    font_dir = Path("/System/Library/Fonts/Supplemental")
    pdfmetrics.registerFont(TTFont("ZGArial", str(font_dir / "Arial.ttf")))
    pdfmetrics.registerFont(TTFont("ZGArial-Bold", str(font_dir / "Arial Bold.ttf")))
    pdfmetrics.registerFont(TTFont("ZGArial-Italic", str(font_dir / "Arial Italic.ttf")))


def load_summary(number: int) -> dict:
    summary = json.loads((SUMMARY_DIR / f"{number}.json").read_text(encoding="utf-8"))
    summary["_sourceHash"] = source_hash(summary)
    return summary


def validate_pdf(summary: dict, path: Path) -> tuple[int, int]:
    reader = PdfReader(str(path))
    if not reader.pages:
        raise RuntimeError(f"#{summary['bookNo']}: empty PDF")
    extracted = "\n".join(page.extract_text() or "" for page in reader.pages)
    # Canvas-drawn running footers can be interleaved with a split paragraph by
    # PDF text extractors. Remove only our exact footer before comparing prose.
    extracted = re.sub(
        r"Zihin Gezgini · Ön Okuma Rehberi\s*\n?\s*\d+",
        " ",
        extracted,
        flags=re.IGNORECASE,
    )
    normalized = normalize_text(extracted)
    compact = re.sub(r"\s+", "", normalized)
    required = [summary["title"], summary.get("author", ""), summary.get("intro", "")]
    for chapter in summary.get("chapters", []):
        required.append(chapter.get("title", ""))
        required.extend(chapter.get("paragraphs", []))
    required.extend(source.get("title", "") for source in summary.get("sources", []))
    required.extend(source.get("url", "") for source in summary.get("sources", []))
    for value in required:
        candidate = normalize_text(value)
        candidate_compact = re.sub(r"\s+", "", candidate)
        if candidate_compact and candidate_compact not in compact:
            raise RuntimeError(
                f"#{summary['bookNo']}: PDF text missing canonical fragment: {value[:90]!r}"
            )
    raw = path.read_bytes()
    if b"/ASCII85Decode" in raw:
        raise RuntimeError(f"#{summary['bookNo']}: ASCII85 stream remains")
    if summary["bookNo"] in (244, 248):
        for removed in REMOVED_TEXT:
            if normalize_text(removed) in normalized:
                raise RuntimeError(f"#{summary['bookNo']}: removed legacy prose returned: {removed}")
    metadata = reader.metadata or {}
    if summary["_sourceHash"] not in str(metadata.get("/Keywords", "")):
        raise RuntimeError(f"#{summary['bookNo']}: source hash missing from metadata")
    expected_urls = {source.get("url", "").strip() for source in summary.get("sources", [])}
    expected_urls.discard("")
    linked_urls: set[str] = set()
    for page in reader.pages:
        for annotation_ref in page.get("/Annots", []):
            annotation = annotation_ref.get_object()
            action = annotation.get("/A") or {}
            if str(action.get("/S", "")) == "/URI" and action.get("/URI"):
                linked_urls.add(str(action["/URI"]))
    missing_links = sorted(expected_urls - linked_urls)
    if missing_links:
        raise RuntimeError(
            f"#{summary['bookNo']}: source URL annotations missing: {missing_links[:3]}"
        )
    return len(reader.pages), len(raw)


def build_all(stage_root: Path) -> list[tuple[int, Path, int, int]]:
    register_fonts()
    cache_root = stage_root / "cache"
    output_root = stage_root / "output"
    base.PDF_OUTPUT_ROOT = output_root
    base.TMP = cache_root
    results = []
    for number in range(1, 301):
        summary = load_summary(number)
        if number in SPECIAL_NUMBERS:
            path = AdaptiveSummaryPdfBook(summary, output_root, cache_root).build()
        else:
            path = repaired.RepairedPdfBook(summary).build()
        pages, size = validate_pdf(summary, path)
        results.append((number, path, pages, size))
        print(f"#{number:03d}: {pages} pages · {size / 1048576:.2f} MiB", flush=True)
    return results


def install(results: list[tuple[int, Path, int, int]]) -> None:
    expected = {str((ROOT / "data" / "pdfs" / path.name).resolve()) for _, path, _, _ in results}
    if len(expected) != 300:
        raise RuntimeError(f"Expected 300 unique PDF targets, got {len(expected)}")
    for _, staged, _, _ in results:
        target = ROOT / "data" / "pdfs" / staged.name
        os.replace(staged, target)


def stamp_installed_hashes() -> None:
    total = 0
    for number in range(1, 301):
        summary = load_summary(number)
        target = ROOT / summary["pdfUrl"].lstrip("/")
        reader = PdfReader(str(target))
        writer = PdfWriter()
        writer.clone_document_from_reader(reader)
        metadata = {
            str(key): str(value)
            for key, value in (reader.metadata or {}).items()
            if value is not None
        }
        metadata["/Keywords"] = f"source-sha256:{summary['_sourceHash']}"
        writer.add_metadata(metadata)
        descriptor, temporary_name = tempfile.mkstemp(prefix=f".{target.name}.", dir=target.parent)
        try:
            with os.fdopen(descriptor, "wb") as handle:
                writer.write(handle)
            os.replace(temporary_name, target)
        finally:
            if os.path.exists(temporary_name):
                os.unlink(temporary_name)
        _pages, size = validate_pdf(summary, target)
        total += size
        if number % 50 == 0:
            print(f"Stamped {number}/300 PDFs", flush=True)
    print(f"Stamped and validated 300 PDFs · {total / 1048576:.2f} MiB", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--install", action="store_true", help="replace the 300 PDFs after validation")
    parser.add_argument("--keep-stage", action="store_true")
    parser.add_argument("--stamp-hashes", action="store_true", help="refresh installed semantic source hashes")
    args = parser.parse_args()
    if args.stamp_hashes:
        stamp_installed_hashes()
        return
    stage_root = Path(tempfile.mkdtemp(prefix="zihin-pdf-rebuild-"))
    try:
        results = build_all(stage_root)
        total = sum(size for _, _, _, size in results)
        print(f"Validated 300 PDFs · {total / 1048576:.2f} MiB", flush=True)
        if args.install:
            install(results)
            print("Installed 300 validated PDFs.", flush=True)
        else:
            print(f"Dry-run output: {stage_root / 'output' / 'data' / 'pdfs'}", flush=True)
    finally:
        if args.install and not args.keep_stage:
            shutil.rmtree(stage_root, ignore_errors=True)


if __name__ == "__main__":
    main()
