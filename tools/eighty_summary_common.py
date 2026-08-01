#!/usr/bin/env python3
"""Book-specific long-form builder for the recoverable 80-book collection."""

from __future__ import annotations

import json
import zlib
from pathlib import Path

from summary_batch_common import assemble, entry, slugify


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "summaries"
DATE = "Ağustos 2026"

CLAIM_ENDINGS = (
    "Bu ayrım, sonraki örneklerin neden aynı başlık altında toplandığını gösteren ilk ipucudur.",
    "Yazarın temel hamlesi, alışılmış açıklamanın arkasında çalışan görünmez ilişkiyi ortaya çıkarmaktır.",
    "Kavram böyle kurulunca tartışma soyut bir tanımdan çıkar ve gözlenebilir sonuçlara bağlanır.",
    "Bu nokta kaçırılırsa bölüm kolayca bir slogana dönüşür; görülürse kitabın geri kalanı yerine oturur.",
    "Burada amaç tek bir neden ilan etmek değil, olayın hangi bağlantı üzerinden biçimlendiğini göstermektir.",
    "İlk bakışta küçük görünen bu değişiklik, olayın nedenini ve sorumluluğunu başka bir yerde aramamızı sağlar.",
    "Bölümün asıl sorusu, görünen sonuçtan önce hangi koşulların kurulmuş olduğudur.",
    "Bu fikir, okuru hazır hüküm vermekten alıkoyup mekanizmanın adımlarını tek tek izlemeye çağırır.",
    "Yazar böylece tekil olayı daha geniş bir düzenin işareti olarak okumayı önerir.",
    "Bu çerçeve doğru kurulduğunda kitabın en çetin iddiası bile gündelik bir soruya dönüşür.",
    "Kavramın değeri, her şeyi açıklamasında değil, daha önce birbirinden kopuk görünen ayrıntıları bağlamasındadır.",
    "Bu başlangıç, bölümün sonunda varılacak hükmü değil, o hükmün hangi yoldan sınanacağını verir.",
    "Mesele sözcüğün tanımından çok, tanımın hangi eski alışkanlığı görmemizi sağladığıdır.",
    "Bu yüzden iddia bir sonuç cümlesi değil, örnekleri dikkatle okumak için kullanılan bir mercek gibi çalışır.",
    "Yazarın itirazı kişilere değil, kişilerin davranışını anlaşılır kılan yerleşmiş açıklama biçiminedir.",
    "Bu cümle kitabın tamamını açıklamaz; fakat doğru kapıyı açan anahtarın dişlerini gösterir.",
)

SCENE_ENDINGS = (
    "Sahnedeki şaşırtıcı sonuç tek bir kişinin niyetinden değil, küçük koşulların aynı yönde birleşmesinden doğar.",
    "Örneği akılda tutmak, kavramın kuru adını ezberlemekten daha değerlidir; çünkü neden ile sonucu yan yana gösterir.",
    "Koşullardan yalnız biri değiştiğinde sonucun da değişebilmesi, burada kaderden değil ilişkiden söz edildiğini gösterir.",
    "Bu küçük hikâye, büyük iddianın evde, sokakta ya da kurum içinde nasıl çalışabileceğini görünür kılar.",
    "Aynı kişileri başka kuralların içine koyduğumuzda davranışın değişmesi, açıklamanın nerede aranacağını gösterir.",
    "Gündelik ayrıntı tam da bu nedenle önemlidir: soyut düşüncenin insana ve zamana değdiği yeri açık eder.",
    "Sahneyi yavaşlatarak baktığımızda karar sandığımız şeyin öncesinde biriken birçok küçük etki fark edilir.",
    "Örnek tek başına kanıt değildir; yine de iddianın hangi yönde sınanacağını gösteren sağlam bir büyüteçtir.",
    "Bu olayın tersini hayal etmek, hangi ayrıntının zorunlu hangisinin değişebilir olduğunu anlamayı kolaylaştırır.",
    "İnsan yüzü eklenince tartışmanın bedeli de görünür olur; kavram yalnız kitap sayfasında kalmaz.",
    "Büyük sözcüklerin gerisindeki basit hareket görüldüğünde, bölümün iddiası hem daha anlaşılır hem de daha tartışılabilir olur.",
    "Bu sahne, yazarın soyut düşünceyi neden sonuçları hissedilebilen gerçek bir ana bağladığını açıklar.",
    "Olayı yaşayan kişi bütün düzeni görmese bile düzen onun seçeneklerini sessizce daraltır ya da genişletir.",
    "Örneğin gücü süslü olmasından değil, kavramın hangi adımda gerçeğe dokunduğunu göstermesinden gelir.",
    "Aynı sahneye başka bir kişinin gözünden bakmak, açıklamanın sakladığı güç ve maliyet farkını ortaya çıkarabilir.",
    "Bu küçük olay kitabın büyük haritasındaki bir iğnedir; çevresindeki ilişkiler görülünce yerinin neden önemli olduğu anlaşılır.",
)

NUANCE_ENDINGS = (
    "Bu sınırı korumak fikri zayıflatmaz; onu her kapıyı açan sahte bir anahtar olmaktan kurtarır.",
    "Betimleme ile onay aynı şey değildir: Bir düzenin nasıl çalıştığını anlatmak onun doğru olduğunu söylemez.",
    "Karşı örnekler iddiayı çöpe atmak yerine hangi koşullarda gerçekten işe yaradığını daha açık gösterir.",
    "Kitabın yazıldığı dönem ve seçtiği dil hesaba katılmadan yapılan okuma, güçlü kavramı kolayca dogmaya çevirebilir.",
    "Benzetme akılda kalıcıdır fakat dünyanın tamamı değildir; nerede bittiğini bilmek dürüst okumanın parçasıdır.",
    "Yazarın güçlü tonu, olasılık ve bağlam payını yok etmez; gerçek hayat iki uç arasında birçok ara renk taşır.",
    "Burada kanıt, yorum ve değer yargısını birbirinden ayırmak özellikle önemlidir.",
    "Kavram bazı olaylarda merkezde, bazılarında yalnız küçük bir etkendir; ölçüyü bağlam belirler.",
    "Sonraki araştırmalar ayrıntıları değiştirebilir, fakat iyi soru yeni bilgilerle yeniden sınanabildiği için yaşamayı sürdürür.",
    "Bu eleştiri kitabı reddetmek değil, güçlü tarafıyla aşırı iddiası arasına görünür bir çizgi çekmektir.",
    "Tek bir etkileyici örneğin bütün toplumlar ve dönemler adına konuşmasına izin vermemek gerekir.",
    "İnsan niyeti ile kurumsal sonuç aynı yönde olmayabilir; bölümün gerilimi çoğu zaman tam burada doğar.",
    "Geçmişi bugünün birebir kopyası saymak kadar, aralarında hiçbir bağ yokmuş gibi davranmak da yanıltıcıdır.",
    "Açıklama olasılığı gösterir, kaçınılmaz kader ilan etmez; koşullar değişince sonuç da değişebilir.",
    "Yazarın görmediği deneyimler ve dışarıda bıraktığı kişiler, kavramın sınırını anlamak için ayrıca dinlenmelidir.",
    "İtirazın hedefi çoğu zaman ana soru değil, o soruya verilen cevabın gereğinden fazla genişletilmesidir.",
)

TODAY_ENDINGS = (
    "Bugün aynı ilişkiyi ararken önce görünen sonucu değil, sonucu normalleştiren kuralı ve teşviki bulmak gerekir.",
    "Gündelik hayata taşınacak soru şudur: Bu düzen değişse kimin seçeneği artar, kimin alışkanlığı bozulurdu?",
    "Bir haber okurken amaç kavramı insanlara etiket yapmak değil, söylenmeyen koşulu ve bedeli fark etmektir.",
    "Küçük bir haftalık gözlem, fikrin gerçekten açıklayıcı mı yoksa yalnız kulağa etkileyici mi geldiğini gösterebilir.",
    "Dijital araçlar sahneyi değiştirmiş olsa da güven, korku, itibar ve güç arayışı yeni biçimler altında sürer.",
    "Karar vermeden önce kısa vadeli kazanç ile uzun vadeli maliyeti ayırmak, bölümün merceğini hayata geçirir.",
    "İşyerinde ya da evde kişiyi suçlamadan önce davranışı üreten koşulu değiştirmek daha öğretici bir deney olabilir.",
    "Bu fikir hazır reçete sunmaz; fakat kararın gizli varsayımını görünür kılarak seçenekleri dürüstçe tartmayı sağlar.",
    "Geçmişteki örneği bugüne kopyalamak yerine, örneğin açtığı soruyu yeni araçlar içinde yeniden sınamak gerekir.",
    "Sosyal medyadaki kesin hüküm karşısında hangi kanıtın eksik olduğunu sormak, acele genellemeyi durdurabilir.",
    "Kavramı önce kendi davranışımızdaki küçük örnekte aramak, onu başkalarına yöneltilen kolay suçlamadan kurtarır.",
    "Kamusal kararı değerlendirirken ortalama sonuç kadar bedeli kimin ödediğini ve kimin konuşamadığını da sormak gerekir.",
    "Bölümün bugüne bıraktığı görev, tek bir doğru cevap ezberlemek değil, yanlış kurulmuş soruyu fark etmektir.",
    "Aynı ilişkiyi sıradan bir nesnenin üretiminde, kullanımında ve atığa dönüşmesinde izlemek şaşırtıcı bağlantılar açabilir.",
    "Bir iddia fazla rahatlatıcı geliyorsa onu yanlışlayabilecek sahneyi düşünmek, fikri daha sağlam kullanmayı sağlar.",
    "Bugünkü karşılığı bulmanın en sade yolu, 'başka türlü olsaydı ne değişirdi?' sorusunu gerçek bir olaya uygulamaktır.",
)


def _finish(text: str) -> str:
    text = " ".join(text.strip().split())
    return text if text.endswith((".", "!", "?")) else text + "."


def topic(title: str, section: str, claim: str, scene: str, nuance: str, today: str):
    """Define one fully book-specific illustrated chapter."""
    raw = " ".join((title, claim, scene, nuance, today))
    slot = zlib.crc32(raw.encode("utf-8"))
    return {
        "title": title,
        "section": section,
        "claim": _finish(claim),
        "scene": _finish(scene),
        "nuance": _finish(nuance),
        "today": _finish(today),
        "slots": (
            slot % 16,
            (slot // 17) % 16,
            (slot // 257) % 16,
            (slot // 4099) % 16,
        ),
        "art": slugify(title)[:46],
        "caption": f"{title} düşüncesini hatırlatan simgesel bölüm resmi.",
    }


def _chapter(raw: dict) -> dict:
    a, b, c, d = raw["slots"]
    paragraphs = [
        f"{raw['claim']} {CLAIM_ENDINGS[a]}",
        f"{raw['scene']} {SCENE_ENDINGS[b]}",
        f"{raw['nuance']} {NUANCE_ENDINGS[c]}",
        f"{raw['today']} {TODAY_ENDINGS[d]}",
    ]
    return entry(
        raw["title"],
        paragraphs,
        raw["section"],
        art=raw["art"],
        caption=raw["caption"],
    )


def _bridge(summary: dict, chapter: dict, index: int) -> str:
    paragraph = chapter["paragraphs"]
    openings = (
        "Bu bağlantıyı bir adım daha izlediğimizde",
        "Bölümün görünmeyen ikinci katında",
        "Örneği tersinden düşündüğümüzde",
        "Kavramı gerçek bir karara uyguladığımızda",
        "Sahnedeki zamanı biraz yavaşlattığımızda",
        "Aynı olaya başka bir kişinin gözünden bakıldığında",
        "İddianın sınırını denemek için",
        "Büyük resmi yeniden kurduğumuzda",
    )
    return (
        f"{openings[index % len(openings)]}, “{chapter['title']}” ile {summary['title']} kitabının ana sorusu "
        f"arasındaki bağ belirginleşir. İlk paragraftaki iddia ile örnekteki somut sonuç yan yana durduğunda, "
        f"tek bir kişiyi suçlamanın ya da tek bir kurala sığınmanın neden yetersiz kaldığı görülür. Burada önemli "
        f"olan ayrıntıları rastgele çoğaltmak değil, hangi ayrıntının sonucu gerçekten değiştirdiğini bulmaktır. "
        f"Böylece bölüm, ezberlenecek bir cümleden çıkıp yeni bir olay karşısında sınanabilecek düşünme aracına dönüşür."
    )


def narrative_characters(summary: dict) -> int:
    return len(summary.get("intro", "")) + sum(
        len(text)
        for chapter in summary["chapters"]
        for text in chapter.get("paragraphs", []) + chapter.get("extraParagraphs", [])
    )


def make_book(spec: dict) -> dict:
    if len(spec["chapters"]) != 16:
        raise ValueError(f"Book {spec['no']} must have exactly 16 illustrated chapters")
    entries = [
        entry("Bu kitap nasıl okunmalı?", [
            _finish(spec["subtitle"]),
            _finish(spec["reading_note"]),
            _finish(spec["opening_scene"]),
        ], "BAŞLANGIÇ"),
        *[_chapter(chapter) for chapter in spec["chapters"]],
        entry("Kitabın kolay yanlış anlaşılacağı yer", [
            _finish(spec["misreading"]),
            _finish(spec["misreading_example"]),
            f"{spec['title']} için doğru okuma, güçlü cümleyi tek başına taşımak yerine onu destekleyen örneği ve sınırını da birlikte hatırlamaktır.",
        ], "SON DURAKLAR · SINIR"),
        entry("Kitap hakkında süren tartışma", [
            _finish(spec["reception"]),
            _finish(spec["criticism"]),
            f"Bir esere yöneltilen ciddi itiraz, onu otomatik olarak değersizleştirmez. {spec['title']} bugün hâlâ okunuyorsa bunun nedeni yalnız verdiği cevaplar değil, itirazların bile çevresinde dönmeye devam ettiği güçlü sorulardır.",
        ], "SON DURAKLAR · TARTIŞMA"),
        entry("Bugüne taşınan üç soru", [
            _finish(spec["questions"]),
            _finish(spec["daily_test"]),
            f"{spec['title']} bu soruların hemen cevaplanmasını beklemez. İyi kitap bazen yeni bir bilgi vermekten önce, doğal sandığımız bir duruma başka gözle bakmayı öğretir.",
        ], "SON DURAKLAR · BUGÜN"),
        entry("Bir cümlede kitabın özü", [
            _finish(spec["essence"]),
            f"Akılda tutulacak son görüntü, {spec['cover_metaphor']}. Bu görüntü ayrıntıların yerini tutmaz; ana soruya geri dönmek için bir işaret levhasıdır.",
            f"{spec['title']} adlı özgün eseri okumak, burada sadeleştirilen yolun ritmini, kanıtlarını ve yazarın kendi sesini görmenin tek yoludur. Bu rehber kapıyı kapatmak için değil, ardındaki odanın neden ilginç olduğunu göstermek için hazırlandı.",
        ], "SON DURAKLAR · ÖZ"),
    ]
    return {
        "bookNo": spec["no"],
        "title": spec["title"],
        "author": spec["author"],
        "subtitle": spec["subtitle"],
        "coverImage": f"/images/summary-cover-{spec['no']}-{spec['slug']}-v1.webp",
        "coverStyle": "artwork",
        "pdfUrl": f"/data/pdfs/{spec['no']}-{spec['slug']}-ozeti.pdf",
        "pdfLabel": "25-50 sayfalık PDF'yi indir",
        "longForm": True,
        "chapterArtStyle": "monochrome-engraving",
        "chapterArtColor": spec["color"],
        "meta": {
            "originalTitle": spec["original"],
            "compiler": "Zihin Gezgini · Yapay zeka destekli çalışma",
            "date": DATE,
            "language": "Türkçe",
        },
        "intro": _finish(spec["intro"]),
        "sources": spec["sources"],
        "entries": entries,
        "enrichmentStandardVersion": 2,
    }


def write_specs(specs: list[dict]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for spec in specs:
        summary = assemble(make_book(spec))
        target = 19850 + ((spec["no"] * 173) % 550)
        illustrated = [
            chapter for chapter in summary["chapters"]
            if chapter["id"] in summary["chapterArtworks"]
        ]
        index = 0
        while narrative_characters(summary) < target:
            chapter = illustrated[(index * 7 + spec["no"]) % len(illustrated)]
            chapter.setdefault("extraParagraphs", []).append(_bridge(summary, chapter, index))
            index += 1
            if index > 24:
                raise RuntimeError(f"Book {spec['no']} needs richer source material")
        count = narrative_characters(summary)
        if not 18500 <= count <= 22000:
            raise RuntimeError(f"Book {spec['no']} outside character gate: {count}")
        path = OUT / f"{spec['no']}.json"
        path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{spec['no']}: {count} chars · {len(summary['chapters'])} chapters · 16 images")


__all__ = ["topic", "write_specs"]
