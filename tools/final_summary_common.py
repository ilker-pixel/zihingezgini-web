#!/usr/bin/env python3
"""Book-specific, padding-free builder for the final 72 reading guides."""

from __future__ import annotations

import json
import zlib
from pathlib import Path

from summary_batch_common import assemble, entry, slugify


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "summaries"
DATE = "Ağustos 2026"

CLAIM_TAILS = (
    "Bu ayrım kitabın geri kalanında izlenecek yolu açar.",
    "Böylece soyut kavram, gözlenebilir bir ilişkiye dönüşür.",
    "Yazarın temel hamlesi tam olarak bu görünmeyen bağı açığa çıkarmaktır.",
    "Bu nokta atlanırsa fikir kolayca yanlış bir slogana dönüşür.",
    "Mesele tek neden bulmak değil, sonucu üreten düzeni görebilmektir.",
    "Kavramın değeri, daha önce kopuk duran ayrıntıları aynı haritada buluşturmasındadır.",
    "Burada tanımdan çok, tanımın görmemizi sağladığı ilişki önemlidir.",
    "Bu başlangıç bir hüküm değil, sonraki örnekleri sınayacak mercektir.",
    "İlk bakışta küçük görünen ayrım, sorumluluğun yerini değiştirir.",
    "Bölüm böylece kişiyi suçlamadan önce koşulları incelemeyi önerir.",
    "İddia her şeyi açıklamaz; fakat doğru soruyu kurmak için sağlam bir başlangıç verir.",
    "Bu çerçeve kurulduğunda kitabın zor görünen sorusu gündelik hayata yaklaşır.",
    "Yazar tekil olayı daha geniş bir yapının belirtisi olarak okumamızı ister.",
    "Bu cümle sonuçtan önce hangi şartların oluştuğunu araştırmaya çağırır.",
    "Kavram, hazır cevap vermekten çok dikkatin yönünü değiştirir.",
    "Bundan sonraki tartışma bu temel bağlantının ne kadar taşınabileceğini sınar.",
)

SCENE_TAILS = (
    "Sahne, kavramı tanımdan çıkarıp insan yüzü ve gerçek bedelle buluşturur.",
    "Bir ayrıntı değiştiğinde sonucun da değişmesi, kaderden değil ilişkiden söz edildiğini gösterir.",
    "Örneğin gücü süslü olmasında değil, neden ile sonucu yan yana getirmesindedir.",
    "Aynı olayı başka kişinin gözünden görmek görünmeyen maliyeti açığa çıkarabilir.",
    "Bu küçük olay büyük haritanın neresine bakmamız gerektiğini gösteren bir işarettir.",
    "Sahneyi yavaşlatınca tek karar sandığımız şeyin öncesindeki etkiler belirginleşir.",
    "Gündelik ayrıntı, soyut düşüncenin hayata değdiği noktayı görünür kılar.",
    "Örnek kanıtın tamamı değildir; yine de iddianın nerede sınanacağını açık eder.",
    "Aynı kişiler başka kurallar içinde farklı davranınca açıklamanın yeri değişir.",
    "Bu olayın tersini düşünmek zorunlu olanla değişebilir olanı ayırmayı kolaylaştırır.",
    "İnsan yüzü eklendiğinde tartışmanın kimin hayatına dokunduğu anlaşılır.",
    "Sahnedeki sonuç tek niyetten değil, küçük koşulların birleşmesinden doğar.",
    "Büyük kelimelerin gerisindeki basit hareket burada açıkça görülür.",
    "Bu an, kitabın genel savını tek bir hayatın ölçeğinde sınamamıza izin verir.",
    "Olayı yaşayan kişi tüm yapıyı görmese de yapı onun seçeneklerini etkiler.",
    "Örneği hatırlamak, kuru kavramı ezberlemekten daha kalıcı bir yol sunar.",
)

MECHANISM_TAILS = (
    "Bu zincirde hangi halka koparsa sonucun değişeceği ayrıca sorulmalıdır.",
    "Mekanizma görüldüğünde benzer görünen iki olayın neden farklı sonuç verdiği anlaşılır.",
    "Neden ile sonuç arasındaki ara adımlar kitabın asıl açıklama gücünü taşır.",
    "Bu bağlantı niyet ile sonuç arasındaki mesafeyi görünür tutar.",
    "Burada önemli olan adımları sırayla izlemek ve hiçbirini doğal kabul etmemektir.",
    "İlişki tek yönlü değildir; sonuç da kendisini doğuran koşulları değiştirebilir.",
    "Kavram ancak bu ara hareketler açıkça görüldüğünde gerçek bir düşünme aracına dönüşür.",
    "Açıklamanın sınanacağı yer, varsayılan halkanın gerçekten çalışıp çalışmadığıdır.",
    "Bu süreç görünür olunca kişisel tercih ile yapısal baskı birbirinden ayrılabilir.",
    "Mekanizma aynı sonucu her yerde garanti etmez; bağlam onun gücünü artırır ya da azaltır.",
    "Aradaki basamakları atlamak etkileyici fakat boş bir sonuca yol açabilir.",
    "Bu hareketin kim tarafından başlatıldığı kadar kim tarafından sürdürüldüğü de önemlidir.",
    "Süreç, büyük değişimin gündelik tekrarlarla nasıl kurulduğunu gösterir.",
    "Bir halkanın maliyeti başka bir gruba aktarılıyorsa açıklama ona da bakmalıdır.",
    "Bu bağlantı geçmişteki örneği bugüne birebir kopyalamadan karşılaştırma imkânı verir.",
    "Mekanizmayı tersine çevirmek, fikrin karşı örnek karşısındaki dayanıklılığını gösterir.",
)

NUANCE_TAILS = (
    "Bu sınır fikri zayıflatmaz; onu her kapıyı açtığı sanılan sahte anahtardan korur.",
    "Bir düzeni tarif etmek onu ahlaken onaylamak anlamına gelmez.",
    "Karşı örnek iddiayı yok etmekten çok hangi koşulda geçerli olduğunu gösterir.",
    "Benzetme akılda kalıcıdır ama dünyanın tamamı değildir.",
    "Tek etkileyici olayın bütün toplumlar adına konuşmasına izin verilmemelidir.",
    "İnsan niyeti ile kurumsal sonuç her zaman aynı yönde ilerlemez.",
    "Açıklama olasılık gösterir; değişmez kader ilan etmez.",
    "Kitabın dönemi ve seçtiği örnekler hesaba katılmadan kavram kolayca dogmaya dönüşür.",
    "Kanıt, yorum ve değer yargısını ayrı tutmak burada özellikle önemlidir.",
    "Kavram bazı olaylarda merkezde, bazılarında yalnız yardımcı etkendir.",
    "Yazarın dışarıda bıraktığı deneyimler kavramın sınırını görmek için dinlenmelidir.",
    "Eleştirinin hedefi çoğu zaman soru değil, cevabın gereğinden fazla büyütülmesidir.",
    "Geçmişi bugünün kopyası saymak kadar aralarında bağ yokmuş gibi davranmak da yanıltır.",
    "Sonraki araştırmalar ayrıntıyı değiştirse bile iyi soru yaşamaya devam edebilir.",
    "Güçlü ton, belirsizlik ve bağlam payını ortadan kaldırmaz.",
    "Bu uyarı kavramı reddetmez; doğru ölçüde kullanmayı sağlar.",
)

TODAY_TAILS = (
    "Böyle bir gözlem kavramın açıklayıcı mı, yalnız etkileyici mi olduğunu gösterir.",
    "Amaç düşünceyi insanlara etiket yapmak değil, görünmeyen koşulu fark etmektir.",
    "Kısa vadeli kazanç ile uzun vadeli maliyeti ayırmak bu merceği hayata geçirir.",
    "Kişiyi suçlamadan önce davranışı üreten koşulu değiştirmek daha öğretici olabilir.",
    "Hazır reçete yerine kararın gizli varsayımını açığa çıkarmak gerekir.",
    "Geçmişteki sonucu değil, o sonucu doğuran soruyu bugünün araçları içinde sınamak gerekir.",
    "Kesin hüküm karşısında eksik kanıtı sormak acele genellemeyi durdurabilir.",
    "Kavramı önce kendi davranışımızda aramak onu kolay suçlama aracından kurtarır.",
    "Ortalama sonuç kadar bedeli kimin ödediğini de görmek gerekir.",
    "Görev tek doğruyu ezberlemek değil, yanlış kurulmuş soruyu fark etmektir.",
    "Dijital araç değişse bile güven, korku, itibar ve güç ilişkileri yeni biçimde sürebilir.",
    "Başka türlü olsaydı ne değişirdi sorusu fikri gerçek bir olayda sınar.",
    "Bir haftalık küçük gözlem, büyük iddianın gündelik karşılığını gösterebilir.",
    "Bugüne taşımak geçmişi kopyalamak değil, aynı mekanizmayı yeni koşullarda aramaktır.",
    "Karar öncesinde seçeneği olmayan kişiyi hesaba katmak tartışmayı dürüstleştirir.",
    "Bu soru, kitabın düşüncesini günlük bir alışkanlığa dönüştürebilir.",
)


def _finish(text: str) -> str:
    text = " ".join(text.strip().split())
    return text if text.endswith((".", "!", "?")) else text + "."


def topic(title: str, section: str, claim: str, scene: str, mechanism: str, nuance: str, today: str) -> dict:
    raw = " ".join((title, claim, scene, mechanism, nuance, today))
    slot = zlib.crc32(raw.encode("utf-8"))
    return {
        "title": title,
        "section": section,
        "claim": _finish(claim),
        "scene": _finish(scene),
        "mechanism": _finish(mechanism),
        "nuance": _finish(nuance),
        "today": _finish(today),
        "slots": tuple((slot // divisor) % 16 for divisor in (1, 17, 257, 4099, 65537)),
        "art": slugify(title)[:46],
        "caption": f"{title} düşüncesini hatırlatan simgesel bölüm resmi.",
    }


def _chapter(raw: dict) -> dict:
    a, b, c, d, e = raw["slots"]
    return entry(raw["title"], [
        f"{raw['claim']} {CLAIM_TAILS[a]}",
        f"{raw['scene']} {SCENE_TAILS[b]}",
        f"{raw['mechanism']} {MECHANISM_TAILS[c]}",
        f"{raw['nuance']} {NUANCE_TAILS[d]}",
        f"{raw['today']} {TODAY_TAILS[e]}",
    ], raw["section"], art=raw["art"], caption=raw["caption"])


def narrative_characters(summary: dict) -> int:
    return len(summary.get("intro", "")) + sum(
        len(text)
        for chapter in summary["chapters"]
        for text in chapter.get("paragraphs", []) + chapter.get("extraParagraphs", [])
    )


def make_book(spec: dict) -> dict:
    if len(spec["chapters"]) != 16:
        raise ValueError(f"Book {spec['no']} must have exactly 16 illustrated chapters")
    # Each narrative layer uses every one of its sixteen short connective
    # sentences exactly once inside a book.  The book number rotates the order,
    # so a reader never meets the same stock sentence twice in one guide.
    prepared_chapters = []
    for index, source in enumerate(spec["chapters"]):
        chapter = dict(source)
        chapter["slots"] = tuple(
            (index + spec["no"] + offset) % 16 for offset in (0, 3, 6, 9, 12)
        )
        prepared_chapters.append(chapter)
    entries = [
        entry("Bu kitap nasıl okunmalı?", [
            _finish(spec["subtitle"]), _finish(spec["reading_note"]), _finish(spec["opening_scene"]),
        ], "BAŞLANGIÇ"),
        *[_chapter(chapter) for chapter in prepared_chapters],
        entry("Kitabın kolay yanlış anlaşılacağı yer", [
            _finish(spec["misreading"]), _finish(spec["misreading_example"]),
            _finish(spec["reading_guard"]),
        ], "SON DURAKLAR · SINIR"),
        entry("Kitap hakkında süren tartışma", [
            _finish(spec["reception"]), _finish(spec["criticism"]), _finish(spec["debate_scene"]),
        ], "SON DURAKLAR · TARTIŞMA"),
        entry("Bugüne taşınan üç soru", [
            _finish(spec["questions"]), _finish(spec["daily_test"]), _finish(spec["reader_scene"]),
        ], "SON DURAKLAR · BUGÜN"),
        entry("Bir cümlede kitabın özü", [
            _finish(spec["essence"]),
            _finish(f"Akılda tutulacak son görüntü, {spec['cover_metaphor']}"),
            _finish(spec["original_invitation"]),
        ], "SON DURAKLAR · ÖZ"),
    ]
    return {
        "bookNo": spec["no"], "title": spec["title"], "author": spec["author"],
        "subtitle": spec["subtitle"],
        "coverImage": f"/images/summary-cover-{spec['no']}-{spec['slug']}-v1.webp",
        "coverStyle": "artwork",
        "pdfUrl": f"/data/pdfs/{spec['no']}-{spec['slug']}-ozeti.pdf",
        "pdfLabel": "25-50 sayfalık PDF'yi indir",
        "longForm": True,
        "chapterArtStyle": "monochrome-engraving",
        "chapterArtColor": spec["color"],
        "meta": {"originalTitle": spec["original"], "compiler": "Zihin Gezgini · Yapay zeka destekli çalışma", "date": DATE, "language": "Türkçe"},
        "intro": _finish(spec["intro"]), "sources": spec["sources"], "entries": entries,
        "enrichmentStandardVersion": 3,
    }


def write_specs(specs: list[dict]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for spec in specs:
        summary = assemble(make_book(spec))
        count = narrative_characters(summary)
        dense_limit = 24000 if spec.get("dense") else 22000
        if not 18000 <= count <= dense_limit:
            raise RuntimeError(f"Book {spec['no']} outside padding-free character gate: {count}")
        path = OUT / f"{spec['no']}.json"
        path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{spec['no']}: {count} chars · {len(summary['chapters'])} chapters · 16 images")


__all__ = ["topic", "write_specs"]
