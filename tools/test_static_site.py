#!/usr/bin/env python3
"""Fast integrity checks for generated Zihin Gezgini pages."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree

from apply_reading_route import PHASES


ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []
EXPECTED_SUMMARY_URL_SHA256 = "213f31e9da8e02cde99e9093ea3d80c211b2e7298e02de2a18bcfbb47c53ee1f"


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
        self.unsafe_blank_targets: list[str] = []
        self._schema_buffer: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "title":
            self._inside_title = True
        if tag in {"a", "img", "script", "link", "audio"}:
            value = values.get("href") or values.get("src")
            if value:
                self.links.append(value)
        if tag == "a" and values.get("target") == "_blank":
            rel_values = (values.get("rel") or "").split()
            if "noopener" not in rel_values:
                self.unsafe_blank_targets.append(values.get("href") or "unknown link")
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
    for link in parser.unsafe_blank_targets:
        ERRORS.append(f"{relative}: target=_blank link lacks noopener: {link}")


def main() -> int:
    summary_files = sorted((ROOT / "data/summaries").glob("*.json"), key=lambda path: int(path.stem))
    summary_records = [json.loads(path.read_text(encoding="utf-8")) for path in summary_files]
    if len(summary_records) != 300:
        ERRORS.append(f"summary archive has {len(summary_records)} records; expected 300")
    for path, summary in zip(summary_files, summary_records):
        if int(path.stem) != int(summary.get("bookNo", 0)):
            ERRORS.append(f"{path.relative_to(ROOT)}: filename and stable bookNo do not match")
        sources = summary.get("sources") or []
        if len(sources) < 2:
            ERRORS.append(f"{path.relative_to(ROOT)}: has {len(sources)} sources; expected at least 2")
            continue
        if not any(re.match(r"^https?://", source.get("url", "")) for source in sources):
            ERRORS.append(f"{path.relative_to(ROOT)}: missing external source URL")
        meta = summary.get("meta", {})
        for field in ("compiler", "date"):
            if field in meta:
                ERRORS.append(f"{path.relative_to(ROOT)}: retains legacy meta.{field}")
        if any("extraParagraphs" in chapter for chapter in summary.get("chapters", [])):
            ERRORS.append(f"{path.relative_to(ROOT)}: retains generated extraParagraphs")

    generated_roots = [
        "yazilar", "zihin-odasi", "okuma-haritasi", "arastirma-arsivi",
        "arastirma", "kitap-ozetleri", "rastgele", "arama",
    ]
    html_files = [ROOT / "index.html", ROOT / "404.html"]
    for directory in generated_roots:
        html_files.extend((ROOT / directory).rglob("*.html"))
    if len(html_files) != 358:
        ERRORS.append(f"generated site has {len(html_files)} HTML pages; expected 358")
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
    if len(locations) != 356:
        ERRORS.append(f"sitemap.xml has {len(locations)} URLs; approved release expects 356")
    try:
        ElementTree.parse(ROOT / "feed.xml")
    except ElementTree.ParseError as exc:
        ERRORS.append(f"feed.xml is invalid XML: {exc}")
    error_parser = DocumentParser()
    error_parser.feed((ROOT / "404.html").read_text(encoding="utf-8"))
    if not any("noindex" in value for value in error_parser.robots):
        ERRORS.append("404.html must be marked noindex")
    books = json.loads((ROOT / "data/books.json").read_text(encoding="utf-8"))
    stable_ids = [book.get("no") for book in books]
    reading_orders = [book.get("readingOrder") for book in books]
    route_phases = [book.get("routePhase") for book in books]
    expected_positions = list(range(1, 301))
    if stable_ids != expected_positions:
        ERRORS.append("data/books.json must stay in stable book-id order 1..300")
    if sorted(reading_orders) != expected_positions:
        ERRORS.append("readingOrder must be a unique, complete permutation of 1..300")
    expected_route_phases = [((int(order) - 1) // 25) + 1 for order in reading_orders]
    if route_phases != expected_route_phases or Counter(route_phases) != Counter({phase: 25 for phase in range(1, 13)}):
        ERRORS.append("routePhase must define 12 consecutive phases of 25 route positions")
    summary_ids = [int(summary.get("bookNo", 0)) for summary in summary_records]
    if summary_ids != expected_positions:
        ERRORS.append("summary bookNo values must match stable ids 1..300")
    books_in_route_order = sorted(books, key=lambda book: int(book["readingOrder"]))
    approved_route = [book_no for phase in PHASES for book_no in phase]
    if [book["no"] for book in books_in_route_order] != approved_route:
        ERRORS.append("readingOrder does not match the approved pedagogical route manifest")
    books_by_no = {int(book["no"]): book for book in books}
    summary_urls = [str(book.get("summaryUrl", "")) for book in books]
    if len(set(summary_urls)) != 300 or any(not url.startswith("/kitap-ozetleri/") for url in summary_urls):
        ERRORS.append("book summaryUrl values must be 300 unique canonical guide paths")
    sitemap_urls = set(locations)
    if any(f"https://zihingezgini.net{url}" not in sitemap_urls for url in summary_urls):
        ERRORS.append("one or more canonical summaryUrl values are absent from sitemap.xml")
    url_contract = json.dumps(
        [(book["no"], book["summaryUrl"]) for book in books],
        ensure_ascii=False,
        separators=(",", ":"),
    )
    if hashlib.sha256(url_contract.encode("utf-8")).hexdigest() != EXPECTED_SUMMARY_URL_SHA256:
        ERRORS.append("the immutable bookNo-to-summaryUrl contract has changed")
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
    search_summaries = [record for record in search_index if record.get("type") == "summary"]
    if [record.get("readingOrder") for record in search_summaries] != expected_positions:
        ERRORS.append("search-index summary records are not in reading-route order")
    if [record.get("bookNo") for record in search_summaries] != [book["no"] for book in books_in_route_order]:
        ERRORS.append("search-index summary book ids do not match the reading route")

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
    for marker in ("home-entry", "Kişisel Yazılar", "300 AI Ön Okuma Rehberi", "Araştırma Arşivi", "mobile-section-nav", "data-mobile-menu-toggle"):
        if marker not in homepage:
            ERRORS.append(f"index.html is missing approved interface marker {marker}")
    if homepage.count('class="home-entry-card ') != 3:
        ERRORS.append("index.html must expose exactly three primary destination cards before the manifesto")
    entry_position = homepage.find('class="home-entry"')
    hero_position = homepage.find('class="home-hero"')
    if entry_position >= 0 and hero_position >= 0 and entry_position > hero_position:
        ERRORS.append("the three primary destinations must appear before the homepage manifesto")

    roadmap = (ROOT / "okuma-haritasi/index.html").read_text(encoding="utf-8")
    if "mobile-section-nav" not in roadmap or "300 Rehber" not in roadmap:
        ERRORS.append("static pages must expose the three primary mobile destinations")
    methodology = (
        "Bu bölüm, kitapları okumadan önce temel fikirlerine hazırlanmak için yapay zekâya hazırlattığım "
        "300 ön okuma rehberinden oluşuyor."
    )
    if methodology not in roadmap:
        ERRORS.append("reading map is missing the collection-level AI methodology statement")
    required_roadmap_features = (
        "data-roadmap-filter=", "data-random-book", "data-export-progress",
        "data-import-progress", "data-roadmap-jump", "start-routes-grid",
        "data-roadmap-continue", "data-roadmap-advanced", "data-phase-progress",
    )
    for feature in required_roadmap_features:
        if feature not in roadmap:
            ERRORS.append(f"reading map is missing feature marker {feature}")
    roadmap_rows = [
        (int(book_no), int(position))
        for book_no, position in re.findall(
            r'data-book-no="(\d+)" data-reading-order="(\d+)"',
            roadmap,
        )
    ]
    if [position for _, position in roadmap_rows] != expected_positions:
        ERRORS.append("reading map DOM is not in readingOrder 1..300")
    if [book_no for book_no, _ in roadmap_rows] != [book["no"] for book in books_in_route_order]:
        ERRORS.append("reading map DOM stable ids do not match the approved route")
    if roadmap.count('class="roadmap-phase"') != 12:
        ERRORS.append("reading map must render exactly 12 route phases")
    if roadmap.count('class="book-check-col"') != 300:
        ERRORS.append("reading map must render 300 label-sized read controls")
    if roadmap.count('class="book-route-meta"') != 300:
        ERRORS.append("reading map must render route and stable identity metadata for 300 books")

    for path in (ROOT / "kitap-ozetleri").glob("*/index.html"):
        source = path.read_text(encoding="utf-8")
        stable_id_match = re.search(r'data-summary-book="(\d+)"', source)
        if not stable_id_match:
            ERRORS.append(f"{path.relative_to(ROOT)} is missing its stable book id")
        else:
            stable_id = int(stable_id_match.group(1))
            expected_path = Path(books_by_no[stable_id]["summaryUrl"].strip("/")) / "index.html"
            if path.relative_to(ROOT) != expected_path:
                ERRORS.append(f"{path.relative_to(ROOT)} does not match book #{stable_id} summaryUrl")
            expected_canonical = f'<link rel="canonical" href="https://zihingezgini.net{books_by_no[stable_id]["summaryUrl"]}">'
            if expected_canonical not in source:
                ERRORS.append(f"{path.relative_to(ROOT)} does not use its stable summaryUrl as canonical")
        forbidden_status_copy = ("<strong>Derleyen:</strong>", "<strong>Tarih:</strong>", "Editoryal durum", "Bende kalan", "Bu kitap şuna bağlanıyor")
        if any(marker in source for marker in forbidden_status_copy):
            ERRORS.append(f"{path.relative_to(ROOT)} exposes disallowed per-book editorial status copy")
        for marker in (
            "data-reading-progress", "data-reader-resume", "data-reader-print", "data-reader-width",
            "data-summary-reading-order", "summary-route-navigation", "Haritaya dön",
            "Yapay zekâyla oluşturulmuş ön okuma rehberi", "data-summary-read-toggle",
            "Kitabın yerini tutmaz", 'class="summary-reader-more" open',
            "data-summary-reading-minutes", "data-summary-toc-status",
        ):
            if marker not in source:
                ERRORS.append(f"{path.relative_to(ROOT)} is missing reader feature {marker}")

    about = (ROOT / "zihin-odasi/index.html").read_text(encoding="utf-8")
    if "Kişisel yazılar" not in about or "bütünüyle yapay zekâ tarafından oluşturuldu" not in about:
        ERRORS.append("about page does not clearly separate personal work from the AI reading collection")

    grouped_toc = (ROOT / "kitap-ozetleri/13-buyuk-tarih/index.html").read_text(encoding="utf-8")
    if grouped_toc.count('class="summary-toc-group"') < 5:
        ERRORS.append("long guides must render a grouped, two-level table of contents")

    search_page = (ROOT / "arama/index.html").read_text(encoding="utf-8")
    if "300 ön okuma rehberini" not in search_page or search_page.count("data-global-search-type=") != 4:
        ERRORS.append("global search is missing canonical guide terminology or collection shortcuts")

    admin_parser = DocumentParser()
    admin_parser.feed((ROOT / "admin/index.html").read_text(encoding="utf-8"))
    if not any("noindex" in value and "nofollow" in value for value in admin_parser.robots):
        ERRORS.append("admin/index.html must be marked noindex and nofollow")
    admin_script = (ROOT / "admin/admin.js").read_text(encoding="utf-8")
    if "sessionStorage.setItem" not in admin_script:
        ERRORS.append("admin token is not stored in sessionStorage")
    if "localStorage.setItem" in admin_script:
        ERRORS.append("admin script still persists configuration in localStorage")

    if ERRORS:
        print("Static site checks failed:")
        for error in ERRORS:
            print(f"- {error}")
        return 1
    print(f"Static site checks passed: {len(html_files)} HTML pages, {len(locations)} sitemap URLs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
