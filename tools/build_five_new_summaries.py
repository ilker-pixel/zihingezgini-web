#!/usr/bin/env python3
"""Build five new long-form, illustrated summary JSON files.

The prose lives here as an auditable source. Running the script performs the
mechanical JSON assembly; it does not invent or fetch text at build time.
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
    return {
        "title": title,
        "paragraphs": paragraphs,
        "section": section,
        "art": art,
        "caption": caption,
    }


def assemble(book: dict) -> dict:
    chapters = []
    artworks = {}
    artwork_index = 0
    for index, raw in enumerate(book.pop("entries"), 1):
        chapter_id = f"durak-{index:02d}-{slugify(raw['title'])}"
        chapter = {
            "id": chapter_id,
            "section": raw["section"],
            "title": raw["title"],
            "paragraphs": raw["paragraphs"],
        }
        chapters.append(chapter)
        # One 4×4 production sheet per book: keep exactly sixteen chapter images.
        if raw.get("art") and artwork_index < 16:
            artwork_index += 1
            image = f"/images/summary-art-{book['bookNo']}-chapter-{artwork_index:02d}-{raw['art']}-v1.webp"
            artworks[chapter_id] = {"image": image, "imageCaption": raw["caption"]}

    result = dict(book)
    result["chapters"] = chapters
    result["chapterArtworks"] = artworks
    return result


BOOKS: list[dict] = []


BOOKS.append({
    "bookNo": 31,
    "title": "Niçin Uyuruz?",
    "author": "Matthew Walker",
    "subtitle": "Uykunun görünmez gece vardiyasını, rüyaları ve modern hayatın uykuya açtığı savaşı gündelik örneklerle anlatan sade ve eleştirel rehber.",
    "coverImage": "/images/optimized/summary-art-31-nicin-uyuruz-v2-960.webp",
    "coverStyle": "artwork",
    "pdfUrl": "/data/pdfs/31-nicin-uyuruz-ozeti.pdf",
    "pdfLabel": "25–50 sayfalık PDF'yi indir",
    "longForm": True,
    "chapterArtStyle": "monochrome-engraving",
    "chapterArtColor": "#355A78",
    "meta": {
        "originalTitle": "Why We Sleep: Unlocking the Power of Sleep and Dreams",
        "compiler": "Zihin Gezgini · Yapay zekâ destekli çalışma",
        "date": "Temmuz 2026",
        "language": "Türkçe",
    },
    "intro": "Uyumak, günün fişini çekmek değildir. Beyin ve beden gece boyunca sırayla temizlik yapar, anıları düzenler, duyguların sesini kısar ve ertesi günün ayarlarını hazırlar. Matthew Walker'ın kitabı bu görünmez vardiyayı büyük bir heyecanla anlatır. Bu rehber kitabın dört parçalı yolunu koruyor; fakat korkutucu oranları ve kesin nedensellik iddialarını bugünkü kanıtlarla karıştırmıyor. Amaç, saati takıntıyla izlemek değil, uykunun neden ciddiye alınması gereken canlı bir süreç olduğunu anlamaktır.",
    "sources": [
        {"id": 1, "title": "Why We Sleep – resmî yayınevi sayfası ve bölüm yapısı", "url": "https://www.simonandschuster.com/books/Why-We-Sleep/Matthew-Walker/9781501144325"},
        {"id": 2, "title": "NHLBI – uyku evreleri", "url": "https://www.nhlbi.nih.gov/health/sleep/stages-of-sleep"},
        {"id": 3, "title": "AASM ve SRS – yetişkinler için uyku süresi uzlaşı metni", "url": "https://aasm.org/seven-or-more-hours-of-sleep-per-night-a-health-necessity-for-adults"},
        {"id": 4, "title": "NICHD – uykuda ne olur?", "url": "https://www.nichd.nih.gov/health/topics/sleep/conditioninfo/Pages/what-happens.aspx"},
        {"id": 5, "title": "NINDS – Understanding Sleep", "url": "https://www.ninds.nih.gov/sites/default/files/2025-05/understanding-sleep.pdf"},
        {"id": 6, "title": "Why We Sleep üzerine ayrıntılı eleştirel inceleme", "url": "https://guzey.com/books/why-we-sleep/"},
    ],
    "entries": [
        entry("Bu kitap nasıl okunmalı?", [
            "Walker uykuyu, sağlığın kenarında duran küçük bir alışkanlık olmaktan çıkarıp hayatın ortasına getirir. Kitabın gücü budur. Okur bir gecenin içinde yalnız dinlenme değil, farklı evreleri ve görevleri olan canlı bir düzen görmeye başlar.",
            "Fakat popüler bilimde güçlü benzetme ile kesin kanıt aynı şey değildir. Kitaptaki bazı sayılar, grafik kullanımları ve tek bir araştırmadan çıkarılan büyük hükümler eleştirilmiştir. Bu özet ana mekanizmaları anlatırken ilişki ile neden-sonuç arasındaki farkı koruyacak.",
            "Son hedef kusursuz uyuyan bir makineye dönüşmek değil. Kendi ritmini, gündüz uyanıklığını ve uzun süren sorunlarda profesyonel destek ihtiyacını fark eden daha sakin bir okur olmaktır.",
        ], "BAŞLANGIÇ"),
        entry("Gece kapanan dükkân değil, çalışan şehir", [
            "Saat gece yarısını geçtiğinde sokaklar boşalır. Dışarıdan bakınca şehir durmuş gibidir. Oysa fırınlar hamur hazırlar, temizlik ekipleri çalışır, hastaneler nöbet tutar. Uyuyan beden de böyledir: Bilinçli hareket azalırken içeride farklı ekipler devreye girer.",
            "Kitabın temel itirazı, uykuyu uyanıklığın eksik hâli saymamızadır. Evrim, canlıyı saatlerce çevreye karşı savunmasız bırakıyorsa, bu pahalı davranışın önemli işler yapması beklenir. Uykunun tek bir görevi yoktur; bir İsviçre çakısı gibi birçok işi aynı zaman diliminde yürütür.",
            "Bir telefonu yalnız ekran karardığı için kapalı sanmak ne kadar eksikse, uyuyan beyni de sessiz sanmak o kadar eksiktir. Ölçüm cihazları, gecenin farklı bölümlerinde farklı elektriksel örüntüler gösterir. Nabız, kas tonu, solunum ve hormonlar da aynı kalmaz.",
            "Bu bakış gündelik bir yanılgıyı düzeltir. Yatakta sekiz saat geçirmek ile sekiz saat uyumak aynı değildir. Uykunun süresi kadar düzeni, kesintiye uğrayıp uğramadığı ve kişinin gündüz nasıl hissettiği de önem taşır.",
            "Akılda kalacak görüntü, gece vardiyasındaki şehirdir. Işıklar azalmıştır ama iş bitmemiştir; yalnız görev değişmiştir.",
        ], "BİRİNCİ KISIM · UYKU NEDİR?", art="night-city", caption="Uyku, ışıkları sönmüş bir şehir değil; farklı ekiplerin çalıştığı görünmez bir gece vardiyasıdır."),
        entry("İki saat: Güneş saati ve uyku kumu", [
            "Akşam koltukta gözleri kapanan biri, yatağa geçince neden birden açılabilir? Çünkü uyku isteğini tek bir düğme yönetmez. Walker iki sistemi yan yana koyar: Yaklaşık yirmi dört saatlik iç saat ve uyanık kaldıkça biriken uyku basıncı.",
            "İç saat, ışık başta olmak üzere çevreden ipucu alır. Sabah ışığı bedenin gündüz programını öne çıkarır; akşam karanlığı geceye hazırlanmasına yardım eder. İnsanlar aynı fabrikadan çıkmış saatler değildir. Kimisi erken, kimisi geç saatlerde daha canlıdır; yaş da bu eğilimi değiştirir.",
            "Uyku basıncını kum saatine benzetebiliriz. Sabah üst hazne boştur. Gün ilerledikçe adenosin denen kimyasal habercinin etkisi artar ve kum aşağı dolar. Uyuyunca basınç azalır. Öğleden sonraki kısa çöküş ise yalnız bu kumla değil, iç saatin günlük dalgasıyla da ilgilidir.",
            "İki sistem bazen birbirini çeker, bazen iter. Gece yarısı çok yorulmuş olsak bile parlak ışık ve hareket bizi açık tutabilir. Sabah alarm çaldığında basınç azalmış olsa da iç saat hâlâ gece programında kalmış olabilir.",
            "Bu yüzden uyku yalnız irade meselesi değildir. 'Erken yat' öğüdü, saati sürekli geçe ayarlanmış bir gence veya gece vardiyasında çalışan birine yeterli açıklama sunmaz. Önce hangi saatin kiminle kavga ettiğini görmek gerekir.",
        ], "BİRİNCİ KISIM · UYKU NEDİR?", art="two-clocks", caption="Uykuyu, iç saat ile gün boyunca biriken uyku basıncının birlikte çalışması belirler."),
        entry("Kahvenin yaptığı şey enerji vermek mi?", [
            "Öğleden sonra içilen kahve, bedene yeni enerji dökmez. Daha çok, yorgunluk haberini taşıyan adenosinin bazı alıcılara ulaşmasını geçici olarak engeller. Benzin deposu dolmamıştır; yalnız gösterge panelindeki uyarı ışığının üzeri kapatılmıştır.",
            "Kafeinin etkisi kişiden kişiye değişir ve saatlerce sürebilir. Bir insan akşam kahvesinden sonra kolayca uyuduğunu söyleyebilir; bu, uykunun mimarisinin hiç etkilenmediğini kanıtlamaz. Öte yandan herkes için tek bir kesin yasak saati vermek de doğru değildir.",
            "Melatonin başka bir yanlış anlaşılmanın merkezindedir. Bu hormon bir bayıltma ilacı gibi uyku üretmez; daha çok karanlığın başladığını bildiren gece habercisidir. Uçakla saat dilimi değiştirince yeni yere uyum sağlamada bu işaretin zamanı önem kazanır.",
            "Jet lag, kol saatinin değil beden saatinin geride kalmasıdır. İstanbul'dan New York'a vardığınızda duvardaki saat akşamı gösterirken karaciğeriniz, bağırsaklarınız ve beyniniz başka bir saati yaşamaya devam edebilir. Uyum birkaç gün ister.",
            "Buradaki pratik ders kahveyi şeytan ilan etmek değildir. Fincanın hangi saatte geldiğini, geceyi ne kadar etkilediğini ve ertesi gün yeni kahve ihtiyacına dönüşüp dönüşmediğini fark etmektir.",
        ], "BİRİNCİ KISIM · UYKU NEDİR?", art="coffee-clock", caption="Kafein yorgunluğu yok etmez; bir süreliğine yorgunluk mesajının önüne perde çeker."),
        entry("Gecenin dalgaları: Hafiften derine, derinden rüyaya", [
            "Uyku tek renk bir karanlık değildir. Gece boyunca hızlı göz hareketlerinin görülmediği NREM evreleri ile REM uykusu arasında döneriz. Bir döngü çoğu yetişkinde kabaca seksen ile yüz dakika sürer ve gecede birkaç kez tekrarlanır.",
            "İlk evre, kıyıdan tekneye adım atmak gibidir; kolayca geri döneriz. İkinci evrede uyku belirginleşir. Derin NREM uykusunda beyin dalgaları yavaşlar, uyandırılmak zorlaşır. Sabahın ilk bölümünde bu derin uyku daha çok yer kaplar.",
            "Gecenin ilerleyen kısmında REM dönemleri uzar. Beyin etkin görünür, canlı rüyalar sıklaşır, büyük kasların hareketi baskılanır. Sanki film gösterilirken salonun kapıları kilitlenmiştir; beden rüyanın her hareketini dışarı taşımaktan korunur.",
            "Bir gecenin başını veya sonunu sürekli kesmek aynı sonucu doğurmayabilir. Çok erken kalkmak, sabaha doğru yoğunlaşan REM uykusundan daha fazla çalabilir. Buna rağmen her evreyi tek bir göreve kilitlemek de bilimsel olarak fazla basittir; bellek gibi işlerde birden çok evre birlikte rol oynar.",
            "Gecenin akılda kalacak resmi bir merdiven değil, tekrar tekrar kıyıya vuran dalgadır. Aynı denize gireriz ama her dalga başka bir ritim taşır.",
        ], "BİRİNCİ KISIM · UYKU NEDİR?", art="sleep-waves", caption="Gece, NREM ve REM uykusunun birbirini izlediği birkaç dalgadan oluşur."),
        entry("Yunus yarım beyinle uyurken insan neden yatağa ihtiyaç duyar?", [
            "Hayvanlar uyku konusunda inanılmaz çözümler geliştirmiştir. Yunus gibi bazı deniz memelileri beynin bir yarısını uyuturken öteki yarısıyla yüzmeye ve nefes almaya devam edebilir. Göçmen kuşlar tehlikeli zamanlarda uykuyu küçük parçalara bölebilir.",
            "Bu çeşitlilik, 'doğru uyku biçimi' diye bütün canlılara uygulanacak tek bir şablon olmadığını gösterir. Avcı olmak, av olmak, yiyeceğe ulaşmak, yavru korumak ve beden büyüklüğü uykunun süresini ve biçimini etkileyebilir.",
            "İnsan uykusunun ilginç yanlarından biri, yere yakın güvenli yatakların REM uykusunu artırmış olabileceği fikridir. Ateş, grup hâlinde korunma ve uygun bir uyku yeri, beynin gece programına daha fazla alan açmış olabilir. Bu, ilgi çekici bir evrimsel açıklamadır; geçmişi doğrudan seyredemediğimiz için dikkatle ele alınmalıdır.",
            "Bir zürafa ile yarasayı yalnız kaç saat uyuduklarıyla karşılaştırmak, iki şehri yalnız nüfusuna göre tanımaya benzer. Uykunun nerede, nasıl ve ne kadar parçalı olduğu da önemlidir.",
            "Kitabın bu bölümünden kalan şaşkınlık şudur: Uyku doğada tek tip bir teslimiyet değil, yaşam koşullarına göre şekil değiştiren eski bir çözümdür.",
        ], "BİRİNCİ KISIM · UYKU NEDİR?", art="half-brain-dolphin", caption="Hayvanların uykusu, çevreye ve yaşama biçimine göre şaşırtıcı çözümler geliştirir."),
        entry("Bebekten yaşlılığa değişen gece", [
            "Yeni doğan bir bebeğin uykusu, yetişkinin düzgün gecesine benzemez. Kısa parçalar hâlinde gelir, gün ile gece henüz net ayrılmamıştır. Çocuklukta derin uyku güçlenir; ergenlikte iç saat daha geçe kayar. Sabah çok erken başlayan okul, gencin biyolojisiyle kavga edebilir.",
            "Bu noktada tembellik suçlaması özellikle yanıltıcıdır. Gece geç saatlere kadar açık kalan ergen, yalnız telefon yüzünden değil, saatinin doğal kayması yüzünden de erken uyuyamayabilir. Ekran ve sosyal hayat bu kaymayı büyütebilir ama hikâyenin tamamı değildir.",
            "Yetişkinlikte uyku gereksinimi bir gecede kaybolmaz. Yaş ilerledikçe uyku daha hafif ve parçalı olabilir, erken yatıp erken kalkma eğilimi artabilir. 'Yaşlıların az uykuya ihtiyacı var' cümlesi, uyuma fırsatı ile gerçek ihtiyaç arasındaki farkı örter.",
            "Kırkından sonra birçok insan gece uyanmalarını başarısızlık gibi görür. Oysa kısa uyanmalar tek başına felaket değildir. Asıl soru tekrar uykuya dönüp dönemediği, gündüz uyanıklığın nasıl olduğu ve horlama, nefes durması, huzursuz bacak gibi belirtilerin bulunup bulunmadığıdır.",
            "Hayat boyu değişen uyku, sabit bir sınav puanı değil, yaşa ve koşula göre yeniden ayarlanan bir ev programıdır.",
        ], "BİRİNCİ KISIM · UYKU NEDİR?", art="lifespan-bed", caption="Bebeklikten yaşlılığa uyku süresi, zamanı ve derinliği aynı kalmaz."),
        entry("Beynin gece arşivcisi", [
            "Bir gün içinde onlarca isim, yüz, yol ve hareket öğreniriz. Hepsini aynı çekmeceye atarsak sabah karmaşa çıkar. Uyku, beynin arşivcisi gibi çalışır: Bazı izleri güçlendirir, bazılarını eski bilgilerle bağlar, önemsiz ayrıntıların bir bölümünü geriye iter.",
            "Öğrenmeden önce uyku da önemlidir. Çok uykusuz bir beyin yeni bilgiyi kaydetmekte zorlanabilir. Fotoğraf makinesinin kartı dolu değildir belki; fakat odak sistemi şaşmış ve el titremeye başlamıştır. Derste gözünüz açık olsa bile kayıt kalitesi düşebilir.",
            "Öğrenmeden sonraki uyku, yeni izin daha dayanıklı hâle gelmesine yardım eder. Parmakla bir dizi tuşa basmak, yeni bir kelimeyi hatırlamak veya bir mekânın yolunu öğrenmek aynı tür bellek değildir; farklı uyku özellikleri bu işlere farklı katkılar verebilir.",
            "Walker bu alanı güçlü ve net bir hikâyeyle anlatır. Güncel araştırma ise 'bütün anıları şu evre saklar' gibi tek cümlelik formüllerden kaçınır. NREM, REM, kısa uyanmalar ve önceki öğrenmenin niteliği birlikte düşünülür.",
            "En sade sonuç şudur: Çalışmayı uzatmak için uykuyu kesmek, ertesi gün kullanacağınız kütüphanenin raflarını gece boyunca devirmek olabilir.",
        ], "İKİNCİ KISIM · UYKU NE İŞE YARAR?", art="memory-archive", caption="Uyku, günün dağınık izlerini seçen, bağlayan ve daha kalıcı hâle getiren bir arşivci gibi çalışır."),
        entry("Uykusuz beynin büyüttüğü küçük mesele", [
            "Az uyuduğunuz bir sabah, mutfakta bırakılmış bir bardak normalden büyük bir saygısızlık gibi görünebilir. Sorun bardakta değildir. Uykusuzluk, duygusal alarm sisteminin sesini yükseltirken onu dengeleyen ön bölgelerin çalışmasını zorlaştırabilir.",
            "Bu nedenle yorgun insan yalnız daha huysuz olmaz; yüz ifadelerini, belirsiz mesajları ve riskleri farklı okuyabilir. Patronun kısa e-postası tehdit, eşin sessizliği reddedilme, trafikteki küçük gecikme kişisel saldırı gibi hissedilebilir.",
            "İlginç olan, uykusuzluğun yalnız olumsuz duyguyu artırmamasıdır. Bazı durumlarda ödül arayışı ve düşünmeden hareket etme de güçlenebilir. Gece yarısı gereksiz alışveriş veya ertesi gün pişman olunacak mesaj, yorgun beynin daralan fren mesafesine örnek olabilir.",
            "Bundan 'her kötü kararın nedeni uykudur' sonucu çıkmaz. İnsan davranışı ilişki, para, hastalık ve geçmiş deneyim gibi birçok etken taşır. Uyku, bu orkestradaki güçlü çalgılardan biridir; tek başına bütün müziği çalmaz.",
            "Pratik hafıza kancası şudur: Çok yorgunken çözülmesi gereken büyük konuşmayı mümkünse erteleyin. Mesele değişmeyebilir ama ona bakan beynin ışığı değişir.",
        ], "İKİNCİ KISIM · UYKU NE İŞE YARAR?", art="emotional-alarm", caption="Uykusuzluk küçük olayların duygusal sesini büyütüp kararların fren mesafesini uzatabilir."),
        entry("Bedenin tamir defteri", [
            "Uyku yalnız beynin işi değildir. Bağışıklık sistemi, metabolizma, iştahı etkileyen sinyaller, kan basıncı ve hormon düzeni gece ritmiyle bağlantılıdır. Sürekli kısa veya parçalı uyku, bu sistemlerin uyumunu bozabilen etkenlerden biridir.",
            "Walker kalp hastalığı, diyabet, kilo artışı, enfeksiyon ve kanser gibi başlıkları sert bir dille yan yana getirir. Burada önemli bir ayrım vardır: Kısa uyuyan gruplarda bir hastalığın daha sık görülmesi, tek nedenin uyku olduğunu kendiliğinden kanıtlamaz. Hastalık da uykuyu bozabilir; iş, yoksulluk, stres ve ilaçlar iki tarafı birlikte etkileyebilir.",
            "Yine de laboratuvar deneyleri ve uzun dönemli gözlemler, kronik yetersiz uykunun masum bir alışkanlık olmadığını destekler. Beden, geceyi bedava boşluk saymaz. Düzenli olarak uyku borcu biriktirmek, bakım zamanını sürekli ertelenen bir araca benzer.",
            "Hafta sonu uzun uyumak bir miktar toparlanma sağlayabilir; fakat bütün haftanın etkisini sihirli biçimde silen banka işlemi değildir. Üstelik çok geç kalkmak pazar gecesi iç saati yeniden kaydırabilir.",
            "Bu bölüm korku üretmek için değil, uykuyu beslenme ve hareket kadar temel bir sağlık davranışı olarak görmek için okunmalı. Belirti veya hastalık varsa çözüm yalnız erken yatmak değil, nedeni değerlendirmektir.",
        ], "İKİNCİ KISIM · UYKU NE İŞE YARAR?", art="body-repair", caption="Gece, bağışıklık, metabolizma ve dolaşımın ortak ritim içinde bakım yaptığı bir zaman dilimidir."),
        entry("Mikrouyku: Açık gözlerin kayıp saniyeleri", [
            "Direksiyon başındaki sürücünün gözleri açık olabilir ama beyin birkaç saniyeliğine çevreden kopabilir. Mikrouyku denen bu kısa boşluk, uzun bir yolun en tehlikeli anıdır. Saatte doksan kilometreyle giden araç birkaç saniyede onlarca metreyi sürücüsüz geçer.",
            "Uykusuzluğun sinsi tarafı, kişinin kendi bozulmasını tam ölçememesidir. Birkaç kötü geceden sonra yeni hâline alışır ve 'Ben böyle de çalışıyorum' der. Oysa dikkat testleri tepki süresinin ve hata sayısının kötüleştiğini gösterebilir.",
            "Bir gecelik tam uykusuzluk ile haftalarca her gece biraz az uyumak farklı deneyimlerdir. Kitap, küçük eksiklerin birikebileceğini vurgular. Bu birikim herkes için aynı hızda ve aynı sonuçla ilerlemez; yine de öznel güvenilirlik iyi bir ölçüm değildir.",
            "Kahve, yüksek sesli müzik veya camı açmak kısa süre uyanıklık hissi verebilir. Bunlar uyku ihtiyacını ortadan kaldırmaz. Özellikle araç kullanırken bastırılamayan esneme, şerit kaçırma ve son kilometreleri hatırlamama ciddi uyarılardır.",
            "Akılda kalan cümle şudur: Uykulu beyin, kendi hakemliğini iyi yapamaz. Güvenlik gerektiren işlerde 'kendimi iyi hissediyorum' tek başına yeterli değildir.",
        ], "İKİNCİ KISIM · UYKU NE İŞE YARAR?", art="microsleep-road", caption="Mikrouyku sırasında araç ilerlerken beynin çevreyle bağlantısı birkaç tehlikeli saniye kesilebilir."),
        entry("Rüya sineması neden bu kadar gerçek gelir?", [
            "Rüyada yıllardır görmediğiniz biri mutfağa girebilir, tavan denize dönüşebilir ve siz bunları uzun süre sorgulamayabilirsiniz. REM uykusunda duygusal ve görsel ağlar canlı çalışırken mantıksal denetimin bazı parçaları gündüzdeki kadar baskın değildir.",
            "Rüya yalnız REM'e ait değildir; başka evrelerden uyandırılan insanlar da zihinsel yaşantılar anlatabilir. Ancak canlı, hikâyeli ve tuhaf rüyalar REM dönemlerinde daha sık hatırlanır. Sabahın sonundaki REM uzadığı için alarmı ertelediğiniz dakikalar bazen yoğun bir rüya getirir.",
            "Kasların büyük bölümündeki geçici hareketsizlik, rüyayı bedende oynamamızı önler. Bu kilit bazı bozukluklarda tam çalışmadığında kişi rüyadaki hareketleri dışarı taşıyabilir. Böyle bir durum eğlenceli bir tuhaflık değil, değerlendirilmesi gereken bir belirti olabilir.",
            "Rüyaların tek ve kesin bir anlam sözlüğü yoktur. Diş düşmesi herkes için aynı gizli mesajı taşımaz. Rüya, yakın yaşantılardan, duygulardan ve eski anılardan parçaları alışılmadık biçimde birleştirebilir.",
            "Rüyayı gece sineması diye hatırlayın; yönetmen tanıdık malzemeyi kullanır ama kurgu kurallarına uymak zorunda değildir.",
        ], "ÜÇÜNCÜ KISIM · RÜYALAR", art="dream-cinema", caption="Rüya sineması, tanıdık insanları ve mekânları gündüz mantığına uymayan bir kurguya dönüştürebilir."),
        entry("Gece terapisti mi, duygu karıştırıcısı mı?", [
            "Walker REM uykusunu, duygusal anıyı olayın keskin kimyasından ayıran bir gece terapistine benzetir. Zor olay kalır ama ertesi gün aynı bedensel alarmı yaratmayabilir. Bu düşünce etkileyicidir ve bazı araştırmalarla uyumludur; bütün travmalar için otomatik tedavi gibi anlaşılmamalıdır.",
            "Kötü bir günün ardından 'bir uyuyayım, geçer' dememizin biyolojik bir karşılığı olabilir. Uyku, anıyı başka anılarla yeniden ilişkilendirir ve duygusal tepkinin ayarına katkı sağlar. Fakat kabus, depresyon veya travma sonrası stres bozukluğunda gece tam tersine acıyı tekrar eden bir alana dönüşebilir.",
            "Rüyaların yaratıcı tarafı da bu gevşek bağlardan doğabilir. Beyin, gündüz yan yana getirmediğimiz fikirleri aynı sahneye taşır. Bir müzisyenin melodi, bir bilim insanının benzetme, sıradan bir insanın çözüm bulması mümkündür; fakat her parlak fikir rüyadan gelmez.",
            "En iyi kullanım, yastığın yanına mucize bekleyerek oturmak değil, zor bir probleme çalıştıktan sonra uykuya yer açmaktır. Sabah gelen bağlantı, gece boyunca görünmez bir yeniden düzenlemenin ürünü olabilir.",
            "Bu bölümün dengeli özeti: Uyku duygu ve yaratıcılığa yardım eden bir ortamdır; tek başına psikoterapi veya ilham makinesi değildir.",
        ], "ÜÇÜNCÜ KISIM · RÜYALAR", art="dream-therapy", caption="Uyku duygusal anıları yeniden işlerken uzak fikirler arasında beklenmedik köprüler kurabilir."),
        entry("Gece gelenler: Uykusuzluk, apne ve başka bozukluklar", [
            "Uykusuzluk yalnız 'uyuyamıyorum' cümlesi değildir. Uykuya dalma, uykuyu sürdürme veya çok erken uyanma sorunu gündüz yaşamını etkiliyorsa ve uzun sürüyorsa değerlendirme gerekir. Yatakta geçirilen tek kötü gece tanı değildir.",
            "Uyku apnesinde üst hava yolu tekrar tekrar kapanabilir. Kişi saatlerce yatakta kalsa da uyku bölünür; yüksek horlama, nefes durmasının fark edilmesi, sabah baş ağrısı ve gündüz uyuklama görülebilir. Horlama her zaman apne demek değildir ama nefes kesilmesi önemlidir.",
            "Narkolepsi, uyku-uyanıklık sınırlarının beklenmedik biçimde karıştığı nörolojik bir durumdur. Bazı kişilerde güçlü duyguyla kas gücü aniden azalabilir. Bu tabloyu 'tembellik' diye yorumlamak, biyolojik bir hastalığa ahlak notu vermektir.",
            "Uyurgezerlik, gece terörü, huzursuz bacak ve REM davranış bozukluğu gibi sorunlar farklı evrelerden ve mekanizmalardan doğar. İnternetteki tek bir belirti listesiyle kendi kendine tanı koymak bu yüzden yanıltıcıdır.",
            "Kitabın en yararlı mesajlarından biri, kötü uykunun karakter kusuru olmadığıdır. Süren sorun, uygun değerlendirme ve tedaviyle ele alınabilecek bir sağlık meselesidir.",
        ], "DÖRDÜNCÜ KISIM · MODERN HAYAT", art="sleep-clinic", caption="Aynı 'kötü uyku' şikâyetinin arkasında birbirinden farklı ve değerlendirilebilir bozukluklar bulunabilir."),
        entry("Ekran, alkol, sıcak oda: Uykuyu kim sabote ediyor?", [
            "Modern gecede güneş battıktan sonra da gündüzü sürdürüyoruz. Parlak ışık iç saati geciktirebilir; ekrandaki içerik zihni uyanık tutabilir. Sorun yalnız mavi ışık değildir. Mesajlaşma, haber, oyun ve 'bir bölüm daha' kararı da yatağın saatini yer.",
            "Alkol hızlı uykuya dalmayı kolaylaştırıyor gibi görünebilir. Fakat bu doğal uyku ile aynı şey değildir; geceyi parçalayabilir, horlamayı ve solunum sorunlarını artırabilir, REM düzenini değiştirebilir. Bayılmaya yakın gevşeme, kaliteli uyku garantisi değildir.",
            "Beden uyku öncesi çekirdek sıcaklığını düşürmeye hazırlanır. Bu yüzden çok sıcak oda zorlayıcı olabilir. Ilık duşun yardımcı olabilmesi ilk bakışta çelişkili görünür; deriye giden kan ve sonrasındaki ısı kaybı bedenin soğumasını destekleyebilir.",
            "Gürültüye 'alıştığını' söyleyen biri her sesi hatırlamayabilir. Yine de beden kısa uyanmalar ve stres tepkileri gösterebilir. Öte yandan mutlak sessizlik arayışı da kaygıyı büyütebilir. Hedef laboratuvar değil, sürdürülebilir bir ortamdır.",
            "Uykuyu sabote eden tek suçlu telefon değildir. Geç mesai, bakım sorumluluğu, vardiya, ağrı, kaygı ve ev koşulları kişisel iradenin çok ötesinde belirleyicidir.",
        ], "DÖRDÜNCÜ KISIM · MODERN HAYAT", art="modern-saboteurs", caption="Parlak ekran, geç saat, alkol ve sıcak ortam aynı gece düzeninin farklı yerlerini bozabilir."),
        entry("Uyku ilacı ile uyku terapisi aynı kapı değil", [
            "Bir uyku ilacı kişiyi sersemletebilir veya uykuya geçişi kolaylaştırabilir; ancak oluşturduğu durum doğal uykunun bütün özelliklerini birebir kopyalamaz. İlaçların yararı, riski ve süresi kişiye göre değerlendirilmelidir. Kitaptan alınacak sonuç reçeteyi kendi başına bırakmak değildir.",
            "Kronik uykusuzluk için en güçlü yaklaşımlardan biri bilişsel davranışçı terapidir. Kişi yalnız 'rahatla' öğüdü almaz. Yatak ile uyanıklık arasındaki yanlış bağı çözmek, uyku fırsatını düzenlemek, felaket düşüncelerini ele almak ve sürdürülebilir alışkanlık kurmak üzerinde çalışır.",
            "Uykusuz insan genellikle yatağa daha erken girip daha uzun kalır. İyi niyetli bu hareket, yatağı saatler süren mücadele alanına çevirebilir. Terapi bazen tam tersine yatağı yeniden yalnız uyku ile eşleştirmeye çalışır.",
            "Takip cihazları yararlı ipuçları verebilir ama tıbbi uyku laboratuvarı değildir. Her sabah uygulamadaki yüzdeye bakıp endişelenmek, 'kusursuz uyku' takıntısı yaratabilir ve uykuyu daha da zorlaştırabilir.",
            "Buradaki ölçü basittir: Araç, daha iyi yaşamanıza yardım ediyor mu; yoksa bütün gün uykunuzu düşünmenize mi neden oluyor? Tedavi de teknoloji de insanın hizmetinde kalmalıdır.",
        ], "DÖRDÜNCÜ KISIM · MODERN HAYAT", art="therapy-door", caption="Uyku ilacı, davranışçı terapi ve takip cihazı aynı amaç için kullanılan ama aynı işi yapmayan araçlardır."),
        entry("Okul, hastane ve işyeri neden uykuyu kişisel sorun sayamaz?", [
            "Bir doktor yirmi dört saatlik nöbetin sonunda hata yaptığında yalnız iradesini sorgulamak eksiktir. Sistem, insan beyninin sınırlarını görmezden gelmiş olabilir. Aynı durum gece vardiyasındaki işçi, sabah karanlığında okula giden genç ve uzun yol şoförü için de geçerlidir.",
            "Walker uyku kaybını toplumsal bir tasarım sorunu olarak görür. Erken okul saatleri ergen saatine ters düşebilir. Hastanelerde aşırı uzun nöbetler hasta güvenliğini etkileyebilir. İşyerinde geç saate kadar çevrimiçi kalmak bağlılık göstergesi sayılabilir.",
            "Bireye 'telefonu bırak' demek ucuzdur; vardiya çizelgesini, ulaşımı, çocuk bakımını ve çalışma kültürünü değiştirmek zordur. Oysa uyku eşitsizliği de vardır. Sessiz, serin ve güvenli odası olmayan insanın biyoloji dersiyle çözülmeyecek sorunları bulunur.",
            "Toplumsal çözüm tek bir büyük yasa değildir. Daha akıllı nöbet düzeni, dinlenme araları, esnek başlangıç saati, ışık tasarımı ve uykulu araç kullanımına karşı eğitim birlikte çalışabilir.",
            "Uykuyu kamusal mesele saymak, herkesin aynı saatte yatması demek değildir. İnsan bedeninin sınırlarını okulun ve işin tasarımına dâhil etmek demektir.",
        ], "DÖRDÜNCÜ KISIM · MODERN HAYAT", art="society-clock", caption="Okul ve çalışma saatleri biyolojik sınırları yok saydığında uyku kaybı kişisel olmaktan çıkar."),
        entry("Kitabın tartışmalı yanı: Korku ne zaman kanıtın önüne geçer?", [
            "Niçin Uyuruz? okuru sarsmak için güçlü cümleler kullanır. Bu anlatım, uykuyu önemsemeyen bir kültürde etkili olmuştur. Fakat bazı eleştirmenler kitapta hatalı aktarılan sayılar, seçici grafikler ve gözlemsel ilişkilerden fazla kesin sonuçlar çıkarıldığını göstermiştir.",
            "Örneğin kısa uyku ile bir hastalık arasında ilişki bulmak önemlidir ama 'az uyku bu hastalığı kesin yaratır' demek için yeterli olmayabilir. Yaş, çalışma düzeni, mevcut hastalık ve ekonomik koşullar hem uykuyu hem sonucu etkileyebilir.",
            "Tartışmayı iki uçtan kurtarmak gerekir. Kitapta hata bulunması uykunun önemsiz olduğunu kanıtlamaz. Uykunun önemli olması da kitaptaki her oranı doğru yapmaz. Bilimsel düşünme tam burada başlar: Ana fikri korurken ayrıntıyı sınamak.",
            "Sağlıklı yetişkinler için düzenli olarak en az yedi saat uyku önerisi uzman uzlaşılarında yer alır; bireysel gereksinim değişebilir. Tek bir sihirli sayı yerine gündüz uyanıklığı, düzen, sağlık durumu ve yaşam evresi birlikte değerlendirilmelidir.",
            "Kitabın en iyi mirası korkuyla yatağa kaçmak değil, uykuyu ciddiye almaktır. En iyi düzeltmesi ise bunu kesinlik gösterisi yapmadan söyleyebilmektir.",
        ], "DÖRDÜNCÜ KISIM · MODERN HAYAT", art="evidence-balance", caption="Uykunun önemini kabul etmek ile kitaptaki her güçlü iddiayı sorgusuz onaylamak aynı şey değildir."),
        entry("On iki maddelik reçete yerine yaşayan bir akşam", [
            "Saat 21.30. Evdeki ışık biraz azalıyor. Telefon tamamen yasaklanmıyor ama yatak odasından uzaklaşıyor. Ertesi sabah aynı saate yakın kalkılacak. Kahvenin son fincanı öğleden sonra içilmiş. Bu sahne, mükemmel bir uyku töreninden daha gerçekçidir.",
            "Düzenli kalkış saati iç saate güçlü bir çıpa verir. Sabah gün ışığı, gündüz hareket, akşam daha düşük ışık ve serin bir oda bu çıpayı destekler. Yatmadan hemen önce büyük öğün, yoğun alkol ve uyarıcı içerik bazı insanlarda işi zorlaştırır.",
            "Uyku gelmiyorsa saati sürekli kontrol etmek kaygıyı büyütür. Uzun süre uyanık kalındığında loş ışıkta sakin bir etkinliğe geçip uykululuk dönünce yatağa gelmek, yatağı mücadele alanı olmaktan çıkarabilir.",
            "Bu öneriler tıbbi tanı veya kişiye özel tedavi değildir. Haftalarca süren uykusuzluk, şiddetli gündüz uykululuğu, nefes kesilmesi, olağandışı hareketler veya güvenlik riski varsa uzman değerlendirmesi gerekir.",
            "Başarı, her gece aynı uygulama puanını almak değildir. Daha dinç uyanmak, gün içinde daha güvenli ve sakin olmak, kötü geceden sonra paniğe kapılmadan ritme geri dönebilmektir.",
        ], "SONUÇ", art="calm-evening", caption="İyi uyku, katı bir tören değil; ışık, zaman, hareket ve sakinlikle kurulan sürdürülebilir bir akşam ritmidir."),
        entry("Bir dakikalık harita", [
            "Uyku, pasif kapanma değil etkin bir gece programıdır. İç saat ile uyku basıncı ne zaman uyuyacağımızı birlikte belirler. NREM ve REM evreleri gece boyunca sırayla gelir; bellek, duygu, beden sağlığı ve dikkat bu düzenle ilişkilidir.",
            "Rüyalar beynin tuhaf gece kurgularıdır; yaratıcılık ve duygusal işlemeye katkı sağlayabilir ama gizli anlam sözlüğü değildir. Uykusuzluk, apne ve başka bozukluklar aynı şikâyetin farklı nedenleri olabilir. Modern hayatın ışığı ve çalışma saatleri kişisel tercihten fazlasını etkiler.",
            "Kitabı okurken iki cümleyi birlikte tutun: Uykuyu küçümsemeyin. Korkutucu bir sayı gördüğünüzde kanıtın ne söylediğini ayrıca sorun.",
        ], "SONUÇ"),
        entry("Kırkından sonra akılda kalacak beş görüntü", [
            "Gece vardiyasındaki şehir: Beden uyurken çalışır. İki saat: İç ritim ile uyku basıncı pazarlık eder. Dalgalı deniz: NREM ve REM gece boyunca tekrarlar. Beynin arşivcisi: Anılar uyku içinde düzenlenir. Açık gözlü sürücüsüz araç: Mikrouyku güveni bir anda boşa çıkarabilir.",
            "Bu beş görüntü, onlarca terimi ezberlemekten daha kullanışlıdır. Bir sonraki kötü gecede kendinizi suçlamak yerine hangi saatin, hangi ortamın veya hangi sağlık sorununun devrede olabileceğini düşünürsünüz.",
            "En önemlisi, uyku hayatın rakibi değildir. Ertesi gün daha dikkatli, daha dengeli ve daha meraklı yaşayabilmek için gecenin yaptığı görünmez hazırlıktır.",
        ], "SONUÇ"),
    ],
})


BOOKS.append({
    "bookNo": 88,
    "title": "İnsanın Anlam Arayışı",
    "author": "Viktor E. Frankl",
    "subtitle": "İnsanın elinden çok şey alındığında bile anlam, sorumluluk ve ilişkiyle kurduğu iç yönü anlatan; sınırlarını da saklamayan sade rehber.",
    "coverImage": "/images/optimized/summary-art-88-insanin-anlam-arayisi-v2-960.webp",
    "coverStyle": "artwork",
    "pdfUrl": "/data/pdfs/88-insanin-anlam-arayisi-ozeti.pdf",
    "pdfLabel": "25–50 sayfalık PDF'yi indir",
    "longForm": True,
    "chapterArtStyle": "monochrome-engraving",
    "chapterArtColor": "#754B4B",
    "meta": {
        "originalTitle": "Man's Search for Meaning",
        "compiler": "Zihin Gezgini · Yapay zekâ destekli çalışma",
        "date": "Temmuz 2026",
        "language": "Türkçe",
    },
    "intro": "Bu kitap iki ayrı kapı açar. İlkinde Viktor Frankl, Nazi kamp sisteminde yaşadığı açlığı, korkuyu, kaybı ve insanın iç dünyasında oluşan değişimleri anlatır. İkincisinde, daha önce geliştirmeye başladığı logoterapi yaklaşımını açıklar: İnsanın temel yönelimlerinden biri anlam bulmaktır. Bu rehber anlatının gücünü korurken çok önemli bir sınır koyar. Hayatta kalmayı yalnız tutuma bağlamaz, kurbanı başına gelenden sorumlu tutmaz ve tek bir tanıklığı Holokost'un tamamı saymaz. Anlam, acıyı haklı çıkaran bir süs değil; kaçınılamayan acının içinde insanın yönünü kaybetmemesine yardım edebilen bir ilişkidir.",
    "sources": [
        {"id": 1, "title": "Beacon Press – Man's Search for Meaning", "url": "https://www.beacon.org/Mans-Search-for-Meaning-P2354.aspx"},
        {"id": 2, "title": "Beacon Press öğretmen rehberi", "url": "https://www.beacon.org/Assets/ClientPages/MansSearchForMeaningtg.aspx"},
        {"id": 3, "title": "Viktor Frankl Institute Vienna", "url": "https://www.viktorfrankl.org/"},
        {"id": 4, "title": "British Journal of Psychiatry – kitap değerlendirmesi", "url": "https://www.cambridge.org/core/journals/the-british-journal-of-psychiatry/article/mans-search-for-meaning-by-victor-frankl/92B65A57083177ADDC20E4B3108B99BD"},
        {"id": 5, "title": "Holocaust and Genocide Studies – eleştirel inceleme", "url": "https://academic.oup.com/hgs/article-abstract/17/1/89/636274"},
        {"id": 6, "title": "Frontiers in Psychology – kitap değerlendirmesi", "url": "https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2016.01493/full"},
    ],
    "entries": [
        entry("Önce saygı: Bu kitap ne değildir?", [
            "İnsanın Anlam Arayışı bir 'güçlü düşün, her şeyi yen' kitabı değildir. Tarihsel bir kitlesel suçun içinden gelen kişisel tanıklık ve psikoterapi düşüncesidir. Kamplarda ölüm, kişinin yeterince umutlu olmamasından değil, Nazi sisteminin açlık, hastalık, zorla çalıştırma ve cinayet düzeninden kaynaklanmıştır.",
            "Frankl bazı gözlemlerini genel insan psikolojisine bağlar. Bunlar güçlü düşünme araçları olabilir; yine de kamp yaşamının tamamını veya her mahkûmun deneyimini temsil etmez. Başka tanıklıklar başka duygular, sessizlikler ve çelişkiler taşır.",
            "Bu özet, anlam fikrini günlük sıkıntılara taşırken tarihsel acıyı kişisel gelişim dekoruna çevirmeyecek. Büyük felaket ile sıradan moral bozukluğu arasında ölçü farkı olduğunu hep hatırlatacak.",
        ], "BAŞLANGIÇ"),
        entry("İstasyonda parçalanan eski hayat", [
            "Tren durur. İnsanlar nereye geldiklerini tam bilmeden aşağı indirilir. Bağırış, acele ve belirsizlik içinde aileler ayrılır. Frankl kamp deneyiminin ilk ruhsal dönemini şok olarak anlatır: Zihin olan biteni gerçek dışı bir sahne gibi algılar.",
            "Yeni gelen insan, birkaç saat önce taşıdığı mesleğin, evin, eşyaların ve planların koruyucu duvar olmadığını görür. Üzerindeki kıyafet, saç ve adı bile sistemli biçimde hedef alınır. Amaç yalnız bedeni denetlemek değil, kişiyi kendine ait hikâyeden koparmaktır.",
            "Şok bazen tuhaf bir umutla birlikte gelir. İnsan, son anda bir istisna olacağına veya yanlışlığın düzeltileceğine inanabilir. Zihin dayanılmaz bilgiyi bir anda almak yerine küçük parçalar hâlinde kabul eder. Bu, aptallık değil korunma biçimidir.",
            "Frankl'ın anlattığı 'seçim' sahneleri, kamp sisteminin keyfî gücünü gösterir. Bir el hareketi ölüm ile geçici yaşamı ayırabilir. Mahkûmun karakteri değil, failin kurduğu mekanizma belirleyicidir.",
            "Akılda kalan görüntü bavulunu tutan insan değildir; bavulun artık hiçbir şeyi koruyamadığını fark eden insandır. Eski hayatın eşyaları geride kalırken içeride hangi bağın tutulacağı sorusu başlar.",
        ], "BİRİNCİ KISIM · KAMP DENEYİMİ", art="arrival-platform", caption="İstasyondaki ilk saatler, eski hayat ile kamp düzeni arasındaki acımasız kopuşu başlatır."),
        entry("İsim yerine numara: Kimliği silme düzeni", [
            "Bir insanın adı, başkalarının ona seslenme biçimidir. Kamp düzeni bu sesi kesip kişiyi değiştirilebilir bir birime dönüştürür. Saçın kesilmesi, eşyanın alınması, aynı kıyafet ve sürekli emir, 'senin özel hayatının önemi yok' mesajını tekrarlar.",
            "Kimlik yalnız nüfus kâğıdı değildir. Sabah sevdiğiniz fincan, yaptığınız iş, sizi bekleyen kişi, kendi seçtiğiniz yürüyüş yolu kim olduğunuzu küçük küçük taşır. Bunlar yok edildiğinde benlik aynasız bir odada kalır.",
            "Frankl mesleki geçmişini ve yazmak istediği kitabı içeride tutmaya çalışır. Bu, kampın onu doktor olarak tanıdığı anlamına gelmez. Dışarıdaki kimliğinin zihinsel izi, içeride kendine verdiği cevabın bir parçası olur.",
            "Bazı mahkûmlar anılar, dua, şiir veya geleceğe dair görev aracılığıyla iç bağ kurmuştur; bazıları kuramamıştır. Hiçbiri ahlaki puan değildir. Aşırı açlık ve şiddet zihinsel alanı daraltır, insanı yalnız bir sonraki lokmaya kilitleyebilir.",
            "Bu bölümün gündelik hayata düşen küçük gölgesi şudur: Birini yalnız işi, hastalığı veya dosya numarasıyla görmek de onun hikâyesini küçültür. Ölçek aynı değildir ama insanı etikete indirme mekanizması tanıdıktır.",
        ], "BİRİNCİ KISIM · KAMP DENEYİMİ", art="name-number", caption="Kimliği silmeye çalışan düzen, insanı adı ve hikâyesi olan bir kişiden değiştirilebilir numaraya indirger."),
        entry("Duyguların kabuk bağlaması", [
            "İlk şokun ardından Frankl ikinci ruhsal dönemi duyarsızlaşma olarak tarif eder. İnsan her acıyı ilk günkü açıklıkla hissederse ayakta kalamayabilir. Zihin, yaranın üstünde kabuk oluşturur; korkunç görüntüler gündelik düzenin parçasıymış gibi görünmeye başlar.",
            "Bu kayıtsızlık zalimlik ile aynı şey değildir. Bazen sinir sisteminin aşırı uyarılmaya karşı kalkanıdır. Açlık, soğuk ve dövülme arasında bütün dikkatin bir parça ekmeğe yönelmesi, kişinin ahlaki değerlerinin yok olduğu anlamına gelmez.",
            "Yine de koruyucu kabuğun bedeli vardır. Başkasının acısına tepki vermek zorlaşabilir, insan kendi iç sesine yabancılaşabilir. Kamp, mahkûmları kaynak için birbirleriyle yarışmaya zorlayarak dayanışmayı da sistemli biçimde yaralar.",
            "Frankl küçük farklılıklara dikkat eder: Birinin son parçasını paylaşması, diğerinin gücünü korumaya çalışması, kapo sistemindeki ayrıcalıklar. Bu davranışları yalnız 'iyi insan, kötü insan' diye açıklamak, zorlayıcı yapıyı görünmez kılar.",
            "Gündelik hayatta tükenmiş bir bakım çalışanının soğuklaşması buna çok uzak bir benzetmeyle anlaşılabilir. İnsan bazen duygusuz olduğu için değil, çok fazla duyguya maruz kaldığı için kapanır.",
        ], "BİRİNCİ KISIM · KAMP DENEYİMİ", art="emotional-shell", caption="Duyarsızlaşma, sürekli şiddet altında zihnin oluşturduğu koruyucu ama bedelli bir kabuk olabilir."),
        entry("Bir lokma ekmek kadar küçülen dünya", [
            "Açlık uzun sürdüğünde hayatın bütün cümleleri yiyecek kelimesine doğru çekilir. Mahkûmlar tariflerden, eski sofralardan ve hayalî yemeklerden konuşabilir. Bu, yüzeysellik değil, bedenin acil ihtiyacının düşünce alanını işgal etmesidir.",
            "Normal zamanda büyük görünen felsefi tartışmalar, soğukta saatlerce ayakta bekleyen insan için uzaklaşır. Frankl, yüksek ideallerden söz ederken bile bedenin gerçeğini saklamaz. Uykusuzluk, bitkinlik ve hastalık iradeyi daraltır.",
            "Bir parça ekmeği hemen yemek mi, güne yaymak mı? Küçücük karar, denetimin neredeyse yok olduğu yerde kişiye geçici bir zaman duygusu verebilir. Sabahın parçası ile akşamın parçası arasında gelecek kurulmuş olur.",
            "Buradan romantik bir yoksulluk övgüsü çıkarılamaz. Açlık insanı arındıran öğretmen değil, Nazi kamp sisteminin kullandığı işkence ve imha aracıdır. Anlam fikri, ekmek ihtiyacını geçersiz kılmaz.",
            "Bölümün güçlü dersi, zihnin bedenden ayrı bir kahraman olmadığıdır. İnsan anlam arar ama önce suya, yemeğe, uykuya ve güvenliğe ihtiyaç duyan canlı bir bedendir.",
        ], "BİRİNCİ KISIM · KAMP DENEYİMİ", art="bread-world", caption="Uzun açlıkta dünya küçülür; bir parça ekmek zamanın ve dikkatin merkezine yerleşir."),
        entry("Küçük seçimlerin kalan alanı", [
            "Frankl'ın en çok hatırlanan fikri, dış koşulların korkunç biçimde daraldığı yerde bile insanın tutumuna ait küçük bir alan kalabileceğidir. Bu alan sınırsız değildir. Kapıyı açıp çıkmak, çalışmayı reddetmek veya şiddeti durdurmak mahkûmun elinde değildir.",
            "Kalan alan bazen bir başkasına sert cevap vermemek, ekmeğin küçücük bir parçasını paylaşmak veya zihninde sevdiği kişiye dönmek kadar dardır. Büyük kahramanlık değil, insanlığın tamamen teslim edilmemesidir.",
            "Bu fikir yanlış kullanılırsa mağdura yük bindirir: 'Demek ki doğru tutumu seçseydin acın azalırdı.' Frankl'ın düşüncesini etik biçimde okumak için imkân ile sorumluluğu ayırmak gerekir. Seçenek yoksa suç da kişiye ait değildir.",
            "Günlük hayatta alan daha geniş olabilir. Değiştiremediğimiz bir hastalık sonucu ile doktor randevusuna hazırlanma biçimi aynı şey değildir. İş kaybını seçmeyiz; yardım istemeyi, günün küçük düzenini ve kiminle konuşacağımızı bazen seçebiliriz.",
            "Küçük alanı bir oda gibi hayal edin. Duvarları biz kurmamış olabiliriz. Yine de içeride yüzümüzü hangi pencereye çevireceğimize dair bazen birkaç santimlik hareket kalır.",
        ], "BİRİNCİ KISIM · KAMP DENEYİMİ", art="small-choice", caption="Dış özgürlük yok edildiğinde bile bazen tutuma ait çok küçük, kırılgan bir iç alan kalabilir."),
        entry("Gelecekteki kürsü: Acının dışından kendine bakmak", [
            "Frankl bazı anlarda zihninde gelecekte bir ders salonu kurar. Kendini yaşadıklarını anlatan bir konuşmacı olarak hayal eder. O anki çamur ve soğuk, bitmiş bir olayın incelendiği sahneye dönüşür. Acı kaybolmaz ama zaman içindeki yeri değişir.",
            "Bu yöntemde gelecek, kaçış masalı değil bakış noktasıdır. Bugünkü ben, yarının gözünden görülür. 'Bu an sonsuza kadar sürmeyecek' düşüncesi, kamp gerçeği içinde kesin bir güvence değildir; yine de zihinsel mesafe yaratabilir.",
            "Bir ameliyat öncesi korkan insanın, iyileştikten sonra bugünü anlatacağını hayal etmesi daha küçük ölçekte benzer bir araçtır. Zihin, yalnız içinde bulunduğu dakikaya hapsolmadığını hisseder.",
            "Fakat gelecek tasarısı herkes için mümkün olmayabilir. Depresyon, travma ve ağır yoksunluk geleceği boşaltabilir. Böyle birine 'hayal et, geçer' demek yardım değil baskı olabilir. Bazen gelecek önce başka bir insanın desteğiyle ödünç alınır.",
            "Akılda kalan görüntü, tel örgünün ötesinde kurulmuş hayalî bir kürsüdür. İnsan oraya fiziksel olarak ulaşmış değildir; fakat bugünkü acıyı tek zaman olmaktan çıkarır.",
        ], "BİRİNCİ KISIM · KAMP DENEYİMİ", art="future-lectern", caption="Gelecekteki bir kürsüyü hayal etmek, acı içindeki bugüne dışarıdan bakılabilecek bir zaman penceresi açar."),
        entry("Sevilen kişinin zihindeki varlığı", [
            "Zorla çalıştırılırken Frankl eşini düşünür. Onun hayatta olup olmadığını bilmez. Buna rağmen sevilen kişinin zihinsel varlığı, kampın el koyamadığı bir ilişki alanı oluşturur. Sevgi burada romantik mutluluk değil, ötekinin varlığını iç dünyada koruma biçimidir.",
            "Bir insanı sevmek, yalnız yanında olduğu saatleri sevmek değildir. Onun bakışını, sesini ve dünyadaki benzersiz yerini taşımaktır. Frankl bu deneyimden, insanın başka birini dış özelliklerinin ötesinde görebildiği sonucunu çıkarır.",
            "Bu düşünce yas yaşayan okura tanıdık gelebilir. Kaybedilen kişi fiziksel olarak dönmez; fakat kararların, alışkanlıkların ve hatıraların içinde ilişki biçim değiştirerek sürebilir. Bu süreklilik acıyı yok etmez.",
            "Sevgiyi anlamın tek yolu saymak da doğru değildir. Eşi veya ailesi olmayan insan eksik değildir. Frankl'ın daha geniş yaklaşımında iş, yaratma, deneyim ve tutum da anlamın yollarıdır.",
            "Bölümün unutulmaz görüntüsü, sert bir kış sabahında görünmeyen iki insanın konuşmasıdır. Dışarıdan yalnız bir mahkûm vardır; içeride ilişki hâlâ cümle kurmaktadır.",
        ], "BİRİNCİ KISIM · KAMP DENEYİMİ", art="inner-beloved", caption="Sevilen kişinin zihindeki varlığı, fiziksel ayrılığın içinde korunabilen bir ilişki alanı yaratabilir."),
        entry("Mizah ve güzellik: Duvarın ince çatlağı", [
            "Korkunç bir ortamda küçük bir şaka nasıl mümkün olabilir? Frankl mizahı, insanın durumundan bir anlığına uzaklaşmasını sağlayan ruhsal silahlardan biri sayar. Şaka felaketi küçültmez; felaketin bütün zihni işgal etmesine kısa bir ara verir.",
            "Bir gün batımı, uzaktaki dağ veya birkaç dakikalık müzik de aynı çatlağı açabilir. İnsan güzelliği fark ettiği için kamp daha az suç olmaz. Tam tersine, şiddet düzeninin tamamen yok edemediği algı gücü görünür olur.",
            "Hastane koridorunda yakınını bekleyen iki kişinin küçük bir anıya gülmesi bazen dışarıdan uygunsuz görünebilir. Oysa gülme yasın inkârı değil, sinir sisteminin nefes alma biçimi olabilir. İnsan tek bir duygudan oluşmaz.",
            "Burada 'olumlu düşünce' sloganı yoktur. Frankl neşeyi emirle üretmez. Küçük anlar kendiliğinden gelir ve kısa sürer. Onları değerli yapan, bütün karanlığı aydınlatmaları değil, karanlığın tek gerçek olmadığını göstermeleridir.",
            "Akılda kalacak resim kalın beton duvar değil, içinden bir çizgi ışık geçen ince çatlak olsun. Mizah ve güzellik bazen yalnız o çizgidir.",
        ], "BİRİNCİ KISIM · KAMP DENEYİMİ", art="crack-of-light", caption="Mizah ve güzellik, korkunç koşulları inkâr etmeden zihne kısa bir mesafe ve nefes alanı açabilir."),
        entry("Özgürlükten sonra neden sevinç hemen gelmez?", [
            "Kamp kapıları açıldığında hikâyenin mutlu sonla bitmesi beklenir. Frankl üçüncü ruhsal dönemde bunun böyle olmadığını anlatır. İnsan özgür olduğunu bilir ama sevinci hissedemeyebilir. Uzun baskıdan sonra duyguların geri dönmesi zaman alır.",
            "Dış dünya gerçek dışı görünebilir. Güzel bir manzara bile beklenen coşkuyu üretmez. Sinir sistemi yıllarca tehlikeye göre ayarlanmışsa güvenliğin haberini bir günde kabul etmez. Kurtuluş fiziksel bir olaydır; ruhsal uyum ayrı bir yolculuktur.",
            "Üstelik eve dönmek, bekleyen hayatı bulmak anlamına gelmeyebilir. Sevilen kişiler öldürülmüş, ev alınmış, şehir değişmiştir. Hayatta kalma umudu gerçekleşirken o umudun bağlandığı dünya yok olmuş olabilir.",
            "Frankl bazı kurtulanlarda acı çektikleri için başkasına zarar verme hakkı doğmuş gibi bir öfke görülebileceğini söyler. Travma davranışı açıklar ama her davranışı haklı çıkarmaz. Özgürlük, sorumluluğu yeniden kurmayı da gerektirir.",
            "Bu bölüm bugünkü travma anlayışına açılan önemli kapıdır: Tehlikenin bitmesi, bedenin tehlike programını hemen kapatmaz. 'Artık iyisin' demek iyileşmeyi hızlandırmaz.",
        ], "BİRİNCİ KISIM · KAMP DENEYİMİ", art="liberation-numbness", caption="Kapı açıldığında beden özgürleşebilir; duyguların güvenli dünyaya dönmesi ise daha uzun sürebilir."),
        entry("Logoterapi: Mutluluk yerine yön aramak", [
            "Kitabın ikinci kapısında kamp anlatısından terapi düşüncesine geçeriz. Frankl, insanı yalnız haz arayan veya güç isteyen bir varlık olarak görmez. Önemli güdülerden birinin, hayatında yerine getirilmesi gereken bir anlam bulmak olduğunu savunur.",
            "Anlamı haritada kuzeyi gösteren ok gibi düşünün. Yol çamurlu olabilir, hava kötü olabilir, yürümek yine de zor olabilir. Ok mutluluk üretmez; hangi tarafa emek vereceğinizi gösterir. Bazen anlamlı hayat neşeli değil, ağırdır.",
            "Logoterapist hazır bir anlam paketi satmaz. Kişinin kendi durumunda hangi görevin, ilişkinin veya tavrın çağırdığını görmesine yardım eder. 'Hayattan ne bekliyorum?' sorusu, 'Hayat şu anda benden ne bekliyor?' biçiminde ters çevrilir.",
            "Bu yaklaşımın gücü sorumluluğu canlı tutmasıdır. Tehlikesi ise sosyal engelleri görmezden gelip her sorunu kişinin anlam eksikliğine bağlamaktır. İşsizlik yalnız tutum, şiddet yalnız bakış açısı değildir.",
            "Dengeli okuma şunu söyler: Koşullar gerçektir; yine de koşulların içinde bazen yön seçme ihtiyacı kalır. Terapi bu iki gerçeği aynı anda taşımalıdır.",
        ], "İKİNCİ KISIM · LOGOTERAPİ", art="inner-compass", caption="Anlam, mutluluk garantisi değil; zor bir yolda emeğin hangi yöne verileceğini gösteren iç pusuladır."),
        entry("Varoluş boşluğu: Pazar günü neden ağır gelebilir?", [
            "Hafta boyunca iş ve görevlerle koşan biri pazar sabahı boşluk hissedebilir. Yapılacaklar listesi sustuğunda 'Bütün bunları niçin yapıyorum?' sorusu yükselir. Frankl buna varoluş boşluğu der: İnsan davranışını yönlendiren anlamın belirsizleşmesi.",
            "Geçmişte gelenekler ve topluluk kuralları birçok seçimi hazır veriyordu. Modern insan daha özgür olabilir ama yönü kendi kurmak zorundadır. Başkalarının yaptığını taklit etmek veya güçlü birinin istediğini yapmak, bu boşluğu geçici olarak örtebilir.",
            "Boşluk her zaman klinik hastalık değildir. Bazen hayatın eski düzeninin artık yetmediğini bildiren işarettir. Çocuklar evden ayrıldığında, emeklilikte veya uzun kariyerin sonunda eski kimlik gevşer ve yeni soru açılır.",
            "Tüketim bu soruya hızlı cevap sunar: Yeni eşya, yeni gezi, yeni unvan. Haz kısa sürünce boşluk geri gelir. Frankl hazzı kötülemez; onu yönün yerine koymanın yetmediğini söyler.",
            "Bu bölümün günlük sorusu 'Beni sürekli ne mutlu eder?' değil, 'Bugün hangi küçük şeye sadık kalırsam günüm boşa gitmemiş olur?' olabilir.",
        ], "İKİNCİ KISIM · LOGOTERAPİ", art="empty-sunday", caption="Görevler sustuğunda ortaya çıkan boşluk, hayatın yönü hakkında bastırılmış soruyu görünür kılabilir."),
        entry("Anlama giden üç yol", [
            "Frankl anlamı üç ana yolda anlatır. Birincisi dünyaya bir şey vermektir: İş yapmak, üretmek, bakım sunmak, bir sorunu çözmek. Bu yol yalnız büyük eserler için değildir; bir bahçeyi yıllarca korumak da yaratıcı sorumluluk olabilir.",
            "İkinci yol dünyadan bir şey almaktır: Bir insanı sevmek, doğayı, sanatı veya hakikati deneyimlemek. Burada anlam performans puanına bağlı değildir. Hastalık nedeniyle üretimi azalan biri, ilişki ve deneyim içinde hâlâ zengin bir hayat kurabilir.",
            "Üçüncü yol, kaçınılmaz acı karşısındaki tutumdur. En çok yanlış anlaşılan budur. Acı önlenebiliyorsa onu gidermek görevdir. Haksız evlilikte kalmak, tedaviyi reddetmek veya yoksulluğu romantikleştirmek 'anlamlı acı' değildir.",
            "Ancak değiştiremeyeceğimiz kayıp, kalıcı hastalık veya ölüm gerçeğiyle karşılaştığımızda tavrımız yeni bir anlam alanı açabilir. Acıya teşekkür etmek gerekmez; onun bizi tamamen tanımlamasına izin vermemek mümkündür.",
            "Üç yolu bir masa gibi düşünün: Üretmek, ilişki kurmak, kaçınılamayana karşı tavır almak. Her dönemde aynı ayak yük taşımaz; hayat ilerledikçe ağırlık birinden diğerine geçebilir.",
        ], "İKİNCİ KISIM · LOGOTERAPİ", art="three-paths", caption="Anlam üretmekten, ilişki ve deneyimden, ayrıca yalnız kaçınılamayan acıya karşı alınan tavırdan doğabilir."),
        entry("Acı, suçluluk ve ölüm: Üç karanlık misafir", [
            "Frankl hayatın üç kaçınılmaz yüzüne bakar: acı, suçluluk ve ölüm. Bunları yok sayan iyimserliği ince bulur. Trajik iyimserlik dediği yaklaşım, karanlığı gördüğü hâlde hayata evet diyebilecek bir yön arar.",
            "Acı, insanı otomatik olarak yüceltmez. Bazı acılar parçalar, bazıları öfke ve hastalık bırakır. Anlam, acının kendisinde hazır değildir; kişi destek ve zamanla ona vereceği cevabı kurabilir veya kuramayabilir.",
            "Suçluluk değişim imkânı taşır. Yaptığımız bir yanlış geri alınmayabilir ama sorumluluğu kabul etmek, zararı onarmak ve aynı davranışı tekrarlamamak geleceğin biçimini değiştirir. Utanç 'Ben bütünüyle kötüyüm' derken sorumluluk 'Yanlış yaptım ve cevap vermeliyim' diyebilir.",
            "Ölüm, zamanın sınırlı olduğunu hatırlatır. Bir gün bitecek olması bir konuşmayı, ziyareti veya emeği değersiz yapmaz; tam tersine ertelemenin sonsuz olmadığını gösterir. Müzik parçası bittiği için anlamsız değildir.",
            "Üç misafiri kapı dışarı atamayız. Fakat onları evin sahibi yapmak zorunda da değiliz. Frankl'ın iyimserliği tam bu gerilimde durur.",
        ], "İKİNCİ KISIM · LOGOTERAPİ", art="tragic-triad", caption="Acı, suçluluk ve ölüm inkâr edilmeden; bunların içinden sorumluluk ve yön üretme imkânı aranır."),
        entry("Korkudan korkmak: Ters niyet ve dikkati dışarı çevirme", [
            "Uykusuz kalmaktan korkan insan yatağa 'Bu gece mutlaka uyumalıyım' baskısıyla girer. Kalbi hızlandıkça başarısız olduğuna inanır; korku uyanıklığı, uyanıklık korkuyu büyütür. Frankl bu kendini besleyen döngülere dikkat eder.",
            "Ters niyet tekniğinde kişi bazen korktuğu şeyi kontrollü biçimde istemeye davet edilir: 'Bakalım ne kadar uyanık kalabileceğim.' Amaç kendine zarar vermek değil, korkunun ciddiyetini mizahla gevşetmektir. Baskı azalınca belirti üzerindeki kilit de gevşeyebilir.",
            "Dikkati dışarı çevirme ise kişinin kendini sürekli ölçmekten çıkıp bir işe veya ilişkiye yönelmesidir. Kekemeliğini her hecede kontrol eden insan daha çok sıkışabilir; konuştuğu kişiye ve anlatmak istediğine döndüğünde öz-gözetim azalabilir.",
            "Bu teknikler her sorun için ev ödevi değildir. Panik, travma, obsesyon veya uykusuzlukta nasıl uygulanacağı profesyonel değerlendirme gerektirebilir. Yanlış yerde 'korkunun üstüne git' demek kişiyi zorlayabilir.",
            "Gündelik ders, bazen belirtinin kendisinden çok onun gelmemesi için kurduğumuz sıkı nöbetin hayatı daralttığını fark etmektir.",
        ], "İKİNCİ KISIM · LOGOTERAPİ", art="fear-loop", caption="Belirtiyi zorla kovalamak bazen korku döngüsünü büyütür; mizah ve dışa yönelen dikkat kilidi gevşetebilir."),
        entry("Hayatın genel anlamı değil, bu anın sorusu", [
            "Frankl herkes için tek cümlelik bir hayat anlamı vermez. Anlam kişiden kişiye ve saatten saate değişebilir. Satrançta 'en iyi hamle nedir?' sorusunun tahtayı görmeden cevaplanamaması gibi, anlam da somut duruma bakmadan bulunmaz.",
            "Bir anne için gece hastanede çocuğunun yanında durmak, bir öğretmen için öğrencinin utancını fark etmek, emekli biri için komşusunun işini kolaylaştırmak o anın çağrısı olabilir. Büyük proje kadar küçük cevap da önemlidir.",
            "Bu yaklaşım anlamı gökten inecek tek büyük keşif olmaktan kurtarır. İnsan yıllarca 'gerçek tutkum ne?' diye beklerken önündeki sorumluluğu kaçırabilir. Anlam çoğu zaman bulduğumuz kadar yaptığımız bir şeydir.",
            "Yine de her talep anlamlı değildir. Sömürücü patronun beklentisi, şiddet uygulayan kişinin isteği veya toplumun utanç dayatması hayatın çağrısı diye kabul edilemez. Vicdan da eleştiri ve ilişki içinde sınanmalıdır.",
            "Bugünün sorusunu yarının kesin kimliği yapmayın. Anlam pusulası hareket hâlindedir; aynı kuzeyde bile yolun dönüşü değişir.",
        ], "İKİNCİ KISIM · LOGOTERAPİ", art="situational-question", caption="Anlam tek bir evrensel cevap değil; somut durumda hayatın önümüze koyduğu soruya verilen özgül cevaptır."),
        entry("Özgürlük heykelinin karşısına sorumluluk heykeli", [
            "Frankl özgürlüğü tek başına bırakmanın keyfîliğe dönüşebileceğini söyler. Seçebilmek önemlidir; fakat seçim kime ve neye karşı cevap verdiğimiz sorusunu da taşır. Bu nedenle özgürlüğün karşı kıyısında sorumluluk bulunur.",
            "Bir işi bırakma özgürlüğü, ardından gelen maddi ve ilişkisel sonuçları yok etmez. Bir görüşü söyleme özgürlüğü, başkasına verilen zararı otomatik olarak önemsiz yapmaz. Özgürlük boş alanda değil, insanlar arasındaki ağda kullanılır.",
            "Frankl'ın meşhur önerisi, Amerika'nın doğusundaki Özgürlük Heykeli'ne karşı batıda bir Sorumluluk Heykeli dikilmesidir. Bu görüntü kitabın tamamını küçük bir haritaya çevirir: İki kıyı birbirini dengeler.",
            "Sorumluluk sürekli suçluluk demek değildir. Her şeyi kontrol edemeyiz. Sorumlu olmak, gerçekten etki edebildiğimiz alanı görmek ve sahip olmadığımız güç için kendimizi cezalandırmamaktır.",
            "Kırkından sonra bu ayrım özellikle rahatlatıcı olabilir. Geçmişte değiştiremeyeceğiniz çok şey vardır; bugün cevap verebileceğiniz birkaç ilişki ve iş de vardır. Enerji ikinci alana taşınır.",
        ], "İKİNCİ KISIM · LOGOTERAPİ", art="freedom-responsibility", caption="Özgürlük seçim alanını açar; sorumluluk bu seçimin insanlar ve sonuçlar içindeki yönünü belirler."),
        entry("Anlamı mutluluk baskısına çevirmemek", [
            "Anlam arayışı da yeni bir başarı yarışına dönüşebilir. İnsan 'Herkes amacını buldu, ben bulamadım' diye kendini eksik hisseder. Oysa Frankl'a göre mutluluk doğrudan kovalandığında kaçabilir; anlamlı bir işe veya insana yönelmenin yan ürünü olarak gelebilir.",
            "Aynı şey başarı için de geçerlidir. Sürekli başarıyı hedefleyen kişi kendi puanını izlemekten yaptığı işin kendisini unutabilir. Bir arkadaşla konuşurken 'iyi arkadaş görünüyor muyum?' diye düşünmek, arkadaşın sesini duymayı zorlaştırır.",
            "Anlamın tek, büyük ve değişmez olması gerekmez. Bugün yaşlı babayı doktora götürmek, yarın bir kitabı bitirmek, başka gün yalnız dinlenip iyileşmek anlamlı olabilir. Dinlenme üretimsizlik değildir.",
            "Depresyondaki birine amaç listesi vermek yeterli değildir. Ruhsal hastalık kişinin anlam görme kapasitesini örtebilir; tedavi, sosyal destek ve güvenlik önce gelebilir. Anlam tıbbi bakımın rakibi değildir.",
            "Bu bölümün uyarısı açıktır: Anlam, insanı hayata bağlayan ip olabilir; boynuna geçirilen yeni bir görev halatı olmamalıdır.",
        ], "ÜÇÜNCÜ KISIM · BUGÜNE TAŞIMAK", art="meaning-without-pressure", caption="Anlam arayışı yeni bir başarı baskısı değil; dikkati benlik puanından ilişki ve işe çeviren yön olmalıdır."),
        entry("Kitabın sınırları ve eleştiriler", [
            "İnsanın Anlam Arayışı milyonlarca okura cesaret vermiştir. Aynı zamanda Holokost araştırmacıları, Frankl'ın kişisel deneyiminden fazla genel psikolojik sonuçlar çıkardığını ve anlatının hayatta kalmayı anlamlı tutuma gereğinden fazla bağlayabildiğini eleştirmiştir.",
            "Bu eleştiri önemlidir çünkü kampta hayatta kalma çoğu kez sevk tarihi, iş görevi, hastalık, rastlantı ve fail kararları gibi kişinin denetimi dışındaki etkenlere bağlıydı. Ölenlerin anlamı az, iradesi zayıf değildi.",
            "Frankl'ın logoterapi düşüncesinin kamplardan önce şekillenmeye başladığını da bilmek gerekir. Kamp deneyimi yaklaşımını derinden etkiledi; fakat teori yalnız orada bir anda doğmadı. Kitap bazen iki hikâyeyi birbirine çok sıkı bağlar.",
            "Bir başka sınır, anlam dilinin kültürden kültüre değişmesidir. Bireysel görev vurgusu, topluluk, adalet ve maddi koşulların rolünü gölgede bırakabilir. İnsan yalnız iç tutumla yaşamaz; güvenli kurumlara ve başkalarının yardımına da ihtiyaç duyar.",
            "Eleştirel okumak kitabı çöpe atmak değildir. Onu doğru rafa koymaktır: Tek bilimsel kanıt veya bütün Holokost'un sesi değil; güçlü, tartışmalı ve etkili bir kişisel-felsefi tanıklık.",
        ], "ÜÇÜNCÜ KISIM · BUGÜNE TAŞIMAK", art="critical-shelf", caption="Kitap güçlü bir tanıklıktır; fakat bütün kurbanların deneyimi veya hayatta kalmanın tek açıklaması olarak okunmamalıdır."),
        entry("Bir günün anlam deneyi", [
            "Sabah kendinize 'Bugün mutlu olacak mıyım?' diye sormak yerine üç küçük pencere açın. Dünyaya ne verebilirim? Kimle veya neyle gerçekten karşılaşabilirim? Değiştiremeyeceğim bir şeye karşı hangi tavrı seçebilirim?",
            "Cevaplar büyük olmak zorunda değildir. Bir işi özenle bitirmek, birinin sözünü bölmeden dinlemek, ağrı içinde yardımı kabul etmek yeterli olabilir. Akşam kendinizi yargılamak için değil, hangi pencerenin açıldığını görmek için dönüp bakın.",
            "Ertesi gün cevap değişebilir. Anlam, ömür boyu aynı işi yapan kahramanın sloganı değil; hayatın değişen sorularına verilen canlı cevaptır. Bazen en anlamlı hareket dinlenmek, sınır koymak veya 'bunu tek başıma yapamıyorum' demektir.",
            "Bu deney acıyı kutsamaz. Önlenebilir acıda ilk sorumluluk onu azaltmaktır. Haksızlığı kabul etmek değil, yardım, tedavi ve adalet aramak da anlamlı eylemdir.",
            "Frankl'dan alınabilecek en sakin ders budur: Hayatın cevabını uzaktan beklemek yerine bugün size düşen küçük cevabı yaşayabilirsiniz.",
        ], "SONUÇ", art="daily-windows", caption="Bir günün anlamı üretmek, karşılaşmak ve kaçınılamayana karşı tavır almak için açılan küçük pencerelerde bulunabilir."),
        entry("Bir dakikalık harita", [
            "Kitap önce şok, duyarsızlaşma ve özgürleşme sonrası uyum gibi kamp deneyimi aşamalarını anlatır. Ardından insanın anlam arayışını merkeze alan logoterapiye geçer. Anlam; bir şey üretmekten, bir insan veya güzellikle karşılaşmaktan ve yalnız kaçınılamayan acıya karşı alınan tavırdan doğabilir.",
            "Özgürlük sınırsız değildir ve sorumlulukla birlikte düşünülür. Korkunun korkuyu büyüttüğü döngülerde mizah, ters niyet ve dikkati dışarı çevirme gibi teknikler ele alınır. Anlam tek bir evrensel cümle değil, somut durumun sorusuna verilen cevaptır.",
            "En önemli etik sınır: Hayatta kalamayan insanları tutum eksikliğiyle açıklamayın. Acıyı anlamlı kılmak, acıyı üreten faili veya koşulu aklamak değildir.",
        ], "SONUÇ"),
        entry("Akılda kalacak dört görüntü", [
            "Bavulunu koruyamayan insan: Eski kimliğin kopuşu. Tel örgünün ötesindeki hayalî kürsü: Geleceğin bakış noktası. Üç ayaklı masa: Üretmek, ilişki kurmak, kaçınılamayana tavır almak. İki kıyıdaki heykel: Özgürlük ile sorumluluğun dengesi.",
            "Bu görüntüler kitabı bir motivasyon sloganından kurtarır. Anlam her şeyi çözmez; fakat insanın hangi işe, ilişkiye veya değere doğru hareket edeceğini gösterebilir.",
            "Ve son cümle şu olabilir: İnsan her koşulun efendisi değildir. Yine de bazı anlarda koşullara vereceği cevabın yazarı olma payını koruyabilir.",
        ], "SONUÇ"),
    ],
})


BOOKS.append({
    "bookNo": 142,
    "title": "Karanlık Bir Dünyada Bilimin Mum Işığı",
    "author": "Carl Sagan",
    "subtitle": "Şaşkınlığı öldürmeden kuşkuyu canlı tutan, iddiaları sınamak için gündelik bir alet çantası sunan sıcak ve eleştirel rehber.",
    "coverImage": "/images/optimized/summary-art-142-bilimin-mum-isigi-v2-960.webp",
    "coverStyle": "artwork",
    "pdfUrl": "/data/pdfs/142-karanlik-bir-dunyada-bilimin-mum-isigi-ozeti.pdf",
    "pdfLabel": "25–50 sayfalık PDF'yi indir",
    "longForm": True,
    "chapterArtStyle": "monochrome-engraving",
    "chapterArtColor": "#554D79",
    "meta": {
        "originalTitle": "The Demon-Haunted World: Science as a Candle in the Dark",
        "compiler": "Zihin Gezgini · Yapay zekâ destekli çalışma",
        "date": "Temmuz 2026",
        "language": "Türkçe",
    },
    "intro": "Carl Sagan bu kitapta bilimi ezberlenecek sonuçlar yığını olarak değil, kandırılmamak için öğrenilen bir düşünme alışkanlığı olarak anlatır. UFO'lardan cadı avlarına, hayal ürünü ejderhadan okul sınıfına kadar çok geniş bir sahnede aynı soruyu sorar: Bir iddiayı doğru saymadan önce ne istemeliyiz? Cevabı soğuk bir alay değildir. Merak ile kuşkunun evliliğidir. Bu rehber kitabın yirmi beş bölümünü on altı güçlü durakta toplar, 1995'in örneklerini bugünün sosyal medya, yapay zekâ ve komplo ortamına taşır. İnanç sahibini küçümsemeden, kanıt standardını da gevşetmeden ilerler.",
    "sources": [
        {"id": 1, "title": "Penguin Random House – The Demon-Haunted World", "url": "https://www.penguinrandomhouse.com/books/159731/the-demon-haunted-world-by-carl-sagan/"},
        {"id": 2, "title": "Kitabın bölüm listesi", "url": "https://afterall.net/books/the-demon-haunted-world/"},
        {"id": 3, "title": "Carl Sagan Portal – Cornell University Library", "url": "https://guides.library.cornell.edu/carl_sagan"},
        {"id": 4, "title": "NASA – bilimsel yöntem ve kanıt kaynakları", "url": "https://science.nasa.gov/universe/overview/"},
        {"id": 5, "title": "Stanford Encyclopedia of Philosophy – scientific method", "url": "https://plato.stanford.edu/entries/scientific-method/"},
    ],
    "entries": [
        entry("Mum neden projektör değil?", [
            "Sagan bilimi karanlığı bir anda yok eden dev bir projektöre değil, küçük bir muma benzetir. Mum sınırlı bir alanı aydınlatır; kenarlarda gölgeler kalır. Fakat o küçük ışık, karanlıkta uydurulan her hikâyeye teslim olmamızı engeller.",
            "Bilim her sorunun cevabını bildiğini iddia etmez. Gücü, bilmediği yerde durabilmesi ve hatasını düzeltecek yollar kurmasıdır. Bu nedenle 'bilmiyoruz' cümlesi yenilgi değil, araştırmanın dürüst başlangıcıdır.",
            "Kitabı okurken alaycı kuşkuculuk ile araştırıcı kuşkuyu ayıracağız. Birincisi her şeye 'saçma' der. İkincisi 'Bunu nasıl biliyoruz, başka açıklama var mı, hangi gözlem fikrimizi değiştirir?' diye sorar.",
        ], "BAŞLANGIÇ"),
        entry("En değerli şey: Yanılabileceğini bilen zihin", [
            "Bir insan yıllarca bir fikre emek verdiğinde onu bırakmak zorlaşır. Fikir artık yalnız düşünce değil, kimliğin odası olur. Bilimin en değerli alışkanlığı, o odanın kapısına dışarıdan kilit takmamasıdır: Yeni kanıt geldiğinde düzen değişebilir.",
            "Sagan çocukken bilimkurgu ve gökyüzüyle büyülenir. Merakını kaybetmez; fakat sevdiği bir fikrin doğru olmasını istemekle doğru olduğuna dair kanıt bulmak arasındaki farkı öğrenir. Bu ayrım kitabın kalbidir.",
            "Bilim insanları da kibirli, kıskanç veya hatalı olabilir. Yöntemin değeri insanların kusursuzluğundan gelmez. Sonucun başkaları tarafından sınanması, ölçümün açıklanması ve eleştirinin kurumsallaşması kişisel kusurlara karşı fren sağlar.",
            "Mahallede herkesin çok sevdiği bir şifacının etkisiz olabileceğini düşünmek rahatsız edicidir. Bilim tam da burada dostluk ile kanıtı ayırmamızı ister. İyi niyet, doğru teşhis veya etkili tedavi garantisi değildir.",
            "Akılda kalan görüntü, fikirlerini cam fanusta saklamayan zihindir. Dışarıdan hava, soru ve düzeltme girebilir.",
        ], "BİRİNCİ KISIM · MERAK VE YANILGI", art="open-mind", caption="Bilimsel zihin, sevdiği fikri bile dışarıdan soru ve düzeltmeye açık tutar."),
        entry("Hayret ile kuşkunun evliliği", [
            "Yıldızlı gökyüzüne bakıp şaşırmak kolaydır. 'Oradaki ışığın ne olduğunu nasıl biliyoruz?' diye sormak ikinci adımdır. Sagan'a göre iyi bilim, bu iki hareketi ayırmaz: Hayret bizi yaklaştırır, kuşku yanlış sonuca çarpmamızı önler.",
            "Yalnız kuşku kullanan insan, hiçbir şeye güvenmeyen taş bir duvara dönüşebilir. Yalnız hayret kullanan insan ise her parlak iddiaya kapılabilir. Evlilik benzetmesinin gücü buradadır; iki taraf birbirinin aşırılığını dengeler.",
            "Bir arkadaşınız gökyüzünde garip ışık gördüğünü anlattığında onun deneyimini küçümsemek gerekmez. Gerçekten bir ışık görmüş olabilir. Soru, deneyimin hangi açıklamayı zorunlu kıldığıdır. Uçak, uydu, gezegen, atmosfer olayı ve algı yanılması da masadadır.",
            "Kuşku insanlara değil, iddialara yönelmelidir. 'Yalancısın' demek yerine 'Bu gözlemi hangi başka yoldan kontrol edebiliriz?' sorusu ilişkiyi korurken standardı yükseltir.",
            "Bilimin ideal duygusu soğukluk değildir. Gözleri açık hayranlıktır: Harika olabilir; şimdi bakalım gerçekten öyle mi.",
        ], "BİRİNCİ KISIM · MERAK VE YANILGI", art="wonder-skepticism", caption="Hayret araştırmaya çağırır, kuşku ise ilk büyüleyici açıklamada durmamızı engeller."),
        entry("Ay'daki adam ve Mars'taki yüz", [
            "Bulutlarda deve, tostta insan yüzü, Ay'da profil görürüz. Beyin dağınık çizgilerden anlamlı biçim çıkarma konusunda hızlıdır. Bu yetenek günlük yaşamda değerlidir; çalılıkta yüz veya hareketi erken fark etmek hayatta kalmayı kolaylaştırmış olabilir.",
            "Aynı hız bazen olmayan örüntüyü varmış gibi gösterir. Mars'ın Cydonia bölgesindeki düşük çözünürlüklü bir görüntü, ışık ve gölgeyle dev bir yüze benzetilmişti. Daha iyi görüntüler geldiğinde arazi sıradan tepelik yapı olarak göründü.",
            "Burada önemli olan ilk gözlemle alay etmek değil, çözünürlük arttığında fikri değiştirebilmektir. 'Yüz olabilir' geçici hipotezdir. 'Kesin uygarlık yaptı ve NASA saklıyor' iddiası ek kanıt yükü taşır.",
            "Bugün telefon kamerasındaki sıkıştırma lekeleri, gece çekimindeki ışık halkaları ve yapay zekâ üretimi görüntüler yeni Mars yüzleri yaratıyor. Görüntünün çarpıcı olması kaynağının güvenilir olduğu anlamına gelmez.",
            "Akılda kalan ders: Beyin bir örüntü avcısıdır. Avladığı her şekil gerçek hayvan değildir.",
        ], "BİRİNCİ KISIM · MERAK VE YANILGI", art="face-on-mars", caption="Beyin belirsiz şekillerde yüz görmeye hazırdır; daha iyi veri ilk izlenimi düzeltebilir."),
        entry("Uzaylı ihtimali ile uzaylı ziyareti iddiası aynı şey değil", [
            "Evren çok büyük olduğu için başka yerde yaşam bulunması makul bir olasılık olabilir. Bundan 'Dün gece tarladaki ışık uzay gemisiydi' sonucu çıkmaz. Genel olasılık ile belirli olayın kanıtı arasında uzun bir köprü vardır.",
            "Sagan uzaylı fikrini küçümsemez; hayatını gezegen bilimine ve dünya dışı yaşam arayışına adamıştır. Tam da bu yüzden kanıt standardını yüksek tutar. Olağanüstü ziyaret iddiası, yanlış anlaşılmış ışık veya sahte fotoğraftan daha güçlü izler bırakmalıdır.",
            "Tanık dürüst olabilir ve yine de yanılabilir. Bellek kamera kaydı değildir; anlatıldıkça değişir, soruların biçiminden etkilenir ve boşlukları doldurur. Çok kişinin aynı şeyi söylemesi de hepsinin bağımsız bilgi aldığı anlamına gelmeyebilir.",
            "Gizlilik iddiası her kanıt eksikliğini açıklamak için kullanılırsa sınanamaz hâle gelir. Kanıt yoksa kurum sakladı, çelişki varsa örtbas etti denir. Böyle bir iddia hangi durumda yanlış sayılacağını göstermiyorsa araştırma kapısı kapanır.",
            "En heyecanlı tutum şudur: Evren yaşam dolu olabilir; bu nedenle her ışığı ziyaret saymak yerine gerçek izi bulacak kadar titiz olmalıyız.",
        ], "BİRİNCİ KISIM · MERAK VE YANILGI", art="alien-claim", caption="Evrende yaşam olasılığı ile belirli bir ışığın uzaylı ziyareti olduğuna dair kanıt aynı şey değildir."),
        entry("Gece odasındaki varlık: Deneyim gerçek, açıklama yanlış olabilir", [
            "Bir insan uyanır, hareket edemez, göğsünde ağırlık hisseder ve odada bir varlık görür. Deneyim korkunç derecede gerçektir. Uyku felci, beynin uyanıklığı ile REM uykusundaki kas hareketsizliğinin kısa süre üst üste gelmesiyle bu sahneyi açıklayabilir.",
            "Farklı kültürler aynı bedensel deneyime cadı, cin, şeytan veya uzaylı adı vermiştir. Değişen varlık, beynin belirsiz duyumu elindeki kültürel hikâyeyle tamamladığını düşündürür. İnsan uyduruyor diye suçlanmaz; yorumun kaynağı araştırılır.",
            "Halüsinasyon yalnız ağır ruhsal hastalıkta görülmez. Uykusuzluk, ateş, bazı ilaçlar, nörolojik durumlar, yas ve duyusal yoksunluk algıyı etkileyebilir. Bu genişlik, her olağanüstü anlatıyı aynı tanıya sıkıştırmamayı gerektirir.",
            "'Ben gördüm' önemli bir veridir ama açıklamanın sonu değildir. Kamera da hata yapabilir; fakat bağımsız kayıt, zaman damgası, çevresel ölçüm ve başka tanıklarla hikâye daha sınanabilir olur.",
            "Sagan'ın insancıl dersi, deneyimi ciddiye alıp ilk açıklamayı mecburi saymamaktır. Korkuyu küçümsemeden nedeni arayabiliriz.",
        ], "BİRİNCİ KISIM · MERAK VE YANILGI", art="sleep-paralysis", caption="Uyku felcinde yaşanan korku gerçektir; kültür, belirsiz deneyime farklı doğaüstü adlar verebilir."),
        entry("Eski şeytanların yeni uzaylıları", [
            "Yüzyıllar önce geceleri insanları ziyaret ettiği anlatılan şeytanlar, bugün bazı hikâyelerde uzaylılara benzer görevler üstlenir. Kaçırılma, beden üzerinde işlem, kayıp zaman ve gizli mesaj gibi motifler yeni kostümle tekrar ortaya çıkabilir.",
            "Bu benzerlik bütün anlatıların aynı kaynaktan geldiğini kanıtlamaz. Fakat insan korkularının kültürel teknolojiye göre biçim değiştirdiğini gösterir. At arabası çağında gökyüzü gemisi başka, uzay çağında başka görünür.",
            "Cadı avları, korkunun kuruma dönüştüğünde ne kadar ölümcül olabileceğini hatırlatır. İtiraf için işkence yapılır, işkence altında gelen anlatı yeni suçlamalara kanıt sayılır. Sistem kendi hikâyesini üretip sonra doğrulanmış gibi kullanır.",
            "Bugünün dijital cadı avında fiziksel işkence olmayabilir; kesilmiş video, isim listesi ve milyonlarca paylaşım bir insanı savunma imkânı bulamadan suçlu ilan edebilir. Mekanizma tanıdıktır: Önce korku, sonra grup teyidi, en son kanıt arayışı.",
            "Geçmişin şeytanlarını incelemek yalnız tarih merakı değildir. Kendi çağımızın hangi korkuyu hangi yeni kostümle dolaştırdığını sormaktır.",
        ], "İKİNCİ KISIM · İDDİALARI SINAMAK", art="old-demons-new-aliens", caption="Kültürel korkular çağın diline göre kostüm değiştirir; eski şeytan anlatıları yeni uzaylı hikâyelerine benzeyebilir."),
        entry("Hatırlamak kazı yapmak değildir", [
            "Belleği toprağa gömülmüş sağlam bir sandık gibi düşünürsek doğru soruyla içinden değişmeden çıkacağını sanırız. Oysa bellek her hatırlamada yeniden kurulur. Parçalar korunur, boşluklar beklenti ve sonradan öğrenilen bilgilerle dolabilir.",
            "Sagan, yönlendirici terapinin özellikle olağanüstü kaçırılma veya unutulmuş travma anlatılarında sahte kesinlik üretebileceğinden kaygılanır. Terapistin beklediği cevap sorunun içine gizlenirse kişi zamanla hayal, rüya ve anıyı ayırmakta zorlanabilir.",
            "Bu, insanların anlattığı travmaları otomatik olarak reddetmek anlamına gelmez. İki hata mümkündür: Gerçek mağduru inanmamak ve hiç yaşanmamış ayrıntıyı telkinle sağlamlaştırmak. Güvenli yaklaşım, destek verirken sorgulamayı yönlendirmemektir.",
            "Bir aile fotoğrafını yıllar sonra herkes farklı anlatabilir. Kimin nerede durduğu küçük ayrıntı gibi görünür ama tekrar edilen yanlış hikâye zamanla tanıdık geldiği için doğru hissedilir. Tanıdıklık doğruluk değildir.",
            "Bellek bölümünün anahtarı şudur: İnsan samimi olabilir, acı çekebilir ve yine de bazı ayrıntılarda yanılabilir. Şefkat ile kanıt dikkatini karşı karşıya koymak gerekmez.",
        ], "İKİNCİ KISIM · İDDİALARI SINAMAK", art="reconstructive-memory", caption="Bellek kapalı sandıktan çıkarılan kayıt değil; her hatırlamada yeniden kurulan kırılgan bir anlatıdır."),
        entry("Garajdaki görünmez ejderha", [
            "Sagan size garajında ateş püskürten bir ejderha olduğunu söyler. Bakmak istersiniz: Görünmezdir. Yere un serpelim dersiniz: Havada uçar. Isı ölçelim dersiniz: Ateşi ısısızdır. Her test önerisi yeni bir kaçışla karşılanır.",
            "Bir noktada şu soru doğar: Hiçbir gözlemle sıradan boş garajdan ayrılamayan ejderhanın var olduğunu söylemek ne ekliyor? Hikâye, yanlışlanabilirlik fikrini gündelik bir tiyatroya çevirir.",
            "İyi bir iddia, hangi bulgunun onu destekleyeceğini ve hangi bulgunun zayıflatacağını söyleyebilmelidir. Her sonuç iddiayla uyumluysa iddia dünyadan bilgi almıyor, yalnız kendini koruyor olabilir.",
            "Günümüzde 'Bu yatırım kesin kazandırır; düşerse gizli güçler bastırdı, yükselirse ben bildim' diyen kişi de ejderhaya yeni özellik ekler. Tahminin önceden kaydedilmesi ve başarısızlığın kabul edilmesi gerekir.",
            "Ejderha benzetmesi inanç sahibiyle dalga geçmek için değil, testten sürekli kaçan açıklamanın nasıl boşaldığını görmek içindir. Garajda ne olursa fikrimiz değişmeyecekse araştırma yapmıyoruzdur.",
        ], "İKİNCİ KISIM · İDDİALARI SINAMAK", art="garage-dragon", caption="Her testten yeni bahaneyle kaçan görünmez ejderha, sınanamayan iddianın bilgi üretmediğini gösterir."),
        entry("Saçmalık saptama çantası", [
            "Sagan'ın en ünlü bölümü, yanıltıcı iddialara karşı zihinsel bir alet çantası sunar. İlk alet bağımsız doğrulamadır. Aynı videoyu kopyalayan yüz hesap, yüz kaynak değildir; tek kaynağın yüz yankısıdır.",
            "İkinci alet farklı açıklamaları yan yana koymaktır. Baş ağrısı yalnız gizemli bir enerjiye değil, susuzluğa, uykusuzluğa, enfeksiyona veya başka birçok nedene bağlı olabilir. Sevdiğimiz açıklamayı seçmeden önce rakipleri düşünürüz.",
            "Üçüncü alet ölçmektir. 'Çok arttı' yerine ne kadar, hangi dönemle karşılaştırınca, nüfusa oranla mı diye sorarız. Sayı her şeyi çözmez ama belirsiz sıfatın büyüsünü azaltır.",
            "Dördüncü alet, kanıt zincirinin her halkasını sınamaktır. Fotoğraf gerçek mi, tarih doğru mu, olayla bağlantısı var mı? Zincirin bir halkası koparsa sonucun ağırlığı azalır.",
            "Son alet, fikrin sahibine değil fikre bakmaktır. Ünvan kanıt değildir; ünvanı olmayan kişi de doğru olabilir. Çanta, otoriteyi yok saymaz ama sözünü bağımsız delille desteklemesini ister.",
        ], "İKİNCİ KISIM · İDDİALARI SINAMAK", art="baloney-kit", caption="Bağımsız doğrulama, rakip açıklama, ölçüm ve sınanabilirlik kandırılmaya karşı günlük alet çantasıdır."),
        entry("Zihnin kaygan taşları: En sık mantık tuzakları", [
            "Bir ürün kullandıktan sonra iyileşmek, ürün sayesinde iyileştiğimizi kanıtlamaz. Hastalık zaten geçiyor olabilir, başka tedavi etkili olabilir veya belirtiler doğal olarak dalgalanabilir. 'Bundan sonra oldu, demek bundan oldu' tuzağı çok yaygındır.",
            "Bir uzman söyledi diye doğru saymak otoriteye başvuru hatasıdır. Uzmanlık önemlidir ama alanı, kanıtı ve uzmanlar arasındaki uzlaşı sorulmalıdır. Ünlü fizikçinin beslenme yorumu otomatik olarak beslenme araştırması değildir.",
            "Korkuluk hatasında karşımızdakinin savını zayıf bir kuklaya çeviririz. 'Bu ilacın yan etkisini konuşalım' diyen kişiyi 'Bütün tıbba düşman' ilan etmek tartışmayı kolay kazanılır ama anlamsız hâle getirir.",
            "Sahte ikilem yalnız iki seçenek sunar: Ya bu komploya inanırsın ya da körsündür. Oysa üçüncü seçenek kanıtın yetersiz olduğunu söylemek olabilir. Dünya çoğu kez iki düğmeli cihaz değildir.",
            "Bu hataları bilmek başkalarını yenmek için değil, kendi sevdiğimiz fikrin kaydığı taşı fark etmek içindir. En zor uygulama aynaya dönendir.",
        ], "İKİNCİ KISIM · İDDİALARI SINAMAK", art="logic-traps", caption="Nedensellik, otorite, korkuluk ve sahte ikilem gibi tuzaklar düşüncenin bastığı kaygan taşlardır."),
        entry("Bilim karşıtlığı nereden beslenir?", [
            "Bilim bazen soğuk, kibirli ve insan anlamına düşman bir kurum gibi sunulur. Bu görüntünün bir kısmı kötü iletişimden, gerçek etik ihlallerden ve kurumlara duyulan haklı güvensizlikten beslenebilir. İnsanların kaygısını küçümsemek karşıtlığı büyütür.",
            "Fakat bilimin hatası ile bilimsel yöntemin gereksizliği aynı sonuç değildir. Bir doktor yanlış yaptı diye mikrop kuramı ortadan kalkmaz. Tam tersine hata kayıtları, bağımsız denetim ve daha iyi çalışma tasarımı yöntemin düzeltme araçlarıdır.",
            "Sagan Newton'ın simyaya ve çağının başka inançlarına ilgisini hatırlatır. Büyük bilimsel başarı, insanın her konuda yanılmaz olması demek değildir. Tarih, dahilerin bile çağlarının kör noktalarını taşıdığını gösterir.",
            "Bugün güvensizlik algoritmalarla büyütülebilir. En öfkeli içerik daha çok paylaşılır; sakin düzeltme heyecan üretmez. Bilim iletişimi yalnız doğru veri vermekle yetinemez, insanların neden o hikâyeye ihtiyaç duyduğunu da anlamalıdır.",
            "Güven talep edilmez, kazanılır. Açık veri, çıkar çatışmasının belirtilmesi, belirsizliğin dürüstçe söylenmesi ve hata düzeltme güvenin gerçek malzemeleridir.",
        ], "ÜÇÜNCÜ KISIM · BİLİM VE TOPLUM", art="science-distrust", caption="Bilime güvensizlik gerçek hatalardan beslenebilir; çözüm yöntemi terk etmek değil, şeffaflık ve düzeltmeyi güçlendirmektir."),
        entry("Bilim insanları günahı bildiğinde", [
            "Bilim bize atomu parçalama gücü verebilir; o gücün hangi amaçla kullanılacağını tek başına söylemez. Sagan nükleer silah, çevre tahribatı ve teknoloji sorumluluğunu ele alırken bilimsel bilgi ile etik kararın evlenmesi gerektiğini savunur.",
            "'Ben yalnız tekniği geliştirdim' cümlesi sonuçtan tamamen kaçış olamaz. Araştırmacı, kurum, şirket ve devlet farklı düzeylerde sorumluluk taşır. Fakat bütün yükü tek bilim insanına bırakmak da siyasi kararları görünmez kılar.",
            "Bir yapay zekâ sistemi ayrımcı sonuç ürettiğinde yalnız kod satırına bakmak yetmez. Hangi veri seçildi, başarı nasıl ölçüldü, kim denetledi, zarar gören itiraz edebiliyor mu? Etik, ürün çıktıktan sonra yapıştırılan etiket değildir.",
            "Bilimin öz-eleştiri geleneği burada hayati olur. Riskleri söyleyen araştırmacı düşman değil, güvenlik sisteminin parçasıdır. Kurumun itibarını korumak için sorunu saklamak kısa vadede sessizlik, uzun vadede daha büyük güvensizlik üretir.",
            "Mum ışığı yalnız dışarıdaki hurafeyi değil, bilimin kendi gölgesini de aydınlatmalıdır.",
        ], "ÜÇÜNCÜ KISIM · BİLİM VE TOPLUM", art="science-ethics", caption="Bilim güç üretir; bu gücün amacı ve sınırı etik, hukuk ve demokratik sorumlulukla birlikte belirlenir."),
        entry("Aptal soru yoktur, susturulmuş merak vardır", [
            "Çocuk 'Gökyüzü neden karanlık?' diye sorduğunda soru basit görünür; aslında evrenin yaşı ve genişlemesine kadar uzanır. Sagan sınıfın en değerli kaynağının bu doğal merak olduğunu düşünür. Alay, merakın üstüne erken kapak kapatır.",
            "Eğitim yalnız doğru cevabı veren öğrenciyi ödüllendirirse soru sorma riskli hâle gelir. Çocuk, anlamadığı yeri gizlemeyi öğrenir. Oysa bilimde iyi soru bazen mevcut cevaptan daha değerlidir; yanlış varsayımı görünür yapar.",
            "Deney yapmak pahalı laboratuvar gerektirmez. İki saksıyı farklı ışıkta büyütmek, iddia yazılmadan önce tahmin kurmak, sonucu kaydetmek ve beklenmeyen farkı konuşmak yöntemin küçük modelidir.",
            "Yetişkin de 'Bunu bilmem gerekirdi' utancıyla soru sormaktan kaçınır. Dolandırıcılar bu utancı sever; karmaşık kelimeyle itirazı bastırırlar. Basit soru çoğu sis perdesini dağıtır: Para tam olarak nereden geliyor? Ölçüm nasıl yapıldı?",
            "Sınıfın ve toplumun sağlığı, en bilgisiz görünen soruya verilen cevabın tonunda saklı olabilir.",
        ], "ÜÇÜNCÜ KISIM · BİLİM VE TOPLUM", art="questioning-classroom", caption="Soru sorabildiği için utanmayan sınıf, bilimsel düşünmenin ve demokratik katılımın ilk laboratuvarıdır."),
        entry("Ev yanarken: Bilim okuryazarlığı neden lüks değil?", [
            "Sagan, teknolojik gücü artan ama bilimin nasıl çalıştığını az bilen bir toplumu yanıcı maddelerle dolu evde yaşayan insana benzetir. Düğmeler büyürken onları kimin, hangi bilgiyle çevirdiği sorusu hayati olur.",
            "İklim, salgın, enerji, tarım ve dijital güvenlik kararları uzmanlık içerir. Vatandaşın her konuda uzman olması gerekmez; fakat iyi uzmanlığı kötü iddiadan ayıracak temel soruları bilmesi gerekir.",
            "Demokrasi yalnız oy verme günü değildir. Kanıtın açık olması, iktidarın sorgulanması, gazetecinin kaynak istemesi ve yurttaşın gerekçe talep etmesi sürekli bir bakım işidir. Sorgulanmayan otorite bilimsel de siyasi de olsa risklidir.",
            "Komplo hikâyesi karmaşık dünyaya tek fail verir ve rahatlık sağlar. Gerçek açıklama ise kurum, hata, çıkar, rastlantı ve geri bildirimlerden oluşabilir. Daha sıkıcı görünür ama çözüm üretmeye daha elverişlidir.",
            "Ev yanarken yalnız yangına inanmayanlarla tartışmak yetmez. Alarmın neden çalışmadığını, çıkışın kime kapalı olduğunu ve söndürme aracının nerede olduğunu da araştırmak gerekir.",
        ], "ÜÇÜNCÜ KISIM · BİLİM VE TOPLUM", art="house-on-fire", caption="Bilim okuryazarlığı, güçlü teknolojilerle dolu ortak evde alarmı anlayıp çıkışı birlikte bulma becerisidir."),
        entry("Bilgi özgürlüğe nasıl yol açar?", [
            "Okuma yazma, yalnız tabelayı çözmek değildir. Bir insan sözleşmeyi okuyabildiğinde, hesabı kontrol ettiğinde ve resmi açıklamayla başka kaynağı karşılaştırdığında başkasının yorumuna daha az bağımlı olur. Bilgi küçük bir özgürlük alanı açar.",
            "Sagan kölelikten kurtulan Frederick Douglass'ın okuma öğrenmesini örnek alır. Okuma, baskının doğal değil kurulmuş olduğunu görmesine yardım eder. Yetkilinin anlattığı dünya tek mümkün dünya olmaktan çıkar.",
            "Bugün dijital okuryazarlık aynı yolun devamıdır. Arama sonucunun sırası doğruluk sırası değildir. Reklam, haber, görüş ve yapay üretilmiş içerik aynı ekranda görünebilir. Kaynağa dönmek yeni okuma yazmadır.",
            "Bilgi tek başına özgürlük garantisi değildir; eğitimli insanlar da propaganda yapabilir. Fakat bilgiye erişim ve eleştiri hakkı olmadan güç dengesini değiştirmek çok daha zordur.",
            "Bir toplumun mumları yalnız laboratuvarda yanmaz. Kütüphanede, bağımsız basında, açık sınıfta ve soruya ceza verilmeyen kurumlarda çoğalır.",
        ], "ÜÇÜNCÜ KISIM · BİLİM VE TOPLUM", art="literacy-freedom", caption="Okuryazarlık, otoritenin anlattığı dünyayı başka kaynaklarla karşılaştırma ve kendi hükmünü kurma gücü verir."),
        entry("Önem bağımlılığı: Evren neden bize özel mesaj vermek zorunda değil?", [
            "İnsan rastlantıda kendine dönük işaret görmekten hoşlanır. Radyoda tam düşündüğü şarkının çalması kaderin mesajı gibi hissedilebilir. Unuttuğumuz yüzlerce uyumsuz an değil, çarpıcı eşleşme hatırlanır.",
            "Astroloji ve kişiye özel kehanetler çoğu insana uyabilecek geniş cümleler kullanabilir. 'Bazen sosyalsiniz ama zaman zaman yalnız kalmak istersiniz' ifadesi tanıdık geldiği için özel görünür. Özel hissetmek, ölçüm değildir.",
            "Sagan evrenin bizi küçümsemediğini söyler; evrenin niyeti olduğunu varsaymak gerekmez. Kozmik ölçekte küçük olmak değersiz olmak anlamına gelmez. Değerimizi galaksinin bize mesaj göndermesinden değil, birbirimize karşı sorumluluğumuzdan kurabiliriz.",
            "Sosyal medya bu önem arzusunu sayılara çevirir: Beğeni, görüntülenme, takipçi. Algoritma bizi merkeze koyuyor gibi görünürken aslında dikkatimizi satabilir. Kişiselleştirme, evrenin sizi seçmesi değildir.",
            "Daha olgun hayret şudur: Evren bizim için kurulmamış olsa bile onu anlayabilecek ve birbirimizi önemseyebilecek canlılarız.",
        ], "ÜÇÜNCÜ KISIM · BİLİM VE TOPLUM", art="significance", caption="Kozmik merkezin dışında olmak değersizlik değil; değeri birbirimizle kurduğumuzu fark etme fırsatıdır."),
        entry("Gerçek vatansever soru sorar", [
            "Bir ülkeyi sevmek, yöneticilerinin her sözünü doğru saymak değildir. Sagan'a göre demokratik sadakat, kurumların hata yapabileceğini kabul edip onları daha iyi olmaya zorlayan soruları içerir.",
            "Savaş, güvenlik veya salgın gibi korkulu dönemlerde soru sormak ihanet diye damgalanabilir. Oysa tam da yüksek riskte kanıt, yetki sınırı ve alternatifler daha dikkatle incelenmelidir. Acele, hesap verebilirliği ortadan kaldırmamalıdır.",
            "Soru yalnız karşı tarafa yöneltilirse araç propaganda olur. Kendi siyasi grubumuzun grafiğine, sevdiğimiz gazetecinin kaynağına ve bize yarayan iddiaya da aynı standardı uygulamak gerekir.",
            "Bugün yapay zekâ ile üretilmiş ses ve videolar, eski propaganda araçlarını hızlandırıyor. İlk heyecan anında paylaşmak yerine kaynağın aslına bakmak, başka güvenilir kanalı aramak ve biraz beklemek demokratik bir davranıştır.",
            "Sagan'ın son mesajı karanlık değildir. İnsanlar kandırılabilir ama öğrenebilir; kurumlar hata yapabilir ama düzeltilebilir. Mum küçük olduğu için değersiz değil, elden ele verilebildiği için güçlüdür.",
        ], "ÜÇÜNCÜ KISIM · BİLİM VE TOPLUM", art="patriot-questions", caption="Demokratik bağlılık, sevdiğimiz grubun iddialarına da kanıt ve hesap verebilirlik soruları yöneltebilmektir."),
        entry("Telefon ekranında beş dakikalık Sagan deneyi", [
            "Çarpıcı bir iddia gördüğünüzde önce durun. İddiayı tek cümleyle yazın. 'Bir şeyler oluyor' değil, tam olarak neyin olduğu söyleniyor? Belirsiz cümle ölçülemez ve kolayca şekil değiştirir.",
            "Sonra ilk kaynağı bulun. Haber başka habere, o da kesilmiş videoya mı dayanıyor? Bağımsız iki kaynak var mı, yoksa aynı metin dolaşıyor mu? Tarih ve yer doğru mu? Eski görüntü yeni olay diye sunulmuş olabilir.",
            "Rakip açıklama kurun. En sevdiğiniz açıklamayı değil, en sıradan olanı da masaya koyun. Hangi bulgu ikisini ayırır? Fikrinizi değiştirecek hiçbir şey düşünemiyorsanız garajdaki ejderhaya yaklaşmış olabilirsiniz.",
            "Duygunuzu fark edin. İçerik sizi çok öfkelendiriyor veya tam inanmak istediğiniz şeyi söylüyorsa hızınızı düşürün. Duygu yanlışlık kanıtı değildir; paylaşma hızını artıran kuvvettir.",
            "Son olarak 'Henüz bilmiyorum' deme hakkınızı kullanın. İnternet hemen taraf seçmeye zorlar. Bilimsel olgunluk bazen kararın ertelenmesidir.",
        ], "SONUÇ", art="phone-check", caption="Bir iddiayı paylaşmadan önce netleştirmek, ilk kaynağa gitmek ve rakip açıklama kurmak beş dakikalık savunmadır."),
        entry("Bir dakikalık harita", [
            "Bilim, sonuç ezberi değil, hatayı bulup düzeltme yöntemidir. Hayret araştırmayı başlatır; kuşku ilk güzel hikâyede durmayı engeller. Beyin yüz ve örüntü görmeye, bellek boşluk doldurmaya, grup ise inancını teyit etmeye yatkındır.",
            "Bağımsız doğrulama, rakip hipotez, ölçüm, yanlışlanabilirlik ve mantık tuzaklarını tanıma Sagan'ın alet çantasını oluşturur. Bilim insanlarının da etik sorumluluğu ve kör noktaları vardır; kurumlar şeffaflıkla güven kazanır.",
            "Bilim okuryazarlığı yalnız laboratuvar meselesi değildir. Eğitim, basın ve demokrasi için özgürlük aracıdır. En kısa kural: İddiaya açık ol, kanıt istemekten utanma, fikrini değiştirecek koşulu önceden düşün.",
        ], "SONUÇ"),
        entry("Akılda kalacak beş görüntü", [
            "Karanlıktaki küçük mum: Sınırlı ama dürüst bilgi. Mars'taki yüz: Örüntü avcısı beyin. Gece odasındaki varlık: Gerçek deneyim, tartışmalı açıklama. Garajdaki ejderha: Testten kaçan iddia. Alet çantası: Bağımsız doğrulama, ölçüm ve rakip açıklama.",
            "Bu görüntüler birini tartışmada yenmek için değil, kendi zihninizin acele ettiği anı yakalamak için kullanılmalı. En kolay kandırıldığımız yer, zaten inanmak istediğimiz yerdir.",
            "Sagan'ın sıcaklığı burada saklıdır: İnsan zihni yanılabilir ama değersiz değildir. Aynı zihin merak eder, yöntem kurar ve hatasını düzeltebilir.",
        ], "SONUÇ"),
    ],
})


BOOKS.append({
    "bookNo": 213,
    "title": "Görme Biçimleri",
    "author": "John Berger",
    "subtitle": "Bir resme, reklama ve ekrana yalnız ne gösterdiğiyle değil; kimin baktığı, kimin sahip olduğu ve ne vaat ettiğiyle bakmayı öğreten görsel rehber.",
    "coverImage": "/images/optimized/summary-art-213-gorme-bicimleri-v2-960.webp",
    "coverStyle": "artwork",
    "pdfUrl": "/data/pdfs/213-gorme-bicimleri-ozeti.pdf",
    "pdfLabel": "25–50 sayfalık PDF'yi indir",
    "longForm": True,
    "chapterArtStyle": "monochrome-engraving",
    "chapterArtColor": "#566148",
    "meta": {
        "originalTitle": "Ways of Seeing",
        "compiler": "Zihin Gezgini · Yapay zekâ destekli çalışma",
        "date": "Temmuz 2026",
        "language": "Türkçe",
    },
    "intro": "Görme Biçimleri ince ama içine yerleştirilmiş bir levye gibi güçlü kitaptır. John Berger, Sven Blomberg, Chris Fox, Michael Dibb ve Richard Hollis'in BBC dizisinden geliştirdiği çalışma yedi denemeden oluşur; üçü yalnız görüntülerle konuşur. Kitap, sanat tarihinin kapısını saygıyla açıp içerideki mobilyaların kimin zevkine göre yerleştirildiğini sorar. Bu rehber resimlerin yerine geçmez; onları daha dikkatli görmeye hazırlık yapar. Yağlıboya tablonun mülkiyetle, kadın imgesinin bakışla, modern reklamın gelecekteki benliğimize duyduğumuz kıskançlıkla nasıl bağ kurduğunu bol gündelik örnekle anlatır.",
    "sources": [
        {"id": 1, "title": "Penguin – Ways of Seeing", "url": "https://www.penguin.co.uk/books/56465/ways-of-seeing-by-berger-john/9780141035796"},
        {"id": 2, "title": "Penguin – kitabın yedi denemelik yapısı üzerine", "url": "https://www.penguin.co.uk/discover/articles/penguin-books-that-shocked-society"},
        {"id": 3, "title": "British Library – John Berger archive", "url": "https://www.bl.uk/collection-guides/john-berger-archive"},
        {"id": 4, "title": "BBC Arts – Ways of Seeing", "url": "https://www.bbc.co.uk/programmes/p00hqlvs"},
        {"id": 5, "title": "Tate – art terms and visual context", "url": "https://www.tate.org.uk/art/art-terms"},
    ],
    "entries": [
        entry("Bu kitap neden önce göze, sonra kelimeye güvenir?", [
            "Çocuk konuşmadan önce yüzü, ışığı ve mesafeyi ayırt eder. Berger bu basit gerçekten başlar: Görmek, kelimeden önce gelir. Sonra kelimeler gördüğümüz şeye ad verir; fakat görüntü ile açıklama hiçbir zaman tam olarak üst üste oturmaz.",
            "Kitabın üç denemesi yalnız görüntülerden oluşur. Bu sayfalarda okura hazır yorum verilmez; yan yana konan resimler arasında kendi bağlantısını kurması beklenir. Sessizlik, yöntemin parçasıdır.",
            "Bu özet zorunlu olarak kelime kullanıyor. Bu nedenle her bölümde bir görsel düşünme deneyi sunacak ve 'Berger'in tek doğru cevabı budur' demek yerine bakışın nasıl yönlendirildiğini gösterecek.",
        ], "BAŞLANGIÇ"),
        entry("Görmek ile bilmek arasındaki bitmeyen mesafe", [
            "Güneşin battığını görürüz ama Dünya'nın döndüğünü biliriz. Sevdiğimiz kişinin yüzüne bakar, o an ne düşündüğünü tam bilemeyiz. Görüntü dünyadaki yerimizi kurar; bilgi görüntüyü açıklar ama onun yerine geçmez.",
            "Bir tabloya müzedeki etiketi okumadan önce baktığınızda renk, beden ve mekân size bir duygu verir. Etikette 'savaş sonrası dönem' yazınca aynı çizgi yeni anlam kazanır. Kelime resmi değiştirmez; bakışınızın yolunu değiştirir.",
            "Berger, görmenin tarafsız kamera olmadığını söyler. Ne bildiğimiz, neye inandığımız, neyi arzuladığımız ve hangi korkuyu taşıdığımız seçtiğimiz ayrıntıyı etkiler. Aynı caddeyi emlakçı, çocuk ve evsiz insan başka türlü görür.",
            "Bu, her yorumun eşit derecede doğru olduğu anlamına gelmez. Tablonun tarihi, malzemesi ve sipariş koşulu hakkında kanıt vardır. Fakat kanıtın bize ulaşma biçimi de bir çerçeve taşır.",
            "İlk egzersiz basittir: Bir görüntüye on saniye bakın, sonra neyi ilk gördüğünüzü yazın. Görüntüyü değil, bakışınızın alışkanlığını da kaydetmiş olursunuz.",
        ], "BİRİNCİ KISIM · GÖRÜNTÜ VE ÇERÇEVE", art="seeing-knowing", caption="Gözün gördüğü ile zihnin bildiği birbirini etkiler ama hiçbir zaman bütünüyle aynı şey olmaz."),
        entry("Biricik tablo milyonlarca ekrana girince", [
            "Eskiden bir freski görmek için belirli kiliseye gitmek gerekirdi. Fotoğraf ve baskı, görüntüyü yerinden çıkarıp evlere, kitaplara ve ekranlara taşıdı. Tablo artık seyahat etmeyen izleyicinin yanına gelir.",
            "Bu çoğalma erişimi demokratikleştirir. Daha çok insan daha çok sanat görebilir. Aynı zamanda eserin ölçeği, yüzeyi, çevresindeki mimari ve fiziksel mesafe kaybolur. Telefonda parmak ucu kadar görünen tablo, duvarı kaplayan tablonun bedensel etkisini vermez.",
            "Berger bu değişimi yalnız kayıp saymaz. Yeniden üretim eski otoriteyi kırabilir, görüntüyü yeni sorulara açabilir. Ancak müze ve piyasa, 'orijinalin paha biçilmez aurasını' öne çıkararak başka bir gizem üretir.",
            "Bir şarkının stadyumda canlı icrası ile telefon hoparlöründeki kaydı aynı beste ama aynı deneyim değildir. Görsel yeniden üretim de buna benzer: İçerik taşınır, bağlam dönüşür.",
            "Bugün yüksek çözünürlük bile bütün farkı kapatmaz. Ekran resmi yaklaştırır; fakat hangi platformun, hangi kırpma ve sırayla sunduğu yeni bir mekân kurar.",
        ], "BİRİNCİ KISIM · GÖRÜNTÜ VE ÇERÇEVE", art="reproduced-painting", caption="Biricik eser ekrana çoğalınca erişim artar; ölçek, yüzey ve mekânın kurduğu anlam değişir."),
        entry("Kamera resmin içinde yürüdüğünde", [
            "Bir tablo bütündür; kamera ise ayrıntı seçer. Önce uzaktaki yüzü büyütür, sonra ele, sonra masadaki bıçağa geçer. İzleyici ressamın kurduğu aynı anda görme düzenini değil, yönetmenin belirlediği sırayı yaşar.",
            "Müzik eklendiğinde anlam daha da değişir. Sakin bir melodi aynı yüzü hüzünlü, hızlı davul tehditkâr gösterebilir. Görüntü değişmemiştir ama çevresindeki ses, bakışın duygusal rayını döşer.",
            "Haber videosunda bir konuşmanın yalnız beş saniyesini görmek de aynı işlemdir. Kırpma yalan olmak zorunda değildir; fakat önce ve sonra çıkarıldığında başka hikâye kurabilir. Çerçevenin dışı görünmediği için yok sanılır.",
            "Berger'in yöntemi kamerayı düşman ilan etmez. Kameranın tarafsız göz gibi davranmadığını fark ettirir. Her çekim noktası, yakınlık ve sıra bir seçimdir.",
            "Bir sonraki videoda kendinize sorun: Beni nereye baktırıyor, ne kadar süre tutuyor ve çerçevenin dışında ne kalmış olabilir? Görsel okuryazarlık bu üç soruyla başlar.",
        ], "BİRİNCİ KISIM · GÖRÜNTÜ VE ÇERÇEVE", art="camera-crop", caption="Kamera ayrıntıyı seçip sıraya koyduğunda aynı tablodan yeni bir anlatı üretir."),
        entry("Sanatı açıklamak mı, gizemli hâle getirmek mi?", [
            "Sanat uzmanı bazen tabloyu yaklaştırmak yerine kalın bir sisle çevreler. Uzun unvanlar, teknik kelimeler ve erişilmez deha hikâyeleri, izleyiciye 'Bunu anlamak sana düşmez' mesajı verebilir.",
            "Berger özellikle geçmişin toplumsal koşullarını saklayan gizemleştirmeye itiraz eder. Bir portredeki zenginlik yalnız estetik ayrıntı değil, mülkiyet ve sınıf düzeninin işareti olabilir. Güzelliği görmek ile koşulu sormak birbirini bozmaz.",
            "Müze etiketi faydalıdır; eserin tarihini ve malzemesini verir. Sorun etiketin tek izin verilen bakışa dönüşmesidir. İzleyici kendi gördüğünü söylemekten utanırsa sanat yaşayan karşılaşma değil, doğru cevap sınavı olur.",
            "Öte yandan 'Ben böyle hissediyorum, başka bilgi gereksiz' demek de eserin tarihini siler. Berger'in açtığı alan iki yönlüdür: Otoriteyi sorgula, ama kanıtı da öğren.",
            "İyi açıklama kapıyı kapatmaz. 'Bu ayrıntıyı gördün mü; siparişi veren insan için ne ifade etmiş olabilir?' diyerek gözünüzü yeniden tabloya gönderir.",
        ], "BİRİNCİ KISIM · GÖRÜNTÜ VE ÇERÇEVE", art="museum-mystery", caption="Sanat bilgisi eserin kapısını açabilir; uzmanlık dili kapıya bekçi olduğunda görüntü izleyiciden uzaklaşır."),
        entry("Erkekler davranır, kadınlar görünür mü?", [
            "Berger Batı görsel geleneğinde erkek ve kadın için farklı bir düzen kurulduğunu söyler. Erkek çoğu kez yapabilecekleriyle, kadın ise nasıl göründüğüyle değerlendirilir. Kadın hem dünyada yaşar hem kendini başkasının gözünden izlemeyi öğrenir.",
            "Bu iç bölünme gündelik hayatta tanıdıktır. Toplantıda konuşan kadın fikrini anlatırken aynı anda sesinin sert, yüzünün yorgun veya kıyafetinin uygun görünüp görünmediğini düşünebilir. Erkekler hiç öz-gözetim yaşamaz demek değildir; baskının tarihsel dağılımı aynı değildir.",
            "Görsel kültür, kadına 'sen kendini nasıl taşırsan başkaları sana öyle davranır' mesajını tekrarlar. Böylece bakılan kişi, kendi üzerinde bekçi görevi görür. Dış bakış içeride yaşamaya başlar.",
            "Bu fikir sonradan 'erkek bakışı' tartışmalarına güçlü bir zemin sağlamıştır. Berger'in dili ikili cinsiyet kalıpları taşır; bugünün toplumsal cinsiyet çeşitliliğini bütünüyle kapsamaz. Yine de bakış ile güç arasındaki bağı açığa çıkarır.",
            "Akılda kalan ayna şudur: İnsan yalnız kendine bakmaz; başkasının nasıl bakacağını da tahmin ederek kendini düzenler.",
        ], "İKİNCİ KISIM · KADIN İMGESİ VE BAKIŞ", art="watched-woman", caption="Görsel düzen kadını yalnız yaşamaya değil, kendini sürekli dışarıdan izlemeye de zorlayabilir."),
        entry("Çıplak olmak ile nü olmak arasındaki fark", [
            "Çıplak olmak, insanın bedeniyle kendisi olmasıdır. Nü ise Berger'in ayrımında, bedenin seyredilmek üzere görsel nesneye dönüştürülmesidir. Biri yaşanan durum, diğeri bakış için kurulmuş gösteridir.",
            "Avrupa yağlıboya geleneğinde kadın çoğu kez izleyiciye dönük, bedeninin seyredildiğinin farkında ve asıl hikâyedeki erkek için değil görünmeyen erkek izleyici için düzenlenmiş görünür. Mitolojik ad, çıplaklığı saygın kılan ince perde olabilir.",
            "Ayna sık kullanılan bir nesnedir. Resim kadını aynaya bakan kibirli kişi diye suçlayabilir; oysa tablo onu seyirlik hâle getiren düzeni kurmuştur. Önce bakış üretilir, sonra bakılan kişi bakılmaktan sorumlu tutulur.",
            "Her çıplak figür aynı değildir. Bazı eserlerde beden karşılıklı ilişki, kırılganlık veya öznel varlık taşır. Berger geleneğin baskın kuralını gösterir; tek tek bütün tabloları tek cümleyle mahkûm etmez.",
            "Bugün beden pozunun kime hitap ettiğini, bakışın karşılık bulup bulmadığını ve kişinin özne mi dekor mu olduğunu sormak bu ayrımı güncellemenin yoludur.",
        ], "İKİNCİ KISIM · KADIN İMGESİ VE BAKIŞ", art="nude-vs-naked", caption="Çıplak beden yaşanan varlık olabilir; nü geleneği bedeni görünmeyen izleyici için seyir nesnesine çevirebilir."),
        entry("Ayna kimin elinde?", [
            "Bir reklamda kadın aynaya bakar. İlk yorum 'Kendini seviyor' olabilir. Berger'in sorusu farklıdır: Aynadaki bakış kime aittir? Kadın kendini deneyimlemek için mi, dışarıdaki izleyicinin ölçüsüne göre denetlemek için mi bakıyor?",
            "Ayna fiziksel nesne olmadan da çalışır. Telefonun ön kamerası, toplantı ekranındaki küçük yüz penceresi ve sosyal medya beğenisi kişiyi aynı anda yaşayan ve kendini seyreden iki role bölebilir.",
            "Bu bölünme yalnız kadınlara özgü değildir. Erkek bedeni de giderek performans ve görünüm baskısına açılır. Yine de tarihsel reklam dili kadın bedenini daha sürekli ve yaygın biçimde ölçü nesnesi yapmıştır.",
            "Çözüm aynayı kırmak değildir. Kimin ölçüsünü kullandığımızı görmek ve bedenle yalnız dış görüntü üzerinden ilişki kurmamaktır. Güç, görüntüden tamamen kaçmakta değil, bakışın kurallarını fark etmekte olabilir.",
            "Günlük deney: Bir fotoğrafınızı seçerken ilk kaygınızı fark edin. Anıyı mı koruyorsunuz, yoksa görünmeyen bir jürinin vereceği puanı mı hesaplıyorsunuz? Cevap bazen ikisidir.",
        ], "İKİNCİ KISIM · KADIN İMGESİ VE BAKIŞ", art="mirror-gaze", caption="Ayna ve ön kamera, insanı aynı anda yaşayan kişi ve kendini dışarıdan denetleyen seyirciye bölebilir."),
        entry("Görüntüler tek başına tartışabilir mi?", [
            "Kitabın yalnız resimlerden oluşan denemeleri, yan yana koymanın da cümle kurduğunu gösterir. Bir klasik nü ile dergi fotoğrafı peş peşe geldiğinde benzer el hareketi veya bakış yönü kelimesiz bir iddia üretir.",
            "Montaj tarafsız değildir. Hangi görüntünün önce geldiği, sayfadaki büyüklüğü ve aradaki boşluk yorum yaratır. Sessiz deneme, kelimesiz olduğu için masum olmaz; okuru etkin karşılaştırmaya çağırır.",
            "Bugünkü fotoğraf akışı dev bir sessiz denemedir. Tatil, savaş, kahve ve reklam aynı başparmak hareketiyle geçer. Platformun sırası, dünyanın hangi olayının yan yana geleceğini belirler.",
            "Berger'in kitabını ekranda özetlemek bu nedenle ironiktir. Orijinal sayfa düzeni ve görüntü dizisi düşüncenin parçasıdır. Metinsel özet ancak yöntemi anlatabilir; görsel karşılaşmayı bütünüyle taşıyamaz.",
            "Küçük egzersiz: İki ilgisiz reklamı yan yana koyun ve ortak beden duruşu, renk veya statü işaretini bulun. Sessiz dil birden görünür olur.",
        ], "İKİNCİ KISIM · KADIN İMGESİ VE BAKIŞ", art="image-essay", caption="Yan yana gelen görüntüler, kelime kullanmadan benzerlik, karşıtlık ve güç ilişkisi üzerine cümle kurabilir."),
        entry("Yağlıboya resimde dokunulabilir dünya", [
            "Yağlıboya boya, kürkün yumuşaklığını, metalin parlaklığını, meyvenin kabuğunu ve kadifenin ağırlığını şaşırtıcı biçimde gösterebilir. Berger bu tekniğin Avrupa'da özel mülkiyetin yükselişiyle kurduğu ilişkiye bakar.",
            "Zengin tüccar veya toprak sahibi, sahip olduklarını tabloda yeniden görür: Ev, arazi, hayvan, kumaş, gümüş, hizmetçi. Resim yalnız güzellik değil, 'Bunlar benim dünyam' diyen görsel envanter olabilir.",
            "Bir emlak ilanında geniş salonun parlak çekimi bugün benzer iş görür. Mekânı yalnız kullanışlı değil, sahip olunacak arzu nesnesi hâline getirir. Görüntü, nesnenin ele geçirilebilir yüzeyini öne çıkarır.",
            "Bu tez bütün yağlıboya resimleri para makbuzuna indirmez. Dini, kişisel ve eleştirel eserler vardır. Berger baskın geleneğin hangi ekonomik hayalle uyumlandığını sorar.",
            "Tabloya yeniden bakın: Hangi nesne en dokunulabilir çizilmiş, kimin sahipliği ima edilmiş, kim eşya kadar sessiz bırakılmış? Yüzey toplumsal düzeni anlatabilir.",
        ], "ÜÇÜNCÜ KISIM · MÜLKİYET VE YAĞLIBOYA", art="oil-possession", caption="Yağlıboyanın parlak yüzeyleri, sahip olunan kumaş, arazi ve nesneleri dokunulabilir bir görsel envantere çevirebilir."),
        entry("Portrede insan mı, servet mi konuşuyor?", [
            "Büyük portrede kişi masanın yanında durur; arkasında arazi, elinde değerli eşya, üzerinde pahalı kumaş vardır. Yüz bireyi gösterirken çevredeki her ayrıntı statüsünü konuşur. Portre, karakter kadar toplumsal konumu da kalıcılaştırır.",
            "Poz doğal görünse bile iktidar dili taşır. Bedenin kapladığı alan, izleyiciye yukarıdan bakış, hizmetçinin küçük tutulması veya hayvanın sahiplikle gösterilmesi hiyerarşiyi düzenler.",
            "Bugünün şirket portresinde deri koltuk, yüksek kat manzarası ve kitaplık aynı görevi sürdürebilir. İnsan yalnız 'Ben buyum' demez; 'Benim erişimim, zamanım ve çevrem budur' der.",
            "Portre sahibinin gerçek karakterini doğrudan okumak tehlikelidir. Sert bakış zalimlik kanıtı değildir. Daha güvenli olan, görüntünün nasıl bir kamu kişiliği kurmak istediğini sormaktır.",
            "Berger'in merceği kişiyi küçültmez; dekorun sessiz konuşmasını işitmemizi sağlar. Servet çoğu zaman yüzün arkasından konuşur.",
        ], "ÜÇÜNCÜ KISIM · MÜLKİYET VE YAĞLIBOYA", art="portrait-status", caption="Portrede beden kadar kumaş, mobilya ve manzara da statü ve sahiplik üzerine sessizce konuşur."),
        entry("Manzara kimin penceresinden?", [
            "Yeşil tarlalar ve uzak tepeler masum doğa görünümü olabilir. Fakat tablo sipariş veren toprak sahibi için mülkün sınırlarını ve bereketini gösteren pencere işlevi de görebilir. Manzara estetik zevk ile ekonomik sahipliği aynı çerçevede buluşturur.",
            "Haritada boş görünen arazi, orada çalışan veya yaşayan insanlar için boş değildir. Görüntü işçileri küçültüp toprağı sahibinin huzurlu uzantısı olarak sunabilir. Kimin emeği görünmüyor sorusu manzarayı değiştirir.",
            "Sömürge ticaretiyle gelen şeker, tütün, kumaş ve değerli malzeme resimlerde zenginlik işareti olabilir; üretimin zorlayıcı koşulları çerçevenin dışında kalır. Nesnenin parlaklığı yolculuğunun karanlığını gizler.",
            "Bugünkü tatil broşüründe boş kumsal, hizmet verenleri ve yerel yaşamı silerek müşteriye geçici sahiplik duygusu sunabilir. 'Kimsenin olmadığı cennet' aslında birinin evidir.",
            "Manzaraya bakarken güzelliği reddetmek gerekmez. Güzelliğin kimin penceresinden ve hangi görünmez emekle sunulduğunu eklemek görüntüyü zenginleştirir.",
        ], "ÜÇÜNCÜ KISIM · MÜLKİYET VE YAĞLIBOYA", art="owned-landscape", caption="Huzurlu manzara aynı anda güzellik, mülkiyet ve çerçeve dışında bırakılmış emek hikâyesi taşıyabilir."),
        entry("Geleneğin içindeki çatlaklar", [
            "Berger güçlü bir genel kural kurar ama büyük sanatın bazen bu kuralı çatlatabildiğini de söyler. Ressam sipariş verenin statüsünü göstermek zorunda olsa bile yüzün yalnızlığını, bedenin kırılganlığını veya mülkün yapaylığını görünür kılabilir.",
            "Bir portrenin resmi pozu ile gözlerdeki tereddüt çatışabilir. Tablo sahibin istediği anıt olmaktan çıkar, yaşayan insanın zaman içindeki geçiciliğini hissettirebilir. Sanat geleneğin dilini kullanıp onun aleyhine konuşabilir.",
            "Bu nedenle Berger'in tezini kalıp gibi kullanmak doğru değildir. 'Yağlıboya eşittir mülkiyet' deyip bakmayı bırakırsak, onun eleştirdiği hazır cevabı biz üretiriz.",
            "İyi eleştiri eserin fazlasını görür. Ekonomik koşulu, cinsiyet düzenini ve tekil sanatçının bu düzenle kavgasını birlikte taşır. Birini seçip ötekileri yok etmez.",
            "Akılda kalan görüntü, kusursuz duvardaki ince çatlağın içinden görünen insandır. Kural vardır; eser bazen kuralın yetmediğini gösterir.",
        ], "ÜÇÜNCÜ KISIM · MÜLKİYET VE YAĞLIBOYA", art="tradition-crack", caption="Bazı eserler geleneğin statü dilini kullanırken insanın kırılganlığını göstererek o dilin içinde çatlak açar."),
        entry("Reklam ürünü değil, gelecekteki seni satar", [
            "Bir parfüm reklamı kokuyu ekrandan veremez. Bunun yerine parfümü kullandıktan sonra olacağınız kişiyi gösterir: Daha arzulanır, daha özgür, daha ayrıcalıklı. Ürün, gelecekteki benliğe geçiş bileti gibi sunulur.",
            "Berger reklamın bugünkü kişiye eksiklik hissettirdiğini söyler. Şu anki hâlin yeterli değildir; satın alırsan başkalarının kıskanacağı bir görüntüye dönüşebilirsin. Reklam sizin kıskançlığınızı değil, gelecekte size duyulacak hayalî kıskançlığı satar.",
            "Bu vaat sürekli ertelenir. Ürün alındığında kısa heyecan gelir, sonra yeni eksiklik belirir. Sistem tatmin olmanızı değil, arzu etmeye devam etmenizi ister.",
            "Her reklam şeytani plan değildir. Ürün hakkında bilgi de verebilir. Berger'in hedefi tek ilan değil, hayatı tüketimle tamamlanacak eksiklik olarak kuran toplam görsel çevredir.",
            "Bir reklam gördüğünüzde ürünü elinizle kapatın. Geriye kalan beden, mekân ve bakış nasıl bir hayat vaat ediyor? Asıl satış çoğu zaman oradadır.",
        ], "DÖRDÜNCÜ KISIM · REKLAM VE BUGÜN", art="future-self", caption="Reklam çoğu kez üründen önce, ürünü alınca başkalarının kıskanacağı gelecekteki benliği satar."),
        entry("Reklam neden eski tabloları taklit eder?", [
            "Lüks saat reklamındaki sütun, kadife, meyve veya mitolojik poz tesadüf olmayabilir. Reklam, yağlıboya geleneğinin zenginlik ve kültür işaretlerini ödünç alır. Ürün yalnız pahalı değil, tarihsel otoriteye bağlı görünür.",
            "Yağlıboya tablo sahibinin elindekini kutlarken reklam henüz sahip olmadığınızı hatırlatır. Biri mevcut servetin, diğeri gelecekte satın alınacak dönüşümün dilidir. Yine de ikisi nesne ile statü arasında köprü kurar.",
            "Bugün spor ayakkabı reklamı klasik kahraman pozunu, otomobil reklamı fethedilecek manzarayı, kozmetik reklamı geleneksel nü bakışını kullanabilir. Görsel alıntı, kelimesiz kültürel prestij taşır.",
            "Bu dili fark etmek reklamdan etkilenmeyeceğimiz anlamına gelmez. Bilmek bağışıklık değil, kısa bir mesafe sağlar. Arzu hâlâ gerçek olabilir; en azından arzunun nasıl düzenlendiğini görürüz.",
            "Görsel hafıza büyük bir depodur. Reklam yeni görünmek için eski sembolleri tekrar tekrar paketler.",
        ], "DÖRDÜNCÜ KISIM · REKLAM VE BUGÜN", art="ad-old-master", caption="Modern reklam, eski yağlıboyanın zenginlik, kahramanlık ve güzellik işaretlerini yeni ürüne aktarabilir."),
        entry("Felaket haberinin yanında parlayan saat", [
            "Dergi sayfasında savaş haberiyle lüks saat reklamı yan yana gelebilir. Haber dünyanın acil ve ortak gerçeğini gösterir; reklam özel geleceğinizin parlaklığını vaat eder. Göz aynı saniyede iki ahlaki evrene girer.",
            "Reklam çevresindeki felaketi içine almaz. Ürün dünyayı değiştirmeyecek, yalnız sizin görüntünüzü değiştirecektir. Bu nedenle reklamın dünyası sürekli, pürüzsüz ve tarihsiz görünür.",
            "Bugünkü akışta deprem videosunun altında tatil önerisi, protestonun yanında cilt ürünü çıkabilir. Algoritma etik montaj yapmaz; dikkat ve gelir ölçüsüne göre içerikleri dizer. Yine de yan yanalık bizde tuhaf bir duygu bırakır.",
            "Kullanıcı bu çelişkiye alıştıkça felaket de reklam kadar kaydırılabilir bir içerik olur. Berger'in eski dergi gözlemi, telefon ekranında daha hızlı ve kişisel hâle gelmiştir.",
            "Bir sonraki akışta yalnız tek görsele değil, komşularına da bakın. Anlam çoğu kez iki içerik arasındaki dikişte belirir.",
        ], "DÖRDÜNCÜ KISIM · REKLAM VE BUGÜN", art="news-and-ad", caption="Felaket haberi ile lüks reklamın yan yanalığı, ortak dünya ile özel tüketim vaadini aynı ekranda çarpıştırır."),
        entry("Sosyal medya: Hem tablo sahibi hem reklam modeli", [
            "Sosyal medyada kişi kendi hayatının ressamı, galericisi, modeli ve izleyicisidir. Masadaki kahveyi, tatili ve bedeni seçip çerçeveler. Sonra başkalarının bakışını sayılarla ölçer. Berger'in bakış ve mülkiyet soruları tek cihazda birleşir.",
            "Paylaşmak yalnız gösteriş değildir. Bağ kurma, hatıra saklama, iş üretme ve topluluk bulma imkânı sunar. Ancak platform görünürlüğü belirli pozları ve hayat biçimlerini ödüllendirdiğinde kullanıcı kendi üzerinde reklam ajansı gibi çalışabilir.",
            "Etkileyici, ürünü kullanmakla kalmaz; ürünle tamamlanmış gelecekteki benliğin canlı kanıtı gibi sunulur. Reklam ile kişisel hayat arasındaki sınır incelir. Samimiyet de satılabilir bir stile dönüşür.",
            "Yapay zekâ görüntüleri bu düzeni daha da karıştırır. Hiç yaşanmamış lüks mekân, kusursuz yüz ve sahte tarihsel fotoğraf gerçek bakış alışkanlıklarımızı kullanır. Kaynak sorusu görsel estetik kadar önemli olur.",
            "Berger bugün yaşasaydı belki ilk sorusu yine aynı olurdu: Bu görüntü neyi gösteriyor değil, nasıl bir bakış ve ilişki kuruyor?",
        ], "DÖRDÜNCÜ KISIM · REKLAM VE BUGÜN", art="social-media-gallery", caption="Sosyal medyada kişi kendi hayatının ressamı, modeli, galericisi ve ölçülen izleyicisi hâline gelebilir."),
        entry("Berger'in güçlü yanı ve eksik bıraktığı yerler", [
            "Görme Biçimleri sanat konuşmasını müze uzmanının tekelinden çıkarır. Sınıf, cinsiyet, mülkiyet ve reklamı aynı görsel dil içinde düşündürür. İnce bir kitapla gündelik bakışı kalıcı biçimde değiştirir.",
            "Gücü aynı zamanda riskidir. Geniş tarihsel geleneği birkaç büyük açıklamayla okur. Her yağlıboya mülkiyet kutlaması, her kadın imgesi aynı bakış düzeni, her izleyici pasif değildir. Tekil eser ve izleyici farklı yollar açabilir.",
            "Kitabın kadın-erkek dili bugünün queer, trans ve farklı bakış deneyimlerini kapsamaya yetmez. Ayrıca Batı Avrupa geleneği merkezde olduğu için başka görsel kültürlerin ayrı tarihleri geri planda kalır.",
            "Bunlar kitabı geçersiz yapmaz; araçlarının nerede dikkatle kullanılacağını gösterir. Berger bize yeni bir gözlük verir. Her manzarayı aynı renge boyamamak için zaman zaman gözlüğü çıkarıp başka araçlarla bakmak gerekir.",
            "En iyi okur, Berger'in sonucunu ezberleyen değil, onun sorusunu yeni görüntüye taşıyandır.",
        ], "DÖRDÜNCÜ KISIM · REKLAM VE BUGÜN", art="critical-lens", caption="Berger güçlü bir eleştirel gözlük verir; onu bütün eserleri tek renge boyayan kalıba çevirmemek gerekir."),
        entry("Bir görüntüyü okumak için altı soru", [
            "Önce ne görüyorum? Yorum yapmadan bedenleri, nesneleri, ışığı ve mekânı sayın. Sonra çerçeveyi sorun: Ne kesilmiş, kamera nerede, hangi ayrıntı büyütülmüş?",
            "Üçüncü soru bakışadır: Kim kime bakıyor, kim izleyiciye dönüyor, kim bakılan ama konuşamayan kişi? Dördüncü soru sahipliğe gider: Hangi nesne, arazi veya beden ele geçirilebilir gibi gösteriliyor?",
            "Beşinci soru zamandır: Görüntü bugünü mü anlatıyor, geçmişin otoritesini mi çağırıyor, gelecekteki beni mi vaat ediyor? Altıncı soru dolaşımdır: Bu görüntüyü nerede, hangi başlıkla ve hangi komşu içeriklerin yanında görüyorum?",
            "Bu sorular tek doğru cevap makinesi değildir. Bakışı yavaşlatır. Bir reklamı satın almayacağınızı kanıtlamaz; neden arzuladığınızı daha açık görmenize yardım eder.",
            "Sonunda tekrar ilk soruya dönün. Aynı görüntüye şimdi baktığınızda ilk on saniyede görmediğiniz ne görünür oldu? Görme biçimi değiştiğinde görüntü yerinde dursa bile dünya biraz değişir.",
        ], "SONUÇ", art="six-questions", caption="Çerçeve, bakış, sahiplik, zaman ve dolaşım soruları görüntünün sessiz düzenini görünür kılar."),
        entry("Bir dakikalık harita", [
            "Görmek kelimeden önce gelir ama bilgi ve inanç neyi gördüğümüzü etkiler. Fotoğraf ve kamera eseri çoğaltırken bağlamını, ölçeğini ve izlenme sırasını değiştirir. Uzmanlık görüntüyü açabilir veya gizemleştirip izleyiciden uzaklaştırabilir.",
            "Batı görsel geleneğinde kadın sıkça görünmeyen erkek izleyici için seyir nesnesi yapılır. Yağlıboya, nesne ve arazinin sahipliğini dokunulabilir yüzeylerle kutlayabilir. Modern reklam bu dili kullanıp gelecekteki kıskanılan benliği satar.",
            "Bugün sosyal medya aynı bakışları kişisel hesaba taşır. Berger'in kalıcı sorusu şudur: Görüntü yalnız ne gösteriyor değil; kime, hangi güç ilişkisi içinde, nasıl bakmayı öğretiyor?",
        ], "SONUÇ"),
        entry("Akılda kalacak beş görüntü", [
            "Ekrana sığan dev tablo: Yeniden üretim bağlamı değiştirir. Resmin içinde yürüyen kamera: Kırpma yeni hikâye kurar. Kadının elindeki ayna: Dış bakış içeride nöbet tutar. Parlayan kadife ve arazi: Yağlıboya sahipliği konuşur. Felaket yanındaki saat reklamı: İki dünya aynı sayfada çarpışır.",
            "Bu beş görüntüyü hatırladığınızda sanat uzmanı olmanız gerekmez. Bir fotoğrafa biraz daha yavaş, reklamın vaadine biraz daha mesafeli ve kendi bakışınıza biraz daha meraklı olursunuz.",
            "Görmek doğal bir yetidir; nasıl baktığımız ise tarih, arzu ve güç tarafından eğitilir. İyi haber şu: Eğitilmiş bakış yeniden eğitilebilir.",
        ], "SONUÇ"),
    ],
})


BOOKS.append({
    "bookNo": 287,
    "title": "Aydınlanma Şimdi",
    "author": "Steven Pinker",
    "subtitle": "Manşetlerin karanlığı ile uzun dönemli verileri karşılaştıran; ilerlemeyi kutlarken kör noktalarını da açıkça gösteren sade ve eleştirel rehber.",
    "coverImage": "/images/optimized/summary-art-287-aydinlanma-simdi-v2-960.webp",
    "coverStyle": "artwork",
    "pdfUrl": "/data/pdfs/287-aydinlanma-simdi-ozeti.pdf",
    "pdfLabel": "25–50 sayfalık PDF'yi indir",
    "longForm": True,
    "chapterArtStyle": "monochrome-engraving",
    "chapterArtColor": "#976037",
    "meta": {
        "originalTitle": "Enlightenment Now: The Case for Reason, Science, Humanism, and Progress",
        "compiler": "Zihin Gezgini · Yapay zekâ destekli çalışma",
        "date": "Temmuz 2026",
        "language": "Türkçe",
    },
    "intro": "Steven Pinker kötü haberleri inkâr etmiyor; ölçeği değiştirmeyi öneriyor. Bugünün manşetini yüzyıllık grafikle yan yana koyduğumuzda insan ömrü, çocuk ölümü, aşırı yoksulluk, eğitim ve birçok güvenlik ölçüsünde büyük ilerleme görürüz. Kitabın cesur iddiası, bu ilerlemenin kendiliğinden değil akıl, bilim, hümanizm ve sorun çözme kurumları sayesinde geldiğidir. Bu rehber yetmiş beş grafiğin arkasındaki hikâyeyi gündelik örneklerle anlatır. Aynı zamanda seçilen göstergenin, başlangıç tarihinin ve ortalamanın kimi görünmez bırakabileceğini sorar. İyimserlik yerine koşullu umut sunar: İşe yarayanı gör, bedeli saklama, ilerlemeyi garanti sanma.",
    "sources": [
        {"id": 1, "title": "Penguin Random House – Enlightenment Now", "url": "https://www.penguinrandomhouse.com/books/317051/enlightenment-now-by-steven-pinker/"},
        {"id": 2, "title": "Google Books – bölüm ve grafik görünümü", "url": "https://books.google.com/books/about/Enlightenment_Now.html?id=J6grDwAAQBAJ"},
        {"id": 3, "title": "Our World in Data – küresel gelişme verileri", "url": "https://ourworldindata.org/"},
        {"id": 4, "title": "UNDP Human Development Reports", "url": "https://hdr.undp.org/"},
        {"id": 5, "title": "IPCC – iklim değerlendirme raporları", "url": "https://www.ipcc.ch/assessment-report/ar6/"},
        {"id": 6, "title": "World Bank – yoksulluk ve eşitsizlik verileri", "url": "https://www.worldbank.org/en/topic/poverty"},
    ],
    "entries": [
        entry("Bu kitap iyimserlik hapı mı?", [
            "Pinker'in kitabı 'Her şey harika' demez. Ana sorusu daha ölçülüdür: İnsanların iyi yaşamasını sağlayan göstergeler uzun dönemde hangi yönde değişti ve hangi fikirlerle kurumlar bu değişime katkı verdi?",
            "Bir grafiğin yükselmesi odadaki acıyı susturmaz. Dünya ortalaması iyileşirken belirli ülke, sınıf veya kuşak gerileyebilir. Bu özet her başarı bölümünde üç pencere açacak: Genel eğilim, gündelik anlam ve görünmeyen bedel.",
            "İlerleme bir doğa yasası değildir. Salgın, savaş, otoriterleşme ve iklim krizi kazanımları geri çevirebilir. Kitabın en yararlı biçimi zafer marşı değil, hangi yöntemlerin işe yaradığını gösteren bakım kılavuzudur.",
        ], "BAŞLANGIÇ"),
        entry("Dört ayaklı masa: Akıl, bilim, hümanizm, ilerleme", [
            "Pinker Aydınlanma'yı tek filozofun veya tek ülkenin malı değil, dört fikir ailesi olarak anlatır. Akıl, iddiayı gelenek ve otorite yerine gerekçeyle sınar. Bilim, dünyaya bakıp yanılgıyı ölçer. Hümanizm, insan ve duyarlı canlıların iyiliğini amaç yapar. İlerleme, sorunların çözülebileceğini kabul eder.",
            "Dört ayaktan biri eksikse masa sallanır. Akıl amaç vermeden yalnız araç hesaplayabilir. Hümanizm olmadan bilim daha etkili silah üretmeye hizmet edebilir. Bilim olmadan iyi niyet etkisiz hatta zararlı politika kurabilir.",
            "İlerleme inanç değildir; karşılaştırma iddiasıdır. Bebeklerin daha az ölmesi, insanların daha uzun yaşaması veya şiddetin azalması ölçülebilir. 'Geçmiş daha iyiydi' nostaljisi de 'gelecek kesin parlak' heyecanı da veriye çağrılır.",
            "Bu fikirler Avrupa Aydınlanması içinde güçlenmiştir ama akıl, merhamet ve gözleme dayalı düşünme yalnız Avrupa'ya ait değildir. Kitabın Batı merkezli anlatısı, başka kültürlerin katkılarını daha az görünür kılabilir.",
            "Akılda kalacak masa şudur: İyi amaç, güvenilir bilgi, açık gerekçe ve düzeltilebilir kurum aynı yüzeyi taşır.",
        ], "BİRİNCİ KISIM · AYDINLANMA FİKRİ", art="four-legged-table", caption="Akıl, bilim, hümanizm ve ilerleme fikri birlikte durduğunda sorun çözme masası dengelenir."),
        entry("Evren bize yardım etmiyor: Entropi, evrim ve bilgi", [
            "Pinker neden ilerlemenin otomatik olmadığını üç fikirle açıklar. Entropi, düzenin kendiliğinden dağılma eğilimini hatırlatır. Ev temizlenmezse tozlanır; köprü bakılmazsa aşınır; kurum denetlenmezse bozulabilir.",
            "Evrim bizi mutlu etmek için tasarlanmamıştır. Hayatta kalmaya ve üremeye yarayan dürtüler bırakmıştır; bunlar işbirliği kadar kıskançlık, grupçuluk ve saldırganlık da üretebilir. Doğal olan her şey iyi değildir.",
            "Bilgi, enerjiyi hedefli kullanıp düzene dönüştürmemizi sağlar. Aşı tarifi, kanalizasyon planı veya deprem yönetmeliği maddi dünyada fark yaratır. Bilgi kopyalanabilir; bir çözüm başka yerde yeniden kullanılabilir.",
            "Bu üçlü kadercilik değildir. Evrenin bize ücretsiz düzen vermediğini, iyiliğin bakım ve öğrenme istediğini söyler. İlerleme, yokuş aşağı yuvarlanmak değil, sürekli pedal çevirmektir.",
            "Gündelik görüntü bakımsız bisiklettir. Sürmeyi bırakınca yalnız durmaz; paslanır. Toplumsal kazanımlar da bakım görmezse gerileyebilir.",
        ], "BİRİNCİ KISIM · AYDINLANMA FİKRİ", art="entropy-bicycle", caption="Düzen kendiliğinden korunmaz; bilgi ve bakım kesildiğinde bisiklet gibi kurumlar da paslanır."),
        entry("Neden dünya kötüleşiyor gibi hissediyoruz?", [
            "Haber, sıradan biçimde çalışan milyonlarca olayı değil, yeni ve çarpıcı sapmayı seçer. Dün milyonlarca uçak güvenle indi cümlesi haber değildir; tek kaza bütün ekranı kaplar. Zihin bu seçilmiş örneklerden dünyanın tamamı hakkında hüküm verir.",
            "Yakınlık ve canlı görüntü riski büyütür. Uzak ülkedeki saldırıyı anında görürüz; geçen yüzyıldaki yüksek günlük şiddeti aynı duyguyla yaşamayız. Geçmiş istatistik, bugün video olarak gelir.",
            "Kötü haber yanlılığı gerçek sorunu icat etmez. Savaş ve afet vardır. Yanlılık, sıklığını ve yönünü sezgisel olarak yanlış tahmin etmemize yol açabilir. Manşet durumun fotoğrafı, uzun seri filmin gidişidir.",
            "Pinker ilerleme korkusu veya 'progressophobia' dediği tavrı eleştirir. Fakat eleştiren herkes veriye düşman değildir; ortalamanın eşitsizliği gizlediğini veya seçilen başlangıç tarihinin sonucu değiştirdiğini haklı olarak sorabilir.",
            "En iyi alışkanlık iki ekran açmaktır: Bugünün acil haberi ve uzun dönemli eğilim. Biri olmadan kayıtsız, öteki olmadan umutsuz olabiliriz.",
        ], "BİRİNCİ KISIM · AYDINLANMA FİKRİ", art="headline-graph", caption="Manşet tek çarpıcı olayı, uzun dönemli grafik ise olayların yıllar içindeki yönünü gösterir."),
        entry("Hayat ve sağlık: Doğum günü neden tarihsel başarıdır?", [
            "Geçmişte çok sayıda çocuk beşinci yaşını göremiyordu. Temiz su, kanalizasyon, aşılama, doğum bakımı, antibiyotik ve daha iyi beslenme bu riski büyük ölçüde azalttı. Ortalama ömrün uzaması yalnız yaşlıların daha çok yaşaması değil, erken ölümlerin azalmasıdır.",
            "Birinci yaş günündeki mum bugün sıradan görünür. Tarihsel açıdan bu sıradanlık dev başarıdır. Aileler çocuklarının yaşamasını daha çok bekleyebilir, kadınlar doğumda daha az ölür, enfeksiyonlar kader olmaktan uzaklaşır.",
            "Sağlık ilerlemesi tek bir dâhinin buluşu değildir. Laboratuvar bilgisi, hemşirelik, kamu altyapısı, eğitim, dağıtım ve güven birlikte çalışır. Aşının bulunması ile her köye ulaşması ayrı başarıdır.",
            "Ortalama yükselirken eşitsizlik sürebilir. Yoksul mahalle, savaş bölgesi veya ayrımcılığa uğrayan grup aynı kazanımı yaşamayabilir. Ayrıca uzun yaşam, kronik hastalık ve bakım ihtiyacını yeni toplumsal görevlere dönüştürür.",
            "Pinker'in güçlü noktası, sağlık mucizesini görünür kılmasıdır. Kör noktası, bu mucizenin siyasal mücadele, kamu yatırımı ve eşit erişim gerektirdiğini zaman zaman hızlı geçmesidir.",
        ], "İKİNCİ KISIM · İLERLEMEYİ ÖLÇMEK", art="birthday-candle", caption="Bugün sıradan görünen birinci yaş günü, çocuk ölümlerinin azalmasıyla mümkün olan büyük tarihsel başarıdır."),
        entry("Dolu tabak ve kalabalık şehir", [
            "Kıtlık insanlık tarihinde sık tekrarlandı. Tarım verimi, gübre, sulama, ulaşım, soğuk zincir ve ticaret daha fazla insanın beslenmesini mümkün kıldı. Gıda yalnız tarlada üretilmez; bozulmadan doğru yere ulaşması gerekir.",
            "Pinker nüfus artarken kişi başına düşen gıdanın da artabildiğini vurgular. Bu, kaynakların sihirli biçimde sınırsız olduğu anlamına gelmez. Bilgi ve kurum, aynı toprak ve emekten daha çok ürün çıkarabilir.",
            "Dolu market rafı dağıtım adaletini kanıtlamaz. İnsanlar yiyecek bulunan şehirde parasızlık, savaş veya siyasi engel yüzünden aç kalabilir. Açlık çoğu zaman yalnız üretim değil erişim ve iktidar sorunudur.",
            "Tarım başarısının çevresel bedeli de vardır: Toprak kaybı, su kullanımı, gübre kirliliği ve biyolojik çeşitlilik baskısı. İlerlemeyi sürdürmek, aynı başarıyı daha az zarar ile üretmek demektir.",
            "Bir somun ekmeği yalnız fırıncının işi olarak değil, tohum, çiftçi, yol, enerji, bilgi ve barış zinciri olarak görün. Zincirin her halkası ilerlemenin bakım ister hâlidir.",
        ], "İKİNCİ KISIM · İLERLEMEYİ ÖLÇMEK", art="food-chain", caption="Dolu tabak; tarım bilgisi, ulaşım, enerji, ticaret ve erişim kurumlarının birlikte kurduğu zincirdir."),
        entry("Zenginlik ile eşitsizlik aynı grafik değil", [
            "Bir köyde herkesin geliri iki katına çıkabilir ama en zenginin geliri on kat artarsa yoksulluk azalırken eşitsizlik büyüyebilir. Bu iki cümle aynı anda doğru olabilir. Tartışmanın karışması, farklı grafikleri tek kelimeyle anlatmaktan doğar.",
            "Pinker mutlak yoksulluğun azalmasına ve dünya gelirinin uzun dönemde büyümesine dikkat çeker. Elektrik, ulaşım, dayanıklı ev eşyası ve iletişim daha çok insana ulaşmıştır. Maddi rahatlık yalnız lüks değil, zamandan ve bedensel emekten tasarruftur.",
            "Eşitsizliğin neden önemsendiğini de küçümsememek gerekir. Para siyasal güç, eğitim, güvenli mahalle ve uzun yaşam satın alabiliyorsa dağılım yalnız kıskançlık değildir. Ortalama gelir artarken fırsat uçurumu toplumu bölebilir.",
            "Aşırı yoksulluk ölçümünde kullanılan eşik, fiyat hesabı ve veri kalitesi tartışılabilir. Bir eşiğin üstüne çıkmak rahat yaşam anlamına gelmez. Grafiğin başarısını kutlarken çizginin hemen üstündeki kırılganlığı görmek gerekir.",
            "Dengeli soru şudur: Pasta büyüdü mü, en alttakinin dilimi gerçekten büyüdü mü, karar masasına kim oturabiliyor? Üçü ayrı ölçüdür.",
        ], "İKİNCİ KISIM · İLERLEMEYİ ÖLÇMEK", art="wealth-inequality", caption="Yoksulluğun azalması, toplam zenginliğin artması ve eşitsizliğin değişmesi üç ayrı grafikte izlenmelidir."),
        entry("Çevre: Zenginleşince kendiliğinden temizlenir mi?", [
            "Pinker bazı kirlilik türlerinin toplum zenginleştikçe ve düzenleme yaptıkça azalabildiğini gösterir. Şehir havası, nehir kirliliği ve orman korumasında politika ile teknoloji gerçek iyileşmeler yaratmıştır. Çevre felaketi kaçınılmaz kader değildir.",
            "Fakat 'önce kirlet, sonra temizlersin' güvenli reçete değildir. İklim değişikliği, tür kaybı ve geri döndürülemez ekosistem çöküşleri yerel dumandan farklıdır. Zararın bir kısmı zengin ülke tüketimi için başka bölgeye taşınabilir.",
            "Pinker nükleer enerji ve teknolojik yeniliği iklim çözümünde önemli görür. Bu araçlar ciddi seçeneklerdir; enerji verimliliği, yenilenebilir kaynak, şebeke, talep değişimi ve adil geçişle birlikte değerlendirilmelidir.",
            "İlerleme anlatısı burada en sıkı sınavını verir. Geçmişte çözdüğümüz sorunlar gelecektekini otomatik çözmez. Fakat çözüm üretme kapasitesini görmek, felç edici kıyamet dili yerine ölçülebilir hedef kurmaya yardım edebilir.",
            "İyi çevre umudu, doğanın kendini toparlayacağına güvenmek değil; fiziksel sınırları kabul edip kurum ve teknolojiyi hızlıca değiştirmektir.",
        ], "İKİNCİ KISIM · İLERLEMEYİ ÖLÇMEK", art="environment-repair", caption="Bazı çevre sorunları politika ve teknolojiyle azalabilir; iklim ve tür kaybı geri döndürülemez sınırlar nedeniyle daha acildir."),
        entry("Barış: Savaş görüntüleri artarken savaş azalabilir mi?", [
            "Her savaş görüntüsü korkunçtur. Pinker uzun tarihsel serilerde devletler arası savaş ve savaşta ölüm oranlarının bazı dönemlerde belirgin biçimde azaldığını savunur. Bu, savaşın bittiği veya eğilimin geri dönemeyeceği anlamına gelmez.",
            "Oran ile toplam sayı ayrımı önemlidir. Dünya nüfusu büyürken mutlak ölüm ve nüfusa oran farklı hikâye anlatabilir. Başlangıç yılı da sonucu değiştirir; özellikle büyük savaşların hemen sonundan başlamak düşüşü dramatikleştirebilir.",
            "Barış yalnız iyi niyetle kurulmaz. Ticaret, uluslararası kurumlar, demokratik denetim, caydırıcılık, insan hakları normları ve savaşın maliyetini görünür kılan iletişim birlikte etkili olabilir. Hangisinin ne kadar etkili olduğu tartışmalıdır.",
            "Sömürge şiddeti, iç savaş, devlet baskısı ve yerinden edilme yalnız devletler arası savaş sayısına bakınca kaybolabilir. Geniş güvenlik resmi farklı şiddet türlerini ayrı ayrı ölçmelidir.",
            "Dengeli sonuç: İnsanlık savaşmaya mahkûm değildir; barış da kendi kendine duran sessizlik değildir. Her kuşak kurumları yeniden işletir.",
        ], "İKİNCİ KISIM · İLERLEMEYİ ÖLÇMEK", art="war-and-trend", caption="Tek savaşın dehşeti ile uzun dönemli savaş eğilimi aynı anda görülmeli; biri ötekini susturmamalıdır."),
        entry("Güvenlik: Günlük hayatın görünmez mühendisliği", [
            "Trafik kazası, işyeri ölümü, yangın ve zehirlenme geçmişte daha sık kader sayılırdı. Emniyet kemeri, hız sınırı, çocuk koltuğu, bina yönetmeliği ve ürün standardı gündelik hayatı daha güvenli hâle getirdi.",
            "Bu başarılar sıkıcıdır çünkü gerçekleşmeyen olay görünmez. Sağlam korkuluk yüzünden düşmeyen kişi haber olmaz. Pinker'in grafikleri görünmez önlemlerin toplam etkisini gösterir.",
            "Terör saldırıları ise nadir olsa bile kasıtlı, dramatik ve sembolik oldukları için risk algısını büyütür. İnsan uçaktan korkup daha tehlikeli kara yoluna yönelebilir. Duygusal korku ile istatistiksel risk farklı davranır.",
            "Risk oranı düşük demek mağdurun acısını küçültmez. Politika, korkuya kapılmadan gerçek tehdidi azaltmalı; aşırı tepkiyle hakları ve başka güvenlik alanlarını zedelememelidir.",
            "Güvenlik ilerlemesinin sırrı kahramanlık değil, ayrıntıdır. Bir vida standardı, net etiket ve bağımsız denetim binlerce hayatın görünmez koruyucusu olabilir.",
        ], "İKİNCİ KISIM · İLERLEMEYİ ÖLÇMEK", art="safety-engineering", caption="Yönetmelik, emniyet kemeri ve denetim gibi sıkıcı ayrıntılar gerçekleşmeyen kazaların görünmez mühendisliğini kurar."),
        entry("Demokrasi ve eşit haklar: Kâğıttaki yasa neden yetmez?", [
            "Daha çok insanın oy hakkı kazanması, köleliğin hukuken kaldırılması, kadın ve azınlık haklarının genişlemesi büyük tarihsel değişimlerdir. Pinker bunları hümanist çemberin genişlemesi olarak okur: Başkasının acısı daha çok insan için ahlaki mesele olur.",
            "Yasa değişikliği vazgeçilmezdir ama gündelik uygulama hemen değişmeyebilir. Oy hakkı kâğıtta varken sandığa erişim engellenebilir; ayrımcılık yasaklanırken işe alım ve konut piyasasında sürebilir.",
            "İlerleme çoğu kez kendiliğinden akıl zaferi değil, dışlanan insanların örgütlü mücadelesiyle gelir. Kitabın kurum ve fikir vurgusu, grev, protesto, sivil itaatsizlik ve bedel ödeyen hareketleri bazen arka plana iter.",
            "Demokrasi yalnız seçim sayısı değildir. Basın özgürlüğü, yargı bağımsızlığı, muhalefet hakkı, barışçıl iktidar değişimi ve azınlığın korunması birlikte gerekir. Sandık otoriterliği tek başına engellemez.",
            "İlerleme grafiğinin arkasında insanlar vardır. Çizgi yükseldiyse birileri 'Bu adaletsiz' deyip mevcut düzeni değiştirmek için risk almıştır.",
        ], "İKİNCİ KISIM · İLERLEMEYİ ÖLÇMEK", art="rights-expansion", caption="Hakların genişlemesi yalnız fikirlerin değil, dışlanan insanların örgütlü mücadelesi ve kurum değişiminin sonucudur."),
        entry("Bilgi ve yaşam kalitesi: Daha çok okul, daha çok boş zaman", [
            "Okuryazarlık ve eğitim dünya genelinde genişledi. İnsan yalnız kitap okumaz; ilaç etiketini, oy pusulasını, sözleşmeyi ve teknik kılavuzu da okuyabilir. Bilgi günlük bağımsızlığı artırır.",
            "Teknoloji ev işlerinin bir bölümünü hafifletti, ulaşımı hızlandırdı ve iletişimi ucuzlattı. Bir çamaşır makinesi felsefi görünmez ama özellikle ücretsiz ev emeği taşıyan kişinin saatlerini geri verebilir.",
            "Boş zamanın artması otomatik olarak iyi yaşam üretmez. Ekran ekonomisi dikkati parçalayabilir, güvencesiz iş çalışma saatini belirsizleştirebilir. Ortalama boş zaman, ikinci iş yapan veya bakım yükü taşıyan insanın deneyimini saklayabilir.",
            "Eğitim yılı artarken öğrenme kalitesi aynı kalmayabilir. Diploma, eleştirel düşünme ve temel beceri garantisi değildir. Pinker'in ilerleme çizgisi, içerik ve dağılım sorularıyla tamamlanmalıdır.",
            "Yine de büyük resmi küçümsememek gerekir. Daha fazla insan bilgiye ulaşabiliyor, kendi hayatı hakkında karar verebiliyor ve yalnız hayatta kalmanın ötesinde uğraşlara zaman ayırabiliyor.",
        ], "İKİNCİ KISIM · İLERLEMEYİ ÖLÇMEK", art="knowledge-free-time", caption="Okuryazarlık ve zaman kazandıran teknoloji, insanın yalnız hayatta kalmak yerine kendi kararlarına alan açabilir."),
        entry("Mutluluk neden ömür kadar net yükselmiyor?", [
            "İnsanlar daha uzun, sağlıklı ve zengin yaşarken mutluluk aynı hızda yükselmeyebilir. Çünkü zihin mutlak düzeye değil karşılaştırmaya ve beklentiye duyarlıdır. Dün lüks olan bugün normal olur; komşunun durumu yeni ölçüye dönüşür.",
            "Gelir yoksullukta büyük fark yaratır. Güvenli ev, yiyecek ve sağlık imkânı mutluluğu etkiler. Temel ihtiyaçlardan sonra ilişkinin, ruh sağlığının, güvenin ve anlamın payı büyür. Para önemsiz değildir; bütün hikâye de değildir.",
            "Pinker yalnızlık ve intihar gibi karanlık göstergeleri de tartışır. Burada veri tanımı ve ülke farkı çok önemlidir. Ruhsal acıyı tek bir uygarlık çizgisine indirgemek, kişinin ihtiyacını görünmez yapabilir.",
            "Modern özgürlük daha çok seçenek sunar; seçenek yükü ve başarısızlık hissi de yaratabilir. İnsan eski baskıdan kurtulurken yeni performans ölçülerine bağlanabilir.",
            "İlerleme, insanların sürekli neşeli olması değil; daha az önlenebilir acı, daha çok seçim ve iyi hayatı kurmak için daha geniş imkân demektir. O imkânın nasıl yaşandığı ayrı sorudur.",
        ], "İKİNCİ KISIM · İLERLEMEYİ ÖLÇMEK", art="happiness-gap", caption="Ömür, sağlık ve gelir artabilir; mutluluk karşılaştırma, ilişki ve anlam nedeniyle aynı düz çizgide ilerlemeyebilir."),
        entry("Büyük tehditler: Nükleer savaş, iklim ve yapay zekâ", [
            "İnsanlık kendi sonunu hazırlayabilecek güçler üretti. Nükleer silahlar kısa sürede yıkım, iklim değişikliği uzun vadeli sistemik risk, ileri teknoloji ise yeni belirsizlikler taşır. Pinker korkunun olasılık hesabını bozabileceğini söyler.",
            "Kıyamet kehaneti felç yaratabilir; 'nasıl olsa bitecek' duygusu çözüm emeğini azaltır. Öte yandan iyimserlik de rehavet yaratabilir. Düşük olasılıklı ama dev etkili risklerde ihtiyat ve kurum gerekir.",
            "İklim riski yalnız uzak ihtimal değildir; gözlenen ısınma ve etkiler gerçek, azaltım ihtiyacı acildir. Teknolojik çözüm umudu emisyon kesme sorumluluğunu ertelememelidir. Nükleer enerji tartışması da maliyet, güvenlik ve hızla birlikte yürütülmelidir.",
            "Yapay zekâ konusunda kitap, insan benzeri kötü niyet varsayımlarına kuşkuyla yaklaşır. Bugün daha somut riskler arasında ayrımcılık, dezenformasyon, iş gücü etkisi, gözetim ve güç yoğunlaşması vardır. Uzak senaryo ile mevcut zarar aynı sepette eritilmemelidir.",
            "Akıllı umut, tehlikeyi küçültmez. Riski bileşenlerine ayırır, olasılık ve etkiyi günceller, geri dönüşü zor alanlarda güvenlik payı bırakır.",
        ], "ÜÇÜNCÜ KISIM · AKIL, BİLİM, HÜMANİZM", art="existential-risks", caption="Büyük tehditlerde kıyamet felci ile rehavet arasında; olasılık, etki ve ihtiyatı birlikte taşıyan kurumlar gerekir."),
        entry("Akıl neden akıllı insanlarda bile tökezler?", [
            "Yüksek eğitim, insanı kendi grubunun hatalarından otomatik kurtarmaz. Zihin çoğu kez doğruyu bulmak için değil, ait olduğu grubun savunmasını yapmak için zekâ kullanır. Akıllı insan daha iyi gerekçe üretip daha ustaca yanılabilir.",
            "Doğrulama yanlılığı sevdiğimiz örnekleri toplar, ters örneği gözden kaçırır. Erişilebilirlik yanlılığı canlı olayı sık sanır. Grup kimliği, kanıtı takım formasına göre değerlendirir. Pinker bu kusurları aklı terk etmek için değil, kişisel sezginin üstüne yöntem kurmak için anlatır.",
            "Olasılık dili özellikle zordur. Testin yüzde doksan dokuz doğru olması, pozitif sonucun yüzde doksan dokuz ihtimalle hastalık demek olduğu anlamına gelmeyebilir; hastalığın toplumdaki sıklığı hesabı değiştirir.",
            "İyi kurumlar tartışma, veri, önceden belirlenmiş ölçüt, bağımsız kontrol ve hata kaydı kullanır. Bunlar insanı kusursuz yapmaz; yanılgının tek zihinde kilitli kalmasını önler.",
            "Akıl bir kişilik özelliği değil, pratik olabilir. 'Ben rasyonelim' demek yerine 'Fikrimi değiştirecek kanıt nedir?' diye sormak daha güvenilirdir.",
        ], "ÜÇÜNCÜ KISIM · AKIL, BİLİM, HÜMANİZM", art="reason-bias", caption="Zekâ yanılgıyı yok etmez; açık ölçüt ve bağımsız denetim aklı kişisel kimliğin dışına taşır."),
        entry("Bilim: Beyaz önlük değil, hata düzeltme düzeni", [
            "Pinker bilimi Aydınlanma'nın en güçlü motorlarından sayar. Bilim yalnız laboratuvar gerçeği değil; iddiayı dünyayla karşılaştırma, ölçme, tekrar etme ve eleştiriye açma alışkanlığıdır.",
            "Bilimsel sonuçlar değiştiğinde bazıları bunu zayıflık sayar. Oysa yeni veriyle değişmeyen sistem dogmadır. Düzeltme rahatsız edici olabilir; yöntemin çalıştığını da gösterebilir.",
            "Kurumlar kusursuz değildir. Yayın baskısı, çıkar çatışması, tekrarlanamayan sonuç ve eşitsiz kaynak dağılımı bilimi etkiler. Bilim savunusu, bilimin gerçek işleyişini eleştirmekten kaçmamalıdır.",
            "Pinker sosyal bilimlerde de veri ve nedensel düşünmenin önemini vurgular. İnsan değerini ölçüye indirgemeden, hangi politikanın gerçekten işe yaradığını sınamak mümkündür. İyi niyet sonuç yerine geçmez.",
            "Beyaz önlük çıkarıldığında geriye kalan şey, hatayı saklamak yerine bulmayı ödüllendiren düzen olmalıdır. Bilimin kamusal güveni buradan gelir.",
        ], "ÜÇÜNCÜ KISIM · AKIL, BİLİM, HÜMANİZM", art="science-correction", caption="Bilimin gücü değişmez görünmekte değil, hatayı bulup yeni kanıtla düzeltmeyi kurala bağlamaktadır."),
        entry("Hümanizm: Kutsal slogan değil, acıyı azaltma ölçüsü", [
            "Hümanizm Pinker için insanların refahını, özgürlüğünü ve acıdan korunmasını ahlaki merkeze alır. Bir politikanın görkemli ideale değil, duyarlı varlıkların hayatında ne yaptığına bakar.",
            "Bu ölçü dinî veya millî kimliği zorunlu olarak düşman saymaz. Kimlikler insanlara ilişki ve anlam verebilir. Sorun, soyut grubun şerefi gerçek insanın hayatından daha değerli sayıldığında başlar.",
            "Hümanist çember zamanla kadınları, farklı ırkları, çocukları, cinsel azınlıkları ve hayvan refahını daha çok kapsayabilir. Bu genişleme tamamlanmış değildir; hukuk ile gündelik saygı arasında boşluk kalır.",
            "Pinker'in evrensel insanlık vurgusu güçlüdür. Fakat evrensel dil, belirli grupların yaşadığı özgül tarih ve güç farklarını atlamamalıdır. Herkese aynı davranmak, başlangıç koşulları çok farklıysa adil sonuç vermeyebilir.",
            "Hümanizmi akılda tutmanın en sade yolu şudur: Kurumun, bayrağın veya teorinin arkasında yaşayan insanı yeniden görünür kılmak.",
        ], "ÜÇÜNCÜ KISIM · AKIL, BİLİM, HÜMANİZM", art="humanist-circle", caption="Hümanizm soyut ihtişam yerine gerçek insanların hayatını, özgürlüğünü ve önlenebilir acısını ölçü alır."),
        entry("Pinker nerede güçlü, nerede tartışmalı?", [
            "Kitabın en güçlü yanı, yalnız manşetle dünya görüşü kurmanın tehlikesini göstermesidir. Uzun dönemli veriler, insanlığın bazı büyük sorunları gerçekten azaltabildiğini ve kurumların fark yarattığını kanıtlar.",
            "Tartışma, hangi göstergenin ilerleme sayıldığı yerde başlar. Ortalama, dağılımı; gelir, ücretsiz bakım emeğini; devletler arası barış, sömürge ve iç şiddeti; uzun yaşam, yaşam kalitesini gizleyebilir. Grafik doğru olsa bile hikâye eksik olabilir.",
            "Pinker eleştirmenlerini zaman zaman akıl karşıtı karamsarlar gibi geniş bir torbaya koyar. Oysa veri seçimi, sömürge tarihi, ekolojik sınır ve eşitsizlik üzerine eleştiri Aydınlanma'nın kendi sorgulama ruhunun parçası olabilir.",
            "İlerlemeyi fikirlerin zaferi olarak anlatmak, sendikaları, kadın hareketini, sömürge karşıtı mücadeleyi ve kamusal yatırımı arka plana itebilir. Akıl ve bilim dünyayı kurumlar ve çatışmalar üzerinden değiştirir.",
            "En verimli okuma ne hayranlık ne reddiyedir. Kitabın grafiğini alın, eksenini kontrol edin, kimin görünmediğini sorun ve işe yarayan mekanizmayı koruyun.",
        ], "ÜÇÜNCÜ KISIM · AKIL, BİLİM, HÜMANİZM", art="critical-graph", caption="Doğru grafik bile seçilen gösterge, başlangıç tarihi ve ortalamanın gizlediği gruplar nedeniyle eksik hikâye anlatabilir."),
        entry("Koşullu umut için dört adım", [
            "Bir sorun seçin: Trafik ölümü, hava kirliliği, okul başarısı veya aile içi şiddet. Önce bugünkü duygunuza değil, güvenilir uzun seriye bakın. Sorun artıyor mu, azalıyor mu, kimlerde yoğunlaşıyor?",
            "İkinci adım işe yarayan mekanizmayı ayırmaktır. Yasa mı, teknoloji mi, eğitim mi, gelir desteği mi, davranış değişimi mi? 'İnsanlık ilerledi' cümlesi eylem vermez; hangi parçanın çalıştığını bilmek verir.",
            "Üçüncü adım bedeli ve dışarıda kalanı bulmaktır. Ortalama iyileşirken kim geride? Çözüm çevresel veya toplumsal başka zarar üretiyor mu? İlerlemeyi sürdürmek, kör noktayı düzeltmeyi içerir.",
            "Dördüncü adım kazanımı garanti sanmamaktır. Bütçe, denetim, eğitim ve demokratik destek kesilirse çizgi geri dönebilir. Başarı bakım ister.",
            "Bu dört adım iyimserlikten daha dayanıklıdır. Dünya iyi olacak diye inanmaz; insanların ne yaptığında bazı şeylerin gerçekten iyileştiğini araştırır.",
        ], "SONUÇ", art="conditional-hope", caption="Koşullu umut; eğilimi ölçer, çalışan mekanizmayı bulur, geride kalanı görür ve kazanımı bakım altında tutar."),
        entry("Bir dakikalık harita", [
            "Aydınlanma'nın dört fikri akıl, bilim, hümanizm ve ilerlemedir. Entropi düzenin bakım istediğini, evrim doğal olanın iyi olmadığını, bilgi ise sorun çözmenin çoğaltılabilir gücünü gösterir. Manşetler çarpıcı olayı seçtiği için uzun dönemli gelişmeyi kaçırabiliriz.",
            "Pinker ömür, sağlık, gıda, zenginlik, barış, güvenlik, haklar, eğitim ve yaşam kalitesinde büyük ilerlemeler gösterir. Her grafikte dağılımı, görünmeyen emeği, ekolojik bedeli ve seçilen başlangıç tarihini ayrıca sormak gerekir.",
            "İlerleme kaçınılmaz değildir. İnsanların bilgi, kurum, mücadele ve düzeltmeyle ürettiği kırılgan sonuçtur. En dengeli cümle: Dünya birçok ölçüde daha iyi oldu; bu, işimizin bittiği değil, bazı işlerin nasıl yapılabildiğini bildiğimiz anlamına gelir.",
        ], "SONUÇ"),
        entry("Akılda kalacak beş görüntü", [
            "Dört ayaklı masa: Akıl, bilim, hümanizm, ilerleme. Paslanan bisiklet: Kazanım bakım ister. Manşet ve grafik: Bugün ile uzun dönem farklı ölçeklerdir. Doğum günü mumu: Sıradan hayat tarihsel başarı olabilir. Büyüyen pasta ve farklı dilimler: Zenginlik ile eşitsizlik aynı ölçü değildir.",
            "Bu görüntüler kitabın yüzlerce sayfasını tek slogana indirmez; okurun doğru soruya daha hızlı ulaşmasını sağlar. İyimser misin kötümser misin yerine hangi gösterge, hangi dönem, kimin hayatı ve hangi mekanizma diye sorarsınız.",
            "Pinker'in bıraktığı en iyi rahatsızlık şudur: Umutsuzluk da kanıt istemeyen rahat bir inanç olabilir. Dünya değişebiliyorsa, hangi değişime emek vereceğimiz sorumluluğu bize geri döner.",
        ], "SONUÇ"),
    ],
})


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for source in BOOKS:
        summary = assemble(dict(source))
        target = OUT / f"{summary['bookNo']}.json"
        target.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{target.relative_to(ROOT)}: {len(summary['chapters'])} chapters, {len(summary['chapterArtworks'])} artworks")


if __name__ == "__main__":
    main()
