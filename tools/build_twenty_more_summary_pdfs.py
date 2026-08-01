#!/usr/bin/env python3
"""Build the second twenty illustrated summaries with the established renderer."""

from pathlib import Path

import build_five_summary_pdfs as builder
from pypdf import PdfReader


builder.BOOK_NUMBERS = (
    12, 17, 32, 41, 66,
    72, 93, 103, 122, 124,
    152, 156, 189, 194, 214,
    222, 241, 253, 271, 275,
)
builder.TMP = Path(__file__).resolve().parents[1] / "tmp" / "pdfs" / "twenty-more-summaries"


class DensePdfBook(builder.PdfBook):
    """Keep all 16 illustrated chapters while removing low-information divider pages."""

    def plan_total_pages(self) -> int:
        artwork_pages = len(self.chapter_art)
        note_pages = 0
        for chapters in self.grouped_sections().values():
            note_run = []
            for chapter in chapters:
                if chapter["id"] in self.chapter_art:
                    note_pages += len(self.note_groups(note_run))
                    note_run = []
                else:
                    note_run.append(chapter)
            note_pages += len(self.note_groups(note_run))
        return 3 + artwork_pages + note_pages + 3 + 1

    def make_styles(self):
        styles = super().make_styles()
        styles["body"].fontSize = 13.1
        styles["body"].leading = 19.0
        return styles

    def draw_bridge(self, stage: int, upcoming: list[dict]) -> None:
        self.begin_page()
        c = self.canvas
        labels = {
            1: ("BİRİNCİ DÖNEMEÇ", "İlk fikirlerden işleyen düzene", (
                "İlk dört durak kitabın temel sorusunu ve kullandığı ana merceği görünür hale getirdi. "
                "Şimdi yazarın bu mercekle olayları nasıl birbirine bağladığına geçiyoruz. Buradaki amaç yeni bir "
                "tanım ezberlemek değil; başlangıçta ayrı görünen parçaların aynı düzen içinde nasıl çalıştığını fark etmek."
            )),
            2: ("İKİNCİ DÖNEMEÇ", "Ayrıntıların içinden büyük resmi görmek", (
                "Yolun ortasında güçlü örneklerle karşılaştık; fakat tek bir çarpıcı sahne kitabın tamamı değildir. "
                "Bu bölümde örneklerin arkasındaki ortak ilişkiyi arayacağız. Bir başlık diğerini açıklıyor mu, yoksa "
                "ona sınır mı koyuyor? Okurken özellikle bu gerilimi izlemek, kolay sloganlardan daha sağlam bir kavrayış verir."
            )),
            3: ("ÜÇÜNCÜ DÖNEMEÇ", "Son virajda eleştiri ve bugünün soruları", (
                "Artık kitabın ana yapısı ayakta. Son dört görselli durakta bu yapının sınırlarını, kör noktalarını ve "
                "bugünkü hayata uzanan sonuçlarını göreceğiz. Güçlü bir kitabı ciddiye almak ona bütünüyle teslim olmak "
                "değildir; nerede aydınlattığını ve nerede başka bir merceğe ihtiyaç bıraktığını birlikte görmektir."
            )),
        }
        eyebrow, title, prose = labels[stage]
        c.setFillColor(self.ink)
        c.setFont("ZGArial-Bold", 9.5)
        c.drawString(23 * builder.mm, 263 * builder.mm, eyebrow)
        title_style = builder.ParagraphStyle(
            f"BridgeTitle{stage}", fontName="ZGArial-Bold", fontSize=23, leading=27,
            textColor=builder.BODY, alignment=builder.TA_LEFT,
        )
        y = builder.draw_rich(c, title, title_style, 23 * builder.mm, 251 * builder.mm, 164 * builder.mm)
        c.setStrokeColor(self.ink)
        c.setLineWidth(2)
        c.line(23 * builder.mm, y - 4 * builder.mm, 187 * builder.mm, y - 4 * builder.mm)

        art = self.chapter_art[upcoming[0]["id"]]
        art_path = builder.ROOT / art["image"].lstrip("/")
        image = builder.RLImage(str(self.pdf_asset(art_path)), width=72 * builder.mm, height=72 * builder.mm)
        image.drawOn(c, 115 * builder.mm, 139 * builder.mm)
        y = builder.draw_rich(c, prose, self.styles["body"], 23 * builder.mm, y - 13 * builder.mm, 82 * builder.mm)

        c.setFillColor(self.ink)
        c.setFont("ZGArial-Bold", 10)
        c.drawString(23 * builder.mm, 130 * builder.mm, "SIRADAKİ DÖRT DURAK")
        list_y = 120 * builder.mm
        item_style = builder.ParagraphStyle(
            f"BridgeItem{stage}", fontName="ZGArial", fontSize=11.2, leading=14.6,
            textColor=builder.BODY, alignment=builder.TA_LEFT,
        )
        for chapter in upcoming:
            c.setFillColor(self.ink)
            c.circle(25 * builder.mm, list_y + 1.5 * builder.mm, 1.1 * builder.mm, fill=1, stroke=0)
            list_y = builder.draw_rich(c, chapter["title"], item_style, 31 * builder.mm, list_y, 150 * builder.mm) - 4 * builder.mm

        question = (
            f"Okuma sorusu: '{upcoming[0]['title']}' ile '{upcoming[-1]['title']}' "
            "aynı düşünce yolunun hangi iki ucunda duruyor?"
        )
        question_style = builder.ParagraphStyle(
            f"BridgeQuestion{stage}", fontName="ZGArial-Italic", fontSize=11.2, leading=15.2,
            textColor=self.ink, alignment=builder.TA_LEFT,
        )
        builder.draw_rich(c, question, question_style, 23 * builder.mm, min(64 * builder.mm, list_y - 7 * builder.mm), 164 * builder.mm)
        self.end_page()

    def build(self) -> Path:
        self.draw_cover()
        self.draw_opening()
        self.draw_contents()
        chapter_numbers = {chapter["id"]: index for index, chapter in enumerate(self.summary["chapters"], 1)}
        art_seen = 0
        all_art_chapters = [
            chapter for chapter in self.summary["chapters"]
            if chapter["id"] in self.chapter_art
        ]
        for _section, chapters in self.grouped_sections().items():
            notes = []
            for chapter in chapters:
                if chapter["id"] in self.chapter_art:
                    if notes:
                        for pair in self.note_groups(notes):
                            self.draw_note_page(pair, chapter_numbers[pair[0]["id"]])
                        notes = []
                    self.draw_art_chapter(chapter, chapter_numbers[chapter["id"]])
                    art_seen += 1
                    if art_seen in (4, 8, 12):
                        self.draw_bridge(art_seen // 4, all_art_chapters[art_seen:art_seen + 4])
                else:
                    notes.append(chapter)
            if notes:
                for pair in self.note_groups(notes):
                    self.draw_note_page(pair, chapter_numbers[pair[0]["id"]])
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


builder.PdfBook = DensePdfBook


if __name__ == "__main__":
    builder.main()
