#!/usr/bin/env python3
"""Create visually rich 25–50 page PDFs from the five summary JSON files."""

from __future__ import annotations

import html
import json
import math
from collections import OrderedDict
from pathlib import Path

from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Image as RLImage
from reportlab.platypus import Paragraph
from PIL import Image as PILImage


ROOT = Path(__file__).resolve().parents[1]
PDF_DIR = ROOT / "data" / "pdfs"
TMP = ROOT / "tmp" / "pdfs" / "five-new-summaries"
BOOK_NUMBERS = (31, 88, 142, 213, 287)
PAGE_W, PAGE_H = A4
PAPER = colors.HexColor("#F4F0E6")
BODY = colors.HexColor("#26323B")
MUTED = colors.HexColor("#69747A")
RULE = colors.HexColor("#D4CEC0")


def register_fonts() -> None:
    base = Path("/System/Library/Fonts/Supplemental")
    pdfmetrics.registerFont(TTFont("ZGArial", str(base / "Arial.ttf")))
    pdfmetrics.registerFont(TTFont("ZGArial-Bold", str(base / "Arial Bold.ttf")))
    pdfmetrics.registerFont(TTFont("ZGArial-Italic", str(base / "Arial Italic.ttf")))


def esc(value: str) -> str:
    return html.escape(value, quote=False).replace("\n", "<br/>")


def color(hex_value: str) -> colors.Color:
    return colors.HexColor(hex_value)


def draw_rich(canvas: Canvas, text: str, style: ParagraphStyle, x: float, top: float, width: float) -> float:
    paragraph = Paragraph(esc(text), style)
    _w, height = paragraph.wrap(width, PAGE_H)
    paragraph.drawOn(canvas, x, top - height)
    return top - height


def paragraph_height(text: str, style: ParagraphStyle, width: float) -> float:
    paragraph = Paragraph(esc(text), style)
    return paragraph.wrap(width, PAGE_H)[1]


class PdfBook:
    def __init__(self, summary: dict):
        self.summary = summary
        self.ink = color(summary["chapterArtColor"])
        self.pdf_path = ROOT / summary["pdfUrl"].lstrip("/")
        self.pdf_path.parent.mkdir(parents=True, exist_ok=True)
        self.chapter_art = summary["chapterArtworks"]
        self.asset_cache_dir = TMP / str(summary["bookNo"])
        self.asset_cache_dir.mkdir(parents=True, exist_ok=True)
        self.styles = self.make_styles()
        self.total_pages = self.plan_total_pages()
        self.page = 0
        self.canvas = Canvas(
            str(self.pdf_path),
            pagesize=A4,
            pageCompression=1,
            invariant=1,
        )
        self.canvas.setTitle(f"{summary['author']} - {summary['title']} | Zihin Gezgini")
        self.canvas.setAuthor("Zihin Gezgini")
        self.canvas.setSubject("Sade, örnekli, eleştirel ve görselleştirilmiş uzun okuma rehberi")

    def pdf_asset(self, path: Path, *, cover: bool = False) -> Path:
        suffix = "cover" if cover else "chapter"
        target = self.asset_cache_dir / f"{path.stem}-{suffix}.jpg"
        if not target.exists() or target.stat().st_mtime < path.stat().st_mtime:
            with PILImage.open(path) as source:
                image = source.convert("RGB")
                image.thumbnail((720, 1080) if cover else (560, 560), PILImage.Resampling.LANCZOS)
                image.save(target, "JPEG", quality=80 if cover else 76, optimize=True, progressive=True)
        return target

    def make_styles(self) -> dict[str, ParagraphStyle]:
        return {
            "body": ParagraphStyle(
                "Body", fontName="ZGArial", fontSize=12.7, leading=18.1,
                textColor=BODY, alignment=TA_JUSTIFY, spaceAfter=5.5,
                splitLongWords=False, allowWidows=0, allowOrphans=0,
            ),
            "body_small": ParagraphStyle(
                "BodySmall", fontName="ZGArial", fontSize=11.3, leading=16.1,
                textColor=BODY, alignment=TA_JUSTIFY, spaceAfter=5,
                splitLongWords=False,
            ),
            "caption": ParagraphStyle(
                "Caption", fontName="ZGArial-Italic", fontSize=9.6, leading=12.4,
                textColor=MUTED, alignment=TA_LEFT,
            ),
            "intro": ParagraphStyle(
                "Intro", fontName="ZGArial", fontSize=12.1, leading=17.2,
                textColor=BODY, alignment=TA_JUSTIFY, spaceAfter=8,
            ),
            "toc": ParagraphStyle(
                "Toc", fontName="ZGArial", fontSize=10.5, leading=14.4,
                textColor=BODY, alignment=TA_LEFT,
            ),
            "note": ParagraphStyle(
                "Note", fontName="ZGArial", fontSize=12.5, leading=17.8,
                textColor=BODY, alignment=TA_JUSTIFY, spaceAfter=5.2,
            ),
        }

    def grouped_sections(self) -> OrderedDict[str, list[dict]]:
        grouped: OrderedDict[str, list[dict]] = OrderedDict()
        for chapter in self.summary["chapters"][1:]:
            grouped.setdefault(chapter["section"], []).append(chapter)
        return grouped

    def plan_total_pages(self) -> int:
        sections = self.grouped_sections()
        divider_pages = sum(1 for section in sections if section != "BAŞLANGIÇ")
        artwork_pages = len(self.chapter_art)
        note_pages = 0
        # Match the real reading order: an artwork page breaks a run of compact
        # note chapters, so notes on its two sides cannot share one page.
        for chapters in sections.values():
            note_run: list[dict] = []
            for chapter in chapters:
                if chapter["id"] in self.chapter_art:
                    note_pages += len(self.note_groups(note_run))
                    note_run = []
                else:
                    note_run.append(chapter)
            note_pages += len(self.note_groups(note_run))
        # Cover + opening + contents + section dividers + art chapters + text notes + sources.
        return 3 + divider_pages + artwork_pages + note_pages + 1

    def note_height(self, chapter: dict) -> float:
        title_style = ParagraphStyle(
            "NoteMeasureTitle", fontName="ZGArial-Bold", fontSize=18.5,
            leading=21.5, textColor=BODY,
        )
        height = 13 * mm + paragraph_height(chapter["title"], title_style, 164 * mm)
        height += sum(paragraph_height(paragraph, self.styles["note"], 164 * mm) + 3.2 for paragraph in chapter["paragraphs"])
        return height

    def note_groups(self, chapters: list[dict]) -> list[list[dict]]:
        groups: list[list[dict]] = []
        current: list[dict] = []
        current_height = 0.0
        for chapter in chapters:
            addition = self.note_height(chapter) + (13 * mm if current else 0)
            if current and (len(current) == 2 or current_height + addition > 216 * mm):
                groups.append(current)
                current = []
                current_height = 0.0
                addition = self.note_height(chapter)
            current.append(chapter)
            current_height += addition
        if current:
            groups.append(current)
        return groups

    def begin_page(self, *, body_page: bool = True) -> None:
        self.page += 1
        self.canvas.setFillColor(PAPER)
        self.canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        if body_page:
            self.canvas.setStrokeColor(RULE)
            self.canvas.setLineWidth(0.55)
            self.canvas.line(22 * mm, PAGE_H - 15 * mm, PAGE_W - 20 * mm, PAGE_H - 15 * mm)
            self.canvas.line(22 * mm, 14 * mm, PAGE_W - 20 * mm, 14 * mm)
            self.canvas.setFillColor(MUTED)
            self.canvas.setFont("ZGArial", 7.6)
            self.canvas.drawString(22 * mm, PAGE_H - 11.8 * mm, self.summary["title"].upper())
            self.canvas.drawRightString(PAGE_W - 20 * mm, PAGE_H - 11.8 * mm, "SADE · ÖRNEKLİ · ELEŞTİREL ANLATIM")
            self.canvas.setFont("ZGArial-Italic", 7.3)
            self.canvas.drawString(22 * mm, 9.2 * mm, "Ders notu değil; kavramların hayatın içinden aktığı görsel okuma yolculuğu")
            self.canvas.setFillColor(self.ink)
            self.canvas.setFont("ZGArial-Bold", 8)
            self.canvas.drawRightString(PAGE_W - 20 * mm, 9.2 * mm, f"{self.page:03d} / {self.total_pages:03d}")

    def end_page(self) -> None:
        self.canvas.showPage()

    def draw_cover(self) -> None:
        self.begin_page(body_page=False)
        c = self.canvas
        c.setFillColor(self.ink)
        c.rect(0, 0, 32 * mm, PAGE_H, fill=1, stroke=0)
        cover_path = ROOT / self.summary["coverImage"].lstrip("/")
        image = RLImage(str(self.pdf_asset(cover_path, cover=True)), width=72 * mm, height=108 * mm)
        image.drawOn(c, 118 * mm, 104 * mm)
        c.setStrokeColor(self.ink)
        c.setLineWidth(1.8)
        c.line(47 * mm, 198 * mm, 107 * mm, 198 * mm)
        c.setFillColor(self.ink)
        c.setFont("ZGArial-Bold", 12)
        c.drawString(47 * mm, 244 * mm, self.summary["author"].upper())
        cover_title_width = 62 * mm
        title_size = 27.0
        longest_word = max(self.summary["title"].split(), key=len)
        while pdfmetrics.stringWidth(longest_word, "ZGArial-Bold", title_size) > cover_title_width and title_size > 18:
            title_size -= 0.5
        title_style = ParagraphStyle(
            "CoverTitle", fontName="ZGArial-Bold", fontSize=title_size, leading=title_size * 1.13,
            textColor=BODY, alignment=TA_LEFT,
        )
        y = draw_rich(c, self.summary["title"], title_style, 47 * mm, 232 * mm, cover_title_width)
        c.setFillColor(MUTED)
        c.setFont("ZGArial", 10.2)
        c.drawString(47 * mm, y - 16 * mm, f"{self.total_pages} sayfalık görselleştirilmiş geniş özet")
        c.setFillColor(BODY)
        c.setFont("ZGArial", 9.6)
        c.drawString(47 * mm, 69 * mm, "16 özgün bölüm gravürü · Gündelik örnekler")
        c.drawString(47 * mm, 62 * mm, "Ana fikirler · Eleştiriler · Akılda kalan sahneler")
        c.setFillColor(MUTED)
        c.setFont("ZGArial-Italic", 8)
        c.drawString(47 * mm, 29 * mm, "Özgün eserin yerini tutmayan açıklamalı okuma rehberi")
        self.end_page()

    def draw_opening(self) -> None:
        self.begin_page()
        c = self.canvas
        c.setFillColor(self.ink)
        c.setFont("ZGArial-Bold", 10)
        c.drawString(23 * mm, 263 * mm, "OKUMAYA BAŞLAMADAN ÖNCE")
        c.setFillColor(BODY)
        c.setFont("ZGArial-Bold", 23)
        c.drawString(23 * mm, 249 * mm, "Bu rehberin pusulası")
        c.setStrokeColor(self.ink)
        c.setLineWidth(2)
        c.line(23 * mm, 242 * mm, 187 * mm, 242 * mm)

        cover_path = ROOT / self.summary["coverImage"].lstrip("/")
        image_bottom = 158 * mm
        image = RLImage(str(self.pdf_asset(cover_path, cover=True)), width=48 * mm, height=72 * mm)
        image.drawOn(c, 139 * mm, image_bottom)
        y = draw_rich(c, self.summary["intro"], self.styles["intro"], 23 * mm, 232 * mm, 108 * mm)

        first = self.summary["chapters"][0]
        opening_title = ParagraphStyle(
            "OpeningTitle", fontName="ZGArial-Bold", fontSize=15.5,
            leading=18.5, textColor=self.ink,
        )
        # The opening chapter uses the full text width. Keep its first line below
        # both the narrow intro column and the cover image so neither can overlap.
        chapter_top = min(y - 8 * mm, image_bottom - 8 * mm)
        y = draw_rich(c, first["title"], opening_title, 23 * mm, chapter_top, 164 * mm) - 3 * mm
        for paragraph in first["paragraphs"]:
            y = draw_rich(c, paragraph, self.styles["body_small"], 23 * mm, y, 164 * mm) - 3.5
        if y < 42 * mm:
            raise RuntimeError(f"Opening page overflow in book {self.summary['bookNo']}")

        c.setFillColor(self.ink)
        c.setFont("ZGArial-Bold", 10)
        c.drawString(23 * mm, 31 * mm, "KULLANIM ÖNERİSİ")
        c.setFillColor(MUTED)
        c.setFont("ZGArial", 9.2)
        c.drawString(23 * mm, 24 * mm, "Bir oturuşta bitirmek zorunda değilsiniz; her gravür bir sonraki durak için hafıza kancasıdır.")
        self.end_page()

    def draw_contents(self) -> None:
        self.begin_page()
        c = self.canvas
        c.setFillColor(self.ink)
        c.setFont("ZGArial-Bold", 10)
        c.drawString(23 * mm, 263 * mm, "YOL HARİTASI")
        c.setFillColor(BODY)
        c.setFont("ZGArial-Bold", 24)
        c.drawString(23 * mm, 248 * mm, f"{len(self.summary['chapters'])} durakta kitabın bütünü")
        c.setStrokeColor(self.ink)
        c.setLineWidth(2)
        c.line(23 * mm, 240 * mm, 187 * mm, 240 * mm)
        columns = [23 * mm, 108 * mm]
        widths = [76 * mm, 79 * mm]
        ys = [229 * mm, 229 * mm]
        midpoint = math.ceil(len(self.summary["chapters"]) / 2)
        for index, chapter in enumerate(self.summary["chapters"], 1):
            col = 0 if index <= midpoint else 1
            c.setFillColor(self.ink)
            c.setFont("ZGArial-Bold", 8.5)
            c.drawString(columns[col], ys[col], f"{index:02d}")
            title_style = self.styles["toc"]
            ys[col] = draw_rich(c, chapter["title"], title_style, columns[col] + 9 * mm, ys[col] + 3, widths[col] - 9 * mm) - 7
            if index == midpoint:
                continue
        self.end_page()

    def draw_section_divider(self, section: str, chapters: list[dict]) -> None:
        self.begin_page()
        c = self.canvas
        c.setFillColor(self.ink)
        c.setFont("ZGArial-Bold", 10)
        c.drawString(23 * mm, 263 * mm, "YENİ BÖLÜM")
        section_style = ParagraphStyle(
            "Section", fontName="ZGArial-Bold", fontSize=24, leading=28,
            textColor=BODY, alignment=TA_LEFT,
        )
        y = draw_rich(c, section, section_style, 23 * mm, 253 * mm, 164 * mm)
        c.setStrokeColor(self.ink)
        c.setLineWidth(2)
        c.line(23 * mm, y - 4 * mm, 187 * mm, y - 4 * mm)

        artwork = next((self.chapter_art[ch["id"]] for ch in chapters if ch["id"] in self.chapter_art), None)
        if artwork:
            img_path = ROOT / artwork["image"].lstrip("/")
        else:
            fallback_art = next(iter(self.chapter_art.values()))
            img_path = ROOT / fallback_art["image"].lstrip("/")
        image = RLImage(str(self.pdf_asset(img_path)), width=91 * mm, height=91 * mm)
        image.drawOn(c, 96 * mm, 112 * mm)

        c.setFillColor(self.ink)
        c.setFont("ZGArial-Bold", 10)
        c.drawString(23 * mm, 202 * mm, "BU BÖLÜMÜN DURAKLARI")
        list_y = 192 * mm
        for idx, chapter in enumerate(chapters, 1):
            c.setFillColor(self.ink)
            c.circle(25 * mm, list_y + 1.5 * mm, 1.1 * mm, fill=1, stroke=0)
            list_style = ParagraphStyle(
                f"SectionItem{idx}", fontName="ZGArial", fontSize=10.7,
                leading=13.8, textColor=BODY,
            )
            list_y = draw_rich(c, chapter["title"], list_style, 30 * mm, list_y, 58 * mm) - 3 * mm

        route_text = (
            "Bu ara sayfa metni uzatmak için değil, zihinde yön duygusu kurmak için var. "
            "Sağdaki gravürü bölümün hafıza kapısı olarak kullanın; soldaki başlıklar ilerledikçe "
            "aynı ana sorunun farklı yüzlerini gösterecek."
        )
        route_top = min(91 * mm, list_y - 8 * mm)
        draw_rich(c, route_text, self.styles["body_small"], 23 * mm, route_top, 164 * mm)
        self.end_page()

    def draw_art_chapter(self, chapter: dict, index: int) -> None:
        self.begin_page()
        c = self.canvas
        art = self.chapter_art[chapter["id"]]
        c.setFillColor(self.ink)
        c.setFont("ZGArial-Bold", 9.3)
        c.drawString(23 * mm, 263 * mm, chapter["section"])
        c.drawRightString(187 * mm, 263 * mm, f"{index:02d}. DURAK")
        title_style = ParagraphStyle(
            "ChapterTitle", fontName="ZGArial-Bold", fontSize=20.5, leading=23.5,
            textColor=BODY, alignment=TA_LEFT,
        )
        y = draw_rich(c, chapter["title"], title_style, 23 * mm, 255 * mm, 164 * mm)
        c.setStrokeColor(self.ink)
        c.setLineWidth(1.3)
        c.line(23 * mm, y - 3 * mm, 187 * mm, y - 3 * mm)
        top = y - 10 * mm

        image_path = ROOT / art["image"].lstrip("/")
        image_size = 91 * mm
        image = RLImage(str(self.pdf_asset(image_path)), width=image_size, height=image_size)
        image.drawOn(c, 23 * mm, top - image_size)
        caption_top = top - image_size - 3 * mm
        caption_bottom = draw_rich(c, art["imageCaption"], self.styles["caption"], 23 * mm, caption_top, image_size)

        right_x = 121 * mm
        right_w = 66 * mm
        right_y = top
        placed = 0
        # Fill the narrow column until it reaches the artwork/caption depth.
        for paragraph in chapter["paragraphs"]:
            height = paragraph_height(paragraph, self.styles["body"], right_w)
            if placed >= 2 and right_y - height < caption_bottom:
                break
            right_y = draw_rich(c, paragraph, self.styles["body"], right_x, right_y, right_w) - 4
            placed += 1

        full_y = min(caption_bottom, right_y) - 6 * mm
        for paragraph in chapter["paragraphs"][placed:]:
            full_y = draw_rich(c, paragraph, self.styles["body"], 23 * mm, full_y, 164 * mm) - 4

        if full_y < 25 * mm:
            raise RuntimeError(f"Chapter overflow in book {self.summary['bookNo']}: {chapter['title']}")
        self.end_page()

    def draw_note_page(self, chapters: list[dict], first_index: int) -> None:
        self.begin_page()
        c = self.canvas
        c.setFillColor(self.ink)
        c.setFont("ZGArial-Bold", 9.5)
        c.drawString(23 * mm, 263 * mm, chapters[0]["section"])
        y = 252 * mm
        for offset, chapter in enumerate(chapters):
            if offset:
                c.setStrokeColor(RULE)
                c.setLineWidth(0.8)
                c.line(23 * mm, y + 3 * mm, 187 * mm, y + 3 * mm)
                y -= 9 * mm
            c.setFillColor(self.ink)
            c.setFont("ZGArial-Bold", 9)
            c.drawString(23 * mm, y, f"{first_index + offset:02d}. DURAK")
            note_title = ParagraphStyle(
                f"NoteTitle{offset}", fontName="ZGArial-Bold", fontSize=18.5,
                leading=21.5, textColor=BODY,
            )
            y = draw_rich(c, chapter["title"], note_title, 23 * mm, y - 5 * mm, 164 * mm) - 4
            for paragraph in chapter["paragraphs"]:
                y = draw_rich(c, paragraph, self.styles["note"], 23 * mm, y, 164 * mm) - 3.2
            y -= 4 * mm
        if y < 24 * mm:
            raise RuntimeError(f"Note page overflow in book {self.summary['bookNo']}")
        self.end_page()

    def draw_sources(self) -> None:
        self.begin_page()
        c = self.canvas
        c.setFillColor(self.ink)
        c.setFont("ZGArial-Bold", 10)
        c.drawString(23 * mm, 263 * mm, "KAYNAKLAR VE KAPSAM")
        c.setFillColor(BODY)
        c.setFont("ZGArial-Bold", 23)
        c.drawString(23 * mm, 248 * mm, "Neye dayandık, nerede durduk?")
        c.setStrokeColor(self.ink)
        c.setLineWidth(2)
        c.line(23 * mm, 240 * mm, 187 * mm, 240 * mm)
        y = 229 * mm
        source_style = ParagraphStyle(
            "Source", fontName="ZGArial", fontSize=10.8, leading=14.6,
            textColor=BODY, alignment=TA_LEFT,
        )
        for source in self.summary.get("sources", []):
            c.setFillColor(self.ink)
            c.setFont("ZGArial-Bold", 8.8)
            c.drawString(23 * mm, y, f"[{source['id']}]")
            y = draw_rich(c, source["title"], source_style, 34 * mm, y + 3, 153 * mm) - 7

        c.setFillColor(self.ink)
        c.setFont("ZGArial-Bold", 11)
        c.drawString(23 * mm, y - 3 * mm, "TELİF VE SORUMLULUK NOTU")
        disclaimer = (
            "Bu çalışma eğitim ve araştırma amacıyla hazırlanmış özgün bir özet ve yorum rehberidir. "
            "Kitabın cümlelerini yeniden üretmez ve özgün eserin yerini tutmaz. Sağlık ve psikoloji "
            "başlıkları genel bilgi verir; tanı, tedavi veya kişiye özel profesyonel öneri değildir."
        )
        y = draw_rich(c, disclaimer, self.styles["body_small"], 23 * mm, y - 10 * mm, 164 * mm)
        c.setFillColor(self.ink)
        c.setFont("ZGArial-Bold", 11)
        c.drawString(23 * mm, y - 10 * mm, "SON CÜMLE")
        last = self.summary["chapters"][-1]["paragraphs"][-1]
        draw_rich(c, last, self.styles["intro"], 23 * mm, y - 18 * mm, 164 * mm)
        self.end_page()

    def build(self) -> Path:
        self.draw_cover()
        self.draw_opening()
        self.draw_contents()
        chapter_numbers = {chapter["id"]: index for index, chapter in enumerate(self.summary["chapters"], 1)}
        for section, chapters in self.grouped_sections().items():
            if section != "BAŞLANGIÇ":
                self.draw_section_divider(section, chapters)
            notes = []
            for chapter in chapters:
                if chapter["id"] in self.chapter_art:
                    if notes:
                        for pair in self.note_groups(notes):
                            self.draw_note_page(pair, chapter_numbers[pair[0]["id"]])
                        notes = []
                    self.draw_art_chapter(chapter, chapter_numbers[chapter["id"]])
                else:
                    notes.append(chapter)
            if notes:
                for pair in self.note_groups(notes):
                    self.draw_note_page(pair, chapter_numbers[pair[0]["id"]])
        self.draw_sources()
        self.canvas.save()
        actual = len(PdfReader(str(self.pdf_path)).pages)
        if actual != self.total_pages:
            raise RuntimeError(f"Page plan mismatch for {self.summary['bookNo']}: planned {self.total_pages}, actual {actual}")
        if not 25 <= actual <= 50:
            raise RuntimeError(f"Book {self.summary['bookNo']} has {actual} pages; required 25–50")
        return self.pdf_path


def main() -> None:
    register_fonts()
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    for number in BOOK_NUMBERS:
        summary = json.loads((ROOT / "data" / "summaries" / f"{number}.json").read_text(encoding="utf-8"))
        path = PdfBook(summary).build()
        reader = PdfReader(str(path))
        words = sum(len((page.extract_text() or "").split()) for page in reader.pages)
        print(f"{path.relative_to(ROOT)}: {len(reader.pages)} pages, {words} extracted words")


if __name__ == "__main__":
    main()
