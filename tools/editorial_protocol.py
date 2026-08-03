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
STOCK_SENTENCE_THRESHOLD = 100

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


def sentences(value: str) -> list[str]:
    return [item.strip() for item in re.split(r"(?<=[.!?])\s+", normalize(value)) if item.strip()]


def summary_sentence_counts(records: list[dict]) -> collections.Counter[str]:
    counts: collections.Counter[str] = collections.Counter()
    for summary in records:
        for chapter in summary.get("chapters", []):
            for paragraph in chapter.get("paragraphs", []) + chapter.get("extraParagraphs", []):
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


def clean_summary_scaffolding() -> tuple[int, int]:
    paths = sorted(SUMMARY_DIR.glob("*.json"), key=lambda path: int(path.stem))
    records = [load(path) for path in paths]
    counts = summary_sentence_counts(records)
    stock = {sentence for sentence, count in counts.items() if count >= STOCK_SENTENCE_THRESHOLD}
    removed = 0
    changed_files = 0
    for path, summary in zip(paths, records):
        changed = False
        for chapter in summary.get("chapters", []):
            for field in ("paragraphs", "extraParagraphs"):
                cleaned = []
                for paragraph in chapter.get(field, []):
                    kept = [sentence for sentence in sentences(paragraph) if sentence not in stock]
                    removed += len(sentences(paragraph)) - len(kept)
                    if kept:
                        cleaned.append(" ".join(kept))
                if cleaned != chapter.get(field, []):
                    chapter[field] = cleaned
                    changed = True
        if changed:
            save(path, summary)
            changed_files += 1
    return changed_files, removed


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
        summary_files, sentences_removed = clean_summary_scaffolding()
        research_files, quotes_removed, sections_removed = clean_research_repetition()
        print(
            f"Editorial cleanup: {map_changes} map descriptions, {sentences_removed} stock sentences in "
            f"{summary_files} summaries, {quotes_removed} duplicate quotes and {sections_removed} repeated sections "
            f"in {research_files} research files."
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
