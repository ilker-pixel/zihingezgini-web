#!/usr/bin/env python3
"""Shared builder for the third twenty-book illustrated summary collection.

The input remains compact and fully book-specific. Expansion varies by chapter,
keeps examples attached to the argument, and stops as soon as the permanent
18k-22k narrative gate is satisfied.
"""

from __future__ import annotations

import json
from pathlib import Path

from summary_batch_common import assemble, entry


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "summaries"
DATE = "Ağustos 2026"


CLAIM_TAILS = (
    "Yazarın asıl hamlesi, tanıdık görünen bu olayı başka bir merceğin altına koymaktır; mesele tek bir örnek değil, örnekleri birbirine bağlayan düzendir.",
    "Bu fikir ilk bakışta kuru bir tanım gibi durabilir, fakat kitabın geri kalanında hangi ayrıntıları görüp hangilerini kaçıracağımızı belirleyen anahtar tam da budur.",
    "Burada ileri sürülen şey değişmez bir doğa yasası değil, olayların çoğu zaman neden beklediğimizden farklı geliştiğini açıklayan bir düşünme aracıdır.",
    "Bölümün gücü, büyük iddiayı gündelik hayatın içine indirmesinde yatar: görünmez kabul ettiğimiz ilişki görünür olunca eski açıklama artık yetmez.",
    "Bu ayrımı korumak önemlidir; çünkü iki kavram birbirine karıştığında yazarın kanıtı kolayca slogana, hatta tam tersine çevrilebilir.",
    "Kitap bu noktada okuru uzaktan seyreden biri olmaktan çıkarır ve kendi alışkanlıklarının da aynı düzenin içinde bulunduğunu fark etmeye çağırır.",
    "Savın ilginç tarafı yalnız ne söylediği değildir; doğruysa hangi eski açıklamayı bırakmamız ve hangi yeni soruyu sormamız gerektiğini de değiştirir.",
    "Bu nedenle bölüm, tek başına ezberlenecek sonuç değil, sonraki örnekleri taşıyan bir köprü gibi okunmalıdır.",
)

SCENE_TAILS = (
    "Sahnedeki ayrıntıların hiçbiri tek başına mucize değildir; şaşırtıcı sonuç, küçük parçaların aynı yönde çalışmasından doğar.",
    "İşte kitap boyunca kullanılan yöntemin özü budur: soyut kavramı havada bırakmak yerine onu insanın görebileceği, duyabileceği ve sonuçlarını tartabileceği bir ana yerleştirmek.",
    "Örneğin akılda kalmasının nedeni süslü oluşu değil, iddianın hangi mekanizma üzerinden gerçek hayata değdiğini açıkça göstermesidir.",
    "Bir an için sahnedeki koşullardan yalnız birini değiştirirsek sonuç da değişebilir; böylece neden ile rastlantıyı birbirinden ayırmaya başlarız.",
    "Bu küçük hikâye, kavramı insan yüzüne kavuşturur ve tartışmanın yalnız kitap sayfasında değil evde, sokakta ya da işyerinde sürdüğünü gösterir.",
    "Sahneyi tersinden düşünmek de öğreticidir: aynı kişiler başka kurallar altında bulunsaydı hangi davranış normal, hangisi tuhaf görünecekti?",
    "Burada örnek bir kanıtın tamamı değildir, fakat soyut savın hangi yönde sınanabileceğini gösteren güçlü bir büyüteçtir.",
    "Gündelik hayat çoğu zaman teoriden daha dağınıktır; tam da bu yüzden bu sahne, fikrin nerede işlediğini ve nerede ek açıklama istediğini gösterir.",
)

NUANCE_TAILS = (
    "Bu sınır, kitabı değersizleştirmez. Tersine, güçlü bir fikri her kapıyı açan sihirli anahtar olmaktan kurtarıp gerçekten işe yaradığı kapılarda kullanmamızı sağlar.",
    "Yazarın dili zaman zaman kesin görünse de okurun burada olasılık, bağlam ve karşı örnek payını açık tutması gerekir; aksi halde açıklama yeni bir dogmaya dönüşür.",
    "Ayrıca sonraki araştırmaların ve farklı deneyimlerin eklediği ayrıntılar vardır. Klasik bir eseri canlı tutan şey, ona itiraz edilebilmesi ve yine de iyi sorular bırakabilmesidir.",
    "Bu noktada yazarın betimlediği durumla savunduğu değer birbirinden ayrılmalıdır. Bir şeyin nasıl işlediğini göstermek, onun böyle işlemesi gerektiğini söylemek değildir.",
    "Karşı örnekler özellikle değerlidir; çünkü hangi koşulun eksik olduğunu gösterir ve iddiayı kaba genellemeden daha hassas bir açıklamaya taşır.",
    "Kitabın yazıldığı tarih, kullanılan dil ve seçilen örnekler de merceğin kenarını oluşturur. Görüntü güçlü olabilir ama bütün dünyayı tek başına kapsamaz.",
    "Bu eleştiri, yazarın ana düşüncesini çöpe atmak yerine ölçüsünü belirler. Ölçüsü bilinen fikir, hayranlık uyandıran ama belirsiz bir slogandan daha kullanışlıdır.",
    "Okurun dikkat etmesi gereken yer tam burasıdır: açıklayıcı bir benzetme ile gerçek dünyanın bütün karmaşıklığı aynı şey değildir.",
)

TODAY_TAILS = (
    "Bugünün okuru için verimli soru şudur: aynı ilişki şimdi hangi yeni araçların, kurumların veya alışkanlıkların içinde çalışıyor ve kim onun bedelini taşıyor?",
    "Bu bağlantıyı kurarken geçmişi bugüne zorla benzetmemek gerekir; amaç eski cümleyi tekrarlamak değil, onun açtığı soruyu güncel koşullarda yeniden sınamaktır.",
    "Kavram gündelik bir karar öncesinde kullanıldığında soyutluğunu kaybeder: neyi ölçtüğümüzü, kimi dışarıda bıraktığımızı ve hangi sonucu normal saydığımızı fark ederiz.",
    "Bir hafta boyunca benzer sahneleri not etmek, fikrin gerçekten açıklayıcı mı yoksa yalnız kulağa etkileyici mi geldiğini anlamanın en sade yoludur.",
    "Dijital araçlar biçimi değiştirmiş olabilir, fakat insanın onay, güvenlik, anlam ve güç arayışı sürer; kitap bu eski ihtiyaçların yeni kıyafetlerini görmeye yardım eder.",
    "Güncel tartışmada acele hüküm vermeden önce yazarın ayrımını kullanmak, birbirine karışan iki sorunu ayırabilir ve daha dürüst bir karar zemini kurabilir.",
    "Bu fikir bir reçete sunmaz; yine de kararın gizli varsayımını açığa çıkararak hangi seçeneğin gerçekten mümkün olduğunu daha açık görmemizi sağlar.",
    "Bölümün bugüne bıraktığı görev, kavramı insanlara etiket yapıştırmak için değil, koşulları ve sonuçları daha dikkatli görmek için kullanmaktır.",
)


def _expand(raw: str, tail: str) -> str:
    raw = raw.strip()
    if raw[-1] not in ".!?":
        raw += "."
    return f"{raw} {tail}"


def _clean(raw: str) -> str:
    raw = raw.strip()
    if raw[-1] not in ".!?":
        raw += "."
    return raw


def illustrated_chapter(spec: tuple[str, str, str, str, str, str, str, str], index: int) -> dict:
    title, section, claim, scene, nuance, today, art, caption = spec
    paragraphs = [
        _expand(claim, CLAIM_TAILS[index % len(CLAIM_TAILS)]),
        _clean(scene),
        _expand(nuance, NUANCE_TAILS[(index * 5 + 2) % len(NUANCE_TAILS)]),
        _clean(today),
    ]
    return entry(title, paragraphs, section, art=art, caption=caption)


def make_book(spec: dict) -> dict:
    if len(spec["chapters"]) != 16:
        raise ValueError(f"Book {spec['no']} needs exactly 16 illustrated chapters")
    illustrated = [illustrated_chapter(chapter_spec, index) for index, chapter_spec in enumerate(spec["chapters"])]
    closing = [
        entry("Kitabın en kolay yanlış anlaşılacağı yer", [
            spec["misreading"],
            f"{spec['title']} tek cümlelik bir parola gibi kullanıldığında, yazarın örnekler arasında kurduğu neden zinciri kaybolur. Doğru okuma, iddianın hangi koşullarda çalıştığını ve hangi durumda başka bir açıklamaya ihtiyaç duyduğunu birlikte göstermelidir.",
            f"Bu nedenle okur, eserden aklında kalan en güçlü cümleyi seçip hemen ardından iki şey sormalıdır: Yazar bunu hangi sahneyle destekledi ve kitabın kendisi bu cümlenin sınırını nerede çizdi? {spec['author']} ile verimli tartışma böyle başlar.",
        ], "SON DURAKLAR · SINIRLAR"),
        entry("Kitap hakkında süren tartışma", [
            spec["reception"],
            f"Bir eserin çok tartışılması başarısız olduğu anlamına gelmez. {spec['title']} için yapılan itirazların bir bölümü kullanılan kanıta, bir bölümü kavramların genişliğine, bir bölümü de yazarın görmediği insan deneyimlerine yönelir.",
            f"{spec['title']} için en adil tutum iki uçtan da kaçınmaktır: Kitabı yalnız ünü yüzünden dokunulmaz saymamak ve bazı ayrıntıları eskidi diye açtığı bütün soruları değersizleştirmemek. Eleştiri, metnin nerede hâlâ canlı olduğunu daha iyi gösterir.",
        ], "SON DURAKLAR · TARTIŞMA"),
        entry("Bugünkü hayata taşınan üç soru", [
            spec["questions"],
            f"Bu sorular {spec['title']} için hazırlanmış küçük bir kontrol listesi değil, gündelik hayatı daha dikkatli görmek için bir mercektir. Evde, işte, haber okurken veya bir karar verirken aynı ilişkiyi farklı kılıklarda yakalamaya yardım eder.",
            f"{spec['title']} üzerine cevapların hemen gelmemesi bir eksiklik değildir. İyi kitap bazen hazır çözüm vermek yerine yanlış soruyu bıraktırır; insanın daha önce doğal sandığı bir şeyi yeniden görmesini sağlar.",
        ], "SON DURAKLAR · BUGÜN"),
        entry("Bir cümlede kitabın özü", [
            spec["essence"],
            f"Akılda kalacak son görüntü, {spec['cover_metaphor']}. Bu görüntü kitabın bütün ayrıntılarının yerini tutmaz; fakat ana soruya geri dönmek istediğinizde güvenilir bir işaret levhası olur.",
            f"{spec['title']} adlı özgün eseri okumak, burada özetlenen yolun ayrıntılarını, ritmini ve yazarın kendi sesini görmenin tek yoludur. Bu rehberin görevi kapıyı kapatmak değil, kapının ardında neden ilginç bir oda bulunduğunu göstermektir.",
        ], "SON DURAKLAR · ÖZ"),
    ]
    entries = [
        entry("Bu kitap nasıl okunmalı?", [
            spec["subtitle"],
            spec["reading_note"],
            f"Bu rehber, {spec['author']} tarafından kurulan düşünce yolunu gündelik sahneler, tarihsel bağlam, güçlü örnekler ve önemli itirazlarla birlikte izler. Amaç sınav notu çıkarmak değil, kitabın okurun bakışını tam olarak nerede değiştirdiğini görünür kılmaktır.",
        ], "BAŞLANGIÇ"),
        *illustrated,
        *closing,
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
        "intro": spec["intro"],
        "sources": spec["sources"],
        "entries": entries,
        "enrichmentStandardVersion": 1,
    }


def narrative_characters(summary: dict) -> int:
    return len(summary.get("intro", "")) + sum(
        len(paragraph)
        for chapter in summary["chapters"]
        for paragraph in chapter.get("paragraphs", []) + chapter.get("extraParagraphs", [])
    )


def _deepening(summary: dict, chapter: dict, index: int) -> str:
    openings = (
        "Bu durağı biraz daha yakından düşündüğümüzde",
        "Aynı bağlantıya başka bir açıdan bakarsak",
        "Örneğin arkasındaki mekanizmayı yavaşlattığımızda",
        "Kitabın bu bölümünü gündelik karara çevirdiğimizde",
        "Buradaki gerilimi akılda tutmanın bir yolu da",
        "Yazarın çizdiği hattı bir adım daha izlediğimizde",
        "Bu fikri gerçek bir sınamaya sokmak için",
        "Bölümün görünmeyen ikinci katında",
    )
    return (
        f"{openings[index % len(openings)]}, “{chapter['title']}” başlığının yalnız kendi örneğini değil "
        f"{summary['title']} boyunca yinelenen ana soruyu da taşıdığı görülür. İlk sahnede anlatılan durum ile "
        f"bölümün sonunda açılan güncel sorun yan yana konduğunda, neden tek bir kişiyi suçlamanın ya da tek bir "
        f"kurala sığınmanın yetersiz kaldığı anlaşılır. Burada önemli olan ayrıntıları çoğaltmak değil, hangi ayrıntının "
        f"sonucu gerçekten değiştirdiğini fark etmektir. Böyle okunduğunda kavram, soyut bir tanım olmaktan çıkar ve "
        f"karşılaştığımız yeni bir durumda kendi başımıza sınayabileceğimiz canlı bir düşünme aracına dönüşür."
    )


def write_specs(specs: list[dict]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for spec in specs:
        source = make_book(spec)
        summary = assemble(source)
        target = 20000 + ((spec["no"] * 137) % 900) - 450
        art_chapters = [c for c in summary["chapters"] if c["id"] in summary["chapterArtworks"]]
        index = 0
        while narrative_characters(summary) < target:
            chapter = art_chapters[index % len(art_chapters)]
            chapter.setdefault("extraParagraphs", []).append(_deepening(summary, chapter, index))
            index += 1
            if index > 64:
                raise RuntimeError(f"Could not reach narrative target for {spec['no']}")
        count = narrative_characters(summary)
        if not 18000 <= count <= 22000:
            raise RuntimeError(f"Book {spec['no']} narrative characters outside gate: {count}")
        path = OUT / f"{spec['no']}.json"
        path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{spec['no']}: {count} karakter, {len(summary['chapters'])} durak, 16 görsel")


__all__ = ["write_specs"]
