#!/usr/bin/env python3
"""Legacy Gazete preview tools; publication in this public repository is retired."""
from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import fcntl
import hashlib
import html
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
TR = ZoneInfo("Europe/Istanbul")
FEEDS = {
    "morning": ("Sabah gündemi", 8),
    "ai": ("AI gündemi", 21),
    "youtube_am": ("YouTube sabah", 10),
    "youtube_pm": ("YouTube akşam", 22),
    "eksi": ("Ekşi gündem", 20),
}
CATEGORIES = {
    "bilim": "Bilim", "teknoloji": "Teknoloji", "ekonomi": "Ekonomi",
    "dunya": "Dünya", "turkiye": "Türkiye", "kultur": "Kültür",
    "saglik": "Sağlık", "cevre": "Çevre", "spor": "Spor",
    "felsefe": "Zihin ve Felsefe", "hava": "Hava Durumu",
}
ORIGIN = "https://zihingezgini.net"
MAX_BYTES = 4_000_000


class InvalidBulletin(ValueError):
    pass


def fail(message):
    raise InvalidBulletin(message)


def require_preview_destination(path):
    """Never recreate newspaper content anywhere in this public checkout."""
    destination = Path(path).resolve()
    public_root = ROOT.resolve()
    if destination == public_root or public_root in destination.parents:
        fail("Bu herkese açık depoda Gazete yayını kaldırıldı; yalnız depo dışındaki önizleme dizinleri kullanılabilir.")


def fields(obj, required, optional=(), label="nesne"):
    if not isinstance(obj, dict):
        fail(f"{label}: nesne gerekli")
    missing = set(required) - obj.keys()
    unknown = obj.keys() - set(required) - set(optional)
    if missing or unknown:
        fail(f"{label}: eksik={sorted(missing)}, tanımsız={sorted(unknown)}")


def text(value, label, maximum, single_line=False):
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        fail(f"{label}: boş olmayan, en çok {maximum} karakterli metin gerekli")
    if any(ord(c) < 32 and c not in "\n\t" for c in value):
        fail(f"{label}: kontrol karakteri")
    if single_line and ("\n" in value or "\r" in value):
        fail(f"{label}: tek satır gerekli")
    return value.strip()


def identifier(value, label):
    if not isinstance(value, str) or not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,95}", value):
        fail(f"{label}: güvenli, en çok 96 karakterli kimlik gerekli")
    return value


def timestamp(value, label):
    if not isinstance(value, str):
        fail(f"{label}: saat dilimli ISO 8601 gerekli")
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        fail(f"{label}: geçersiz ISO 8601")
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        fail(f"{label}: saat dilimi gerekli")
    return parsed


def source_date(value):
    if value is None:
        return
    if isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        try:
            dt.date.fromisoformat(value)
            return
        except ValueError:
            pass
    timestamp(value, "kaynak yayın tarihi")


def metadata(value, label):
    if not isinstance(value, dict) or len(canonical(value)) > 40_000:
        fail(f"{label}: en çok 40.000 karakterli JSON nesnesi gerekli")


def order(b):
    return (timestamp(b["scheduled_for"], "slot"),
            timestamp(b.get("prepared_at") or b["completed_at"], "paket hazırlama/tamamlanma"))


def validate_bulletin(b, now):
    fields(b, ("feed_id", "bulletin_id", "scheduled_for", "completed_at", "coverage_start",
               "coverage_end", "topics"), ("prepared_at", "metadata"), label="bülten")
    feed = b["feed_id"]
    if not isinstance(feed, str) or feed not in FEEDS:
        fail("tanımsız kaynak bülten")
    identifier(b["bulletin_id"], "bulletin_id")
    scheduled = timestamp(b["scheduled_for"], "scheduled_for")
    completed = timestamp(b["completed_at"], "completed_at") if b["completed_at"] is not None else None
    prepared = timestamp(b["prepared_at"], "prepared_at") if b.get("prepared_at") else None
    if completed is None and prepared is None:
        fail("tamamlanma saati bilinmiyorsa ayrı prepared_at gerekli")
    start = timestamp(b["coverage_start"], "coverage_start") if b["coverage_start"] is not None else None
    end = timestamp(b["coverage_end"], "coverage_end") if b["coverage_end"] is not None else None
    local = scheduled.astimezone(TR)
    if (local.hour, local.minute, local.second, local.microsecond) != (FEEDS[feed][1], 0, 0, 0):
        fail(f"{feed}: Türkiye saati {FEEDS[feed][1]:02}:00 bekleniyor")
    if bool(start) != bool(end) or (start and (start > end or end > (completed or prepared))):
        fail("bilinen kapsam başlangıcı <= kapsam sonu <= tamamlanma/paket zamanı gerekli")
    if any(t and t > now + dt.timedelta(minutes=5) for t in (completed, prepared, scheduled)):
        fail("gelecekteki bülten yayımlanamaz")
    if "metadata" in b:
        metadata(b["metadata"], "bülten metaverisi")
        bm = b['metadata']
        if bm.get('delivered_at'): timestamp(bm['delivered_at'], 'teslim zamanı')
        cutoff = bm.get('research_cutoff')
        if cutoff is not None:
            if not isinstance(cutoff, dict): fail('research_cutoff: nesne gerekli')
            if cutoff.get('at'): timestamp(cutoff['at'], 'araştırma kesimi')
        gaps = bm.get('source_gaps')
        if gaps is not None and (not isinstance(gaps, list) or any(not isinstance(x,dict) for x in gaps)):
            fail('source_gaps: nesne listesi gerekli')
    topics = b["topics"]
    if not isinstance(topics, list) or not 1 <= len(topics) <= 30:
        fail("bülten 1–30 tamamlanmış konu içermeli")
    seen = set()
    for t in topics:
        fields(t, ("id", "category", "title", "summary", "what_happened", "sources"),
               ("metadata", "full_text", "full_text_sources", "full_text_sections", "full_text_metadata"), label="konu")
        identifier(t["id"], "konu kimliği")
        if t["id"] in seen:
            fail("yinelenen konu kimliği")
        seen.add(t["id"])
        if not isinstance(t["category"], str) or t["category"] not in CATEGORIES:
            fail("tanımsız konu kategorisi")
        text(t["title"], "başlık", 160, True)
        text(t["summary"], "tek cümle özet", 500, True)
        text(t["what_happened"], "Ne oldu?", 50_000)
        if "full_text" in t:
            text(t["full_text"], "Kaynak anlatımı", 200_000)
        if any(k in t for k in ("full_text_sources", "full_text_sections", "full_text_metadata")) and "full_text" not in t:
            fail("full_text ek alanları için full_text gerekli")
        if "full_text_metadata" in t:
            metadata(t["full_text_metadata"], "kaynak anlatımı metaverisi")
            if t["full_text_metadata"].get('source_url'): validate_url(t["full_text_metadata"]['source_url'])
            for key in ("publication", "event_time"):
                value = t["full_text_metadata"].get(key)
                if value is not None:
                    if not isinstance(value, dict): fail(f"full_text_metadata.{key}: nesne gerekli")
                    for name in ("at", "date") if key == "publication" else ("start", "end"):
                        source_date(value.get(name))
        if "full_text_sections" in t:
            sections = t["full_text_sections"]
            if not isinstance(sections, list) or not 1 <= len(sections) <= 60:
                fail("full_text_sections: 1–60 bölüm gerekli")
            for section in sections:
                fields(section, ("heading", "timestamp", "url", "paragraphs"), ("warning",), label="kaynak bölümü")
                if "warning" in section and type(section["warning"]) is not bool: fail("bölüm warning: boolean gerekli")
                if section["heading"] is not None: text(section["heading"], "bölüm başlığı", 500, True)
                if section["timestamp"] is not None:
                    if not isinstance(section["timestamp"], str) or not re.fullmatch(r"(?:\d{1,3}:)?\d{1,3}:[0-5]\d", section["timestamp"]):
                        fail("bölüm zaman kodu geçersiz")
                if section["url"] is not None: validate_url(section["url"])
                if not isinstance(section["paragraphs"], list) or not 1 <= len(section["paragraphs"]) <= 100:
                    fail("bölüm paragraf listesi gerekli")
                for paragraph in section["paragraphs"]: text(paragraph, "bölüm paragrafı", 50_000)
        if "metadata" in t:
            metadata(t["metadata"], "konu metaverisi")
            if "publication" in t["metadata"]:
                pub = t["metadata"]["publication"]
                if not isinstance(pub, dict): fail("publication: nesne gerekli")
                source_date(pub.get("at"))
                source_date(pub.get("date"))
            event = t['metadata'].get('event_time')
            if event is not None:
                if not isinstance(event,dict):fail('event_time: nesne gerekli')
                source_date(event.get('start'))
                source_date(event.get('end'))
        validate_sources(t["sources"])
        if "full_text_sources" in t:
            validate_sources(t["full_text_sources"])
    return b


def validate_sources(sources):
    if not isinstance(sources, list) or not 1 <= len(sources) <= 32:
        fail("konu 1–32 kaynak içermeli")
    for s in sources:
        fields(s, ("name", "url", "published_at"), label="kaynak")
        text(s["name"], "kaynak adı", 160, True)
        validate_url(s["url"])
        source_date(s["published_at"])


def validate_url(value):
    url = text(value, "kaynak URL", 2048, True)
    try:
        u = urlsplit(url)
        good = u.scheme in ("http", "https") and u.hostname and not u.username and not u.password
    except ValueError:
        good = False
    if not good or any(c.isspace() for c in value):
        fail("kaynak URL: kimlik bilgisi içermeyen HTTP(S) adresi gerekli")


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def read_json(path):
    raw = Path(path).read_bytes()
    if len(raw) > MAX_BYTES:
        fail("JSON paketi 4 MB sınırını aşıyor")
    def unique_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                fail(f"yinelenen JSON alanı: {key}")
            result[key] = value
        return result
    try:
        return json.loads(raw, object_pairs_hook=unique_pairs)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(f"JSON okunamadı: {exc}")


def validate_bundle(bundle, now):
    fields(bundle, ("schema_version", "bulletins"), label="paket")
    if type(bundle["schema_version"]) is not int or bundle["schema_version"] != 1:
        fail("schema_version=1 gerekli")
    if not isinstance(bundle["bulletins"], list) or not 1 <= len(bundle["bulletins"]) <= len(FEEDS):
        fail(f"paket 1–{len(FEEDS)} bülten içermeli")
    seen = set()
    for b in bundle["bulletins"]:
        validate_bulletin(b, now)
        if b["feed_id"] in seen:
            fail("pakette aynı kaynak iki kez bulunamaz")
        seen.add(b["feed_id"])


def load_current(root, now):
    path = root / "gazete/data/current.json"
    if not path.exists():
        return {"schema_version": 1, "bulletins": []}
    current = read_json(path)
    fields(current, ("schema_version", "bulletins"), label="durum")
    if current.get("bulletins"):
        validate_bundle(current, now)
    elif current != {"schema_version": 1, "bulletins": []}:
        fail("geçersiz boş durum")
    return current


def merge(current, bundle):
    by_feed = {b["feed_id"]: b for b in current["bulletins"]}
    changed, duplicate, stale = [], [], []
    for b in bundle["bulletins"]:
        feed = b["feed_id"]
        old = by_feed.get(feed)
        if old:
            if b["bulletin_id"] == old["bulletin_id"]:
                # Repackaging the same completed text is not a new bulletin.
                if canonical({k:v for k,v in b.items() if k != 'prepared_at'}) != canonical({k:v for k,v in old.items() if k != 'prepared_at'}):
                    fail(f"{feed}: aynı bulletin_id farklı içerikle gönderildi")
                duplicate.append(feed)
                continue
            new_order, old_order = order(b), order(old)
            if new_order < old_order:
                stale.append(feed)
                continue
            if new_order == old_order:
                fail(f"{feed}: aynı yayın zamanı için çelişkili bülten")
        by_feed[feed] = b
        changed.append(feed)
    result = {"schema_version": 1, "bulletins": [by_feed[f] for f in FEEDS if f in by_feed]}
    if len(canonical(result).encode()) > MAX_BYTES:
        fail("birleşik durum 4 MB sınırını aşıyor")
    return result, {"changed": changed, "duplicate": duplicate, "stale": stale}


def esc(value):
    return html.escape(str(value), quote=True)


def date_label(value):
    if value is None:
        return "Yayın tarihi kaynakta belirtilmemiş"
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return dt.date.fromisoformat(value).strftime("%d.%m.%Y")
    return timestamp(value, "tarih").astimezone(TR).strftime("%d.%m.%Y %H.%M") + " TSİ"


def article_path(b, topic):
    return f"yazi/{b['feed_id']}/{topic['id']}/"


def detail_path(b, topic):
    return article_path(b, topic) + "detay/"


def prose(value):
    return ''.join(f'<p>{esc(p.strip())}</p>' for p in re.split(r"\n\s*\n", value) if p.strip())


def detail_sources(topic):
    # Keep every original source; additional provenance belongs to the detail only.
    sources = list(topic["sources"])
    for source in topic.get("full_text_sources", []):
        if source not in sources:
            sources.append(source)
    return sources


def source_anchor(b, t):
    return f"kaynak-{b['feed_id']}-{t['id']}"


def narrative(t):
    # Transform only known section headings and safe Markdown links; all source
    # paragraphs remain visible without truncation or generated expansion.
    headings = {}
    for s in t.get("full_text_sections", []):
        if s["heading"]:
            label = (s["timestamp"] + " · " if s["timestamp"] else "") + s["heading"]
            headings[label] = s
    def inline(value):
        result, start = [], 0
        for match in re.finditer(r"\[([^\]\n]+)\]\((https?://[^\s)]+)\)", value):
            try: validate_url(match[2])
            except InvalidBulletin: continue
            result += [esc(value[start:match.start()]), f'<a href="{esc(match[2])}" rel="noopener noreferrer">{esc(match[1])}</a>']
            start = match.end()
        return ''.join(result) + esc(value[start:])
    parts = []
    for paragraph in re.split(r"\n\s*\n", t.get("full_text", t["what_happened"])):
        paragraph = paragraph.strip()
        if not paragraph: continue
        section = headings.get(paragraph)
        if section:
            label = esc(paragraph)
            url = section["url"]
            video = t.get('full_text_metadata', {}).get('source_url')
            if not url and video and section['timestamp'] and urlsplit(video).hostname in ('www.youtube.com', 'youtube.com', 'youtu.be'):
                seconds = 0
                for part in section['timestamp'].split(':'): seconds = seconds * 60 + int(part)
                url = video + ('&' if '?' in video else '?') + f't={seconds}s'
            if url: label = f'<a href="{esc(url)}" rel="noopener noreferrer">{label}</a>'
            parts.append(f'<h3{(" class=\"source-warning\"" if section.get("warning") else "")}>{label}</h3>')
        else: parts.append(f'<p>{inline(paragraph)}</p>')
    return ''.join(parts)


def quick_read(t):
    pages = t.get('full_text_metadata', {}).get('quick_read_pages', [])
    result = []
    for page in pages:
        body = f'<h3>{esc(page["title"])}</h3>' + prose(page['about'])
        for key in ('main', 'example', 'importance'):
            part = page.get(key)
            if part: body += f'<h4>{esc(part["heading"])}</h4>' + prose(part['text'])
        for key in ('takeaway', 'caveat'):
            if page.get(key): body += prose(page[key])
        diagram = page.get('diagram')
        if diagram:
            body += f'<h4>{esc(diagram["title"])}</h4><ol>'
            body += ''.join(f'<li><strong>{esc(step["label"])}</strong> {esc(step["text"])}</li>' for step in diagram['steps'])
            body += '</ol>' + prose(diagram.get('caption', ''))
        result.append('<section class="quick-page">' + body + '</section>')
    return '<section class="prose quick-reading"><h2>Bir çırpıda</h2>' + ''.join(result) + '</section>' if result else ''


def shell(title, body, categories, route="", active=""):
    nav = ''.join(f'<a href="/gazete/konu/{c}/"{chr(32)+"aria-current=\"page\"" if c == active else ""}>{esc(CATEGORIES[c])}</a>' for c in categories)
    return f'''<!doctype html>
<html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} · Gündem Gazetesi</title><meta name="description" content="Tamamlanmış bültenlerden, konuya göre düzenlenen günlük gazete.">
<link rel="canonical" href="{ORIGIN}/gazete/{route}"><link rel="stylesheet" href="/gazete/static/style.css"></head>
<body><a class="skip" href="#icerik">İçeriğe geç</a><header class="masthead"><a class="brand" href="/gazete/">Gündem Gazetesi</a>
<nav aria-label="Gazete konuları">{nav}</nav></header><main id="icerik">{body}</main>
<footer><span>Gündem Gazetesi · Saatler Türkiye saatidir. Kaynaklar ve yayın/kayıt bilgileri Kaynaklar bölümünde yer alır.</span><a class="footer-sources" href="/gazete/kaynaklar/"{(' aria-current="page"' if active == 'kaynaklar' else '')}>Kaynaklar</a></footer><script src="/gazete/static/freshness.js" defer></script></body></html>'''


def has_detail(b, t):
    if b['feed_id'] == 'morning':
        return False
    if b['feed_id'] == 'eksi':
        short = len(t['what_happened'].split())
        full = len(t.get('full_text', '').split())
        return full >= short + 20 and full * 5 >= short * 6
    return True


def card(b, t):
    label = FEEDS[b["feed_id"]][0]
    detail_cta = f'<a class="detail-read" href="/gazete/{detail_path(b,t)}">Detaylı oku <span aria-hidden="true">→</span></a>' if has_detail(b,t) else ''
    return f'''<article class="story"><p class="eyebrow">{esc(CATEGORIES[t['category']])} <span>· {esc(label)}</span></p>
<h2><a href="/gazete/{article_path(b,t)}">{esc(t['title'])}</a></h2><p>{esc(t['summary'])}</p>
<div class="story-actions"><a class="read" href="/gazete/{article_path(b,t)}">Yazıyı oku <span aria-hidden="true">→</span></a>
{detail_cta}</div></article>'''


def freshness(current, now):
    by_feed = {b["feed_id"]: b for b in current["bulletins"]}
    rows = []
    for feed, (label, hour) in FEEDS.items():
        expected = now.astimezone(TR).replace(hour=hour, minute=0, second=0, microsecond=0)
        if expected > now:
            expected -= dt.timedelta(days=1)
        b = by_feed.get(feed)
        late = b is None or timestamp(b["scheduled_for"], "slot") < expected
        status = "Yeni bülten bekleniyor" if late else "Son bülten hazır"
        content = ('<span>Tamamlanma saati belirtilmemiş</span>' if b and b['completed_at'] is None else
                   f'<time datetime="{esc(b["completed_at"])}">{date_label(b["completed_at"])}</time>') if b else '<span>Henüz bülten yok</span>'
        if b: content += f'<small>Bülten saati: {date_label(b["scheduled_for"])}</small>'
        slot = b["scheduled_for"] if b else ""
        rows.append(f'<li data-hour="{hour}" data-slot="{esc(slot)}"><strong>{label}</strong><span class="status" aria-live="polite">{status}</span>{content}</li>')
    return '<details class="freshness"><summary>Güncelleme bilgisi <span>· ' + str(len(by_feed)) + ' kaynak</span></summary><div><ul>' + ''.join(rows) + '</ul><p>Yeni bülten geldiğinde o kaynağın yazıları ve kaynakları birlikte yenilenir. Bekleyen bültenlerde son yazılar okunmaya devam eder. Bülten saati planlanan saattir; bilinmeyen tamamlanma zamanı yerine kullanılmaz.</p></div></details>'


def render(current, output, now):
    require_preview_destination(output)
    output.mkdir(parents=True)
    (output / "data").mkdir()
    (output / "data/current.json").write_text(json.dumps(current, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "static").mkdir()
    css = (ROOT / "tools/gazete/style.css").read_text(encoding="utf-8")
    (output / "static/style.css").write_text(css, encoding="utf-8")
    shutil.copyfile(ROOT / "tools/gazete/freshness.js", output / "static/freshness.js")
    shutil.copyfile(ROOT / "tools/gazete/bundle.schema.json", output / "bundle.schema.json")
    pairs = [(b,t) for b in current["bulletins"] for t in b["topics"]]
    pairs.sort(key=lambda pair: timestamp(pair[0]["scheduled_for"], "slot"), reverse=True)
    categories = [c for c in CATEGORIES if any(t["category"] == c for _,t in pairs)]
    routes = []
    def write(route, title, body, active=""):
        dest = output / route / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(shell(title, body, categories, route, active), encoding="utf-8")
        routes.append(route)
    lead = '<section class="intro"><h1>Bugün ne oldu?</h1><p>Bilimden ekonomiye, günün gelişmeleri ve onları anlatan yazılar.</p></section>'
    groups = []
    for c in categories:
        selected = [(b,t) for b,t in pairs if t["category"] == c]
        header = f'<div class="group-heading"><h2>{CATEGORIES[c]}</h2><a href="/gazete/konu/{c}/">Tümünü gör <span class="count">({len(selected)})</span></a></div>'
        groups.append(f'<section class="topic-group" aria-label="{CATEGORIES[c]}">{header}<div class="stories">' + ''.join(card(b,t) for b,t in selected[:3]) + '</div></section>')
    stories = ''.join(groups) or '<p class="empty">İlk tamamlanmış bülten geldiğinde yazılar burada yer alacak.</p>'
    write("", "Bugün ne oldu?", lead + freshness(current, now) + stories)
    for c in categories:
        write(f"konu/{c}/", CATEGORIES[c], f'<section class="intro"><p class="eyebrow">KONU</p><h1>{CATEGORIES[c]}</h1></section><section class="stories">' + ''.join(card(b,t) for b,t in pairs if t["category"] == c) + '</section>', c)
    source_groups = []
    for b,t in pairs:
        paragraphs = prose(t["what_happened"])
        article_paragraphs = prose(t.get('full_text', t['what_happened'])) if b['feed_id'] == 'morning' else paragraphs
        detail_cta = f'<p><a class="detail-read" href="/gazete/{detail_path(b,t)}">Detaylı oku <span aria-hidden="true">→</span></a></p>' if has_detail(b,t) else ''
        def source_list(items):
            rows = ''.join(f'<li><a href="{esc(s["url"])}" rel="noopener noreferrer">{esc(s["name"])}</a>' + (f'<span>{date_label(s["published_at"])}</span>' if s['published_at'] else '') + '</li>' for s in items)
            return rows
        tm, bm = t.get('metadata', {}), b.get('metadata', {})
        pub = tm.get('publication', {})
        source_time = pub.get('at') or pub.get('date')
        notes = []
        if source_time: notes.append(f'Yayın/kayıt tarihi: {date_label(source_time)}')
        if pub.get('note'): notes.append(esc(pub['note']))
        event = tm.get('event_time', {})
        if event.get('start'): notes.append(f'Olay başlangıcı: {date_label(event["start"])}')
        if event.get('end'): notes.append(f'Olay sonu: {date_label(event["end"])}')
        if event.get('note'): notes.append(esc(event['note']))
        completed_label = date_label(b['completed_at']) if b['completed_at'] else 'Kaynakta belirtilmemiş'
        timing = [f'Bülten tamamlandı: {completed_label}']
        if b.get('prepared_at'): timing.append(f'Paket hazırlandı: {date_label(b["prepared_at"])}')
        if b['coverage_start']:
            timing.append(f'Kapsanan dönem: {date_label(b["coverage_start"])} – {date_label(b["coverage_end"])}')
        else: timing.append('Kesin kapsam başlangıcı ve sonu kaynakta belirtilmemiş')
        if bm.get('delivered_at'): timing.append(f'Teslim: {date_label(bm["delivered_at"])}')
        cutoff = bm.get('research_cutoff') or {}
        if cutoff.get('at'): timing.append(f'Araştırma kesimi: {date_label(cutoff["at"])} ({esc(cutoff.get("precision", ""))})')
        if cutoff.get('note'): timing.append(esc(cutoff['note']))
        if bm.get('coverage_note'): timing.append(esc(bm['coverage_note']))
        for gap in bm.get('source_gaps') or []:
            timing.append('Bekleyen kaynak: ' + esc(gap.get('title','')) + '. ' + esc(gap.get('reason','')))
        source_notes = ''.join(f'<p class="coverage">{n}</p>' for n in notes)
        timing_html = '<br>'.join(timing)
        body = f'''<article class="article"><a class="back" href="/gazete/konu/{t['category']}/">← {CATEGORIES[t['category']]}</a>
<p class="eyebrow">{FEEDS[b['feed_id']][0]} · Bülten: {date_label(b['scheduled_for'])}</p><h1>{esc(t['title'])}</h1><p class="dek">{esc(t['summary'])}</p>
<section class="prose"><h2>Ne oldu?</h2>{article_paragraphs}</section>
{detail_cta}
<p class="source-link"><a href="/gazete/kaynaklar/#{source_anchor(b,t)}">Kaynaklar ve kayıt bilgisi</a></p>
<nav class="article-return" aria-label="Okumaya devam"><a href="/gazete/konu/{t['category']}/">{CATEGORIES[t['category']]} yazıları</a><a href="/gazete/">Gazete ana sayfası</a></nav></article>'''
        write(article_path(b,t), t["title"], body, t["category"])
        availability = '' if "full_text" in t else '<p class="detail-note">Bu konu için ayrı bir uzun kaynak anlatımı bulunmuyor. Kaynakta mevcut en kapsamlı metin aşağıda.</p>'
        if "full_text" in t and len(t["full_text"].split()) <= len(t["what_happened"].split()):
            availability = '<p class="detail-note">Özgün kaynak anlatımı aşağıda. Bu konunun kaynak metni kısa yazıdan daha uzun değildir; kaynakta olduğu biçimiyle sunulur.</p>'
        # A source narrative supplements the short article. Keep its original
        # caveats visible as well, even if a supplied narrative omits them.
        short_context = '' if "full_text" not in t else f'<details class="short-context"><summary>Kısa yazı ve çekinceleri</summary><section class="prose">{paragraphs}</section></details>'
        back_links = f'<nav class="detail-back" aria-label="Yazıya dönüş"><a href="/gazete/{article_path(b,t)}">← Kısa yazıya dön</a><a href="/gazete/">Gazete ana sayfası</a></nav>'
        detail_body = f'''<article class="article detail-article">{back_links}
<p class="eyebrow">{FEEDS[b['feed_id']][0]} · Bülten: {date_label(b['scheduled_for'])}</p><h1>{esc(t['title'])}</h1>
{availability}<section class="prose source-narrative"><h2>Kaynak anlatımı</h2>{narrative(t)}</section>{quick_read(t)}{short_context}
<p class="source-link"><a href="/gazete/kaynaklar/#{source_anchor(b,t)}">Kaynaklar ve kayıt bilgisi</a></p>{back_links}</article>'''
        write(detail_path(b,t), t["title"] + " · Kaynak anlatımı", detail_body, t["category"])
        fm = t.get('full_text_metadata', {})
        detail_notes = []
        for label,key in [('Kaynak yayını', 'publication'), ('Olay bilgisi', 'event_time')]:
            value = fm.get(key) or {}
            at = value.get('at') or value.get('date') if key == 'publication' else None
            if at: detail_notes.append(f'<p>{label}: {date_label(at)}</p>')
            if value.get('note'): detail_notes.append(f'<p>{esc(value["note"])}</p>')
        provenance = fm.get('provenance')
        provenance_html = '<pre>' + esc(json.dumps(provenance, ensure_ascii=False, indent=2)) + '</pre>' if provenance else ''
        originals = f'<p>Özgün başlık: {esc(fm["original_title"])}</p>' if fm.get('original_title') else ''
        unknown_date = '<p>Yayın tarihi kaynakta belirtilmemiş bağlantılara tarih atanmamıştır. Yazının yayın/kayıt ve kapsam bilgileri aşağıdadır.</p>' if any(s['published_at'] is None for s in detail_sources(t)) else ''
        source_groups.append(f'''<section class="source-group" id="{source_anchor(b,t)}"><h2><a href="/gazete/{article_path(b,t)}">{esc(t['title'])}</a></h2><p class="eyebrow">{FEEDS[b['feed_id']][0]} · {CATEGORIES[t['category']]}</p>
<ul class="source-list">{source_list(detail_sources(t))}</ul>
<details class="records"><summary>Tarih, kapsam ve kaynak kaydı</summary>{unknown_date}{originals}{source_notes}{''.join(detail_notes)}<p class="coverage">{timing_html}</p>{provenance_html}</details></section>''')
    write('kaynaklar/', 'Kaynaklar', '<section class="intro"><h1>Kaynaklar</h1><p>Güncel gazetede yer alan yazıların kaynakları. Yeni bültenlerle birlikte yenilenir.</p></section>' + ''.join(source_groups), 'kaynaklar')
    # Old newspaper URLs terminate here rather than retaining obsolete topics/editions.
    (output / "404.html").write_text(shell("Yazı bulunamadı", '<section class="intro"><h1>Bu yazı artık güncel gazetede yok.</h1><p><a href="/gazete/">Son yazılara dön</a></p></section>', categories), encoding="utf-8")
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>{ORIGIN}/gazete/{r}</loc></url>\n' for r in routes) + '</urlset>\n'
    (output / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    (output / ".nojekyll").write_text("", encoding="utf-8")


@contextlib.contextmanager
def locked(root):
    # Keep lock and staging outside the tracked tree. Serializes import/read/merge/render.
    token = hashlib.sha256(str(root.resolve()).encode()).hexdigest()[:24]
    lock = Path(tempfile.gettempdir()) / f"gazete-{token}.lock"
    with lock.open("a") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        yield


def replace_site(root, current, now):
    require_preview_destination(root)
    target = root / "gazete"
    recovery = root / ".gazete-previous"
    if recovery.exists():
        if not target.exists():
            recovery.rename(target)
        else:
            shutil.rmtree(recovery)
    stage_parent = Path(tempfile.mkdtemp(prefix=".gazete-stage-", dir=root))
    try:
        stage = stage_parent / "gazete"
        render(current, stage, now)
        if target.exists():
            target.rename(recovery)
        try:
            stage.rename(target)
        except BaseException:
            if recovery.exists() and not target.exists():
                recovery.rename(target)
            raise
        if recovery.exists():
            shutil.rmtree(recovery)
    finally:
        shutil.rmtree(stage_parent, ignore_errors=True)


def import_bundle(root, bundle, now):
    require_preview_destination(root)
    validate_bundle(bundle, now)  # Validate all feeds before changing any feed.
    with locked(root):
        recovery = root / ".gazete-previous"
        if recovery.exists() and not (root / "gazete").exists():
            recovery.rename(root / "gazete")
        current = load_current(root, now)
        merged, result = merge(current, bundle)
        if result["changed"]:
            replace_site(root, merged, now)
        return result


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--import-bundle", type=Path)
    group.add_argument("--check-bundle", type=Path)
    group.add_argument("--render", action="store_true")
    p.add_argument("--root", type=Path, default=ROOT)
    p.add_argument("--now", help="Test/preview clock only; production uses real UTC time")
    args = p.parse_args(argv)
    now = timestamp(args.now, "now") if args.now else dt.datetime.now(dt.timezone.utc)
    root = args.root.resolve()
    if not root.is_dir() or root == Path('/') or root == Path.home():
        p.error("mevcut depo/önizleme kök dizini gerekli")
    try:
        if not args.check_bundle:
            require_preview_destination(root)
        if args.check_bundle:
            validate_bundle(read_json(args.check_bundle), now)
            result = {"valid": True}
        elif args.import_bundle:
            result = import_bundle(root, read_json(args.import_bundle), now)
        else:
            with locked(root):
                replace_site(root, load_current(root, now), now)
            result = {"rendered": True}
        print(json.dumps(result, ensure_ascii=False))
    except (InvalidBulletin, OSError) as exc:
        print(f"Gazete değişmedi: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
