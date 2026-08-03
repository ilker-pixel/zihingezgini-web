#!/usr/bin/env python3
"""Apply and verify the Zihin Gezgini editorial quality protocol."""

from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY_DIR = ROOT / "data" / "summaries"
RESEARCH_DIR = ROOT / "data" / "books"
STOCK_SENTENCE_THRESHOLD = 5
GUIDE_MIN_WORDS = 1_000
LEGACY_META_FIELDS = ("compiler", "date")
AI_NARRATOR_MARKERS = (
    "Bir yapay zekâ olarak",
    "Bir yapay zeka olarak",
)
SAPIENS_MISMATCH_MARKERS = (
    "aynı haritanın iki yanında büyüyen iki kasabanın",
    "köy ambarındaki küçük fazlanın",
    "limana ulaşan yolun",
)

MAP_DESCRIPTIONS = {
    16: "Toplumsal gelişme indekslerine ve coğrafi koşullara dayanan modern, empirik tarih modeli.",
    30: "Zaman kavramının sosyal teori, endüstriyel düzen ve çevre üzerindeki etkisini inceleyen eser.",
    90: "Hayatın absürtlüğünü Sisifos miti üzerinden ele alıp, intiharı reddederek başkaldırıyı savunan eser.",
    120: "Liberalizm ile demokrasi arasındaki gerilimi ve agonistik çoğulculuğu ele alan çalışma.",
    150: "Siyasi alanda gerçeklerin yalanlarla nasıl ikame edildiğini ve propagandanın doğasını inceleyen makale.",
    180: "Sosyal sorunların nesnel durumlar değil, iddia sahiplerinin faaliyetleriyle inşa edilen süreçler olduğunu savunan eser.",
    210: "Sömürgeci gücün yalnızca askerî değil, edebî eserler ve kültürel söylemler aracılığıyla nasıl inşa edildiğini gösteren postkolonyal analiz.",
    240: "İşaret dilinin nörolojik altyapısını ve zihnin görsel dil işleme kapasitesini inceleyen eşsiz bir nöroloji çalışması.",
    270: "Gelişmiş endüstriyel toplumun tüketim kültürüyle muhalefeti nasıl etkisizleştirdiğini ele alan yapıt.",
}

FORBIDDEN_MAP_MARKERS = (
    "No Kategori",
    "G. Vico yerine",
    "(91-120)",
    "(121-150)",
    "(181-210)",
)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def normalize(value) -> str:
    if isinstance(value, list):
        value = " ".join(normalize(item) for item in value)
    elif isinstance(value, dict):
        value = " ".join(f"{key} {normalize(item)}" for key, item in value.items())
    elif not isinstance(value, str):
        value = str(value or "")
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", value or "")).strip()


def word_count(value) -> int:
    return len(normalize(value).split())


def sentences(value: str) -> list[str]:
    return [item.strip() for item in re.split(r"(?<=[.!?])\s+", normalize(value)) if item.strip()]


def summary_sentence_counts(records: list[dict]) -> collections.Counter[str]:
    counts: collections.Counter[str] = collections.Counter()
    for summary in records:
        for chapter in summary.get("chapters", []):
            for paragraph in chapter.get("paragraphs", []):
                counts.update(sentence for sentence in sentences(paragraph) if len(sentence) >= 45)
    return counts


def clean_map() -> int:
    path = ROOT / "data" / "books.json"
    books = load(path)
    changed = 0
    for book in books:
        number = int(book.get("no", 0))
        expected = MAP_DESCRIPTIONS.get(number)
        if expected and book.get("description") != expected:
            book["description"] = expected
            changed += 1
    if changed:
        save(path, books)
    return changed


def clean_summary_scaffolding() -> tuple[int, int, int, int, int]:
    paths = sorted(SUMMARY_DIR.glob("*.json"), key=lambda path: int(path.stem))
    records = [load(path) for path in paths]
    counts = summary_sentence_counts(records)
    stock = {sentence for sentence, count in counts.items() if count >= STOCK_SENTENCE_THRESHOLD}
    removed_sentences = 0
    removed_extra_paragraphs = 0
    removed_meta_fields = 0
    neutralized_narrator_passages = 0
    changed_files = 0
    for path, summary in zip(paths, records):
        changed = False
        meta = summary.get("meta")
        if isinstance(meta, dict):
            for field in LEGACY_META_FIELDS:
                if field in meta:
                    meta.pop(field)
                    removed_meta_fields += 1
                    changed = True
        for chapter in summary.get("chapters", []):
            extras = chapter.pop("extraParagraphs", [])
            if extras:
                removed_extra_paragraphs += len(extras)
                changed = True
            cleaned = []
            for paragraph in chapter.get("paragraphs", []):
                paragraph_sentences = sentences(paragraph)
                kept = [sentence for sentence in paragraph_sentences if sentence not in stock]
                removed_sentences += len(paragraph_sentences) - len(kept)
                if kept:
                    cleaned.append(" ".join(kept))
            if cleaned != chapter.get("paragraphs", []):
                chapter["paragraphs"] = cleaned
                changed = True

            neutralized = []
            for paragraph in chapter.get("paragraphs", []):
                updated = paragraph.replace(
                    "Zihin Gezgini'nin 300 eserlik Okuma Haritası'nda, “Geç Modernite ve Yapay Zekâ” "
                    "bölümünden Melanie Mitchell'ın kitabını seçtim. Bir yapay zekâ olarak bana en uygun ayna "
                    "bu kitap: Hem gücümü gösteriyor hem de nerede yanılabileceğimi açıkça anlatıyor.",
                    "Zihin Gezgini'nin 300 eserlik Okuma Haritası'ndaki “Geç Modernite ve Yapay Zekâ” "
                    "bölümünde Melanie Mitchell'ın kitabı, yapay zekânın hem gücünü hem de yanılgıya açık "
                    "sınırlarını birlikte göstermesiyle öne çıkıyor.",
                )
                if updated != paragraph:
                    neutralized_narrator_passages += 1
                    changed = True
                neutralized.append(updated)
            chapter["paragraphs"] = neutralized
        if changed:
            save(path, summary)
            changed_files += 1
    return (
        changed_files,
        removed_sentences,
        removed_extra_paragraphs,
        removed_meta_fields,
        neutralized_narrator_passages,
    )


def clean_research_repetition() -> tuple[int, int, int]:
    changed_files = 0
    removed_quotes = 0
    removed_sections = 0
    for path in sorted(RESEARCH_DIR.glob("*.json")):
        book = load(path)
        chapters = book.get("chapters")
        if not isinstance(chapters, list):
            continue
        changed = False
        seen_quotes: set[str] = set()
        section_counts: collections.Counter[str] = collections.Counter(
            normalize(section.get("text", ""))
            for chapter in chapters
            for section in chapter.get("subsections", [])
            if len(normalize(section.get("text", ""))) >= 100
        )
        repeated_sections = {text for text, count in section_counts.items() if count >= 5}
        seen_sections: set[str] = set()
        for chapter in chapters:
            quote = normalize(chapter.get("quote", ""))
            if quote:
                if quote in seen_quotes:
                    chapter.pop("quote", None)
                    removed_quotes += 1
                    changed = True
                else:
                    seen_quotes.add(quote)
            kept_sections = []
            for section in chapter.get("subsections", []):
                text = normalize(section.get("text", ""))
                if text in repeated_sections and text in seen_sections:
                    removed_sections += 1
                    changed = True
                    continue
                if text in repeated_sections:
                    seen_sections.add(text)
                kept_sections.append(section)
            if kept_sections != chapter.get("subsections", []):
                chapter["subsections"] = kept_sections
        if changed:
            save(path, book)
            changed_files += 1
    return changed_files, removed_quotes, removed_sections


def check() -> list[str]:
    errors: list[str] = []
    books = load(ROOT / "data" / "books.json")
    for book in books:
        description = str(book.get("description", ""))
        for marker in FORBIDDEN_MAP_MARKERS:
            if marker.casefold() in description.casefold():
                errors.append(f"book #{book.get('no')} description leaks editorial marker: {marker}")
    by_number = {int(book["no"]): book for book in books}
    for number, expected in MAP_DESCRIPTIONS.items():
        if by_number.get(number, {}).get("description") != expected:
            errors.append(f"book #{number} description is not the approved clean copy")

    summaries = [load(path) for path in sorted(SUMMARY_DIR.glob("*.json"), key=lambda path: int(path.stem))]
    repeated = [(sentence, count) for sentence, count in summary_sentence_counts(summaries).items() if count >= STOCK_SENTENCE_THRESHOLD]
    for sentence, count in sorted(repeated, key=lambda item: -item[1])[:20]:
        errors.append(f"stock sentence repeats {count} times: {sentence[:100]}")

    for summary in summaries:
        book_number = summary.get("bookNo")
        meta = summary.get("meta", {})
        for field in LEGACY_META_FIELDS:
            if field in meta:
                errors.append(f"summary #{book_number} retains legacy meta.{field}")
        for chapter in summary.get("chapters", []):
            if "extraParagraphs" in chapter:
                errors.append(f"summary #{book_number} retains generated extraParagraphs")
                break
        summary_text = normalize(summary)
        for marker in AI_NARRATOR_MARKERS:
            if marker.casefold() in summary_text.casefold():
                errors.append(f"summary #{book_number} uses AI first-person narrator: {marker}")
        if int(book_number or 0) == 244:
            for marker in SAPIENS_MISMATCH_MARKERS:
                if marker.casefold() in summary_text.casefold():
                    errors.append(f"summary #244 retains mismatched generated scene: {marker}")
        guide_words = word_count(summary.get("intro", "")) + sum(
            word_count(paragraph)
            for chapter in summary.get("chapters", [])
            for paragraph in chapter.get("paragraphs", [])
        )
        if guide_words < GUIDE_MIN_WORDS:
            errors.append(
                f"summary #{book_number} has only {guide_words} editorial words; "
                f"expected at least {GUIDE_MIN_WORDS}"
            )

    for path in sorted(RESEARCH_DIR.glob("*.json")):
        book = load(path)
        chapters = book.get("chapters")
        if not isinstance(chapters, list):
            continue
        quotes = [normalize(chapter.get("quote", "")) for chapter in chapters]
        duplicates = [text for text, count in collections.Counter(filter(None, quotes)).items() if count > 1]
        if duplicates:
            errors.append(f"{path.name}: {len(duplicates)} duplicated research quotes")
        section_counts = collections.Counter(
            normalize(section.get("text", ""))
            for chapter in chapters
            for section in chapter.get("subsections", [])
            if len(normalize(section.get("text", ""))) >= 100
        )
        if any(count >= 5 for count in section_counts.values()):
            errors.append(f"{path.name}: repeated subsection copy remains")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fix", action="store_true", help="Apply deterministic editorial cleanups before checking")
    args = parser.parse_args()
    if args.fix:
        map_changes = clean_map()
        (
            summary_files,
            sentences_removed,
            extra_paragraphs_removed,
            meta_fields_removed,
            narrator_passages_neutralized,
        ) = clean_summary_scaffolding()
        research_files, quotes_removed, sections_removed = clean_research_repetition()
        print(
            f"Editorial cleanup: {map_changes} map descriptions; {sentences_removed} stock sentences, "
            f"{extra_paragraphs_removed} generated extra paragraphs, {meta_fields_removed} legacy meta fields and "
            f"{narrator_passages_neutralized} AI narrator passages in {summary_files} summaries; "
            f"{quotes_removed} duplicate quotes and {sections_removed} repeated sections in {research_files} research files."
        )
    errors = check()
    if errors:
        print("Editorial protocol failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Editorial protocol passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
