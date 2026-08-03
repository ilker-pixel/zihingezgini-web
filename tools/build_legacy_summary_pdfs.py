#!/usr/bin/env python3
"""Build polished PDFs for the five original summaries that lacked downloads."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer


ROOT = Path(__file__).resolve().parents[1]
BOOKS = {
    1: "1-zamanin-kisa-tarihi-ozeti.pdf",
    3: "3-fizik-uzerine-yedi-kisa-ders-ozeti.pdf",
    4: "4-evrenin-dokusu-ozeti.pdf",
    5: "5-kaos-yeni-bir-bilim-teorisi-ozeti.pdf",
    6: "6-sarhos-yuruyusu-ozeti.pdf",
}
PAPER = colors.HexColor("#F4F0E6")
INK = colors.HexColor("#28231E")
MUTED = colors.HexColor("#5F584F")
ACCENT = colors.HexColor("#8B5B38")
RULE = colors.HexColor("#D4CEC0")


def register_fonts() -> None:
    base = Path("/System/Library/Fonts/Supplemental")
    pdfmetrics.registerFont(TTFont("ZGArial", str(base / "Arial.ttf")))
    pdfmetrics.registerFont(TTFont("ZGArial-Bold", str(base / "Arial Bold.ttf")))
    pdfmetrics.registerFont(TTFont("ZGArial-Italic", str(base / "Arial Italic.ttf")))


def markup(value: str) -> str:
    value = html.escape(value or "")
    value = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", value)
    value = re.sub(r"\*(.+?)\*", r"<i>\1</i>", value)
    return value.replace("\n", "<br/>")


def styles():
    base = getSampleStyleSheet()
    return {
        "cover_kicker": ParagraphStyle("CoverKicker", parent=base["Normal"], fontName="ZGArial-Bold", fontSize=10, leading=14, textColor=ACCENT, spaceAfter=10),
        "cover_title": ParagraphStyle("CoverTitle", parent=base["Title"], fontName="ZGArial-Bold", fontSize=30, leading=34, textColor=INK, alignment=TA_LEFT, spaceAfter=10),
        "cover_author": ParagraphStyle("CoverAuthor", parent=base["Normal"], fontName="ZGArial", fontSize=13, leading=18, textColor=MUTED, spaceAfter=18),
        "intro": ParagraphStyle("Intro", parent=base["BodyText"], fontName="ZGArial", fontSize=11.5, leading=17, textColor=INK, alignment=TA_JUSTIFY, spaceAfter=10),
        "chapter_no": ParagraphStyle("ChapterNo", parent=base["Normal"], fontName="ZGArial-Bold", fontSize=9, leading=12, textColor=ACCENT, spaceAfter=8),
        "chapter": ParagraphStyle("Chapter", parent=base["Heading1"], fontName="ZGArial-Bold", fontSize=22, leading=26, textColor=INK, spaceAfter=15),
        "body": ParagraphStyle("Body", parent=base["BodyText"], fontName="ZGArial", fontSize=11.2, leading=17, textColor=INK, alignment=TA_JUSTIFY, spaceAfter=10, splitLongWords=False),
        "toc": ParagraphStyle("Toc", parent=base["Normal"], fontName="ZGArial", fontSize=10.5, leading=15, textColor=INK, spaceAfter=4),
        "source": ParagraphStyle("Source", parent=base["Normal"], fontName="ZGArial", fontSize=9.2, leading=13, textColor=MUTED, spaceAfter=6),
        "note": ParagraphStyle("Note", parent=base["Normal"], fontName="ZGArial-Italic", fontSize=9.2, leading=14, textColor=MUTED, spaceBefore=14),
    }


def decorate_page(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    if doc.page > 1:
        canvas.setStrokeColor(RULE)
        canvas.line(20 * mm, 15 * mm, A4[0] - 20 * mm, 15 * mm)
        canvas.setFont("ZGArial", 8)
        canvas.setFillColor(MUTED)
        canvas.drawString(20 * mm, 10 * mm, "ZİHİN GEZGİNİ · OKUMA REHBERİ")
        canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, str(doc.page))
    canvas.restoreState()


def build_pdf(summary: dict, filename: str) -> Path:
    output = ROOT / "data" / "pdfs" / filename
    output.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(output), pagesize=A4, rightMargin=22 * mm, leftMargin=22 * mm,
        topMargin=22 * mm, bottomMargin=22 * mm,
        title=f"{summary['title']} Özeti", author="Zihin Gezgini",
    )
    style = styles()
    story = [Spacer(1, 11 * mm), Paragraph("ZİHİN GEZGİNİ · OKUMA REHBERİ", style["cover_kicker"])]
    cover = ROOT / summary.get("coverImage", "").lstrip("/")
    if cover.is_file():
        story.extend([Image(str(cover), width=62 * mm, height=62 * mm, kind="proportional"), Spacer(1, 10 * mm)])
    story.extend([
        Paragraph(markup(summary["title"]), style["cover_title"]),
        Paragraph(markup(summary.get("author", "")), style["cover_author"]),
        Paragraph("Özgün eserin yerini tutmayan, kavramları tanımaya ve asıl okumaya hazırlanmaya yönelik bağımsız rehber.", style["note"]),
        PageBreak(),
        Paragraph("Okumaya başlamadan önce", style["chapter"]),
        Paragraph(markup(summary.get("intro", "")), style["intro"]),
        PageBreak(),
        Paragraph("İçindekiler", style["chapter"]),
    ])
    for index, chapter in enumerate(summary.get("chapters", []), 1):
        story.append(Paragraph(f"{index:02d} · {markup(chapter.get('title', ''))}", style["toc"]))
    for index, chapter in enumerate(summary.get("chapters", []), 1):
        story.extend([
            PageBreak(),
            Paragraph(f"BÖLÜM {index:02d}", style["chapter_no"]),
            Paragraph(markup(chapter.get("title", "")), style["chapter"]),
        ])
        for paragraph in chapter.get("paragraphs", []) + chapter.get("extraParagraphs", []):
            story.append(Paragraph(markup(paragraph), style["body"]))
        takeaway = chapter.get("takeaway")
        if takeaway:
            story.append(Paragraph(f"Bölümün özü: {markup(takeaway)}", style["note"]))
    sources = summary.get("sources", [])
    if sources:
        story.extend([PageBreak(), Paragraph("Kaynaklar ve ileri okumalar", style["chapter"])])
        for source in sources:
            story.append(Paragraph(f"[{source.get('id')}] {markup(source.get('title', ''))}<br/><link href=\"{html.escape(source.get('url', ''), quote=True)}\">{html.escape(source.get('url', ''))}</link>", style["source"]))
    story.extend([Spacer(1, 8 * mm), Paragraph("Bu bağımsız ve ticari olmayan okuma rehberi eğitim ve araştırma amacıyla hazırlanmıştır; özgün eserin yerini tutmaz.", style["note"])])
    doc.build(story, onFirstPage=decorate_page, onLaterPages=decorate_page)
    reader = PdfReader(str(output))
    if len(reader.pages) < 8:
        raise RuntimeError(f"Unexpectedly short PDF for book {summary['bookNo']}: {len(reader.pages)} pages")
    if summary["title"] not in (reader.pages[0].extract_text() or ""):
        raise RuntimeError(f"Cover title missing in PDF for book {summary['bookNo']}")
    return output


def main() -> int:
    register_fonts()
    for number, filename in BOOKS.items():
        path = ROOT / "data" / "summaries" / f"{number}.json"
        summary = json.loads(path.read_text(encoding="utf-8"))
        summary["pdfUrl"] = f"/data/pdfs/{filename}"
        summary["pdfLabel"] = "PDF okuma rehberini indir"
        summary["longForm"] = True
        path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        output = build_pdf(summary, filename)
        pages = len(PdfReader(str(output)).pages)
        print(f"Built #{number}: {output.name} ({pages} pages)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
