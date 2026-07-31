#!/usr/bin/env python3
"""Build five more long-form illustrated summary JSON files."""

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
    "bookNo": 7,
    "title": "Türlerin Kökeni",
    "author": "Charles Darwin",
    "subtitle": "Canlı çeşitliliğinin hazır bir vitrin değil, küçük farkların kuşaklar boyunca dallandığı uzun bir tarih olduğunu gündelik örneklerle anlatan rehber.",
    "coverImage": "/images/summary-art-7-turlerin-kokeni-v2.webp",
    "coverStyle": "artwork",
    "pdfUrl": "/data/pdfs/7-turlerin-kokeni-ozeti.pdf",
    "pdfLabel": "25-50 sayfalık PDF'yi indir",
    "longForm": True,
    "chapterArtStyle": "monochrome-engraving",
    "chapterArtColor": "#4F6B4C",
    "meta": {
        "originalTitle": "On the Origin of Species",
        "compiler": "Zihin Gezgini · Yapay zeka destekli çalışma",
        "date": "Temmuz 2026",
        "language": "Türkçe",
    },
    "intro": "Darwin okura tek bir sihirli cümle sunmaz. Güvercin yetiştiricilerinden adalara, fosillerden arı peteklerine kadar yüzlerce küçük gözlemi aynı masaya koyar ve büyük soruyu sorar: Türler neden birbirine hem benzer hem de farklıdır? Bu rehber kitabın kanıt yürüyüşünü koruyor, doğal seçilimi günlük örneklerle açıklıyor ve Darwin'in bilmediği genetik, mutasyon ve genetik sürüklenme gibi modern ekleri ayrı tutuyor. Amaç canlıları bir başarı merdivenine dizmek değil; her canlının geçmişten gelen, çevreyle sınanan ve akrabalarına bağlanan bir hikayesi olduğunu görmek. Sosyal Darwinizm ve ırkçı yanlış kullanımlar da bilimin kendisiyle karıştırılmadan ele alınıyor.",
    "sources": [
        {"id": 1, "title": "Darwin Online - Türlerin Kökeni birinci baskı ve bölüm içeriği", "url": "https://darwin-online.org.uk/content/contentblock?basepage=1&hitpage=102&itemID=F373&viewtype=side"},
        {"id": 2, "title": "Darwin Online - Birinci baskıya bölüm bölüm giriş", "url": "https://darwin-online.org.uk/EditorialIntroductions/Chancellor_vanWyhe_Origin1st.html"},
        {"id": 3, "title": "Nature Education - Türleşme ve modern sentez", "url": "https://www.nature.com/scitable/knowledge/library/speciation-the-origin-of-new-species-26230527/"},
        {"id": 4, "title": "National Academies - Evrimin kanıtları ve DNA", "url": "https://nap.nationalacademies.org/resource/11876/Evolution%20Brochure.pdf"},
        {"id": 5, "title": "Genetics and the Origin of Species - Darwin'den modern genetiğe", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC33678/"},
    ],
    "entries": [
        entry("Bu kitap nasıl okunmalı?", [
            "Türlerin Kökeni hızlı sonuç veren modern bir popüler bilim kitabı değildir. Darwin aynı fikri farklı hayvanlar, bitkiler ve coğrafyalar üzerinden tekrar tekrar sınar. Bu yüzden her ayrıntıyı ezberlemek yerine kanıt zincirini izlemek daha yararlıdır.",
            "Kitabın merkezinde üç basit parça vardır: Bireyler birbirinden farklıdır, bu farkların bir bölümü aktarılabilir ve her doğan canlı yaşamını sürdürüp yavru bırakamaz. Bu üç parça birleştiğinde popülasyon kuşaklar boyunca değişebilir.",
            "Darwin DNA'yı, genleri ve mutasyonun moleküler kaynağını bilmiyordu. Modern biyoloji onun ana fikrini genetikle güçlendirdi, bazı ayrıntıları düzeltti ve doğal seçilimin yanına sürüklenme ile gen akışı gibi başka süreçler ekledi. Özet boyunca eski kitap ile bugünkü bilgi ayrı raflarda tutulacak.",
        ], "BAŞLANGIÇ"),
        entry("Güvercinlikte başlayan büyük soru", [
            "Darwin doğaya çıkmadan önce insanın seçtiği hayvanlara bakar. Bir güvercin yetiştiricisi daha geniş kuyruklu kuşları çiftleştirir, başka biri hızlı uçanları seçer. Kuşaklar geçtikçe aynı atadan çok farklı görünen ırklar ortaya çıkar. İnsan yeni özelliği yaratmaz; var olan farklar arasından seçim yapar.",
            "Bunu bir çekmecedeki renkli düğmelere benzetin. Her nesilde yalnız kırmızıya yakın düğmeleri ayırıp yeniden çoğaltırsanız kutunun rengi değişir. Seçimin küçük olması önemsiz değildir; tekrar sayısı sonucu büyütür.",
            "Yapay seçilim Darwin'e doğanın da seçici bir eleği olabileceğini düşündürür. Fakat doğanın hedefi, planı ve jüri masası yoktur. Daha çok yavru bırakmaya yardım eden özellikler, bunu başardıkları için sonraki kuşakta daha sık görünür.",
            "Bu başlangıç zekice bir anlatım hamlesidir. Okur önce değişimin mümkün olduğunu kendi çiftlik ve bahçe deneyiminden kabul eder. Sonra aynı mantığın insan eli olmadan nasıl işleyebileceği sorulur.",
            "Akılda kalacak görüntü güvercinliktir: Birkaç kuş arasındaki küçük fark, yeterince uzun zamanda canlı biçimlerinin ne kadar esnek olabileceğini gösterir.",
        ], "BİRİNCİ KISIM · DEĞİŞİMİN HAM MADDESİ", art="pigeon-loft", caption="Güvercin yetiştiricisi farkları yaratmaz; kuşaklar boyunca hangi farkların çoğalacağını seçerek görünümü değiştirir."),
        entry("Doğada birbirinin kopyası yok", [
            "Bir parkta aynı türden yüz ağaca uzaktan bakınca hepsi eşit görünür. Yaklaşınca yaprak biçimi, büyüme hızı, hastalığa dayanıklılık ve çiçeklenme zamanı değişir. Tür adı ortak bir dosya etiketi verir; dosyanın içindeki bireyler yine farklıdır.",
            "Darwin'in büyük dönüşlerinden biri türü değişmez kalıp gibi değil, değişken bir topluluk olarak görmesidir. Ortalama yararlı bir özet olabilir ama hiçbir birey tam olarak ortalama olmak zorunda değildir.",
            "Farkların hepsi işe yarar değildir. Bazıları zararlı, bazıları nötr, bazıları da yalnız belirli çevrede avantajlıdır. Kalın kürk soğukta korur, aşırı sıcakta yük olabilir. Özelliğin değeri çevreden bağımsız fiyat etiketi taşımaz.",
            "Bugün bu farkların genetik, gelişimsel ve çevresel kaynaklarını daha iyi biliyoruz. Darwin mekanizmayı bilmese de seçilimin çalışabilmesi için çeşitliliğin şart olduğunu doğru görmüştü.",
            "Doğal seçilimin ilk malzemesi kusursuzluk değil, farklılıktır. Herkes aynı olsaydı değişen çevre karşısında seçilecek bir seçenek de kalmazdı.",
        ], "BİRİNCİ KISIM · DEĞİŞİMİN HAM MADDESİ", art="variation-forest", caption="Aynı türden bireyler ortak etiketi taşır ama hız, biçim ve dayanıklılık bakımından birbirinin kopyası değildir."),
        entry("Bir fil ailesinin taşan hesabı", [
            "Darwin, çok yavaş üreyen filin bile bütün yavruları yaşasaydı zamanla dünyayı dolduracağını söyler. Balık, böcek veya bitki tohumu için sayı çok daha hızlı büyür. Oysa çevremiz her yıl sonsuz canlıyla dolmaz.",
            "Bir sinema salonunda yüz koltuk, kapıda bin bilet olduğunu düşünün. Herkes içeri giremez. Doğada koltuklar yiyecek, su, yuva alanı, eş, güvenli mevsim ve hastalıktan kaçış gibi sınırlardır.",
            "Buradaki mücadele yalnız diş ve pençe değildir. Kuraklığa dayanamayan fide, gölge altında ışık bulamayan ot veya eş bulamayan kuş da üreme yarışının dışında kalabilir. Darwin mücadeleyi geniş anlamda kullanır.",
            "Nüfus hesabı acımasız görünür ama doğal seçilimin mantıksal kapısını açar. Doğandan daha azı ürüyorsa, kimlerin ürüdüğü gelecek kuşağın özelliklerini etkiler.",
            "Taşan hesap bize seçilimin neden durmadan çalışabileceğini gösterir. Yaşam üretkendir; çevre ise sınırsız değildir.",
        ], "BİRİNCİ KISIM · DEĞİŞİMİN HAM MADDESİ", art="overflowing-offspring", caption="Canlılar çevrenin taşıyabileceğinden daha çok yavru üretir; sınırlı koltuklar kuşakların bileşimini değiştirir."),
        entry("Mücadele değil, ilişkiler ağı", [
            "Yaşam mücadelesi sözü yalnız kavga görüntüsü çağırabilir. Darwin'in örnekleri daha karmaşıktır. Bir bitkinin sayısı onu tozlaştıran böceğe, böcek yuvası başka bir hayvana, o hayvan da otlak düzenine bağlı olabilir.",
            "Bir mahallede fırın, okul, otobüs ve su hattı birbirinden ayrı görünür. Su kesilince fırın da okul da etkilenir. Ekosistemde de tek türün değişimi görünmeyen bağlantıları ortaya çıkarabilir.",
            "Rekabet gerçektir ama işbirliği de evrimin parçasıdır. Ortak avlanan hayvanlar, çiçek ile tozlaştırıcı veya bağırsak bakterileriyle konak arasındaki ilişkiler karşılıklı yarar sağlayabilir. Seçilim yalnız yalnız savaşan birey üretmez.",
            "Bu nedenle 'en güçlü yaşar' kaba özeti yanıltıcıdır. Uyum bazen hız, bazen kamuflaj, bazen sabır, bazen de grup içinde işbirliği demektir. Kas gücü her çevrenin ortak parası değildir.",
            "Doğa ringden çok ağdır. Bir düğüm çekildiğinde sonuç, bağlantıların yönüne göre bütün sisteme yayılabilir.",
        ], "BİRİNCİ KISIM · DEĞİŞİMİN HAM MADDESİ", art="ecological-web", caption="Doğadaki mücadele yalnız kavga değildir; rekabet, işbirliği, iklim ve karşılıklı bağımlılık aynı ağda çalışır."),
        entry("Doğal seçilim bir elek gibi", [
            "Bir sahilde açık ve koyu renkli kabuklar olduğunu düşünün. Kuşlar açık kumda koyu kabukları daha kolay görüyorsa açık renkli olanların yaşayıp üreme olasılığı biraz artabilir. Tek nesilde fark küçük, yüzlerce nesilde belirgin olabilir.",
            "Elek benzetmesi yararlıdır ama eksiktir. Doğa bir defada son ürünü ayırmaz; çevre değiştikçe eleğin delikleri de değişir. Dün koruyan renk, zemin değiştiğinde görünür hale gelebilir.",
            "Seçilim bireyin yaşamı boyunca onu ihtiyaca göre dönüştürmez. Zürafa boynunu uzattığı için yavrusu uzun boyunlu doğmaz. Popülasyonda aktarılabilir boy farkları varsa, belirli koşullarda daha çok yavru bırakanlar zamanla ortalamayı değiştirir.",
            "Uyum başarısı yalnız hayatta kalmak değildir. Hiç yavru bırakmayan çok uzun ömürlü bireyin özelliği gelecek kuşağa aktarılmaz. Biyolojik anlamda sonuç, üreme katkısıyla ölçülür.",
            "Eleğin bilinçli eli yoktur. Sonuç planlı görünebilir çünkü küçük yararlı farklar tekrar tekrar korunmuştur.",
        ], "İKİNCİ KISIM · SEÇİLİMİN ÇALIŞMASI", art="selection-sieve", caption="Doğal seçilim çevreye göre işleyen değişken bir elektir; küçük üreme farkları kuşaklar boyunca birikir."),
        entry("İhtiyaç özellik üretmez", [
            "Kutup ayısının beyaz kürkü kar yağınca sipariş edilmedi. Popülasyondaki kalıtsal renk farklarından kamuflaja yardım edenler belirli koşullarda daha çok aktarılmış olabilir. Sonuca bakınca amaç görürüz; süreçte ise kör varyasyon ve ayıklanma vardır.",
            "Bir anahtar ustası cebinde yüzlerce eski anahtar taşır. Kapıyı görünce uygun olanı dener. Kapı anahtarı o anda yaratmaz. Varyasyon da seçilimden önce veya ondan bağımsız ortaya çıkar; çevre hangisinin işe yaradığını belirler.",
            "Bu, canlıların davranarak çevreyi hiç değiştirmediği anlamına gelmez. Kunduz baraj kurar, insan tarım yapar, bakteri ortamı dönüştürür. Canlı ile çevre birbirini etkiler; yine de kalıtsal değişimin kaynağını yalnız ihtiyaçla açıklayamayız.",
            "Doğal seçilim ileriye bakmaz. Gelecekte yararlı olacak özellik, bugün maliyetliyse sırf yarın lazım diye korunmaz. Evrim plan yapan mühendis değil, geçmiş sonuçlarla ilerleyen tamircidir.",
            "Bu ayrım, 'Canlı buna neden ihtiyaç duydu?' sorusunu 'Bu özellik hangi koşullarda daha çok aktarıldı?' sorusuna çevirir.",
        ], "İKİNCİ KISIM · SEÇİLİMİN ÇALIŞMASI", art="keys-and-lock", caption="Çevre ihtiyaca göre yeni anahtar üretmez; var olan kalıtsal farklar arasından o anda işe yarayanları ayıklar."),
        entry("Merdiven değil, dallanan ağaç", [
            "Evrim çoğu zaman balıktan insana çıkan düz bir merdiven gibi çizilir. Darwin'in tek ünlü şeması ise dallanan ağaçtır. Ortak ata gövdeyi, ayrılan soylar dalları, yok olan çizgiler kuruyan uçları temsil eder.",
            "Bugünkü maymunlar bizim eski halimiz değildir. İnsanlarla yaşayan diğer insansı maymunlar, ortak atadan ayrılmış kuzen dallardır. Bir kuzen diğerinin çocukluğu değildir.",
            "Ağaçta yukarı çıkmak ahlaki üstünlük anlamına gelmez. Bakteriler milyarlarca yıldır başarılıdır. Bir orkide, kartal veya insan kendi çevresine farklı biçimde uyar; hepsini tek başarı sınavına sokmak anlamsızdır.",
            "Ortak köken benzerlikleri açıklar. Omurgalıların benzer kemik planı, embriyo gelişimindeki ortaklıklar ve DNA dizilerindeki akrabalık aynı eski gövdeden kalan işaretlerdir.",
            "Ağaç görüntüsü insanı merkezin tahtından indirir ama akrabalık çemberini büyütür. Yaşamın dışında değil, dallarından birindeyiz.",
        ], "İKİNCİ KISIM · SEÇİLİMİN ÇALIŞMASI", art="branching-tree", caption="Evrim tek hedefe çıkan merdiven değil; ortak atalardan ayrılan, bazı kolları sönen dallı bir yaşam ağacıdır."),
        entry("Aynı mahallede farklılaşmak", [
            "Bir adadaki kuş topluluğunun bir bölümü sert tohum, diğer bölümü yumuşak meyveyle beslenmeye başlasın. Gaga biçimleri ve eş seçimi zamanla ayrışırsa başlangıçtaki tek topluluk iki ayrı yola girebilir.",
            "Darwin çeşitlenmeyi, benzer bireylerin aynı kaynağa sıkışması yerine farklı yaşam biçimlerine açılmasıyla ilişkilendirir. Bir pazarda beş aynı fırın yerine biri ekmek, biri pasta, biri simit yaptığında rekabetin biçimi değişir.",
            "Modern biyoloji türleşmede coğrafi ayrılığın, gen akışının kesilmesinin ve üreme engellerinin önemini daha açık anlatır. Dağ, nehir veya uzak ada toplulukları ayrı deneylere dönüştürebilir.",
            "Sınır her zaman keskin değildir. Türleşme bir ışık düğmesi gibi bir anda açılmayabilir; ara aşamalar ve kısmi üreme engelleri bulunabilir. 'Tür' kavramının bazı canlılarda tartışmalı olması teorinin kusuru değil, doğanın sürekliliğinin işaretidir.",
            "Dallanma, farklı yaşam alanlarının aynı eski malzemeden yeni çözümler çıkarmasıdır.",
        ], "İKİNCİ KISIM · SEÇİLİMİN ÇALIŞMASI", art="diverging-island-birds", caption="Ayrılan çevreler ve üreme yolları, aynı atadan gelen toplulukları zamanla farklı tür dallarına taşıyabilir."),
        entry("Eş seçiminin gösterişli faturası", [
            "Tavus kuşunun kuyruğu kaçmayı zorlaştırabilir ama eş bulmayı kolaylaştırabilir. Darwin bu tür özellikleri cinsel seçilimle açıklar. Hayatta kalma ile eş seçme başarısı bazen aynı yönde çalışmaz.",
            "Bir konser salonunda en güvenli ayakkabı değil, dikkat çeken kıyafet seçilebilir. Doğada da gösteri, ses, renk, boynuz veya davranış rakipleri aşmaya ve eşin dikkatini çekmeye hizmet edebilir.",
            "Cinsel seçilim basit erkek gösterir, dişi seçer kalıbına sıkıştırılmamalıdır. Türler arasında ebeveynlik, rekabet ve seçim rolleri çok çeşitlidir. Modern araştırma bu ilişkileri Darwin'in döneminden daha geniş görür.",
            "Gösterişli özellik bedelsiz değildir. Kuyruğun enerji maliyeti veya boynuzun yaralanma riski vardır. Tam da bu maliyet, bazı koşullarda taşıyıcının durumuna dair işaret olabilir.",
            "Evrim yalnız çevreden kaçma hikayesi değildir; aynı türün üyeleri de birbirinin geleceğini şekillendirir.",
        ], "İKİNCİ KISIM · SEÇİLİMİN ÇALIŞMASI", art="peacock-display", caption="Cinsel seçilim bazen hayatta kalma maliyeti taşıyan gösterişli özellikleri eş bulma başarısıyla yaygınlaştırabilir."),
        entry("Göz gibi karmaşık bir şey nasıl oluşur?", [
            "Darwin kendi teorisinin zor sorularından kaçmaz. Gözün bütün parçaları birlikte çalışırken küçük adımlar nasıl yararlı olabilir? Cevabı, kusursuz kamera göz ile hiç göz arasına birçok işlevsel basamak koymaktır.",
            "Işığa duyarlı birkaç hücre yalnız aydınlık ve karanlığı ayırır. Hafif çukur ışığın yönünü gösterir. Daha derin çukur görüntüyü kabaca odaklar; saydam doku koruma ve odaklama sağlayabilir. Her basamak kendi halinde işe yarayabilir.",
            "Bir dağa yalnız zirveden bakınca dik duvar görürüz. Arkadaki kıvrımlı patika görünmez. Karmaşık organın bugünkü halini tek sıçramada istemek de aynı yanılsamadır.",
            "Bu anlatım her organın kesin tarihini tek başına kanıtlamaz. Ayrıntılı soy, genetik ve gelişim verileri gerekir. Fakat 'yarım göz işe yaramaz' itirazının zorunlu olmadığını gösterir.",
            "Evrim hazır parçaları değiştirir, yeniden kullanır ve yamalar. Sonuç etkileyici olabilir ama mühendis masasında sıfırdan çizilmiş olmak zorunda değildir.",
        ], "ÜÇÜNCÜ KISIM · İTİRAZLAR VE KANITLAR", art="eye-stairway", caption="Karmaşık göz tek sıçramayla değil, her biri kendi koşulunda yararlı olabilen küçük işlevsel basamaklarla düşünülebilir."),
        entry("Fosil arşivinin eksik rafları", [
            "Darwin döneminde fosil kaydı bugünkünden çok daha yoksuldu. Eğer yaşam yavaşça değiştiyse neden her ara biçimi bulamıyoruz? Darwin bu soruyu arşivin oluşma şartlarıyla yanıtlar.",
            "Bir canlının fosilleşmesi nadirdir. Hızla gömülmeli, sert parçaları korunmalı, kaya sonradan erimemeli ve milyonlarca yıl sonra erişilebilir yüzeye çıkmalıdır. Sonra biri doğru yerde kazmalıdır.",
            "Aile albümünüzde çocukluğun her günü yoktur. Yine de bebeklik ve yetişkinlik fotoğrafları arasında bir yabancı yaratık varsaymazsınız. Eksik albüm değişimi yok saydırmaz, fakat hikayeyi daha dikkatli kurmayı gerektirir.",
            "Darwin'den sonra çok sayıda geçiş özelliği taşıyan fosil bulundu ve tarihleme yöntemleri gelişti. Yine de kayıt hiçbir zaman video kadar sürekli olmayacaktır.",
            "Eksiklik kanıtın düşmanı değil, yorumun sınırıdır. İyi teori boş rafı saklamaz; neden boş olabileceğini ve hangi bulgunun fikri değiştireceğini söyler.",
        ], "ÜÇÜNCÜ KISIM · İTİRAZLAR VE KANITLAR", art="fossil-archive", caption="Fosil kaydı kesintisiz film değil; oluşması, korunması ve bulunması zor olan eksik ama giderek zenginleşen bir arşivdir."),
        entry("Arı peteği ve içgüdünün basamakları", [
            "Arı peteğinin düzgün altıgenleri bilinçli mimar varmış gibi görünür. Darwin içgüdüyü değişmez mucize saymak yerine, davranış farklarının da seçilimle birikebileceğini savunur.",
            "Farklı arı türlerinde basit yuvarlak hücrelerden daha düzenli yapılara uzanan çeşitlilik, işlevsel ara basamakların mümkün olduğunu gösterir. Balmumunu daha verimli kullanan küçük davranış farkları avantaj sağlayabilir.",
            "İçgüdü, hayvanın davranışı hiç öğrenmediği veya çevrenin önemsiz olduğu anlamına gelmez. Kalıtsal eğilim ile deneyim birlikte çalışabilir. Kuşun yuva kurma eğilimi doğuştan gelirken malzeme seçimi koşullarla değişebilir.",
            "Darwin'in kısır işçi böcekler sorunu özellikle zordur: Üremeyen bireyin özelliği nasıl seçilir? Cevap, davranışın akrabaların ve koloninin üreme başarısına katkısıyla ilgilidir; modern akraba seçilimi bunu daha açık matematikleştirir.",
            "Petek görüntüsü, karmaşık davranışın da kuşaklar boyunca ayıklanan küçük farklardan doğabileceğini hatırlatır.",
        ], "ÜÇÜNCÜ KISIM · İTİRAZLAR VE KANITLAR", art="honeycomb-instinct", caption="Petek gibi karmaşık içgüdüler, farklı türlerde görülen işlevsel ara basamaklar ve koloni yararıyla açıklanabilir."),
        entry("Melezler ve tür sınırının bulanıklığı", [
            "At ile eşek çiftleştiğinde katır doğabilir ama katır çoğunlukla kısırdır. Bu örnek türler arasında üreme engeli fikrini gösterir. Fakat doğada bütün sınırlar bu kadar temiz değildir.",
            "Bazı farklı türler verimli melez oluşturabilir, bazı aynı tür toplulukları zor çiftleşir. Bitkilerde kromozom değişimleri yeni türü hızlı biçimde ortaya çıkarabilir. Bakterilerde tür kavramı daha da farklı işler.",
            "Renk tayfında kırmızı ile turuncuyu ayıran çizgiyi kesin çizmek zordur; yine de renkler anlamsız değildir. Türler de evrimsel süreçte oluşan kümelerdir, her zaman değişmez kutular değil.",
            "Darwin melez kısırlığının özel olarak yerleştirilmiş bir mühür değil, başka farklılıkların yan sonucu olabileceğini savunur. Modern genetik bu engellerin çeşitli mekanizmalarını gösterir.",
            "Bulanık sınır bilimi zayıflatmaz. Tam tersine, türleşmenin devam eden bir süreç olduğunu görünür kılar.",
        ], "ÜÇÜNCÜ KISIM · İTİRAZLAR VE KANITLAR"),
        entry("Adalar neden bu kadar konuşkan?", [
            "Okyanus adaları evrimin doğal deney odalarıdır. Anakaraya uzaktır, gelen canlı sayısı sınırlıdır ve boş yaşam alanları yeni dallanmalara fırsat verir. Bu yüzden ada türleri hem yakın kıtanın canlılarına benzer hem de yalnız adaya özgü özellikler taşır.",
            "Bir adada kara memelisi az, uçabilen kuş veya rüzgarla taşınan tohum çok olabilir. Dağılım yalnız iklime göre açıklansaydı benzer iklimli her adada aynı canlıları beklerdik. Tarih ve ulaşılabilirlik de önemlidir.",
            "Komşu adalardaki akraba türler, ortak atanın farklı koşullarda değişmesine dair güçlü ipucu verir. Canlıların konumu, biçimleri kadar soy geçmişini anlatır.",
            "Bugün kıtaların hareketini, ada yaşlarını ve DNA akrabalığını Darwin'den çok daha iyi biliyoruz. Bu yeni ölçümler biyocoğrafya kanıtını güçlendirdi.",
            "Ada haritası şunu söyler: Doğa yalnız nerede yaşadığınızı değil, oraya nasıl ve kimlerle geldiğinizi de kaydeder.",
        ], "ÜÇÜNCÜ KISIM · İTİRAZLAR VE KANITLAR", art="island-map", caption="Ada canlıları iklim kadar göç yolunu ve ortak atayı da anlatır; coğrafya yaşam tarihinin görünür arşividir."),
        entry("Aynı kemik, başka görev", [
            "İnsan kolu, yarasa kanadı, balina yüzgeci ve atın ön bacağı farklı işler yapar. Yine de temel kemik dizilişleri şaşırtıcı biçimde benzerdir. Ortak plan, ortak köken fikriyle anlam kazanır.",
            "Bir evin eski odasını mutfağa, depoya veya çalışma alanına çevirebilirsiniz. Duvarların bazıları geçmiş planı ele verir. Evrim de eski yapıları yeni işlerde kullanır.",
            "Körelmiş organlar aynı tarihin başka izidir. Balinalardaki küçük leğen kemikleri veya uçamayan kuşlardaki kanat yapıları bugünkü işlevle tam açıklanmayabilir, fakat atalarının yaşamıyla anlaşılır.",
            "Sınıflandırma böylece yalnız benzer kutuları düzenleme işi olmaktan çıkar. Canlı grupları, dallanan akrabalık tarihinin adları haline gelir. Modern DNA karşılaştırmaları bazı eski sınıfları düzeltti.",
            "Aynı kemik planı, doğanın her canlıyı ayrı sayfada sıfırdan çizmediğini; eski taslakların değiştirilerek kullanıldığını gösterir.",
        ], "ÜÇÜNCÜ KISIM · İTİRAZLAR VE KANITLAR", art="homologous-limbs", caption="Kol, kanat, yüzgeç ve bacak farklı işler yaparken aynı temel kemik planıyla ortak kökenin izini taşır."),
        entry("Darwin'in bilmediği çekmece: Genler", [
            "Darwin kalıtsal farkların nasıl korunduğunu bilmiyordu. O dönemde yaygın karışmalı kalıtım fikri, farklılıkların her nesilde ortalamaya erimesi sorununu doğuruyordu. Mendel'in bezelye deneyleri daha sonra parçacıklı kalıtımı gösterdi.",
            "Yirminci yüzyılda genetik ile doğal seçilim birleşti. Mutasyon ve yeniden birleşme yeni varyasyon üretir; gen frekansları seçilim, sürüklenme ve gen akışıyla değişir. Buna modern sentez denir.",
            "Bir iskambil destesini düşünün. Yeni kart baskısı mutasyona, kartların karılması yeniden birleşmeye, bazı kartların oyunda daha çok kalması seçilime benzer. Küçük destede rastlantı da sonucu güçlü biçimde değiştirebilir.",
            "DNA ortak kökeni bağımsız biçimde sınamamızı sağladı. Yakın akrabaların dizileri genel olarak daha benzerdir ve bu benzerlikler dallanan soy ağacıyla uyuşur.",
            "Modern genetik Darwin'i kutsal metne dönüştürmez. Eksik mekanizmayı tamamlar, bazı varsayımları düzeltir ve teoriyi ölçülebilir hale getirir.",
        ], "DÖRDÜNCÜ KISIM · BUGÜN NEREDEYİZ?", art="genes-drawer", caption="Darwin'in eksik bıraktığı kalıtım çekmecesini Mendel, DNA ve popülasyon genetiği doldurdu."),
        entry("Seçilim tek oyuncu değil", [
            "Bir fırtına adadaki kuşların yarısını rastgele yok ederse kalan özellikler daha iyi oldukları için değil, şans eseri çoğalabilir. Genetik sürüklenme özellikle küçük topluluklarda rastlantının gücünü anlatır.",
            "Göç eden bireyler genleri başka topluluğa taşır; buna gen akışı denir. Mutasyon yeni varyasyon getirir. Eş seçimi, gelişim kısıtları ve çevreyi değiştiren davranışlar da evrimsel sonucu etkiler.",
            "Futbol maçını yalnız forvetle açıklamak gibi, bütün evrimi yalnız seçilime indirgemek eksiktir. Doğal seçilim uyumu açıklamada merkezi oyuncudur ama saha, hakem, hava ve tesadüf de sonucu değiştirir.",
            "Bazı özellikler doğrudan yararlı oldukları için değil, yararlı başka bir özelliğe genetik olarak bağlı oldukları veya ciddi maliyet taşımadıkları için kalabilir.",
            "Darwin'in büyük fikri ayakta kalır; modern biyoloji sahnedeki oyuncu sayısını artırır. Bilim ilerledikçe iyi teori darbe alıp yok olmak yerine daha kesin sınırlar kazanabilir.",
        ], "DÖRDÜNCÜ KISIM · BUGÜN NEREDEYİZ?", art="evolutionary-players", caption="Doğal seçilim merkezi olsa da mutasyon, sürüklenme, gen akışı ve gelişim kısıtları aynı evrim sahnesinde rol oynar."),
        entry("Evrim ilerleme merdiveni değildir", [
            "Evrim kelimesi günlük dilde sürekli daha iyiye gidiş gibi kullanılır. Oysa biyolojik değişim belirli çevrede üreme başarısıyla ilgilidir. Mağarada göz kaybı, enerji tasarrufu sağlıyorsa gerileme değil uyum olabilir.",
            "İnsan evrimin hedefi değildir. Dinozorlar bizim için yolu açmak üzere yaşamadı; bakteriler ilkel ve başarısız kalıntılar değildir. Her yaşayan soy, bugüne kadar süren kendi tarihinin sonucudur.",
            "Doğal olanın ahlaken iyi olduğu da söylenemez. Hastalık, yavru ölümü ve parazitlik doğaldır ama insan toplumu bunları azaltmaya çalışır. Doğadan değer yasası çıkarmak ayrı bir felsefi karardır.",
            "Bu ayrım sosyal Darwinizm için önemlidir. Ekonomik eşitsizliği veya sömürgeciliği 'doğal yarış' diye haklı göstermek biyolojiden ahlak sıçraması yapar. Darwin'in teorisi toplumda güçlünün haklı olduğunu söylemez.",
            "Yaşam ağacında taç yoktur. İnsan aklı güçlü bir özellik olabilir; aynı akıl başkalarının acısını azaltma sorumluluğu da yaratır.",
        ], "DÖRDÜNCÜ KISIM · BUGÜN NEREDEYİZ?"),
        entry("Bir dakikalık harita", [
            "Popülasyonlarda aktarılabilir farklılıklar bulunur. Canlılar çevrenin taşıyabileceğinden daha çok yavru üretir. Belirli koşullarda daha çok üremeye yardım eden farklar kuşaklar boyunca yaygınlaşabilir; buna doğal seçilim deriz.",
            "Soylar ayrılır, değişir ve bazen yok olur. Bu süreç tek hedefe çıkan merdiven değil, ortak atalardan dallanan ağaç üretir. Fosiller, coğrafi dağılım, benzer organ planları, embriyoloji ve bugün DNA bu akrabalık tarihini destekler.",
            "Darwin genetiği bilmiyordu. Modern sentez mutasyon, genler ve popülasyon matematiğini ekledi; sürüklenme ve gen akışı gibi seçilim dışı süreçleri görünür kıldı. Evrim ahlaki ilerleme veya güçlünün haklılığı değildir.",
        ], "SONUÇ"),
        entry("Akılda kalacak beş görüntü", [
            "Güvercinlik: Küçük farklar seçilince büyür. Taşan salon: Her doğan üreyemez. Değişken elek: Çevre hangi farkın işe yaradığını değiştirir. Dallı ağaç: Canlılar kuzen soylar halinde ayrılır. Eksik arşiv: Fosil kaydı parçalıdır ama okunabilir.",
            "Bu beş görüntü bir canlı özelliği gördüğünüzde doğru soruları hatırlatır: Toplulukta hangi farklar vardı? Bunların hangisi aktarılabiliyordu? Çevre kimin daha çok yavru bırakmasına yol açtı? Rastlantı ve göç ne yaptı?",
            "Darwin'in kalıcı başarısı bütün cevapları bilmesi değildir. Ayrı ayrı görünen sayısız canlıyı, sınanabilir ortak bir tarih fikrinde birleştirmesidir.",
        ], "SONUÇ"),
    ],
})


BOOKS.append({
    "bookNo": 36,
    "title": "Hızlı ve Yavaş Düşünme",
    "author": "Daniel Kahneman",
    "subtitle": "Zihnin hızlı kestirmeleriyle yavaş denetimini, günlük kararların görünmeyen tuzaklarını ve bu fikirlerin sınırlarını canlı örneklerle anlatan rehber.",
    "coverImage": "/images/summary-art-36-hizli-ve-yavas-dusunme-v2.webp",
    "coverStyle": "artwork",
    "pdfUrl": "/data/pdfs/36-hizli-ve-yavas-dusunme-ozeti.pdf",
    "pdfLabel": "25-50 sayfalık PDF'yi indir",
    "longForm": True,
    "chapterArtStyle": "monochrome-engraving",
    "chapterArtColor": "#72515C",
    "meta": {
        "originalTitle": "Thinking, Fast and Slow",
        "compiler": "Zihin Gezgini · Yapay zeka destekli çalışma",
        "date": "Temmuz 2026",
        "language": "Türkçe",
    },
    "intro": "Bir fiyat etiketinin ilk gördüğümüz sayısı pazarlığımızı etkileyebilir. Kötü bir haber, dünyadaki tehlikeyi olduğundan büyük hissettirebilir. Bir projenin geçmişteki benzerlerini unutup bu kez her şeyin kusursuz gideceğini düşünebiliriz. Daniel Kahneman bu şaşırtıcı hataları iki akılda kalıcı oyuncuyla anlatır: Hızlı, çağrışımlı ve çabasız çalışan Sistem 1 ile hesap yapan, dikkat isteyen Sistem 2. Bu rehber kitabın bütün büyük bölümlerini koruyor; kavramları alışverişten doktor kararına, tatilden iş planına uzanan sahnelerle açıyor. Aynı zamanda iki sistemin gerçek beyin bölmeleri değil anlatım benzetmeleri olduğunu, her sezginin hata sayılmayacağını ve sosyal hazırlama gibi bazı ünlü deneylerin tekrar sınamalarında tartışma çıktığını açıkça belirtiyor.",
    "sources": [
        {"id": 1, "title": "Macmillan - Hızlı ve Yavaş Düşünme resmi kitap tanıtımı", "url": "https://us.macmillan.com/books/9780374275631/thinkingfastandslow/"},
        {"id": 2, "title": "Nobel Prize - Daniel Kahneman Nobel dersi", "url": "https://www.nobelprize.org/prizes/economic-sciences/2002/kahneman/lecture/"},
        {"id": 3, "title": "Nobel Prize - Sınırlı akılcılık ve karar verme özeti", "url": "https://www.nobelprize.org/prizes/economic-sciences/2002/popular-information/"},
        {"id": 4, "title": "Nature - Davranış biliminde tekrarlanabilirlik bağlamı", "url": "https://www.nature.com/articles/s44271-023-00003-2"},
        {"id": 5, "title": "PMC - Sosyal hazırlama çalışmalarının çok laboratuvarlı sınaması", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC10031630/"},
    ],
    "entries": [
        entry("Bu kitap nasıl okunmalı?", [
            "Bu kitap bir hata avcılığı yarışması değildir. Kahneman'ın amacı insanı aptal ilan etmek değil, çoğu gün mükemmel iş gören hızlı düşünmenin hangi koşullarda düzenli biçimde yanılabildiğini göstermektir.",
            "Sistem 1 ve Sistem 2, kafamızda yaşayan iki küçük kişi değildir. Biri otomatik işlemler, diğeri dikkat isteyen işlemler için kullanılan öğretici adlardır. Aynı kararın içinde ikisi de yer alabilir; aralarında kesin bir duvar yoktur.",
            "Her bölümde üç soru kullanacağız: Zihin hangi kestirmeyi yaptı, bu kestirme normalde neden işe yarıyor ve hangi bilgi onu yanıltıyor? Böyle okuyunca kavramlar ezber listesi olmaktan çıkar, günlük kararlar için kontrol paneline dönüşür.",
        ], "BAŞLANGIÇ"),
        entry("Sopayla topun bir liralık şaşırtmacası", [
            "Bir sopa ile top birlikte 1 lira 10 kuruş olsun. Sopa toptan 1 lira pahalıysa top kaç kuruştur? Zihin çoğu kişiye hemen 10 kuruş der. Cevap akıcı ve ikna edicidir, fakat sopa 1 lira 10 kuruş olursa toplam 1 lira 20 kuruşa çıkar.",
            "Yavaşça denklem kurunca topun 5, sopanın 1 lira 5 kuruş olduğu görülür. İlk cevap rastgele değildir; zihin toplam ile farkı birbirine karıştıran kolay bir işlem yapmıştır. Sistem 1 soruya benzeyen daha basit bir soruyu yanıtlamıştır.",
            "Hızlı düşünme konuşmayı anlamak, yüzü tanımak ve ani tehlikede frene basmak için vazgeçilmezdir. Her işlemi uzun hesapla yapsaydık markette bir rafın önünden ayrılamazdık. Sorun hız değil, hızın ürettiği cevabın denetlenmeden onaylanmasıdır.",
            "Sistem 2 kontrol edebilir ama dikkat pahalıdır. Yorgunken, acelemiz varken veya cevap hoşumuza gitmişken denetim zayıflar. Bu yüzden basit görünen kritik bir hesapta kalem kullanmak, zekasızlık değil iyi tasarımdır.",
            "Sopa ve top, kitabın küçük amblemidir: Aklımıza ilk gelen cevap bazen yalnızca aklımıza ilk gelendir.",
        ], "BİRİNCİ KISIM · İKİ ÇALIŞMA TARZI", art="bat-ball-puzzle", caption="Sopa ve top sorusu, akıcı ilk cevabın küçük bir yavaş denetimle nasıl değişebildiğini gösterir."),
        entry("Dikkatin dar ışığı", [
            "Kalabalık bir istasyonda arkadaşınızla konuşurken arkanızdaki ilan değişebilir ve siz fark etmeyebilirsiniz. Göz açık olduğu halde görmek, dikkatin oraya ayrıldığı anlamına gelmez. Zihin kameradan çok seçici bir sahne ışığı gibi çalışır.",
            "Ünlü bir görevde insanlardan top paslarını saymaları istenir. Sayıya gömülen bazı izleyiciler kadrajdan geçen olağanüstü bir figürü bile kaçırır. Sonradan görüntü gösterilince bunu nasıl görmediklerine inanamazlar.",
            "Sistem 2 bir işi dikkatle yaparken başka işlere ayıracak kaynağı azalır. Araç kullanırken zor bir adresi arayan kişinin radyoyu kısması bu yüzden tanıdıktır. Ses yolu kapatmıyordur; dikkat yükünü azaltmak isteriz.",
            "Kaçırdığımız şeyi kaçırdığımızı da bilmeyebiliriz. Bu durum tanıklıkta, tıpta ve iş güvenliğinde önemlidir. 'Bakıyordum, demek ki görürdüm' güvenilir bir kural değildir.",
            "Dikkat ışığı güçlüdür ama dardır. Önemli kararları tek kişinin gözüne bırakmamak, kontrol listesi ve ikinci göz kullanmak bu insani sınırı kabul etmektir.",
        ], "BİRİNCİ KISIM · İKİ ÇALIŞMA TARZI", art="attention-spotlight", caption="Dikkat bir projektör gibi seçtiği alanı aydınlatır; görüntüde bulunan her şey bilinçte görünmez."),
        entry("Tembel denetçi neden hemen atlamaz?", [
            "Kahneman Sistem 2'yi biraz tembel bir denetçiye benzetir. Denetçi gerektiğinde hesap yapar, kurala uyar ve dürtüyü bastırır; fakat her küçük işlem için masadan kalkmak istemez. Çoğu öneriyi hızlı sistemden kabul eder.",
            "Uzun bir günün sonunda internetten alışveriş yaparken sepete eklenen ürünü daha az sorgulamamız bu tabloya uyar. Dikkat ve özdenetim sınırsız pil değildir. Yine de bunun basit bir enerji deposu gibi ölçüldüğü bazı eski iddialar daha sonra tartışılmıştır.",
            "Denetçinin tembelliği bütünüyle kusur değildir. Sabah kapıyı açmak, tanıdık yolda yürümek ve her sözcüğü anlamak için kurul toplasaydık hayat kilitlenirdi. Alışkanlıklar zihinsel emeği tasarruf eder.",
            "Asıl soru hangi kararı otomatiğe bırakacağımızdır. Ucuz, geri döndürülebilir seçimlerde hız işe yarar. Sağlık, büyük para ve başkasının hayatını etkileyen kararlarda küçük bir bekleme aralığı değerlidir.",
            "İyi karar veren kişi her zaman yavaş değildir; yavaşlamaya değen yeri tanır.",
        ], "BİRİNCİ KISIM · İKİ ÇALIŞMA TARZI", art="lazy-controller", caption="Yavaş denetçi her hızlı cevabı incelemez; dikkat pahalı olduğu için çoğu günlük öneriyi otomatik olarak onaylar."),
        entry("Çağrışım makinesi boşluğu doldurur", [
            "'Muz' sözcüğünden sonra 'sarı', 'meyve' veya 'maymun' daha kolay akla gelir. Zihin tek tek dosya çekmek yerine bağlantılı bir ağ çalıştırır. Bir düşünce komşusunu uyandırır, o da başka bir kapıyı açar.",
            "Bu ağ sayesinde yarım cümleyi tamamlar, yüz ifadesinden niyet sezer ve hikayeyi hızla kavrarız. Fakat ağ kanıt görmeden de tutarlı sahne kurabilir. Bir kişi için önce 'soğuk' kelimesini duyunca belirsiz davranışını daha mesafeli yorumlayabiliriz.",
            "Kitap hazırlama etkilerine geniş yer verir: Önce görülen bir işaret sonraki düşünceyi kolaylaştırabilir. Kelime tanıma gibi temel hazırlama etkileri sağlamdır; bazı geniş sosyal davranış iddiaları ise tekrarlama çalışmalarında aynı gücü göstermemiştir.",
            "Bu ayrım önemlidir. İlginç bir deney, bütün insanların gizli düğmelerle uzaktan yönetildiğini kanıtlamaz. Etkinin büyüklüğü, koşulu ve tekrar edilebilirliği ayrı ayrı sorulmalıdır.",
            "Çağrışım makinesi dünyayı hızlı anlamlandırır. Onu susturamayız; fakat kurduğu ilk hikayenin tek mümkün hikaye olmadığını hatırlayabiliriz.",
        ], "BİRİNCİ KISIM · İKİ ÇALIŞMA TARZI", art="associative-machine", caption="Çağrışım ağı bir düşünceden komşusuna sıçrayarak hız kazandırır, bazen eksik kanıttan tamamlanmış hikaye üretir."),
        entry("İlk sayı pazarlığın görünmez kazığı", [
            "Bir emlakçı önce çok yüksek bir fiyat söylerse sonraki indirim makul görünebilir. İlk sayı konuyla ilgisiz olsa bile tahminleri kendi yönüne çekebilir. Kahneman buna çapalama etkisi der.",
            "Gemi yaşı sorulmadan önce rulette büyük sayı gören birinin tahmini, küçük sayı göreninkinden yüksek çıkabilir. İnsanlar sayının rastgele olduğunu bilse bile zihin o çevrede cevap aramaya başlar.",
            "Pazarlıkta satıcının ilk rakamı yalnız teklif değil, ölçü cetveli olur. İndirim yüzdesi aynı cetvele bağlı olduğu için sahte bir kazanç hissi doğabilir. Savunma, ilk fiyattan önce bağımsız piyasa aralığı hazırlamaktır.",
            "Çapa her kişiyi aynı miktarda çekmez ve sihir değildir. Bilgi, uzmanlık ve açık karşılaştırma etkisini azaltabilir. Fakat 'bana işlemez' demek kanıt sayılmaz; çünkü hareket çoğu zaman bilinç dışında başlar.",
            "Bir sayı masaya geldiğinde önce kaynağını sorun: Ölçüm mü, istek mi, rastgele başlangıç mı? Cetvel eğriyse hassas hesap da eğri sonuç verir.",
        ], "İKİNCİ KISIM · KESTİRMELER", art="anchoring-sticker", caption="İlk görülen sayı görünmez bir çapa gibi sonraki tahminlerin hareket edeceği alanı daraltabilir."),
        entry("Haberlerde çoksa dünyada da çok sanmak", [
            "Uçak kazası görüntüleri günlerce ekranda kalır; sıradan trafik kazaları tek tek haber olmaz. Bu yüzden uçuş riski zihinde olduğundan daha büyük, her gün kullanılan yol daha sıradan hissedilebilir.",
            "Zihin bir olayın olasılığını hesaplarken belleğe sorar: Bundan kaç örnek kolayca bulabiliyorum? Canlı, yeni ve duygulu örnekler hızlı gelir. Kahneman bu kestirmeye bulunabilirlik der.",
            "Kestirme bazen akıllıdır. Mahallede üç dükkana aynı hırsız girmişse kolay hatırlama gerçek bir artışı gösterebilir. Sorun, medyanın seçimi veya kişisel travmanın görünürlük ile sıklık arasındaki bağı bozmasıdır.",
            "Bir hastalığı yaşayan arkadaşınız olması, riskin sizin için arttığını göstermeyebilir; yalnız zihinsel yakınlığı artırır. Tersine sessiz ilerleyen yaygın riskler manşet olmadığı için küçümsenebilir.",
            "Canlı örneği çöpe atmayın, yanına taban oranını koyun. Hikaye 'bu olabilir' der; sayı 'ne kadar sık olur' sorusunu yanıtlar.",
        ], "İKİNCİ KISIM · KESTİRMELER", art="availability-news", caption="Canlı ve sık tekrarlanan haberler belleğe kolay gelir; kolay hatırlamak, olayın gerçekten daha sık olduğu anlamına gelmez."),
        entry("İkna edici profil ile gerçek olasılık", [
            "Sessiz, düzenli ve kitap düşkünü bir kişi anlatıldığında onun kütüphaneci olduğunu tahmin etmek kolaydır. Profil kalıba uyar. Fakat toplumda satış görevlisi sayısı kütüphaneciden çok fazlaysa başlangıç oranı sonucu etkiler.",
            "Temsil edicilik kestirmesi 'Bu kişi hangi hikayeye benziyor?' sorusunu yanıtlar. Olasılık sorusu ise hem benzerliği hem de grupların ne kadar yaygın olduğunu ister. Zihin çoğu zaman yalnız renkli profili kullanır.",
            "Bir girişimci enerjik ve parlak sunum yapıyor diye şirketinin başarılı olma olasılığı kendiliğinden yükselmez. Sektördeki kapanma oranı, sermaye ve müşteri verisi de masada olmalıdır.",
            "Kalıplar bütünüyle işe yaramaz değildir; deneyimden özet bilgi taşıyabilir. Fakat küçük bir betimleme, güvenilir istatistiği silmemelidir. Özellikle işe alımda profil hikayesi önyargıyı bilim kılığına sokabilir.",
            "İyi soru şudur: Bu betimlemeyi hiç görmeseydim başlangıç olasılığını kaç verirdim? Sonra yeni kanıtın onu ne kadar değiştirmesi gerektiğini düşünün.",
        ], "İKİNCİ KISIM · KESTİRMELER", art="representative-profile", caption="Bir profil mesleğin kalıbına benzeyebilir, fakat gerçek olasılık o mesleğin toplumdaki başlangıç sıklığını da içerir."),
        entry("Küçük hastanenin büyük dalgalanması", [
            "Bir şehirde küçük ve büyük hastane olsun. Erkek bebek oranının bir yıl boyunca yüzde 60'ı aştığı günler hangisinde daha çok görülür? Birçok kişi eşit der; oysa küçük hastanede günlük doğum az olduğu için rastlantı daha geniş sallanır.",
            "On kez para atınca yedi tura şaşırtıcı değildir. On bin atışta yüzde 70 tura son derece şaşırtıcıdır. Örnek büyüdükçe rastlantısal uçlar genellikle daralır.",
            "İnsanlar küçük örneklerin bütünü kusursuz temsil etmesini bekler. Üç müşterinin övgüsüyle ürünün harika, iki kötü haftayla yatırımın çürük olduğuna karar veririz. Küçük sayı gürültüyü karakter gibi gösterir.",
            "Küçük örnek hiçbir şey anlatmaz demek de yanlıştır. İlk ipucunu verir; yalnız güven aralığı geniştir. Kararın ağırlığına göre daha çok veri veya tekrar gerekir.",
            "Dalgalanan küçük hastane, istatistikte sık unutulan bir resmi akılda tutar: Az sayıda olay, şansın sesini yükseltir.",
        ], "İKİNCİ KISIM · KESTİRMELER", art="small-sample-hospital", caption="Küçük örneklerde rastlantı daha sert dalgalanır; birkaç gözlem bütün topluluğun temiz minyatürü değildir."),
        entry("Pilotun başarısı neden ortalamaya döner?", [
            "Bir eğitmen olağanüstü iniş yapan pilotu övdükten sonra sonraki inişin kötüleştiğini, kötü inişi azarladıktan sonra ise düzeldiğini görür. Buradan övgünün bozduğu, cezanın geliştirdiği sonucunu çıkarabilir.",
            "Oysa olağanüstü sonuçların bir kısmı beceriye, bir kısmı da rüzgar gibi geçici şansa bağlıdır. Aşırı iyi günün ardından daha sıradan, aşırı kötü günün ardından daha sıradan sonuç gelmesi doğaldır. Buna ortalamaya dönüş denir.",
            "Bir öğrenci en kötü sınavından sonra özel ders alıp yükselirse bütün artışı derse yazmak kolaydır. Ders yararlı olabilir; fakat başlangıç zaten olağandışı düşükse bir miktar dönüş beklenirdi. Karşılaştırma grubu bu yüzden değerlidir.",
            "Ortalamaya dönüş kader değildir ve her değişimi açıklamaz. Yalnız aşırı ölçümden sonra doğal bir geri hareket beklendiğini söyler. Nedensel hikaye kurmadan önce bu matematiksel gölge kontrol edilmelidir.",
            "Pilot sahnesi, geri bildirimin değerini azaltmaz. Bize yalnız ödül ve cezanın etkisini görmek için ilk bakıştan daha iyi deney gerektiğini öğretir.",
        ], "İKİNCİ KISIM · KESTİRMELER", art="regression-pilot", caption="Aşırı iyi veya kötü performansın ardından daha sıradan sonuç gelmesi, müdahale olmasa da beklenebilen ortalamaya dönüş olabilir."),
        entry("Gördüğün her şeymiş gibi", [
            "Bir iş adayının sıcak konuşması ve düzgün özgeçmişi elimizdeyse zihin hızla güvenilir bir kişi hikayesi kurar. Bilmediğimiz referanslar, ölçülmemiş beceriler ve görüşme günündeki şans sahnenin dışında kalır.",
            "Kahneman bu eğilimi 'elde olan bilgi her şeymiş gibi' düşünmekle anlatır. Zihin tutarlı hikayeyi, bilginin miktarından daha çok sever. İki uyumlu ipucu, on karışık ipucundan daha ikna edici hissedebilir.",
            "Haber başlığı suçlayıcıysa kişi hakkındaki ilk yargı oluşur; sonraki düzeltme aynı güce ulaşmayabilir. Eksikliği görmek için özel çaba gerekir, çünkü görünmeyen veri kendi adına bağırmaz.",
            "Çözüm her kararı sonsuz veriyle boğmak değildir. Önemli kararda kısa bir 'Neyi bilmiyoruz?' turu yapmak, karşı kanıt aramak ve ayrı gözlemcilerin değerlendirmesini önce bağımsız almak hikaye baskısını azaltır.",
            "Projektörün içi çok aydınlıksa sahnenin geri kalanının karanlık olduğunu unutmak kolaydır.",
        ], "ÜÇÜNCÜ KISIM · AŞIRI GÜVEN", art="wysiati-spotlight", caption="Zihin elindeki birkaç uyumlu parçadan tamamlanmış öykü kurar; görünmeyen kanıt sessiz kaldığı için eksiklik hissedilmez."),
        entry("Sonucu bildikten sonra geçmiş dümdüz görünür", [
            "Bir şirket battığında eski haberlerdeki her sorun işaret gibi parlar. Başarılı olduğunda aynı riskler cesaretin kanıtı sayılabilir. Sonucu öğrendikten sonra geçmişteki belirsizlik silinir.",
            "Geri görüş yanlılığı 'zaten belliydi' duygusu üretir. Oysa karar anındaki insanlar geleceğin hangi dalının gerçekleşeceğini bilmiyordu. Sonuç, eski ihtimalleri yeniden boyar.",
            "Bu yanlılık yöneticiyi yalnız sonuçla değerlendirmeye iter. İyi süreç kötü şansla kaybedebilir, kötü süreç iyi şansla kazanabilir. Kumar masasında tek el, stratejinin kalitesini göstermez.",
            "Karar günlüğü yararlıdır: Karardan önce ne bildiğinizi, hangi olasılıkları verdiğinizi ve neyin fikrinizi değiştireceğini yazın. Sonra hafızanın başarı hikayesine küçük bir kayıt karşı koyar.",
            "Geçmiş film değildir; sonucu bilen anlatıcının yeniden kurguladığı bir hikayedir. Adaletli ders çıkarmak için eski belirsizliği geri çağırmak gerekir.",
        ], "ÜÇÜNCÜ KISIM · AŞIRI GÜVEN", art="hindsight-story", caption="Sonuç öğrenilince geçmişteki dağınık işaretler kaçınılmaz bir yol gibi dizilir; karar anındaki belirsizlik görünmez olur."),
        entry("İtfaiyecinin sezgisi ile borsa tahmini aynı mı?", [
            "Deneyimli bir itfaiyeci zeminde açıklayamadığı bir tuhaflık hissedip ekibini çıkarabilir; saniyeler sonra döşeme çöker. Yıllarca yinelenen düzenler, bilinçli cümle kurulmadan tanınabilir.",
            "Kahneman ile uzmanlık araştırmacısı Gary Klein'ın ortak ölçüsü iki koşula bakar: Çevrede öğrenilebilir düzen var mı ve kişi hızlı, güvenilir geri bildirim aldı mı? Satranç ve bazı acil durumlar bu koşulları sağlayabilir.",
            "Borsa gibi yüksek gürültülü alanlarda aynı olay nadiren aynı sonucu üretir. Birkaç başarılı tahmin, kalıcı uzmanlık görüntüsü yaratabilir. Güven duygusu doğruluk ölçeri değildir; hikayenin zihinde ne kadar akıcı olduğudur.",
            "Doktorun yıllara dayanan örüntü bilgisi değerlidir, fakat nadir hastalıkta taban oranı ve test sonucu yine gerekir. Sezgiyle istatistik düşman değil, farklı koşullarda kullanılan araçlardır.",
            "Bir uzmanın sözünü değerlendirirken ününden önce eğitim sahasını sorun: Düzen tekrar ediyor muydu, hatayı çabuk görebiliyor muydu?",
        ], "ÜÇÜNCÜ KISIM · AŞIRI GÜVEN", art="expert-intuition", caption="Uzman sezgisi, düzenli ortam ve hızlı geri bildirimle eğitildiğinde güçlenir; gürültülü alanda güven doğruluğu garanti etmez."),
        entry("Proje içeriden kısa, dışarıdan uzun görünür", [
            "Bir ekip yeni ders kitabını iki yılda bitireceğine inanır. Herkes kendi planını, yeteneğini ve güzel işbirliğini görür. Benzer ekiplerin çoğunun yedi yılda bitirdiği veya bıraktığı bilgisi ise kenarda kalır.",
            "İçeriden bakış özel hikayeyi anlatır: Kim ne yapacak, işler nasıl ilerleyecek? Dışarıdan bakış benzer projelerin gerçek dağılımını sorar. Planlama yanılgısı, ilk hikayenin ikinci veriyi bastırmasıdır.",
            "Ev tadilatında ustaya yalnız bu evin kaç hafta süreceğini sormak yerine son yirmi benzer işin ortancasını sorun. Sonra gerçekten özel olan koşullar için düzeltme yapın. Referans sınıfı kaba ama sağlam bir başlangıç verir.",
            "İyimserlik girişim enerjisi yaratabilir; hiç kimse bütün güçlükleri canlı hissetse başlamayabilir. Fakat bütçe ve takvim, motivasyon konuşmasından farklı bir görevdir. Umutla muhasebeyi aynı tabloya yazmamak gerekir.",
            "Dışarıdan bakış kişisel hikayeyi küçümsemez. Onu dünyadaki benzer hikayelerin içine yerleştirir.",
        ], "ÜÇÜNCÜ KISIM · AŞIRI GÜVEN", art="outside-view", caption="İçeriden plan kusursuz görünürken dışarıdan bakış, benzer projelerin gerçek süre ve başarısızlık dağılımını hatırlatır."),
        entry("Kazanç ve kayıp nereden ölçülür?", [
            "Maaşınızın 40 binden 50 bine çıkmasıyla 60 binden 50 bine düşmesi aynı son gelire ulaştırır. Buna rağmen hisler ters olur. Zihin yalnız son serveti değil, başladığı noktaya göre değişimi değerlendirir.",
            "Kahneman ve Amos Tversky'nin beklenti teorisi, kararların referans noktasına bağlı olduğunu söyler. Sıfır çizgisi bankadaki mutlak toplam değil; dün, beklenti, komşu veya ilan edilen hedef olabilir.",
            "Bir mağaza önce fiyatı yükseltip sonra indirim yazdığında referans noktamızı etkiler. Ürün aynı olduğu halde '200 lira kazandım' hissi doğar. Gerçek soru alternatif mağazalarda ne ödendiğidir.",
            "Referans noktası sabit değildir. Zam kısa süre sonra yeni normale dönüşür; ilk sevinç azalır. Bu uyum, daha fazlasının neden her zaman aynı mutluluk artışını vermediğini kısmen açıklar.",
            "Kararda önce sıfır çizgisini bulun. Bazen tartıştığınız seçenekler değil, gizlice seçilmiş başlangıç noktası duyguyu yönetir.",
        ], "DÖRDÜNCÜ KISIM · KARARLAR", art="reference-point", caption="Aynı sonuca yükselerek veya düşerek ulaşmak farklı hissedilir; karar duygusu seçilen referans noktasına bağlıdır."),
        entry("Kupayı vermek almaktan daha acı", [
            "Bir gruba kahve kupası verilir, diğerine satın alma fırsatı sunulur. Kupaya sahip olanların istediği satış fiyatı, sahip olmayanların vermek istediğinden yüksek olabilir. Sahiplik, nesneyi kayıp tarafına taşır.",
            "Kayıptan kaçınma, eşit miktardaki kaybın benzer kazançtan çoğu durumda daha ağır hissedilmesini anlatır. Yüz lira bulmanın sevinci, yüz lira kaybetmenin acısını tam dengelemeyebilir.",
            "Bu yüzden insanlar kötü yatırımı sırf zararı kabul etmemek için tutabilir veya değişimin olası kaybını büyütüp mevcut düzenin görünmeyen maliyetini küçümseyebilir. Statüko bedava değildir ama kayıp gibi görünmez.",
            "Etkiler bağlama göre değişir; her insan ve her karar aynı oranı göstermez. Laboratuvar bulgusunu değişmez doğa yasası gibi kullanmak kitabın kendi uyarısına ters düşer.",
            "Kupayı elinize aldığınız anda fiyatın değişmesi, değerin yalnız nesnede değil, sahiplikle kurulan ilişkide de üretildiğini gösterir.",
        ], "DÖRDÜNCÜ KISIM · KARARLAR", art="loss-aversion-mug", caption="Sahip olduğumuz kupadan vazgeçmek kayıp gibi hissedildiği için, satışta istediğimiz fiyat satın alma isteğimizden yükselebilir."),
        entry("Aynı ameliyat, başka cümle", [
            "Bir doktor ameliyat için 'Yüz hastanın doksanı yaşıyor' diyebilir. Başka doktor 'Yüz hastanın onu ölüyor' der. Sayısal bilgi aynıdır; yaşama ve ölüm çerçevesi karar duygusunu değiştirebilir.",
            "Çerçeveleme etkisi, kararın yalnız sonuca değil nasıl sunulduğuna bağlı olduğunu gösterir. Et yüzde 80 yağsız dendiğinde, yüzde 20 yağlı denmesine göre daha çekici gelebilir.",
            "Her dil seçimi çerçevedir; tamamen çerçevesiz konuşamayız. Etik görev önemli kararda eşdeğer sunumları yan yana koymak, mutlak sayıları göstermek ve gizlenen karşı seçeneği görünür kılmaktır.",
            "Siyasette vergi 'yük', yatırım veya 'ortak katkı' olarak adlandırılabilir. Sözcük yalnız süs değildir; hangi değer ve kaybın öne çıkacağını düzenler. Yine de çerçeve etkisi insanların hiçbir gerçek tercihi olmadığı anlamına gelmez.",
            "Aynı ameliyatı iki cümleyle duyunca fikriniz değişiyorsa durup veriyi ortak bir biçime çevirin. Dil değişsin, hesap aynı kalsın.",
        ], "DÖRDÜNCÜ KISIM · KARARLAR", art="framing-surgery", caption="Yaşama ve ölüm çerçeveleri aynı ameliyat oranını farklı hissettirebilir; eşdeğer sunumları yan yana görmek gerekir."),
        entry("Nadir ihtimaller neden hem korkutur hem cezbedici gelir?", [
            "Piyango bileti küçük bir olasılığa büyük ağırlık verir; sigorta da küçük felaket ihtimalini satın alınabilir huzura çevirir. İnsan nadir sonuçları bazen olması gerekenden fazla, bazen deneyiminde hiç görmeyince az önemser.",
            "Beklenti teorisinde olasılıkların psikolojik ağırlığı düz değildir. Kesinlik ile yüzde 99 arasındaki fark, yüzde 40 ile 41 arasından daha büyük hissedilebilir. Kesin kazancı korumak için riskten kaçarken kesin kayıptan kaçmak için risk arayabiliriz.",
            "Tek karar ile tekrar eden karar ayrılmalıdır. Bir kez oynanan küçük riskin duygusu, yüzlerce benzer kararın toplam hesabından farklıdır. İşletmeler geniş çerçeveyle portföye, birey ise tek olaya bakabilir.",
            "Nadir olayda yalnız 'olur mu' değil, 'olasılık kaç, zarar ne, kaç kez karşılaşacağım ve telafi gücüm var mı' diye sorun. Düşük olasılık büyük yıkım yaratıyorsa önlem yine akıllıca olabilir.",
        ], "DÖRDÜNCÜ KISIM · KARARLAR"),
        entry("Yaşayan ben ile hatırlayan ben", [
            "Bir tatilin her günü güzel geçebilir, fakat son gün bavul kaybolursa anı o kötü sonla renklenir. Yaşayan ben binlerce anı tecrübe eder; hatırlayan ben hikayeyi seçilmiş birkaç sahneyle saklar.",
            "Kahneman acı veren tıbbi işlemlerde zirve ve sonun hatırada orantısız rol oynayabildiğini anlatır. Süre uzasa bile daha yumuşak bir son, toplam deneyimin anısını iyileştirebilir. Buna süreyi ihmal ve zirve-son örüntüsü denir.",
            "Bu ayrım tatil planını garipleştirir: Fotoğraf ve final için mi, yaşanacak saatler için mi seçim yapıyoruz? İkisi de gerçek insani çıkar olabilir, fakat aynı şeyi ölçmez.",
            "Mutluluğun tek sayısı yoktur. Günlük duygular, yaşam memnuniyeti ve hatırlanan hikaye farklı sorulara cevap verir. Birini ölçüp hepsini bildiğimizi sanmak hatadır.",
        ], "BEŞİNCİ KISIM · İKİ BENLİK"),
        entry("Kitabın sınırları ve tekrarlama tartışması", [
            "Kitabın ana omurgası karar bilimine büyük katkı yaptı, fakat içindeki her deney aynı güçte değildir. Özellikle insanların davranışını küçük kelime veya çevre ipuçlarıyla değiştirdiği iddia edilen bazı sosyal hazırlama sonuçları daha büyük tekrar çalışmalarında zayıf ya da tutarsız çıktı.",
            "Kahneman da araştırmacıları daha sağlam tekrarlar yapmaya çağırdı. Bu gelişme kitabı çöpe atmaz; bilimde bir paketin içindeki bulguların ayrı ayrı tartılması gerektiğini gösterir. Çapa, kayıp çerçevesi veya taban oranı gibi alanların kanıt yapısı da kendi içinde değerlendirilmelidir.",
            "Sistem 1 ve 2 fiziksel beyin haritası değildir. Hızlı düşünme her zaman kötü, yavaş düşünme her zaman doğru değildir. Uzun uzun düşünen insan da yanlış veri, çıkar veya önyargıyla kötü karar verebilir.",
            "Yanlılık listesi başkalarını küçümseme aracına dönüşebilir. En kolay yanlılık, kendimizi tarafsız gözlemci saymaktır. İyi kullanım, etiketi karşıdakine yapıştırmadan önce süreç, veri ve geri bildirim düzenini iyileştirmektir.",
            "Kitabın kalıcı hediyesi kusursuz zihin vaadi değil, hatanın öngörülebilir olduğu yerlerde çevreyi daha iyi tasarlama alışkanlığıdır.",
        ], "SINIRLAR VE BUGÜN"),
        entry("Bir dakikalık harita", [
            "Hızlı düşünme çağrışımlı, otomatik ve ucuzdur; yavaş düşünme dikkat, hesap ve denetim ister. Zihin çoğu zaman zor sorunun yerine kolayını cevaplar ve elindeki az bilgiden tutarlı hikaye kurar.",
            "Çapalar tahmini, bulunabilir örnekler risk duygusunu, temsili profiller taban oranı kullanımını etkiler. Küçük örnekler şansı büyütür, aşırı sonuçlar ortalamaya dönebilir, sonuç bilgisi geçmişi kaçınılmaz gösterir ve içeriden bakış projeyi olduğundan kolay hissettirir.",
            "Kararlar referans noktasına bağlıdır; kayıp çoğu zaman eşit kazançtan ağır gelir ve aynı sonuç farklı çerçevede farklı hissedilir. Deneyimleyen ben ile hatırlayan ben aynı mutluluk hesabını yapmaz. Çözüm her zaman daha çok düşünmek değil; kontrol listesi, taban oranı, dışarıdan bakış, bağımsız tahmin ve iyi geri bildirimdir.",
        ], "SONUÇ"),
        entry("Akılda kalacak beş görüntü", [
            "Sopa ve top: İlk cevap kontrol ister. Projektör: Dikkat dar alanı görür. Fiyat çapası: İlk sayı cetveli büker. Küçük hastane: Az veri çok sallanır. Kahve kupası: Sahiplik kaybın ağırlığını değiştirir.",
            "Bir karar çok önemliyse bu beş görüntüyle kısa tur yapın. Cevabım fazla mı akıcı? Neyi görmüyorum? Başlangıç sayısını kim koydu? Örnek yeterli mi? Vazgeçmeyi kayıp saydığım için mi tutunuyorum?",
            "Amaç sezgiyi susturmak değildir. Sezgi hayatı taşır; iyi düzenlenmiş yavaş kontrol, yalnızca uçurum kenarlarında korkuluk olur.",
        ], "SONUÇ"),
    ],
})


BOOKS.append({
    "bookNo": 95,
    "title": "Prens",
    "author": "Niccolò Machiavelli",
    "subtitle": "İktidarın nasıl kurulduğunu, neden çöktüğünü ve ahlak ile zorunluluk arasındaki karanlık gerilimi Rönesans İtalya'sının sahneleriyle anlatan rehber.",
    "coverImage": "/images/summary-art-95-prens-v2.webp",
    "coverStyle": "artwork",
    "pdfUrl": "/data/pdfs/95-prens-ozeti.pdf",
    "pdfLabel": "25-50 sayfalık PDF'yi indir",
    "longForm": True,
    "chapterArtStyle": "monochrome-engraving",
    "chapterArtColor": "#774D3E",
    "meta": {
        "originalTitle": "Il Principe",
        "compiler": "Zihin Gezgini · Yapay zeka destekli çalışma",
        "date": "Temmuz 2026",
        "language": "Türkçe",
    },
    "intro": "Prens çoğu zaman 'kötü olmanın el kitabı' diye anılır. Oysa kitap daha rahatsız edici bir şey yapar: Bir hükümdarın iyi niyetinden çok, davranışının devleti gerçekten koruyup korumadığına bakar. Machiavelli parçalanmış, istilaya açık ve sürekli ittifak değiştiren Rönesans İtalya'sında yazıyordu. Bu rehber onun kalıtsal ve yeni devletler, halk ile seçkinler, kendi ordusu, görünüş, korku, talih ve siyasi beceri üzerine bütün ana tezlerini sahnelerle anlatıyor. Aynı zamanda Prens'i kişisel ilişkilerde acımasızlığı haklı çıkaran reçete gibi kullanmanın yanlışlığını, yazarın cumhuriyetçi düşüncesini ve dönemin erkek egemen şiddet dilini de görünür kılıyor.",
    "sources": [
        {"id": 1, "title": "Project Gutenberg - Prens tam metin ve bölüm yapısı", "url": "https://www.gutenberg.org/files/1232/1232-h/1232-h.htm"},
        {"id": 2, "title": "Project Gutenberg - Prens kitap sayfası", "url": "https://www.gutenberg.org/ebooks/1232"},
        {"id": 3, "title": "Stanford Encyclopedia of Philosophy - Machiavelli, virtù, fortuna ve cumhuriyetçilik", "url": "https://plato.stanford.edu/archives/fall2024/entries/machiavelli/"},
    ],
    "entries": [
        entry("Bu kitap nasıl okunmalı?", [
            "Prens'i okurken önce iki soruyu ayırmak gerekir: Machiavelli siyasette gerçekte ne olduğunu mu anlatıyor, yoksa hükümdara ne yapması gerektiğini mi söylüyor? Kitap iki işi sık sık birbirine yaklaştırır ve rahatsızlık tam burada doğar.",
            "Metindeki 'prens' masal kahramanı değil, devletin tek yöneticisidir. 'Erdem' diye çevrilen virtù da yalnız ahlaki iyilik değildir; cesaret, esneklik, karar gücü, zamanlama ve koşullara biçim verme becerisini içerir.",
            "Bu rehber cümleleri günümüz ilişkilerine reçete olarak taşımayacak. Devlet zorunun aile, arkadaşlık ve işyeri için normal davranış sayılması istismarı aklayabilir. Önce tarih sahnesini, sonra iddiayı, en son sınırını göreceğiz.",
        ], "BAŞLANGIÇ"),
        entry("Kırık İtalya haritası", [
            "Machiavelli'nin İtalya'sı tek bir devlet değildi. Floransa, Venedik, Milano, Papalık Devleti, Napoli ve daha küçük güçler rekabet ediyor; Fransa, İspanya ve Kutsal Roma İmparatorluğu müdahale ediyordu. Bugün dost olan yarın kapıya ordu getirebilirdi.",
            "Machiavelli Floransa Cumhuriyeti'nde görev yaptı, elçiliklerde yöneticileri yakından gördü. Medici ailesi iktidara dönünce görevden alındı, hapsedildi ve siyaset dışına itildi. Prens bu yenilginin ardından 1513'te yazıldı.",
            "Bir apartmanda yönetim her hafta el değiştirirken dışarıdan güçlü şirketlerin binayı paylaşmaya çalıştığını düşünün. Nezaket yetmez; borç, güvenlik, ittifak ve içerideki gruplar aynı anda yönetilmelidir. Kitabın sertliği böyle bir aciliyet duygusundan gelir.",
            "Bu bağlam her cümleyi doğru yapmaz, fakat neden düzeni en yüksek iyi gibi gördüğünü açıklar. Machiavelli için dağılmış ülke yalnız siyasi kusur değil, yabancı güce açık yaradır.",
            "Kırık harita kitabın arka planıdır: Güç üzerine düşünce huzurlu çalışma odasında değil, kaybedilmiş bir devletin enkazında doğar.",
        ], "BİRİNCİ KISIM · DEVLETİ KURMAK", art="fragmented-italy", caption="Parçalanmış ve dış güçlere açık Rönesans İtalya'sı, Prens'in sürekli güvenlik ve birlik arayışını açıklar."),
        entry("Eski ev ile yeni ev aynı yönetilmez", [
            "Kalıtsal hükümdarlıkta insanlar ailenin adını, törenini ve kurallarını bilir. Yönetici ağır bir hata yapmazsa alışkanlık ona destek olabilir. Yeni ele geçirilen devlette ise her karar karşılaştırılır ve eski düzenin özlemi canlıdır.",
            "Yeni taşındığınız mahallede yıllardır çalışan bakkalı devraldığınızı düşünün. Rafları değiştirir, eski çalışanları çıkarır ve fiyatları yükseltirseniz yalnız bugünkü müşteriyi değil, anısını da karşınıza alırsınız. Yeni güç henüz alışkanlık üretmemiştir.",
            "Machiavelli devlet türlerini ayırarak başlar çünkü tek reçete vermek istemez. Miras kalan ülke, yeni fetih, karma devlet, eski cumhuriyet ve dini yönetim farklı direnç taşır.",
            "Bu sınıflandırmanın basit dersi hâlâ güçlüdür: Bir kurumun geçmişi bugünkü seçeneğin maliyetini belirler. Kağıt üzerindeki aynı değişiklik, iki yerde aynı tepkiyi doğurmaz.",
            "Yönetici önce hangi eve girdiğini anlamalıdır. Kilit eskiyse yeni anahtarın parlaması işe yaramaz.",
        ], "BİRİNCİ KISIM · DEVLETİ KURMAK", art="old-and-new-house", caption="Kalıtsal devlet alışkanlığın desteğini taşır; yeni devlet ise eski düzenin hafızası ve yeni beklentilerle aynı anda uğraşır."),
        entry("Karma devletin iki hafızası", [
            "Bir hükümdar ülkesine yeni bir bölge eklediğinde ortaya karma devlet çıkar. Yeni halk, eski yöneticiden hoşnutsuz olduğu için kapıyı açmış olabilir; fakat yeni yönetim bütün beklentileri karşılayamaz. Değişimi isteyenler de kısa sürede hayal kırıklığı yaşayabilir.",
            "Machiavelli dil, gelenek ve kurum benzerse eski hanedanı kaldırıp yerel düzeni büyük ölçüde korumayı önerir. Farklı bölgede ise yöneticinin orada bulunmasını, sorun büyümeden görmesini veya yerleşimler kurmasını tartışır.",
            "Yeni patron uzaktan yalnız rapor okursa küçük kızgınlıklar geç fark edilir. Sahaya yakınlık bilgiyi hızlandırır; fakat işgal mantığı ve zorla yerleşim yerel halk için ağır adaletsizlik doğurabilir. Yazarın devlet gözü, maruz kalanların acısını çoğu kez ikincil görür.",
            "Karma devlet iki hafızayla yaşar: Eski düzenin kaybı ve yeni düzenin verdiği söz. Başarısızlık, yalnız bugünkü hizmetle değil, bu iki karşılaştırmayla ölçülür.",
            "Fetih haritada tek renk olabilir; insanların zihninde sınır çok daha uzun süre kalır.",
        ], "BİRİNCİ KISIM · DEVLETİ KURMAK", art="mixed-principality", caption="Yeni katılan bölge, eski düzenin özlemiyle yeni yönetime bağlanan umudu birlikte taşır; fetih hafızayı hemen silmez."),
        entry("Kendi kılıcın mı, ödünç zırh mı?", [
            "Machiavelli iktidarın kendi gücüyle mi, başkasının silahı veya lütfuyla mı kurulduğunu sorar. Başkasının ordusuyla yükselen kişi, zaferden sonra bile o güce bağımlıdır. Ödünç merdiven sahibi çekilince düşebilir.",
            "Bir şirket bütün temel işini tek dış tedarikçiye bırakırsa kısa vadede hız kazanır. Tedarikçi fiyatı yükselttiğinde veya rakibe geçtiğinde şirketin adı kendine, kasları başkasına ait olur. Siyasi bağımlılık da buna benzer.",
            "Kendi kaynaklarıyla yükselmek daha zor ve yavaştır. Fakat kurum, sadakat ve öğrenme içeride birikir. Machiavelli Musa, Romulus ve başka kurucu örneklerle fırsat kadar örgütleme becerisini vurgular.",
            "'Kendi silahı' yalnız kaba kuvvet diye okunmamalıdır. Vergi toplama, yönetim bilgisi, halk desteği ve güvenilir kurum da bağımsız kapasitedir. Yalnız kişiye bağlı güç ise ölümünde dağılabilir.",
            "Ödünç zırh parlak görünür, fakat bedeninize uymaz. Kitabın kalıcı uyarılarından biri kapasite ile gösterişi ayırmaktır.",
        ], "BİRİNCİ KISIM · DEVLETİ KURMAK", art="own-arms", caption="Başkasının gücüyle kazanılan iktidar ödünç zırh gibidir; hızlı korur ama sahibi vazgeçtiğinde bedeni savunmasız bırakır."),
        entry("Virtù: İyi çocuk olmak değil, koşula biçim vermek", [
            "Machiavelli'nin virtù sözcüğü Türkçedeki erdemden daha sert ve geniştir. Liderin fırsatı görmesi, hızla karar vermesi, cesaret göstermesi ve yöntemini hava değişince değiştirebilmesi anlamına gelir.",
            "Bir kaptan sakin denizde nazik rota izleyebilir; fırtınada aynı hareket yetersiz kalır. Sorun nazikliğin kötü olması değil, tek davranışın her havaya uymamasıdır. Machiavelli esnekliği başarı için merkezi görür.",
            "İnsanlar kendilerine geçmişte başarı getiren tarza bağlanır. Tedbirli kişi fırsat anında ağır kalır, saldırgan kişi geri çekilmesi gereken yerde duvara çarpar. Talih değişir ama huy aynı kaldığında uyumsuzluk doğar.",
            "Bu beceri ahlaki değerden bağımsız anlatıldığı için tehlikelidir. Etkili olmak iyi olmak demek değildir. Bir zorba da koşulları ustaca okuyabilir; sonuçta oluşan düzenin adil olup olmadığı ayrıca sorulmalıdır.",
            "Virtù, taşı tek darbede kıran güçten çok hangi taşı, hangi açıyla ve hangi anda yontacağını bilmektir.",
        ], "İKİNCİ KISIM · GÜCÜ KORUMAK", art="virtu-sculptor", caption="Virtù, sabit bir iyi huydan çok koşulu okuma, zamanı yakalama ve yöntemi değiştirme becerisidir."),
        entry("Cesare Borgia'nın parlak ve karanlık laboratuvarı", [
            "Prens'in en unutulmaz kişisi Cesare Borgia'dır. Babası Papa VI. Alexander'ın desteğiyle Orta İtalya'da güç kazanır, rakiplerini bölüp etkisizleştirir ve düzensiz Romagna bölgesini kontrol altına almaya çalışır.",
            "Borgia sert yönetici Remirro de Orco'yu düzen kurmak için kullanır, sonra halkın nefretini ondan ayırmak için onu acımasız biçimde ortadan kaldırır. Machiavelli bu sahneyi siyasi hesap ve görünüş yönetimi örneği olarak sunar.",
            "Hikaye hayranlık kadar dehşet uyandırmalıdır. Bir insanı araç olarak kullanıp sonra halka gösteri için feda etmek, etkili görünse bile ahlaki cinayettir. Kitabı anlamak, yazarın soğuk değerlendirmesini onaylamak değildir.",
            "Borgia gelecekteki papalık seçimini de hazırlamaya çalışır, fakat babasının ölümü ve kendi hastalığı planı bozar. Machiavelli'ye göre çoğu önlemi almış, yine de olağanüstü talih darbesine yenilmiştir.",
            "Borgia satranç ustası gibidir; fakat tahta taş değil insanlardan oluşur. Bu ayrıntı, siyasi etkinliğin ahlaki maliyetini görünür tutar.",
        ], "İKİNCİ KISIM · GÜCÜ KORUMAK", art="borgia-chessboard", caption="Cesare Borgia güç kurma becerisinin örneğidir, fakat insanları araçlaştıran yöntemleri siyasi etkinlik ile ahlak arasındaki uçurumu gösterir."),
        entry("Bir kez kullanılan sertlik, her gün açılan yara", [
            "Machiavelli sertliğin iyi veya kötü kullanılmasından söz eder. 'İyi' sözcüğü burada ahlaki övgü değil, iktidarı koruma ölçüsüdür. Zorunlu görülen zararların başta ve bir defada, yararların ise zamanla verilmesini önerir.",
            "Her hafta yeni ceza uygulanan mahallede insanlar yarın kimin hedef olacağını bilmez. Korku tek olaya değil, gündelik havaya dönüşür. Sürekli yara yönetimi istikrar değil, sessiz bir patlama üretir.",
            "Bir defalık şiddetin de kurban için 'iyi' olmadığını açık tutmalıyız. Machiavelli yönetici gözünden toplumsal tepkiyi hesaplar; adalet, hak ve travma açısından değerlendirme daha geniş bir ahlak çerçevesi ister.",
            "Yazarın sezgisi, belirsiz ve keyfi cezanın devleti çürüttüğüdür. Modern hukuk bunu farklı bir dille, önceden bilinen kural, ölçülülük ve bağımsız yargı gereğiyle sınırlar.",
            "Yaranın kapanması için bıçağın durması gerekir. Fakat en iyi siyaset, önce bıçağın gerçekten zorunlu olup olmadığını sorgular.",
        ], "İKİNCİ KISIM · GÜCÜ KORUMAK", art="cruelty-scars", caption="Sürekli ve keyfi sertlik korkuyu gündelik havaya çevirir; siyasi hesap ile kurbanın ahlaki hakkı aynı ölçü değildir."),
        entry("Halk ile seçkinlerin terazisi", [
            "Machiavelli her şehirde iki temel istek görür: Seçkinler yönetmek ve baskı kurmak ister; halk ise baskı görmemek ister. Sivil prens bu çatışmanın içinden, ya seçkinlerin ya halkın desteğiyle yükselir.",
            "Seçkinlerin sayısı azdır ama kaynakları, bağlantıları ve yönetim tutkuları büyüktür. Halk kalabalıktır ve temel isteği daha sınırlıdır. Bu yüzden Machiavelli halk desteğini daha güvenilir temel sayma eğilimindedir.",
            "Bir apartmanda birkaç büyük mülk sahibi yönetimi kontrol etmek, yüz kiracı ise huzur ve adil aidat ister. Yönetici yalnız güçlü azınlığa yaslanırsa çoğunluğun sessiz öfkesini biriktirir.",
            "Halkı desteklemek demokrasi kurmakla aynı şey değildir; Prens yine tek yöneticiyi düşünür. Fakat iktidarın yalnız saray çevresinden değil, yönetilenlerin kabulünden beslendiğini görmesi önemlidir.",
            "Terazi tamamen dengelenmez. Siyaset, farklı isteklerin kalıcı gerilimini yönetme işidir.",
        ], "İKİNCİ KISIM · GÜCÜ KORUMAK", art="people-and-elites", caption="Seçkinler yönetmek, halk ezilmemek ister; prensin dayanıklılığı bu iki farklı talep arasındaki temele bağlıdır."),
        entry("Paralı askerin boş zırhı", [
            "İtalyan şehir devletleri sık sık paralı asker birliklerine dayanıyordu. Machiavelli onları çıkarcı, disiplinsiz ve tehlikeli bulur: Barışta devlete yük, savaşta kaçmaya hazır, zaferde ise yönetime tehdit olabilirler.",
            "Paralı askerin en güçlü bağlılığı ücret sözleşmesinedir. Karşı taraf daha çok verirse veya savaş riski büyürse amaç ayrışabilir. Savunma gibi varlık meselesini tümüyle dışarıya vermek, kaderin anahtarını kiraya çıkarmaktır.",
            "Yardımcı birlik daha da risklidir: Başka hükümdarın güçlü ordusu gelir, yenilirse siz kaybedersiniz; kazanırsa size hükmedebilir. Zafer bile bağımlılık üretir.",
            "Modern devlet ile Rönesans ordusu aynı değildir. Yine de kritik altyapı, veri, enerji veya uzmanlığı tek dış aktöre bağlama sorusu bugün de tanıdıktır. Esneklik ile temel kapasite arasında denge gerekir.",
            "Boş zırh uzaktan ordu gibi görünür. Yaklaştığınızda içinde sizin iradeniz değil, başkasının çıkarı vardır.",
        ], "ÜÇÜNCÜ KISIM · SAVAŞ VE HAZIRLIK", art="mercenary-armor", caption="Paralı ve yardımcı ordular güç görüntüsü verir, fakat en kritik anda bağlılıklarının başka bir merkeze ait olduğu anlaşılabilir."),
        entry("Barış gününde savaş çalışmak", [
            "Machiavelli prensin savaş sanatını ana işi sayar. Barış zamanında araziyi tanımasını, bedenini hazırlamasını, tarihi komutanların kararlarını incelemesini ister. Çünkü kriz geldiğinde öğrenmeye başlamak geçtir.",
            "Yangın sırasında ilk kez tahliye planı yazılmaz. Tatbikat, harita ve sorumluluk dağılımı sakin günde yapılır. Kitabın askeri dili bugün afet, siber saldırı veya salgın hazırlığına daha barışçıl biçimde çevrilebilir.",
            "Fakat her şeyi savaş gibi görmek de tehlikelidir. Muhalifi düşman, eleştiriyi saldırı sayan yönetim öğrenme kanallarını kapatır. Hazırlık, sürekli savaş psikolojisi yaratmak değildir.",
            "Tarih okumak Machiavelli için örnek deposudur. Akıllı yönetici geçmişi kopyalamaz; benzer koşullarda hangi kararın neden çalıştığını inceler. Benzetmenin sınırını da bilmelidir.",
            "Barış, hazırlığın zıddı değil fırsatıdır. Güvenli köprü fırtına başlamadan güçlendirilir.",
        ], "ÜÇÜNCÜ KISIM · SAVAŞ VE HAZIRLIK", art="peace-training", caption="Krizde ilk kez öğrenmek geçtir; sakin zaman araziyi tanıma, tatbikat yapma ve geçmiş örnekleri sorgulama zamanıdır."),
        entry("Sevilmek mi, korkulmak mı?", [
            "Machiavelli ikisinin bir arada olmasının iyi olduğunu, fakat seçim zorunluysa korkulmanın daha güvenli olabileceğini söyler. İnsan sevgisinin çıkar değişince çözülebileceğini, ceza korkusunun daha öngörülebilir bağ kurduğunu düşünür.",
            "Bu cümle kitabın en çok koparılan parçasıdır. Hemen ardından nefret edilmekten kaçınmayı şart koşar. Korku ile nefret aynı değildir; keyfi hakaret, mala ve onura saldırı iktidarı içeriden çürütür.",
            "Yine de korkuyla yönetim ciddi sorun taşır. İnsanlar kötü haberi saklar, yaratıcılık azalır ve yönetici gerçek desteği sessizlik sanır. Modern kurumlar sürdürülebilir güveni kural, hesap verebilirlik ve katılımla kurmaya çalışır.",
            "Ailede veya işyerinde bu cümleyi tehdit hakkı gibi kullanmak istismardır. Machiavelli'nin savaş içindeki devlet hesabı, kişisel ilişkide korkunun normal olduğu anlamına gelmez.",
            "Korku hızlı itaat üretebilir; güven ise doğruyu söyleyebilen bir çevre üretir. Kitabın sorusu güvenliği, bizim ek sorumuz insan onurunu da içermelidir.",
        ], "DÖRDÜNCÜ KISIM · GÖRÜNÜŞ VE İNSANLAR", art="love-fear-balance", caption="Machiavelli korkunun sevgiden güvenilir olabileceğini savunur ama nefret sınırını koyar; modern bakış korkunun bilgi ve onur maliyetini de görür."),
        entry("Aslanın gücü, tilkinin gözü", [
            "Yönetici hem aslan hem tilki olmalıdır: Aslan kurtları korkutur ama tuzağı göremez; tilki tuzağı görür ama kurtları kaçıramaz. Güç ile kurnazlık birbirinin eksik yanını tamamlar.",
            "Yalnız sert davranan kişi kandırılabilir, yalnız pazarlık yapan kişi açık saldırıda savunmasız kalabilir. İyi strateji tehdidin türünü ayırt etmeyi gerektirir. Her sorun çekiç görünüyorsa elde yalnız çekiç vardır.",
            "Machiavelli sözün tutulmasını da sonuç açısından tartışır. Karşı taraf sözü bozduğunda ve koşullar değiştiğinde prensin bağlı kalmayabileceğini söyler. Bu, güvenin uzun vadeli değerini küçümseyebilir.",
            "Sözlerin kolay bozulduğu sistemde herkes sözleşme, denetim ve silaha daha çok para harcar. Kısa vadeli tilki başarısı uzun vadede güven piyasasını yok edebilir. Kurumlar tam da kişisel kurnazlığı sınırlamak için vardır.",
            "Aslan ve tilki canlı bir benzetmedir; eksik üçüncü hayvan belki hafızası güçlü fildir. İnsanlar aldatmayı unutmaz.",
        ], "DÖRDÜNCÜ KISIM · GÖRÜNÜŞ VE İNSANLAR", art="lion-and-fox", caption="Aslan açık tehdide, tilki gizli tuzağa karşıdır; tek davranış biçimi değişen siyasi tehlikeleri yönetmeye yetmez."),
        entry("Görünmek ile olmak arasındaki maske", [
            "Machiavelli insanların çoğunun yöneticinin iç dünyasını değil, görünen davranış ve sonucu değerlendirdiğini söyler. Prens merhametli, sadık, dürüst ve dindar görünmeli; gerekirse tersini yapabilmelidir.",
            "Bu öneri siyasetin sahne yönünü acımasızca açığa çıkarır. Tören, kıyafet, slogan ve fotoğraf yalnız süs değil, meşruiyet üretimidir. Uzakta yaşayan halk yöneticiyi çoğunlukla aracılı görüntülerden tanır.",
            "Fakat görünüş gerçeği sonsuza dek örtemez. Politikanın sonuçları mutfak fiyatında, mahkeme kararında ve güvenlikte hissedilir. İletişim ile gerçek arasındaki mesafe büyüdükçe maskeyi taşımak pahalılaşır.",
            "Modern medya görüntü yönetimini katladı, aynı zamanda kayıt ve karşı anlatı imkanını da artırdı. Bir fotoğraf güçlü olabilir; çelişen bin telefon görüntüsü maskeyi parçalayabilir.",
            "Machiavelli'nin aynası rahatsız eder çünkü erdemin kendisiyle erdem görüntüsünün siyasi piyasada aynı değeri taşımadığını söyler. Okurun görevi bu farkı normalleştirmek değil, denetlenebilir kılmaktır.",
        ], "DÖRDÜNCÜ KISIM · GÖRÜNÜŞ VE İNSANLAR", art="public-mask", caption="Siyasi görünüş meşruiyet üretir, fakat maskeyle gündelik sonuç arasındaki mesafe büyüdükçe güven kırılır."),
        entry("Mala ve onura dokunma", [
            "Machiavelli nefretin güçlü kaynakları arasında insanların malına ve aile onuruna saldırmayı sayar. İnsanların babalarının ölümünü mallarının kaybından daha çabuk unutabileceğini söyleyen karanlık abartısı, mülkiyetin siyasi ağırlığını vurgular.",
            "Ev yalnız ekonomik varlık değildir; emek, güvenlik ve aile hafızasıdır. Keyfi el koyma, bugün zengin görünen bir kurbanın ötesinde herkese 'sıra bana gelebilir' mesajı verir. Yatırım ve sadakat çözülür.",
            "Machiavelli özel hayatın sınırını da iktidar hesabıyla korur. Modern hak anlayışı ise insan onurunu yöneticinin çıkarından bağımsız değer sayar. Aynı davranışa farklı gerekçeyle karşı çıkılır.",
            "Vergi ile keyfi yağma aynı şey değildir. Öngörülebilir, genel ve denetlenebilir kural siyasi topluluğun giderini paylaşabilir; kişinin düşmanına göre değişen el koyma korku üretir.",
            "Korunan ev görüntüsü, devletin yalnız sınır değil gündelik güven duygusu olduğunu hatırlatır.",
        ], "DÖRDÜNCÜ KISIM · GÖRÜNÜŞ VE İNSANLAR", art="protected-home", caption="Keyfi biçimde mala ve özel onura dokunmak tek kurbanı değil, herkesin yarın duygusunu tehdit ederek nefreti büyütür."),
        entry("Danışman çemberi ve dalkavuk tuzağı", [
            "Bir hükümdarın aklı, seçtiği danışmanlardan anlaşılır. Bilgili ve devlete bağlı kişiler çevresindeyse iyi yargı ihtimali artar; yalnız kendi çıkarını düşünen bakan, efendisini de zayıflatır.",
            "Fakat sarayda kötü haber vermek tehlikeliyse herkes hoş cümle üretir. Yönetici övgüyü gerçeklik sanır, kararlar körleşir. Machiavelli dalkavuklardan kaçmak için belirli bilge kişilere doğruyu söyleme izni verilmesini önerir.",
            "İzin yetmeyebilir. Lider, kötü haberi getiren kişiyi cezalandırıyorsa duvardaki 'açık kapı' yazısı kimseyi içeri sokmaz. Psikolojik güven davranışla kurulur.",
            "Machiavelli son kararın prense ait kalmasını ister; danışman herkesin rüzgarıyla savrulmamalıdır. Fakat modern karmaşık toplumda bağımsız kurum ve özgür basın, tek kişinin seçtiği çemberden daha geniş düzeltme sağlar.",
            "İyi danışman aynadır, makyajcı değil. Aynayı kırmak yüzü değiştirmez.",
        ], "DÖRDÜNCÜ KISIM · GÖRÜNÜŞ VE İNSANLAR", art="advisor-circle", caption="Yönetici hoş sözle çevrilirse gerçekliği kaybeder; iyi danışman iktidarın duymak istemediği haberi de güvenle taşıyabilmelidir."),
        entry("Talih taşan bir nehir gibi", [
            "Machiavelli talihi taşkın nehre benzetir. Sular kabardığında ovayı yıkar; fakat sakin zamanda set, kanal ve köprü hazırlanabilir. Şans her şeyi yönetmez, hazırlıksızlığın vereceği zararı büyütür.",
            "Bu benzetme Borgia'nın öyküsünü açıklar. Becerisi çok sayıda taşı yerleştirmiştir, fakat papanın ani ölümü ve kendi hastalığı sel gibi gelir. Sonuç yalnız yetenek veya yalnız şans değildir.",
            "İnsan başarıyı bütünüyle kendine, yenilgiyi bütünüyle talihe yazmaya eğilimlidir. Nehir görüntüsü iki kolay hikayeyi de bozar. Yağmuru durduramazsınız, fakat taşkın yatağına ev yapıp yapmamak seçiminizdir.",
            "Machiavelli'nin talih hakkında kadınları aşağılayan, dönemin cinsiyetçi şiddet dilini kullanan benzetmeleri vardır. Bunları cilalamadan belirtmek gerekir; siyasi içgörü aşağılayıcı dili zorunlu kılmaz.",
            "Talih kaprislidir, virtù hazırlıktır. Yine de en yüksek set bile her seli durdurmaz; siyasi alçakgönüllülük buradan başlar.",
        ], "BEŞİNCİ KISIM · TALİH VE SON", art="fortune-river", caption="Talih taşan nehir gibidir; yağmuru seçemeyiz ama sakin zamanda set kurmak ve yerleşim yerini düşünmek elimizdedir."),
        entry("Kitap ahlaksızlığı mı öğretiyor?", [
            "Prens ahlakı yok saymaz; ahlaki iyilik ile siyasi sonucun her zaman örtüşmediğini söyler. Merhamet görüntüsü büyük kargaşaya yol açabilir, sınırlı sertlik daha fazla ölümü önleyebilir iddiasını tartışır. Sorun, sonucu kimin ve nasıl ölçtüğüdür.",
            "Yalnız niyetle yetinmemek değerlidir. Fakat 'devlet için gerekliydi' sözü denetimsiz bırakılırsa her zalim kendine mazeret bulur. Gerekli olan ile iktidara yararlı olan kolayca karışır.",
            "Modern hukukta hak, yetki ayrılığı, seçim, özgür basın ve bağımsız yargı bu gerekçe tekelini sınırlar. Machiavelli'nin tek prensine bırakılan hesabı toplumun görünür tartışmasına açar.",
            "Kitabı verimli okumak için iki sütun tutun: Eylemin kısa vadeli etkisi ve insanlara yüklediği hak ihlali. Sadece bir sütun siyasi saflık, sadece öteki siyasi körlük yaratabilir.",
            "Prens bizi kötülüğe çağırmaktan çok, iyi adın kötü sonucu örtebildiği dünyayla yüzleştirir. Cevap ahlakı atmak değil, sonucu da ahlakın içine almaktır.",
        ], "SINIRLAR VE BAŞKA MACHIAVELLI"),
        entry("Machiavelli yalnız prenslerin yazarı değil", [
            "Machiavelli'nin Söylevler adlı geniş eserinde Roma Cumhuriyeti, yurttaş özgürlüğü, çatışan sınıflar ve karma yönetim üzerine düşünmesi Prens portresini değiştirir. Yazar yalnız tek adam yönetimini yücelten basit bir saray danışmanı değildir.",
            "Bazı yorumcular Prens'i Medici ailesine iş başvurusu, bazıları İtalya'yı birleştirme çağrısı, bazıları iktidarın sırlarını halka açan teşhir metni olarak okur. Tek niyet üzerinde tam uzlaşma yoktur.",
            "Cumhuriyetçi bağlam, halkın siyasal canlılığını ve kurumların tek liderden daha kalıcı oluşunu görünür kılar. Prens acil kurucu anı, Söylevler daha uzun özgürlük düzenini düşünür gibi okunabilir.",
            "Bu nedenle 'Makyavelist' kelimesini yalnız hilekar insan anlamında kullanmak yazarın düşünce alanını daraltır. Onun asıl yeniliği siyaseti kendi sonuçları, çatışmaları ve kurumlarıyla ayrı bir inceleme alanına çevirmesidir.",
        ], "SINIRLAR VE BAŞKA MACHIAVELLI"),
        entry("Dönemin kör noktaları", [
            "Prens neredeyse bütünüyle erkek hükümdarlar, ordular, fetihler ve seçkin çevreler üzerinden konuşur. Kadınlar siyasi özne olarak az görünür; talih benzetmesinde aşağılayıcı şiddet dili kullanılır. Bu dil tarihsel diye zararsızlaşmaz.",
            "Fethedilen halk çoğu zaman yönetilecek sorun, öldürülen rakip ise satranç taşı gibi anlatılır. Aşağıdan bakan tarih, aynı sahnelerde sürgün, açlık, yas ve kırılmış aile görür.",
            "Kitabın gücü soğuk siyasi sonucu görmesidir; kör noktası insanların değerini bazen yalnız bu sonuca etkileri kadar görmesidir. Günümüz okuru etkinlik sorusunu hak, eşitlik ve katılım sorusuyla tamamlamalıdır.",
            "Machiavelli'yi kendi yüzyılında konumlandırmak yargıyı kolaylaştırmak değil, hangi problemin ona ait, hangi kullanımın bize ait olduğunu ayırmaktır.",
        ], "SINIRLAR VE BAŞKA MACHIAVELLI"),
        entry("Bir dakikalık harita", [
            "Devletler aynı tür değildir: Kalıtsal, yeni, karma, sivil ve dini yönetim farklı direnç taşır. Yeni iktidar eski düzenin hafızasıyla uğraşır; başkasının lütfu ve ordusuyla yükselen kendi dayanağını kurmadıkça kırılgandır.",
            "Virtù koşulu okuma ve yöntem değiştirme becerisi, fortuna ise denetlenemeyen talih payıdır. Kendi kapasitesi, halk desteği, hazırlık, doğru danışman ve nefret üretmeme gücü dayanıklılığı artırır. Aslan açık tehdidi, tilki tuzağı temsil eder.",
            "Kitap iyi görünmekle iyi olmak, ahlaki niyetle siyasi sonuç arasındaki farkı açar. Fakat etkili olanı haklı saymak zorunda değiliz. Cumhuriyetçi eserleri ve dönemin kör noktalarıyla birlikte okunduğunda Prens bir zorbalık reçetesinden çok iktidarın tehlikeli anatomisi olur.",
        ], "SONUÇ"),
        entry("Akılda kalacak beş görüntü", [
            "Kırık İtalya haritası: Sertliğin tarih sahnesi. Ödünç zırh: Bağımlı güç. Aslan ve tilki: Kuvvet ile kurnazlık. Danışman aynası: Kötü haberi duyabilmek. Taşan nehir: Talih ve hazırlık.",
            "Bir siyasi iddiayı incelerken bu görüntülerle sorun: Hangi devlet türü konuşuluyor? Güç gerçekten kimin? Halkın desteği mi sessizliği mi var? Danışman doğruyu söyleyebiliyor mu? Şans payı başarı hikayesinden siliniyor mu?",
            "Machiavelli'nin asıl rahatsız edici dersi, iktidarın güzel sözcüklerden bağımsız sonuçlar ürettiğidir. Bizim ek dersimiz, sonucun insan hakkından bağımsız değerlendirilemeyeceğidir.",
        ], "SONUÇ"),
    ],
})


BOOKS.append({
    "bookNo": 185,
    "title": "Metaforlarla Yaşamak",
    "author": "George Lakoff ve Mark Johnson",
    "subtitle": "Metaforun şiirdeki süs değil, zamanı, tartışmayı, sevgiyi ve gündelik kararları düzenleyen görünmez düşünce haritası olduğunu anlatan rehber.",
    "coverImage": "/images/summary-art-185-metaforlarla-yasamak-v2.webp",
    "coverStyle": "artwork",
    "pdfUrl": "/data/pdfs/185-metaforlarla-yasamak-ozeti.pdf",
    "pdfLabel": "25-50 sayfalık PDF'yi indir",
    "longForm": True,
    "chapterArtStyle": "monochrome-engraving",
    "chapterArtColor": "#3E6770",
    "meta": {
        "originalTitle": "Metaphors We Live By",
        "compiler": "Zihin Gezgini · Yapay zeka destekli çalışma",
        "date": "Temmuz 2026",
        "language": "Türkçe",
    },
    "intro": "'Zaman harcadım', 'tartışmayı kazandı', 'ilişkimiz çıkmaza girdi' derken şiir yazdığımızı düşünmeyiz. George Lakoff ile Mark Johnson tam burada şaşırtıcı bir kapı açar: Metafor yalnız güzel söz değildir; soyut bir alanı daha somut başka bir alan üzerinden düşünüp yaşamamızı sağlar. Zaman para, tartışma savaş, sevgi yolculuk gibi haritalar hangi ayrıntıyı gördüğümüzü ve hangi çözümü doğal saydığımızı etkiler. Bu rehber kitabın yapısal, yönelimsel ve varlık metaforlarını, metonimiyi, beden deneyimini, tutarlılığı, yeni metaforları ve felsefi sonucunu gündelik sahnelerle anlatıyor. Son bölümde kültür farkları, karşılıklı etki ve her dil örneğinden doğrudan zihin yapısı çıkarma tehlikesi de ele alınıyor.",
    "sources": [
        {"id": 1, "title": "University of Chicago Press - Metaforlarla Yaşamak resmi kitap sayfası", "url": "https://press.uchicago.edu/ucp/books/book/chicago/M/bo3637992.html"},
        {"id": 2, "title": "Google Books - Metaphors We Live By bölüm yapısı", "url": "https://books.google.com/books/about/Metaphors_We_Live_By.html?id=r6nOYYtxzUoC"},
        {"id": 3, "title": "Cambridge - Metaforik yön ve dilin rolü üzerine eleştirel değerlendirme", "url": "https://www.cambridge.org/core/books/metaphor/metaphorical-directionality-the-role-of-language/7C6C7CFD05AB38448720656851EBBBF8"},
        {"id": 4, "title": "Cambridge - Metaforik çerçevelemenin etkileri üzerine meta-analiz", "url": "https://www.cambridge.org/core/journals/language-and-cognition/article/metaphorical-framing-in-political-discourse-through-words-vs-concepts-a-metaanalysis/865DFAB51172998E1C9574D74E275AAE"},
    ],
    "entries": [
        entry("Bu kitap nasıl okunmalı?", [
            "Kitap size gizli söz sanatlarını ezberletmeye çalışmaz. Gündelik dilde tekrar eden ifadeleri bir araya getirir ve bunların ortak bir düşünce düzeni kurup kurmadığını sorar. Tek cümleden değil, örüntüden ilerler.",
            "Metaforda iki alan vardır. Kaynak alan daha somut ve tanıdıktır; hedef alan açıklanmaya çalışılan soyut konudur. 'Zaman paradır' derken para dünyasındaki harcama, tasarruf ve bütçe ilişkileri zaman alanına taşınır.",
            "Bu harita bütün hedefi kapsamaz. Zaman para olabilir ama yalnız para değildir. Her metafor bazı yönleri aydınlatır, bazılarını gölgede bırakır. Kitabın en önemli alışkanlığı, hangi ışığın yandığını ve karanlıkta ne kaldığını sormaktır.",
        ], "BAŞLANGIÇ"),
        entry("Tartışma savaş mı, dans mı?", [
            "'Savını savundu', 'zayıf noktasına saldırdı', 'itirazını püskürttü', 'tartışmayı kazandı' deriz. Bu ifadeler tek tek tesadüf değildir; tartışmayı savaş üzerinden düzenleyen bir sistem oluşturur.",
            "Savaş haritasında karşıdaki rakiptir, düşünce mevzidir, cümle silahtır ve sonuç zafer veya yenilgidir. Bu düzen yalnız konuşma biçimini değil davranışı da etkiler: Açık aramak, geri adım atmamak ve son sözü almak doğal görünür.",
            "Şimdi tartışmayı dans gibi düşünün. Amaç karşıdakini yere sermek değil, hareketleri birbirine uydurarak birlikte yeni bir biçim üretmek olsun. Aynı anlaşmazlıkta soru sormak zayıflık değil ritmi anlamak olur.",
            "Lakoff ve Johnson başka kültürde tartışmanın gerçekten dans olarak yaşanabileceğini düşünmemizi ister. Bu bir tarih iddiasından çok zihinsel deneydir: Metafor değişirse eylemin anlamı da değişebilir.",
            "Savaş her tartışmada yanlış değildir; bazı çıkar çatışmaları gerçektir. Fakat tek harita olduğunda öğrenme ihtimalini yenilgi sanabiliriz.",
        ], "BİRİNCİ KISIM · GÖRÜNMEYEN HARİTALAR", art="argument-war-dance", caption="Tartışmayı savaş olarak kurmak saldırı ve savunmayı, dans olarak kurmak ortak ritim ve uyumu öne çıkarır."),
        entry("Tek sözcük değil, sistemli eşleştirme", [
            "Metafor bir kelimeyi başka kelimeyle değiştirmekten daha fazlasıdır. Bir alanın ilişkileri başka alana düzenli biçimde taşınır. Yolculukta başlangıç, hedef, engel, yön ve yol arkadaşı vardır; ilişkide başlangıç, ortak amaç, sorun ve birlikte ilerleme bunlara bağlanabilir.",
            "'İlişkimiz ilerlemiyor', 'aynı yolda değiliz', 'bir kavşağa geldik' ve 'çıkmazdayız' ifadeleri aynı haritanın parçalarıdır. Tek bir süslü benzetme değil, birbirini destekleyen cümle ailesi görürüz.",
            "Harita tam kopya değildir. Arabada yakıt biter ama ilişkide 'yakıt' bambaşka şeyler olabilir. Kaynak alandan yalnız bazı ilişkiler seçilir; benzetmeyi gereğinden fazla uzatırsak saçma sonuçlar çıkar.",
            "Bu sistemlilik, yeni cümleyi hiç duymadan anlamamızı sağlar. Biri 'Bu evlilikte direksiyon kimde?' dediğinde yolculuk ve araç bilgisini ilişkiye aktarırız.",
            "Metaforun gücü tek parlak kelimede değil, çok sayıda çıkarımı aynı anda taşıyan görünmez köprü ağındadır.",
        ], "BİRİNCİ KISIM · GÖRÜNMEYEN HARİTALAR", art="mapping-grid", caption="Kavramsal metafor tek sözcük değil; kaynak alandaki ilişkileri hedef alana düzenli biçimde taşıyan bir eşleştirme ağıdır."),
        entry("El feneri neyi gösterir, neyi saklar?", [
            "'Zaman paradır' dediğimizde zamanı sınırlı kaynak gibi görürüz. Toplantı zaman kaybettirir, yöntem zaman kazandırır, insan vaktini yatırıma dönüştürür. Ölçme ve planlama kolaylaşır.",
            "Aynı ışık başka özellikleri karartır. Zaman her zaman biriktirilemez, ödünç verilemez ve geri alınamaz. Bir arkadaşla amaçsızca oturmak ekonomik cetvelde israf, ilişki cetvelinde değer olabilir.",
            "Bir işletme çalışanı yalnız 'insan kaynağı' diye adlandırdığında beceri ve kapasiteyi görür, acı ve benzersiz yaşamı arka plana itebilir. Sözcük açıkça kötü değildir; fakat ışığın sınırı vardır.",
            "Eleştirel düşünme metaforu yasaklamak değildir, çünkü metaforsuz soyut düşünce çok zordur. Birden fazla el feneri kullanmaktır. Zaman bazen para, bazen mevsim, bazen akış, bazen armağan olarak görülebilir.",
            "Her etkili cümlede küçük bir soru saklayın: Bu ifade bana neyi çok net gösteriyor ve neyi görünmez yapıyor?",
        ], "BİRİNCİ KISIM · GÖRÜNMEYEN HARİTALAR", art="highlight-hide", caption="Metafor el feneri gibi bazı özellikleri parlatır, aynı anda hedef alanın başka yönlerini karanlıkta bırakır."),
        entry("Düşünceyi paketleyip göndermek", [
            "'Fikrimi cümleye koyamadım', 'sözlerin boş', 'mesaj ona ulaşmadı' dediğimizde iletişimi taşıma işi gibi kurarız. Düşünce nesne, sözcük kap, iletişim kanal ve dinleyici alıcı olur.",
            "Bu kanal metaforu çok kullanışlıdır. Metni dosyaya koyar, postayla yollar, alıcının açmasını bekleriz. Fakat anlam gerçekten kutunun içinde hazır duran eşya değildir. Dinleyici bağlama, geçmişine ve amacına göre yeniden kurar.",
            "Bir yönetici 'Mesajı açıkça verdim, anlamadıysa onun sorunu' diyebilir. Paket modeli bütün sorumluluğu alıcıya iter. Oysa aynı cümle iki ekip için farklı anlam taşıyabilir; geri bildirim iletişimin parçasıdır.",
            "Yanlış anlaşılmada yalnız kelimeyi tekrar etmek yerine ortak bağlamı kontrol etmek gerekir. 'Bunu duyunca ne anladın?' sorusu paketin teslim fişinden daha değerlidir.",
            "İletişim bazen gönderi, bazen ortak yemek pişirme gibidir. İkinci görüntü anlamın birlikte üretildiğini hatırlatır.",
        ], "BİRİNCİ KISIM · GÖRÜNMEYEN HARİTALAR", art="conduit-package", caption="Kanal metaforu düşünceyi sözcük paketine konan nesne gibi gösterir; anlamın dinleyiciyle birlikte kurulmasını gölgeleyebilir."),
        entry("Mutluluk yukarıda, keder aşağıda", [
            "Moralimiz yükselir, dibe vururuz, başımız dik gezer, çökeriz. Bunlar yönelimsel metaforlardır: Tek bir kavramı nesneye benzetmekten çok, bir kavramlar ailesini yukarı-aşağı gibi mekansal eksende düzenler.",
            "Beden deneyimi bu yönlere temel verebilir. Sağlıklı ve uyanık insan çoğunlukla ayakta, hasta veya ölü beden yataydır. Kontrol sahibi kişi üstte, kontrol edilen altta konumlanabilir. Fakat biyoloji tek başına bütün kültürel anlamı belirlemez.",
            "'Fiyatlar yükseldi' dediğimizde daha çok miktarı yukarıyla eşleriz. Bardaktaki sıvı arttıkça seviye yükselir; grafikler de bu bedensel deneyimi kullanır. Bir çizgiye bakıp ekonomik duyguyu hızla anlarız.",
            "Aynı yön farklı alanlarda ahlaki hiyerarşi yaratabilir: yüksek kültür, aşağı davranış, üst sınıf. Fiziksel yön toplumsal değer gibi görünmeye başlayınca eleştiri gerekir.",
            "Yukarı ve aşağı yalnız sözlükte değil, beden, grafik, bina ve kurum düzeninde birlikte yaşar.",
        ], "İKİNCİ KISIM · BEDEN VE NESNELER", art="orientation-up-down", caption="Yukarı-aşağı yönü beden deneyiminden duyguya, miktara ve toplumsal değere uzanan geniş bir kavram ailesini düzenler."),
        entry("Sınırı çizince içi ve dışı doğar", [
            "İnsan bedeni derisiyle çevrilidir; kendimizi bir iç ve dışa sahip olarak yaşarız. Bu temel deneyim görüş alanını, odayı, toplantıyı, durumu ve duyguyu kap gibi düşünmeye uzanır.",
            "'Belaya girdim', 'depresyondan çıktı', 'toplantının içindeyiz', 'görüş alanımda' deriz. Soyut durum bir kap, kişi onun içindeki nesne olur. Sınırı geçtiğinde durum değişmiş sayılır.",
            "Kap metaforu kategorileri kolaylaştırır. Bir davranış yasanın içinde mi dışında mı? Fakat doğadaki birçok sınır yumuşaktır. Bir insan ne zaman yaşlılık kategorisine girer? Çizgi idari olarak gerekli olabilir, gerçekliği keskinleştirebilir.",
            "Bir ekip 'bizim içimizden' ve 'dışarıdakiler' diye konuştuğunda aidiyet koruma sağlar, aynı zamanda yabancılaştırma üretebilir. Fiziksel sınır ahlaki sınır gibi işlemeye başlar.",
            "Kap faydalıdır ama duvar değildir. Hangi çizginin doğal, hangisinin bizim kararımız olduğunu ayrıca sormak gerekir.",
        ], "İKİNCİ KISIM · BEDEN VE NESNELER", art="container-boundary", caption="Bedenin iç-dış deneyimi durumları ve grupları kap gibi düşünmemizi sağlar; çizilen sınır bazen gerçeği olduğundan keskin gösterir."),
        entry("Enflasyon canavarı kimin eylemini saklıyor?", [
            "'Enflasyon kazancımızı yedi', 'hayat ona ihanet etti', 'teori gerçeği açıklıyor' derken soyut olaya kişilik veririz. Kişileştirme, karmaşık süreci niyet sahibi bir varlık gibi kavramayı kolaylaştırır.",
            "Canavar görüntüsü tehlikenin hızını ve korkusunu anlatabilir. Fakat fiyatları belirleyen şirketler, para politikası, arz sorunu ve gelir dağılımı gibi farklı aktörleri tek yaratığın arkasında saklayabilir.",
            "Kişileştirme yalnız masal değildir. 'Kanser vücuda saldırıyor' ifadesi tedaviyi savaş olarak kurar; bazı hastalara mücadele gücü verir, bazılarına hastalık ilerlerse yenilmişlik ve suçluluk hissettirebilir.",
            "Soyut sürece yüz vermek hafızayı güçlendirir. İyi kullanım, yüzün altında mekanizma olduğunu unutmamaktır. Canavarın dişlerini saymak yetmez; onu hangi koşulların beslediğini araştırmak gerekir.",
            "Metafor faili gösterebilir de saklayabilir de. Bu nedenle canlı anlatımın ardından düz bir neden listesi istemek yararlıdır.",
        ], "İKİNCİ KISIM · BEDEN VE NESNELER", art="personified-inflation", caption="Enflasyonu canavar gibi görmek tehdidi canlılaştırır, fakat sürecin içindeki farklı kurum ve kararları tek yüzün arkasında saklayabilir."),
        entry("Taç konuştuğunda: Metonimi", [
            "Metonimide bir şeyi ona yakın başka bir şeyle anarız. 'Saray açıklama yaptı' derken binayı değil yönetimi, 'masada bir Picasso var' derken ressamı değil eserini kastederiz.",
            "Metafor bir alanı başka alan üzerinden anlamaya eğilimliyken metonimi aynı deneyim alanındaki yakınlıktan yararlanır. Taç hükümdara, üniforma mesleğe, yüz kişiye erişim sağlar.",
            "Bu seçim de tarafsız değildir. Haberde 'Ankara karar verdi' demek iç tartışmaları tek irade gibi gösterir. 'Sokak öfkeli' demek hangi insanların, hangi nedenle öfkeli olduğunu belirsizleştirir.",
            "Reklamda güzel yüz bütün ürünün yerine geçebilir. Yüzü hatırlamak kolaydır; üretim koşulu, fiyat ve dayanıklılık arka planda kalır. Parça bütünü temsil eder ama bütünü kanıtlamaz.",
            "Taç konuşmaz; insanlar konuşur. Metonimi hızlı işaret verir, eleştirel okur işaretin arkasındaki kişileri geri çağırır.",
        ], "İKİNCİ KISIM · BEDEN VE NESNELER", art="metonymic-crown", caption="Metonimi taç, saray veya yüz gibi yakın bir parçayı daha geniş kişi ve kurumun yerine geçirerek hızlı erişim sağlar."),
        entry("Sıcak fincan, sıcak insan", [
            "Çocuk için bedensel sıcaklık çoğu zaman kucak, bakım ve güvenle birlikte yaşanır. Bu tekrarlar sıcaklığı sevgi ve yakınlıkla bağlayabilir. 'Sıcak bir insan', 'soğuk karşılama' ifadeleri bu eşleşmeyi taşır.",
            "Kitabın geniş tezi kavramların havada duran soyut semboller değil, bedensel ve toplumsal deneyimle biçimlendiğidir. Denge, ağırlık, yol, yakınlık ve sıcaklık soyut düşünceye malzeme verir.",
            "Bu, eline sıcak fincan verilen herkesin otomatik olarak daha cömert olacağı gibi güçlü ve değişmez bir kural değildir. Bazı bedensel hazırlama deneyleri tekrar sınamalarında tartışılmıştır. Dil örüntüsü ile anlık davranış etkisini ayırmak gerekir.",
            "Beden ortak olsa da yaşam koşulları ve kültür eşleşmeyi değiştirir. Sıcak iklimde serinlik rahatlık ve misafirperverlik işareti olabilir. Deneyim bedensel, anlam aynı zamanda tarihseldir.",
            "Fincan görüntüsü metaforun kökünü gösterir; tek deneyle bütün ağacı açıklamaz.",
        ], "İKİNCİ KISIM · BEDEN VE NESNELER", art="warmth-affection", caption="Bedensel sıcaklık ile bakımın birlikte yaşanması yakınlığı sıcaklıkla düşünmeye temel verebilir; kültür ve bağlam bu bağı biçimlendirir."),
        entry("Takvim neden kasaya benzer?", [
            "Sanayi toplumunda emek saatle ölçülür, ücret zamana bağlanır, randevu takvime bölünür. Böylece zaman yalnız akıp giden olay değil, harcanan, ayrılan, bütçelenen ve israf edilen kıt kaynağa dönüşür.",
            "Bir arkadaşınıza 'Bana iki saat ayırdı' dediğinizde zaman bir pay gibi sunulur. 'Bu yöntem haftada üç saat kazandırır' cümlesi, verim hesabını para kazancı kadar doğal gösterir.",
            "Bu metafor toplumsal kurumla güçlenir. Saat, fabrika, bordro ve takvim aynı düşünceyi her gün yeniden kurar. Dil yalnız dünyayı anlatmaz; dünya düzeni de hangi dilin kolaylaşacağını belirler.",
            "Zaman-para haritası planlama için mükemmeldir ama her anı verim ölçüsüne sokarsa dinlenme suçluluk olur. Çocukla amaçsız oyun 'çıktısız' görünürken ilişkinin asıl değeri orada oluşabilir.",
            "Takvim bir kasa olabilir, fakat hayat yalnız hesap değildir. Hangi anı yatırım, hangisini armağan saydığımız yaşam biçimini değiştirir.",
        ], "ÜÇÜNCÜ KISIM · GÜNDELİK HAYAT", art="time-money", caption="Saat, ücret ve takvim zamanı para gibi bütçelenen bir kaynağa dönüştürür; bu harita verimi gösterirken amaçsız değeri gölgeleyebilir."),
        entry("Sevgi yolculuğunda direksiyon kimde?", [
            "'Birlikte uzun yol geldik', 'ilişki ilerlemiyor', 'yollarımız ayrıldı' cümleleri sevgiyi ortak yolculuk olarak kurar. Sevenler yolcu, ilişki araç, ortak amaç varış noktası ve sorunlar engeldir.",
            "Bu harita bir tartışmada seçenek üretir. Araç bozulduysa onarabilir, rota yanlışsa değiştirebilir, hedefler ayrıysa yolları ayırabiliriz. Metafor yalnız tanım değil, çıkarım motorudur.",
            "Fakat ilişki her zaman tek araçta tek hedef değildir. İnsanların ayrı amaçları, değişen kimlikleri ve dinlenme ihtiyacı vardır. 'İlerlemeyen ilişki' mutlaka bozuk olmayabilir; sakinlik de değerli olabilir.",
            "Direksiyon sorusu güç ilişkisini görünür kılar. Kararı hep biri veriyorsa ortak yol görüntüsü adaletsizliği saklıyor olabilir. Aynı metafor eleştiri için tersine çevrilebilir.",
            "Yolculuk sevgiyi zaman içinde anlamaya yardım eder. Ama bazen bahçe, sohbet veya müzik haritası ilişkinin başka bir gerçeğini daha iyi anlatır.",
        ], "ÜÇÜNCÜ KISIM · GÜNDELİK HAYAT", art="love-journey", caption="Sevgiyi yolculuk olarak düşünmek ortak hedef, engel ve yön değişimini görünür kılar; tek araç varsayımı güç farkını saklayabilir."),
        entry("Fikirler neden yenir?", [
            "Bir düşünceyi sindirir, ham fikri pişirir, bilgiye aç olur ve sözün tadına varırız. Zihin fikri yiyecek, anlamayı yeme ve sindirme üzerinden kurar. Yeni bilgi bedene alınan besin gibi içselleşir.",
            "Öğretmen 'Konuyu lokmalara bölelim' dediğinde karmaşık dersi küçük parçalara ayırır. Benzetme iyi bir öğretim planı üretir: hazırlamak, sunmak, zaman vermek ve sindirimi kontrol etmek.",
            "Fakat öğrenci yalnız tüketici olursa bilgi başkasının pişirdiği hazır tabak gibi görünür. Oysa soru sormak, denemek ve itiraz etmek mutfakta çalışmaya benzer. Metafor rol dağılımını etkiler.",
            "'Zehirli fikir' ifadesi bazı düşüncelerin yalnız yanlış değil bulaşıcı tehlike gibi yasaklanmasını kolaylaştırabilir. Gerçek zarar olabilir; yine de hangi kanıtla zehir dediğimizi sormak gerekir.",
            "Yemek masası düşünmenin toplumsal yanını da gösterir. Bilgi tek başına yutulan hap değil, paylaşılırken değişen tarif olabilir.",
        ], "ÜÇÜNCÜ KISIM · GÜNDELİK HAYAT", art="ideas-food", caption="Fikirleri yiyecek gibi düşünmek hazırlama ve sindirmeyi görünür kılar; öğrenciyi yalnız tüketiciye indirgeme riski taşır."),
        entry("Haritalar üst üste nasıl tutunur?", [
            "Bir kavram için birden çok metafor kullanırız. Tartışma savaş olabilir, bina da olabilir: Savın temeli, desteği, yapısı ve çöküşü vardır. Bu haritalar aynı şey değildir ama belirli amaçlarda birbirine uyabilir.",
            "Tutarlılık, her görüntünün tek dev resimde eksiksiz birleşmesi demek değildir. Yolculukta yön, kapta iç-dış, savaşta rakip vardır. Bazen aynı konuşmada işbirliği yapar, bazen çelişirler.",
            "Bir şirket 'ailesiniz' deyip aynı anda çalışanı 'kaynak' diye ölçebilir. Aile sadakat, kaynak değiştirilebilirlik çağrıştırır. İki metafor arasındaki gerilim, kurumun çalışanla kurduğu ilişkinin çatlağını gösterebilir.",
            "Gündelik dil bu çelişkilerle yine de işler, çünkü her bağlamda bütün sistemi etkinleştirmeyiz. Konuşan kişi ihtiyacı olan kısmı öne çıkarır.",
            "Üst üste şeffaf haritalar gibi düşünün. Aynı araziyi farklı işaretlerle gösterirler; hiçbiri arazinin kendisi değildir.",
        ], "ÜÇÜNCÜ KISIM · GÜNDELİK HAYAT", art="overlapping-maps", caption="Bir kavramı birden çok kısmi metafor düzenleyebilir; haritalar bazı noktalarda uyuşur, bazı noktalarda gerilim yaratır."),
        entry("Yeni metafor yeni pencere açar", [
            "Yerleşik metaforlar fark edilmez; yeni metafor ise tanıdık alanı şaşırtarak başka eylem olasılığı açar. 'Sorunla savaşmak' yerine 'sorunla birlikte yaşamayı öğrenmek' denince hedef yok etmekten uyuma dönebilir.",
            "Bir mahalleyi 'çürüyen bölge' diye adlandırmak yıkım ve temizleme çağrıştırır. 'Bakımı ihmal edilmiş bahçe' demek sulama, sabır ve yerel kökleri koruma seçeneklerini öne çıkarabilir. İkisi de tarafsız değildir.",
            "Yeni metafor yalnız söz değişimiyle gerçeği değiştirmez. Bahçe denilen mahallede kira, güvenlik ve altyapı sorunları somuttur. Fakat hangi müdahaleyi düşünebildiğimizi genişletebilir.",
            "Şairin yaptığı gündelik düşünceden tamamen ayrı değildir. Şair var olan eşleştirmeleri uzatır, birleştirir veya beklenmedik kaynak alan getirir. Yaratıcılık paylaşılan beden ve kültür üzerine kurulur.",
            "Pencere duvarı yok etmez; daha önce görünmeyen manzarayı açar. İyi metafor çözümün kendisi değil, yeni sorunun başlangıcıdır.",
        ], "DÖRDÜNCÜ KISIM · GERÇEKLİK VE DEĞİŞİM", art="new-metaphor-window", caption="Yeni metafor aynı soruna başka pencere açarak farklı amaç ve eylemleri düşünülebilir hale getirebilir."),
        entry("Kısmi doğruluk neden yalan değildir?", [
            "Bir şehir haritası yolları gösterir, ağaç türlerini göstermez. Botanik harita ağaçları gösterir, otobüs saatini göstermez. Birinin eksik olması onu yalan yapmaz; hangi amaç için çizildiğine bakılır.",
            "Metaforik doğruluk da bağlama ve amaca bağlıdır. 'Enflasyon gelirimi yedi' deneyimin gerçek kaybını anlatabilir, fakat mekanizmanın bilimsel açıklaması değildir. İfade bir yönü doğru yakalarken başka soruda yetersiz kalır.",
            "Bu görüş 'her şey keyfi, hiçbir gerçek yok' demek değildir. Dünyanın direnci vardır; yanlış köprü hesabı köprüyü yıkar. Fakat dünyayı hangi kategori ve önem sırasıyla anlattığımız insan amaçlarından bağımsız değildir.",
            "İki kişi aynı olaya farklı metaforla bakabilir ve ikisi de bir parça görebilir. Tartışmanın görevi tek doğru resmi zorlamak yerine hangi haritanın hangi kanıtı açıkladığını karşılaştırmaktır.",
            "Kısmi bakış alçakgönüllülük ister: Haritanız gerekli olabilir, bütün arazi olmayabilir.",
        ], "DÖRDÜNCÜ KISIM · GERÇEKLİK VE DEĞİŞİM", art="partial-truth", caption="Metafor şehir haritası gibi amaç için seçilmiş kısmi doğruluk sunar; eksik olmak yalan olmakla aynı değildir."),
        entry("İki uç arasındaki üçüncü yol", [
            "Yazarlar bir uçta nesnelciliği görür: Dünya hazır nesne ve özelliklerden oluşur, doğru dil onları aynen kopyalar. Öteki uçta öznelcilik vardır: Anlam yalnız kişisel duygu ve hayal gücüdür.",
            "Deneyimci yaklaşım ikisini bağlamaya çalışır. Anlam bedenimiz, çevremiz, kültürümüz ve amaçlarımızla etkileşim içinde doğar. Dünya keyfimize göre değişmez, fakat ona erişimimiz bedensiz bir kamera değildir.",
            "Bir sandalye oturmak için nesnedir; fakat küçük çocuk için tırmanma aracı, marangoz için malzeme ve müzede tarih olabilir. Fiziksel yapı aynıdır, anlamlı özellik amaçla seçilir.",
            "Bu üçüncü yol bilim düşmanlığı değildir. Ölçüm de belirli soru, araç ve kategoriyle yapılır; sonra dünyanın cevabı tahmini sınar. İnsan katkısı bulunması kanıtın önemsiz olduğu anlamına gelmez.",
            "İki lens görüntüsü akılda kalabilir: Biri yalnız dış dünyayı, diğeri yalnız iç duyguyu görür. Derinlik, iki bakışın etkileşiminden doğar.",
        ], "DÖRDÜNCÜ KISIM · GERÇEKLİK VE DEĞİŞİM", art="two-lenses", caption="Deneyimci yaklaşım anlamı ne yalnız dış nesnede ne yalnız iç duyguda, beden ile dünyanın etkileşiminde kurar."),
        entry("Aynı beden, farklı kültürler", [
            "İnsanların yerçekimi, beden sınırı ve hareket deneyimi ortak yönler taşır. Bu yüzden yukarı-aşağı, içeri-dışarı ve yol gibi kaynaklar birçok dilde bulunabilir. Fakat hangi eşleşmenin öne çıkacağı kültüre göre değişir.",
            "Zaman bazı dillerde ön-arka, bazı topluluklarda doğu-batı yönleriyle daha güçlü düzenlenebilir. Aile, hastalık ve başarı metaforları tarih, din, iş düzeni ve coğrafyayla biçimlenir.",
            "Bir dildeki ifadeyi doğrudan başka dile çevirmek bu yüzden duygu kaybettirebilir. Sözlük karşılığı aynı olsa bile taşıdığı gündelik sahne farklıdır. İyi çeviri kelimeyi değil, mümkünse haritayı taşır.",
            "Ortak beden kültürü gereksiz kılmaz; kültür de bedeni silemez. Metafor ikisinin buluşma yerlerinden biridir.",
        ], "SINIRLAR VE BUGÜN"),
        entry("Kanıt nerede, yorum nerede?", [
            "Gündelik dilde düzenli metafor ailelerinin bulunması güçlü bir gözlemdir. Fakat insanların her ifadeyi kullanırken bütün haritayı bilinçte çalıştırdığı sonucu ayrıca deney ister. Dil örüntüsü zihinsel mekanizmanın tek kanıtı değildir.",
            "Araştırmalar metaforik çerçevelerin yargıyı etkileyebildiğini gösterir, ancak etkiler konuya, sözcüğe, kişiye ve deney tasarımına göre değişebilir. Küçük bir ifade insanı kukla gibi yönetmez.",
            "Yönün yalnız somuttan soyuta olduğu da tartışılır. Dil alışkanlığı zamanla hangi benzetmenin kolay geldiğini etkileyebilir; kaynak ile hedef arasında karşılıklı öğrenme bulunabilir. Teori sonraki çalışmalarla genişlemiştir.",
            "Metafor çözümlemesi bazen yorumcunun her yerde istediği kalıbı bulmasına dönüşebilir. İyi analiz çok sayıda örnek, alternatif açıklama, bağlam ve mümkünse davranış verisi arar.",
            "Kitabın fikri en iyi kesin şifre çözücü gibi değil, dikkatli soru üretme aracı gibi kullanılır.",
        ], "SINIRLAR VE BUGÜN"),
        entry("Bir toplantıda metaforu değiştirmek", [
            "Ekibiniz 'Rakibi ezmeliyiz' diyorsa önce savaş haritasının neyi iyi gösterdiğini sorun: Aciliyet, rekabet ve savunma olabilir. Sonra neyi sakladığını bulun: Müşteri ihtiyacı, işbirliği veya uzun vadeli güven.",
            "Aynı durumu ekosistem, yolculuk veya zanaat olarak yeniden anlatın. Ekosistem karşılıklı bağımlılığı, yolculuk rota ve engeli, zanaat kalite ile ustalığı öne çıkarır. Hangisi yeni ve sınanabilir eylem üretiyor?",
            "Metafor seçimi kanıtın yerini tutmamalıdır. 'Biz aileyiz' deniyorsa ücret ve iş güvenliği verisine yine bakılır. Güzel görüntü maddi gerçeği örtemez.",
            "Pratik yöntem dört adımdır: Tekrarlanan ifadeleri topla, ortak kaynak alanı bul, aydınlanan ve saklanan yönleri yaz, alternatif metaforu somut bir kararla dene.",
            "Dil değişikliği küçük görünebilir. Fakat insanlar sorun adını değiştirince çözüm rafının da değiştiğini fark edebilir.",
        ], "SINIRLAR VE BUGÜN"),
        entry("Bir dakikalık harita", [
            "Metafor yalnız şiir süsü değildir; soyut hedef alanı daha somut kaynak alanın ilişkileriyle anlamamızı sağlar. Tartışma savaş, zaman para, sevgi yolculuk olduğunda yalnız söz değil, çıkarım ve eylem yolu da değişir.",
            "Yapısal metaforlar ilişkiler ağı taşır; yönelimsel metaforlar yukarı-aşağı gibi eksenler kurar; varlık ve kap metaforları olayı nesne ve sınıra dönüştürür. Kişileştirme, metonimi ve beden deneyimi gündelik anlamın başka araçlarıdır.",
            "Her harita kısmi olduğu için bazı yönleri gösterir, bazılarını saklar. Yeni metafor yeni eylem açabilir. Fakat dil örüntüsünden bütün zihin mekanizmasını hemen çıkaramayız; kültür, bağlam, kanıt ve karşılıklı etkiyi de hesaba katmalıyız.",
        ], "SONUÇ"),
        entry("Akılda kalacak beş görüntü", [
            "Savaş ve dans: Aynı tartışmanın iki eylem düzeni. El feneri: Gösteren ve saklayan metafor. Zaman kasası: Kurumun güçlendirdiği harita. Yolculuk arabası: İlişkinin çıkarım motoru. Üst üste haritalar: Hiçbir bakış bütün arazi değildir.",
            "Bir cümle sizi çok güçlü biçimde yönlendiriyorsa sorun: Hedef alan ne, kaynak alan ne? Kaynaktan hangi ilişkiler taşındı? Hangi kişiler veya nedenler görünmez kaldı? Başka bir metafor hangi seçeneği açar?",
            "Metaforların dışında yaşayamayız. Fakat tek metaforun içinde kilitli kalmak zorunda da değiliz.",
        ], "SONUÇ"),
    ],
})


BOOKS.append({
    "bookNo": 284,
    "title": "Ezilenlerin Pedagojisi",
    "author": "Paulo Freire",
    "subtitle": "Eğitimi bilgi doldurma işi olmaktan çıkarıp dünyayı birlikte anlama ve değiştirme pratiği olarak kuran, güçlü ama dikkatle uygulanması gereken bir rehber.",
    "coverImage": "/images/summary-art-284-ezilenlerin-pedagojisi-v2.webp",
    "coverStyle": "artwork",
    "pdfUrl": "/data/pdfs/284-ezilenlerin-pedagojisi-ozeti.pdf",
    "pdfLabel": "25-50 sayfalık PDF'yi indir",
    "longForm": True,
    "chapterArtStyle": "monochrome-engraving",
    "chapterArtColor": "#7B5848",
    "meta": {
        "originalTitle": "Pedagogy of the Oppressed",
        "compiler": "Zihin Gezgini · Yapay zeka destekli çalışma",
        "date": "Temmuz 2026",
        "language": "Türkçe",
    },
    "intro": "Paulo Freire sınıfta oturan insanı boş bardak, öğretmeni de bilgi sürahisi gibi görmeye itiraz eder. Ona göre insan dünyayı yalnız seyreden değil, adını koyan ve başkalarıyla birlikte değiştirebilen bir öznedir. Ezilenlerin Pedagojisi, baskının insanı nasıl susturduğunu, ezilenin baskıcının sesini nasıl içine alabildiğini, özgürleşmenin neden yukarıdan armağan edilemeyeceğini, bankacı eğitim yerine problem kuran eğitimi, diyaloğu ve düşünceyle eylemin birleştiği praksisi anlatır. Bu rehber kitabın bütün dört bölümlük omurgasını koruyor; okuma yazma çemberinden işyeri eğitimine uzanan örnekler veriyor. Aynı zamanda öğretmen otoritesi, temel bilgi öğretimi, güvenli olmayan diyalog ortamları ve sınıf, ırk, cinsiyet gibi farklı baskıların tek ikili şemaya sığmaması üzerine eleştirileri de açık tutuyor.",
    "sources": [
        {"id": 1, "title": "Bloomsbury - Ezilenlerin Pedagojisi resmi kitap sayfası", "url": "https://www.bloomsbury.com/us/pedagogy-of-the-oppressed-9781501314148/"},
        {"id": 2, "title": "UNESCO - Eğitim ve özgürleşme bağlamında Freire", "url": "https://unesdoc.unesco.org/in/rest/annotationSVC/DownloadWatermarkedAttachment/attach_import_c723d71d-8a4e-412e-824d-8a6ba12b58b7?_=137333eng.pdf"},
        {"id": 3, "title": "UNESCO - Öğrenme ortamları ve katılım üzerine araştırma", "url": "https://uis.unesco.org/sites/default/files/documents/a-place-to-learn-lessons-from-research-on-learning-environments-2012-en.pdf"},
        {"id": 4, "title": "Cambridge - Freire'nin tarihsel ve eğitimsel bağlamı", "url": "https://www.cambridge.org/core/product/E9CBCCED72C5C6DE3805F5A4B22673F8/core-reader"},
        {"id": 5, "title": "Cambridge - Kitabın dili ve farklı eğitim anlayışı üzerine değerlendirme", "url": "https://www.cambridge.org/core/books/banned/of-course-its-a-different-education-thats-the-point/57646764350B493B60ACE9C415BB6A1C"},
    ],
    "entries": [
        entry("Bu kitap nasıl okunmalı?", [
            "Ezilenlerin Pedagojisi kolay bir yöntem kitabı değildir. Freire düşünceyi insanlaşma, baskı, bilinç, diyalog ve devrim gibi büyük kavramlarla kurar. Aynı fikri yoğun cümlelerle döndürdüğü için örneksiz okunduğunda sisli gelebilir.",
            "Bu rehber her kavramı bir sahneye bağlayacak: Toprak işçisinin okuma çemberi, söz hakkı olmayan sınıf, kötü haberi söyleyemeyen çalışan, mahallenin su sorununu araştıran grup. Ama örnek kitabın tek doğru uygulaması sayılmayacak.",
            "Freire'nin 'ezen' ve 'ezilen' ayrımı güç ilişkisini keskin görmemizi sağlar, fakat dünyadaki bütün insanları iki sabit kutuya yerleştirmez. Kişi bir alanda baskı görürken başka alanda başkasına güç uygulayabilir. Okuma boyunca bu karmaşıklık korunacak.",
        ], "BAŞLANGIÇ"),
        entry("Brezilya'da bir okuma çemberi", [
            "Freire'nin fikirleri yalnız üniversite odasında doğmadı. Brezilya'da yoksul ve yetişkin emekçilerle okuma yazma çalışmalarında, ders malzemesini insanların gündelik dünyasından çıkarmaya çalıştı. Toprak, kuyu, ücret ve oy gibi sözcükler hayatın gerçek sorularına açılıyordu.",
            "Bir işçi 'kuyu' kelimesini hecelemeyi öğrenirken yalnız harfleri birleştirmez. Kuyuyu kimin açtığını, suya kimin eriştiğini ve neden bazı evlerin susuz kaldığını konuşabilir. Sözcüğü okumak, dünyayı okumaya bağlanır.",
            "Bu yöntem hazır siyasi cevabı öğrenciye ezberletmek değildir. İyi uygulamada öğretmen soruyu kurar, insanların deneyimini dinler, bilgiyi araştırmaya açar ve kendi görüşünü de tartışılabilir kılar.",
            "Freire 1964 askeri darbesinin ardından sürgüne gitti; Şili dahil farklı ülkelerde çalıştı. Kitap Latin Amerika'daki eşitsizlik, sömürge mirası ve siyasi dönüşüm ortamında 1960'ların sonunda biçimlendi.",
            "Okuma çemberi kitabın amblemidir: Sandalyeler öne değil birbirine döner, fakat ortadaki soru gerçek dünyadan gelir.",
        ], "BİRİNCİ KISIM · BASKI VE İNSANLAŞMA", art="literacy-circle", caption="Freire'nin okuma çemberinde harf öğrenmek, gündelik yaşamın su, emek ve söz hakkı sorunlarını birlikte okumaya bağlanır."),
        entry("İnsanlaşma neden merkezde?", [
            "Freire için insanlaşmak yalnız nazik veya eğitimli olmak değildir. Kendi dünyasını anlayabilmek, konuşabilmek, karar verebilmek, yaratabilmek ve başkalarıyla ortak yaşam kurabilmektir. İnsan tamamlanmış eşya değil, olma halinde bir varlıktır.",
            "Baskı insanı nesneye indirger. Bir işçi yalnız maliyet kalemi, öğrenci yalnız not numarası, yurttaş yalnız oy deposu olduğunda kendi sözünün öznesi olmaktan uzaklaşır. Ezen de başkasını nesneleştirirken kendi insanlığını daraltır.",
            "Bu nedenle özgürleşme bir grubun ötekini ezme sırasını devralması değildir. Amaç ilişkilerin insanı nesneleştiren biçimini değiştirmektir. Eski sandalyeye yeni kişi oturursa düzen aynı kalabilir.",
            "İnsanlaşma soyut güzel söz olarak kalırsa güçsüzdür. Barınma, sağlık, güvenlik, eğitim ve söz hakkı gibi maddi koşullar insanların seçeneklerini gerçek kılar veya daraltır.",
            "Kırık insan figürü bize baskının yalnız gelir eksikliği değil, kendi hayatına anlamlı biçimde katılamama olduğunu hatırlatır.",
        ], "BİRİNCİ KISIM · BASKI VE İNSANLAŞMA", art="broken-humanity", caption="Baskı insanı karar veren özne olmaktan çıkarıp nesneye indirger; özgürleşme yalnız koltuktaki kişiyi değil ilişkiyi değiştirmeyi amaçlar."),
        entry("Açık kafesten çıkmak neden korkutabilir?", [
            "Dışarıdan bakınca özgürlük herkesin hemen isteyeceği açık kapı gibi görünür. Freire ise özgürlüğün sorumluluk, belirsizlik ve karar yükü getirdiğini söyler. Uzun süre başkasının emrine alışan kişi açık kapıda geri çekilebilir.",
            "Bir fabrikada çalışanlar yıllarca yalnız talimat almış olsun. Bir gün yönetici 'Artık siz karar verin' derse sevinçle birlikte kaygı doğar. Hangi ölçüyle karar verilecek, hata olursa kim koruyacak, konuşanın başına ne gelecek?",
            "Korku kişisel zayıflık değildir; geçmiş ceza deneyiminin akıllı izi olabilir. Güvenli alan, zaman, ortak kural ve gerçek yetki olmadan 'özgürsünüz' demek sorumluluğu aşağıya atmak olabilir.",
            "Freire özgürlüğü armağan değil, birlikte kazanılan bir uygulama olarak görür. İnsan karar verdikçe, sonucunu gördükçe ve yeniden düşündükçe özgürlük kası gelişir.",
            "Açık kafes görüntüsü şunu sorar: Kapı gerçekten açık mı, yoksa çıkana görünmez ceza mı var?",
        ], "BİRİNCİ KISIM · BASKI VE İNSANLAŞMA", art="open-cage", caption="Özgürlük sorumluluk ve risk taşıdığı için açık kapı tek başına yetmez; güven ve gerçek yetki olmadan insan geri çekilebilir."),
        entry("Baskıcının aynadaki sesi", [
            "Ezilen kişi baskıyı yalnız dışarıdan yaşamaz; baskıcının değerlerini içine alabilir. Zenginliği insan değeri, sertliği liderlik, sessizliği saygı saymaya başlayabilir. Freire buna baskıcının imgesini içselleştirme olarak bakar.",
            "Yıllarca aksanı küçümsenen çocuk büyüdüğünde kendi çocuğuna aynı aksanı yasaklayabilir. Yarayı sürdürürken kendini koruduğunu düşünür. Güçlü görünmenin yolu eski aşağılamayı tekrar etmek olur.",
            "Bu durum ezileni suçlamak için kullanılamaz. İçselleştirme, eşitsiz düzenin ne kadar derine işlediğini gösterir. Kişinin seçimi vardır ama seçenekleri korku, ödül ve tekrar biçimlendirir.",
            "Eleştirel bilinç yalnız 'bana bunu yaptılar' demekle kalmaz, 'bu ses benim içimde nasıl konuşuyor' diye sorar. Utancın kaynağını kişisel kusurdan toplumsal kurala taşır.",
            "Ayna kırılınca yüz kaybolmaz; yalnız ödünç alınmış görüntü sorgulanmaya başlar.",
        ], "BİRİNCİ KISIM · BASKI VE İNSANLAŞMA", art="oppressor-mirror", caption="Baskıcının değerleri ezilenin iç sesine dönüşebilir; eleştirel bilinç ödünç alınmış yargıyı kendi gerçeğinden ayırmaya çalışır."),
        entry("Sahte cömertliğin akan çatısı", [
            "Bir evin çatısı sürekli akıyor, ev sahibi her yağmurda kiracıya kova hediye ediyor olsun. Kova gerçek ihtiyacı azaltır, fakat çatıyı onarmadığı için bağımlılığı sürdürür. Freire buna sahte cömertlik gözüyle bakar.",
            "Yardım her zaman sahte değildir. Aç insana bugün yemek vermek gereklidir. Sorun, yardım edenin açlığı üreten ücret, toprak veya hak düzenini koruyup kendi cömertliğini alkışlamasıdır.",
            "Gerçek cömertlik insanların sürekli el açmak zorunda kalmadığı koşulları kurmaya yönelir. Bu, acil desteği kesmek değil, acil destekle yapısal değişimi birlikte düşünmektir.",
            "Yardım programında karar yalnız bağışçıdaysa alan kişinin bilgisi ve önceliği görünmez olabilir. Katılım, yardımı romantik bir ortaklığa değil, daha doğru ve onurlu tasarıma çevirebilir.",
            "Kovayı küçümsemeyin; yağmur altında gereklidir. Ama gözünüzü çatıda tutun.",
        ], "BİRİNCİ KISIM · BASKI VE İNSANLAŞMA", art="false-generosity", caption="Akan çatıda sürekli kova dağıtmak acıyı azaltır ama nedeni korur; gerçek cömertlik acil yardım ile yapısal onarımı birleştirir."),
        entry("Kimse kimseyi tek başına özgürleştiremez", [
            "Freire'nin temel cümlesi özgürleşmenin yukarıdan armağan edilemeyeceğidir. İyi niyetli uzman insanlar adına her şeyi belirlerse onları yine nesne konumunda tutabilir. İçerik değişir, ilişki değişmez.",
            "Bir mahalleye dışarıdan gelen ekip oyun alanını nereye yapacağını yalnız haritadan seçsin. Çocukların yolu, kadınların güvenlik kaygısı ve yaşlıların gölge ihtiyacı bilinmez. Halkın katılımı romantik süs değil, bilginin kaynağıdır.",
            "Bu, uzmanlığın gereksiz olduğu anlamına gelmez. Mühendis zemini, doktor salgını, öğretmen okuma yöntemini bilir. Diyalog, uzman bilgisinin yerel deneyimle karşılaşması ve kararın şeffaf biçimde paylaşılmasıdır.",
            "Ezilenlerin mücadeleye katılması, sonucunu sahiplenmesini ve yeni baskı biçimlerini fark etmesini sağlar. Fakat katılım için zaman, güvenlik ve erişim sağlanmazsa yalnız en güçlü sesler konuşabilir.",
            "Karşılıklı tutulan ip görüntüsü önemlidir: Bir kişi diğerini sürüklemez; herkes aynı ağırlık ve riskle de başlamaz.",
        ], "BİRİNCİ KISIM · BASKI VE İNSANLAŞMA", art="mutual-liberation", caption="Özgürleşme yukarıdan teslim edilen paket değil; uzmanlık ile yaşantı bilgisinin gerçek yetki içinde birlikte çalışmasıdır."),
        entry("Kumbara sınıfı", [
            "Freire geleneksel eğitimi bankacı modele benzetir. Öğretmen bilgi yatırır, öğrenci sessiz hesap gibi kabul eder. Başarı yatırılan içeriği sınav günü aynı biçimde geri çekmektir.",
            "Sınıfta öğretmen konuşur, öğrenciler dinler; öğretmen seçer, öğrenciler uyar; öğretmen bilir, öğrenciler bilmez. Bu düzen yalnız yöntem değil, dünyadaki otorite ilişkisinin provasıdır. İnsan hazır gerçekliği kabul etmeye alışır.",
            "Bilgi aktarımının her türü kötü değildir. Harf sesi, çarpım tablosu, güvenlik kuralı veya uzman tanımı bazen açık anlatım ister. Sorun öğrencinin hiçbir zaman soru kuran ve bilgiyi kullanan özneye dönüşmemesidir.",
            "Kumbara modeli öğretmeni de daraltır. Öğrencinin yanlış sorusu, yerel örneği ve farklı çözümü dersin zenginliği değil düzen bozucu görülür. Öğretmen kendi bilgisini sınama fırsatını kaybeder.",
            "Kumbara dolabilir ama düşünemez. Eğitim insanı bilgi deposundan daha fazlası olarak görmelidir.",
        ], "İKİNCİ KISIM · EĞİTİMİN İKİ YÜZÜ", art="banking-classroom", caption="Bankacı eğitim öğretmeni bilgi yatıran, öğrenciyi sessiz hesap gibi kurar; ezber büyürken soru kurma gücü daralabilir."),
        entry("Cevap vermek yerine problemi görünür kılmak", [
            "Problem kuran eğitim, öğretmenin bütün cevapları saklayıp öğrenciyi tahmine zorlaması değildir. Gerçek bir durumu birlikte incelemek, bilinenleri ve bilinmeyenleri ayırmak, bilgi edinmek ve sonucu eylemle sınamaktır.",
            "Mahallede su kesiliyorsa sınıf süreleri kaydeder, harita çıkarır, altyapı bilgisi öğrenir, belediyenin sorumluluğunu araştırır ve çözüm önerir. Matematik, dil ve yurttaşlık aynı gerçek problemde buluşabilir.",
            "Problem gerçek olduğu için öğrencinin deneyimi değerlidir; fakat kişisel deneyim tek başına yeterli kanıt değildir. Ölçüm, tarih ve uzman bilgisiyle genişler. Diyalog bilimsel titizliğin zıddı değil, ona giden ortak yol olabilir.",
            "Öğretmen soruyu seçerken bile güç kullanır. Bu yüzden neden bu problemi seçtiğini açıklamalı ve öğrencilerin başka problemler getirmesine yer açmalıdır.",
            "Tahtadaki soru işareti boşluk değil davettir: Dünyanın değişmez görünümünü araştırılabilir hale getirir.",
        ], "İKİNCİ KISIM · EĞİTİMİN İKİ YÜZÜ", art="problem-posing", caption="Problem kuran eğitim gerçek durumu soru, ölçüm, bilgi ve eylemle araştırır; öğrencinin deneyimini kanıtla buluşturur."),
        entry("Öğretmen-öğrenci, öğrenci-öğretmen", [
            "Freire öğretmen ile öğrenci arasındaki katı karşıtlığı dönüştürmek ister. Öğretmen öğrenirken öğretir, öğrenci öğretirken öğrenir. Bu, ikisinin aynı bilgiye ve sorumluluğa sahip olduğu anlamına gelmez.",
            "Bir marangoz ustası tekniği bilir; çırak yeni kullanım sorusuyla ustanın alışkanlığını sorgulatabilir. Ustanın bilgisi gerçektir, çırağın deneyimi de gerçek katkıdır. İlişki tek yönlü boru olmaktan çıkar.",
            "Öğretmen dersin güvenliğinden, kaynak seçiminden ve yanlış bilginin düzeltilmesinden sorumludur. Otorite ile otoriterlik ayrılmalıdır. Şeffaf, gerekçeli ve itiraza açık otorite öğrenmeyi koruyabilir.",
            "Öğrenciyi romantik biçimde her şeyi zaten bilen kişi saymak da saygı değildir. İnsanların öğrenme hakkı vardır; eksik bilgiye sahip olmak aşağılık olmak değildir.",
            "Daire biçimli sınıf hiyerarşiyi tek başına yok etmez. Asıl değişim, kimin sorusunun bilgi sayıldığı ve kararın nasıl gerekçelendirildiğidir.",
        ], "İKİNCİ KISIM · EĞİTİMİN İKİ YÜZÜ", art="teacher-student-circle", caption="Diyalojik sınıfta öğretmen uzmanlık ve sorumluluğunu korurken öğrencinin deneyimi ve sorusu bilgiyi dönüştüren gerçek katkı olur."),
        entry("Diyalog sohbetten daha ağırdır", [
            "Freire'de diyalog herkesin sırayla konuştuğu hoş sohbet değildir. Dünyayı anlamak ve değiştirmek için insanların ortak adlandırma çalışmasıdır. Sözcük, düşünce ile eylemi birlikte taşır.",
            "Toplantıda herkes beş dakika konuşup karar yine önceden veriliyorsa katılım dekor olur. Gerçek diyalog söylenen sözün süreci etkileyebilmesini, gerekçelerin cevap almasını ve gücün bir ölçüde paylaşılmasını ister.",
            "Diyalog anlaşma garantisi değildir. İnsanlar aynı kanıta bakıp farklı değerler nedeniyle ayrılabilir. Ama karşıdakini nesne değil, gerekçe sunabilen özne saymak çatışmanın biçimini değiştirir.",
            "Güç farkı görünmezse en rahat konuşan kişi masayı doldurur. Kolaylaştırıcı söz süresini, dili, çocuk bakımını, fiziksel erişimi ve misilleme riskini düşünmelidir.",
            "Yuvarlak masa eşitliğin resmi olabilir; gerçek eşitlik, sözün sonucuna dokunabilmesidir.",
        ], "ÜÇÜNCÜ KISIM · DİYALOG VE PRAKSİS", art="dialogue-table", caption="Diyalog sırayla konuşmak değil, sözün ortak araştırma ve karar üzerinde gerçek etkisi olduğu bir ilişki kurmaktır."),
        entry("Sevgi, alçakgönüllülük, inanç ve umut", [
            "Freire diyalog için sevgi, alçakgönüllülük, insanlara inanç, umut ve eleştirel düşünme sayar. Bu sözcükler duygusal süs değil, konuşmanın koşullarıdır. Karşıdakini değersiz görüyorsanız cevabını gerçekten beklemezsiniz.",
            "Alçakgönüllülük 'hiçbir şey bilmiyorum' demek değildir. Bildiğinin sınırını, hata ihtimalini ve karşıdakinin başka bilgi taşıdığını kabul etmektir. Uzmanın dürüst 'bilmiyorum' sözü güveni azaltmak yerine güçlendirebilir.",
            "Umut pasif iyimserlik değildir. Değişimin mümkün olduğuna inanıp bunun için örgütlü emek vermektir. Koşullar ağırsa umut, gerçekliği küçültmeden eylem alanını bulur.",
            "Sevgi de eleştirisiz yumuşaklık değildir. Bir öğrencinin düşüncesine saygı duyup yanlış hesabını açıkça göstermek mümkündür. Saygı, insanı hatasıyla yalnız bırakmak değildir.",
            "Bu malzemeler tarif gibi ölçülemez, fakat yoklukları hemen hissedilir: Kibir diyaloğu ders vermeye, umutsuzluk eylemi seyirciliğe çevirir.",
        ], "ÜÇÜNCÜ KISIM · DİYALOG VE PRAKSİS", art="dialogue-ingredients", caption="Diyalog sevgi, alçakgönüllülük, insanlara güven, umut ve eleştirel düşünmeyle taşınır; bunlar etkili ortak araştırmanın koşullarıdır."),
        entry("Dünyaya ad vermek", [
            "Bir durumun adı değişince görünüşü de değişebilir. 'Tembel öğrenci' dediğimizde sorun kişinin özü olur; 'gece çalışan ve derste uyuyan öğrenci' dediğimizde çalışma koşulu araştırılabilir hale gelir.",
            "Freire için insanlar dünyayı adlandırırken onu insan dünyasına dönüştürür. Adlandırma tek kişinin etiket yapıştırması değil, deneyim ve kanıt üzerine ortak söz üretimidir.",
            "Baskın gruplar hangi kelimelerin normal olduğunu belirleyebilir. Düşük ücret 'piyasa gerçeği', itiraz 'nankörlük' diye adlandırıldığında çıkar ilişkisi doğa yasası görünür. Eleştirel eğitim bu etiketleri açar.",
            "Fakat her yeni ad otomatik olarak doğru değildir. Bir gruba hoş gelen dil başka gerçeği saklayabilir. Ad, ölçüm ve etkilenen insanların farklı deneyimleriyle sınanmalıdır.",
            "Etiket dosyayı kapatabilir; iyi kavram dosyayı araştırmaya açar.",
        ], "ÜÇÜNCÜ KISIM · DİYALOG VE PRAKSİS", art="naming-world", caption="Dünyaya verilen ad sorunun kaynağını kişi, koşul veya kurum olarak gösterebilir; iyi adlandırma araştırmayı kapatmaz, açar."),
        entry("Praksis: Düşünce ve eylemin dönen çarkı", [
            "Praksis, düşünce ile eylemin dünyayı dönüştürmek üzere birleşmesidir. Yalnız konuşma sözelcilik, yalnız düşünmeden hareket ise kör aktivizm olabilir. Biri dünyaya dokunmaz, öteki hatasını göremez.",
            "Mahalle grubu trafik tehlikesini konuşur, araç sayar, belediyeyle görüşür, hız kesici dener ve sonucu yeniden ölçer. Eylem yeni bilgi üretir; düşünce bir sonraki eylemi düzeltir. Çark bu yüzden döner.",
            "Başarısızlık praksisin parçasıdır. İlk çözüm işe yaramazsa suçlu aramak yerine varsayım gözden geçirilir. Eleştirel eğitim kesin reçeteden çok öğrenen bir süreç kurar.",
            "Eylem riski herkes için aynı değildir. İşini kaybetme veya şiddet görme tehlikesi olan kişiye 'neden harekete geçmiyorsun' demek zalimce olabilir. Kolektif koruma ve strateji düşüncenin ahlaki parçasıdır.",
            "Praksis çarkı tek yönde dönmez: Dünya düşünceyi, düşünce eylemi, eylem yeniden dünyayı değiştirir.",
        ], "ÜÇÜNCÜ KISIM · DİYALOG VE PRAKSİS", art="praxis-wheel", caption="Praksis düşünme, eyleme geçme, sonucu görme ve yeniden düşünme döngüsüdür; ne boş söz ne kör harekettir."),
        entry("Üretken tema mahallede nasıl bulunur?", [
            "Freire eğitim içeriğinin insanların gerçek yaşamındaki güçlü çelişkilerden çıkarılmasını önerir. İş, toprak, aile, sağlık, göç veya güvenlik çevresinde tekrar eden kaygılar üretken tema olabilir.",
            "Araştırmacı mahalleye hazır başlıkla inmek yerine konuşmaları dinler, gündelik sahneleri kaydeder ve temsili görüntüler hazırlar. Sonra insanlarla birlikte bu görüntülerin ne anlattığını çözer. Süreç hem bilgi toplar hem soru üretir.",
            "Bir otobüs durağı resmi 'ulaşım' temasını açabilir; konuşma kadınların gece güvenliği, işe geç kalma cezası ve engelli erişimine uzanabilir. Tema tek kelime değil, ilişkiler düğümüdür.",
            "Dışarıdan gelen eğitimci yalnız en gürültülü sesi dinlerse yanlış tema seçer. Evde çalışanlar, çocuklar, azınlık dili konuşanlar ve toplantıya gelemeyenlerin yöntemle dahil edilmesi gerekir.",
            "Mahalle haritası ders planına dönüşürken insanlar araştırmanın nesnesi değil, anlamın ortak yazarı olur.",
        ], "ÜÇÜNCÜ KISIM · DİYALOG VE PRAKSİS", art="generative-themes", caption="Üretken tema insanların gündelik yaşamındaki çelişkilerden ortak araştırmayla çıkar; tek sözcükten çok ilişkiler düğümüdür."),
        entry("Karşı-diyalogun dört aracı", [
            "Freire baskıcı eylemi dört başlıkla inceler: Fetih, böl ve yönet, manipülasyon ve kültürel istila. Bunlar insanlarla konuşmak yerine insanlar üzerinde işlem yapmanın farklı yollarıdır.",
            "Fetih karşıdakinin dünyasını sahip olunacak alan sayar. Bölme ortak çıkarı olan grupları birbirine şüpheyle baktırır. Manipülasyon gerçek amacı saklayıp rıza görüntüsü üretir. Kültürel istila dış değerleri yerel deneyimin tek ölçüsü yapar.",
            "Bir şirket çalışanları ayrı ayrı görüşmeye çağırıp ortak ücret konuşmasını yasaklarsa bölme işler. Hazır kararı 'siz istediniz' diye sunan anket manipülasyon olabilir. Yerel dili bilgisizlik saymak kültürel istilaya yaklaşır.",
            "Bu kavramlar her anlaşmazlığı komplo diye açıklamamalıdır. Bazen grupların çıkarı gerçekten farklıdır, anket kötü tasarlanmıştır veya ortak standart gereklidir. Niyet kadar karar yetkisi ve sonuç incelenmelidir.",
            "Dört araç kutusu bir şüphe makinesi değil, gücün ilişkiyi nasıl tek yönlü kurduğunu görme merceğidir.",
        ], "DÖRDÜNCÜ KISIM · EYLEM BİÇİMLERİ", art="antidialogue-tools", caption="Fetih, bölme, manipülasyon ve kültürel istila insanı ortak özne değil üzerinde işlem yapılacak nesne olarak kurar."),
        entry("Diyalojik eylemin dört karşılığı", [
            "Freire karşı tarafa işbirliği, özgürleşme için birlik, örgütlenme ve kültürel sentez koyar. İşbirliği ortak probleme birlikte bakar; birlik parçalanmış insanların ortak gücünü görmesini sağlar; örgütlenme bu gücü süreklileştirir.",
            "Kültürel sentezde dışarıdan gelen kişi kendi bilgisini saklamaz, fakat yerel dünyayı boş arazi saymaz. Yeni anlayış iki tarafın karşılaşmasında doğar. Ne yerel olan otomatik olarak kutsal, ne uzman olan otomatik olarak üstündür.",
            "Bir sağlık ekibi aşı bilgisini getirirken mahalledeki güvensizlik tarihini dinleyebilir. İnsanların sorularını propaganda saymak yerine kanıt, yan etki ve erişim sorununu açıkça konuşur. Bu, bilimden vazgeçmek değil uygulama bilgisini güçlendirmektir.",
            "Örgütlenme ile manipülasyon arasındaki fark amaç kadar yöntemdir. İnsanlar kararın gerçek sahibi mi, yoksa hazır hedef için sayı mı? Liderlik gereklidir ama tabanın eleştirisine kapalıysa yeni hiyerarşi doğar.",
            "Dört karşılık, diyaloğun yalnız iyi niyet değil kurum, zaman ve ortak sorumluluk istediğini gösterir.",
        ], "DÖRDÜNCÜ KISIM · EYLEM BİÇİMLERİ", art="dialogical-tools", caption="İşbirliği, birlik, örgütlenme ve kültürel sentez diyaloğu kalıcı ortak eyleme dönüştürür; liderliği hesap verebilir kılar."),
        entry("Ezen kim, kararı kim veriyor?", [
            "Freire'nin güçlü dili haksızlığı görünür yapar, fakat her anlaşmazlıkta karşı tarafı 'ezen' ilan etmek diyaloğu başlamadan bitirebilir. Güç yalnız kötü niyet değil, kaynak, kural koyma ve sonuçtan kaçınma kapasitesidir.",
            "Bir öğretmen not verir ve sınıf düzenini korur; bu güç gerçektir ama otomatik olarak baskı değildir. Ölçüt, yetkinin amacı, sınırı, gerekçesi, itiraz yolu ve insanı susturup susturmadığıdır.",
            "Öğrenci de akranına zorbalık yapabilir; çalışan müşteri üzerinde, ebeveyn çocuk üzerinde güç taşıyabilir. İnsan sabit kimlik değil, kesişen ilişkiler içinde farklı konumlar yaşayabilir.",
            "'Kim karar veriyor, kim bedel ödüyor, kim konuşamıyor, kim kuralı değiştirebiliyor?' soruları etiketten daha somut bir güç haritası çıkarır.",
            "Eleştirel eğitim kendi kavramını da eleştiriye açmalıdır. Aksi halde özgürleştirici dil yeni bir ezber bankasına dönüşür.",
        ], "SINIRLAR VE BUGÜN"),
        entry("Tek ikili tabloya sığmayan hayat", [
            "Kitabın ana ekseni sınıfsal ve sömürgeci baskıdır. Daha sonraki feminist, ırk karşıtı ve sömürge sonrası düşünürler cinsiyet, ırk, engellilik, cinsellik ve dilin bu tabloyu nasıl karmaşıklaştırdığını genişletti.",
            "Aynı yoksul topluluk içinde kadınların sözü bastırılabilir; sömürgeye karşı çıkan erkek evde baskıcı olabilir. Ortak mücadele iç farklılığı susturursa özgürlük birileri için ertelenir.",
            "Deneyim konuşmak için önemli kaynaktır, fakat bir grubun tek temsilcisi yoktur. En görünür kişinin sözü bütün grubun gerçeği sayılmamalıdır. Yöntem farklı sesleri güvenli biçimde toplamalıdır.",
            "Bu ekler Freire'yi reddetmekten çok temel sorusunu çoğaltır: Kim özne sayılıyor ve kimin dünyayı adlandırma hakkı elinden alınıyor?",
        ], "SINIRLAR VE BUGÜN"),
        entry("Diyalog her yerde güvenli ve yeterli değildir", [
            "Şiddet tehdidi olan odada açık konuşma istemek insanı tehlikeye atabilir. Patronun bulunduğu toplantıda çalışanların sessizliği bilinç eksikliği değil işini koruma stratejisi olabilir. Önce anonim kanal, hukuki koruma ve güvenli alan gerekebilir.",
            "Acil durumda uzun diyalog mümkün olmayabilir. Yangında öğretmen çıkış yönünü tartışmaya açmaz. Temel okuma becerisinde açık anlatım ve tekrar değerlidir. Mesele otoriteyi yok etmek değil, nerede neden kullanıldığını sınırlamaktır.",
            "Öğrencinin merakı yanlış bilgiyle karşılaşabilir. Öğretmen kanıt standardını, kaynak kontrolünü ve bilimsel bilgiyi sunmalıdır. 'Herkesin doğrusu kendine' tavrı güçlü olanın yanlışını koruyabilir.",
            "Freire'nin yöntemi en iyi, bilgi aktarımı, yapılandırılmış alıştırma ve diyalojik problem çözmeyi ihtiyaca göre birleştiren eğitimde yaşar. Tek teknik bütün derslerin anahtarı değildir.",
            "Güvenlik, gerçek ve söz hakkı birbirinin düşmanı olmak zorunda değildir; iyi tasarım üçünü aynı masaya getirir.",
        ], "SINIRLAR VE BUGÜN"),
        entry("Bir dakikalık harita", [
            "Baskı insanı dünyasını adlandıran özne olmaktan çıkarıp nesneleştirir. Ezilen kişi baskıcının değerlerini içselleştirebilir ve özgürlüğün belirsizliğinden korkabilir. Özgürleşme yukarıdan armağan değil, etkilenen insanların ortak praksisidir.",
            "Bankacı eğitim bilgiyi sessiz öğrenciye yatırır; problem kuran eğitim gerçek durumu deneyim, bilgi, soru ve eylemle araştırır. Diyalog sohbet değil, sözün ortak kararı etkilediği ilişkidir. Praksis düşünce, eylem, sonuç ve yeniden düşünme döngüsüdür.",
            "Fetih, bölme, manipülasyon ve kültürel istilaya karşı işbirliği, birlik, örgütlenme ve kültürel sentez önerilir. Fakat öğretmen sorumluluğu, temel bilgi, güvenlik ve kesişen baskılar ihmal edilmemelidir. Özgürleştirici dil de hesap verebilir olmalıdır.",
        ], "SONUÇ"),
        entry("Akılda kalacak beş görüntü", [
            "Okuma çemberi: Sözcükle dünyayı birlikte okumak. Açık kafes: Özgürlüğün risk ve güven ihtiyacı. Akan çatı: Yardımla nedeni ayırmak. Kumbara sınıfı: Bilgi yatırımı ile özne kaybı. Praksis çarkı: Düşünce ve eylemin birbirini düzeltmesi.",
            "Bir eğitim veya katılım projesinde sorun: Problemi kim seçti? Kimin deneyimi bilgi sayıldı? Söz kararı gerçekten etkiliyor mu? Uzmanlık nasıl açıklanıyor ve sınanıyor? Konuşmanın bedelini en çok kim ödüyor?",
            "Freire'nin kalıcı çağrısı, insanlara konuşma izni vermek değil, zaten taşıdıkları insanlık ve düşünme hakkını kurumların gerçek gücüne dönüştürmektir.",
        ], "SONUÇ"),
    ],
})


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for source in BOOKS:
        summary = assemble(source)
        target = OUT / f"{summary['bookNo']}.json"
        target.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        words = sum(len(paragraph.split()) for chapter in summary["chapters"] for paragraph in chapter["paragraphs"])
        print(f"{target.relative_to(ROOT)}: {len(summary['chapters'])} chapters, {len(summary['chapterArtworks'])} artworks, {words} words")


if __name__ == "__main__":
    main()
