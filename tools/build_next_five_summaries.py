#!/usr/bin/env python3
"""Build the second set of five long-form illustrated summary JSON files.

The prose is kept here as an auditable source. The script only assembles the
handwritten material into the site's established summary schema.
"""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "summaries"


def slugify(value: str) -> str:
    table = str.maketrans({
        "ç": "c", "Ç": "c", "ğ": "g", "Ğ": "g", "ı": "i", "İ": "i",
        "ö": "o", "Ö": "o", "ş": "s", "Ş": "s", "ü": "u", "Ü": "u",
    })
    normalized = unicodedata.normalize("NFKD", value.translate(table))
    normalized = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    return re.sub(r"[^a-zA-Z0-9]+", "-", normalized.lower()).strip("-")


def entry(title: str, paragraphs: list[str], section: str, *, art: str = "", caption: str = "") -> dict:
    return {"title": title, "paragraphs": paragraphs, "section": section, "art": art, "caption": caption}


def assemble(source: dict) -> dict:
    book = dict(source)
    raw_entries = book.pop("entries")
    chapters = []
    artworks = {}
    art_index = 0
    for index, raw in enumerate(raw_entries, 1):
        chapter_id = f"durak-{index:02d}-{slugify(raw['title'])}"
        chapters.append({
            "id": chapter_id,
            "section": raw["section"],
            "title": raw["title"],
            "paragraphs": raw["paragraphs"],
        })
        if raw.get("art"):
            art_index += 1
            image = f"/images/summary-art-{book['bookNo']}-chapter-{art_index:02d}-{raw['art']}-v1.webp"
            artworks[chapter_id] = {"image": image, "imageCaption": raw["caption"]}
    if art_index != 16:
        raise ValueError(f"Book {book['bookNo']} has {art_index} artworks; expected 16")
    book["chapters"] = chapters
    book["chapterArtworks"] = artworks
    return book


BOOKS: list[dict] = []


BOOKS.append({
    "bookNo": 2,
    "title": "Kozmos",
    "author": "Carl Sagan",
    "subtitle": "İnsanın kozmik adresini, yıldızlardan gelen maddesini ve bilginin merakla nasıl büyüdüğünü gündelik benzetmelerle anlatan görsel yolculuk.",
    "coverImage": "/images/optimized/summary-art-2-kozmos-v2-960.webp",
    "coverStyle": "artwork",
    "pdfUrl": "/data/pdfs/2-kozmos-ozeti.pdf",
    "pdfLabel": "25-50 sayfalık PDF'yi indir",
    "longForm": True,
    "chapterArtStyle": "monochrome-engraving",
    "chapterArtColor": "#315B68",
    "meta": {
        "originalTitle": "Cosmos",
        "compiler": "Zihin Gezgini · Yapay zeka destekli çalışma",
        "date": "Temmuz 2026",
        "language": "Türkçe",
    },
    "intro": "Carl Sagan gökyüzüne bakarken yalnız yıldızları anlatmaz. Bir fikrin nasıl doğduğunu, insanların yanlış yollara sapıp yeniden nasıl ölçmeye başladığını ve küçük bir gezegenin sakinlerinin evrendeki yerlerini öğrenirken neden daha sorumlu olması gerektiğini anlatır. Bu rehber kitabın on üç bölümlük büyük yürüyüşünü koruyor, 1980'den sonra değişen bilimsel ayrıntıları güncel bilgilerle ayırıyor ve her kavramı gündelik bir görüntüye bağlıyor. Amaç formül ezberlemek değil; evreni öğrenmenin insanın kendine bakışını nasıl değiştirdiğini hissetmektir.",
    "sources": [
        {"id": 1, "title": "Cosmos - resmi yayınevi tanıtımı ve kapsamı", "url": "https://www.penguinrandomhouse.com/books/159730/cosmos-by-carl-sagan/"},
        {"id": 2, "title": "NASA Science - Evren nedir ve yaşı", "url": "https://science.nasa.gov/exoplanets/what-is-the-universe/"},
        {"id": 3, "title": "NASA Science - Erken evren", "url": "https://science.nasa.gov/mission/webb/early-universe/"},
        {"id": 4, "title": "NASA Exoplanet Exploration - Gezegen sistemleri", "url": "https://science.nasa.gov/exoplanets/"},
        {"id": 5, "title": "NASA Astrobiology - Yaşamın kökeni ve evrimi", "url": "https://astrobiology.nasa.gov/about/"},
    ],
    "entries": [
        entry("Bu kitap nasıl okunmalı?", [
            "Kozmos bir ders kitabı gibi doğrusal ilerlemez. Astronomiden biyolojiye, eski İskenderiye'den uzay araçlarına sıçrar. Bu sıçramaların ortak sorusu şudur: İnsan, evren hakkında bildiğini nasıl öğrendi?",
            "Sagan'ın bilimsel ayrıntılarının bir bölümü yazıldığı dönemin bilgisini taşır. Evrenin yaşı, gezegen sayıları ve gözlem araçları konusunda bugün daha ilerideyiz. Yine de kitabın asıl omurgası eskimedi: Merak, kuşku, kanıt ve kozmik ölçekte alçakgönüllülük.",
            "Bu özet, yıldız adlarını ezberletmek yerine on altı sahne kuracak. Her sahne gökyüzündeki büyük fikri mutfak masasına, takvime, kütüphaneye veya yolculuğa yaklaştıracak.",
        ], "BAŞLANGIÇ"),
        entry("Kozmik okyanusun kıyısında", [
            "Gece deniz kenarında durduğunuzu düşünün. Önünüzdeki karanlık suyun sonunu göremezsiniz; yalnız kıyıya vuran birkaç dalgayı seçersiniz. Sagan için insanlık da kozmik okyanusun kıyısındadır. Bildiklerimiz kıyıdaki köpük kadar küçük, fakat o köpüğe bakarak okyanusun kurallarını anlamaya başlamış durumdayız.",
            "Bu benzetme insanı değersizleştirmez. Tam tersine, küçücük bir beynin milyonlarca ışık yılı uzaktaki galaksilerin ne yaptığını anlayabilmesi olağanüstüdür. Evren çok büyük, insan ömrü çok kısa olabilir; merak bu iki ölçek arasında köprü kurar.",
            "Bir teleskop yalnız uzağı büyüten dürbün değildir. Geçmişe bakma makinesidir. Güneş'i sekiz dakika önceki, Andromeda Galaksisi'ni yaklaşık iki buçuk milyon yıl önceki haliyle görürüz. Çünkü ışığın yolculuğu zaman alır.",
            "Gökyüzüne bakmak bu yüzden eski bir fotoğraf albümünü açmaya benzer. Aynı anda farklı yaşlardaki sayfaları görürüz. En uzak ışık, evrenin çok genç olduğu dönemlerden gelir.",
            "İlk hafıza görüntüsü kıyıda duran insandır: Ayağının altında küçük bir kara parçası, önünde sonu görünmeyen ama akılla araştırılabilen bir okyanus.",
        ], "BİRİNCİ KISIM · KOZMİK ADRES", art="cosmic-shore", caption="İnsanlık, uçsuz kozmik okyanusun kıyısında birkaç dalgadan bütün denizi anlamaya çalışan meraklı bir yolcudur."),
        entry("Adresimizi en baştan yazmak", [
            "Bir mektuba yalnız apartman numarası yazarsanız postacı onu bulamaz. Kozmik adres de katman katmandır: Dünya, Güneş Sistemi, Samanyolu, yerel galaksi grubu ve gözlenebilir evren. Her katman, alıştığımız büyüklüğü biraz daha küçültür.",
            "Dünya, Güneş'in çevresindeki gezegenlerden yalnız biridir. Güneş de Samanyolu'ndaki yüz milyarlarca yıldızdan sıradan sayılabilecek bir tanesidir. Samanyolu ise evrendeki sayısız galaksiden biridir. Bu sıralama merkezde olduğumuz fikrini yavaşça söker.",
            "Eski insanlar göğün kendileri için döndüğünü düşünmekte haksız değildi; gözün verdiği ilk izlenim budur. Sabah Güneş doğar, akşam batar. Bilim, ilk izlenimin üzerine ölçüm koyarak 'Belki hareket eden biziz' diyebilme cesaretidir.",
            "Kozmik adresin güzel yanı, bizi evsiz bırakmamasıdır. Dünya daha küçük görünür ama daha kıymetli olur. Ulaşabildiğimiz, nefes alabildiğimiz ve bütün tarihimizin yaşandığı tek ortak evdir.",
            "Sagan'ın büyük düşünce hareketi budur: Merkezden çıkarır, fakat anlamsızlığa atmaz. Sorumluluğu büyütür.",
        ], "BİRİNCİ KISIM · KOZMİK ADRES", art="cosmic-address", caption="Kozmik adres her satırda genişler; Dünya küçülürken ortak evimizin değeri daha görünür hale gelir."),
        entry("Evreni bir yıla sıkıştırmak", [
            "On üç milyar yılı aşkın zamanı zihinde tutmak zordur. Sagan evrenin bütün tarihini tek takvim yılına sıkıştırır. Büyük Patlama 1 Ocak'tır. Galaksiler ve yıldızlar aylar boyunca oluşur. Güneş Sistemi yılın son bölümünde belirir. İnsanlık ise 31 Aralık gecesinin son dakikalarında sahneye çıkar.",
            "Bu takvimde yazılı tarih, yılın son saniyelerine sığar. Krallar, savaşlar, şehirler ve icatlar bize çok uzun görünür; kozmik ölçekte göz kırpması kadar kısadır. Takvim, insan emeğini küçültmekten çok böbürlenmenin süresini gösterir.",
            "Bir şirketin yüz yıllık binasına bakıp 'hep buradaydı' diyebiliriz. Kozmik takvim ise binanın, şehrin ve türümüzün neredeyse az önce ortaya çıktığını söyler. Kalıcılık duygumuz ölçeğe bağlıdır.",
            "Bugünkü ölçümlere göre evren yaklaşık 13,8 milyar yaşındadır. Sagan'ın kitabındaki sayılar dönemin verilerine göre farklılaşabilir; takvim yönteminin etkisi değişmez.",
            "Akılda kalan görüntü, son saniyede kalemi eline alan insanlıktır. Önünde çok eski bir defter, elinde ise henüz birkaç satırlık tecrübe vardır.",
        ], "BİRİNCİ KISIM · KOZMİK ADRES", art="cosmic-calendar", caption="Kozmik takvimde insanlık yılın son anlarında belirir; eski sandığımız tarih evren için henüz birkaç saniyedir."),
        entry("İskenderiye Kütüphanesi: Kaybolan gelecek", [
            "Sagan eski İskenderiye'yi yalnız geçmişin şehri olarak değil, bilginin başka türlü ilerleyebileceği bir kavşak olarak anlatır. Limana gelen metinlerin kopyalandığı, farklı dillerin ve fikirlerin yan yana geldiği büyük bir hafıza merkezi hayal eder.",
            "Kütüphane, insan beyninin dışarı taşınmış hali gibidir. Tek kişinin ömrü kısa olabilir; yazı sayesinde bir düşünce başka yüzyıla aktarılır. Fakat kurumlar korunmazsa birikim kendiliğinden yaşamaz. Savaş, ihmal, dogma ve ekonomik çöküş rafları sessizleştirebilir.",
            "Bir ailede büyükbabanın bildiği zanaat kimseye aktarılmazsa onunla birlikte kaybolur. Uygarlıkta da durum aynıdır. Bilgi yalnız keşfedilmez; kopyalanır, öğretilir, tartışılır ve korunur.",
            "Sagan'ın İskenderiye anlatısı tarihçiler arasında ayrıntıları bakımından tartışılabilir. Kütüphanenin tek gecede yandığı basit hikaye gerçeği tam vermez. Ancak ana ders güçlüdür: Bilimsel ilerleme kırılgandır ve kuruma ihtiyaç duyar.",
            "Bu yüzden her okul, arşiv ve özgür tartışma alanı geleceğe bırakılmış bir yangın söndürücü gibidir.",
        ], "BİRİNCİ KISIM · KOZMİK ADRES", art="alexandria-library", caption="Bilgi keşfedilmek kadar korunmak ve aktarılmak ister; kütüphane uygarlığın dışarıdaki hafızasıdır."),
        entry("Kepler'in kusurlu çemberi", [
            "Yüzyıllar boyunca gökyüzüne kusursuz çember yakıştırıldı. Çember göze ve felsefeye güzel geliyordu. Johannes Kepler ise Mars'ın hareketini hesaplarken verinin bu güzelliğe uymadığını gördü. Küçük farkları yok saymak yerine yıllarca onlarla uğraştı ve yörüngelerin elips olduğunu kabul etti.",
            "Bu, bilim tarihinin en insani sahnelerinden biridir. Elinizde sevdiğiniz bir fikir ve masada ona uymayan birkaç sayı vardır. Sayıları düzeltmek kolay, fikri düzeltmek zordur. Kepler sonunda göğün kendi estetiğini insanın estetiğinin önüne koydu.",
            "Bir terzinin müşteriyi hazır kalıba zorlamak yerine kalıbı müşteriye göre değiştirmesi gibi, iyi teori de doğaya göre biçimlenir. Ölçümün değeri, fikri doğruladığında değil, yanlışlayabildiğinde büyür.",
            "Kepler'in hayatı mistik inançlar, aile sıkıntıları ve büyük matematiksel sezgilerle doluydu. Bilim insanı kusursuz akıl makinesi değildir. Çelişkileri olan biri, yine de yönteme sadık kaldığı anda büyük bir düzeltme yapabilir.",
            "Elips yalnız bir geometrik şekil değildir; gerçeğin hoşumuza gitmeyen küçük farkta saklanabileceğini hatırlatan işarettir.",
        ], "BİRİNCİ KISIM · KOZMİK ADRES", art="kepler-ellipse", caption="Kepler güzel çemberi değil, inatçı veriyi seçti; elips gerçeğin küçük uyumsuzlukta saklanabileceğini gösterdi."),
        entry("Elinizdeki atomun uzun yolculuğu", [
            "Masadaki bardağı tutan el, çok eski malzemeden yapılmıştır. Hidrojenin büyük bölümü evrenin ilk dönemlerinden, karbon ve oksijen gibi ağır elementler ise yıldızların içindeki nükleer fırınlardan gelir. İnsan bedeni şiir olsun diye değil, fiziksel olarak yıldız maddesidir.",
            "Bir yıldız yaşamı boyunca hafif çekirdekleri birleştirir. Büyük yıldızların son aşamalarında ve patlamalarında daha ağır elementler oluşup uzaya saçılır. Sonraki yıldızlar, gezegenler ve canlılar bu zenginleşmiş buluttan doğar.",
            "Bunu mahalle fırınına benzetebiliriz. İlk hamur yalnız birkaç malzemelidir. Her kuşak fırın çevreye yeni tatlar ve kırıntılar bırakır; sonraki hamur daha zengin olur. Güneş ve Dünya da önceki yıldız kuşaklarının mirasını taşır.",
            "Bu bilgi soy ağacını genişletir. Akrabalığımız yalnız insanlar ve canlılarla değildir; bedenimiz galaksinin kimyasal tarihine bağlıdır.",
            "Sagan bilimi burada hayranlıkla birleştirir. Mucizeyi doğa yasalarının karşısına koymaz; yasaların sıradan maddeyi düşünen canlıya dönüştürmesinde bulur.",
        ], "İKİNCİ KISIM · YILDIZLAR VE GEZEGENLER", art="stardust-hand", caption="Elimizdeki karbon ve oksijen, bizden önce yaşamış yıldızların fırınlarından geçerek bugüne ulaştı."),
        entry("Yıldızların doğumu ve ölümü", [
            "Yıldızlar göğe çakılmış değişmez lambalar değildir. Gaz ve toz bulutları kendi çekimleri altında çöker, merkez ısınır ve nükleer tepkimeler başlar. Yıldız böyle doğar. Kütlesi, ne kadar hızlı yanacağını ve nasıl öleceğini büyük ölçüde belirler.",
            "Büyük bir yakıt deposu her zaman uzun yol demek değildir. Çok büyük yıldızlar yakıtı çok hızlı tüketir. Küçük yıldızlar daha sakin yanabilir. Dev yıldızın gösterişli hayatı, kısa ama parlak bir harcamaya benzer.",
            "Güneş orta yaşlı bir yıldızdır. Bir gün yakıt dengesi değişecek, şişecek ve sonunda dış katmanlarını bırakacaktır. Bu olay insan takviminde yakın değildir; yine de yıldızların da tarih içinde olduğunu gösterir.",
            "Bir yıldızın ölümü çevresi için yalnız son değildir. Uzaya saçılan malzeme yeni bulutları, gezegenleri ve belki yaşamı besler. Kozmosta mezarlık ile doğumhane aynı maddeleri paylaşır.",
            "Gece gördüğümüz ışıkların farklı renk ve parlaklıkları, yaşları ve sıcaklıkları hakkında ipucu verir. Gökyüzü sabit dekor değil, çok yavaş çekilmiş bir aile filmidir.",
        ], "İKİNCİ KISIM · YILDIZLAR VE GEZEGENLER", art="stellar-life", caption="Yıldızlar doğar, yakıt tüketir ve ölür; sonları yeni dünyaların malzemesini hazırlayabilir."),
        entry("Güneş Sistemi bir aile albümü", [
            "Gezegenleri tek tek ezberlemek yerine aynı ailede büyüyen farklı kardeşler gibi düşünün. Hepsi yaklaşık aynı gaz ve toz diskinden doğdu, fakat konumları, kütleleri ve geçirdikleri çarpışmalar onları çok farklı hale getirdi.",
            "İç tarafta kayaç gezegenler, dışta büyük gaz ve buz devleri bulunur. Uydular, asteroitler ve kuyruklu yıldızlar da aile albümünün kenarında kalmış eski fotoğraflar gibidir. Oluşum döneminin izlerini taşırlar.",
            "Uzay aracı bir gezegene yaklaştığında yalnız yeni manzara çekmez. Krater sayısı yüzeyin yaşını, atmosfer bileşimi iklim tarihini, manyetik alan ise iç yapıyı anlatır. Görüntü, ölçümle birlikte geçmişin belgesine dönüşür.",
            "Sagan'ın döneminden sonra binlerce ötegezegen keşfedildi. Artık başka yıldızların çevresinde gezegen bulunup bulunmadığını değil, ne kadar çeşitli olduklarını soruyoruz. Güneş Sistemi tek örnek olmaktan çıktı.",
            "Yine de ailemizin ayrıntılı tanıdığımız tek üyesi Dünya'dır. Uzak gezegenlerin keşfi, evimizin bakımını ertelemek için kaçış bileti değildir.",
        ], "İKİNCİ KISIM · YILDIZLAR VE GEZEGENLER", art="solar-family", caption="Gezegenler aynı başlangıç diskinden doğmuş farklı kardeşlerdir; yüzeyleri ortak geçmişin ayrı sonuçlarını taşır."),
        entry("Venüs'ün serası", [
            "Venüs büyüklük bakımından Dünya'ya benzer, fakat yüzeyi kurşunu eritecek kadar sıcaktır. Yoğun karbondioksit atmosferi ısıyı güçlü biçimde tutar. Sagan bu komşu dünyayı gezegen ikliminin nasıl başka bir yola sapabileceğini göstermek için kullanır.",
            "Sera etkisi olmasaydı Dünya yaşanamayacak kadar soğuk olurdu. Sorun sera etkisinin varlığı değil, enerji dengesinin ne kadar değiştiğidir. Battaniye kışın hayat kurtarır; üst üste çok sayıda battaniye nefes aldırmaz.",
            "Venüs, Dünya'nın geleceğinin bire bir resmi değildir. İki gezegenin suyu, atmosferi ve jeolojik tarihi farklıdır. Fakat atmosferin küçük bir dekor değil, yüzey koşullarını belirleyen etkin sistem olduğunu çarpıcı biçimde gösterir.",
            "Bugünkü iklim bilimi Sagan'ın zamanından çok daha ayrıntılıdır. İnsan kaynaklı sera gazlarının Dünya'yı ısıttığı güçlü ölçümlerle bilinir. Venüs benzetmesi bilimsel farkları silmeden uyarı resmi olarak kullanılmalıdır.",
            "Komşu gezegen bize şunu söyler: Bir dünyanın iklimi sonsuza kadar aynı kalacağına dair söz vermez.",
        ], "İKİNCİ KISIM · YILDIZLAR VE GEZEGENLER", art="venus-greenhouse", caption="Venüs, atmosferin bir gezegenin yüzeyini nasıl kökten değiştirebileceğini gösteren yakıcı bir komşudur."),
        entry("Mars'ta gördüğümüz yüzler", [
            "İnsan zihni belirsiz çizgilerden anlam üretmeyi sever. Eski teleskoplarla Mars'a bakan bazı gözlemciler yüzeyde kanallar gördüğünü düşündü. Çizgiler, gelişmiş bir uygarlığın su yolları olarak anlatıldı. Daha iyi görüntüler geldiğinde bu düzenli ağ kayboldu.",
            "Bu hikaye aptallığın değil, algının nasıl çalıştığının örneğidir. Bulutlarda hayvan, duvar lekesinde yüz görürüz. Beklenti, gözün boşluklarını tamamlar. Uzak ve bulanık bir gezegen, arzu için dev bir perdeye dönüşebilir.",
            "Uzay araçları Mars'ın gerçekten ilginç olduğunu gösterdi: Kurumuş akarsu izleri, buz, eski su geçmişi ve karmaşık jeoloji. Hayali kanallar yok oldu ama daha sağlam sorular doğdu.",
            "Bilimde yanlış bir fikrin çökmesi merakın sonu değildir. Çocukça cevap geri çekilir, daha iyi soru kalır. Mars'ta yaşam olup olmadığını hâlâ araştırıyoruz; henüz kesin kanıtımız yok.",
            "Akılda kalacak ders, teleskoptaki ince çizgidir. Görmek ile gördüğümüzü yorumlamak arasına her zaman küçük bir boşluk koymak gerekir.",
        ], "İKİNCİ KISIM · YILDIZLAR VE GEZEGENLER", art="mars-canals", caption="Mars kanalları, bulanık görüntünün beklentiyle birleşince nasıl kesin hikayeye dönüşebildiğini gösterir."),
        entry("Canlılığın ilk kıvılcımı", [
            "Dünya'nın genç döneminde okyanuslar, volkanlar, enerji kaynakları ve basit kimyasal maddeler vardı. Yaşamın tam olarak hangi yoldan başladığını bilmiyoruz. Fakat canlı maddenin doğaüstü ayrı bir malzemeden yapılmadığını, aynı kimyanın düzenlenmiş hali olduğunu biliyoruz.",
            "Sagan laboratuvarda erken Dünya koşullarını taklit eden deneylere büyük önem verir. Basit gazlar ve enerji kullanılarak aminoasit gibi organik yapı taşlarının oluşabilmesi, yaşamın bütün yolunu açıklamaz; ilk basamağın doğa yasalarıyla mümkün olabileceğini gösterir.",
            "Bir mutfakta un, su ve maya görmek ekmeğin kendiliğinden hazır olduğu anlamına gelmez. Malzeme, tarif, ortam ve zaman gerekir. Yaşamın kökeni araştırması da yapı taşından kendini kopyalayan sistemlere giden uzun köprüyü arar.",
            "Bugün hidrotermal bacalar, sığ havuzlar, RNA benzeri moleküller ve başka senaryolar inceleniyor. Tek bir kesin hikaye yoktur. Bilmediğimiz boşluğu dürüstçe açık tutmak bilimin zayıflığı değil, çalışma alanıdır.",
            "Kıvılcım görüntüsü bu nedenle tek bir şimşek değil, kimyanın çok uzun süre boyunca birçok yolu denediği büyük bir laboratuvardır.",
        ], "ÜÇÜNCÜ KISIM · YAŞAM VE ZİHİN", art="origin-lab", caption="Yaşamın başlangıcı tek bir sihirli an değil, erken Dünya kimyasının uzun süre sınadığı yolların açık sorusudur."),
        entry("DNA: Dört harfle yazılan akrabalık", [
            "Canlıların görünüşleri şaşırtıcı biçimde farklıdır; yine de kalıtım bilgisinin temel dili ortaktır. DNA'nın dört kimyasal harfi, bakteriden ağaca ve insana kadar yaşamın akrabalığını taşır. Farklı kitaplar aynı alfabe ve benzer ciltleme yöntemiyle yazılmış gibidir.",
            "Evrim önceden çizilmiş merdiven değildir. Dallanıp budaklanan ağaçtır. İnsan tepe basamağına yerleştirilmiş nihai ürün değil, yaşayan dallardan biridir. Başka canlılarla ortak atalar paylaşır.",
            "Doğal seçilim geleceği bilmez. O anda çoğalmaya katkı sağlayan özellikler yayılabilir. Çevre değişince dün yararlı olan bugün yük olabilir. Bu yüzden evrim kusursuz mühendis değil, elindeki parçaları yeniden kullanan tamircidir.",
            "Sagan, yaşamın kozmik olasılıklarını düşünürken Dünya'daki birliği temel alır. Başka dünyalarda yaşam varsa aynı DNA'yı kullanmak zorunda değildir. Fakat enerji, bilgi ve kopyalama gibi ortak sorunlarla karşılaşması beklenir.",
            "Dört harfli alfabe bizi doğadan ayırmaz. Bedenimizdeki her hücre, eski akrabalığın sessiz kaydını taşır.",
        ], "ÜÇÜNCÜ KISIM · YAŞAM VE ZİHİN", art="dna-tree", caption="DNA'nın ortak alfabesi yaşamı merdiven değil, kökleri çok eskiye uzanan dallı bir ağaç olarak gösterir."),
        entry("Beyin içindeki küçük kütüphane", [
            "İnsan beyni katman katman oluşmuş uzun evrim tarihini taşır. Sagan bu yapıyı eski bölümlerin üzerine yeni odalar eklenmiş bir kütüphaneye benzetir. Solunum ve temel dürtüler, duygular, planlama ve dil aynı binada birlikte çalışır.",
            "Bu tür katman benzetmeleri öğreticidir ama beynin üç ayrı bağımsız parça halinde çalıştığı kaba şemalara dönüştürülmemelidir. Modern sinirbilim, bölgelerin yoğun ağlar halinde işbirliği yaptığını gösterir.",
            "Beynin asıl olağanüstü yanı, evrenin kendi üzerine düşünmesini mümkün kılmasıdır. Yıldızlarda üretilmiş atomlar, bir kafatası içinde birleşip yıldızların yaşını hesaplar. Madde, kendine ayna tutar.",
            "Fakat zeka otomatik bilgelik değildir. Aynı beyin teleskop ve aşı yapabildiği gibi propaganda ve silah da yapabilir. Bilgi gücü büyütür; yönünü değerler ve kurumlar belirler.",
            "Kütüphanenin rafları dolu olabilir, ama hangi kitabı ne zaman açacağımız ayrı bir eğitim ister. Sagan'ın bilime ahlakı eklediği yer burasıdır.",
        ], "ÜÇÜNCÜ KISIM · YAŞAM VE ZİHİN", art="brain-library", caption="Beyin, evrim boyunca eklenmiş odaları olan bir kütüphane gibi çalışır; bilgi birikimi bilgelik garantisi değildir."),
        entry("Işık hızındaki tren", [
            "Gündelik hayatta zaman herkes için aynı akıyormuş gibi görünür. Einstein'ın göreliliği, çok yüksek hızlarda ve güçlü kütle çekiminde bu ortak saatin ayrıldığını gösterir. Hareketli trenin saati ile perondaki saatin ölçümü aynı kalmak zorunda değildir.",
            "Bunu gözle fark etmeyiz çünkü arabalarımız ışık hızına göre çok yavaştır. Fakat uyduların saatlerinde görelilik düzeltmeleri yapılmazsa konum sistemleri hızla hata biriktirir. En tuhaf teori cebimizdeki haritanın çalışmasına yardım eder.",
            "Görelilik 'Her şey kişiye göre değişir' demek değildir. Tam tersine, gözlemciler arasındaki farkları kesin matematik kurallarıyla bağlar. Keyfilik değil, daha geniş bir düzen sunar.",
            "Sagan zaman ve uzayı anlatırken hayal gücünü ölçümle birlikte yürütür. Düşünce deneyi, kanıtın yerine geçen hikaye değil, hangi ölçümün anlamlı olduğunu bulma aracıdır.",
            "Işık hızındaki tren, sağduyunun evrenin tamamı için hazırlanmadığını hatırlatır. Sağduyu mahallede iyidir; kozmosta ölçüm ister.",
        ], "ÜÇÜNCÜ KISIM · YAŞAM VE ZİHİN", art="relativity-train", caption="Görelilik zamanı keyfi yapmaz; farklı hareket ve kütle çekimi koşullarındaki saatleri kesin kurallarla birbirine bağlar."),
        entry("Kozmik telefonda kimse var mı?", [
            "Samanyolu'nda çok sayıda yıldız ve gezegen varsa başka zeki canlılar olabilir mi? Sagan bu soruya hevesle yaklaşır, ama cevap ile arzu arasındaki mesafeyi korur. Olasılık yüksek görünebilir; doğrulanmış sinyal olmadan 'varlar' diyemeyiz.",
            "SETI çalışmaları gökyüzünü radyo ve başka işaretler için dinler. Bu, rastgele her paraziti uzaylı saymak değildir. Sinyalin tekrarlanması, doğal ve insani kaynakların elenmesi, bağımsız gözlem gibi sıkı kontroller gerekir.",
            "Karanlık odada telefon beklemek gibi, sessizlik de yorum ister. Kimsenin olmaması, çok uzakta olmaları, kısa süre yayın yapmaları veya yanlış frekansta dinlememiz aynı sessizliği üretebilir.",
            "Drake denklemi kesin sayı makinesi değildir. Bilmediğimiz çarpanları görünür hale getiren soru listesi gibidir: Kaç yıldız, kaç gezegen, yaşam ne kadar sık, teknoloji ne kadar uzun süre iz bırakıyor?",
            "En önemli kazanç, cevap gelmeden de ortaya çıkar. Başka uygarlığı düşünmek, kendi uygarlığımızın ne kadar genç ve kırılgan olduğunu fark ettirir.",
        ], "DÖRDÜNCÜ KISIM · GELECEK VE SORUMLULUK", art="seti-radio", caption="Kozmik sessizlik tek bir cevap değildir; dikkatli dinleme, arzuyu kanıttan ayıran uzun bir bekleyiştir."),
        entry("Soluk mavi ev ve ortak kader", [
            "Uzaktan çekilmiş Dünya görüntüsünde ülkelerin sınırları görünmez. Bütün savaşlar, aşklar, pazarlar ve anılar küçük bir ışık noktasında yaşanmıştır. Sagan kozmik bakışı siyasi kaçış değil, ortak kaderi görünür kılan bir mercek olarak kullanır.",
            "Kitabın yazıldığı dönemde nükleer savaş tehdidi anlatının merkezindeydi. Teknolojik olarak güçlü, duygusal olarak kabileci bir tür kendi evini yok edebilir. Aynı çelişki iklim, biyolojik riskler ve başka büyük teknolojilerde de sürer.",
            "Kozmik ölçekte sınırlar önemsiz görünse de insanların yaşadığı adaletsizlik önemsiz değildir. 'Hepimiz aynı gezegendeyiz' cümlesi, bedeli kimin ödediğini saklamak için kullanılmamalıdır. Ortaklık eşit sorumluluk değil, ortak sonuç anlamına gelir.",
            "Başka gezegenleri araştırmak Dünya'dan vazgeçmek değildir. Denizci yeni kıtaları merak ederken gemisindeki deliği de kapatmak zorundadır. Şimdilik yaşamı bildiğimiz tek liman burasıdır.",
            "Soluk mavi nokta insanı küçültmez; kavgalarımızı küçültür ve koruma görevimizi büyütür.",
        ], "DÖRDÜNCÜ KISIM · GELECEK VE SORUMLULUK", art="pale-blue-home", caption="Uzaktan bakınca sınırlar kaybolur; küçük ortak evimizin kırılganlığı ve onu koruma sorumluluğu belirginleşir."),
        entry("Bilimin mumu ve iktidarın gölgesi", [
            "Bilim insan işi olduğu için kurumların çıkarlarından, önyargılardan ve güç ilişkilerinden tamamen bağımsız değildir. Tarih, kötüye kullanılan araştırmalar ve dışlanan insanlarla doludur. Sagan'ın bilim sevgisi bu sorunları görmezden gelmek zorunda değildir.",
            "Bilimi özel yapan, bilim insanının kusursuzluğu değil; iddianın eleştiriye, ölçüme ve düzeltmeye açık olmasıdır. Ancak bu düzeltme düzeni için özgür tartışma, şeffaf veri ve hesap verebilir kurum gerekir.",
            "Kozmik hayranlık da bazen Dünya'daki politik sorunları sisleyebilir. Büyük evren karşısında her şey küçük denirse adalet talebi de küçültülebilir. Daha dengeli okuma, iki ölçeği birlikte taşır: Kozmosta küçüğüz, birbirimizin hayatında çok etkiliyiz.",
            "Kitabın kalıcı gücü, bilginin duygudan arınmış olması değil; merak, şaşkınlık ve sorumluluğu aynı sayfada buluşturmasıdır.",
        ], "DÖRDÜNCÜ KISIM · GELECEK VE SORUMLULUK"),
        entry("1980'den sonra değişen gökyüzü", [
            "Kozmos yayımlandığından beri ötegezegenler keşfedildi, evrenin yaşına ilişkin ölçümler keskinleşti, uzay teleskopları çok erken galaksileri gözledi ve robot araçlar Güneş Sistemi'ni ayrıntılı biçimde gezdi. Bazı sayılar eskidi, merakın alanı genişledi.",
            "Bu güncellemeler Sagan'ı yanlışlamaktan çok onun yöntemini sürdürür. Bilimsel kitap kutsal metin değildir. Yeni ölçüm geldiğinde kenarına not düşülür, bazı cümleler değiştirilir ve yeni sorular eklenir.",
            "Okur için en iyi tutum, eski baskıdaki her ayrıntıyı savunmak veya kitabı bütünüyle çöpe atmak değildir. Ana fikri, tarihsel bağlamı ve güncel kanıtı ayrı raflarda tutmaktır.",
        ], "SONUÇ"),
        entry("Bir dakikalık kozmik harita", [
            "Evren yaklaşık 13,8 milyar yıllık büyük bir tarihtir. Dünya, sıradan bir yıldızın çevresindeki küçük ama yaşam taşıdığı bilinen tek gezegendir. Bedenimiz yıldızlarda üretilmiş elementlerden, zihnimiz çok uzun bir evrimden gelir.",
            "Bilgi; gözlem, ölçüm, hata ve düzeltme yoluyla büyür. Kepler'in elipsi, Mars kanalları ve İskenderiye'nin kırılgan rafları aynı dersi verir: Gerçek merak ister, ama merak kurum ve kuşku olmadan kolayca hikayeye dönüşür.",
            "Kozmik bakışın son cümlesi kaçış değil sorumluluktur. Evren çok büyük olduğu için Dünya önemsiz değil; bildiğimiz bütün yaşam burada olduğu için eşsiz derecede korunmaya değerdir.",
        ], "SONUÇ"),
        entry("Akılda kalacak beş görüntü", [
            "Kozmik kıyı: Bildiklerimiz büyük okyanusun kenarıdır. Uzun adres: Dünya merkez değil, evdir. Yılın son saniyesi: İnsanlık çok yenidir. Kepler'in elipsi: Veri güzel fikri düzeltebilir. Soluk mavi nokta: Ortak ev küçük ve kırılgandır.",
            "Bu beş görüntü yüzlerce yıldız adından daha kullanışlıdır. Gökyüzüne baktığınızda yalnız uzak cisimleri değil, merakın tarihini ve kendi bedeninizin eski malzemesini hatırlarsınız.",
            "Sagan'ın bıraktığı duygu yalnız hayranlık değildir. Evreni anlayabilen bir türün, kendi evini koruyabilecek kadar olgunlaşıp olgunlaşamayacağı sorusudur.",
        ], "SONUÇ"),
    ],
})


BOOKS.append({
    "bookNo": 60,
    "title": "Sevme Sanatı",
    "author": "Erich Fromm",
    "subtitle": "Sevilmeyi beklemekten sevebilme yeteneğine geçişi; bakım, saygı, emek ve cesaret üzerinden anlatan sade ve eleştirel rehber.",
    "coverImage": "/images/optimized/summary-art-60-sevme-sanati-v2-960.webp",
    "coverStyle": "artwork",
    "pdfUrl": "/data/pdfs/60-sevme-sanati-ozeti.pdf",
    "pdfLabel": "25-50 sayfalık PDF'yi indir",
    "longForm": True,
    "chapterArtStyle": "monochrome-engraving",
    "chapterArtColor": "#8A4F58",
    "meta": {
        "originalTitle": "The Art of Loving",
        "compiler": "Zihin Gezgini · Yapay zeka destekli çalışma",
        "date": "Temmuz 2026",
        "language": "Türkçe",
    },
    "intro": "Erich Fromm aşkı, doğru kişiye rastlandığında kendiliğinden çalışan bir duygu olarak değil, öğrenilen ve bütün kişiliği isteyen bir yaşam sanatı olarak ele alır. Bu yüzden kitap sevgili bulma kılavuzu değildir. Anne sevgisinden kardeşçe sevgiye, kendini sevmekten modern toplumun ilişki pazarına kadar uzanan daha geniş bir soruya bakar: İnsan sevilme arzusunu aşarak gerçekten sevebilir mi? Bu rehber kitabın canlı omurgasını korurken 1950'lerin cinsiyet, aile ve cinsellik anlayışındaki eskimiş hükümleri açıkça ayırır. Amaç fedakarlık yarışına girmek değil; bakım, sorumluluk, saygı ve bilgiyi sınırlarla birlikte düşünmektir.",
    "sources": [
        {"id": 1, "title": "The Art of Loving - resmi yayınevi tanıtımı", "url": "https://www.bloomsbury.com/us/art-of-loving-9780826412607/"},
        {"id": 2, "title": "Google Books - içerik yapısı ve bibliyografik bilgi", "url": "https://books.google.com/books/about/The_Art_of_Loving.html?id=pM8MzzntBRcC"},
        {"id": 3, "title": "Erich Fromm'un sevgi kavramına psikobiyografik bakış", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC13059089/"},
        {"id": 4, "title": "The Art of Loving üzerine varoluşçu, psikodinamik ve teolojik eleştiri", "url": "https://theses.gla.ac.uk/80302/"},
    ],
    "entries": [
        entry("Bu kitap nasıl okunmalı?", [
            "Fromm'un temel hamlesi basittir: Çoğu insan sevme yeteneğini değil, nasıl sevileceğini düşünür. Daha çekici, başarılı veya ilginç olursa sevginin geleceğine inanır. Kitap soruyu ters çevirir: Benim sevme kapasitem ne durumda?",
            "Bu ters çevirme güçlüdür, fakat yanlış kullanılırsa insanı her ilişki sorunu için kendini suçlamaya götürebilir. Sevgi tek kişinin ustalığıyla kurulmaz; karşılıklılık, güvenlik ve sınır gerekir. Şiddet veya sömürü karşısında daha çok sevmek çözüm değildir.",
            "Özeti bir ilişki testi gibi değil, davranış aynası gibi okuyun. Her bölümde 'Bunu kimden bekliyorum?' kadar 'Bunu nasıl veriyorum ve nerede sınır koyuyorum?' sorusunu da tutun.",
        ], "BAŞLANGIÇ"),
        entry("Sevilmek mi, sevmek mi?", [
            "Bir mağaza vitrininin önünde duran insan, ürünün beğenilmesi için nasıl sunulduğunu düşünür. Fromm modern insanın kendine de böyle baktığını söyler: Daha iyi görünürsem, daha çok kazanırsam, doğru şeyleri söylersem sevilirim. Sevgi sorunu pazarlanabilir olma sorununa dönüşür.",
            "Bu bakışta bütün dikkat dışarıdadır. Karşı taraf beni seçti mi, mesajıma ne kadar hızlı döndü, başkaları beni çekici buluyor mu? İnsan sevgi almaya odaklandıkça sevginin etkin tarafını kaçırır: dinlemek, emek vermek, tanımak ve ötekinin büyümesini istemek.",
            "Sevilme ihtiyacı yanlış değildir. Bebekten yetişkine herkes görülmek ve kabul edilmek ister. Fromm'un itirazı, bütün ilişkiyi bu ihtiyacın etrafında kurmaktır. Sürekli alkış bekleyen kişi, karşısındakini insan değil ayna gibi kullanabilir.",
            "Bir akşam eve gelen eşinizi düşünün. İlk soru 'Beni özledin mi?' olabilir. Sevme yönündeki soru ise 'Günün nasıl geçti, gerçekten nasılsın?'dır. İki soru da insanidir; denge, yalnız aynaya bakıp bakmadığımızı gösterir.",
            "Kitabın kapısı burada açılır: Sevgi başımıza gelen güzel olay kadar, bizim dünyaya yönelttiğimiz bir yetenektir.",
        ], "BİRİNCİ KISIM · SEVGİNİN TEORİSİ", art="loving-vs-liked", caption="Sevilmeyi bekleyen kişi aynaya, sevmeyi öğrenen kişi karşısındaki insanın gerçekliğine bakar."),
        entry("Sanat denince neden çalışma akla gelir?", [
            "Kimse piyano çalmayı yalnız doğru piyanoyu bulma meselesi saymaz. Nota, tekrar, sabır ve dikkat gerektiğini kabul ederiz. Fromm'a göre sevgi de sanattır; fakat insanlar ilişkiyi doğru kişiyi bulunca otomatik çalışan bir cihaz gibi görür.",
            "Sanat benzetmesi romantizmi öldürmez. Güzel bir müzik ilk heyecanı taşıyabilir, ama konseri sürdüren şey çalışılmış ustalıktır. İlişkide de ilk çekim ile yıllar sonra ötekini görebilme yeteneği aynı şey değildir.",
            "Pratik demek yapay teknikler uygulamak değildir. Dikkatini dağıtmadan dinlemek, verdiği sözü tutmak, incittiğinde özür dilemek ve ötekinin değişmesine alan açmak tekrar edilen davranışlardır. Karakter bu tekrarların içinde şekillenir.",
            "Bir marangoz tahtayı zorla kendi hayaline uydurursa kırar. Malzemenin damarını tanır. Sevgi de öteki insanı hazır kalıba sokmak yerine onun mizacını, geçmişini ve sınırlarını öğrenmeyi ister.",
            "Sanatın güzel tarafı, yeteneğin sabit olmamasıdır. İnsan hatasını fark edip daha iyi sevmeyi öğrenebilir. Zor tarafı ise bunun yalnız niyetle gerçekleşmemesidir.",
        ], "BİRİNCİ KISIM · SEVGİNİN TEORİSİ", art="love-workshop", caption="Sevgi hazır bir duygu değil; müzik ve zanaat gibi dikkat, tekrar ve karakter isteyen canlı bir pratiktir."),
        entry("Ayrılık duygusu: Kalabalıkta bile yalnız olmak", [
            "Fromm insanın temel sıkıntısını ayrılık bilinciyle açıklar. Kendimizin başkasından ayrı olduğunu, tek başımıza karar verdiğimizi ve bir gün öleceğimizi biliriz. Bu farkındalık hem özgürlük hem ürperti getirir.",
            "Kalabalık bir toplantıda herkesle konuşup yine de görülmediğinizi hissetmiş olabilirsiniz. Fiziksel yakınlık ayrılığı tek başına çözmez. İnsan anlaşılmak, bir bütüne katılmak ve kendini aşmak ister.",
            "Bu ihtiyacı bastırmanın birçok yolu vardır. Kalabalığa körü körüne uymak, sürekli eğlenceye kaçmak, işe gömülmek veya bir ilişkiye yapışmak geçici birlik duygusu verebilir. Fakat benliği eriterek kurulan birlik, gerçek yakınlık değildir.",
            "Olgun sevgi ilginç bir denge kurar: İki kişi bağlanır ama iki ayrı insan olarak kalır. Köprü iki kıyıyı birleştirir; kıyıları yok etmez. Sınır ortadan kalkarsa köprü değil bataklık oluşur.",
            "Fromm'un sevgi teorisi bu nedenle yalnız romantik değildir. İnsan olmanın yalnızlık sorununa, özgürlüğü kaybetmeden bağ kurma cevabıdır.",
        ], "BİRİNCİ KISIM · SEVGİNİN TEORİSİ", art="bridge-separation", caption="Olgun sevgi iki ayrı kıyı arasında köprü kurar; yakınlık için benliklerin yok olması gerekmez."),
        entry("Olgun sevgi etkin bir güçtür", [
            "Fromm sevgiyi edilgin biçimde 'düşmek' yerine etkin biçimde 'vermek' üzerinden anlatır. Buradaki vermek kendini tüketmek veya sürekli taviz vermek değildir. Canlılığını, ilgisini, bilgisini ve sevincini ilişkiye katmaktır.",
            "Bir öğretmen öğrencinin cevabını onun yerine yazarsa yardım etmiş görünür ama gelişimini engeller. Gerçek verme, ötekinin kendi gücünü kullanmasına yardım eder. Sevgide de amaç bağımlı bir hayran üretmek değil, canlı bir insanın büyümesine eşlik etmektir.",
            "Vermek, zenginliğin işaretidir derken Fromm paradan söz etmez. İçinde ilgi ve üretkenlik bulunan kişi, paylaşınca boşalmaz. Fakat bu fikir bakım emeğinin tek tarafa yüklendiği ilişkileri romantikleştirmemelidir.",
            "Karşılıklılık her gün eşit dakika hesabı değildir. Hastalıkta biri daha çok taşır, başka zamanda roller değişir. Uzun vadede tek kişinin sürekli kaynak, diğerinin sürekli tüketici olduğu düzen sevgi değil sömürü olabilir.",
            "Etkin sevginin ölçüsü yalnız sıcak duygu değil, ilişkinin iki tarafında daha fazla canlılık ve gerçeklik üretip üretmediğidir.",
        ], "BİRİNCİ KISIM · SEVGİNİN TEORİSİ", art="active-giving", caption="Olgun verme kendini silmek değil; ötekinin kendi gücüyle büyümesine canlılık ve emek katmaktır."),
        entry("Dört ayak: Bakım, sorumluluk, saygı, bilgi", [
            "Fromm sevgiyi dört ayaklı bir masa gibi kurar. Bakım yoksa sevgi sözde kalır. Bir bitkiyi sevdiğini söyleyen ama sulamayan kişi duygusunu davranışa çevirmemiştir. Bakım, ötekinin yaşamına somut ilgi göstermektir.",
            "Sorumluluk, başkasının bütün yükünü almak değildir. İhtiyacına cevap verebilecek kadar uyanık olmaktır. Yetişkin ilişkisinde sorumluluk gönüllü ve karşılıklı olmalıdır; kontrol bahanesine dönüşmemelidir.",
            "Saygı, ötekini benim istediğim kişiye çevirmemektir. Onu kendi yönü, seçimi ve sınırları olan ayrı bir insan olarak görmek demektir. 'Senin iyiliğin için' cümlesi saygı yoksa kolayca baskıya dönüşür.",
            "Bilgi ise yüzeydeki rolü aşar. Eşinizin kahveyi nasıl içtiğini bilmek hoş ayrıntıdır; korktuğunda neden sustuğunu, hangi geçmişin onu etkilediğini anlamaya çalışmak daha derin bilgidir. Bu bilgi merakla gelir, sorgu memurluğuyla değil.",
            "Masa ancak dört ayak birlikte durduğunda sağlamdır. Bakım saygısızsa boğar, sorumluluk bilgisizse yanlış yere koşar, bilgi bakımsızsa soğuk gözleme dönüşür.",
        ], "BİRİNCİ KISIM · SEVGİNİN TEORİSİ", art="four-legged-love", caption="Bakım, sorumluluk, saygı ve bilgi birlikte olduğunda sevgi dengeli ve taşıyıcı bir yapıya dönüşür."),
        entry("Anne ve baba sevgisi benzetmesinin sınırı", [
            "Fromm anne sevgisini koşulsuz kabul, baba sevgisini ise kural ve başarıyla ilişkilendirir. Bu şema kitabın en tanınan ama bugün en dikkatli okunması gereken bölümlerindendir. Döneminin cinsiyet rolleri aileyi iki sabit kutba ayırır.",
            "Gerçek hayatta şefkat ve sınır herhangi bir ebeveynden gelebilir. Tek ebeveynli, geniş aileli, evlat edinilmiş veya eşcinsel ebeveynli aileler bu iki özelliği farklı biçimlerde taşır. Çocuğun ihtiyacı kadın ve erkek rolünün ezberi değil, güvenli kabul ile gelişmeyi destekleyen sınırın birleşimidir.",
            "Benzetmenin işe yarayan çekirdeği şudur: İnsan yalnız var olduğu için değerli olduğunu hissetmek ister; aynı zamanda dünyada sorumluluk almayı ve sınırla yaşamayı öğrenir. Bu iki deneyim dengelenmediğinde ya koşullu değere ya da sınır tanımazlığa kayabilir.",
            "Yetişkin ilişkilerinde eşten anne veya baba beklemek yük yaratır. Partner, çocuklukta eksik kalan her şeyi sınırsızca tamir etmekle görevli değildir. Yakınlık destek sunar, terapi ve ebeveynliğin bütün işlevlerini üstlenmez.",
            "Fromm'un şemasını rol dağılımı değil, iki insani ihtiyaç olarak yeniden okumak daha adildir: Olduğun halinle kabul ve büyümeni isteyen dürüst sınır.",
        ], "İKİNCİ KISIM · SEVGİNİN BİÇİMLERİ", art="care-and-boundary", caption="Çocuğun ve yetişkinin ihtiyacı sabit cinsiyet rolleri değil; kabul ile geliştirici sınırın güvenli birleşimidir."),
        entry("Kardeşçe sevgi: Yakın çevrenin dışına taşmak", [
            "Fromm için kardeşçe sevgi bütün sevgi biçimlerinin tabanıdır. Buradaki kardeşlik biyolojik akrabalık değil, başka insanda ortak insanlığı görebilmektir. Yalnız bana benzeyeni değil, ihtiyacı olan yabancıyı da özne saymaktır.",
            "Apartmanda asansörde karşılaştığınız temizlik görevlisini görünmez saymak kolaydır. Adını sormak tek başına büyük sevgi değildir; onu hizmet işlevinden ibaret görmeyen bakışın başlangıcıdır. Saygı günlük karşılaşmalarda belli olur.",
            "Kardeşçe sevgi acımadan farklıdır. Acıma yukarıdan aşağı bakabilir; dayanışma eşit değeri kabul eder. Yardım edilen kişi bizim iyilik hikayemizin dekoru değildir.",
            "Bu sevgi soyut insanlık söylemine de dönüşebilir. Uzak kıtalardaki herkesi sevdiğini söyleyip evdeki yükü paylaşmamak kolaydır. Evrensel ilke, yakındaki somut davranışta sınanır.",
            "Fromm sevgiyi özel çiftin duvarından çıkarır. İyi ilişki, iki kişinin dünyadan kaçtığı ada değil, dünyayla daha insani bağ kurduğu liman olmalıdır.",
        ], "İKİNCİ KISIM · SEVGİNİN BİÇİMLERİ", art="human-circle", caption="Kardeşçe sevgi benzerlik aramaz; başka insanda işlevin, sınıfın ve yabancılığın ötesinde ortak değeri görür."),
        entry("Anaç sevgi: Büyütmek ve bırakabilmek", [
            "Fromm anaç sevgiyi yaşamı koruma ve çocuğa yaşam sevincini aktarma gücü olarak anlatır. Yalnız süt vermek değil, dünyanın yaşanmaya değer olduğu duygusunu da vermektir. Bu nitelik biyolojik anneliğe veya tek bir cinsiyete ait değildir.",
            "Bakımın büyük sınavı çocuğun ayrılmasına izin vermektir. Küçükken elinden tutulan kişi büyüdükçe kendi yolunu seçer. Ebeveyn çocuğu kendi başarısının uzantısı sayarsa sevgi bağa dönüşür.",
            "Bahçıvan fidanı çekerek uzatamaz. Toprağı, suyu ve ışığı sağlar; büyümenin kendi ritmine saygı duyar. Çocuk yetiştirmede de koruma ile kontrol arasındaki çizgi buradadır.",
            "Yetişkin ilişkilerinde sürekli kurtarıcı rolüne girmek anaç sevginin gölgesidir. Karşı tarafın sorumluluğunu alıp onu güçsüz bırakmak, bakım gibi görünse de bağımlılığı sürdürebilir.",
            "Büyüten sevginin başarısı kendine bağlamak değil, bağ kopmadan ayrılığa dayanabilmektir.",
        ], "İKİNCİ KISIM · SEVGİNİN BİÇİMLERİ", art="growing-and-letting-go", caption="Büyüten sevgi korur ama sahiplenmez; fidanın kendi yönünde uzamasına ve bir gün ayrılmasına izin verir."),
        entry("Erotik sevgi: Birlik, seçim ve emek", [
            "Erotik sevgi bir kişiyle özel yakınlık kurma arzusudur. Başlangıçtaki yoğun çekim, iki yabancı arasındaki duvarların bir anda yıkıldığı hissini verir. Fromm bu ani birleşmenin kalıcı sevgi sanılmasına karşı uyarır.",
            "İlk günlerde anlatılacak çok şey vardır. Geçmiş, alışkanlıklar ve hayaller paylaşılır. Zamanla yenilik azalınca bazı çiftler yakınlığın bittiğini düşünür. Oysa yüzeydeki bilgi tükendiğinde gerçek tanıma yeni başlayabilir.",
            "Özel seçim, dünyadaki herkese aynı biçimde davranmamak demektir. Fakat partneri sahip olunan tek nesneye çevirmek değildir. Sadakat, denetim ve kıskançlıkla aynı şey değildir; ortak karar ve güven içerir.",
            "Fromm erotik sevgiyi irade ve sözle de ilişkilendirir. Bu, duygusuz görev evliliği savunmak değildir. Duygunun dalgalandığı günlerde bile ilişkinin bakımını sürdürecek kararın önemini gösterir.",
            "Birlik, iki kişinin bütün farklarını eritmesi değil, farkların içinde yeniden birbirini seçebilmesidir.",
        ], "İKİNCİ KISIM · SEVGİNİN BİÇİMLERİ", art="chosen-partnership", caption="Erotik sevgi ilk heyecanın ötesinde, iki ayrı insanın güven ve emekle birbirini yeniden seçmesidir."),
        entry("Kendini sevmek bencillik midir?", [
            "Bir uçakta oksijen maskesini önce kendinize takmanız istenir. Bu öğüt başkasını önemsememek değildir; nefessiz kişinin yardım edemeyeceğini kabul eder. Fromm da kendini sevme ile bencilliği ayırır.",
            "Kendini sevmek, kendi ihtiyaç ve sınırlarını başkasınınki kadar gerçek saymaktır. Sürekli yorgun olduğu halde herkese evet diyen kişi fedakar görünebilir; zamanla öfke ve kırgınlık biriktirebilir.",
            "Bencillik ise yalnız kendi çıkarını görür. Fromm'a göre aşırı bencil kişi aslında kendisiyle de verimli bir ilişki kuramamış olabilir; iç boşluğu dışarıdan sürekli alma isteğiyle doldurur.",
            "Kendine bakım da performans projesine dönüşebilir. Kusursuz beden, kusursuz ev ve kusursuz sakinlik peşinde koşmak özsaygıyı yeniden pazara bağlar. Kendini sevmek, eksik ve değişen halini de insan sayabilmektir.",
            "Sağlıklı ölçü basittir: Kendinize gösterdiğiniz anlayış başkasının varlığını silmiyor, başkasına verdiğiniz bakım da sizi yok etmiyorsa iki yön birlikte çalışıyordur.",
        ], "İKİNCİ KISIM · SEVGİNİN BİÇİMLERİ", art="oxygen-mask", caption="Kendini sevmek başkasını unutmak değil; kendi ihtiyaç ve sınırlarını da aynı insanlık ölçüsünde gerçek saymaktır."),
        entry("Tanrı sevgisi ve en yüksek değer", [
            "Fromm farklı dinlerde Tanrı sevgisinin insanın olgunlaşma biçimleriyle birlikte değiştiğini tartışır. Korkulan otorite, koruyucu ebeveyn veya insanın içinde taşıdığı birlik ilkesi gibi farklı imgeler görür.",
            "Bu bölüm inanan ve inanmayan okur için ortak bir soruya çevrilebilir: Hayatınızda en yüksek değeri neye veriyorsunuz? Para, başarı, ulus, aile, hakikat veya merhamet davranışlarınızı nasıl yönlendiriyor?",
            "İnsan 'Ben hiçbir şeye tapmam' diyebilir ama takvimine bakıldığında bütün vaktini başarıya sunduğu görülebilir. Resmi inanç ile fiili bağlılık aynı olmayabilir.",
            "Fromm otoriter din ile mistik birlik arayışını ayırır. Yine de geniş din tarihi birkaç gelişim basamağına indirgenemez. İnanç gelenekleri içlerinde hem baskı hem özgürleşme biçimleri taşır.",
            "Bölümün kalıcı sorusu, sevginin yalnız kişisel duygu mu yoksa insanın bütün dünyaya yönelişi mi olduğudur.",
        ], "İKİNCİ KISIM · SEVGİNİN BİÇİMLERİ", art="highest-value", caption="Tanrı sevgisi tartışması, insanın hayatında neyi en yüksek değer yaptığı ve vaktini neye sunduğu sorusuna açılır."),
        entry("İlişki pazarı: İyi bir takas aramak", [
            "Fromm modern ilişkileri pazar mantığıyla karşılaştırır. İnsanlar kendi değer paketlerini sunar, alabilecekleri en iyi eşleşmeyi arar. Eğitim, görünüş, gelir ve toplumsal itibar görünmez fiyat etiketlerine dönüşebilir.",
            "Bugün uygulamalar bu benzetmeyi daha görünür kılıyor. Parmağın bir hareketiyle yeni profil gelir. Seçenek bolluğu insanı özgürleştirebilir; aynı zamanda karşısındakini her an değiştirilebilir ürün gibi görmeye teşvik edebilir.",
            "Pazar benzetmesi bütün ilişkileri açıklamaz. İnsanlar ekonomik koşullardan etkilenirken yine de şefkat, dayanışma ve beklenmedik bağlılık kurabilir. Toplum karakteri güçlüdür, kader değildir.",
            "Sorun tercih yapmak değil, insanın değerini tercih edilirlikle eşitlemektir. Reddedilmek acıtır; fakat birinin seçmemesi bütün kişiliğin fiyatını belirlemez.",
            "Fromm'un eleştirisi bugün şu soruyla canlı kalır: Karşımızdakini gerçekten tanıyor muyuz, yoksa özellik listesini mi karşılaştırıyoruz?",
        ], "ÜÇÜNCÜ KISIM · TOPLUM VE SEVGİ", art="relationship-market", caption="Pazar mantığı ilişkide insanı özellik paketine çevirebilir; seçim çoğalırken gerçek tanıma yüzeyselleşebilir."),
        entry("Aşkın dağılması neden yalnız çiftin suçu değil?", [
            "İki kişi akşam eve yorgun, borç kaygılı ve sürekli ulaşılabilir halde geliyorsa yakınlık için yalnız iyi niyet yetmeyebilir. Fromm sevgi güçlüğünü bireysel karakterin yanında toplumun çalışma ve tüketim düzeniyle bağlar.",
            "Reklam sürekli yeni heyecan satar. İlişki sıradanlaştığında arıza varmış gibi hissedilir. Oysa gündelik sevgi çoğu zaman gösterişli değildir: ilaç almak, yük paylaşmak, aynı hikayeyi yeniden dinlemek gibi küçük işlerde yaşar.",
            "Çalışma hayatı zamanı böler. Bakım emeği görünmez ve eşitsiz dağıldığında bir taraf romantizm eksikliğinden önce dinlenme eksikliği yaşar. Sevgi konuşması maddi koşulları görmelidir.",
            "Bunun tersi de doğrudur: Toplumu suçlamak kişisel sorumluluğu yok etmez. Kırıcı dil, kaçınma ve denetim ekonomik sistemin arkasına saklanamaz. Yapı davranışı etkiler; davranış yine bizim alanımızdır.",
            "İlişkinin sorunu bazen iki kişilik odada, bazen odanın kirasında ve çalışma saatinde bulunur. İyi okuma iki ölçeği birlikte tutar.",
        ], "ÜÇÜNCÜ KISIM · TOPLUM VE SEVGİ", art="tired-couple", caption="Yakınlık yalnız duygudan değil, zaman, bakım emeği, ekonomik baskı ve gündelik davranışların ortak düzeninden etkilenir."),
        entry("Sahte birlik biçimleri", [
            "İki kişi hiç tartışmıyorsa çok uyumlu olabilir; biri sürekli susuyor da olabilir. Fromm, çatışmasız görünüm ile gerçek yakınlığı ayırır. Olgun çatışma yüzeyde gürültü çıkarabilir ama iki kişiyi daha görünür kılar.",
            "Bir başka sahte birlik, ortak düşman üzerinden kurulur. Çift herkesi küçümser, yalnız birbirini doğru sayar. Bu yakınlık ilk başta güçlü görünür; dünyayla bağ kesildikçe kapalı devreye dönüşür.",
            "Cinsel yakınlık da tek başına duygusal birliği garanti etmez. Bedensel yakınlık değerli olabilir, fakat korku, saygısızlık ve yalnızlığı otomatik çözmez. Aynı yatakta iki yabancı kalmak mümkündür.",
            "Sosyal medyada kusursuz çift görüntüsü üretmek de ilişkinin kendisinden ayrı bir işe dönüşebilir. Fotoğrafın uyumu, evdeki emeğin adil dağıldığını söylemez.",
            "Gerçek birlik, dışarıya nasıl göründüğünden çok iki insanın korkmadan gerçek olabilmesi ve birbirinin özgürlüğüne dayanabilmesiyle anlaşılır.",
        ], "ÜÇÜNCÜ KISIM · TOPLUM VE SEVGİ"),
        entry("Disiplin, sabır ve düzen", [
            "Fromm sevme sanatının disiplin istediğini söyler. Bu, ilişkiyi askeri programa çevirmek değil; yalnız canımız istediğinde değil, düzenli biçimde dikkat gösterebilmektir. Bitki ayda bir kova suyla değil, ihtiyacına uygun süreklilikle yaşar.",
            "Sabır, değişimin hemen sonuç vermemesine dayanır. Bir konuşmada yılların alışkanlığı çözülmez. Özürden sonra güvenin dönmesi, yeni davranışın tekrar tekrar görülmesini isteyebilir.",
            "Modern hayat hız ister. Mesaja hemen yanıt, soruna hemen çözüm, duyguda hemen rahatlama bekleriz. Sevgi bazen sonucu zorlamadan yanında kalabilme becerisidir.",
            "Düzenin tehlikesi mekanikleşmedir. Her cuma çiçek almak güzel olabilir; yalnızca görevi tamamlamak için yapılınca karşı tarafın o gün neye ihtiyacı olduğunu kaçırabilir. Disiplin canlı dikkati desteklemeli, onun yerine geçmemelidir.",
            "Ustalık büyük jestlerden önce küçük güvenilir tekrarlarla oluşur. Sevgi karakteri takvimde görünmeyen bu tekrarlar kurar.",
        ], "DÖRDÜNCÜ KISIM · SEVGİNİN PRATİĞİ", art="patient-practice", caption="Sevgi ustalığı büyük jestten önce, dikkat ve güveni küçük ama düzenli davranışlarla yeniden kurar."),
        entry("Yoğunlaşmak ve gerçekten dinlemek", [
            "Birini dinlerken cevabınızı hazırlıyor, telefona bakıyor veya eski tartışmayı düşünüyorsanız bedeniniz odada olsa da dikkatiniz dağınıktır. Fromm yoğunlaşmayı sevme sanatının merkezine koyar.",
            "Yoğunlaşmak karşı tarafı sessizce onaylamak değildir. Söylediğini anlamaya çalışırken kendi görüşünüzü koruyabilirsiniz. Dinleme, teslimiyet değil temas kurma biçimidir.",
            "Kısa bir deney yapılabilir: Beş dakika boyunca çözüm önermeden yalnız soru sorun. 'Bunu duyunca ne hissettin?' deyin. Birçok insanın tavsiye değil, önce anlaşılma istediği ortaya çıkar.",
            "Kendini dinlemek de önemlidir. Bedendeki gerginlik, yükselen öfke veya evet derken gelen isteksizlik sınır hakkında bilgi verir. İç sesi bastıran kişi dışarıda dürüst olamaz.",
            "Dikkat bugünün kıt kaynaklarından biridir. Birine bölünmemiş birkaç dakika vermek, pahalı hediyeden daha derin bir 'Buradasın ve seni görüyorum' mesajı taşıyabilir.",
        ], "DÖRDÜNCÜ KISIM · SEVGİNİN PRATİĞİ", art="deep-listening", caption="Gerçek dinleme cevap hazırlamayı kısa süreliğine bırakıp ötekinin deneyimine bölünmemiş dikkat vermektir."),
        entry("Akılcı inanç ve cesaret", [
            "Sevgi garantisizdir. Karşı taraf değişebilir, ilişki bitebilir veya verdiğimiz emek istediğimiz sonucu üretmeyebilir. Fromm bu belirsizliğe rağmen bağ kurmayı cesaret olarak görür.",
            "Akılcı inanç, kanıtsız iyimserlik değildir. Kendimizin ve ötekinin gelişme kapasitesine, geçmiş davranışlarla desteklenen güven duymaktır. Kör inanç işaretleri yok sayar; akılcı inanç onları görerek risk alır.",
            "Bir arkadaşınıza kırıldığınızı söylemek küçük ama gerçek risktir. Susarsanız reddedilmezsiniz, fakat tanınma ihtimalini de kapatırsınız. Yakınlık savunmasızlık olmadan kurulmaz.",
            "Cesaret sınır koymayı da içerir. 'Seni seviyorum, fakat bana böyle davranmana izin vermiyorum' cümlesi sevginin karşıtı değildir. Korkudan her şeye katlanmak, ilişkiyi dürüstlükten uzaklaştırır.",
            "Sevgi sanatı başarısız olmayacağımıza inanmak değil; sonuç garanti değilken bile daha canlı, saygılı ve gerçek davranışı seçebilmektir.",
        ], "DÖRDÜNCÜ KISIM · SEVGİNİN PRATİĞİ", art="courageous-heart", caption="Sevginin cesareti kör güven değil; belirsizliği görerek dürüst konuşmak, bağ kurmak ve gerektiğinde sınır koymaktır."),
        entry("Kitabın eskimiş ve tartışmalı tarafları", [
            "Fromm'un erkek ve kadın kutupları, annelik ve babalık rolleri, eşcinselliğe ilişkin ifadeleri bugünün bilgisi ve eşitlik anlayışıyla sorunludur. Bunlar zamansız hakikat gibi değil, 1950'lerin sınırlı çerçevesi olarak görülmelidir.",
            "Kitap bazen çok geniş insanlık hükümleri verir. Kültür, sınıf, travma, nöroçeşitlilik ve farklı ilişki biçimleri sevme deneyimini değiştirir. Tek bir olgunluk çizgisi herkesi aynı cetvelle ölçemez.",
            "Yine de sevginin beceri, karakter ve toplumsal koşullarla ilişkili olduğu fikri canlıdır. En verimli okuma, eski kabuğu savunmak değil; bakım, saygı, bilgi ve özgürlük çekirdeğini daha kapsayıcı hale getirmektir.",
        ], "SONUÇ"),
        entry("Sevgi kendini silmek değildir", [
            "Bu kitap kolayca 'Daha çok emek ver, her şeyi anlayışla karşıla' diye yanlış okunabilir. Oysa şiddet, aşağılama, sürekli manipülasyon veya korku varsa temel sorun sevgi tekniği değildir. Güvenlik ve destek önce gelir.",
            "Sağlıklı sevgi iki insanın gerçekliğini taşır. Birinin ihtiyaçları sürekli yasa, diğerininki sürekli istisna olamaz. Sınır ilişkiyi cezalandırmak değil, hangi koşulda kalabileceğimizi açık etmektir.",
            "Profesyonel destek gereken durumlarda kitap önerisi tedavi yerine geçmez. Sevme kapasitesi önemlidir, fakat herkesin yükünü tek başımıza iyileştirmek görevimiz değildir.",
        ], "SONUÇ"),
        entry("Bir dakikalık harita", [
            "Fromm'a göre sevgi yalnız duygu değil, öğrenilen etkin bir güçtür. Bakım, sorumluluk, saygı ve bilgi birlikte çalışır. Kardeşçe sevgi insanlığı, anaç sevgi büyütüp bırakmayı, erotik sevgi özel seçimi, kendini sevme ise kendi değerini de korumayı anlatır.",
            "Modern pazar insanı tercih edilen pakete çevirebilir. Çalışma baskısı ve tüketim kültürü yakınlığı zorlaştırır. Yine de kişisel davranış alanı kalır: dikkat, disiplin, sabır, dinleme, dürüstlük ve cesaret.",
            "En dengeli cümle şudur: Sevmek kendini feda etmek değil, iki ayrı insanın canlılığını ve özgürlüğünü birlikte büyütme sanatıdır.",
        ], "SONUÇ"),
        entry("Akılda kalacak beş görüntü", [
            "Ayna ve pencere: Sevilmek aynaya, sevmek ötekine bakar. Köprü: Yakınlık iki kıyıyı yok etmez. Dört ayaklı masa: Bakım, sorumluluk, saygı, bilgi. Bahçıvan: Büyütür ama çekerek uzatmaz. Oksijen maskesi: Kendine bakım bencillik değildir.",
            "Bu görüntüler ilişkinin zor anında hızlı bir kontrol listesi olur. Şu anda ötekini gerçekten görüyor muyum? Onu değiştirmeye mi çalışıyorum? Kendi sınırımı saklıyor muyum? Davranışım iki tarafta canlılık mı, korku mu üretiyor?",
            "Fromm'un kitabı doğru kişiyi vaat etmez. Daha zor ve daha değerli bir soru bırakır: Ben, sevginin gerektirdiği dikkat ve özgürlüğe ne kadar hazırım?",
        ], "SONUÇ"),
    ],
})


BOOKS.append({
    "bookNo": 81,
    "title": "Kahramanın Bin Yüzü",
    "author": "Joseph Campbell",
    "subtitle": "Mitlerdeki ayrılma, sınanma ve dönüş ritmini; katı senaryo kalıbına çevirmeden, modern örnekler ve eleştirilerle anlatan görsel rehber.",
    "coverImage": "/images/optimized/summary-art-81-kahramanin-bin-yuzu-v2-960.webp",
    "coverStyle": "artwork",
    "pdfUrl": "/data/pdfs/81-kahramanin-bin-yuzu-ozeti.pdf",
    "pdfLabel": "25-50 sayfalık PDF'yi indir",
    "longForm": True,
    "chapterArtStyle": "monochrome-engraving",
    "chapterArtColor": "#6C5536",
    "meta": {
        "originalTitle": "The Hero with a Thousand Faces",
        "compiler": "Zihin Gezgini · Yapay zeka destekli çalışma",
        "date": "Temmuz 2026",
        "language": "Türkçe",
    },
    "intro": "Joseph Campbell dünyanın farklı mitlerinde tekrar eden bir hareket görür: Kahraman alışılmış dünyadan ayrılır, bilinmeyenin içinde sınanıp değişir ve kazandığı şeyi topluma geri getirir. İnternette dolaşan on iki maddelik senaryo şablonlarından daha geniş ve daha karmaşık olan kitap, psikoloji, din, ritüel ve yüzlerce hikayeyi yan yana getirir. Bu rehber Campbell'ın üç ana hareketini koruyor: ayrılma, erginlenme ve dönüş. Ancak modeli bütün kültürlerin değişmez yasası saymıyor; erkek merkezli dili, seçilen örnekleri ve farklı anlatıları görünmez kılma riskini açıkça tartışıyor. Amaç her hikayeyi aynı kalıba sıkıştırmak değil, dönüşümün güçlü bir haritasını dikkatle kullanmaktır.",
    "sources": [
        {"id": 1, "title": "Joseph Campbell Foundation - Hero with a Thousand Faces", "url": "https://www.jcf.org/learn/joseph-campbell-collected-works"},
        {"id": 2, "title": "Joseph Campbell Foundation - Kahramanın yolculuğu ve üç ana aşama", "url": "https://www.jcf.org/learn/joseph-campbell-heros-journey"},
        {"id": 3, "title": "Separation, Initiation, and Return - modelin üçlü çekirdeği", "url": "https://www.jcf.org/post/separation-initiation-and-return"},
        {"id": 4, "title": "JCF - Kahraman yolculuğunun erkek merkezli yapısına eleştiri", "url": "https://www.jcf.org/post/at-one-ment-with-the-demon"},
        {"id": 5, "title": "JCF - Campbell ve sinema etkisi", "url": "https://www.jcf.org/post/myth-campbell-film"},
    ],
    "entries": [
        entry("Bu kitap nasıl okunmalı?", [
            "Campbell'ın kitabı basit bir masal listesi değildir. Aynı sayfada Buda, Odysseus, yerli halk anlatıları, rüyalar ve dinsel semboller buluşabilir. Okur sürekli kültür ve çağ değiştirir.",
            "En güvenli pusula üç kelimedir: Ayrılma, erginlenme, dönüş. Diğer aşamalar zorunlu kontrol noktaları değil, bazı hikayelerde görülen değişken motiflerdir. Bir anlatıda mentor bulunmayabilir, başka birinde dönüş reddedilebilir.",
            "Bu özet modeli önce canlı biçimde anlatacak, sonra sınırlarını gösterecek. Haritayı arazinin kendisi sanmadan, hikayelerin ve hayat geçişlerinin neden bizi etkilediğini araştıracağız.",
        ], "BAŞLANGIÇ"),
        entry("Harita, reçete değil", [
            "Bir dağ haritasında dere, patika ve zirve işaretlenir. Fakat yürüyüşçü her taşı aynı sırayla görmez. Campbell'ın kahraman yolculuğu da böyle okunmalıdır. Hikayelerde tekrar eden yönleri gösterir; bütün anlatıların uyması gereken trafik yasası değildir.",
            "Yolculuğun çekirdeği üç harekettir. Kahraman bildiği dünyadan ayrılır. Yabancı alanda sınanır ve değişir. Sonra bir kazanımla geri döner. Bu kazanım eşya, bilgi, şifa, yeni bakış veya toplumu kurtaran bir çözüm olabilir.",
            "İnternette model çoğu kez on iki ya da on yedi kutulu senaryo formülüne çevrilir. Campbell'ın kendisi ise motifleri farklı mitlerdeki olası görünümler olarak inceler. Kutuların hepsi bulunmak zorunda değildir.",
            "Bir emeklilik hikayesi düşünün. Kişi iş kimliğinden ayrılır, boşluk ve yeni denemeler yaşar, sonra topluma başka biçimde katılır. Ejderha yoktur ama dönüşüm ritmi vardır.",
            "Haritanın yararı, karmaşık değişimi isimlendirmesidir. Zararı ise her hayatı tek kahraman ve tek zafer çizgisine zorlamasıdır. Bu iki ihtimali birlikte tutacağız.",
        ], "BİRİNCİ KISIM · AYRILMA", art="map-not-recipe", caption="Kahraman yolculuğu arazinin kendisi değil; bazı dönüşüm yollarını görünür kılan, eksik ve kullanışlı bir haritadır."),
        entry("Maceraya çağrı", [
            "Hikaye alışılmış düzenin bozulmasıyla başlar. Bir mektup gelir, yabancı kapıyı çalar, hastalık belirir, kayıp yaşanır veya kahraman içindeki huzursuzluğu artık susturamaz. Campbell buna maceraya çağrı der.",
            "Çağrı her zaman davul ve boruyla gelmez. Kırk beş yaşında işine karşı duyduğu boşluk, çocuğun evden ayrılması veya yıllardır ertelenen sağlık kontrolü de insanı eski düzenin dışına çağırabilir.",
            "Kurbağa Prens masalındaki beklenmedik karşılaşma, Musa'nın yanan çalısı veya telefonla gelen iş haberi aynı değildir. Fakat hepsinde bilinen dünyanın sınırı çatlar ve yeni görev görünür.",
            "Çağrının önemli yanı olaydan çok merkez değişimidir. Dün önemsiz görünen şey bugün bütün dikkati çeker. Eski hedefler küçülür, bilinmeyen büyür.",
            "Campbell için bu an kaderin kapıyı açmasıdır. Modern dilde ise insanın koşullar, arzu ve zorunluluk tarafından yeni bir eşiğe getirilmesi diyebiliriz.",
        ], "BİRİNCİ KISIM · AYRILMA", art="call-at-door", caption="Maceraya çağrı, alışılmış hayatın duvarında açılan ve insanın dikkat merkezini değiştiren ilk çatlağıdır."),
        entry("Çağrıyı reddetmek", [
            "Kapı açıldığında ilk tepki çoğu zaman ilerlemek değil geri çekilmektir. Kahraman görevi tehlikeli, saçma veya kendine fazla büyük bulur. Reddediş korkaklık karikatürü değildir; bilinen kimliği koruma çabasıdır.",
            "Yeni iş teklifini isteyen biri, başvuru formunu haftalarca açmayabilir. Boşanması gerektiğini bilen kişi yıllarca 'Şimdi zamanı değil' diyebilir. Çağrı, yalnız fırsat değil kayıp da içerir. Yeniye giderken eski rol bırakılır.",
            "Mitlerde reddediş bazen dünyayı daraltır. Kahraman güvenli yerde kalmak isterken sorun büyür. Hayatta ise her çağrıyı kabul etmek zorunda değiliz. Tehlikeli veya başkasının dayattığı çağrıya hayır demek bilgelik olabilir.",
            "Bu nedenle model karar makinesi değildir. Asıl soru şudur: Hayır dememin nedeni değerlerim mi, yoksa değişim korkusunu gerekçelendiren alışkanlık mı?",
            "Reddediş bölümü, kahramanlığın korkusuzluk olmadığını gösterir. Cesaret çoğu kez korkuyu ortadan kaldırmadan bir sonraki adımı atmaktır.",
        ], "BİRİNCİ KISIM · AYRILMA", art="refused-letter", caption="Çağrıyı reddetmek değişimin taşıdığı kaybı ve korkuyu görünür kılar; cesaret korkunun yokluğu değildir."),
        entry("Beklenmedik yardımcı", [
            "Kahraman yola çıkmaya yaklaştığında yaşlı bilge, hayvan, peri, öğretmen veya sıradan bir yabancı yardım sunabilir. Campbell buna doğaüstü yardım der. Yardımcı bütün sorunu çözmez; eşiği geçmeye yetecek araç verir.",
            "Masalda sihirli kılıç olabilir. Günlük hayatta iyi bir doktorun açıklaması, arkadaşın telefon numarası, bir ustanın ilk dersi veya yıllar önce okunmuş cümle aynı işlevi görebilir.",
            "Yardımın gelmesi kahramanın tek başına olmadığını gösterir. Modern başarı hikayeleri kişiyi kendi kendini yaratmış gibi sunar; mitler çoğu zaman görünür ve görünmez destek ağlarını kabul eder.",
            "Fakat mentor da kusursuz değildir. Öğretmen kendi korkusunu aktarabilir, yardım karşılığında itaat isteyebilir. Gerçek yardım bağımlılık üretmek yerine yolcunun kendi karar gücünü artırır.",
            "Akılda kalan görüntü, karanlık yola küçük bir fener uzatan eldir. Fener yolu yürümez; yalnız ilk birkaç adımı görünür yapar.",
        ], "BİRİNCİ KISIM · AYRILMA", art="helper-lantern", caption="Yardımcı kahramanın yerine yürümez; karanlıkta ilk adımları gösterecek araç, bilgi veya güven sunar."),
        entry("İlk eşik ve kapıdaki bekçi", [
            "Bilinen dünya ile yabancı alan arasında bir eşik vardır. Kapıda canavar, nöbetçi, fırtına veya iç korku bekler. Eşik bekçisi yalnız düşman değildir; yolcunun eski araçlarla ilerleyemeyeceğini gösteren sınavdır.",
            "İlk terapi randevusunun kapısında durmak, yabancı ülkede pasaport kontrolünden geçmek veya ilk kez kalabalık önünde konuşmak eşik duygusu yaratabilir. Geri dönmek hâlâ mümkündür, fakat geçince eski rahatlık bozulur.",
            "Bekçi bazen dış kurumdur: para, diploma, ayrımcılık veya aile baskısı. Her engeli yalnız iç korkuya indirgemek adaletsizdir. Bazı kapılar gerçekten eşitsiz biçimde korunur.",
            "Kahraman bekçiyi öldürmek zorunda değildir. Onunla anlaşabilir, bilmeceyi çözebilir veya kendisi hakkındaki yanılgıyı bırakarak geçebilir. Güç tek çözüm değildir.",
            "Eşik, niyetin davranışa dönüştüğü çizgidir. 'Bir gün yapacağım' cümlesi burada biter; ayak gerçekten öte tarafa basar.",
        ], "BİRİNCİ KISIM · AYRILMA", art="threshold-guardian", caption="Eşik bekçisi bilinmeyene geçişin bedelini gösterir; bazı engeller içsel, bazıları ise gerçek toplumsal kapılardır."),
        entry("Balinanın karnı: Eski benliğin kaybolması", [
            "Eşiği geçen kahraman bazen yutulur, mağaraya iner veya karanlıkta kaybolur. Campbell balinanın karnı motifini eski kimliğin geçici ölümü olarak yorumlar. Dışarıdaki unvanlar burada işe yaramaz.",
            "İşten çıkarılan biri ilk günlerde yalnız maaşını değil, 'Ben kimim?' cevabını da kaybedebilir. Hastalık, göç veya yas, insanı eski aynaların çalışmadığı karanlık odaya sokabilir.",
            "Bu dönemi hemen olumlu dönüşüm diye süslemek tehlikelidir. Karanlık gerçek acı, belirsizlik ve destek ihtiyacı taşır. Her kayıp otomatik bilgelik üretmez.",
            "Ritüeller bu geçişe zaman ve anlam verebilir. Cenaze, mezuniyet veya emeklilik töreni bir kimliğin bittiğini ve yenisinin henüz tamamlanmadığını topluca kabul eder.",
            "Balinanın karnı, başarısızlığın değil ara bölgenin görüntüsüdür. Eski oda kapanmış, yeni kapı henüz açılmamıştır.",
        ], "BİRİNCİ KISIM · AYRILMA", art="belly-of-whale", caption="Balinanın karnı eski kimliğin çözülüp yenisinin henüz kurulmadığı karanlık ve belirsiz ara bölgeyi simgeler."),
        entry("Sınavlar yolu", [
            "Erginlenme tek büyük dövüşten çok bir dizi küçük sınavla ilerler. Kahraman dost ve düşmanları tanır, beceri kazanır, yanılır ve tekrar dener. Campbell buna sınavlar yolu der.",
            "Yeni bir dili öğrenen yetişkin ilk gün kahramanca konuşma yapmaz. Markette kelimeyi karıştırır, yanlış otobüse biner, utançla güler ve ertesi gün yeniden dener. Dönüşüm tekrarın içinde oluşur.",
            "Masallardaki üç görev, psikolojik olarak alışkanlığın farklı yüzlerini gösterebilir. İlkinde fiziksel korku, ikincisinde sabırsızlık, üçüncüsünde kibir sınanır. Aynı sorun yeni kostümle geri gelir.",
            "Yardımcılar bu bölümde önemlidir. Yolculuk bireysel görünse de ekip, dostluk ve tesadüf olmadan birçok sınav geçilemez. Kahramanlık yalnızlık kültü değildir.",
            "Sınavların amacı acı çekme puanı toplamak değil, eski benliğin yetmediği yerde yeni ilişki ve yetenek geliştirmektir.",
        ], "İKİNCİ KISIM · ERGİNLENME", art="road-of-trials", caption="Dönüşüm tek zaferden değil; yanılma, yardım alma ve yeniden denemenin oluşturduğu sınavlar yolundan geçer."),
        entry("Tanrıçayla karşılaşma: Ödül değil bütünlük", [
            "Campbell bazı mitlerde kahramanın tanrıçayla karşılaşmasını yaşamın bütünlüğüyle temas olarak okur. Fakat kullandığı dil kadını kahramanın ödülü veya ruhsal gelişimin aracı gibi gösterebilir. Bu nedenle motif bugünün gözüyle yeniden düşünülmelidir.",
            "Karşılaşmayı cinsiyetli bir ödül yerine, kahramanın dışladığı yaşam yönüyle buluşması olarak okuyabiliriz: şefkat, beden, yaratıcılık, ilişki veya doğa. Bu nitelikler herhangi bir cinsiyete ait değildir.",
            "Yıllarca yalnız verimle yaşayan bir yöneticinin hasta yakınına bakım verirken kırılganlığı öğrenmesi böyle bir bütünleşme olabilir. Kazandığı şey başka bir insanı sahiplenmek değil, kendi dar kimliğinin genişlemesidir.",
            "Mit sembolü gerçek kadınların yerine konduğunda sorun çıkar. Kadınlar fikir, eşik veya ödül değil, kendi yolculuklarının öznesidir. Model bunu açıkça tanımadığında eleştiri gerekir.",
            "Motifin işe yarayan çekirdeği, olgunlaşmanın fetih kadar kabul ve ilişki de istediğidir.",
        ], "İKİNCİ KISIM · ERGİNLENME", art="meeting-wholeness", caption="Tanrıçayla karşılaşma, bir kişiyi ödüle çevirmeden kahramanın dışladığı yaşam yönüyle bütünleşmesi olarak okunabilir."),
        entry("Baştan çıkarıcı gölge", [
            "Campbell'ın 'baştan çıkarıcı kadın' dili kitabın en eskimiş noktalarındandır. Sorunu kadına yükleyen bu motif, daha adil biçimde kahramanı yolundan saptıran gölge olarak yeniden okunabilir: güç hırsı, kolay zafer, kibir veya bağımlılık.",
            "Bir toplumsal hareketin lideri başlangıçta adalet için yola çıkıp zamanla alkış ve denetim tutkusuna kapılabilir. Düşman dışarıda yenilmiş, içeride yeni biçim almıştır.",
            "Gölge yalnız kötü arzu değildir. Bastırılan korku, yas veya utanç da kararları gizlice yönetebilir. Kahraman onu yok etmek yerine tanımadığında aynı hata tekrar eder.",
            "Bu aşama başarı anında özellikle önemlidir. İnsan zayıfken değil güç kazandığında değerlerinden uzaklaşabilir. Sınav kılıcı almak değil, kılıcı ne için kullanacağını bilmektir.",
            "Baştan çıkarılma görüntüsü, suçu dışarıdaki figüre atmak yerine kendi kör noktamıza bakınca değer kazanır.",
        ], "İKİNCİ KISIM · ERGİNLENME", art="inner-shadow", caption="Yoldan çıkaran güç dışarıdaki bir kadın değil; kahramanın tanımadığı hırs, korku ve kolay zafer arzusunun gölgesi olabilir."),
        entry("Babayla hesaplaşma: Otoritenin aynası", [
            "Campbell birçok mitte kahramanın baba veya büyük otorite figürüyle karşılaşmasını anlatır. Bu figür gerçek ebeveyn, kral, tanrı, kurum veya insanın içindeki sert yargıç olabilir.",
            "Genç doktor yıllarca hocasının onayını arayabilir. Bir gün kendi hastası için farklı karar vermesi gerektiğinde yalnız tıbbi değil, psikolojik bir eşik geçer. Otoriteyi yok etmez; onunla eşit sorumluluk düzeyinde ilişki kurar.",
            "Hesaplaşma intikam olmak zorunda değildir. Bazen ebeveynin sınırlı bir insan olduğunu kabul etmek, ondan alınamayan şeyi yas tutmak ve içindeki sesini yeniden değerlendirmek gerekir.",
            "Modelin baba dili yine dar olabilir. Otorite deneyimi anne, aile, devlet, gelenek veya piyasa üzerinden gelebilir. Esas hareket, dış buyruğun kör egemenliğinden iç sorumluluğa geçiştir.",
            "Kahraman burada 'Artık kimseye ihtiyacım yok' demez. Kendi kararının sonucunu taşıyabilecek yetişkin konumuna yaklaşır.",
        ], "İKİNCİ KISIM · ERGİNLENME", art="authority-mirror", caption="Otoriteyle hesaplaşma onu körce yıkmak değil; dış onaydan iç sorumluluğa geçip sonucu taşıyabilmektir."),
        entry("Apotheosis: Daha geniş bir benlik", [
            "Bazı mitlerde kahraman büyük sınavdan sonra tanrısal bir görüşe, dinginliğe veya genişlemiş bilince ulaşır. Campbell buna apotheosis der. Günlük dilde bunu her şeyi çözen aydınlanma anı değil, eski bakışın sınırını aşmak olarak düşünebiliriz.",
            "Uzun aile kavgasında yalnız kimin haklı olduğunu soran biri, bir gün kuşaklar boyunca aktarılan korkuyu görür. Sorun bitmeyebilir; fakat kendini hikayenin tek merkezi saymayan daha geniş bakış doğar.",
            "Bu tür anlar kalıcı sarhoşluk değildir. İçgörü gündelik hayata çevrilmezse güzel hatıra olarak kalır. Aydınlandığını ilan eden kişi çöpü hâlâ başkasına toplatıyorsa dönüşüm eksiktir.",
            "Ruhsal deneyimler bazı insanlar için derin olabilir, fakat psikolojik krizle karıştırılmamalıdır. Yoğun deneyimin sağlık ve güvenlik boyutu varsa profesyonel değerlendirme gerekir.",
            "Apotheosis'in sade resmi yüksek dağdan bakmaktır. Yollar küçülür, bağlantılar görünür; yine de aşağı inip yürümek gerekir.",
        ], "İKİNCİ KISIM · ERGİNLENME", art="mountain-view", caption="Daha geniş bakış sorunu sihirli biçimde bitirmez; insanı hikayenin tek merkezi olmaktan çıkarıp bağlantıları gösterir."),
        entry("Nihai armağan", [
            "Yolculuğun derin noktasında kahraman bir armağan elde eder. Bu ateş, kutsal su, şifa, bilgi veya yeni yaşam gücü olabilir. Campbell buna nihai armağan der.",
            "Prometheus'un ateşi teknoloji ve bilgiyi, masaldaki şifalı su yaşamı onarmayı simgeleyebilir. Modern hikayede araştırmacının bulduğu tedavi veya ailede yıllardır konuşulmayan gerçeği söyleme cesareti armağan olabilir.",
            "Armağan her zaman kahramanın hakkıyla kazandığı ödül değildir. Bazen bağışlanır, çalınır veya büyük bedelle alınır. Bu çeşitlilik başarı kültürünün 'Çalışan herkes kazanır' basitliğini bozar.",
            "Asıl soru armağanın kimin için olduğudur. Yalnız kahramanın gücünü artırıyorsa yolculuk yarım kalabilir. Mit, kazanımın toplumun yarasına dönmesini bekler.",
            "Bir doktorun bilgisi hastaya, bir sanatçının görüşü seyirciye, iyileşen kişinin deneyimi başka acı çekenlere ulaşınca armağan dolaşıma girer.",
        ], "İKİNCİ KISIM · ERGİNLENME", art="ultimate-boon", caption="Nihai armağan eşya, bilgi veya şifa olabilir; değeri kahramanın elinde kalmayıp yaşama geri döndüğünde büyür."),
        entry("Dönüşü reddetmek", [
            "Kahraman armağanı bulduğunda neden geri dönmek istemesin? Çünkü yeni dünya daha anlamlı, eski çevre ise dar ve anlaşılmaz görünebilir. Campbell dönüşün de çağrı kadar zor olduğunu söyler.",
            "Uzun eğitimden sonra memleketine dönen kişi eski arkadaşların onu hâlâ önceki haliyle gördüğünü fark edebilir. Terapiyle değişen biri, ailedeki eski rolüne yeniden çağrılır. İç dönüşüm dış ilişkilerde hemen tanınmaz.",
            "Bazen özel deneyimi anlatmak da zordur. Dağdaki manzarayı hiç çıkmamış birine kelimelerle taşımaya benzer. Kahraman anlaşılmama korkusuyla armağanı saklayabilir.",
            "Dönüşü reddetmek dinlenme ihtiyacı da olabilir. Her acıdan çıkan kişi hemen başkalarına ders vermek zorunda değildir. Paylaşımın zamanı ve sınırı kişiye aittir.",
            "Mitin ısrarı şudur: Dönüşüm yalnız özel kaçışa dönüşürse ortak dünya değişmez. Bir noktada köprü yeniden kurulmalıdır.",
        ], "ÜÇÜNCÜ KISIM · DÖNÜŞ", art="refusal-to-return", caption="Yeni görüşü kazanan kişi eski dünyaya dönmekte zorlanabilir; değişimin paylaşılması ikinci bir cesaret ister."),
        entry("Sihirli kaçış ve dışarıdan kurtarılmak", [
            "Bazı kahramanlar armağanı izinle almaz; peşlerine güçler düşer. Sihirli kaçışta şekil değiştiren engeller, kovalamaca ve son anda yardım görülür. Başka anlatılarda kahraman dönüş için dışarıdan kurtarılmak zorundadır.",
            "Bu motif, dönüşümün son aşamasında bile kişinin kendi kendine yetmediğini kabul eder. Bağımlılıktan çıkan biri tedavi ekibine, ailesine ve güvenli çevreye ihtiyaç duyabilir. İç karar önemlidir, sistem desteği de önemlidir.",
            "Modern kahraman anlatıları bazen yardımı zayıflık sayar. Campbell'ın birçok miti tam tersini gösterir: Yardımcılar başlangıçta olduğu gibi dönüşte de belirir.",
            "Sihirli kaçış, elde edilen gücün eski düzen tarafından kolay bırakılmadığını da anlatabilir. Baskıcı kurumdan ayrılan kişinin yasal, ekonomik veya fiziksel engellerle karşılaşması gerçektir.",
            "Kurtarılmak kahramanlığı bozmaz. İnsanın dönüş yolunda başkasının elini tutabilmesi, yeni olgunluğun parçası olabilir.",
        ], "ÜÇÜNCÜ KISIM · DÖNÜŞ", art="magic-flight-rescue", caption="Dönüşte yardım almak zayıflık değil; değişimin kişisel cesaret kadar güvenli ilişki ve kurum istediğini kabul etmektir."),
        entry("Dönüş eşiğini geçmek", [
            "Yabancı dünyada öğrenilen şey günlük hayata nasıl çevrilir? Dönüş eşiğinin sorusu budur. Kahraman olağanüstü deneyimi market, iş, aile ve sıradan pazartesi içinde yaşatmak zorundadır.",
            "Meditasyon kampında sakin olmak ile trafikte korna çalındığında sakin kalmak farklıdır. Eğitimin sertifikası, işyerindeki davranışa dönüşmedikçe armağan kapıda kalır.",
            "Eski çevre de değişen kişiye direnebilir. Aile, barış sağlayan çocuğun artık arabulucu olmamasını bencillik sayabilir. Yeni sınırın kalıcı olması tekrar ve destek ister.",
            "Dönüş aynı zamanda çeviri işidir. Kahraman gördüğünü ötekilerin anlayacağı dile indirir. Fazla büyük sözler yerine küçük kullanılabilir davranışlar sunar.",
            "Eşik geçildiğinde iki dünya birbirine dokunur. Olağanüstü deneyim gündeliği küçümsemez; gündelik hayatın şeklini değiştirir.",
        ], "ÜÇÜNCÜ KISIM · DÖNÜŞ", art="return-threshold", caption="Dönüş eşiği, büyük içgörünün sıradan pazartesiye, ilişkilere ve küçük davranışlara çevrildiği yerdir."),
        entry("İki dünyanın ustası", [
            "Yolculuğun sonunda kahraman bilinen ve bilinmeyen dünya arasında daha özgür hareket edebilir. Campbell buna iki dünyanın ustası der. Eski kimliğini tamamen reddetmez, yeni görüşü de gizlemez.",
            "Göçmen iki dili ve iki kültürü taşıyabilir. İlk başta hiçbir yere ait değilmiş gibi hissederken zamanla iki dünyayı bağlayan kişi olabilir. Ustalık tek tarafa kesin dönüş değil, gerilimi taşıma becerisidir.",
            "İç dünya ile dış görev de iki dünya sayılabilir. İnsan duygusunu dinler ama her duygunun emrine girmez; sorumluluk alır ama yalnız görev makinesine dönüşmez.",
            "Bu aşama kusursuz son değildir. Yeni çağrılar gelir, eski korkular geri döner. Campbell iyi hayatı bir kez tamamlanan değil, defalarca yinelenen yolculuklar olarak düşünür.",
            "Ustalığın sade ölçüsü, insanın kazandığı özgürlüğü başkasının hayatına baskı değil armağan olarak taşıyabilmesidir.",
        ], "ÜÇÜNCÜ KISIM · DÖNÜŞ", art="two-worlds", caption="İki dünyanın ustası tek bir kimliğe kapanmaz; içgörü ile gündeliği, aidiyet ile özgürlüğü birlikte taşıyabilir."),
        entry("Kozmogonik çevrim: Dünyalar da doğar ve çözülür", [
            "Kitabın ikinci büyük parçası yalnız bireysel kahramanı değil, evrenlerin ve tanrıların doğuşunu anlatan kozmogonik çevrimi inceler. Biçimsiz kaynaktan dünya çıkar, düzen kurulur, yaşam çoğalır ve sonunda biçimler yeniden çözülür.",
            "Bu bölüm Campbell'ın ilgisinin senaryo yazarlığından çok daha geniş olduğunu gösterir. Mitler yalnız 'Bir kişi nasıl başarır?' demez; zaman, ölüm, toplum ve varlığın neden var olduğu hakkında sembolik evrenler kurar.",
            "Bilimsel kozmoloji ile mitolojik yaratılış aynı tür açıklama değildir. Biri gözlem ve matematikle fiziksel süreçleri araştırır, diğeri kültürel anlam ve değer dünyası kurar. Birini diğerinin kanıtı yapmak iki alanı da karıştırır.",
        ], "DÖRDÜNCÜ KISIM · HARİTAYI ELEŞTİRMEK"),
        entry("Bin yüz gerçekten tek yüz mü?", [
            "Campbell'ın karşılaştırmaları çarpıcı benzerlikler bulur, fakat benzerliği seçme biçimi önemlidir. Çok farklı bağlamlardan motifleri yan yana koyduğumuzda aralarındaki tarih, güç ve yerel anlam kaybolabilir.",
            "Her hikaye tek kahramanın ayrılıp zaferle dönmesini anlatmaz. Topluluk merkezli, döngüsel, trajik, gündelik veya kahramanlığı reddeden anlatılar vardır. Bazı hikayelerde değişen kişi değil ilişkiler ağıdır.",
            "Model özellikle erkek kahramanı ve kadını ödül, anne veya ayartıcı olarak konumlandırdığı için eleştirilmiştir. Bugün kahraman, kadın, erkek veya cinsiyet dışı herhangi biri olabilir; hatta tek özne bir topluluk olabilir.",
            "Bu eleştiriler haritayı yakmayı gerektirmez. Üzerine 'Burada başka yollar var' notu düşer. Campbell'ın modeli güçlü bir yorum aracı olarak kalır, evrensel yasa olarak değil.",
        ], "DÖRDÜNCÜ KISIM · HARİTAYI ELEŞTİRMEK"),
        entry("Hayata uygularken dikkat", [
            "Her acıyı kahramanlık sınavı saymak mağduru romantikleştirebilir. Hastalık, savaş veya şiddet insanı otomatik olgunlaştırmaz. Güvenlik, yas ve destek önce gelir; anlam daha sonra ve kişinin kendi hakkıdır.",
            "Kendimizi hikayenin kahramanı görmek başkalarını yardımcı veya engel rolüne indirebilir. Oysa onların da merkezde olduğu ayrı hayatlar vardır. İyi kullanım, benlik şişirmek yerine sorumluluğu büyütür.",
            "Model bir değişimde bulunduğunuz yeri adlandırmak için yararlıdır: çağrı mı, eşik mi, sınav mı, dönüş mü? Fakat bir sonraki adımı gerçek koşullar, ilişkiler ve uzmanlık belirlemelidir.",
        ], "DÖRDÜNCÜ KISIM · HARİTAYI ELEŞTİRMEK"),
        entry("Bir dakikalık harita", [
            "Kahraman yolculuğunun çekirdeği ayrılma, erginlenme ve dönüştür. Çağrı, reddediş, yardımcı, eşik, karanlık ara bölge, sınavlar, içgörü, armağan ve dönüş bu büyük hareketlerin olası yüzleridir.",
            "Armağanın değeri yalnız kahramanı büyütmesinde değil, topluma geri taşınmasındadır. Dönüş bu yüzden maceranın eki değil, tamamlayıcı yarısıdır.",
            "Modeli reçete değil harita olarak kullanın. Her kültürü aynı kalıba sokmayın, kadınları ve başka insanları kahramanın dekoru yapmayın, gerçek acıyı dönüşüm masalıyla örtmeyin.",
        ], "SONUÇ"),
        entry("Akılda kalacak beş görüntü", [
            "Çalan kapı: Çağrı alışılmış düzeni bozar. Eşik bekçisi: Niyet davranışa dönüşür. Balinanın karnı: Eski kimlik çözülür. Armağan: Kazanım paylaşılınca anlam kazanır. İki kıyılı köprü: Dönüş, öğrendiğini gündeliğe taşır.",
            "Bu görüntüler bir film izlerken, masal okurken veya kendi hayatınızda geçiş yaşarken sorular üretir. Kim ayrılıyor? Ne kaybediyor? Kim yardım ediyor? Hangi güç onu değiştiriyor? Ne ile geri dönüyor?",
            "Campbell'ın en verimli mirası bütün hikayelerin aynı olduğunu söylemek değil, değişimin neden hikaye olarak anlatıldığında dayanılır ve paylaşılır hale geldiğini göstermektir.",
        ], "SONUÇ"),
    ],
})


BOOKS.append({
    "bookNo": 143,
    "title": "Siyah Kuğu",
    "author": "Nassim Nicholas Taleb",
    "subtitle": "Dünyayı değiştiren beklenmedik olayları, tahmin yanılgılarını ve belirsizlik içinde daha dayanıklı yaşama fikrini gündelik sahnelerle anlatan rehber.",
    "coverImage": "/images/optimized/summary-art-143-siyah-kugu-v2-960.webp",
    "coverStyle": "artwork",
    "pdfUrl": "/data/pdfs/143-siyah-kugu-ozeti.pdf",
    "pdfLabel": "25-50 sayfalık PDF'yi indir",
    "longForm": True,
    "chapterArtStyle": "monochrome-engraving",
    "chapterArtColor": "#3F4A54",
    "meta": {
        "originalTitle": "The Black Swan: The Impact of the Highly Improbable",
        "compiler": "Zihin Gezgini · Yapay zeka destekli çalışma",
        "date": "Temmuz 2026",
        "language": "Türkçe",
    },
    "intro": "Taleb dünyayı düzenli bir saat gibi değil, uzun sakin dönemlerin arasına dev sıçramalar yerleştiren belirsiz bir sistem olarak görür. Siyah Kuğu dediği olay, gerçekleşmeden önce olasılık dışı sayılır, büyük etki yaratır ve olduktan sonra herkes onu açıklayan düzgün bir hikaye kurar. Kitap finans, tarih, bilim, başarı ve gündelik kararlar arasında dolaşır. Bu rehber Taleb'in keskin benzetmelerini koruyor; fakat her sürprizi Siyah Kuğu saymıyor, kavramın sonradan gevşek kullanılmasını ve yazarın polemikçi üslubunu ayrıca tartışıyor. Amaç geleceği bildiğini iddia etmek değil, bilmediğimiz şeylerin zararını azaltıp iyi sürprizlere açık alan kurmaktır.",
    "sources": [
        {"id": 1, "title": "The Black Swan - resmi yayınevi tanıtımı", "url": "https://www.penguinrandomhouse.com/books/176226/the-black-swan-second-edition-by-nassim-nicholas-taleb/"},
        {"id": 2, "title": "Nassim Nicholas Taleb - resmi araştırma biyografisi ve Incerto çerçevesi", "url": "https://www.fooledbyrandomness.com/CV.htm"},
        {"id": 3, "title": "Cambridge - belirsizlik ve Siyah Kuğu kavramının girişimcilik bağlamı", "url": "https://www.cambridge.org/core/journals/journal-of-management-and-organization/article/facing-uncertainty-an-entrepreneurial-view-of-the-future/C42E7F6333EC1B2F680AF36EE946DAA9"},
        {"id": 4, "title": "Cambridge - bilinmeyen olasılıkları düşünmeye ilişkin istatistik örneği", "url": "https://assets.cambridge.org/97805217/32499/excerpt/9780521732499_excerpt.pdf"},
    ],
    "entries": [
        entry("Bu kitap nasıl okunmalı?", [
            "Taleb sakin öğretmen gibi yazmaz. Alay eder, öfkelenir, isim takar, otobiyografik hikayeler anlatır ve aynı fikre farklı kapılardan geri döner. Bu üslup kitabı canlı, bazen de yorucu yapar.",
            "Özetin pusulası üç sorudur: Hangi olaylar dünyayı orantısız biçimde değiştiriyor? Zihin ve modeller bu olayları neden kaçırıyor? Tahmin edemiyorsak nasıl daha az kırılgan yaşayabiliriz?",
            "Bu kitap yatırım tavsiyesi değildir. Belirsizlik düşüncesi kişisel para kararlarına uygulanacaksa gelir, borç, zaman ufku ve profesyonel destek gibi gerçek koşullar ayrıca değerlendirilmelidir.",
        ], "BAŞLANGIÇ"),
        entry("Bin gün beslenen hindi", [
            "Bir hindi her sabah çiftçinin elinden yem alır. Birinci gün temkinlidir. Yüzüncü gün insanın dost olduğuna daha çok inanır. Her yeni beslenme günü inancını güçlendirir. Tam güven en yüksek noktaya çıktığında bayram öncesi bıçak gelir.",
            "Taleb'in hindi hikayesi geçmiş verinin geleceği garanti etmediğini anlatır. Hindi yanlış hesap yapmamıştır; hesabında hiç bulunmayan rejim değişikliğini görememiştir. Onu besleyen sistem, bir gün onu kesen sistem olur.",
            "Bir şirket yıllarca düzenli kazanç gösterebilir. Çalışanlar bunun doğal düzen olduğuna inanır. Teknoloji, yasa veya tek büyük dava oyunu değiştirince geçmiş ortalama koruma sağlamaz.",
            "Buradan 'Geçmiş işe yaramaz' sonucu çıkmaz. Geçmiş çoğu günlük olay için değerlidir. Sorun, sistemi kökten değiştirebilecek olayların veri setinde henüz görünmemesidir.",
            "Hindi bize güvenin en tehlikeli anda en yüksek olabileceğini hatırlatır. Uzun sakinlik, riskin yokluğu değil görünmemesi olabilir.",
        ], "BİRİNCİ KISIM · GÖREMEDİĞİMİZ OLAY", art="thanksgiving-turkey", caption="Her sakin gün hindinin güvenini artırır; sistem değiştiğinde geçmişteki düzen en tehlikeli yanılsamaya dönüşebilir."),
        entry("Siyah Kuğu'nun üç özelliği", [
            "Avrupa'da bütün kuğuların beyaz olduğu sanılırken Avustralya'da siyah kuğu görülmesi, tek gözlemin genel kuralı yıkabileceğini gösterdi. Taleb bu adı daha geniş bir olay sınıfı için kullanır.",
            "Birinci özellik, olayın mevcut beklenti dünyasının dışında kalmasıdır. İkinci özellik, çok büyük etki yaratmasıdır. Üçüncü özellik ise olaydan sonra insanların onu açıklayıp sanki beklenebilirmiş gibi göstermesidir.",
            "Bir piyango kazanmak kişi için şaşırtıcı ve büyük olabilir, fakat piyangonun birine çıkacağı sistem içinde bilinmektedir. Her nadir olay Siyah Kuğu değildir. Kavram, modelimizin kör olduğu orantısız sıçramaları vurgular.",
            "Aynı olay herkes için siyah olmayabilir. Hazırlıklı uzman bir risk görürken toplum görmeyebilir. Siyah Kuğu, olayın renginden çok gözlemcinin bilgi sınırıyla ilgilidir.",
            "Bu ayrım kavramın her habere yapıştırılmasını önler. Beklenmedik, büyük ve sonradan hikayeleştirilen üç ayak birlikte aranmalıdır.",
        ], "BİRİNCİ KISIM · GÖREMEDİĞİMİZ OLAY", art="black-swan-lake", caption="Siyah Kuğu beklenmedik, büyük etkili ve olduktan sonra kolayca açıklanmış görünen olayların simgesidir."),
        entry("Ortalamaistan ve Aşırıistan", [
            "Taleb iki hayali ülke kurar. Ortalamaistan'da tek bir gözlem bütünü fazla değiştiremez. Bin kişinin boy ortalamasına dünyanın en uzun insanını ekleseniz sonuç biraz oynar. Aşırıistan'da ise tek kişi toplamı ele geçirebilir.",
            "Servet, kitap satışı, internet görünürlüğü ve şirket büyüklüğü Aşırıistan'a daha yakındır. Bin yazarın satışına tek küresel yıldız eklendiğinde toplamın büyük bölümü ona ait olabilir. Ortalama temsil gücünü kaybeder.",
            "Bir kafede aynı anda hizmet verilen müşteri sayısı fiziksel olarak sınırlıdır. Dijital şarkı ise bir kez üretildikten sonra milyonlara ulaşabilir. Ölçeklenebilirlik, ödülü ve riski uçlara taşır.",
            "Gerçek dünya iki kutudan daha karmaşıktır. Aynı alanın bazı yönleri Ortalamaistan, bazıları Aşırıistan olabilir. Hastalık süresi ile sağlık harcamasının dağılımı aynı davranmayabilir.",
            "Önemli soru 'Ortalama kaç?'tan önce gelir: Burada tek bir aşırı olay toplamı değiştirebilir mi? Cevap evetse ortalamaya fazla güvenmemek gerekir.",
        ], "BİRİNCİ KISIM · GÖREMEDİĞİMİZ OLAY", art="two-countries", caption="Ortalamaistan'da uç değer bütünü az etkiler; Aşırıistan'da tek olay toplamın ve hikayenin çoğunu ele geçirebilir."),
        entry("Mezarlıkta görünmeyen başarısızlar", [
            "Başarılı girişimciler okul bırakıp risk aldıklarını anlatır. Onları dinleyen kişi 'Demek okul bırakmak başarı getiriyor' diyebilir. Aynı kararı verip kaybolmuş binlerce insan konferans sahnesinde değildir. Taleb buna sessiz kanıt sorunu der.",
            "Antik hikayede deniz kazasından kurtulanların adak resimleri gösterilir. Bir düşünür, 'Peki dua edip yine de boğulanların resimleri nerede?' diye sorar. Duvar yalnız yaşayanları sergiler; denizin sessiz mezarlığını göstermez.",
            "Sosyal medya da başarı müzesi kurar. Satılan ev, biten maraton ve büyüyen iş görünür. Aynı yöntemle başarısız olanlar daha az paylaşılır. Gördüğümüz örneklem hayatın tamamı değildir.",
            "Bu, başarı hikayelerinden hiçbir şey öğrenilemez demek değildir. Aynı stratejiyi kullanan başarısız örnekleri de aramak gerekir. Tavsiyenin sonucu mu, yoksa sonucu yaşayan kişinin sonradan seçtiği açıklama mı olduğunu sorgularız.",
            "Mezarlık görüntüsü sert ama yararlıdır: Veri setinde bulunmayanlar bazen sonucu belirleyen asıl kalabalıktır.",
        ], "BİRİNCİ KISIM · GÖREMEDİĞİMİZ OLAY", art="silent-cemetery", caption="Sahnede yalnız kazananlar konuşur; aynı yöntemi deneyip kaybolan sessiz kalabalık hesaba katılmadan başarı tarifi kurulamaz."),
        entry("Anlatı yanılgısı: Dağınık noktaları birleştirmek", [
            "Bir olay olduktan sonra zihin başlangıç, gelişme ve sonuç kurar. Şirketin neden battığını, takımın neden kazandığını veya bir ilişkinin neden bittiğini birkaç düzenli sebebe bağlarız. Hikaye belirsizliği sindirilebilir hale getirir.",
            "Sorun hikayenin yalan olması değil, seçici olmasıdır. Binlerce ayrıntıdan sonuca uyan birkaçını alır, rastlantıyı ve görünmeyen etkileşimi geride bırakır. Sonra anlatının akıcılığını doğrulukla karıştırırız.",
            "Bir komşunun hastalığını tek bir alışkanlığa bağlamak rahatlatıcı olabilir: 'Şunu yaptığı için oldu.' Böylece kendi güvenliğimizi kontrol altında hissederiz. Gerçek nedenler daha karmaşık ve kısmen bilinmez olabilir.",
            "Hikayesiz düşünmek mümkün değildir. Taleb'in önerisi anlatıyı tamamen bırakmak değil, onun sıkıştırma yaptığını hatırlamaktır. 'Başka hangi hikaye aynı veriye uyabilir?' sorusu iyi frendir.",
            "Dağınık noktaları birleştiren kalem, bazı noktaları görünmez yapar. Çizginin güzel olması haritanın tamamı olduğu anlamına gelmez.",
        ], "İKİNCİ KISIM · ZİHNİN TUZAKLARI", art="narrative-dots", caption="Zihin dağınık olayları akıcı çizgiye dönüştürür; iyi hikaye, seçilmeyen noktaları ve rastlantıyı saklayabilir."),
        entry("Doğrulama avcılığı", [
            "Bir fikre inandığımızda onu doğrulayan örnekleri toplamak doğal gelir. Yeni diyetin işe yaradığı beş kişiyi hatırlar, yaramadığı onlarca kişiyi 'doğru uygulamadılar' diye dışarıda bırakırız.",
            "Bin beyaz kuğu görmek bütün kuğuların beyaz olduğunu kesin kanıtlamaz; tek siyah kuğu bu genel hükmü yıkar. Bu nedenle iyi sınama, fikri destekleyen kadar onu zorlayan gözlemi de arar.",
            "İş görüşmesinde ilk beş dakikada olumlu izlenim edinen yönetici, sonraki cevapları bu fikri doğrulayacak biçimde yorumlayabilir. Önceden belirlenmiş ölçüt ve birden fazla değerlendirici kişisel hikayeyi azaltır.",
            "Karşı kanıt aramak sürekli karamsarlık değildir. Köprüyü açmadan önce yük testine sokmak, köprüye güvenmediğimiz için değil insan taşıyacağı için gereklidir.",
            "Taleb'in kuşkusu günlük bir cümleye çevrilebilir: 'Yanılıyor olsaydım ne görmeyi beklerdim?' Bu soru fikrin kapısını içeriden açar.",
        ], "İKİNCİ KISIM · ZİHNİN TUZAKLARI", art="confirmation-hunt", caption="Doğrulama avcısı sevdiği örnekleri toplar; iyi sınama fikrin yanlış çıkabileceği kapıyı özellikle açık bırakır."),
        entry("Kumarhane yanılgısı", [
            "Kumarhanede ruletin olasılıkları, kart kuralları ve masa limitleri hesaplanabilir. Risk yöneticileri bu düzenli oyuna odaklanabilir. Oysa kumarhanenin en büyük zararı masadan değil, öngörülmemiş bir olaydan gelebilir.",
            "Taleb buna oyun yanılgısı der: Gerçek hayatı, kuralları ve olasılıkları baştan belli oyunlara benzetmek. Model temizdir, dünya ise kural değiştirir, oyuncu ekler ve bazen masayı devirir.",
            "Bir fabrikanın arıza tablosu makinelerin bilinen hata oranlarını içerir. Sel, tedarik zinciri çöküşü veya kilit kişinin ayrılması tabloda ayrı düşünülmemiş olabilir. Hesap doğru, kapsam eksiktir.",
            "Modeller işe yaramaz değildir. Uçak, sigorta ve sağlık planlaması onsuz olmaz. Sorun modelin sınırını unutmak ve ölçülemeyeni sıfır sanmaktır.",
            "Kumarhane görüntüsü, kesin sayı gördüğümüzde şu soruyu sordurur: Bu sayı oyunun dışından gelebilecek hangi olayı içermiyor?",
        ], "İKİNCİ KISIM · ZİHNİN TUZAKLARI", art="casino-outside-risk", caption="Masa oyunlarının riski hesaplanabilir; gerçek zarar bazen kuralların dışında kalan ve tabloda hiç bulunmayan olaydan gelir."),
        entry("Uzman neden emin konuşur?", [
            "Televizyonda gelecek hakkında duraksamadan konuşan uzman güven verir. 'Bilmiyorum' diyen kişi daha az etkileyici görünür. Taleb, karmaşık sosyal sistemlerde tahmin başarısının çoğu kez ün ve özgüven kadar güçlü olmadığını savunur.",
            "İnsanlar sonuç açıklanınca doğru tahmini hatırlar, yanlış tahminleri unutur. Uzman da geçmiş cümlesini yeni olaya uyacak biçimde yorumlayabilir. Tahminler tarih atılarak kaydedilmediğinde hafıza kolayca editör olur.",
            "Uzmanlık alan farkı taşır. Kısa vadeli hava tahmini ile on yıl sonraki siyasi düzen aynı belirsizlikte değildir. Deneyin tekrarlanabildiği dar alanlarda uzman çok değerli olabilir; Aşırıistan'da alçakgönüllülük gerekir.",
            "İyi uzman kesinlik satmak yerine aralık, koşul ve bilinmeyenleri söyler. Fikrini neyin değiştireceğini açıklar. Bu üslup daha sıkıcı ama daha güvenilirdir.",
            "Taleb'in sert eleştirisini bütün uzmanlara düşmanlık diye okumamak gerekir. Amaç bilgiye değil, bilginin sınırını gizleyen gösteriye kuşku duymaktır.",
        ], "İKİNCİ KISIM · ZİHNİN TUZAKLARI", art="confident-pundit", caption="Kesin konuşmak doğru tahmin göstergesi değildir; güvenilir uzman koşulları, aralığı ve fikrini değiştirecek kanıtı açıklar."),
        entry("Çan eğrisi ne zaman kırılır?", [
            "Boy uzunluğu gibi birçok özellik ortalama çevresinde toplanır ve uç değerler hızla seyrekleşir. Çan eğrisi bu dünyada güçlü araçtır. Taleb'in itirazı, aynı rahat modeli servet, piyasa hareketi veya savaş büyüklüğü gibi kalın kuyruklu alanlara taşımaktır.",
            "Kalın kuyruk, uzak olayların sandığımızdan daha sık ve daha etkili olmasıdır. Birkaç dev sonuç toplamı belirleyebilir. Geçmiş veri kısa ise bu uçları görmeyip riski küçük hesaplayabiliriz.",
            "Bir şehirde günlük ekmek tüketimi çok oynak olmayabilir. Tek bir kitabın satış sayısı ise milyonlarla sıfır arasında dağılabilir. Aynı istatistik dili iki alanı aynı derecede iyi anlatmaz.",
            "Taleb bazen çan eğrisine karşı savaşını fazla geniş anlatır. Normal dağılım doğru alanda son derece yararlıdır. Sorun araç değil, hangi malzemede kullanıldığını kontrol etmemektir.",
            "Çan eğrisinin kırıldığı görüntü, model seçiminin teknik ayrıntı değil, güvenlik kararı olabileceğini hatırlatır.",
        ], "ÜÇÜNCÜ KISIM · AŞIRIİSTAN'DA YAŞAM", art="broken-bell-curve", caption="Çan eğrisi bazı alanlarda güçlüdür; kalın kuyruklu dünyada nadir uçlar toplamı ve güvenlik hesabını ele geçirebilir."),
        entry("Ölçeklenebilir işlerin piyangosu", [
            "Diş hekimi aynı saatte sınırlı sayıda hasta görebilir. Bir müzisyenin kaydı ise aynı anda milyonlarca kişiye ulaşabilir. Taleb ikinci işi ölçeklenebilir sayar. Gelir sınırı büyür, fakat kazananların yoğunlaşması da artar.",
            "Yazar, uygulama geliştirici veya içerik üreticisi küçük maliyetle büyük kitleye ulaşabilir. Bu fırsat çekicidir. Aynı anda çok sayıda insan yarışır ve görünürlük birkaç kişide toplanabilir.",
            "Başarı hikayesi yalnız yetenekle açıklanamaz. Zamanlama, ağ etkisi, şans ve ilk küçük avantajın büyümesi rol oynar. Bu, emeğin değersiz olduğu değil, sonucun emeğe düzgün oranlanmadığı anlamına gelir.",
            "Ölçeklenmeyen işler küçümsenmemelidir. Hemşire, usta ve öğretmen doğrudan ilişki kurar; gelir tavanı olabilir ama toplumsal değeri yüksektir. Piyasanın ödülü değer ölçüsü değildir.",
            "Aşırıistan'da kariyer planı yalnız zirve hayaline dayanırsa kırılgan olur. Temel geçim ile büyük denemeyi ayırmak daha dayanıklı olabilir.",
        ], "ÜÇÜNCÜ KISIM · AŞIRIİSTAN'DA YAŞAM", art="scalable-stage", caption="Ölçeklenebilir iş milyonlara ulaşabilir; aynı yapı ödülü az sayıda kazanana yığarak başarıyı emekten koparabilir."),
        entry("Geriye bakınca her şey kaçınılmaz görünür", [
            "Bugünün dünyasından geçmişe bakınca internetin, belirli şirketlerin veya siyasi sonuçların adım adım kaçınılmaz geldiğini sanabiliriz. Oysa karar anında birçok yol açıktı; küçük rastlantılar bazılarını kapattı.",
            "Bir filmin sonunu bilen kişi ikinci izleyişte bütün ipuçlarını fark eder. İlk izleyişte aynı işaretler binlerce ayrıntı arasındadır. Tarih yorumunda sonu bilmenin ayrıcalığını yaşayanların bilgisini sanmak kolaydır.",
            "Bu yanılgı yöneticiyi de etkiler. Başarılı projedeki kararlar bilgelik, başarısız projedeki benzer kararlar aptallık diye anlatılır. Sonuç, karar kalitesini geriye doğru boyar.",
            "İyi değerlendirme, o anda mevcut bilgiyle sürecin kalitesine bakar. Kötü karar şansla iyi sonuç, iyi karar şanssızlıkla kötü sonuç üretebilir.",
            "Taleb'in tarih uyarısı, geçmişi anlamsız yapmaz. Onu tek raylı tren yerine ayrılan yollar ve kapanan fırsatlar olarak görmemizi ister.",
        ], "ÜÇÜNCÜ KISIM · AŞIRIİSTAN'DA YAŞAM", art="branching-history", caption="Sonu bildiğimizde geçmiş tek ray gibi görünür; karar anında ise birçok yol açık ve sonuç kısmen rastlantıya bağlıdır."),
        entry("Tümevarım sorunu: Güneş yarın doğacak mı?", [
            "Geçmişte tekrar eden düzenin gelecekte süreceğine güveniriz. Sabah Güneş'in doğacağını, musluktan su akacağını ve işyerinin açılacağını varsayarız. Günlük hayat bu güven olmadan işlemez.",
            "Felsefedeki tümevarım sorunu, geçmiş tekrarın geleceği mantıksal kesinlikle garanti etmediğini söyler. Taleb bu eski sorunu risk dünyasına taşır. Bin sakin gün, bin birinci günün sakin olacağını kanıtlamaz.",
            "Buradan hiçbir şey planlanamaz sonucu çıkmaz. Düzenli alanlarda geçmiş güçlü rehberdir. Yapılacak iş, tahmin hatasının bedeli büyük olduğunda güvenlik payı bırakmaktır.",
            "Asansör kablosu ortalama yükün biraz üstüne göre yapılmaz; büyük güvenlik katsayısı kullanılır. Çünkü yanılmanın bedeli, fazla malzeme kullanmanın bedelinden yüksektir.",
            "Tümevarım sorusu bizi felç etmek için değil, kesinlik ile pratik güven arasındaki farkı görmek için kullanılır.",
        ], "ÜÇÜNCÜ KISIM · AŞIRIİSTAN'DA YAŞAM", art="induction-sunrise", caption="Tekrarlanan geçmiş pratik güven sağlar ama mantıksal garanti vermez; büyük bedelli alanlarda güvenlik payı gerekir."),
        entry("Tahmin ufku uzadıkça sis koyulaşır", [
            "Yarınki randevu saatini planlamak ile on yıl sonraki mesleğin ayrıntısını bilmek aynı değildir. Zaman ufku uzadıkça teknoloji, politika, sağlık ve tesadüf yolları çoğalır. Küçük hata dallanarak büyür.",
            "Şirketler beş yıllık planı kesin rakamlarla yazdığında sayının ayrıntısı güven hissi yaratabilir. Oysa virgülden sonraki basamak bilgi değil süs olabilir. Senaryo ve aralık daha dürüsttür.",
            "Tahminin zor olması hazırlığın gereksiz olduğu anlamına gelmez. Tam tersine, tek geleceğe kilitlenmek yerine farklı koşullarda çalışacak seçenekler kurmak gerekir.",
            "Bir aile bütçesi gelir artışını umut edebilir, fakat acil durum payı bırakır. Plan hedef verir; tampon, planın yanlış çıkmasına dayanır.",
            "Sisli yolda far yalnız belli mesafeyi gösterir. Sürücü bütün yolu gördüğünü iddia etmez; hızını görüş mesafesine göre ayarlar.",
        ], "ÜÇÜNCÜ KISIM · AŞIRIİSTAN'DA YAŞAM", art="foggy-forecast", caption="Tahmin ufku uzadıkça sis artar; iyi plan tek geleceği bilmek yerine görüş mesafesine uygun hız ve seçenek kurar."),
        entry("Halter stratejisi", [
            "Taleb belirsizlikte bir halter görüntüsü kullanır. Ağırlığın büyük bölümü çok güvenli tarafta, küçük bölümü ise yüksek risk ve yüksek fırsat tarafındadır. Ortadaki sahte güven bölgesinden kaçınır.",
            "Kariyerde bu, temel geliri korurken sınırlı zamanla cesur proje denemek olabilir. Proje başarısız olursa hayat çökmez; başarılı olursa büyük kapı açabilir. Uygulama kişiye göre değişir.",
            "Finansta halterin ne anlama geldiği teknik ve kişiseldir. Kitaptan tek başına yatırım oranı çıkarılamaz. Güvenli görünen araçların da enflasyon, kurum ve likidite riski olabilir.",
            "Stratejinin ana ilkesi aşağı yönü sınırlayıp yukarı yönü açık bırakmaktır. Bir denemenin kaybını baştan taşıyabileceğiniz boyuta indirmek buna örnektir.",
            "Halter görüntüsü cesaret ile güvenliği düşman olmaktan çıkarır. Küçük kontrollü riskler, bütün hayatı tek tahmine bağlamadan yeniliğe alan açar.",
        ], "DÖRDÜNCÜ KISIM · KIRILGANLIĞI AZALTMAK", art="barbell-strategy", caption="Halter stratejisi temel güvenliği korurken küçük, sınırlı kayıplı alanlarda büyük fırsatlara açık denemeler yapar."),
        entry("Sağlamlık, kırılganlık ve fazlalık", [
            "Kırılgan bardak darbede zarar görür. Sağlam taş darbeye dayanır. Taleb daha sonraki çalışmalarında düzensizlikten yarar gören sistemleri ayrıca geliştirecektir; Siyah Kuğu'nda temel amaç beklenmedik darbeye karşı kırılganlığı azaltmaktır.",
            "Fazlalık verimsiz görünebilir. Yedek lastik, ikinci tedarikçi, boş hastane kapasitesi veya nakit tamponu normal günde kullanılmaz. Kriz gününde sistemin yaşamını sürdürür.",
            "Aşırı verimlilik her boşluğu keser. Tam zamanında çalışan zincir ucuzdur; tek parça gecikince bütün üretim durabilir. Dayanıklılık bazen kullanılmayan kaynak için ödeme yapar.",
            "Merkezileşme de kırılganlık yaratabilir. Tek büyük sistem çökerse herkes etkilenir. Küçük ve bağımsız parçalar hata sınırını daraltabilir, fakat her alanda aynı çözüm çalışmaz.",
            "Fazlalık israf ile aynı değildir. Soru, boş kapasitenin hangi nadir darbede sigorta görevi gördüğüdür.",
        ], "DÖRDÜNCÜ KISIM · KIRILGANLIĞI AZALTMAK", art="redundant-bridge", caption="Yedek ve boş kapasite sakin günde pahalı görünür; beklenmedik darbede sistemin bütünüyle çökmesini önleyebilir."),
        entry("Olumlu Siyah Kuğu'ya kapı açmak", [
            "Beklenmedik olayların hepsi felaket değildir. Bir fikir, karşılaşma veya küçük deneme çok büyük olumlu sonuç doğurabilir. İnternet üzerindeki bir yazı beklenmedik işbirliğine, tesadüfi sohbet yeni mesleğe dönüşebilir.",
            "Olumlu sürprizi tahmin etmek yerine ona maruz kalma alanı artırılabilir. Çok sayıda düşük maliyetli deneme yapmak, farklı insanlarla konuşmak, üretimi görünür kılmak ve seçenekleri açık tutmak buna örnektir.",
            "Şans kapıyı çaldığında hazırlık yine önemlidir. Müzisyen yıllarca çalışmamışsa beklenmedik sahne fırsatını kullanamayabilir. Talih sonuçta rol oynar; emek fırsattan yararlanma kapasitesini büyütür.",
            "Her kapıyı açık tutmak da mümkün değildir. Dikkat ve zaman sınırlıdır. Ama tek dar plana kapanmak, olumlu sapmaların içeri gireceği pencereyi kapatır.",
            "Taleb'in iyimser tarafı burada görünür: Geleceği bilmemek yalnız korku değil, hayal edemediğimiz iyi sonuçların da mümkün olmasıdır.",
        ], "DÖRDÜNCÜ KISIM · KIRILGANLIĞI AZALTMAK", art="positive-black-swan", caption="Olumlu Siyah Kuğu tahmin edilmez; düşük maliyetli denemeler ve açık seçenekler onun içeri gireceği kapıları çoğaltır."),
        entry("Taleb nerede güçlü, nerede yorucu?", [
            "Kitabın gücü, düzgün geçmiş grafiğinin verdiği sahte güveni bozmasıdır. Sessiz kanıt, anlatı yanılgısı, model sınırı ve kalın kuyruk gibi fikirler karar vermeyi gerçekten değiştirir.",
            "Taleb bazen eleştirdiği insanları karikatüre çevirir, kendi örneklerini geniş genellemelere taşır ve kavramların sınırını polemik içinde bulanıklaştırır. Her büyük sürprizi Siyah Kuğu diye adlandırmak kavramı değersizleştirir.",
            "Tahmin edilemeyen olaya hazırlanma öğüdü de kaynak meselesini saklayabilir. Yedek, tampon ve seçenek kurmak yoksul birey için zengin kurumdan çok daha zordur. Dayanıklılık yalnız kişisel bilgelik değil, toplumsal politika sorusudur.",
            "En iyi okuma Taleb'in kesin cümlelerini yeni bir dogma yapmaz. Onun kuşkusunu kendisine de uygular: Bu örnekte görünmeyen veri ne, karşı örnek ne, risk kime dağılıyor?",
        ], "SONUÇ"),
        entry("Gündelik hayata üç güvenli uygulama", [
            "Birinci uygulama tahmini kaydetmektir. Sonuçtan önce ne beklediğinizi yazın; hafızanın sonradan hikayeyi düzeltmesini engellersiniz. İkincisi tek noktadan arıza yerlerini bulmaktır: Tek gelir, tek tedarikçi, tek şifre veya tek uzman nerede?",
            "Üçüncüsü küçük tersinir denemeler yapmaktır. Kaybı baştan sınırlı olan deneme, uzun rapordan daha çok bilgi verebilir. Başarısızlık bütün sistemi yıkmadan erken gelir.",
            "Sağlık, hukuk ve para gibi yüksek riskli alanlarda bu ilkeler uzman değerlendirmesinin yerine geçmez. Belirsizliği kabul etmek, rastgele davranmak değil daha dikkatli güvenlik payı kurmaktır.",
        ], "SONUÇ"),
        entry("Bir dakikalık harita", [
            "Siyah Kuğu beklenti dışında kalan, büyük etki yaratan ve sonradan kolayca açıklanmış görünen olaydır. Aşırıistan'da tek sonuç toplamı ele geçirebilir; geçmiş ortalama uç riski saklayabilir.",
            "Zihin sessiz kanıtı unutur, doğrulayan örneği seçer ve dağınık olaydan düzgün hikaye kurar. Modeller belirli oyunda işe yarar; oyunun dışından geleni sıfır sanmamak gerekir.",
            "Geleceği kesin bilmek yerine kırılganlığı azaltın, yedek ve güvenlik payı kurun, kaybı sınırlı denemeler yapın ve olumlu sürprize açık seçenekler bırakın.",
        ], "SONUÇ"),
        entry("Akılda kalacak beş görüntü", [
            "Beslenen hindi: Sakin geçmiş güveni yanlış anda büyütebilir. Siyah kuğu: Tek gözlem genel kuralı yıkar. Sessiz mezarlık: Görünmeyen başarısızları say. Kırık çan eğrisi: Uçlar toplamı ele geçirebilir. Halter: Aşağı yönü sınırla, fırsat kapısını açık tut.",
            "Bu görüntüler geleceği gösteren fal değildir. Kesin sayı ve güzel hikaye karşısında hangi bilginin eksik olduğunu, yanılmanın bedelini ve sistemin nereden kırılacağını sormaya yarar.",
            "Taleb'in en kalıcı cümlesi şu düşüncedir: Bilmediğimizi kabul etmek güçsüzlük değil, yanlış kesinliğin vereceği zarardan korunmanın başlangıcıdır.",
        ], "SONUÇ"),
    ],
})


BOOKS.append({
    "bookNo": 243,
    "title": "Yorgunluk Toplumu",
    "author": "Byung-Chul Han",
    "subtitle": "Sürekli başarma, kendini geliştirme ve erişilebilir olma baskısının insanı nasıl kendi yöneticisine çevirdiğini anlatan sade ve eleştirel rehber.",
    "coverImage": "/images/optimized/summary-art-243-yorgunluk-toplumu-v2-960.webp",
    "coverStyle": "artwork",
    "pdfUrl": "/data/pdfs/243-yorgunluk-toplumu-ozeti.pdf",
    "pdfLabel": "25-50 sayfalık PDF'yi indir",
    "longForm": True,
    "chapterArtStyle": "monochrome-engraving",
    "chapterArtColor": "#665078",
    "meta": {
        "originalTitle": "Müdigkeitsgesellschaft / The Burnout Society",
        "compiler": "Zihin Gezgini · Yapay zeka destekli çalışma",
        "date": "Temmuz 2026",
        "language": "Türkçe",
    },
    "intro": "Byung-Chul Han çok kısa bir kitapta büyük bir teşhis koyar: Geçmişin toplumu insana 'Yapmalısın' derken bugünün performans toplumu 'Yapabilirsin' der. Bu olumlu görünen cümle sınır tanımadığında kişi kendi patronuna, denetçisine ve sömürücüsüne dönüşür. Yorgunluk artık yalnız kaslarda değil, dikkat ve benlikte yaşanır. Bu rehber kitabın sekiz bölümlük düşünce hattını gündelik sahnelerle açıyor; fakat depresyon, ADHD ve tükenmişliği tek toplumsal nedene indirmiyor. Han'ın şiirsel teşhisini tıbbi açıklama yerine koymadan, sınıf, bakım emeği ve çalışma koşulları gibi eksik bıraktığı alanları da ekliyor.",
    "sources": [
        {"id": 1, "title": "The Burnout Society - Stanford University Press resmi tanıtımı", "url": "https://www.sup.org/books/theory-and-philosophy/burnout-society"},
        {"id": 2, "title": "Stanford University Press - birinci bölüm örneği", "url": "https://www.sup.org/books/theory-and-philosophy/burnout-society/excerpt/chapter-1"},
        {"id": 3, "title": "De Gruyter / Stanford - kitabın bölüm içeriği", "url": "https://www.degruyterbrill.com/document/doi/10.1515/9780804797504-fm/html?lang=en"},
        {"id": 4, "title": "University of Notre Dame - Yorgunluk Toplumu eleştirisinin sınırları", "url": "https://churchlifejournal.nd.edu/articles/the-limits-of-the-burnout-society-critique/"},
        {"id": 5, "title": "Constellations - Han'ın eleştirel çerçevesindeki paradokslar", "url": "https://onlinelibrary.wiley.com/doi/full/10.1111/1467-8675.70007"},
    ],
    "entries": [
        entry("Bu kitap nasıl okunmalı?", [
            "Han istatistik raporu yazmaz; çağın ruhunu yoğun benzetmelerle anlatan felsefi deneme yazar. Cümleleri bir odayı aniden aydınlatabilir, fakat ışığın dışında kalan ayrıntılar vardır.",
            "Kitabı 'Bütün hastalıkların nedeni telefon ve kapitalizm' diye okumak yanlış olur. Ruhsal ve nörolojik durumlar biyolojik, psikolojik ve toplumsal birçok etkene sahiptir. Han'ın dili klinik tanı değil, toplumsal deneyim yorumudur.",
            "Bu özet iki soruyu birlikte taşıyacak: Han hangi gündelik duyguyu çok iyi yakalıyor? Bu duyguyu açıklarken kimlerin deneyimini ve hangi nedenleri eksik bırakıyor?",
        ], "BAŞLANGIÇ"),
        entry("Dış düşmandan iç aşırı yüke", [
            "Han geçmiş yüzyılı bağışıklık modeliyle anlatır. İçeride biz, dışarıda yabancı vardır. Tehdit dışarıdan gelir; sınır, yasak ve savunma öne çıkar. Bugünün sorunlarını ise aşırı olumlu yükle ilişkilendirir: fazla iletişim, fazla üretim, fazla uyarı.",
            "Bir kalenin kapısına saldıran düşmanı görmek kolaydır. Telefon bildirimleri, açık sekmeler ve bitmeyen hedefler ise misafir gibi içeri girer. Her biri küçük ve yararlı görünür; toplamda zihnin odalarını doldurur.",
            "Han depresyon, ADHD ve tükenmişlik gibi durumları bu 'nöronal' çağın işaretleri olarak sayar. Bu bağlantı güçlü bir kültür eleştirisidir, tıbbi neden açıklaması değildir. Bu durumlar yalnız aşırı pozitiflikten doğmaz.",
            "Yine de deneyim tanıdıktır. İnsan tehlikeden kaçmıyor olabilir; kendi yapılacaklar listesinin altında ezilir. Dışarıdan saldırı yoktur, içeride durmayan bir motor vardır.",
            "İlk görüntü kalkan ile aşırı yüklenen beyin arasındadır. Sorun yalnız neyi dışarıda tuttuğumuz değil, ne kadar şeyi içeri aldığımızdır.",
        ], "BİRİNCİ KISIM · PERFORMANSIN TEŞHİSİ", art="shield-and-overload", caption="Eski tehdit kapıdaki düşman gibi görünürdü; yeni yorgunluk yararlı görünen uyarıların içeride birikmesiyle büyüyebilir."),
        entry("Fabrikanın 'Yapmalısın'ı, ekranın 'Yapabilirsin'i", [
            "Disiplin toplumunda fabrika düdüğü, okul zili ve ceza tehdidi vardır. Emir dışarıdan gelir: Zamanında gelmelisin, kurala uymalısın. Han bugünün performans toplumunda dilin değiştiğini söyler: Yapabilirsin, kendini aşabilirsin, en iyi halin olabilirsin.",
            "İkinci dil daha özgür ve sevecen görünür. Gerçekten de eski yasakların bir bölümü kalkmış, insanlar daha çok seçenek kazanmıştır. Fakat yapabilme sınırsız göreve dönüşünce başarısızlık kişisel kusur gibi yaşanır.",
            "Koşu bandında biri bizi kırbaçlamaz. Hızı kendimiz artırır, ekrandaki önceki derecemizi geçmeye çalışırız. Düşünce şudur: Durursam beni engelleyen dış güç değil, yetersiz ben olurum.",
            "Bu değişim dış baskının bittiği anlamına gelmez. Düşük ücret, vardiya, işsizlik korkusu ve yönetici denetimi sürer. Han'ın modeli özellikle orta sınıf ve bilgi işi deneyimini güçlü yakalar, bütün emeği aynı biçimde açıklamaz.",
            "İki toplum üst üste bulunabilir: Patron 'Yapmalısın' der, çalışan içeriden 'Daha fazlasını yapabilmeliyim' diye ekler.",
        ], "BİRİNCİ KISIM · PERFORMANSIN TEŞHİSİ", art="factory-and-treadmill", caption="Dış emir ile iç hedef yan yana çalışabilir; insan hem kurala uyar hem de koşu bandının hızını kendi eliyle artırır."),
        entry("Olumlu kelimelerin ağır baskısı", [
            "'Her şeyi yapabilirsin' cümlesi çocuk için cesaret verici olabilir. Fakat yapısal engelleri ve gerçek sınırları yok saydığında acımasızlaşır. Yapamadığınızda dünya değil, yalnız siz suçlu görünürsünüz.",
            "Bir çalışan aynı anda iyi ebeveyn, fit beden, sürekli öğrenen uzman, sosyal arkadaş ve huzurlu insan olmaya çağrılır. Bu hedeflerin her biri tek başına güzel olabilir. Hepsi kesintisiz görev olduğunda hayat kontrol paneline dönüşür.",
            "Olumluluk itirazı da zorlaştırabilir. Toplantıda 'Bu süre gerçekçi değil' diyen kişi çözüm odaklı olmamakla suçlanır. Sorunu söylemek negatiflik, sınır koymak isteksizlik sayılır.",
            "Han'ın 'olumluluğun şiddeti' dediği şey yumruk gibi görünmez. İnsan kendi isteğiyle katılıyor hisseder. Bu nedenle baskının kaynağını işaret etmek zorlaşır.",
            "Olumlu cümle ancak hayır deme hakkı, başarısızlık alanı ve maddi destekle gerçek özgürlüğe dönüşür. Yoksa gülümseyen bir emir olabilir.",
        ], "BİRİNCİ KISIM · PERFORMANSIN TEŞHİSİ", art="positive-command", caption="'Yapabilirsin' cümlesi hayır deme ve sınır hakkı yoksa cesaret değil, gülümseyen bir emre dönüşebilir."),
        entry("Kendi patronu, kendi işçisi", [
            "Han'ın en çarpıcı fikri öz sömürüdür. Kişi dış patronun emrini beklemeden kendini çalıştırır, ölçer ve cezalandırır. Özgür olduğunu düşünürken patron ile işçi aynı bedende birleşir.",
            "Serbest çalışan gece yarısı bilgisayarı kapatamaz. Kimse zorlamıyor gibi görünür; kira, müşteri puanı, görünürlük ve kendi hedefi aynı anda onu masada tutar. Dış koşullar iç sese dönüşmüştür.",
            "Öz sömürü kavramı gerçek patronu görünmez yapmamalıdır. Platform kuralları, ücret politikası ve güvencesizlik somuttur. İnsan yalnız kendine baskı uygulamaz; sistem bu baskıyı ödüllendirir ve zorunlu kılabilir.",
            "Aynadaki patron dinlenirken bile konuşur: Bugün kaç adım, kaç sayfa, kaç müşteri, kaç beğeni? Dinlenme de ertesi gün daha verimli olmak için yatırım sayılır.",
            "Özgürlük, yalnız işi kendi seçmek değil, işi bırakabilme ve sonuçta yok olmama gücüdür. Bu güç ekonomik ve toplumsal koşullara bağlıdır.",
        ], "BİRİNCİ KISIM · PERFORMANSIN TEŞHİSİ", art="boss-in-mirror", caption="Öz sömürüde patron aynaya taşınır; dış hedefler kişinin kendi sesi gibi konuşarak dinlenmeyi bile performansa bağlar."),
        entry("Çoklu görev: İlerleme mi, alarm hali mi?", [
            "Aynı anda e-posta yazıp toplantı dinlemek, mesaj cevaplamak ve yemek düşünmek modern beceri gibi sunulur. Han bunun insanlığın ileri yeteneği değil, vahşi doğadaki hayvanın sürekli çevre kontrolüne benzeyen dağınık dikkat olduğunu söyler.",
            "Bir kuş yemek yerken hem gagasına hem yaklaşan tehlikeye bakar. Derin düşünmeye değil hayatta kalmaya uygundur. Sürekli bildirim de zihni benzer küçük sıçramalara zorlar.",
            "Beyin birçok bilişsel işi gerçekten aynı anda yürütmekten çok hızlı geçiş yapar. Her geçiş iz bırakır. Gün sonunda çok şey yapılmış hissi, önemli hiçbir işin derinleşmediği gerçeğini saklayabilir.",
            "Bakım işi yapan kişi için çoklu görev bazen seçim değil zorunluluktur. Çocuk, yemek ve iş aynı anda çağırır. Sorunu kişisel dikkat eksikliği diye anlatmak bakım düzenini görünmez kılar.",
            "Han'ın uyarısı, hayatın bütün eşzamanlılığını yok etmek değil; düşünme gerektiren iş için kesintisiz zamanın değerini yeniden hatırlamaktır.",
        ], "İKİNCİ KISIM · DİKKAT VE DURMAK", art="multitasking-bird", caption="Çoklu görev derin ustalık değil, sürekli çevre tarayan alarm dikkati üretebilir; bazı insanlar içinse yapısal zorunluluktur."),
        entry("Derin can sıkıntısının kuyusu", [
            "Telefon gelmeden önce otobüs beklemek boşluk yaratırdı. İnsan pencereden bakar, düşünce kendi yoluna giderdi. Bugün birkaç saniyelik boşluk ekrana uzanan elle kapatılır. Han derin can sıkıntısının kaybını önemser.",
            "Can sıkıntısı her zaman iyi değildir. Yalnızlık, işsizlik veya depresyon içindeki ağır boşluk acı verici olabilir. Han'ın savunduğu şey zorunlu sıkıntı değil, hiçbir uyarıyla hemen doldurulmayan serbest zaman alanıdır.",
            "Bir kuyunun dibindeki su hemen görünmez. Beklemek gerekir. Yaratıcı fikir de çoğu zaman ilk dakikada gelmez; zihnin hazır parçaları tükendikten sonra yeni bağlantı oluşur.",
            "Çocuk 'Sıkıldım' dediğinde hemen etkinlik sunmak yerine güvenli boşluk bırakıldığında kendi oyununu kurabilir. Yetişkin için yürüyüş, sessiz oturuş veya amaçsız bakış benzer alan açar.",
            "Derin can sıkıntısı verimsiz zaman değil, henüz hedefe dönüşmemiş ihtimaldir. Her boşluğu ürünle doldurmak bu ihtimali kurutur.",
        ], "İKİNCİ KISIM · DİKKAT VE DURMAK", art="boredom-well", caption="Derin can sıkıntısı hemen doldurulmayan bir kuyu gibidir; yeni düşünce hazır uyarılar tükendiğinde yüzeye çıkabilir."),
        entry("Vita activa ve durmayan makine", [
            "Han, Hannah Arendt'in etkin yaşam tartışmasına girer. Modern insanın yalnız çalışmadığını, kendini sürekli üreten bir projeye dönüştüğünü söyler. Faaliyet anlamın aracı olmaktan çıkıp kendi başına zorunluluk olur.",
            "Çamaşır makinesi işini bitirince durur. İnsan ise bir hedef tamamlandığında yenisini açar. Gelen kutusu sıfırlanır, birkaç dakika sonra tekrar kontrol edilir. Durma ölçütü yoktur.",
            "Faaliyet kötü değildir. Üretmek, bakım vermek ve siyasal eylem insan yaşamını kurar. Sorun her hareketin ekonomik veya kişisel performans puanına çevrilmesidir.",
            "Arendt'in dünyasında eylem başkalarıyla ortak alan kurabilir. Han'ın yorgun öznesi ise çoğu kez kendi projesine kapanır. Birlikte dünyayı değiştirmek yerine kendini günceller.",
            "Makine görüntüsü şu soruyu bırakır: Bu işi hangi amaç için yapıyorum ve bitmiş sayılacağı bir an var mı? Cevap yoksa faaliyet kendi yakıtımızı tüketir.",
        ], "İKİNCİ KISIM · DİKKAT VE DURMAK", art="endless-machine", caption="Durma ölçütü olmayan faaliyet, hedefleri tamamlamak yerine sürekli yenileyen ve insanı kendi yakıtıyla çalıştıran makineye dönüşür."),
        entry("Bakmayı öğrenmek", [
            "Han düşüncenin ilk dersini bakmayı öğrenmekte bulur. Hemen tepki vermemek, dürtünün peşinden koşmamak ve nesnenin kendi hızında görünmesine izin vermek. Bu pasiflik değil, dikkatin eğitilmesidir.",
            "Kuş gözlemcisi ağacın önünde sabırla durur. İlk dakika yalnız yaprak görür. Sonra küçük hareketi, rengi ve sesi ayırt eder. Hızlı bakanın boş sandığı yerde dünya çoğalır.",
            "Toplantıda sert söz duyunca anında cevap vermek güç gibi görünebilir. Bir nefeslik gecikme, tepki ile seçilmiş cevap arasına alan koyar. İrade bazen hızlı hareket değil geciktirebilme becerisidir.",
            "Dijital akış, her görüntüye birkaç saniye verir. Bakış nesneye yerleşmeden yenisi gelir. Uzun kitap, resim veya yüz yüze konuşma bu ritme karşı sabır kasını çalıştırır.",
            "Bakmayı öğrenmek dünyayı tüketilecek içerik olmaktan çıkarır. Nesnenin, insanın ve fikrin bize hemen hizmet etmeyen yönünü görmeye başlarız.",
        ], "İKİNCİ KISIM · DİKKAT VE DURMAK", art="patient-seeing", caption="Bakmayı öğrenmek tepkiyi geciktirir; hızlı gözün boş sandığı yerde ayrıntı, ilişki ve seçme özgürlüğü belirir."),
        entry("Bartleby'nin masası", [
            "Melville'in katibi Bartleby kendisinden istenen işlere giderek 'Yapmamayı tercih ederim' diye karşılık verir. Han bu figürü disiplin toplumunun dünyasında okur. Bartleby'nin reddi özgürleştirici slogan olmaktan çok donmuş bir çıkmaz taşır.",
            "Bugün 'Hayır' demek direnç gibi görünebilir. Fakat işini kaybetme riski taşıyan çalışan için bu seçenek eşit değildir. Reddetme gücü maddi güvenceye bağlıdır.",
            "Bartleby hiçbir alternatif kurmaz; yalnız çekilir. Bu nedenle pasif direnç ile tükenmiş kapanma arasındaki çizgi belirsizdir. Bazen hayır yeni alan açar, bazen yardım çağrısıdır.",
            "Han performans toplumunda öznenin dış emre değil kendi beklentisine yenildiğini söyler. Bartleby'nin eski 'Yapmayacağım'ı, bugünün 'Artık yapamıyorum'una dönüşebilir.",
            "Boş masa görüntüsü romantik değildir. İnsanın kapasitesi çöktüğünde felsefi direniş etiketi koymadan önce bakım ve destek gerekir.",
        ], "İKİNCİ KISIM · DİKKAT VE DURMAK", art="bartleby-desk", caption="Bartleby'nin boş masası hayır deme ile yapamaz hale gelme arasındaki farkı ve reddin maddi koşullarını düşündürür."),
        entry("Ben yorgunluğu", [
            "Han bir tür yorgunluğu insanı kendine kapatan 'ben yorgunluğu' olarak anlatır. Kişi yalnız başkalarına değil, kendine de tahammül edemez. Dünya görevler ve başarısızlık aynaları halinde görünür.",
            "Yoğun tükenmede arkadaşın mesajı bile yeni iş gibi hissedilebilir. Kişi sevmediği için değil, cevap verecek iç alan bulamadığı için geri çekilir. Yalnızlık yorgunluğu, yorgunluk yalnızlığı büyütür.",
            "Bu deneyimi ahlaki tembellik diye damgalamak zararlıdır. Uzun süren çökkünlük, işlev kaybı, uyku veya iştah değişikliği profesyonel değerlendirme isteyebilir. Felsefi kavram tanı koymaz.",
            "Ben yorgunluğu başarısızlık duygusuyla birleştiğinde kişi sistemin beklentisini kendi değeri sanır. 'Yapamadım' kolayca 'Değersizim'e dönüşür.",
            "İlk küçük ayrım önemlidir: Kapasitem azaldı; insanlık değerim değil. Dinlenme ve yardım bu ayrımı yeniden kurabilir.",
        ], "ÜÇÜNCÜ KISIM · YORGUNLUĞUN İKİ YÜZÜ", art="isolated-tiredness", caption="Ben yorgunluğu insanı kendi başarısızlık aynasına kapatır; azalan kapasite insanlık değerinin azalması değildir."),
        entry("Biz yorgunluğu", [
            "Han başka bir yorgunluk ihtimali de görür. Birlikte ağır iş yapmış insanların akşam sessizce oturması gibi, benlik duvarlarını yumuşatan ortak yorgunluk. Bu yorgunluk insanları ayırmak yerine yan yana getirebilir.",
            "Uzun yürüyüşten sonra arkadaşlarla konuşmadan manzaraya bakmak buna benzer. Kimse kendini kanıtlamaz. Yorgunluk rekabeti kısa süreliğine susturur ve ortak kırılganlığı görünür yapar.",
            "Bu fikri aşırı romantikleştirmemek gerekir. Ağır emek, hastalık ve uykusuzluk yalnızca güzel birlik üretmez. Bedeni yıpratan koşulların iyileştirilmesi gerekir.",
            "Biz yorgunluğunun değeri, performans öznesinin 'Ben yaptım' duvarını gevşetmesidir. İnsan başkasının temposunu fark eder, sessizliği paylaşır.",
            "Belki dinlenmenin toplumsal hali budur: Herkesin ayrı ayrı kendini tamir ettiği odalar değil, kimsenin işe yararlığını kanıtlamadığı ortak zaman.",
        ], "ÜÇÜNCÜ KISIM · YORGUNLUĞUN İKİ YÜZÜ", art="shared-tiredness", caption="Biz yorgunluğu rekabeti susturup insanların kanıt sunmadan aynı sessizlik ve kırılganlıkta yan yana kalmasına izin verir."),
        entry("Bildirimlerle parçalanan gün", [
            "Han'ın kitabı akıllı telefon çağının başlarında yazıldı; bugün tezi daha görünür hissedilebilir. İş mesajı, haber, aile grubu, alışveriş uyarısı ve beğeni aynı ekranda sıraya girer. Her biri küçük çağrı, toplamı kesintisiz nöbettir.",
            "Telefon tek başına düşman değildir. Acil durumda yardım, uzaktaki yakınla temas, eğitim ve erişilebilirlik sağlar. Sorun cihazın varlığı değil, ekonomik tasarımın dikkati sürekli geri çağırmasıdır.",
            "Bildirim kapatmak bazı kişiler için yararlı olabilir; işverenin anında cevap beklentisi sürüyorsa bireysel ayar yetmez. Dikkat sorunu aynı zamanda çalışma kültürü sorunudur.",
            "Gün boyunca yüz küçük kesinti, akşam 'Hiçbir şey yapmadım ama çok yoruldum' hissi bırakabilir. Yorgunluk yalnız iş miktarından değil, tekrar tekrar yön değiştirmekten gelir.",
            "Ekranı suçlamak yerine çağrının sahibini sorun: Bu bildirim kimin çıkarına, hangi aciliyeti gerçek, hangisini sessize alma hakkım var?",
        ], "ÜÇÜNCÜ KISIM · YORGUNLUĞUN İKİ YÜZÜ", art="notification-storm", caption="Bildirim fırtınası tek tek küçük ama toplamda sürekli nöbet yaratır; dikkat ayarı kadar cevap beklentisi de değişmelidir."),
        entry("Bedenin kırmızı ışıkları", [
            "Performans dili bedeni aşılması gereken engel gibi görebilir. Kahveyle uykuyu, ağrı kesiciyle ağrıyı, motivasyon sözüyle tükenmeyi bastırırız. Beden ise gösterge panelindeki kırmızı ışıkları yeniden yakar.",
            "Her yorgunluk toplumsal değildir. Kansızlık, tiroit sorunları, uyku bozuklukları, enfeksiyon, ilaçlar ve birçok sağlık durumu benzer belirti verebilir. Uzun süren veya ağır yorgunluk değerlendirilmelidir.",
            "Bedeni dinlemek her sinyali felaket saymak da değildir. Düzen, süre ve işlev değişimine bakılır. Bir yoğun günün yorgunluğu ile haftalarca yataktan çıkamama aynı değildir.",
            "Han'ın felsefesi bedenin itirazını anlamlandırabilir; doktor muayenesinin yerini tutmaz. Toplumsal neden ile biyolojik neden çoğu zaman birbirini dışlamaz.",
            "Kırmızı ışığı bantla kapatmak arabayı tamir etmez. Dinlenme, tıbbi bakım ve çalışma koşulu değişikliği farklı onarım yolları olabilir.",
        ], "ÜÇÜNCÜ KISIM · YORGUNLUĞUN İKİ YÜZÜ", art="body-dashboard", caption="Bedenin kırmızı ışıkları yalnız irade eksikliği değildir; dinlenme, tıbbi değerlendirme ve koşul değişikliği ayrı ayrı gerekebilir."),
        entry("Tükenmişlik yalnız bireyin projesi mi?", [
            "Kurumsal eğitimler bazen çalışana nefes egzersizi öğretirken aşırı iş yükünü aynı bırakır. Birey daha iyi dayanacak şekilde ayarlanır, yangının kaynağına dokunulmaz. Han'ın eleştirisi bu çelişkiyi görünür kılar.",
            "İş tasarımı, personel sayısı, vardiya, ücret, söz hakkı ve yöneticinin davranışı tükenmişliği etkiler. Çözüm yalnız kişisel dayanıklılık değildir. Dinlenme hakkı ve makul yük kurumsal sorumluluktur.",
            "Evdeki ücretsiz bakım emeği de hesaba katılmalıdır. İşten çıkan kişi ikinci vardiyada çocuk, yaşlı ve ev işleri taşıyorsa 'boş zaman' kağıt üzerinde vardır. Yorgunluk toplumsal cinsiyet ve sınıfa eşit dağılmaz.",
            "Dayanışma bireyin suçunu azaltır. Çalışanlar ortak sorunu konuştuğunda herkes kendi yetersizliği sandığı şeyin düzenli bir iş tasarımı sonucu olduğunu görebilir.",
            "Kolektif çözüm kişinin öz bakımını gereksiz yapmaz. İki düzey birbirini tamamlar: İnsan yardım alır, kurum da zarar üreten koşulu değiştirir.",
        ], "DÖRDÜNCÜ KISIM · SINIRLAR VE ÇIKIŞLAR", art="collective-workplace", caption="Tükenmişlik yalnız nefes tekniğiyle çözülmez; iş yükü, ücret, bakım emeği ve söz hakkı ortak biçimde değişmelidir."),
        entry("Dinlenmeyi performanstan kurtarmak", [
            "Uyku uygulamasında yüksek puan almak, tatilde bütün görülecek yerleri bitirmek ve meditasyonda seri korumak dinlenmeyi yeni başarı alanına çevirebilir. Kişi dururken bile kendini ölçer.",
            "Gerçek dinlenme her zaman faydalı çıktı üretmek zorunda değildir. Ertesi gün daha çok çalışmak için değil, yaşamın kendisi için boş zaman olabilir. Amaçsız sohbet, yavaş yemek veya pencereden bakmak meşru hale gelir.",
            "Bu fikir ayrıcalık sorusunu taşır. İki işte çalışan, bakım veren veya güvensiz evde yaşayan kişinin boşluğu sınırlıdır. Dinlenme yalnız kişisel seçim değil, zaman ve gelir adaleti meselesidir.",
            "Dinlenme bazen etkin de olabilir: bahçeyle uğraşmak, dans etmek, arkadaş görmek. Ölçü hareketsizlik değil, faaliyetin performans borcu üretip üretmemesidir.",
            "Boş sandığımız zaman, benliğin işe yararlılık belgesi sunmadan var olabildiği alandır. Han'ın kitabının en sakin çıkışı burada bulunur.",
        ], "DÖRDÜNCÜ KISIM · SINIRLAR VE ÇIKIŞLAR", art="unmeasured-rest", caption="Dinlenme yeni puan tablosu değil; insanın fayda ve gelişim belgesi sunmadan var olabildiği ölçülmeyen zaman olabilir."),
        entry("Yavaşlık tek başına çözüm mü?", [
            "Yavaşlamak bazı insanlara dikkat ve iyileşme alanı açar. Fakat güvencesiz çalışan kişi yalnız kendi hızını seçemeyebilir. Sorunu yaşam tarzına indirgemek, iktidar ve para ilişkisini gizler.",
            "Han'ın anlatısı bazen bütün toplumu tek performans öznesi gibi resmeder. Oysa işsiz kişinin, fabrika işçisinin, göçmenin, engelli bireyin ve üst düzey yöneticinin baskıları farklıdır. Herkes kendini aynı biçimde sömürmez.",
            "Ruhsal durumları çağın metaforu yapmak da bireyin özgül acısını azaltabilir. Depresyon düşünsel bir simge değil, ciddi ve farklı nedenleri olan bir sağlık durumudur. ADHD de yalnız dikkat çağının ürünü diye açıklanamaz.",
            "Yine de Han'ın teşhisi önemli bir kör noktayı yakalar: Özgürlük dili baskının aracı olabilir ve insan kendini sınırsız proje gibi tüketebilir. Eleştiri, tezi atmak yerine sınırını çizer.",
            "Denge terazisinin bir kefesinde kişisel dikkat ve sınır, diğerinde gelir, kurum, bakım ve sağlık vardır. Çıkış iki kefeyi birlikte gerektirir.",
        ], "DÖRDÜNCÜ KISIM · SINIRLAR VE ÇIKIŞLAR", art="balanced-causes", caption="Yorgunluğu anlamak için kişisel alışkanlık ile sağlık, sınıf, bakım emeği ve kurum koşullarını aynı terazide tutmak gerekir."),
        entry("Küçük ama gerçek üç deney", [
            "Birincisi durma ölçütü koymaktır. Bir iş başlamadan 'Bugün hangi noktada yeterli sayacağım?' diye yazın. Bitmeyen hedefin sınırını görünür yaparsınız.",
            "İkincisi dikkat adası kurmaktır. Kısa bir süre tek iş, tek konuşma veya amaçsız yürüyüş seçin. Başarı süresinde değil, kesintiyi fark edip geri dönebilmededir.",
            "Üçüncüsü bireysel sandığınız yorgunluğu paylaşmaktır. Güvendiğiniz insanlarla yük ve beklenti hakkında konuşun. Ortak sorun varsa ortak değişiklik arayın. Uzun süren ağır belirtilerde profesyonel destek alın.",
        ], "SONUÇ"),
        entry("Bir dakikalık harita", [
            "Han'a göre disiplin toplumunun 'Yapmalısın' emri, performans toplumunda 'Yapabilirsin' baskısına dönüşür. İnsan kendi patronu ve işçisi olur; sınırsız hedef, çoklu görev ve sürekli bağlantı dikkati tüketir.",
            "Derin can sıkıntısı ve bakmayı öğrenmek, tepki ile düşünce arasına alan koyar. Ben yorgunluğu yalnızlaştırır; paylaşılan yorgunluk rekabeti gevşetip ortak kırılganlığı görünür yapabilir.",
            "Bu felsefi teşhis tıbbi açıklama değildir. Tükenmişliği anlamak için beden, ruh sağlığı, ücret, iş yükü, bakım emeği ve toplumsal eşitsizlik birlikte düşünülmelidir.",
        ], "SONUÇ"),
        entry("Akılda kalacak beş görüntü", [
            "Gülümseyen emir: Yapabilirsin bazen zorunluluktur. Aynadaki patron: Kişi kendini denetler. Alarm kuşu: Çoklu görev derinliği parçalar. Boş kuyu: Can sıkıntısı yeni düşünceye alan açar. Ölçüsüz bank: Dinlenme puan üretmeden var olmaktır.",
            "Bu görüntüler yorgun bir günde kendinizi suçlamak yerine sorunu ayırmanıza yardım eder. Gerçek aciliyet ne? Bu hedef kimin? Beden ne söylüyor? Hangi yük kişisel, hangisi ortak değişiklik istiyor?",
            "Han'ın kitabı tembelliği övmez. Yaşamın yalnız üretimden ibaret olmadığını ve insanın sürekli daha fazlasını yapma gücüyle değil, gerektiğinde durabilme özgürlüğüyle de ölçüldüğünü hatırlatır.",
        ], "SONUÇ"),
    ],
})


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for source in BOOKS:
        summary = assemble(source)
        target = OUT / f"{summary['bookNo']}.json"
        target.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{target.relative_to(ROOT)}: {len(summary['chapters'])} chapters, {len(summary['chapterArtworks'])} artworks")


if __name__ == "__main__":
    main()
