#!/usr/bin/env python3
"""Generate crawlable HTML pages from the Zihin Gezgini JSON archive.

The current homepage remains a lightweight interactive application. This build
step creates real, canonical URLs for every substantive item so search engines,
social previews and no-JavaScript visitors receive the complete content.
"""

from __future__ import annotations

import html
import json
import math
import re
import shutil
import unicodedata
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape as xml_escape


ROOT = Path(__file__).resolve().parents[1]
SITE_URL = "https://zihingezgini.net"
GENERATED_DIRS = (
    "yazilar",
    "zihin-odasi",
    "okuma-haritasi",
    "arastirma-arsivi",
    "arastirma",
    "kitap-ozetleri",
    "rastgele",
    "arama",
)

EVRE_TITLES = {
    1: "Temeller: Evren, Doğa ve Canlılık",
    2: "Zihin ve Benlik",
    3: "Karakter ve İyi Yaşam",
    4: "Toplum ve Sözleşme",
    5: "Hakikat ve Yöntem",
    6: "Ekonomi Politik ve Sınıf",
    7: "Dil ve Anlamlandırma",
    8: "Görsel Kültür, Estetik ve Kimlik",
    9: "Geç Modernite ve Yapay Zekâ",
    10: "Sentezler ve Bütünsel Felsefe",
}

MONTHS_TR = (
    "",
    "Ocak",
    "Şubat",
    "Mart",
    "Nisan",
    "Mayıs",
    "Haziran",
    "Temmuz",
    "Ağustos",
    "Eylül",
    "Ekim",
    "Kasım",
    "Aralık",
)

START_ROUTES = (
    ("Evreni anlamak", "Fizikten kozmolojiye sağlam bir başlangıç.", (1, 2, 3, 4, 5)),
    ("Zihin ve benlik", "Bilinç, karar ve benlik duygusunu izleyen rota.", (31, 36, 39, 42, 49)),
    ("İyi yaşam", "Karakter, anlam ve gündelik hayat üzerine beş durak.", (60, 61, 63, 68, 70)),
    ("Toplum ve iktidar", "Sözleşmeden modern devlete uzanan düşünce çizgisi.", (93, 100, 107, 108, 115)),
    ("Teknoloji ve gelecek", "Geç modernite ve yapay zekâ üzerine başlangıç rotası.", (243, 248, 253, 254, 259)),
)


def load_json(relative_path: str) -> Any:
    with (ROOT / relative_path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def strip_html(value: str) -> str:
    value = re.sub(r"<script\b[^>]*>.*?</script>", " ", value or "", flags=re.I | re.S)
    value = re.sub(r"<style\b[^>]*>.*?</style>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def excerpt(value: str, limit: int = 158) -> str:
    clean = strip_html(value)
    if len(clean) <= limit:
        return clean
    shortened = clean[: limit + 1].rsplit(" ", 1)[0]
    return shortened.rstrip(".,;:–—-") + "…"


def slugify(value: str) -> str:
    table = str.maketrans({
        "ç": "c", "Ç": "c", "ğ": "g", "Ğ": "g", "ı": "i", "İ": "i",
        "ö": "o", "Ö": "o", "ş": "s", "Ş": "s", "ü": "u", "Ü": "u",
    })
    value = unicodedata.normalize("NFKD", value.translate(table))
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return value or "icerik"


def date_iso(value: str) -> str:
    return (value or "")[:10]


def date_tr(value: str) -> str:
    try:
        parsed = datetime.fromisoformat(value)
        return f"{parsed.day} {MONTHS_TR[parsed.month]} {parsed.year}"
    except (TypeError, ValueError):
        return value or ""


def absolute_asset(value: str | None, fallback: str = "/images/thinking_man_sketch.png") -> str:
    asset = value or fallback
    if asset.startswith("http://") or asset.startswith("https://"):
        return asset
    return f"{SITE_URL}/{asset.lstrip('/')}"


def display_asset(value: str | None, fallback: str = "/images/thinking_man_sketch.png") -> str:
    """Use a bounded WebP display copy while retaining the source for social metadata."""
    asset = value or fallback
    if not asset.startswith("/images/"):
        return asset
    relative = Path(asset.removeprefix("/images/"))
    candidate = Path("images/optimized") / relative.parent / f"{relative.stem}-960.webp"
    if (ROOT / candidate).exists():
        return "/" + candidate.as_posix()
    return asset


def summary_path(summary: dict[str, Any]) -> str:
    return f"/kitap-ozetleri/{summary['bookNo']}-{slugify(summary['title'])}/"


def write_file(relative_path: str | Path, content: str) -> None:
    target = ROOT / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    normalized = "\n".join(line.rstrip() for line in content.splitlines())
    target.write_text(normalized.rstrip() + "\n", encoding="utf-8")


def header(active: str = "") -> str:
    links = (
        ("home", "/", "Başlangıç"),
        ("roadmap", "/okuma-haritasi/", "Okuma Haritası"),
        ("library", "/arastirma-arsivi/", "Araştırma Arşivi"),
        ("about", "/zihin-odasi/", "Zihin Odası"),
        ("search", "/arama/", "Arama"),
    )
    nav = "".join(
        f'<a href="{href}" class="nav-link{" active" if key == active else ""}">{label}</a>'
        for key, href, label in links
    )
    return f"""
    <header class="site-header">
      <div class="header-inner">
        <a href="/" class="logo-link" aria-label="Zihin Gezgini kişisel düşünce arşivi ana sayfası">
          <img src="/images/optimized/zihin_gezgini_logo_sketch-960.webp" class="header-logo" width="72" height="72" alt="">
          <span class="brand-copy">
            <span class="brand-kicker">Kişisel düşünce arşivi</span>
            <span class="site-title">Zihin Gezgini</span>
          </span>
        </a>
        <nav class="site-nav" aria-label="Ana menü">
          {nav}
          <a href="/rastgele/" class="nav-link nav-link-random">Rastgele ↝</a>
          <button type="button" class="theme-toggle-btn" data-theme-toggle title="Temayı değiştir" aria-label="Temayı değiştir">◐</button>
        </nav>
      </div>
    </header>"""


def footer() -> str:
    return """
    <footer class="site-footer">
      <div class="footer-inner">
        <div class="footer-socials">
          <a href="https://www.youtube.com/@Zihin_Gezgini" target="_blank" rel="noopener">YouTube</a>
          <a href="https://zihingezgini.substack.com" target="_blank" rel="noopener">Substack</a>
          <a href="https://open.spotify.com/show/3PLOqIu8IrkzFu30aA6cQB" target="_blank" rel="noopener">Spotify</a>
          <a href="https://podcasts.apple.com/tr/podcast/zihin-gezgini/id1812203751" target="_blank" rel="noopener">Apple Podcasts</a>
          <a href="https://instagram.com/zihin_gezgini" target="_blank" rel="noopener">Instagram</a>
        </div>
        <p>Zihin Gezgini · İlker Manavoğlu'nun kişisel düşünce arşivi.</p>
        <p class="footer-sub">Analog düşünceler, dijital kâğıt üzerine.</p>
      </div>
    </footer>"""


def page_shell(
    *,
    title: str,
    description: str,
    path: str,
    content: str,
    active: str = "",
    image: str | None = None,
    schema: dict[str, Any] | list[dict[str, Any]] | None = None,
    page_type: str = "website",
    body_class: str = "",
    noindex: bool = False,
    static_css_version: int = 3,
    static_js_version: int = 2,
) -> str:
    canonical = f"{SITE_URL}{path}"
    image_url = absolute_asset(image)
    schema_html = ""
    if schema:
        schema_json = json.dumps(schema, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
        schema_html = f'<script type="application/ld+json">{schema_json}</script>'
    robots_html = '<meta name="robots" content="noindex,follow">' if noindex else ""
    return f"""<!DOCTYPE html>
<html lang="tr" class="light-theme">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description, quote=True)}">
  <meta name="author" content="İlker Manavoğlu">
  {robots_html}
  <link rel="canonical" href="{canonical}">
  <link rel="icon" type="image/webp" href="/images/optimized/zihin_gezgini_logo_sketch-960.webp">
  <link rel="alternate" type="application/rss+xml" title="Zihin Gezgini RSS" href="/feed.xml">
  <meta property="og:locale" content="tr_TR">
  <meta property="og:type" content="{page_type}">
  <meta property="og:site_name" content="Zihin Gezgini">
  <meta property="og:url" content="{canonical}">
  <meta property="og:title" content="{html.escape(title, quote=True)}">
  <meta property="og:description" content="{html.escape(description, quote=True)}">
  <meta property="og:image" content="{image_url}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title, quote=True)}">
  <meta name="twitter:description" content="{html.escape(description, quote=True)}">
  <meta name="twitter:image" content="{image_url}">
  {schema_html}
  <link rel="stylesheet" href="/style.css?v=65">
  <link rel="stylesheet" href="/zihin-v2.css?v=4">
  <link rel="stylesheet" href="/static-pages.css?v={max(static_css_version, 7)}">
  <script src="/static-page.js?v={max(static_js_version, 4)}" defer></script>
</head>
<body class="static-page {html.escape(body_class)}">
  <a class="skip-link" href="#main-content">Ana içeriğe geç</a>
  <div class="paper-texture"></div>
  <div class="app-container">
    {header(active)}
    <main class="site-content" id="main-content">
      {content}
    </main>
    {footer()}
  </div>
</body>
</html>"""


def breadcrumb(items: list[tuple[str, str]]) -> str:
    links = []
    for index, (label, href) in enumerate(items):
        if index == len(items) - 1:
            links.append(f'<span aria-current="page">{html.escape(label)}</span>')
        else:
            links.append(f'<a href="{href}">{html.escape(label)}</a>')
    return f'<nav class="static-breadcrumb" aria-label="İçerik yolu">{"<span>›</span>".join(links)}</nav>'


def section_search(*, scope: str, title: str, description: str, placeholder: str, total: int) -> str:
    search_id = f"{scope}-section-search"
    return f"""
        <section class="section-search-panel" data-section-search data-search-scope="{html.escape(scope, quote=True)}" data-search-total="{total}" aria-labelledby="{search_id}-title">
          <div class="section-search-copy">
            <p class="section-search-eyebrow">Yalnızca bu bölüm</p>
            <h2 id="{search_id}-title">{html.escape(title)}</h2>
            <p>{html.escape(description)}</p>
          </div>
          <form class="section-search-form" role="search">
            <label class="section-search-label" for="{search_id}">{html.escape(title)}</label>
            <div class="section-search-control">
              <span aria-hidden="true">⌕</span>
              <input id="{search_id}" type="search" data-section-search-input placeholder="{html.escape(placeholder, quote=True)}" autocomplete="off" enterkeyhint="search">
              <button type="button" data-section-search-clear hidden>Temizle</button>
            </div>
            <p class="section-search-status" data-section-search-status aria-live="polite">{total} kayıt</p>
          </form>
          <p class="section-search-empty" data-section-search-empty hidden>Bu bölümde aramana uyan bir sonuç bulunamadı.</p>
        </section>"""


def render_post(post: dict[str, Any]) -> tuple[str, str, str]:
    slug = post["slug"]
    path = f"/yazilar/{slug}/"
    description = excerpt(post.get("content", ""))
    title = f"{post['title']} | Zihin Gezgini"
    featured = post.get("featuredImage")
    featured_html = ""
    if featured and not post.get("hideFeaturedImageInPost"):
        featured_display = display_asset(featured)
        featured_html = (
            f'<img src="{html.escape(featured_display, quote=True)}" class="post-featured-img" '
            f'width="960" height="600" decoding="async" fetchpriority="high" alt="{html.escape(post["title"], quote=True)}">'
        )

    audio_html = ""
    if post.get("audioFile"):
        audio_html = f"""
        <section class="static-audio" aria-label="Sesli dinle">
          <strong>Sesli dinle</strong>
          <audio controls preload="none" src="{html.escape(post['audioFile'], quote=True)}"></audio>
        </section>"""
    else:
        match = re.search(r'https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)[\w-]+', post.get("content", ""))
        if match:
            audio_html = f"""
            <section class="static-audio" aria-label="Sesli monolog">
              <strong>Sesli monolog</strong>
              <a href="{html.escape(match.group(0), quote=True)}" target="_blank" rel="noopener">YouTube'da dinle ↗</a>
            </section>"""

    body = f"""
      <article class="post-detail static-article" data-post-slug="{html.escape(slug)}">
        {breadcrumb([("Başlangıç", "/"), ("Yazılar", "/yazilar/"), (post['title'], path)])}
        <header class="post-meta">
          <div class="post-detail-category">{html.escape(post.get('category', 'Düşünce'))}</div>
          <h1 class="post-detail-title">{html.escape(post['title'])}</h1>
          <div class="post-meta-sub">
            <time datetime="{html.escape(post.get('date', ''))}">{html.escape(date_tr(post.get('date', '')))}</time>
            <span>• {max(1, len(strip_html(post.get('content', '')).split()) // 200 + 1)} dk okuma</span>
            <button type="button" class="post-share-btn" data-share>Bağlantıyı paylaş</button>
          </div>
        </header>
        {audio_html}
        {featured_html}
        <div class="post-body">{post.get('content', '')}</div>
        <div class="post-subscribe-section">
          <h3>Zihin Gezgini Substack</h3>
          <p>Yeni yazılar ve felsefi karalamalar için bültene katılabilirsin.</p>
          <a href="https://zihingezgini.substack.com" target="_blank" rel="noopener" class="subscribe-btn">Substack'te abone ol ↗</a>
        </div>
      </article>"""

    schema = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post["title"],
        "description": description,
        "datePublished": post.get("date", ""),
        "dateModified": post.get("date", ""),
        "mainEntityOfPage": f"{SITE_URL}{path}",
        "image": absolute_asset(featured),
        "author": {"@type": "Person", "name": "İlker Manavoğlu"},
        "publisher": {"@type": "Organization", "name": "Zihin Gezgini"},
    }
    return path, page_shell(
        title=title,
        description=description,
        path=path,
        content=body,
        image=featured,
        schema=schema,
        page_type="article",
        body_class="post-page",
    ), date_iso(post.get("date", ""))


def render_post_archive(posts: list[dict[str, Any]]) -> str:
    cards = []
    for post in posts:
        image_html = ""
        if post.get("featuredImage"):
            image_html = (
                f'<div class="card-img-container"><img src="{html.escape(display_asset(post["featuredImage"]), quote=True)}" '
                f'class="card-img" loading="lazy" decoding="async" width="640" height="400" alt="{html.escape(post["title"], quote=True)}"></div>'
            )
        search_text = " ".join((
            str(post.get("title", "")),
            str(post.get("category", "")),
            excerpt(post.get("content", ""), 500),
        ))
        cards.append(f"""
        <a class="post-card" href="/yazilar/{html.escape(post['slug'])}/" data-section-search-item data-search-text="{html.escape(search_text, quote=True)}">
          {image_html}
          <div class="card-content">
            <span class="card-category">{html.escape(post.get('category', 'Düşünce'))}</span>
            <h2 class="card-title">{html.escape(post['title'])}</h2>
            <time class="card-date" datetime="{html.escape(post.get('date', ''))}">{html.escape(date_tr(post.get('date', '')))}</time>
          </div>
        </a>""")
    content = f"""
      <section class="static-index" data-section-search-collection="posts">
        {breadcrumb([("Başlangıç", "/"), ("Yazılar", "/yazilar/")])}
        <header class="static-page-heading">
          <p class="section-kicker">Özgün üretimler</p>
          <h1>Defterden bütün kayıtlar</h1>
          <p>Felsefe, bilim, psikoloji ve gündelik hayata düşülmüş kişisel notlar.</p>
        </header>
        {section_search(scope="posts", title="Yazılarda ara", description=f"Yalnızca bu bölümdeki {len(posts)} kişisel yazı aranır; Okuma Haritası ve Araştırma Arşivi sonuçlara katılmaz.", placeholder="Başlık, konu veya kavram yaz", total=len(posts))}
        <div class="posts-grid static-post-grid">{''.join(cards)}</div>
      </section>"""
    return page_shell(
        title="Yazılar | Zihin Gezgini",
        description="İlker Manavoğlu'nun felsefe, bilim, psikoloji ve gündelik hayat üzerine kişisel yazıları.",
        path="/yazilar/",
        content=content,
        schema={"@context": "https://schema.org", "@type": "CollectionPage", "name": "Zihin Gezgini Yazıları"},
        static_css_version=6,
        static_js_version=3,
    )


def render_about() -> str:
    content = f"""
      <section class="about-container static-about">
        <div class="about-image-container">
          <img src="/images/optimized/thinking_man_sketch-960.webp" class="about-featured-img" width="720" height="720" decoding="async" alt="Düşünen insan çizimi">
        </div>
        <div class="about-header">
          {breadcrumb([("Başlangıç", "/"), ("Zihin Odası", "/zihin-odasi/")])}
          <h1 class="about-title">Bu alan neden var?</h1>
          <div class="divider"></div>
        </div>
        <div class="about-content">
          <p>Zihin Gezgini iki ayrı alandan oluşuyor. Kişisel yazılar, notlar, fotoğraflar, müzik denemeleri ve film analizleri bana ait; okuduklarımı, düşündüklerimi ve denediklerimi kaybetmemek için tuttuğum kişisel arşivi oluşturuyor.</p>
          <p>Okuma Haritası'ndaki 300 ön okuma rehberi ise bütünüyle yapay zekâ tarafından oluşturuldu. Bu metinleri ben yazmadım; yapay zekâdan istediğim çıktıları koleksiyonun amacı ve yayın düzeni doğrultusunda yönettim.</p>
          <p>Bu koleksiyonu kitapları okumadan önce temel fikirlerine hazırlanmak, hepsini okuyamadığımda da eser hakkında bir başlangıç fikri edinmek için tasarladım. Önce kendi okuma yolculuğum için kurdum; başkaları da yararlansın diye yayımladım.</p>
          <blockquote>“Biriktiriyorum, çünkü kaybolsun istemiyorum.”</blockquote>
          <div class="about-links">
            <a href="https://www.youtube.com/@Zihin_Gezgini" target="_blank" rel="noopener" class="about-link-btn youtube-btn">YouTube Monologları</a>
            <a href="https://zihingezgini.substack.com" target="_blank" rel="noopener" class="about-link-btn substack-btn">Substack Yazıları</a>
            <a href="https://open.spotify.com/show/3PLOqIu8IrkzFu30aA6cQB" target="_blank" rel="noopener" class="about-link-btn spotify-btn">Spotify</a>
            <a href="https://podcasts.apple.com/tr/podcast/zihin-gezgini/id1812203751" target="_blank" rel="noopener" class="about-link-btn apple-btn">Apple Podcasts</a>
            <a href="https://instagram.com/zihin_gezgini" target="_blank" rel="noopener" class="about-link-btn instagram-btn">Instagram</a>
          </div>
        </div>
      </section>"""
    return page_shell(
        title="Zihin Odası | Zihin Gezgini",
        description="Zihin Gezgini'ndeki kişisel üretimler ile yapay zekâ tarafından oluşturulan 300 ön okuma rehberi arasındaki ayrım.",
        path="/zihin-odasi/",
        content=content,
        active="about",
        schema={"@context": "https://schema.org", "@type": "AboutPage", "name": "Zihin Odası"},
    )


def render_roadmap(books: list[dict[str, Any]], summary_meta: dict[int, dict[str, Any]]) -> str:
    groups = []
    for evre in range(1, 11):
        rows = []
        for book in [item for item in books if item.get("evre") == evre]:
            summary = ""
            summary_info = summary_meta.get(book.get("no"), {})
            summary_url = summary_info.get("url")
            if summary_url:
                summary = f'<a class="book-summary-btn" href="{summary_url}">Rehberi oku</a>'
            title_text = str(book.get("title", ""))
            title = html.escape(title_text)
            if summary_url:
                title = f'<a class="book-title-link book-summary-title-link" href="{summary_url}">{title}</a>'
            elif book.get("link"):
                title = f'<a href="{html.escape(book["link"], quote=True)}" rel="noopener">{title}</a>'
            row_classes = "book-item-row has-summary" if summary_url else "book-item-row"
            row_link_attrs = f' data-summary-href="{summary_url}"' if summary_url else ""
            search_text = " ".join(str(book.get(key, "")) for key in ("no", "author", "title", "category", "pubDate", "description"))
            rows.append(f"""
            <article class="{row_classes}" id="kitap-{book.get('no')}"{row_link_attrs} data-section-search-item data-search-text="{html.escape(search_text, quote=True)}" data-book-no="{book.get('no')}" data-book-title="{html.escape(title_text, quote=True)}" data-book-author="{html.escape(str(book.get('author', '')), quote=True)}" data-book-category="{html.escape(str(book.get('category', '')), quote=True)}" data-book-phase="{evre}" data-book-pdf="{'yes' if summary_info.get('pdf') else 'no'}">
              <div class="book-check-col">
                <input type="checkbox" data-roadmap-book="{book.get('no')}" aria-label="{html.escape(title_text, quote=True)} okundu">
              </div>
              <div class="book-info-col">
                <div class="book-title-row">
                  <span class="book-no">#{book.get('no')}</span>
                  <strong class="book-author">{html.escape(str(book.get('author', '')))}</strong> — {title} {summary}
                </div>
                <details class="book-details-native">
                  <summary>Açıklama</summary>
                  <div class="book-meta-row">
                    <span class="book-category-tag">{html.escape(str(book.get('category', '')))}</span>
                    <span>{html.escape(str(book.get('pubDate', '')))}</span>
                  </div>
                  <p class="book-desc">{html.escape(str(book.get('description', '')))}</p>
                </details>
              </div>
            </article>""")
        groups.append(f"""
        <section class="roadmap-phase" id="evre-{evre}" data-section-search-group>
          <h2><span>{evre:02d}</span>{html.escape(EVRE_TITLES[evre])}</h2>
          <div class="roadmap-books-list">{''.join(rows)}</div>
        </section>""")

    quick_nav = "".join(f'<a href="#evre-{i}" data-section-search-group-link="evre-{i}">{i:02d}</a>' for i in range(1, 11))
    book_by_no = {int(book["no"]): book for book in books}
    route_cards = []
    for route_title, route_description, route_numbers in START_ROUTES:
        route_links = "".join(
            f'<a href="#kitap-{number}"><span>#{number}</span>{html.escape(book_by_no[number]["title"])}</a>'
            for number in route_numbers if number in book_by_no
        )
        route_cards.append(
            f'<article class="start-route"><h3>{html.escape(route_title)}</h3><p>{html.escape(route_description)}</p><div>{route_links}</div></article>'
        )
    categories = sorted({str(book.get("category", "")).strip() for book in books if book.get("category")})
    category_options = "".join(f'<option value="{html.escape(category, quote=True)}">{html.escape(category)}</option>' for category in categories)
    content = f"""
      <section class="roadmap-container static-roadmap" data-section-search-collection="roadmap">
        {breadcrumb([("Başlangıç", "/"), ("Okuma Haritası", "/okuma-haritasi/")])}
        <header class="roadmap-header">
          <p class="section-kicker">Yapay zekâ ile oluşturulan 300 ön okuma rehberi</p>
          <h1 class="roadmap-title">Okuma Serüveni</h1>
          <p class="roadmap-method-note"><strong>Bu bölümün yöntemi:</strong> Bu bölüm, kitapları okumadan önce temel fikirlerine hazırlanmak için yapay zekâya hazırlattığım 300 ön okuma rehberinden oluşuyor. Önce kendi okuma yolculuğum için tasarladım; başkaları da yararlansın diye yayımladım. Rehberler kitapların yerini tutmaz, kitaba açılan bir başlangıç kapısı sunar.</p>
          <p class="roadmap-subtitle">Bu bir başarı listesi değil; düşüncenin farklı alanları arasında ilerleyen kişisel bir araştırma rotasıdır. Okuma işaretlerin yalnızca bu tarayıcıda saklanır.</p>
          <nav class="static-phase-nav" aria-label="Okuma evreleri">{quick_nav}</nav>
          <div class="roadmap-stats">
            <div class="stats-text"><span>Toplam ilerleme</span><strong data-roadmap-count>0% (0 / 300)</strong></div>
            <div class="stats-progress-bar"><div class="stats-progress-fill" data-roadmap-fill style="width:0"></div></div>
          </div>
        </header>
        <section class="start-routes" aria-labelledby="start-routes-title">
          <div class="start-routes-heading"><p class="section-kicker">Nereden başlamalı?</p><h2 id="start-routes-title">Beş kısa başlangıç rotası</h2></div>
          <div class="start-routes-grid">{''.join(route_cards)}</div>
        </section>
        {section_search(scope="roadmap", title="Okuma Haritası'nda ara", description="Bu arama yalnızca Okuma Haritası'ndaki 300 kitabı; yazar, eser adı, kategori ve açıklama bilgileriyle tarar.", placeholder="300 kitap içinde ara", total=len(books))}
        <section class="roadmap-toolbox" data-roadmap-tools aria-label="Okuma haritası araçları">
          <div class="roadmap-filter-grid">
            <label>Kategori<select data-roadmap-filter="category"><option value="all">Tüm kategoriler</option>{category_options}</select></label>
            <label>Evre<select data-roadmap-filter="phase"><option value="all">Tüm evreler</option>{''.join(f'<option value="{i}">Evre {i:02d}</option>' for i in range(1, 11))}</select></label>
            <label>Okuma durumu<select data-roadmap-filter="status"><option value="all">Tümü</option><option value="unread">Yalnızca okunmamışlar</option><option value="read">Yalnızca okunanlar</option></select></label>
            <label>PDF<select data-roadmap-filter="pdf"><option value="all">Tümü</option><option value="yes">PDF olanlar</option><option value="no">PDF olmayanlar</option></select></label>
            <label>Sırala<select data-roadmap-sort><option value="number">Harita sırası</option><option value="title">Eser adına göre</option><option value="author">Yazara göre</option></select></label>
            <form class="roadmap-number-jump" data-roadmap-jump><label for="roadmap-book-number">Kitap numarası</label><div><input id="roadmap-book-number" type="number" min="1" max="300" inputmode="numeric" placeholder="1–300"><button type="submit">Git</button></div></form>
          </div>
          <div class="roadmap-actions">
            <button type="button" data-random-book>Rastgele kitap seç</button>
            <button type="button" data-export-progress>İlerlemeyi yedekle</button>
            <button type="button" data-import-progress>Yedeği geri yükle</button>
            <input type="file" accept="application/json" data-import-progress-file hidden>
            <button type="button" data-reset-filters>Filtreleri temizle</button>
          </div>
          <p class="roadmap-filter-status" data-roadmap-filter-status aria-live="polite">300 kitap gösteriliyor.</p>
        </section>
        {''.join(groups)}
      </section>"""
    schema = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Zihin Gezgini Yapay Zekâ Ön Okuma Haritası",
        "numberOfItems": len(books),
        "itemListElement": [
            {"@type": "ListItem", "position": item.get("no"), "name": item.get("title")}
            for item in books
        ],
    }
    return page_shell(
        title="300 Yapay Zekâ Ön Okuma Rehberi | Zihin Gezgini",
        description="Kitapların temel fikirlerine hazırlanmak için yapay zekâ ile oluşturulmuş 300 ön okuma rehberi ve kişisel okuma rotası.",
        path="/okuma-haritasi/",
        content=content,
        active="roadmap",
        schema=schema,
        static_css_version=6,
        static_js_version=3,
        body_class="roadmap-page",
    )


def markdown_inline(value: str) -> str:
    value = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", value or "")
    value = re.sub(r"\*(.+?)\*", r"<em>\1</em>", value)
    return value.replace("\n", "<br>")


def render_summary(summary: dict[str, Any]) -> tuple[str, str]:
    path = summary_path(summary)
    is_cover_artwork = summary.get("coverStyle") == "artwork"
    has_chapter_artwork = summary.get("chapterArtStyle") == "monochrome-engraving"
    chapter_art_color = str(summary.get("chapterArtColor", "#8B5B38"))
    if not re.fullmatch(r"#[0-9A-Fa-f]{6}", chapter_art_color):
        chapter_art_color = "#8B5B38"
    hero_class = " has-cover-art" if is_cover_artwork else ""
    cover_class = " summary-cover-art" if is_cover_artwork else ""
    chapters = []
    for chapter in summary.get("chapters", []):
        chapter_artwork = summary.get("chapterArtworks", {}).get(chapter.get("id", ""), {})
        chapter_image = chapter.get("image") or chapter_artwork.get("image")
        chapter_image_caption = chapter.get("imageCaption") or chapter_artwork.get("imageCaption", "")
        chapter_paragraphs = chapter.get("paragraphs", [])
        paragraphs = "".join(
            f'<p class="reader-paragraph">{markdown_inline(paragraph)}</p>'
            for paragraph in chapter_paragraphs
        )
        image = ""
        if chapter_image:
            image_class = " chapter-artwork" if has_chapter_artwork else ""
            visible_caption = "" if has_chapter_artwork else f"\n              <figcaption>{html.escape(chapter_image_caption)}</figcaption>"
            image = f"""
            <figure class="reader-chapter-img-box{image_class}">
              <img src="{html.escape(chapter_image, quote=True)}" class="reader-chapter-img" loading="lazy" decoding="async" width="960" height="960" alt="{html.escape(chapter_image_caption)}">{visible_caption}
            </figure>"""
        takeaway = ""
        if chapter.get("takeaway") and not has_chapter_artwork:
            takeaway = f'<aside class="reader-takeaway-card"><span class="takeaway-badge">Bölümün özü</span><p>“{html.escape(chapter["takeaway"])}”</p></aside>'
        section_label = ""
        if chapter.get("section"):
            section_label = f'\n          <p class="reader-section-label">{html.escape(chapter["section"])}</p>'
        source_refs = ""
        if chapter.get("sourceRefs"):
            refs = " ".join(
                f'<a href="#kaynak-{int(ref)}">[{int(ref)}]</a>'
                for ref in chapter["sourceRefs"]
            )
            source_refs = f'<p class="reader-source-refs">Kaynak izi: {refs}</p>'
        chapters.append(f"""
        <section class="reader-chapter-section" id="{html.escape(str(chapter.get('id', '')))}">{section_label}
          <h2 class="reader-chapter-title">{html.escape(chapter.get('title', ''))}</h2>
          <div class="reader-chapter-wrapper {'has-media' if image or takeaway else ''}">
            <div class="reader-chapter-text">{paragraphs}{source_refs}</div>
            <div class="reader-chapter-media">{image}{takeaway}</div>
          </div>
        </section>""")
    meta = summary.get("meta", {})
    pdf_link = ""
    if summary.get("pdfUrl"):
        pdf_label = summary.get("pdfLabel", "Renkli PDF'yi indir")
        pdf_link = (
            f'\n            <a class="summary-download-btn" href="{html.escape(summary["pdfUrl"], quote=True)}" download>'
            f'<span>{html.escape(pdf_label)}</span><small>Çevrimdışı okumak için</small></a>'
        )
    toc = ""
    if summary.get("longForm"):
        toc_items = "".join(
            f'<li><a href="#{html.escape(str(chapter.get("id", "")), quote=True)}">'
            f'<span>{index:02d}</span>{html.escape(chapter.get("title", ""))}</a></li>'
            for index, chapter in enumerate(summary.get("chapters", []), 1)
        )
        toc = f"""
        <details class="summary-toc" data-summary-toc>
          <summary>{len(summary.get('chapters', []))} duraklık okuma rotasını aç</summary>
          <ol>{toc_items}</ol>
        </details>"""
    sources = ""
    if summary.get("sources"):
        source_items = "".join(
            f'<li id="kaynak-{int(source["id"])}"><span>[{int(source["id"])}]</span> '
            f'<a href="{html.escape(source["url"], quote=True)}" target="_blank" rel="noopener">'
            f'{html.escape(source["title"])}</a></li>'
            for source in summary["sources"]
        )
        sources = f"""
        <details class="summary-sources">
          <summary>Kaynaklar ve ileri okumalar ({len(summary['sources'])})</summary>
          <ol>{source_items}</ol>
        </details>"""
    description = excerpt(summary.get("intro", "")) or f"{summary['title']} kitabının kapsamlı Türkçe özeti."
    reading_text = " ".join(
        [strip_html(summary.get("intro", ""))]
        + [strip_html(paragraph) for chapter in summary.get("chapters", []) for paragraph in chapter.get("paragraphs", [])]
    )
    reading_minutes = max(1, math.ceil(len(reading_text.split()) / 220))
    cover_display = display_asset(summary.get("coverImage"))
    original_title = html.escape(meta.get('originalTitle', ''))
    body = f"""
      <div class="reading-progress" data-reading-progress aria-hidden="true"><span></span></div>
      <article class="summary-reader-container static-summary{' is-long-form' if summary.get('longForm') else ''}{' has-chapter-artwork' if has_chapter_artwork else ''}" data-summary-book="{summary.get('bookNo')}"{' style="--chapter-art-ink: ' + chapter_art_color + ';"' if has_chapter_artwork else ''}>
        {breadcrumb([("Başlangıç", "/"), ("Okuma Haritası", "/okuma-haritasi/"), (summary['title'], path)])}
        <header class="summary-hero-split{hero_class}">
          <div class="summary-hero-left">
            <span class="summary-meta-book-no">#{summary.get('bookNo')}</span>
            <h1 class="summary-book-title">{html.escape(summary['title'])}</h1>
            <p class="summary-book-author">{html.escape(summary.get('author', ''))}</p>
            <p class="summary-book-subtitle">{html.escape(summary.get('subtitle', ''))}</p>
            <div class="summary-book-meta-box">
              <div><strong>Orijinal adı:</strong> {original_title}</div>
              <div><strong>Okuma süresi:</strong> yaklaşık {reading_minutes} dakika</div>
            </div>{pdf_link}
          </div>
          <div class="summary-hero-right"><img src="{html.escape(cover_display, quote=True)}" class="summary-featured-img{cover_class}" width="720" height="960" decoding="async" fetchpriority="high" alt="{html.escape(summary['title'], quote=True)} kapağı"></div>
        </header>
        <nav class="summary-reader-tools" aria-label="Okuma araçları">
          <span>{reading_minutes} dk okuma</span>
          <button type="button" data-reader-resume hidden>Kaldığın yere dön</button>
          <button type="button" data-reader-font="decrease" aria-label="Yazıyı küçült">A−</button>
          <button type="button" data-reader-font="increase" aria-label="Yazıyı büyüt">A+</button>
          <button type="button" data-reader-width>Satır genişliği</button>
          <button type="button" data-reader-print>Yazdır / PDF</button>
        </nav>
        <div class="summary-intro-box"><h2>Giriş</h2><p>{summary.get('intro', '')}</p></div>{toc}
        <div class="summary-chapters-list">{''.join(chapters)}</div>{sources}
        <footer class="summary-reader-footer"><p class="disclaimer-text"><strong>Telif ve sorumluluk notu:</strong> Bu bağımsız ve ticari olmayan okuma rehberi eğitim ve araştırma amacıyla hazırlanmıştır; özgün eserin yerini tutmaz ve yazar ya da yayınevi tarafından hazırlanmış veya onaylanmış değildir.</p></footer>
      </article>"""
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": f"{summary['title']} Ön Okuma Rehberi",
        "description": description,
        "mainEntityOfPage": f"{SITE_URL}{path}",
        "image": absolute_asset(summary.get("coverImage")),
        "author": {"@type": "Organization", "name": "Zihin Gezgini · Yapay Zekâ Okuma Haritası"},
        "about": {
            "@type": "Book",
            "name": summary["title"],
            "author": {"@type": "Person", "name": summary.get("author", "")},
        },
    }
    return path, page_shell(
        title=f"{summary['title']} Ön Okuma Rehberi | Zihin Gezgini",
        description=description,
        path=path,
        content=body,
        active="roadmap",
        image=summary.get("coverImage"),
        schema=schema,
        page_type="article",
        body_class="summary-page",
        static_css_version=5 if has_chapter_artwork else (4 if is_cover_artwork else 3),
    )


def render_table(table: Any) -> str:
    if not table:
        return ""
    rows: list[list[str]] = []
    headers: list[str] = []
    if isinstance(table, dict):
        headers = ["Başlık", "Açıklama"]
        rows = [[str(key), str(value)] for key, value in table.items()]
    elif isinstance(table, list) and table:
        if all(isinstance(row, dict) for row in table):
            headers = list(table[0].keys())
            rows = [[str(row.get(key, "")) for key in headers] for row in table]
        elif all(isinstance(row, (list, tuple)) for row in table):
            rows = [[str(cell) for cell in row] for row in table]
    if not rows:
        return ""
    head = ""
    if headers:
        head = "<thead><tr>" + "".join(f"<th>{html.escape(cell)}</th>" for cell in headers) + "</tr></thead>"
    body = "".join("<tr>" + "".join(f"<td>{html.escape(cell)}</td>" for cell in row) + "</tr>" for row in rows)
    return f'<div class="static-table-wrap"><table class="reader-table">{head}<tbody>{body}</tbody></table></div>'


def render_research_book(book: dict[str, Any], index_item: dict[str, Any]) -> tuple[str, str]:
    path = f"/arastirma/{book['id']}/"
    toc = []
    for index, chapter in enumerate(book.get("chapters", []), 1):
        chapter_id = f"bolum-{index}"
        title = html.escape(chapter.get("title", f"Bölüm {index}"))
        quote = html.escape(strip_html(chapter.get("quote", "")))
        toc.append(
            f'<li><a href="#{chapter_id}" data-research-chapter="{index}"><strong>{title}</strong>'
            f'{f"<span>{quote}</span>" if quote else ""}</a></li>'
        )
    cover = index_item.get("cover", f"/covers/{book['id']}.png")
    if not cover.startswith("/"):
        cover = "/" + cover
    description = excerpt(book.get("desc", ""))
    body = f"""
      <article class="static-research-book" data-research-id="{html.escape(book['id'], quote=True)}">
        {breadcrumb([("Başlangıç", "/"), ("Araştırma Arşivi", "/arastirma-arsivi/"), (book['title'], path)])}
        <header class="research-book-hero">
          <div>
            <p class="section-kicker">Araştırma masası · Çalışma dosyası</p>
            <h1>{html.escape(book['title'])}</h1>
            <p class="research-book-subtitle">{html.escape(book.get('subtitle', ''))}</p>
            <p>{html.escape(book.get('desc', ''))}</p>
            <a class="download-btn" href="/data/pdfs/{html.escape(book['id'])}.pdf" download>PDF olarak indir</a>
          </div>
          <img src="{html.escape(display_asset(cover), quote=True)}" width="720" height="960" decoding="async" fetchpriority="high" alt="{html.escape(book['title'], quote=True)} kapağı">
        </header>
        <section class="research-intro"><h2>Giriş ve sunuş</h2><div>{book.get('intro', '')}</div></section>
        <details class="research-toc"><summary>100 bölümün fihristini aç</summary><ol>{''.join(toc)}</ol></details>
        <section class="research-loader">
          <p>Tam metin yalnızca istediğinde yüklenir; böylece sayfa hızlı açılır ve gereksiz veri tüketmez.</p>
          <button type="button" class="static-primary-link" data-load-research>Tam metni tarayıcıda aç</button>
          <span role="status" data-research-status></span>
        </section>
        <div class="research-chapters" data-research-content></div>
        <section class="research-conclusion"><h2>Sonuç</h2><div>{book.get('conclusion', '')}</div></section>
      </article>"""
    schema = {
        "@context": "https://schema.org",
        "@type": "CreativeWork",
        "name": book["title"],
        "description": description,
        "url": f"{SITE_URL}{path}",
        "image": absolute_asset(cover),
        "isAccessibleForFree": True,
        "creator": {"@type": "Organization", "name": "Zihin Gezgini Araştırma Masası"},
    }
    return path, page_shell(
        title=f"{book['title']} | Zihin Gezgini Araştırma Arşivi",
        description=description,
        path=path,
        content=body,
        active="library",
        image=cover,
        schema=schema,
        page_type="article",
        body_class="research-book-page",
    )


def render_research_archive(index_items: list[dict[str, Any]]) -> str:
    cards = []
    for item in index_items:
        cover = item.get("cover", "")
        if cover and not cover.startswith("/"):
            cover = "/" + cover
        search_text = " ".join(str(item.get(key, "")) for key in ("title", "category", "desc"))
        cards.append(f"""
        <a class="static-research-card" href="/arastirma/{html.escape(item['id'])}/" data-section-search-item data-search-text="{html.escape(search_text, quote=True)}">
          <img src="{html.escape(display_asset(cover), quote=True)}" loading="lazy" decoding="async" width="480" height="640" alt="{html.escape(item['title'], quote=True)} kapağı">
          <span>{html.escape(item.get('category', 'Araştırma'))}</span>
          <h2>{html.escape(item['title'])}</h2>
          <p>{html.escape(item.get('desc', ''))}</p>
          <strong>{item.get('chapterCount', 100)} bölüm →</strong>
        </a>""")
    content = f"""
      <section class="library-layout static-library" data-section-search-collection="research">
        {breadcrumb([("Başlangıç", "/"), ("Araştırma Arşivi", "/arastirma-arsivi/")])}
        <header class="library-header">
          <p class="section-kicker">Araştırma masası</p>
          <h1>Araştırma Arşivi</h1>
          <p>Okumak, karşılaştırmak ve daha sonra özgün üretime dönüştürmek için kullanılan kapsamlı çalışma dosyaları.</p>
        </header>
        {section_search(scope="research", title="Araştırma Arşivi'nde ara", description=f"Yalnızca bu bölümdeki {len(index_items)} araştırma dosyası aranır; Okuma Haritası kitapları sonuçlara katılmaz.", placeholder="Araştırma başlığı veya konu yaz", total=len(index_items))}
        <div class="static-research-grid">{''.join(cards)}</div>
      </section>"""
    schema = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Zihin Gezgini Araştırma Arşivi",
        "hasPart": [
            {"@type": "CreativeWork", "name": item["title"], "url": f"{SITE_URL}/arastirma/{item['id']}/"}
            for item in index_items
        ],
    }
    return page_shell(
        title="Araştırma Arşivi | Zihin Gezgini",
        description="Bilim, felsefe, tarih, sanat ve kültür alanlarında kapsamlı araştırma çalışmaları.",
        path="/arastirma-arsivi/",
        content=content,
        active="library",
        schema=schema,
        static_css_version=6,
        static_js_version=3,
    )


def render_global_search() -> str:
    content = f"""
      <section class="global-search-page" data-global-search>
        {breadcrumb([("Başlangıç", "/"), ("Arama", "/arama/")])}
        <header class="static-page-heading">
          <p class="section-kicker">Bütün arşiv</p>
          <h1>Tek yerden ara</h1>
          <p>Yazıları, 300 kitap özetini ve araştırma dosyalarını aynı anda tara.</p>
        </header>
        <form class="global-search-form" role="search">
          <label for="global-search-input">Aranacak kelime</label>
          <div><input id="global-search-input" type="search" placeholder="Kitap, yazar, kavram veya konu" autocomplete="off" autofocus><button type="submit">Ara</button></div>
          <label for="global-search-type">İçerik türü</label>
          <select id="global-search-type"><option value="all">Bütün arşiv</option><option value="summary">Ön okuma rehberleri</option><option value="post">Yazılar</option><option value="research">Araştırmalar</option></select>
        </form>
        <p class="global-search-status" data-global-search-status aria-live="polite">Arama dizini hazırlanıyor…</p>
        <div class="global-search-results" data-global-search-results></div>
      </section>"""
    return page_shell(
        title="Arama | Zihin Gezgini",
        description="Zihin Gezgini yazıları, 300 kitap özeti ve araştırma arşivinde tek yerden arama.",
        path="/arama/",
        content=content,
        active="search",
        schema={"@context": "https://schema.org", "@type": "SearchResultsPage", "name": "Zihin Gezgini Arama"},
        body_class="search-page",
    )


def build_search_index(posts: list[dict[str, Any]], summaries: list[dict[str, Any]], research_index: list[dict[str, Any]]) -> None:
    records = []
    for post in posts:
        records.append({
            "type": "post", "label": "Yazı", "title": post["title"],
            "subtitle": str(post.get("category", "Yazı")), "description": excerpt(post.get("content", ""), 220),
            "url": f"/yazilar/{post['slug']}/",
        })
    for summary in summaries:
        records.append({
            "type": "summary", "label": "Ön okuma rehberi", "title": summary["title"],
            "subtitle": summary.get("author", ""), "description": excerpt(summary.get("intro", ""), 220),
            "url": summary_path(summary),
        })
    for item in research_index:
        records.append({
            "type": "research", "label": "Araştırma", "title": item["title"],
            "subtitle": item.get("category", ""), "description": excerpt(item.get("desc", ""), 220),
            "url": f"/arastirma/{item['id']}/",
        })
    write_file("data/search-index.json", json.dumps(records, ensure_ascii=False, separators=(",", ":")))


def render_random(posts: list[dict[str, Any]]) -> str:
    urls = [f"/yazilar/{post['slug']}/" for post in posts]
    script = json.dumps(urls, ensure_ascii=False).replace("</", "<\\/")
    content = f"""
      <section class="static-empty-state">
        <p class="section-kicker">Rastgele düşünce</p>
        <h1>Arşivden bir sayfa seçiliyor…</h1>
        <p>Yönlendirme başlamazsa <a href="/yazilar/">bütün yazılara dön</a>.</p>
      </section>
      <script>const pages={script};location.replace(pages[Math.floor(Math.random()*pages.length)]);</script>"""
    return page_shell(
        title="Rastgele Bir Düşünce | Zihin Gezgini",
        description="Zihin Gezgini arşivinden rastgele bir yazı.",
        path="/rastgele/",
        content=content,
    )


def render_404() -> str:
    content = """
      <section class="static-empty-state">
        <p class="section-kicker">404 · Kayıp sayfa</p>
        <h1>Bu düşünce yolu burada bitiyor.</h1>
        <p>Aradığın içerik taşınmış veya kaldırılmış olabilir.</p>
        <p><a class="static-primary-link" href="/">Başlangıca dön</a> · <a href="/yazilar/">Yazıları aç</a></p>
      </section>"""
    return page_shell(
        title="Sayfa Bulunamadı | Zihin Gezgini",
        description="Aradığınız sayfa bulunamadı. Zihin Gezgini ana sayfasına veya yazı arşivine dönebilirsiniz.",
        path="/404.html",
        content=content,
        noindex=True,
    )


def build_sitemap(entries: list[tuple[str, str | None, str, str]]) -> None:
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, lastmod, changefreq, priority in entries:
        lines.extend(["  <url>", f"    <loc>{xml_escape(SITE_URL + path)}</loc>"])
        if lastmod:
            lines.append(f"    <lastmod>{xml_escape(lastmod)}</lastmod>")
        lines.extend([f"    <changefreq>{changefreq}</changefreq>", f"    <priority>{priority}</priority>", "  </url>"])
    lines.append("</urlset>")
    write_file("sitemap.xml", "\n".join(lines))


def build_rss(posts: list[dict[str, Any]]) -> None:
    items = []
    for post in posts[:30]:
        try:
            published = datetime.fromisoformat(post.get("date", "")).replace(tzinfo=timezone(timedelta(hours=3)))
            pub_date = format_datetime(published)
        except (TypeError, ValueError):
            pub_date = ""
        url = f"{SITE_URL}/yazilar/{post['slug']}/"
        items.append(f"""    <item>
      <title>{xml_escape(post['title'])}</title>
      <link>{xml_escape(url)}</link>
      <guid isPermaLink="true">{xml_escape(url)}</guid>
      <description>{xml_escape(excerpt(post.get('content', ''), 280))}</description>
      <pubDate>{xml_escape(pub_date)}</pubDate>
    </item>""")
    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Zihin Gezgini</title>
    <link>{SITE_URL}/</link>
    <description>İlker Manavoğlu'nun kişisel düşünce arşivi.</description>
    <language>tr-TR</language>
    <atom:link xmlns:atom="http://www.w3.org/2005/Atom" href="{SITE_URL}/feed.xml" rel="self" type="application/rss+xml" />
{chr(10).join(items)}
  </channel>
</rss>"""
    write_file("feed.xml", feed)


def build_legacy_routes(summaries: list[dict[str, Any]]) -> None:
    summary_map = {str(item["bookNo"]): summary_path(item) for item in summaries}
    script = f"""(() => {{
  const hash = window.location.hash || "";
  const summaries = {json.dumps(summary_map, ensure_ascii=False, separators=(',', ':'))};
  let target = null;
  if (hash.startsWith("#/post/")) target = "/yazilar/" + hash.slice(7) + "/";
  else if (hash === "#/roadmap") target = "/okuma-haritasi/";
  else if (hash === "#/library") target = "/arastirma-arsivi/";
  else if (hash === "#/about") target = "/zihin-odasi/";
  else if (hash === "#/random") target = "/rastgele/";
  else {{
    const match = hash.match(/^#\\/book\\/(\\d+)\\/summary$/);
    if (match && summaries[match[1]]) target = summaries[match[1]];
  }}
  if (target) window.location.replace(target);
}})();"""
    write_file("legacy-routes.js", script)


def build_static_site() -> None:
    print("Building crawlable static pages…")
    for directory in GENERATED_DIRS:
        target = ROOT / directory
        if target.exists():
            shutil.rmtree(target)

    post_index = load_json("data/posts.json")
    posts = [load_json(f"data/posts/{item['slug']}.json") for item in post_index]
    summaries = [load_json(str(path.relative_to(ROOT))) for path in sorted((ROOT / "data/summaries").glob("*.json"), key=lambda p: int(p.stem))]
    books = load_json("data/books.json")
    research_index = load_json("data/kutuphane_index.json")

    summary_meta = {
        int(item["bookNo"]): {"url": summary_path(item), "pdf": bool(item.get("pdfUrl"))}
        for item in summaries
    }
    sitemap_entries: list[tuple[str, str | None, str, str]] = [
        ("/", None, "weekly", "1.0"),
        ("/yazilar/", None, "weekly", "0.9"),
        ("/zihin-odasi/", None, "monthly", "0.7"),
        ("/okuma-haritasi/", None, "monthly", "0.8"),
        ("/arastirma-arsivi/", None, "monthly", "0.8"),
        ("/arama/", None, "weekly", "0.8"),
    ]

    write_file("yazilar/index.html", render_post_archive(posts))
    for post in posts:
        path, rendered, lastmod = render_post(post)
        write_file(path.lstrip("/") + "index.html", rendered)
        sitemap_entries.append((path, lastmod, "monthly", "0.8"))

    write_file("zihin-odasi/index.html", render_about())
    write_file("okuma-haritasi/index.html", render_roadmap(books, summary_meta))

    for summary in summaries:
        path, rendered = render_summary(summary)
        write_file(path.lstrip("/") + "index.html", rendered)
        sitemap_entries.append((path, None, "monthly", "0.7"))

    write_file("arastirma-arsivi/index.html", render_research_archive(research_index))
    write_file("arama/index.html", render_global_search())
    build_search_index(posts, summaries, research_index)
    index_by_id = {item["id"]: item for item in research_index}
    for item in research_index:
        book = load_json(f"data/books/{item['id']}.json")
        path, rendered = render_research_book(book, index_by_id[item["id"]])
        write_file(path.lstrip("/") + "index.html", rendered)
        sitemap_entries.append((path, None, "monthly", "0.6"))

    write_file("rastgele/index.html", render_random(posts))
    write_file("404.html", render_404())
    build_sitemap(sitemap_entries)
    build_rss(posts)
    build_legacy_routes(summaries)
    write_file("robots.txt", "User-agent: *\nAllow: /\nDisallow: /admin/\n\nSitemap: https://zihingezgini.net/sitemap.xml")
    write_file(".nojekyll", "")
    print(f"Generated {len(posts)} posts, {len(summaries)} summaries and {len(research_index)} research books.")


if __name__ == "__main__":
    build_static_site()
