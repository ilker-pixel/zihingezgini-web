#!/usr/bin/env python3
"""Fast integrity checks for generated Zihin Gezgini pages."""

from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []


class DocumentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title = ""
        self._inside_title = False
        self.links: list[str] = []
        self.canonical: list[str] = []
        self.descriptions: list[str] = []
        self.robots: list[str] = []
        self.schemas: list[str] = []
        self._schema_buffer: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "title":
            self._inside_title = True
        if tag in {"a", "img", "script", "link", "audio"}:
            value = values.get("href") or values.get("src")
            if value:
                self.links.append(value)
        if tag == "link" and values.get("rel") == "canonical" and values.get("href"):
            self.canonical.append(values["href"] or "")
        if tag == "meta" and values.get("name") == "description":
            self.descriptions.append(values.get("content") or "")
        if tag == "meta" and values.get("name") == "robots":
            self.robots.append(values.get("content") or "")
        if tag == "script" and values.get("type") == "application/ld+json":
            self._schema_buffer = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._inside_title = False
        if tag == "script" and self._schema_buffer is not None:
            self.schemas.append("".join(self._schema_buffer))
            self._schema_buffer = None

    def handle_data(self, data: str) -> None:
        if self._inside_title:
            self.title += data
        if self._schema_buffer is not None:
            self._schema_buffer.append(data)


def local_target_exists(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.scheme or parsed.netloc or url.startswith(("mailto:", "tel:", "data:")):
        return True
    path = parsed.path
    if not path or path == "/":
        return (ROOT / "index.html").exists()
    candidate = ROOT / path.lstrip("/")
    if path.endswith("/"):
        candidate /= "index.html"
    return candidate.exists()


def check_html(path: Path) -> None:
    parser = DocumentParser()
    try:
        parser.feed(path.read_text(encoding="utf-8"))
    except Exception as exc:
        ERRORS.append(f"{path.relative_to(ROOT)}: HTML parse error: {exc}")
        return
    relative = path.relative_to(ROOT)
    if relative != Path("index.html") and path.name == "index.html":
        if not parser.title.strip():
            ERRORS.append(f"{relative}: missing title")
        if len(parser.canonical) != 1:
            ERRORS.append(f"{relative}: expected one canonical URL, got {len(parser.canonical)}")
        if len(parser.descriptions) != 1 or not parser.descriptions[0].strip():
            ERRORS.append(f"{relative}: missing meta description")
    for schema in parser.schemas:
        try:
            json.loads(schema)
        except json.JSONDecodeError as exc:
            ERRORS.append(f"{relative}: invalid JSON-LD: {exc}")
    for link in parser.links:
        if link.startswith("#"):
            continue
        if not local_target_exists(link):
            ERRORS.append(f"{relative}: missing local target {link}")


def main() -> int:
    summary_files = sorted((ROOT / "data/summaries").glob("*.json"))
    summary_records = [json.loads(path.read_text(encoding="utf-8")) for path in summary_files]
    for path, summary in zip(summary_files, summary_records):
        sources = summary.get("sources") or []
        if not sources:
            ERRORS.append(f"{path.relative_to(ROOT)}: missing sources")
            continue
        if not any(re.match(r"^https?://", source.get("url", "")) for source in sources):
            ERRORS.append(f"{path.relative_to(ROOT)}: missing external source URL")

    generated_roots = [
        "yazilar", "zihin-odasi", "okuma-haritasi", "arastirma-arsivi",
        "arastirma", "kitap-ozetleri", "rastgele", "arama",
    ]
    html_files = [ROOT / "index.html", ROOT / "404.html"]
    for directory in generated_roots:
        html_files.extend((ROOT / directory).rglob("*.html"))
    for path in html_files:
        check_html(path)

    sitemap = ElementTree.parse(ROOT / "sitemap.xml")
    locations = [node.text or "" for node in sitemap.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
    if any("#" in location for location in locations):
        ERRORS.append("sitemap.xml contains fragment URLs")
    if len(locations) != len(set(locations)):
        ERRORS.append("sitemap.xml contains duplicate URLs")
    expected_url_count = 6 + len(json.loads((ROOT / "data/posts.json").read_text(encoding="utf-8")))
    expected_url_count += len(summary_records)
    expected_url_count += len(json.loads((ROOT / "data/kutuphane_index.json").read_text(encoding="utf-8")))
    if len(locations) != expected_url_count:
        ERRORS.append(f"sitemap.xml has {len(locations)} URLs; expected {expected_url_count}")
    try:
        ElementTree.parse(ROOT / "feed.xml")
    except ElementTree.ParseError as exc:
        ERRORS.append(f"feed.xml is invalid XML: {exc}")
    error_parser = DocumentParser()
    error_parser.feed((ROOT / "404.html").read_text(encoding="utf-8"))
    if not any("noindex" in value for value in error_parser.robots):
        ERRORS.append("404.html must be marked noindex")
    books = json.loads((ROOT / "data/books.json").read_text(encoding="utf-8"))
    expected_titles = {
        244: "Sapiens: Hayvanlardan Tanrılara",
        248: "Yapay Zekâ: Düşünen İnsanlar İçin Bir Rehber",
    }
    for book in books:
        if book.get("hasSummary") and not local_target_exists(book.get("summaryUrl", "")):
            ERRORS.append(f"book #{book.get('no')} has no valid summaryUrl")
        if book.get("no") in expected_titles and book.get("title") != expected_titles[book["no"]]:
            ERRORS.append(f"book #{book['no']} has an incomplete title")

    for summary in summary_records:
        pdf_url = summary.get("pdfUrl")
        if not pdf_url or not local_target_exists(pdf_url):
            ERRORS.append(f"summary #{summary.get('bookNo')} has no valid PDF download")

    search_index = json.loads((ROOT / "data/search-index.json").read_text(encoding="utf-8"))
    expected_search_count = len(summary_records)
    expected_search_count += len(json.loads((ROOT / "data/posts.json").read_text(encoding="utf-8")))
    expected_search_count += len(json.loads((ROOT / "data/kutuphane_index.json").read_text(encoding="utf-8")))
    if len(search_index) != expected_search_count:
        ERRORS.append(f"search index has {len(search_index)} records; expected {expected_search_count}")
    if {record.get("type") for record in search_index} != {"post", "summary", "research"}:
        ERRORS.append("search index does not contain all three content types")

    scoped_search_pages = {
        "yazilar/index.html": len(json.loads((ROOT / "data/posts.json").read_text(encoding="utf-8"))),
        "okuma-haritasi/index.html": len(json.loads((ROOT / "data/books.json").read_text(encoding="utf-8"))),
        "arastirma-arsivi/index.html": len(json.loads((ROOT / "data/kutuphane_index.json").read_text(encoding="utf-8"))),
    }
    for relative, expected_items in scoped_search_pages.items():
        source = (ROOT / relative).read_text(encoding="utf-8")
        item_count = len(re.findall(r"\bdata-section-search-item\b", source))
        if source.count("data-section-search-collection=") != 1:
            ERRORS.append(f"{relative}: expected one scoped search collection")
        if source.count("data-section-search data-search-scope=") != 1:
            ERRORS.append(f"{relative}: expected one scoped search panel")
        if item_count != expected_items:
            ERRORS.append(f"{relative}: search indexes {item_count} items; expected {expected_items}")

    if "YOUR_GOOGLE_VERIFICATION_TOKEN_HERE" in (ROOT / "index.html").read_text(encoding="utf-8"):
        ERRORS.append("index.html still contains the verification placeholder")
    if re.search(r"new Date\(\)\.getTime\(\)", (ROOT / "app.js").read_text(encoding="utf-8")):
        ERRORS.append("app.js still bypasses caches with timestamps")

    homepage = (ROOT / "index.html").read_text(encoding="utf-8")
    if homepage.count("<main") != 1:
        ERRORS.append(f"index.html must contain exactly one main landmark; found {homepage.count('<main')}")
    if homepage.count("<h1") != 1:
        ERRORS.append(f"index.html must contain exactly one h1; found {homepage.count('<h1')}")
    if "googletagmanager.com" in homepage or "fonts.googleapis.com" in homepage:
        ERRORS.append("index.html still contains a blocking analytics or remote-font request")

    roadmap = (ROOT / "okuma-haritasi/index.html").read_text(encoding="utf-8")
    required_roadmap_features = (
        "data-roadmap-filter=", "data-random-book", "data-export-progress",
        "data-import-progress", "data-roadmap-jump", "start-routes-grid",
    )
    for feature in required_roadmap_features:
        if feature not in roadmap:
            ERRORS.append(f"reading map is missing feature marker {feature}")

    for path in (ROOT / "kitap-ozetleri").glob("*/index.html"):
        source = path.read_text(encoding="utf-8")
        if "<strong>Derleyen:</strong>" in source or "<strong>Tarih:</strong>" in source:
            ERRORS.append(f"{path.relative_to(ROOT)} exposes disallowed editorial status metadata")
        for marker in ("data-reading-progress", "data-reader-resume", "data-reader-print", "data-reader-width"):
            if marker not in source:
                ERRORS.append(f"{path.relative_to(ROOT)} is missing reader feature {marker}")

    if ERRORS:
        print("Static site checks failed:")
        for error in ERRORS:
            print(f"- {error}")
        return 1
    print(f"Static site checks passed: {len(html_files)} HTML pages, {len(locations)} sitemap URLs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
