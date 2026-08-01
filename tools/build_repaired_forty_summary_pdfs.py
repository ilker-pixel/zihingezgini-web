#!/usr/bin/env python3
"""Build the repaired forty summaries with natural continuation pages.

The first artwork page keeps each existing interior image exactly once.  Long
chapters continue at readable type size instead of shrinking or being padded by
generic divider pages.  Image captions are part of the enriched prose, so they
are not duplicated beneath the image.
"""

from __future__ import annotations

from pathlib import Path

import build_five_summary_pdfs as builder
from pypdf import PdfReader
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle


builder.BOOK_NUMBERS = (
    8, 18, 34, 38, 61, 70, 92, 99, 121, 138,
    151, 157, 182, 195, 211, 216, 238, 244, 266, 294,
    12, 17, 32, 41, 66, 72, 93, 103, 122, 124,
    152, 156, 189, 194, 214, 222, 241, 253, 271, 275,
)
builder.TMP = Path(__file__).resolve().parents[1] / "tmp" / "pdfs" / "repaired-forty"


class RepairedPdfBook(builder.PdfBook):
    def make_styles(self):
        styles = super().make_styles()
        styles["body"].fontSize = 12.4
        styles["body"].leading = 17.6
        styles["note"].fontSize = 12.2
        styles["note"].leading = 17.4
        return styles

    @staticmethod
    def paragraphs(chapter: dict) -> list[str]:
        return chapter.get("paragraphs", []) + chapter.get("extraParagraphs", [])

    def note_height(self, chapter: dict) -> float:
        title_style = ParagraphStyle(
            "RepairNoteMeasureTitle", fontName="ZGArial-Bold", fontSize=18.5,
            leading=21.5, textColor=builder.BODY,
        )
        height = 13 * builder.mm + builder.paragraph_height(chapter["title"], title_style, 164 * builder.mm)
        height += sum(
            builder.paragraph_height(paragraph, self.styles["note"], 164 * builder.mm) + 3.2
            for paragraph in self.paragraphs(chapter)
        )
        return height

    def art_first_page_count(self, chapter: dict) -> int:
        title_style = ParagraphStyle(
            "RepairMeasureChapterTitle", fontName="ZGArial-Bold", fontSize=20.5,
            leading=23.5, textColor=builder.BODY, alignment=TA_LEFT,
        )
        title_bottom = 255 * builder.mm - builder.paragraph_height(
            chapter["title"], title_style, 164 * builder.mm
        )
        top = title_bottom - 10 * builder.mm
        image_bottom = top - 91 * builder.mm
        right_y = top
        right_w = 66 * builder.mm
        paragraphs = self.paragraphs(chapter)
        placed = 0
        for paragraph in paragraphs:
            height = builder.paragraph_height(paragraph, self.styles["body"], right_w)
            if placed >= 2 and right_y - height < image_bottom:
                break
            right_y -= height + 4
            placed += 1
        full_y = min(image_bottom, right_y) - 6 * builder.mm
        for paragraph in paragraphs[placed:]:
            height = builder.paragraph_height(paragraph, self.styles["body"], 164 * builder.mm)
            if full_y - height - 4 < 25 * builder.mm:
                break
            full_y -= height + 4
            placed += 1
        return placed

    def continuation_groups(self, chapter: dict) -> list[list[str]]:
        paragraphs = self.paragraphs(chapter)
        remaining = paragraphs[self.art_first_page_count(chapter):]
        groups: list[list[str]] = []
        continuation_title = ParagraphStyle(
            "RepairContinuationMeasure", fontName="ZGArial-Bold", fontSize=18.5,
            leading=21.5, textColor=builder.BODY,
        )
        while remaining:
            y = 250 * builder.mm - builder.paragraph_height(
                f"{chapter['title']} — devam", continuation_title, 164 * builder.mm
            ) - 10 * builder.mm
            group: list[str] = []
            while remaining:
                height = builder.paragraph_height(remaining[0], self.styles["note"], 164 * builder.mm) + 3.2
                if group and y - height < 25 * builder.mm:
                    break
                if not group and y - height < 25 * builder.mm:
                    raise RuntimeError(
                        f"Single continuation paragraph overflow in {self.summary['bookNo']}: {chapter['title']}"
                    )
                group.append(remaining.pop(0))
                y -= height
            groups.append(group)
        return groups

    def plan_total_pages(self) -> int:
        artwork_pages = 0
        note_pages = 0
        for chapters in self.grouped_sections().values():
            note_run: list[dict] = []
            for chapter in chapters:
                if chapter["id"] in self.chapter_art:
                    note_pages += len(self.note_groups(note_run))
                    note_run = []
                    artwork_pages += 1 + len(self.continuation_groups(chapter))
                else:
                    note_run.append(chapter)
            note_pages += len(self.note_groups(note_run))
        # Three visual checkpoints connect each block of four illustrations.
        # They are dense route maps, not generic text padding.
        return 3 + artwork_pages + note_pages + 3 + 1

    def draw_checkpoint(self, stage: int, completed: list[dict], upcoming: list[dict]) -> None:
        self.begin_page()
        c = self.canvas
        c.setFillColor(self.ink)
        c.setFont("ZGArial-Bold", 9.5)
        c.drawString(23 * builder.mm, 263 * builder.mm, f"OKUMA EŞİĞİ {stage} / 3")
        title_style = ParagraphStyle(
            f"RepairCheckpointTitle{stage}", fontName="ZGArial-Bold", fontSize=22,
            leading=25.5, textColor=builder.BODY, alignment=TA_LEFT,
        )
        checkpoint_titles = (
            "İlk bağlantılar artık görünür",
            "Ayrıntılardan büyük resme",
            "Son sorulara yaklaşırken",
        )
        y = builder.draw_rich(
            c, checkpoint_titles[stage - 1], title_style,
            23 * builder.mm, 252 * builder.mm, 164 * builder.mm,
        )
        c.setStrokeColor(self.ink)
        c.setLineWidth(1.5)
        c.line(23 * builder.mm, y - 3 * builder.mm, 187 * builder.mm, y - 3 * builder.mm)

        thumb = 38 * builder.mm
        gap = 4 * builder.mm
        image_top = y - 12 * builder.mm
        for offset, chapter in enumerate(completed):
            art = self.chapter_art[chapter["id"]]
            image_path = builder.ROOT / art["image"].lstrip("/")
            image = builder.RLImage(str(self.pdf_asset(image_path)), width=thumb, height=thumb)
            col = offset % 2
            row = offset // 2
            image.drawOn(
                c,
                23 * builder.mm + col * (thumb + gap),
                image_top - thumb - row * (thumb + gap),
            )

        right_x = 110 * builder.mm
        right_w = 77 * builder.mm
        c.setFillColor(self.ink)
        c.setFont("ZGArial-Bold", 9.3)
        c.drawString(right_x, image_top, "GERİDE KALAN DÖRT DURAK")
        item_style = ParagraphStyle(
            f"RepairCheckpointItem{stage}", fontName="ZGArial", fontSize=10.3,
            leading=13.4, textColor=builder.BODY, alignment=TA_LEFT,
        )
        list_y = image_top - 7 * builder.mm
        for chapter in completed:
            c.setFillColor(self.ink)
            c.circle(right_x + 1.5 * builder.mm, list_y + 1.2 * builder.mm, 0.9 * builder.mm, fill=1, stroke=0)
            list_y = builder.draw_rich(c, chapter["title"], item_style, right_x + 6 * builder.mm, list_y, right_w - 6 * builder.mm) - 3 * builder.mm

        c.setFillColor(self.ink)
        c.setFont("ZGArial-Bold", 9.3)
        c.drawString(right_x, list_y - 3 * builder.mm, "SIRADAKİ DÖRT DURAK")
        list_y -= 10 * builder.mm
        for chapter in upcoming:
            c.setFillColor(self.ink)
            c.circle(right_x + 1.5 * builder.mm, list_y + 1.2 * builder.mm, 0.9 * builder.mm, fill=1, stroke=0)
            list_y = builder.draw_rich(c, chapter["title"], item_style, right_x + 6 * builder.mm, list_y, right_w - 6 * builder.mm) - 3 * builder.mm

        question_style = ParagraphStyle(
            f"RepairCheckpointQuestion{stage}", fontName="ZGArial-Italic", fontSize=10.8,
            leading=14.6, textColor=self.ink, alignment=TA_LEFT,
        )
        question = (
            f"Bağlantı sorusu: “{completed[0]['title']}” ile “{completed[-1]['title']}” arasında "
            f"hangi düşünce yolu kuruluyor? Bir sonraki durak olan “{upcoming[0]['title']}” bu yolu "
            "nasıl değiştirebilir?"
        )
        builder.draw_rich(c, question, question_style, 23 * builder.mm, 64 * builder.mm, 164 * builder.mm)
        self.end_page()

    def draw_art_chapter(self, chapter: dict, index: int) -> None:
        paragraphs = self.paragraphs(chapter)
        placed = self.art_first_page_count(chapter)
        self.begin_page()
        c = self.canvas
        art = self.chapter_art[chapter["id"]]
        c.setFillColor(self.ink)
        c.setFont("ZGArial-Bold", 9.3)
        c.drawString(23 * builder.mm, 263 * builder.mm, chapter["section"])
        c.drawRightString(187 * builder.mm, 263 * builder.mm, f"{index:02d}. DURAK")
        title_style = ParagraphStyle(
            "RepairChapterTitle", fontName="ZGArial-Bold", fontSize=20.5, leading=23.5,
            textColor=builder.BODY, alignment=TA_LEFT,
        )
        y = builder.draw_rich(c, chapter["title"], title_style, 23 * builder.mm, 255 * builder.mm, 164 * builder.mm)
        c.setStrokeColor(self.ink)
        c.setLineWidth(1.3)
        c.line(23 * builder.mm, y - 3 * builder.mm, 187 * builder.mm, y - 3 * builder.mm)
        top = y - 10 * builder.mm
        image_path = builder.ROOT / art["image"].lstrip("/")
        image_size = 91 * builder.mm
        image = builder.RLImage(str(self.pdf_asset(image_path)), width=image_size, height=image_size)
        image.drawOn(c, 23 * builder.mm, top - image_size)
        image_bottom = top - image_size

        right_x = 121 * builder.mm
        right_w = 66 * builder.mm
        right_y = top
        narrow_count = 0
        for paragraph in paragraphs[:placed]:
            height = builder.paragraph_height(paragraph, self.styles["body"], right_w)
            if narrow_count >= 2 and right_y - height < image_bottom:
                break
            right_y = builder.draw_rich(c, paragraph, self.styles["body"], right_x, right_y, right_w) - 4
            narrow_count += 1
        full_y = min(image_bottom, right_y) - 6 * builder.mm
        for paragraph in paragraphs[narrow_count:placed]:
            full_y = builder.draw_rich(c, paragraph, self.styles["body"], 23 * builder.mm, full_y, 164 * builder.mm) - 4
        if full_y < 24 * builder.mm:
            raise RuntimeError(f"First art page overflow in {self.summary['bookNo']}: {chapter['title']}")
        self.end_page()

        continuation_title = ParagraphStyle(
            "RepairContinuationTitle", fontName="ZGArial-Bold", fontSize=18.5,
            leading=21.5, textColor=builder.BODY, alignment=TA_LEFT,
        )
        for continuation_index, group in enumerate(self.continuation_groups(chapter), 1):
            self.begin_page()
            c = self.canvas
            c.setFillColor(self.ink)
            c.setFont("ZGArial-Bold", 9.3)
            c.drawString(23 * builder.mm, 263 * builder.mm, chapter["section"])
            c.drawRightString(187 * builder.mm, 263 * builder.mm, f"{index:02d}. DURAK · DEVAM {continuation_index}")
            y = builder.draw_rich(
                c, f"{chapter['title']} — devam", continuation_title,
                23 * builder.mm, 250 * builder.mm, 164 * builder.mm,
            ) - 10 * builder.mm
            c.setStrokeColor(self.ink)
            c.setLineWidth(1.1)
            c.line(23 * builder.mm, y + 5 * builder.mm, 187 * builder.mm, y + 5 * builder.mm)
            for paragraph in group:
                y = builder.draw_rich(c, paragraph, self.styles["note"], 23 * builder.mm, y, 164 * builder.mm) - 3.2
            if y < 24 * builder.mm:
                raise RuntimeError(f"Continuation overflow in {self.summary['bookNo']}: {chapter['title']}")
            self.end_page()

    def draw_note_page(self, chapters: list[dict], first_index: int) -> None:
        self.begin_page()
        c = self.canvas
        c.setFillColor(self.ink)
        c.setFont("ZGArial-Bold", 9.5)
        c.drawString(23 * builder.mm, 263 * builder.mm, chapters[0]["section"])
        y = 252 * builder.mm
        for offset, chapter in enumerate(chapters):
            if offset:
                c.setStrokeColor(builder.RULE)
                c.setLineWidth(0.8)
                c.line(23 * builder.mm, y + 3 * builder.mm, 187 * builder.mm, y + 3 * builder.mm)
                y -= 9 * builder.mm
            c.setFillColor(self.ink)
            c.setFont("ZGArial-Bold", 9)
            c.drawString(23 * builder.mm, y, f"{first_index + offset:02d}. DURAK")
            note_title = ParagraphStyle(
                f"RepairNoteTitle{offset}", fontName="ZGArial-Bold", fontSize=18.5,
                leading=21.5, textColor=builder.BODY,
            )
            y = builder.draw_rich(c, chapter["title"], note_title, 23 * builder.mm, y - 5 * builder.mm, 164 * builder.mm) - 4
            for paragraph in self.paragraphs(chapter):
                y = builder.draw_rich(c, paragraph, self.styles["note"], 23 * builder.mm, y, 164 * builder.mm) - 3.2
            y -= 4 * builder.mm
        if y < 24 * builder.mm:
            raise RuntimeError(f"Note page overflow in book {self.summary['bookNo']}")
        self.end_page()

    def build(self) -> Path:
        self.draw_cover()
        self.draw_opening()
        self.draw_contents()
        chapter_numbers = {chapter["id"]: index for index, chapter in enumerate(self.summary["chapters"], 1)}
        all_art_chapters = [
            chapter for chapter in self.summary["chapters"]
            if chapter["id"] in self.chapter_art
        ]
        art_seen = 0
        for _section, chapters in self.grouped_sections().items():
            notes: list[dict] = []
            for chapter in chapters:
                if chapter["id"] in self.chapter_art:
                    if notes:
                        for group in self.note_groups(notes):
                            self.draw_note_page(group, chapter_numbers[group[0]["id"]])
                        notes = []
                    self.draw_art_chapter(chapter, chapter_numbers[chapter["id"]])
                    art_seen += 1
                    if art_seen in (4, 8, 12):
                        self.draw_checkpoint(
                            art_seen // 4,
                            all_art_chapters[art_seen - 4:art_seen],
                            all_art_chapters[art_seen:art_seen + 4],
                        )
                else:
                    notes.append(chapter)
            if notes:
                for group in self.note_groups(notes):
                    self.draw_note_page(group, chapter_numbers[group[0]["id"]])
        self.draw_sources()
        self.canvas.save()
        actual = len(PdfReader(str(self.pdf_path)).pages)
        if actual != self.total_pages:
            raise RuntimeError(
                f"Page plan mismatch for {self.summary['bookNo']}: planned {self.total_pages}, actual {actual}"
            )
        if not 25 <= actual <= 50:
            raise RuntimeError(f"Book {self.summary['bookNo']} has {actual} pages; required 25-50")
        return self.pdf_path


builder.PdfBook = RepairedPdfBook


if __name__ == "__main__":
    builder.main()
