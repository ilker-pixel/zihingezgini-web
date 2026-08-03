#!/usr/bin/env python3
"""Build summaries eleven through fifteen in the twenty-book collection."""

from summary_batch_common import entry, write_books

DATE = "Temmuz 2026"
BOOKS = []


def base(no, title, author, subtitle, color, original, slug, sources, entries):
    return {
        "bookNo": no, "title": title, "author": author, "subtitle": subtitle,
        "coverImage": f"/images/summary-art-{no}-{slug}-v1.webp", "coverStyle": "artwork",
        "pdfUrl": f"/data/pdfs/{no}-{slug}-ozeti.pdf", "pdfLabel": "25-50 sayfalık PDF'yi indir",
        "longForm": True, "chapterArtStyle": "monochrome-engraving", "chapterArtColor": color,
        "meta": {"originalTitle": original, "compiler": "Zihin Gezgini · Yapay zeka destekli çalışma", "date": DATE, "language": "Türkçe"},
        "intro": subtitle, "sources": sources, "entries": entries,
    }


BOOKS.append(base(151, "Ulusların Zenginliği", "Adam Smith",
    "Bir toplumu zengin yapanın kasadaki altın değil insanların üretken emeği olduğunu; iğne atölyesinden pazara, ücretten kâra, vergiden devlete uzanan geniş bir soruşturmayla anlatan iktisat klasiğinin sade rehberi.",
    "#596A4B", "An Inquiry into the Nature and Causes of the Wealth of Nations", "uluslarin-zenginligi",
    [
        {"id": 1, "title": "Project Gutenberg - The Wealth of Nations tam metni", "url": "https://www.gutenberg.org/files/3300/3300-h/3300-h.htm"},
        {"id": 2, "title": "Adam Smith Works - Glasgow Üniversitesi", "url": "https://www.gla.ac.uk/explore/adamsmith300/"},
        {"id": 3, "title": "Encyclopaedia Britannica - Adam Smith", "url": "https://www.britannica.com/biography/Adam-Smith"},
        {"id": 4, "title": "Library of Economics and Liberty - Wealth of Nations", "url": "https://www.econlib.org/library/Smith/smWN.html"},
    ], [
        entry("Bu kitap nasıl okunmalı?", [
            "Ulusların Zenginliği serbest piyasa için yazılmış kısa manifesto değildir. Beş büyük kitapta üretim, sermaye, ekonomik tarih, siyasal iktisat sistemleri, vergi ve kamu görevleri incelenir.",
            "Smith insanın yalnız bencil olduğunu söylemez. Daha önceki Ahlaki Duygular Kuramı'nda sempatiyi tartışır; bu kitapta değiş tokuş ve kurumların büyük ölçekte nasıl çalıştığına odaklanır.",
            "Rehber görünmez eli yerine oturtacak, işçilerin durumu ve tüccar gücü hakkındaki sert uyarıları da koruyacak.",
        ], "BAŞLANGIÇ"),
        entry("İğne fabrikasındaki şaşırtıcı artış", [
            "Tek işçi teli çekip keser, sivriltir, baş yapar ve paketlerse günde az sayıda iğne üretebilir. İşler bölündüğünde on kişi binlerce iğne çıkarır.",
            "Bir mutfakta herkes aynı anda her yemeği yapmaya çalışmak yerine biri doğrar, biri pişirir, biri servis ederse bekleme ve araç değiştirme azalır.",
            "İş bölümü el becerisini artırır, görev geçişini azaltır ve özel makine icadını teşvik eder. Zenginliğin ilk büyük motoru budur.",
            "Fakat aynı işi durmadan yapmak zihni köreltebilir. Smith devletin temel eğitimi desteklemesini tam da bu insani maliyet yüzünden ister.",
        ], "BİRİNCİ KISIM · EMEĞİN GÜCÜ", art="pin-factory", caption="İğne üretiminin küçük adımlara bölünmesi aynı emeği olağanüstü çoğaltırken işin insani maliyetini de büyütebilir."),
        entry("İş bölümünü pazar büyütür", [
            "Küçük köyde yalnız düğme yapan kişi geçinemez; müşterisi azdır. Büyük şehir ve uzak ticaret, dar uzmanlığın ürününü alacak kadar geniş pazar yaratır.",
            "Bir fırın yalnız mahalleye satıyorsa üç çeşit ekmek yapar; ülkeye dağıtım kurunca tek üründe uzman ekip yaşayabilir.",
            "Uzmanlaşma pazarı, pazar uzmanlaşmayı büyütür. Yol, liman ve güvenilir para bu karşılıklı döngünün altyapısıdır.",
            "Bu nedenle üretkenlik yalnız atölyedeki disiplin değil, toplumun bağlantı genişliğidir.",
        ], "BİRİNCİ KISIM · EMEĞİN GÜCÜ", art="market-radius", caption="Pazar genişledikçe dar uzmanlık yaşayabilir; uzmanlaşma da pazara daha çok ve ucuz ürün sunar."),
        entry("Değiş tokuş eden insan", [
            "Smith akşam yemeğini kasap, bira üreticisi ve fırıncının iyilikseverliğinden değil kendi çıkarlarını gözetirken yaptıkları değiş tokuştan beklediğimizi söyler.",
            "Bu cümle insanların sevgisiz olduğu anlamına gelmez. Yabancılar arasında her gün süren büyük işbirliğinin kişisel dostluk gerektirmeden kurulabildiğini açıklar.",
            "Markette satıcıya açlığınızı değil karşılıklı kazancı anlatırsınız. Fiyat ortak dil olur, hukuk ve güven bu dili taşır.",
            "Aile, arkadaşlık ve bakım yalnız alışveriş mantığıyla açıklanamaz. Smith'in sahnesi piyasa ilişkisinin belirli alanıdır.",
        ], "BİRİNCİ KISIM · EMEĞİN GÜCÜ", art="baker-buyer", caption="Yabancılar kişisel sevgi olmadan karşılıklı çıkar ve güvenilir kurallar sayesinde her gün işbirliği yapabilir."),
        entry("Gerçek fiyat emektir", [
            "Para fiyatı değişebilir; Smith malın kişiye ne kadar emek harcattığı veya başkasının emeğinden ne kadar satın alabildiğiyle daha temel bir ölçü arar.",
            "Bir ayakkabı bugün on, yarın yüz para birimi olabilir. Onu kazanmak için gereken çalışma süresi alım gücünü daha somut anlatır.",
            "İlkel toplumda emek daha doğrudan ölçü gibi görünür; sermaye ve toprak mülkiyeti geliştikçe fiyat ücret, kâr ve rant arasında bölünür.",
            "Smith tek ve tamamlanmış emek değer teorisi bırakmaz. Metindeki farklı açıklamalar sonraki iktisat tartışmalarını besler.",
        ], "BİRİNCİ KISIM · EMEĞİN GÜCÜ", art="labor-clock", caption="Paranın rakamı değişse de bir malı elde etmek için gereken yaşam zamanı gerçek bedeli görünür kılabilir."),
        entry("Doğal fiyat ile pazar fiyatı", [
            "Bir malın doğal fiyatı ücret, kâr ve rantın olağan düzeylerini karşılar. Pazar fiyatı ise o günkü arz ve talebe göre yukarı veya aşağı oynar.",
            "Konser gecesi otel odası pahalanır, boş sezonda ucuzlar. Bina aynı, talep değişmiştir.",
            "Yüksek fiyat yeni satıcıyı çeker, üretim artar ve fiyat gerileyebilir. Düşük fiyat üretimi azaltır. Rekabet bir geri besleme kurar.",
            "Bu süreç sürtünmesiz değildir. Tekel, bilgi farkı ve pazara giriş engeli fiyatı uzun süre olağan düzeyden uzak tutabilir.",
        ], "İKİNCİ KISIM · ÜCRET, KÂR, RANT", art="market-scales", caption="Günlük pazar fiyatı arz ve taleple salınırken rekabet onu üretim gelirlerinin olağan dengesine doğru çekebilir."),
        entry("Ücret pazarlığında eşit olmayan taraflar", [
            "İşçi ile işveren sözleşme masasına kağıt üzerinde özgür gelir, fakat işveren daha uzun süre bekleyebilir ve daha kolay örgütlenebilir. Smith bu güç eşitsizliğini açıkça belirtir.",
            "Birinin yarın kirayı ödemesi gerekirken diğerinin aylarca birikimi varsa 'ikisi de hayır diyebilir' cümlesi gerçek pazarlığı anlatmaz.",
            "Büyüyen toplumda emek talebi artınca ücretler yükselebilir. Smith çalışan çoğunluğun durumunu ülkenin refah ölçüsü sayar.",
            "Piyasa sözleşmesi güçten bağımsız değildir. Özgürlük için seçeneklerin gerçekten kullanılabilir olması gerekir.",
        ], "İKİNCİ KISIM · ÜCRET, KÂR, RANT", art="unequal-table", caption="Sözleşme masasında iki imza eşit görünse de bekleme gücü farklıysa gerçek pazarlık dengesi eşit değildir."),
        entry("Kâr neden ücretle aynı değildir?", [
            "Sermaye sahibi malzeme ve ücret için önceden kaynak ayırır, satış riskini taşır ve bunun karşılığında kâr bekler. Kâr yalnız yönetici emeğinin ücreti değildir.",
            "Fırıncı un ve kira parasını ekmek satılmadan öder. Ekmek bozulur veya müşteri gelmezse kaybı taşır.",
            "Fakat rekabet zayıfsa kâr risk karşılığını aşabilir. Tüccarlar bir araya geldiğinde konuşmanın halka karşı fiyat artırma planına dönebileceğini Smith iğneleyerek söyler.",
            "Sermaye üretimi büyütür, aynı zamanda yoğunlaştığında siyasi güç kazanır. Kitap bu iki yüzü birlikte görür.",
        ], "İKİNCİ KISIM · ÜCRET, KÂR, RANT", art="capital-risk", caption="Sermaye satıştan önce masraf ve risk taşır; rekabet yoksa bu karşılık kolayca ayrıcalıklı kazanca dönüşebilir."),
        entry("Rant: Yerin payı", [
            "Toprak sahibi üretime doğrudan emek katmadan, kıt ve verimli yere erişim karşılığında rant alabilir. Ürünün fiyatı ücret ve kâr yanında bu payı da taşır.",
            "Aynı kahve iki sokakta farklı kira yüzünden başka fiyatla satılır. Müşteri akışını sağlayan konum sahibine gelir yaratır.",
            "Smith sınıfların çıkarlarının her zaman toplumla aynı olmadığını inceler. Toprak sahibi, işçi ve sermayedar fiyat değişiminden farklı etkilenir.",
            "Ulusun tek çıkarı varmış gibi konuşmak, gelirin kimde biriktiğini gizler.",
        ], "İKİNCİ KISIM · ÜCRET, KÂR, RANT", art="land-rent", caption="Konum ve kıt toprağa sahiplik, üretime doğrudan emek eklemeden fiyatın içinden rant payı çekebilir."),
        entry("Görünmez el gerçekten nerede?", [
            "Ünlü ifade kitapta sınırlı bağlamda geçer. Sermayesini yerli kullanıma yönelten tüccar kendi güvenini ararken toplam üretime istemeden katkı sağlayabilir.",
            "Kalabalık pazarda tek merkez kimsenin bütün kararını vermez; fiyatlar dağınık bilgiyi kısmen koordine eder. Ortaya çıkan düzen planlanmamış olabilir.",
            "Bu, her özel çıkarın kamu yararı yarattığı sihirli yasa değildir. Smith tekel, ayrıcalık, hile ve sömürge ticaretini sertçe eleştirir.",
            "Görünmez elin çalışması için görünür hukuk, rekabet ve güven gerekir. Kuralsız güç kendiliğinden uyum üretmez.",
        ], "ÜÇÜNCÜ KISIM · TİCARET VE DEVLET", art="invisible-coordination", caption="Dağınık pazar kararları plansız düzen kurabilir, fakat görünmez koordinasyon görünür hukuk ve rekabete dayanır."),
        entry("Merkantilist altın sandığı", [
            "Dönemin devletleri zenginliği ülkede biriken altın ve ticaret fazlasıyla ölçüyordu. Smith gerçek zenginliğin halkın tüketebildiği yıllık mal ve hizmet akışı olduğunu savunur.",
            "Evin kasasında altın varken mutfak, eğitim ve üretim çöküyorsa aile zengin sayılmaz. Para araçtır, ihtiyaçları karşılayan üretim amaçtır.",
            "İthalatı engelleyip ihracatı destekleyen ayrıcalıklar tüketiciye pahalı ürün yükleyebilir. Koruma çoğu zaman örgütlü üreticinin kazancını dağınık halka ödetir.",
            "Ulusal gurur ekonomik hesabı gölgeleyebilir; Smith faturayı kimin ödediğini sorar.",
        ], "ÜÇÜNCÜ KISIM · TİCARET VE DEVLET", art="gold-and-bread", caption="Altın dolu sandık ekmek, barınma ve üretim sağlamıyorsa ulusun gerçek yaşam zenginliğini ölçmez."),
        entry("Mutlak üstünlük ve ticaret", [
            "Bir ülke şarabı, diğeri kumaşı daha az kaynakla üretiyorsa uzmanlaşma ve değiş tokuş ikisine de yarar sağlayabilir. Evde ayakkabı yapmak yerine usta ayakkabıcıdan almak gibi.",
            "Smith'in açıklaması daha sonra karşılaştırmalı üstünlük teorisiyle geliştirildi. Onun metninde temel vurgu emeği en üretken alana yöneltmektir.",
            "Ticaretin toplam kazancı bütün kişilere eşit dağılmaz. İthalatla rekabet eden işçi işini kaybedebilir; geçiş maliyeti soyut toplamda kaybolmamalıdır.",
            "Açık ticaret yarar üretebilir, fakat adil uyum ve siyasi güç sorusunu tek başına çözmez.",
        ], "ÜÇÜNCÜ KISIM · TİCARET VE DEVLET", art="wine-and-cloth", caption="Uzmanlaşma toplam üretimi büyütebilir; kazancın toplum içindeki dağılımı ise ayrı bir adalet sorusudur."),
        entry("Sömürge tekellerinin faturası", [
            "Smith sömürgeler üzerindeki ticaret tekellerini, savaş masrafını ve tüccar ayrıcalığını eleştirir. İmparatorluk kazancı bütün halka değil belirli çıkar gruplarına akabilir.",
            "Bir şirket kârı alırken donanma ve savaş vergisini toplum ödüyorsa özel bilanço iyi, kamusal bilanço kötü olabilir.",
            "Sömürge halklarının yaşadığı şiddet Smith'in ekonomik hesabından daha geniştir. Yine de imparatorluğu ulusal zenginlik diye kutsamaması döneminde önemlidir.",
            "Bugün de şirket kazancı ile çevre, güvenlik ve kamu maliyetini aynı deftere yazmak gerekir.",
        ], "ÜÇÜNCÜ KISIM · TİCARET VE DEVLET", art="colonial-ledger", caption="Sömürge şirketi kârı toplarken savaş ve yönetim masrafını halka bırakabilir; iki bilanço birlikte okunmalıdır."),
        entry("Devletin üç büyük görevi", [
            "Smith savunma, adalet ve özel kişilerin kârlı bulmayacağı kamusal işler için devlete görev verir. Yol, köprü ve eğitim pazarın altyapısını kurar.",
            "Sokak lambası yalnız onu satın alanın önünü aydınlatamaz; fayda çevreye yayılır. Özel gelir toplam yararı karşılamadığı için ortak finansman gerekebilir.",
            "Devletin harcaması sınırsız değildir. Hesap verme, yararlananın katkısı ve etkinlik önemlidir.",
            "Smith'in devleti gece bekçisi kadar küçük değildir. Piyasanın işlemesi için aktif kurumlar gerekir.",
        ], "DÖRDÜNCÜ KISIM · KAMU VE VERGİ", art="public-bridge", caption="Köprü ve eğitim gibi ortak altyapılar özel kârı aşan fayda ürettiği için kamusal görev alanına girer."),
        entry("İş bölümü zihni körelttiğinde", [
            "Aynı birkaç işlemi ömür boyu yapan emekçi düşünme ve yurttaşlık kapasitesini kullanamaz hale gelebilir. Smith bunu gelişmiş toplumun ciddi tehlikesi sayar.",
            "Günde bin kez tek vida sıkan kişi ürünü bütünüyle görmez. Eli ustalaşırken merakı daralabilir.",
            "Temel eğitim yalnız işverene beceri sağlamak için değil insanın yargı ve ortak yaşam yetisini korumak için gereklidir.",
            "Üretkenlik hesabına insanın gelişimini eklemezsek ucuz ürünün görünmeyen fiyatını kaçırırız.",
        ], "DÖRDÜNCÜ KISIM · KAMU VE VERGİ", art="single-screw", caption="Tek harekette ustalaşan işçi ürünün bütününden ve kendi zihinsel gelişiminden uzaklaşabilir."),
        entry("Adil verginin dört ölçüsü", [
            "Vergi ödeme gücüne uygun, miktarı belirsiz olmayan, uygun zamanda alınan ve tahsil maliyeti düşük olmalıdır. Keyfi vergi ekonomik olduğu kadar siyasi güvensizlik yaratır.",
            "Kasada fiyatı belli olmayan ürün gibi, ne zaman ne kadar vergi çıkacağını bilmeyen kişi plan yapamaz ve memurun keyfine bağımlı kalır.",
            "Tahsil için yüz lira harcayıp kasaya elli lira koymak toplum kaybıdır. Uyum maliyeti de verginin parçasıdır.",
            "Bu ölçüler modern vergi tasarımının sade ama kalıcı kontrol listesidir.",
        ], "DÖRDÜNCÜ KISIM · KAMU VE VERGİ", art="tax-principles", caption="Adil vergi ödeme gücü, kesinlik, uygun zaman ve düşük tahsil maliyetini aynı terazide tutar."),
        entry("Kamu borcu ve gelecek kuşak", [
            "Savaş giderini borçla karşılamak bugünkü vergi acısını erteler. Hükümet harcama desteğini kolay toplar, fatura faizle geleceğe taşınır.",
            "Ailenin düğün masrafını kredi kartına atıp yalnız asgari ödeme yapması gibi, siyasi rahatlık uzun yük oluşturabilir.",
            "Borç her zaman kötü değildir; üretken altyapı gelecek kuşağa hem varlık hem yük bırakabilir. Smith özellikle sürekli savaş borçlarına kuşkuyla bakar.",
            "Doğru soru borcun varlığı değil ne için, hangi maliyetle ve kimin yararına alındığıdır.",
        ], "DÖRDÜNCÜ KISIM · KAMU VE VERGİ", art="debt-calendar", caption="Kamu borcu bugünkü harcamanın faturasını takvimde ileri taşır; gelecek kuşak yükle birlikte ne kazandığını sormalıdır."),
        entry("Smith neyi öngöremedi?", [
            "Sanayi devriminin dev şirketlerini, fosil yakıt krizini, merkez bankalarının bugünkü rolünü ve dijital tekelleri Smith tam biçimiyle göremezdi.",
            "Piyasa fiyatı çevre kirliliği gibi dış maliyeti taşımayabilir. Fabrikanın ucuz ürünü nehir temizliğini halka bırakıyorsa görünen fiyat eksiktir.",
            "Kitabı bugüne uygulamak ilkeleri yeni kurumlarla geliştirmeyi gerektirir; 1776 düzenini kopyalamayı değil.",
        ], "SON DURAKLAR"),
        entry("Ne sağın ne solun tek cümlesi", [
            "Smith rekabet ve ticaretin gücünü savunur; aynı zamanda işveren birliklerini, tekelleri, sömürge ayrıcalığını ve iş bölümünün insani zararını eleştirir.",
            "Onu yalnız görünmez el veya yalnız emekçi dostu yaparsak metnin dengesini kaybederiz. Piyasa üretken bir düzen ve güç ilişkileri alanıdır.",
            "Kalıcı yöntem, slogan seçmek değil her kurumda üretkenlik, özgürlük ve dağılımı birlikte sormaktır.",
        ], "SON DURAKLAR"),
        entry("Bir ürünü Smith gibi okumak", [
            "Elinizdeki telefonu alın. İş bölümü kaç ülkeye yayılmış, ücret ve kâr kimlere gidiyor, altyapıyı kim finanse ediyor, çevre bedeli fiyatta mı?",
            "Sonra rekabeti sorun: Yeni üretici girebilir mi, bilgi alıcıda mı, yoksa tekel fiyatı mı var?",
            "Bir ürün etiketi böylece bütün ulusun kurum ve emek haritasına dönüşür.",
        ], "SON DURAKLAR"),
        entry("Bir cümlede kitabın özü", [
            "Ulusun zenginliği altın yığını değil, iş bölümü ve değiş tokuşla büyüyen üretken emektir; fakat bu güç rekabet, adalet, eğitim ve kamusal altyapı olmadan ayrıcalığa dönüşebilir.",
            "Akılda kalacak görüntü iğne atölyesidir: Üretim çoğalır, ama tezgahın başındaki insanı ve dışarıdaki kuralları unutursak hesabın yarısı kaybolur.",
        ], "SON DURAKLAR"),
    ]))


BOOKS.append(base(157, "Borç: İlk 5000 Yıl", "David Graeber",
    "Paranın takastan doğduğu basit masalı tersine çevirip borcu ahlak, şiddet, devlet, pazar ve insan ilişkilerinin merkezine koyan; tabletlerden kredi kartına uzanan beş bin yıllık kışkırtıcı tarih.",
    "#7B553E", "Debt: The First 5,000 Years", "borc-ilk-5000-yil",
    [
        {"id": 1, "title": "David Graeber resmi sitesi - Debt", "url": "https://davidgraeber.org/books/debt-the-first-5000-years/"},
        {"id": 2, "title": "David Graeber - Debt makalesi", "url": "https://davidgraeber.org/articles/debt-the-first-five-thousand-years/"},
        {"id": 3, "title": "IMF - Paranın tarihi ve kredi tartışması", "url": "https://www.imf.org/external/pubs/ft/fandd/2012/09/basics.htm"},
        {"id": 4, "title": "Bank of England - Money in the modern economy", "url": "https://www.bankofengland.co.uk/quarterly-bulletin/2014/q1/money-in-the-modern-economy-an-introduction"},
    ], [
        entry("Bu kitap nasıl okunmalı?", [
            "Graeber geniş tarih ve antropolojiyi tek büyük savda birleştirir: Ekonomik borç, ahlaki yükümlülük ve siyasi güç birbirinden ayrı değildir. Kitap kesin kronoloji kadar alışılmış hikayeleri sarsmayı amaçlar.",
            "Bazı tarihçiler ayrıntılarını ve dönem genellemelerini eleştirmiştir. Rehber ana örüntüyü aktarırken kışkırtıcı iddiayı kanıtlanmış tek yasa gibi sunmayacak.",
            "Borç alanı suçlamak veya borcu ödememeyi öğütlemek amaç değildir. Hangi borcun meşru, hangi ilişkinin zorla sayıya çevrilmiş olduğunu sormaktır.",
        ], "BAŞLANGIÇ"),
        entry("Takastan para doğdu masalı", [
            "Klasik hikayede köylü ayakkabısını verip buğday almak ister, fakat karşı taraf ayakkabı istemez. Takas zorluğu parayı, para da krediyi doğurur.",
            "Graeber antropologların saf takasla yaşayan toplum örneği bulmadığını vurgular. Köy içinde insanlar 'bugün benden, sonra senden' diye açık hesap yaşar.",
            "Komşunuzdan iki yumurta alırken her seferinde anında eşdeğer vermezsiniz. İlişki ve hafıza kredi işlevi görür.",
            "Takas daha çok yabancılar veya para düzeni çöktüğünde görülebilir. Paranın tek köken masalı böylece ters döner.",
        ], "BİRİNCİ KISIM · BORCUN AHLAKI", art="barter-myth", caption="Yakın toplulukta değişim anlık takastan çok hafıza ve gelecekte karşılık beklentisi taşıyan açık hesap olabilir."),
        entry("Borç ile söz arasındaki fark", [
            "Her yükümlülük borç değildir. Arkadaşınıza hayatını kurtardığı için borçlu hissedebilirsiniz, fakat bunu kaç lirayla kapatacağınız anlamsızdır.",
            "Borç, yükümlülüğün sayı ve vade ile ölçülebilir hale gelmesidir. Tam da bu kesinlik ilişkiyi devredilebilir ve zorla tahsil edilebilir yapar.",
            "Bir iyiliğe teşekkür bağı kurarken, senet alacaklı ile borçluyu eşitsiz konuma koyabilir. Sayı tarafsız görünür ama arkasında hukuk ve güç vardır.",
            "Graeber ahlak dilindeki borç, suç, günah ve kefaret bağlarını bu dönüşüm üzerinden okur.",
        ], "BİRİNCİ KISIM · BORCUN AHLAKI", art="promise-ledger", caption="Açık uçlu insan yükümlülüğü sayı ve vadeye çevrilince devredilebilen, tahsil edilebilen borca dönüşür."),
        entry("Borç mutlaka ödenmeli mi?", [
            "'İnsan borcunu ödemeli' güçlü ahlaki cümledir. Fakat bütün borçlar ödense kredi sistemi biter; ayrıca yağmacıya verilen zorunlu söz ile eşit sözleşme aynı değildir.",
            "Tefeci aç aileye imkansız faizle para vermişse kağıt imzalıdır, fakat ilişkinin adaleti yalnız imzada bitmez.",
            "Graeber kimin kime ne borçlu olduğunun tarih boyunca iktidarla belirlendiğini gösterir. Devlet borcu siler, köylünün borcunu tahsil edebilir.",
            "Soru ödeme ahlakını yok etmek değil, borcun hangi koşulda doğduğunu hesaba katmaktır.",
        ], "BİRİNCİ KISIM · BORCUN AHLAKI", art="unequal-contract", caption="İmzalı sözleşme borcu ölçer, fakat açlık ve güç eşitsizliği altında doğan ilişkinin adaletini tek başına kanıtlamaz."),
        entry("İnsan ekonomileri", [
            "Graeber bazı toplumlarda değişimin nesne biriktirmekten çok insan ilişkileri kurduğunu söyler. Evlilik hediyesi kadının fiyatı değil aileler arası bağın işaretidir.",
            "Düğünde takılan altın daha sonra başka düğünde geri döner. Defter vardır ama amaç kâr değil ilişkilerin devamıdır.",
            "İnsan hayatı tam eşdeğere çevrilemez. Tazminat kaybı satın almaz; topluluğun sorumluluğunu tanır.",
            "Para bu alanlara girdiğinde ölçüm kolaylığı, insanı nesne gibi hesaplama tehlikesi taşır.",
        ], "BİRİNCİ KISIM · BORCUN AHLAKI", art="wedding-gifts", caption="Düğün hediyesi mal alışverişinden çok aileler arasında zaman içinde dolaşan ilişki ve sorumluluk işaretidir."),
        entry("Mezopotamya'nın kil tabletleri", [
            "İlk yazılı kayıtların önemli kısmı tapınak ve saray hesaplarıdır. Arpa, gümüş ve emek borçları kil tabletlere yazılır. Para madeni sikke olmadan önce hesap birimi olarak yaşar.",
            "Bakkal defterindeki lira, kasada o anda banknot olmasa da borcu ölçer. Mezopotamya gümüş birimi de çoğu işlemde tartılı metal dolaşmadan hesap görebilir.",
            "Hasat kötü olduğunda köylü borçlanır, faiz büyür ve aile üyelerini hizmete vermek zorunda kalabilir. Borç toplumsal çözülme yaratır.",
            "Hükümdarların dönemsel borç afları ekonomiyi ve özgür yurttaş tabanını sıfırlamaya çalışır.",
        ], "İKİNCİ KISIM · PARA VE ŞİDDET", art="clay-tablet", caption="Kil tablet para sikkesinden önce arpa, gümüş ve emek borçlarını ortak hesap diliyle kaydetti."),
        entry("Jübile: Borcu sıfırlamak", [
            "Eski Yakın Doğu hükümdarları bazı kişisel borçları siler, borç kölelerini serbest bırakır ve toprağı geri verebilirdi. Amaç yalnız merhamet değil düzenin çökmesini önlemekti.",
            "Monopoly oyununda bütün arsalar tek kişide toplandığında oyun teknik olarak sürer ama kimse hareket edemez. Tahtayı sıfırlamak oyuncuları geri getirir.",
            "Modern borç affı aynı koşullara sahip değildir; banka, tasarruf sahibi ve kamu dengeleri vardır. Yine de borcun doğal ve ebedi hak değil siyasi kurum olduğunu gösterir.",
            "Hangi borcun silineceği her dönemde güç mücadelesidir.",
        ], "İKİNCİ KISIM · PARA VE ŞİDDET", art="debt-jubilee", caption="Borç affı yalnız iyilik değil, toplumun bütün toprağının ve emeğinin alacaklılarda kilitlenmesini önleyen sıfırlama olabilir."),
        entry("Sikke ile asker aynı yolda", [
            "Graeber madeni paranın yayılmasını büyük ordular ve devlet vergileriyle ilişkilendirir. Devlet askere sikke verir, halktan vergiyi aynı sikkeyle ister; halk askere mal satarak sikke edinir.",
            "Kışlaya yakın pazarda ortak ödeme aracı hızla yerleşir. Vergi, paraya talep yaratır.",
            "Altın ve gümüş anonimdir; yabancılar arasında kişisel güven olmadan el değiştirir. Savaş ve köle ticareti bu taşınabilir değeri besleyebilir.",
            "Para yalnız barışçı takas kolaylığı değil, devlet ve şiddet ağının da ürünü olabilir.",
        ], "İKİNCİ KISIM · PARA VE ŞİDDET", art="coin-and-soldier", caption="Devlet askere sikke verip vergiyi sikkeyle isteyince kışla çevresinde para kullanan pazar kendiliğinden büyür."),
        entry("Kölelik ve insanın fiyatı", [
            "Savaş esiri toplumsal bağlarından koparılıp satılabilir nesneye dönüşür. Graeber için kölelik insan ekonomisinin piyasa tarafından parçalanmasının uç örneğidir.",
            "Bir kişinin adı, ailesi ve sözü silinip yalnız bedeni fiyatlanır. Sayı, şiddetin izini tarafsız işlem gibi gösterebilir.",
            "Tarih boyunca borç köleliği de aileleri bu sınıra itmiştir. Borçlu kişi sözleşmede insan, tahsilde teminat haline gelir.",
            "Modern özgür emek kölelikle aynı değildir, fakat insan zamanının fiyatlandırılması tartışmasını miras alır.",
        ], "İKİNCİ KISIM · PARA VE ŞİDDET", art="broken-name", caption="Kölelik insanı aile ve toplum bağlarından koparıp adı yerine fiyatı olan taşınabilir nesneye çevirir."),
        entry("Şiddet hesabı neden basitleştirir?", [
            "Eşit olmayan ilişkide ayrıntılı insan bağını görmezden gelmek için zor gerekir. Fatih, aldığı toprağın eski sözlerini tek sayı ve vergi tablosuna çevirebilir.",
            "Bir mahalleyi haritada boş arsa gibi boyamak, orada yaşayanların hikayesini siler. Cetvel kolaylaşır çünkü itiraz bastırılmıştır.",
            "Graeber piyasanın her zaman şiddet olduğunu söylemez. Tam ölçülebilir, kişisiz değişimin tarihsel olarak zorla açılmış alanlarda büyüyebildiğini gösterir.",
            "Ekonomik sayının arkasındaki toplumsal kopuşu sormak kitabın temel alışkanlığıdır.",
        ], "İKİNCİ KISIM · PARA VE ŞİDDET", art="violent-ledger", caption="Şiddet karmaşık insan bağlarını susturduğunda toprak ve emek kolayca tek sütunlu hesap tablosuna dönüşür."),
        entry("Ortaçağda kredi dünyası", [
            "Büyük imparatorlukların çözülmesiyle sikke dolaşımı bazı yerlerde azalır, yerel kredi ve güven ağları öne çıkar. Para yok olmaz; hesap olarak yaşamaya devam eder.",
            "Pazar esnafı birbirine gün sonunda metal ödemek yerine borçları karşılıklı mahsup edebilir. Para çantadan çok defterde dolaşır.",
            "Dini gelenekler faiz, tefecilik ve adil fiyat üzerine kurallar geliştirir. Ekonomi ahlaktan ayrı alan sayılmaz.",
            "Graeber tarih ritmini sikke dönemleri ile kredi dönemlerinin salınımı olarak anlatır; gerçek coğrafya bundan daha çeşitli olabilir.",
        ], "ÜÇÜNCÜ KISIM · BEŞ BİN YILLIK SALINIM", art="credit-market", caption="Metal para azalsa bile esnafın karşılıklı defteri ve güveni değişimi sürdüren kredi parası yaratabilir."),
        entry("Din, günah ve kefaret dili", [
            "Birçok dilde borç ile suç veya günah arasında yakınlık vardır. İnsan Tanrı'ya, atalara veya topluma ödenemez borç taşıdığı hissiyle yaşar.",
            "Hayat armağansa bedeli nedir? Ödenemeyen borç suçluluk üretebilir; ritüel, kurban veya bağış hesabı kapatma yolu sunar.",
            "Graeber dini yalnız ekonomi kopyası saymaz. Karşılıklı olarak borç dili ahlakı, ahlak dili ekonomik yükümlülüğü biçimlendirir.",
            "Modern 'başarısız borçlu' utancı da mali durumu kişisel değer hükmüne çevirebilir.",
        ], "ÜÇÜNCÜ KISIM · BEŞ BİN YILLIK SALINIM", art="moral-debt", caption="Ödenemeyen manevi borç fikri ekonomik yükümlülüğü suç, günah ve kefaret diliyle birbirine bağlar."),
        entry("Kapitalist kredi makinesi", [
            "Modern banka kredisi gelecekteki emeği bugünkü paraya çevirir. Şirket ve devlet borçlanarak yatırım yapar; büyüme gelecekteki gelirin borcu karşılayacağı beklentisine dayanır.",
            "Henüz yapılmamış ev için kredi açılır, inşaat başlar ve yıllar sürecek çalışma bugünün duvarına dönüşür.",
            "Kredi üretken kapasite açabilir, aynı zamanda geleceği alacaklıya bağlar. Büyüme durduğunda borç yükü sertleşir.",
            "Para yalnız mevcut zenginliğin jetonu değil, geleceğe ilişkin toplumsal sözleşmedir.",
        ], "ÜÇÜNCÜ KISIM · BEŞ BİN YILLIK SALINIM", art="future-mortgage", caption="Kredi henüz kazanılmamış gelecekteki emeği bugünün evine, fabrikasına veya devlet harcamasına çevirir."),
        entry("Devlet borcu ve özel borç", [
            "Büyük devlet ve şirket borçları yeniden yapılandırılabilirken küçük borçluya ahlaki sorumluluk hatırlatılır. Graeber bu çifte standardı sorgular.",
            "Banka batınca sistemik risk, aile batınca kişisel hata denmesi gücün ahlak dilini nasıl dağıttığını gösterir.",
            "Her kurtarma haksız, her tahsil yanlış değildir. Fakat kuralın kim için esnediği meşruiyetin merkezindedir.",
            "Borç ahlakını eşit uygulamak, alacaklının risk ve sorumluluğunu da hesaba katmayı gerektirir.",
        ], "ÜÇÜNCÜ KISIM · BEŞ BİN YILLIK SALINIM", art="double-standard", caption="Büyük borçluya sistem, küçüğe ahlak dersi verilmesi borç kurallarının güçle birlikte esnediğini gösterir."),
        entry("1971 sonrası işaret para", [
            "Doların altınla resmi bağı kesildiğinde dünya parası daha açık biçimde devlet ve kredi güvenine dayandı. Graeber bunu yeni bir sanal para döneminin işareti sayar.",
            "Bankadaki bakiye kasada adınıza ayrılmış banknot destesi değildir. Banka kredisi verildiğinde yeni mevduat yaratabilir; para büyük ölçüde hesap kaydıdır.",
            "Sanal olması gerçek olmadığı anlamına gelmez. Vergi, hukuk ve üretim ağı işarete güç verir.",
            "Dijital ödeme eski kil tabletin uzak akrabasıdır: Toplumsal borç ortak defterde yaşar.",
        ], "DÖRDÜNCÜ KISIM · BUGÜN", art="digital-tablet", caption="Kil tablet ile banka ekranı farklı teknolojiler olsa da para çoğu zaman ortak defterdeki toplumsal alacak kaydıdır."),
        entry("Kredi kartındaki görünmez ilişki", [
            "Kartla tek dokunuş alışverişi zahmetsiz gösterir. Arka planda banka, işyeri, ağ şirketi, faiz, ücret ve risk puanı çalışır.",
            "Nakit acısı görünmeyince gelecek gelir kolay harcanır. Tasarım ekonomik olduğu kadar psikolojiktir.",
            "Borçlu yalnız para almaz; davranışı ölçülür, sınıflandırılır ve gelecekteki erişimi belirlenir. Kredi skoru yeni itibar defteridir.",
            "Graeber'in yöntemi kartı şeytanlaştırmak değil, kolay yüzeyin altındaki kurum ve güç ilişkisini görünür kılmaktır.",
        ], "DÖRDÜNCÜ KISIM · BUGÜN", art="credit-card-network", caption="Kartın tek dokunuşunun altında faiz, veri, puanlama ve gelecekteki emek hakkında geniş bir ilişki ağı çalışır."),
        entry("Borç affı adil midir?", [
            "Af borçluyu rahatlatır, fakat düzenli ödeyenin veya küçük tasarruf sahibinin hakkı ne olacak? Modern toplumda sonuçlar eski jübileden daha karmaşıktır.",
            "Öte yandan ödenemeyeceği baştan belli borcu sürdürmek üretimi, aileyi ve toplumsal katılımı kilitleyebilir. İflas hukuku bu yüzden ekonomik sıfırlama sağlar.",
            "Adil çözüm borcun kaynağını, alacaklının riskini, kamusal maliyeti ve gelecekte aynı sorunu önleyecek kuralları birlikte tartar.",
            "Graeber kesin teknik plan yerine ahlaki hayal gücünü açar: Bütün alacaklar insan hayatından daha kutsal değildir.",
        ], "DÖRDÜNCÜ KISIM · BUGÜN", art="debt-reset-scale", caption="Borç affı borçlu, alacaklı ve toplumun geleceğini aynı terazide tartmayı gerektiren siyasi bir sıfırlamadır."),
        entry("Kitabın eleştirilen yerleri", [
            "Graeber beş bin yılı tek ciltte dolaşırken dönemler ve coğrafyalar arasında büyük sıçramalar yapar. Bazı uzmanlar kaynak kullanımını, borç-sikke salınımını ve takas anlatısının hedefini fazla genelleyici bulur.",
            "Antropolojik örnekler ekonomik bütünlüğü temsil etmeyebilir; modern iktisat da paranın tek çizgili takas kökenini bütünüyle savunmaz.",
            "Yine de kitap güçlü bir düzeltme yapar: Parayı toplum dışı doğal nesne değil tarihsel kurum olarak görür.",
        ], "SON DURAKLAR"),
        entry("Borç ile ahlakı ayırmadan düşünmek", [
            "Bir borcu değerlendirirken yalnız miktarı değil rızayı, bilgi eşitliğini, faizi, riski ve zorunluluğu sorun. Alacaklı hangi kaybı üstlenmiş, hangi güvenceden yararlanmış?",
            "Aynı zamanda söz vermenin güven için değerini koruyun. Bütün borcu zulüm saymak işbirliğinin zaman köprüsünü yıkar.",
            "Denge, sözü ciddiye alırken insanı rakama indirgememektir.",
        ], "SON DURAKLAR"),
        entry("Evinizdeki üç borç", [
            "Parasal borcu, ilişki borcunu ve toplumsal borcu ayrı yazın. Bankaya taksit, dosta iyilik, önceki kuşağın kurduğu altyapı aynı kelimeyi taşısa da aynı biçimde ödenmez.",
            "Hangisi sayıyla kapanır, hangisi karşılıklılık ister, hangisi sonraki kişiye aktaracağınız sorumluluktur?",
            "Bu ayrım suçluluk sisini dağıtır ve gerçek yükümlülüğü daha dürüst kılar.",
        ], "SON DURAKLAR"),
        entry("Bir cümlede kitabın özü", [
            "Borç paradan önce gelen insan yükümlülüğünün sayı ve vadeye çevrilmiş halidir; bu yüzden her borç sözleşmesinin arkasında ahlak, devlet, şiddet ve kimin hesabının silinebileceği sorusu vardır.",
            "Akılda kalacak görüntü kil tablet ile kredi kartıdır: Teknoloji değişir, fakat ortak defterin kurallarını kimin yazdığı belirleyici kalır.",
        ], "SON DURAKLAR"),
    ]))


BOOKS.append(base(182, "Felsefi Soruşturmalar", "Ludwig Wittgenstein",
    "Sözcüklerin gizli özünü aramak yerine günlük kullanımına bakmayı; dil oyunları, aile benzerliği, kural izleme, özel dil ve zihin kavramları üzerinden felsefi düğümleri çözmeyi öğreten sıra dışı rehber.",
    "#5A6071", "Philosophische Untersuchungen", "felsefi-sorusturmalar",
    [
        {"id": 1, "title": "Wiley - Philosophical Investigations resmi sayfası", "url": "https://www.wiley-vch.de/en/areas-interest/humanities-social-sciences/philosophy-12pl/historical-western-philosophy-12pl4/wittgenstein-12pl45/philosophical-investigations-978-1-4051-5928-9"},
        {"id": 2, "title": "Stanford Encyclopedia of Philosophy - Wittgenstein", "url": "https://plato.stanford.edu/entries/wittgenstein/"},
        {"id": 3, "title": "Internet Encyclopedia of Philosophy - Wittgenstein", "url": "https://iep.utm.edu/wittgenstein/"},
        {"id": 4, "title": "Routledge - Guidebook to Philosophical Investigations", "url": "https://www.routledge.com/The-Routledge-Guidebook-to-Wittgensteins-Philosophical-Investigations/McGinn/p/book/9780415452564"},
    ], [
        entry("Bu kitap nasıl okunmalı?", [
            "Felsefi Soruşturmalar baştan sona tek kanıt kuran ders kitabı değildir. Kısa paragraflar, sorular, hayali konuşmalar ve örneklerle okurun düşünme alışkanlığını değiştirir.",
            "Wittgenstein teori kurmaktan çok dilin bizi büyülediği yerleri gösterir. Felsefi sorun bazen yeni bilgiyle değil kullandığımız kelimenin yollarını görerek çözülür.",
            "Rehber her ünlü sözü bağlamında tutacak; 'anlam kullanımdır' ifadesini her kelime için katı tanım yapmayacak.",
        ], "BAŞLANGIÇ"),
        entry("Augustinus'un dil resmi", [
            "Kitap, çocuğun yetişkinlerin nesne gösterip ad söylemesiyle dil öğrendiği resimle açılır. Bu resimde her sözcük bir nesnenin adı, cümle adlar dizisidir.",
            "Market listesinde 'elma, ekmek, süt' için model iyi çalışır. Ama 've', 'belki', 'acı', 'oyun' veya 'yarın' hangi nesnenin adıdır?",
            "Wittgenstein modelin yanlış değil dar olduğunu gösterir. Bir dil işlevini bütün dil sanınca sahte sorunlar doğar.",
            "Felsefi terapi ilk adımda şunu sorar: Elinizdeki resim hangi örnekleri görünmez kılıyor?",
        ], "BİRİNCİ KISIM · DİLİN ÇEŞİTLİ İŞLERİ", art="label-picture", caption="Her sözcüğü nesne etiketi sayan dil resmi alışveriş listesinde çalışır, fakat dilin bütün işlerini açıklayamaz."),
        entry("İnşaatçıların küçük dili", [
            "Bir işçi 'blok', 'sütun', 'döşeme' diye bağırır, diğeri doğru taşı getirir. Sözcük burada nesne adı kadar emirdir; anlam ortak işteki görevinden doğar.",
            "Mutfakta 'tuz!' demek sözlük cümlesi değil uzat, getir veya eksik anlamına gelebilir. Bağlam kelimeye eylem verir.",
            "Wittgenstein böyle küçük dil oyunları kurarak karmaşık dilin farklı kullanım parçalarını görünür kılar.",
            "Dil yalnız dünyayı betimlemez; sorar, şaka yapar, söz verir, dua eder, ölçer ve teselli eder.",
        ], "BİRİNCİ KISIM · DİLİN ÇEŞİTLİ İŞLERİ", art="builders-language", caption="İnşaat alanında 'blok' sözü etiket değil ortak iş içinde taşı getiren bir hamledir."),
        entry("Anlam kullanımda yaşar", [
            "Bir kelimenin anlamını yalnız kafadaki görüntü veya sözlük açıklamasıyla değil, dilde nasıl kullanıldığıyla ararız. Para da kağıdından çok alışverişteki rolüyle paradır.",
            "'Oyun' kelimesini çocuk oyunu, futbol ve kart oyununda kullanırız. Hepsinde ortak tek öz bulamasak da kullanım yollarını biliriz.",
            "Kullanım keyfi değildir. Topluluk, bağlam ve öğrenilmiş kurallar hangi hamlenin yerinde olduğunu belirler.",
            "Sözcük alet çantasındaki alet gibidir; biçiminden önce hangi işte nasıl tutulduğuna bakın.",
        ], "BİRİNCİ KISIM · DİLİN ÇEŞİTLİ İŞLERİ", art="word-toolbox", caption="Sözcükler aynı biçimde duran etiketler değil, farklı dil işlerinde kullanılan aletler gibi anlam kazanır."),
        entry("Aile benzerliği", [
            "Oyunların hepsinde eğlence, rekabet veya kural ortak değildir. Bazıları yalnız, bazıları kazanan olmadan oynanır. Yine de birbirine çapraz benzerliklerle bağlıdır.",
            "Aile fotoğrafında herkesin aynı burnu yoktur; birinde göz, diğerinde gülüş, başkasında yürüyüş benzer. Tek özellik değil örtüşen ağ aileyi tanıtır.",
            "Bir kavramın sınırı bulanık diye işe yaramaz olmaz. 'Şehir' nerede biter sorusu zor olsa da şehir kelimesini kullanırız.",
            "Felsefe her kavram için gizli ortak öz istemeyi bıraktığında gerçek kullanım çeşitliliğini görür.",
        ], "BİRİNCİ KISIM · DİLİN ÇEŞİTLİ İŞLERİ", art="family-photos", caption="Tek ortak yüz özelliği olmadan örtüşen göz, gülüş ve yürüyüş benzerlikleri aileyi birbirine bağlar."),
        entry("Yaşam biçimi", [
            "Dil oyunu havada duran kod değildir; insanların çalışma, kutlama, bakım, eğitim ve çatışma pratiklerine gömülüdür. Wittgenstein buna yaşam biçimi der.",
            "'Geçmiş olsun' cümlesinin anlamı yalnız sözcüklerde değil hastalık, ziyaret ve nezaket kurumundadır.",
            "Tamamen yabancı yaşam biçiminde aynı işareti çevirsek bile neyin şaka, emir veya ayıp olduğunu kaçırabiliriz.",
            "Anlamak sözlüğe ek olarak ortak dünyada nasıl hareket edildiğini öğrenmektir.",
        ], "İKİNCİ KISIM · KURAL VE TOPLULUK", art="form-of-life", caption="Sözün anlamı yalnız sözlükte değil hastalık, ziyaret ve bakım gibi paylaşılan yaşam pratiklerinde yerleşir."),
        entry("Kural yolu tek başına çizmez", [
            "Bir sayı dizisini '2, 4, 6, 8' diye sürdürün. Kuralı artı iki sayarsınız, fakat geçmiş örneklerle uyumlu başka karmaşık kurallar da uydurulabilir.",
            "Yazılı tarif 'kısık ateş' der; yeni aşçı ocağın ve yemeğin içinde bunun ne olduğunu uygulamayla öğrenir.",
            "Her kuralı açıklamak için yeni kural istersek sonsuz gerileme çıkar. Bir yerde topluluğun yerleşmiş uygulaması açıklamayı durdurur.",
            "Kural izlemek özel yorum seçmek değil, eğitimle edinilmiş ortak pratiğe katılmaktır.",
        ], "İKİNCİ KISIM · KURAL VE TOPLULUK", art="number-rule", caption="Geçmiş sayı dizisi tek başına gelecekteki hamleyi zorunlu kılmaz; kural ortak uygulamada yön kazanır."),
        entry("Bir kez doğru yapmak yetmez", [
            "Tek davranışın kurala uygun olması tesadüf olabilir. Kural izlemek tekrar edilebilir ölçü ve doğru-yanlış ayrımı gerektirir.",
            "Bir okçu bir kez hedefi gözleri kapalı vurabilir; bu nişan alma tekniğini bildiğini göstermez.",
            "Kişinin 'ben böyle yorumladım' demesi her kullanımı doğru yapmaz. Dil oyununun toplumsal kontrolü vardır.",
            "Wittgenstein anlamı tamamen özel zihinden çıkarıp kamusal öğrenme ve düzeltme alanına yerleştirir.",
        ], "İKİNCİ KISIM · KURAL VE TOPLULUK", art="lucky-arrow", caption="Tek isabet kural bilgisi değildir; doğru kullanım tekrar, eğitim ve düzeltilebilir ölçü gerektirir."),
        entry("Özel dil mümkün mü?", [
            "Yalnız benim erişebildiğim iç duyuma her geldiğinde 'S' yazdığımı düşünün. Doğru kullandığımı kontrol edecek bağımsız ölçü yoksa doğru görünmesi ile doğru olması ayrılmaz.",
            "Her gün kendi terazinizin doğru olduğunu yine aynı teraziyle sınamak gibi, özel işaret kendi ölçüsünü kuramaz.",
            "Bu, acının gerçek olmadığı veya başkasının acımı benim kadar bildiği anlamına gelmez. Acı dilinin kullanımını yüz, davranış, yardım ve öğrenme içinde ediniriz.",
            "İç deneyim özeldir; onu anlamlı dilde ifade etmenin ölçüsü kamusal yaşamdan gelir.",
        ], "İKİNCİ KISIM · KURAL VE TOPLULUK", art="private-diary-mark", caption="Yalnız sahibinin eriştiği işaret doğru kullanımı yine kendisiyle ölçerse, doğruluk ile doğru sanma ayrımı kaybolur."),
        entry("Kutudaki böcek", [
            "Herkesin kutusunda yalnız kendisinin gördüğü bir şey var ve herkes ona böcek diyor olsun. Kutuların içi farklı, hatta boş olabilir; kelimenin kamusal kullanımı bundan etkilenmez.",
            "'Böcek' sözcüğünün işlevi gizli nesnenin resmiyle değil konuşmadaki yeriyle belirlenir. Gizli şey açıklama çarkında boşa döner.",
            "Benzetme bilincin önemsiz olduğunu söylemez. İç nesneyi dil anlamının tek temeli yapmanın sorununu gösterir.",
            "Zihni açıklarken kafanın içindeki hayali nesneleri çoğaltmak yerine kavramların kullanımına bakarız.",
        ], "ÜÇÜNCÜ KISIM · ZİHİN KAVRAMLARI", art="beetle-box", caption="Kutudaki gizli böcek ne olursa olsun kelimenin ortak anlamı konuşmadaki kamusal işlevinden doğar."),
        entry("Acımı nereden biliyorum?", [
            "Kendi acımı gözlemleyip kanıt toplayarak bilmem; acı içindeyimdir. Başkasının acısını ise davranış, söz ve durumdan anlarım.",
            "Doktor 'acı çektiğinden emin misin?' diye kanıt istemez, yerini ve şiddetini sorar. Birinci kişi cümlesi rapordan çok ifadedir.",
            "Bu dilbilgisi farkını unutunca kendi zihnimize dış nesne gibi bakıp sonsuz kesinlik ararız.",
            "Wittgenstein felsefi düğümü psikolojik deneyle değil, 'bilmek' kelimesinin farklı işlevleriyle çözer.",
        ], "ÜÇÜNCÜ KISIM · ZİHİN KAVRAMLARI", art="pain-expression", caption="Kendi acım kanıtla keşfettiğim nesne değil yaşadığım durumdur; başkasının acısı ortak ifadelerden anlaşılır."),
        entry("İç süreç dış ölçü ister", [
            "Anlamak, niyet etmek veya hatırlamak içsel olay olabilir, fakat bu kavramları hangi durumda kullandığımız dış ölçülere bağlıdır.",
            "Öğrenci 'anladım' der ve yeni problemi çözer. Çözüm, gizli anlama parıltısının değil becerinin ölçüsüdür.",
            "İç süreç yok demek davranışçılık olurdu. Wittgenstein iç olanın kavramdaki rolünü yanlış kurmamamızı ister.",
            "Zihni görünmez makine gibi tasarlamak yerine insanın bütün davranış ve yaşam bağlamını görürüz.",
        ], "ÜÇÜNCÜ KISIM · ZİHİN KAVRAMLARI", art="understanding-test", caption="Anlama içte parlayan özel nesne değil, yeni durumda ne yapabildiğimizle ölçülen canlı bir beceridir."),
        entry("Okuma makinesi yanılsaması", [
            "Bir kişi metni akıcı okur, diğeri harfleri tek tek söyler. Okumanın başladığı tek iç anı veya zihinsel dişliyi bulmak isteriz.",
            "Oysa okuma farklı bağlamlarda eğitim, hız, hata düzeltme ve anlamayla kurulan yetiler ailesidir. Gizli tek süreç aramak kavramı daraltır.",
            "Piyanistin notayı takip etmesi ile çocuğun hecelemesi aynı ailede farklı örneklerdir.",
            "Wittgenstein mekanizma sorusunu yasaklamaz; nöroloji süreçleri inceler. Felsefenin yaptığı, 'okuma' kelimesinin tek mekanizma adı olmadığını göstermektir.",
        ], "ÜÇÜNCÜ KISIM · ZİHİN KAVRAMLARI", art="reading-family", caption="Akıcı okuma, heceleme ve nota takibi tek gizli dişlinin değil örtüşen beceriler ailesinin üyeleridir."),
        entry("Felsefi sinek şişeden nasıl çıkar?", [
            "Wittgenstein felsefenin amacını sineğe şişeden çıkış yolunu göstermek diye anlatır. Sinek camı görmez, aynı yere çarpar; sorun dış dünyada değil hareket resmindedir.",
            "Zihin 'içeride nesne', zaman 'akan madde', anlam 'kelimenin taşıdığı paket' diye düşünülünce belirli sorular kaçınılmaz görünür.",
            "Kavramın farklı kullanımını göstermek camın kenarını görünür yapar. Yeni teori değil, eski büyünün çözülmesi gelir.",
            "Felsefi huzur bütün merakı bitirmek değil sahte zorunluluğu ortadan kaldırmaktır.",
        ], "DÖRDÜNCÜ KISIM · FELSEFİ TERAPİ", art="fly-bottle", caption="Sinek görünmez cama aynı yerden çarpar; dil resmi fark edilince felsefi çıkış yolu açılabilir."),
        entry("Dil tatile çıktığında", [
            "Felsefi sorunlar kelimeler günlük işinden koparıldığında doğar der Wittgenstein. 'Zaman nedir?' sorusu zaman kelimesini ölçme, bekleme ve hatırlama kullanımlarından ayırabilir.",
            "Çekici vitrinde döndürüp 'çekicin özü nedir?' diye sormak yerine çivide, sökmede ve düzeltmede nasıl kullanıldığına bakın.",
            "Gündelik dil her zaman kusursuz değildir, fakat kavramın evini gösterir. Filozof kelimeyi boş arazide çalıştırmaya zorlamamalıdır.",
            "Soruyu yok etmek yerine onu gerçek kullanım örnekleriyle yeniden kurarız.",
        ], "DÖRDÜNCÜ KISIM · FELSEFİ TERAPİ", art="word-on-holiday", caption="Kelime günlük işinden tatile çıkınca boşlukta dönmeye başlar; onu kullanım evine geri getirmek düğümü çözer."),
        entry("Açıklama bir yerde biter", [
            "Her gerekçenin arkasına yeni gerekçe istersek sonsuza gideriz. Bir yerde 'yaptığımız şey bu' diyen yerleşmiş uygulamaya ulaşırız.",
            "Satrançta filin çapraz gitmesini neden diye sorup tarihini açıklayabilirsiniz; oyunun içinde son cevap kuralın nasıl öğretildiği ve uygulandığıdır.",
            "Bu kör itaat değildir. Uygulamalar eleştirilebilir; eleştiri de başka ölçü ve yaşam amaçları içinde yapılır.",
            "Wittgenstein zeminsiz kesinlik arzusunu sınırlar. Dil havada değil insan eyleminin kayasında durur.",
        ], "DÖRDÜNCÜ KISIM · FELSEFİ TERAPİ", art="bedrock-practice", caption="Gerekçe zinciri sonunda insanların birlikte yaptığı ve öğrettiği uygulamanın kayasına dayanır."),
        entry("Tractatus'tan dönüş", [
            "Genç Wittgenstein dili dünyanın mantıksal resmini kuran daha tek biçimli yapı olarak görmüştü. Soruşturmalar bu idealin günlük dil çeşitliliğini kaçırdığını gösterir.",
            "Tek raylı tren modeli yerine yollar, patikalar, meydanlar ve oyun alanları olan şehir gelir.",
            "Bu tamamen geçmişi reddetmek değildir; dil ile dünya ilişkisi ilgisi sürer. Fakat tek öz yerine çoğul kullanım öne çıkar.",
            "Filozofun kendi eski kitabını eleştirmesi düşünsel cesaretin kitabın biçimine dönüşmesidir.",
        ], "DÖRDÜNCÜ KISIM · FELSEFİ TERAPİ", art="one-rail-to-city", caption="Tek mantık rayı yerini farklı işlere giden sokak ve patikalardan oluşan yaşayan dil şehrine bırakır."),
        entry("Kullanım her şeyi haklı çıkarır mı?", [
            "Bir kelimenin toplumda kullanılması o kullanımın ahlaken doğru olduğunu göstermez. Ayrımcı söz de yerleşmiş olabilir; anlam açıklaması eleştirinin yerine geçmez.",
            "Wittgenstein dilin nasıl işlediğini betimler. Hangi yaşam biçimini seçmemiz gerektiği için ek ahlaki ve siyasi gerekçeler gerekir.",
            "Ayrıca yeni bilimsel kavramlar günlük dilden uzaklaşabilir. Kullanım yaklaşımı onları dışlamaz; laboratuvar da kendi eğitimli dil oyununu kurar.",
        ], "SON DURAKLAR"),
        entry("Topluluk bireyi ezer mi?", [
            "Anlamın kamusal ölçüye dayanması bireyin hiç yenilik yapamayacağı anlamına gelmez. Yeni kullanım anlaşılır bağlar kurarsa toplulukta yerleşebilir.",
            "Şair kelimeyi beklenmedik yerde kullanır, fakat etki eski yolları tamamen unutmadığı için duyulur.",
            "Özel deneyim korunur; yalnız anlamı tek kişinin denetimsiz işaretine bağlamak reddedilir.",
        ], "SON DURAKLAR"),
        entry("Gündelik kavram soruşturması", [
            "Sizi kilitleyen bir kelime seçin: başarı, gerçek, zeka veya özgürlük. Tek tanım aramak yerine beş farklı cümlede nasıl kullanıldığını yazın.",
            "Hangi örnekler aile benzerliği taşıyor, hangi kullanım başka dil oyununa ait? Sorununuz kelimenin tek öz taşımaması yüzünden mi büyüyor?",
            "Bu alıştırma cevap vermezse bile camın nerede olduğunu gösterir.",
        ], "SON DURAKLAR"),
        entry("Bir cümlede kitabın özü", [
            "Felsefi düğümlerin çoğu sözcükleri günlük yaşam oyunlarından koparıp tek gizli öz aradığımızda doğar; kullanım çeşitliliğini görmek düşünceyi yeniden hareket ettirir.",
            "Akılda kalacak görüntü alet çantasıdır: Bütün kelimeler aynı çekiç değildir ve hangi işi yaptıklarına bakmadan biçimlerinden anlam çıkaramayız.",
        ], "SON DURAKLAR"),
    ]))


BOOKS.append(base(195, "Televizyon Öldürüyor", "Neil Postman",
    "Bir toplumun ne konuştuğunu yalnız sansürün değil konuştuğu aracın biçimlendirdiğini; siyaset, haber, din ve eğitimin televizyon ekranında neden gösteriye dönüştüğünü anlatan medya eleştirisini telefon çağına taşıyan rehber.",
    "#6C4D48", "Amusing Ourselves to Death", "televizyon-olduruyor",
    [
        {"id": 1, "title": "Penguin Random House - Amusing Ourselves to Death", "url": "https://www.penguinrandomhouse.com/books/297276/amusing-ourselves-to-death-by-neil-postman/"},
        {"id": 2, "title": "NYU Steinhardt - Neil Postman ve Medya Ekolojisi", "url": "https://steinhardt.nyu.edu/news/50-years-media-studies-nyu-steinhardt"},
        {"id": 3, "title": "Pew Research Center - Haber tüketimi", "url": "https://www.pewresearch.org/topic/news-habits-media/news-platforms-sources/"},
    ], [
        entry("Bu kitap nasıl okunmalı?", [
            "Türkçe başlık serttir; özgün başlık 'Kendimizi Ölesiye Eğlendirmek' anlamına gelir. Postman televizyonun insan öldürdüğünü değil kamusal düşünceyi eğlence biçimine çevirdiğini savunur.",
            "Kitap 1985 ABD televizyonuna bakar. İnternet ve sosyal medya yoktur, fakat araç biçiminin düşünceyi nasıl yönlendirdiği sorusu daha da günceldir.",
            "Rehber ekranı şeytanlaştırmayacak; Postman'ın güçlü sezgisini veri, erişim ve yeni medya farklarıyla sınayacak.",
        ], "BAŞLANGIÇ"),
        entry("Orwell mi Huxley mi?", [
            "Orwell gerçeğin yasaklandığı, kitapların yakıldığı ve insanların acıyla yönetildiği dünyadan korkuyordu. Huxley ise gerçeğin ilgisizlikte boğulduğu, kimsenin kitap okumak istemediği haz toplumunu hayal etti.",
            "Postman Amerika'nın Huxley'e yaklaştığını söyler. Sansürcü kapıyı kilitlemeden de sürekli eğlence ciddi düşünceyi masadan kaldırabilir.",
            "Kütüphane açıkken kimse uzun metne dikkat veremiyorsa özgür erişim tek başına yetmez. Dikkat kamusal kaynaktır.",
            "Kitabın alarmı budur: Bizi baskılayan şeye direnebiliriz; sevdiğimiz oyalanmanın yönetimini fark etmek daha zordur.",
        ], "BİRİNCİ KISIM · ARAÇ DÜŞÜNCEYİ BİÇİMLENDİRİR", art="orwell-huxley", caption="Gerçek yalnız yasakla değil, sonsuz eğlence içinde ilgisiz hale gelerek de kamusal hayattan kaybolabilir."),
        entry("Araç yalnız boru değildir", [
            "Bir iletişim aracı aynı mesajı nötr biçimde taşımaz. Dumanla felsefe kitabı anlatamaz, televizyonda sessiz uzun kanıt izleyici kaybedebilir.",
            "Şişe suyun tadını, miktarını ve içme hızını etkiler. Medya da hangi içeriğin kolay üretileceğini ve inanılır görüneceğini biçimlendirir.",
            "Postman bunu medya metaforu olarak düşünür: Saat zamanı, yazı hakikati, televizyon kamusal görünürlüğü başka ölçülere bağlar.",
            "Bu teknolojik kader değildir; insanlar aracı düzenleyebilir. Fakat biçimin eğilimini görmeden içerik düzeltmek eksik kalır.",
        ], "BİRİNCİ KISIM · ARAÇ DÜŞÜNCEYİ BİÇİMLENDİRİR", art="message-container", caption="İletişim aracı nötr boru değil, hangi mesajın kolay akacağını belirleyen biçimli bir kaptır."),
        entry("Tipografinin ağır zamanı", [
            "Basılı kültür uzun cümle, sırayla ilerleyen kanıt ve okuyucunun geri dönmesine imkan verir. On dokuzuncu yüzyıl dinleyicileri saatler süren siyasi tartışmaları takip edebiliyordu.",
            "Kitap masada bekler; okur durur, not alır ve önceki sayfaya döner. Tempo okurun kısmen kontrolündedir.",
            "Postman bu dönemi romantikleştirir. Okuryazarlık eşit dağılmamış, gazeteler her zaman ciddi olmamıştır. Yine de baskının akıl yürütmeye elverişli yönünü gösterir.",
            "Araç belirli zihin alışkanlığını teşvik eder: Sabır, bağlantı ve çelişki takibi.",
        ], "BİRİNCİ KISIM · ARAÇ DÜŞÜNCEYİ BİÇİMLENDİRİR", art="slow-print", caption="Basılı sayfa okuyucuya durma, geri dönme ve uzun kanıtın halkalarını kendi temposunda izleme imkanı verir."),
        entry("Telgraf bağlamı koparıyor", [
            "Telgraf uzak bilgiyi hızla taşır, fakat çoğu haber alıcının eylemiyle bağlantısızdır. Bugün öğrenilen olay yarın yenisiyle yer değiştirir.",
            "Bin kilometre ötede küçük bir skandalı anında bilirsiniz, yan sokaktaki kararı kaçırırsınız. Bilgi miktarı artarken kullanım bağı azalır.",
            "Fotoğraf olayı kanıttan çok çarpıcı görüntüye bağlar. Telgrafın hızına fotoğrafın etkisi eklenince televizyonun zemini oluşur.",
            "Postman için sorun uzak bilgiden haberdar olmak değil, bağlamsız parçaların bilgi sanılmasıdır.",
        ], "BİRİNCİ KISIM · ARAÇ DÜŞÜNCEYİ BİÇİMLENDİRİR", art="telegraph-fragments", caption="Telgraf uzak olay parçalarını hızla getirirken onları açıklayan bağlam ve alıcının eylem imkanını geride bırakabilir."),
        entry("Şimdi bunu bırakıp ötekine geçiyoruz", [
            "Televizyon haberinde savaş görüntüsünden reklama, cinayetten hava durumuna aynı sunucu tonu ve kısa geçişle gidilir. Olayların ağırlığı ortak akışta düzleşir.",
            "Bir cenaze konuşmasının ortasında deterjan şarkısı çalmak uygunsuz olurdu. Ekran akışı bu uyumsuzluğu normalleştirir.",
            "İzleyicinin önceki haberi düşünmesi için sessizlik yoktur. Yeni görüntü eskisini kovar; tepki duygu düzeyinde kalır.",
            "Postman'ın ünlü 'şimdi bunu' eleştirisi parçalanmış dikkat ve bağlamsızlığın dilidir.",
        ], "İKİNCİ KISIM · HER ŞEY GÖSTERİ", art="news-to-ad", caption="Savaş görüntüsünden reklama tek geçiş, olayların ahlaki ağırlığını aynı eğlence akışında düzleştirebilir."),
        entry("Haber neden yüz ister?", [
            "Televizyonda haber sunucusunun görünüşü, sesi ve güven veren kişiliği içeriğin kanıtı kadar önem kazanır. Hakikat iyi performansla karışır.",
            "Doktor rolündeki oyuncu ekranda sakin görünür diye tıbbi iddiası doğru olmaz. Fakat görüntü sözden önce duygusal güven üretir.",
            "Kısa süre ve reklam arası karmaşık belirsizliği taşımaz. Kesin cümle ile çarpıcı görüntü ödüllenir.",
            "Postman haberi gereksiz saymaz; televizyon biçiminin hangi haber türünü seçtiğini sorgular.",
        ], "İKİNCİ KISIM · HER ŞEY GÖSTERİ", art="trusted-face", caption="Ekranda güven veren yüz, kanıtın yerini almadan önce habere duygusal doğruluk hissi verebilir."),
        entry("Siyaset otuz saniyeye sığarsa", [
            "Televizyon reklamı adayın programını değil akılda kalıcı imgesini satar. Seçmen yurttaştan izleyiciye, tartışma marka yarışına dönüşebilir.",
            "Bir vergi planını otuz saniyede anlatmak zordur; rakibin kötü fotoğrafını göstermek kolaydır. Araç kolay olanı seçime taşır.",
            "Görüntü politikada her zaman vardı, fakat televizyon sürekli performansı merkezi hale getirir. Adayın saç kesimi bütçe hesabıyla aynı ekranda yarışır.",
            "Demokrasi bilgi kadar dikkat süresi ve tartışma biçimine dayanır.",
        ], "İKİNCİ KISIM · HER ŞEY GÖSTERİ", art="campaign-commercial", caption="Siyasi program uzun açıklama isterken kısa reklam adayları fikirden çok marka ve görüntü olarak yarıştırır."),
        entry("Din gösteriye dönüşünce", [
            "Dini törenin kutsallığı mekan, cemaat, sessizlik ve gelenekle kurulur. Televizyon vaizi aynı ekranı komedi ve reklamla paylaşınca biçim değişir.",
            "İzleyici kanalı tek tuşla değiştirebilir; vaaz dikkati tutmak için sahne performansına yaklaşır. Kutsal deneyim tüketici seçimine girer.",
            "Postman inancı değil televizyon ortamının onu nasıl yeniden biçimlendirdiğini eleştirir.",
            "Aynı soru eğitim ve kültür için de geçerlidir: Görünür olmak uğruna araç neyi feda ettiriyor?",
        ], "İKİNCİ KISIM · HER ŞEY GÖSTERİ", art="televised-pulpit", caption="Kutsal tören reklam ve eğlenceyle aynı ekranı paylaşınca dikkat rekabeti içeriğin biçimini değiştirir."),
        entry("Eğitim eğlence olmak zorunda mı?", [
            "Televizyon öğretimi çocuğa ön koşul, çaba ve devam gerektirmeyen ders sunabilir. Her bölüm kendi başına anlaşılır, kafa karışıklığı ve sınav yoktur.",
            "Gerçek öğrenme bazen sıkılma, tekrar ve yanlış yapma ister. Her dakika eğlence beklentisi zor konuyla kalma kasını zayıflatabilir.",
            "Görsel anlatım güçlü öğretim aracı olabilir; tehlike eğitim değerini yalnız izlenme zevkiyle ölçmektir.",
            "İyi ders merak uyandırır ama öğrenciyi yalnız müşteri memnuniyetine indirgemez.",
        ], "ÜÇÜNCÜ KISIM · EKRANDAN TELEFONA", art="learning-effort", caption="Görsel merak kapıyı açabilir, fakat öğrenme tekrar, hata ve zor soruyla kalma emeğini yine ister."),
        entry("Televizyon bizi aptal mı yapar?", [
            "Postman bireysel zekaya hakaret etmez. En zeki kişi bile ortamın hız, görüntü ve eğlence beklentisine göre konuşmak zorunda kalabilir.",
            "Bir profesörün beş saniyelik cevap vermesi istenirse konu basitleşir; sorun profesörün kapasitesi değil kabın hacmidir.",
            "İzleyici de ekran dışında uzun kitap okuyabilir. Araç tek başına kader değildir.",
            "Eleştiri toplumsal ölçektedir: Kamusal kurumlar aynı biçime uyduğunda hangi düşünceler sistemli olarak görünmez olur?",
        ], "ÜÇÜNCÜ KISIM · EKRANDAN TELEFONA", art="small-container", caption="Karmaşık düşünce küçük zaman kabına sıkıştırıldığında kayıp kişinin zekasından değil ortamın hacminden doğar."),
        entry("Telefon ekranında 'şimdi bunu'", [
            "Sosyal medya Postman'ın parçalı akışını kişiselleştirir. Savaş, kedi videosu, reklam ve arkadaş fotoğrafı aynı başparmak hareketinde birbirini izler.",
            "Televizyon programını yapımcı seçerken algoritma sizin durma ve öfkelenme davranışınızı ölçer. Eğlence artık geri bildirimli dikkat makinesidir.",
            "Kullanıcı yalnız pasif izleyici değildir; üretir, yorumlar ve örgütlenir. Bu yeni imkan Postman'ın tek yönlü ekran modelini aşar.",
            "Yine de biçim sorusu kalır: Hangi içerik paylaşılmaya, hangisi yavaşça unutulmaya daha yatkın?",
        ], "ÜÇÜNCÜ KISIM · EKRANDAN TELEFONA", art="infinite-scroll", caption="Sonsuz akış savaş, reklam ve eğlenceyi aynı başparmak hareketinde bağlamsız komşulara dönüştürür."),
        entry("Algoritma neyi ödüllendirir?", [
            "Platformun geliri ekranda geçirilen zamana bağlıysa sakin ve tamamlanmış bilgi yerine öfke, korku ve merak boşluğu avantaj kazanabilir.",
            "Pazarda en yüksek sesli satıcı sürekli öne alınırsa kaliteli ama sessiz ürün görünmez kalır. Algoritma kamusal meydanın yer dağıtıcısıdır.",
            "Bu dağıtım tarafsız matematik değildir; şirket amacı ve kullanıcı davranışı koda dönüşür.",
            "Medya okuryazarlığı yalnız yalanı tanımak değil görünürlüğün ekonomik teşvikini anlamaktır.",
        ], "ÜÇÜNCÜ KISIM · EKRANDAN TELEFONA", art="algorithm-market", caption="Dikkat pazarında algoritma en doğru sesi değil kullanıcıyı en uzun tutan sesi meydanın önüne çıkarabilir."),
        entry("Görüntü her zaman yüzeysel değildir", [
            "Belgesel, canlı tanıklık ve görsel açıklama yazının veremediği deneyim sunabilir. Ay'a iniş veya savaş görüntüsü ortak hafızayı değiştirmiştir.",
            "Sorun görüntünün varlığı değil, görüntünün kanıt ve bağlamın yerine geçirilmesidir. İyi görsel düşünceyi açar, kötü kullanım düşünceyi kapatır.",
            "Postman baskıya duyduğu sevgiyle televizyonun yaratıcı imkanlarını küçümseyebilir. Her araç içinde karşı biçimler üretilebilir.",
            "Eleştirel izleyici görüntüden kaçmaz; arkasındaki tarih, seçim ve montajı sorar.",
        ], "ÜÇÜNCÜ KISIM · EKRANDAN TELEFONA", art="deep-image", caption="Görüntü düşüncenin düşmanı değildir; bağlam ve kanıtla birleştiğinde görünmeyeni güçlü biçimde öğretebilir."),
        entry("Çözüm televizyonu kapatmak mı?", [
            "Postman kolay teknik çözüm sunmaz. Sorun tek cihaz değil toplumun hakikati eğlence ölçüsüyle değerlendirmesidir.",
            "Bir akşam ekranı kapatmak dikkati dinlendirir, fakat siyaset ve eğitimin gösteri düzenini değiştirmez. Kurumların biçim tasarımı gerekir.",
            "Uzun söyleşi, reklamsız kamusal yayın, şeffaf algoritma ve medya eğitimi araç içinde başka alışkanlıklar kurabilir.",
            "İlk adım ortamı görünür kılmaktır. Suyun içindeki balık gibi, medya biçimini fark etmeden seçtiğimizi sanırız.",
        ], "DÖRDÜNCÜ KISIM · DİKKATİ GERİ ALMAK", art="fish-sees-water", caption="Medya ortamını fark etmek, içinde yüzen balığın ilk kez suyu görmesi gibi seçim alanı açar."),
        entry("Haber diyeti değil haber mutfağı", [
            "Yalnız daha az haber tüketmek değil, haberin nasıl üretildiğini bilmek gerekir. Kaynak, bağlam, düzeltme ve çıkar zincirini görünür yapan yayın seçin.",
            "Atıştırmalık akış yerine belirli saatte birkaç uzun analiz okumak, parçaları aynı masada birleştirir.",
            "Her haber için 'Bu bilgiyle ne yapabilirim, hangi geçmişi bilmem gerekiyor?' sorusu bağlamı geri getirir.",
            "Amaç dünyadan kaçmak değil bilgi ile eylem arasında tekrar köprü kurmaktır.",
        ], "DÖRDÜNCÜ KISIM · DİKKATİ GERİ ALMAK", art="news-kitchen", caption="Haber atıştırmalık akış değil kaynak, tarih ve eylem bağıyla hazırlanan düşünce mutfağı olabilir."),
        entry("Ekran tasarımında sürtünme", [
            "Otomatik oynatma ve sonsuz kaydırma durmayı zorlaştırır. Bilinçli sürtünme, bölüm sonunda kapanma, bildirim sınırı ve okuma listesi seçimi geri verebilir.",
            "Markette kasaya şeker koymak davranışı yönlendirir; telefonda varsayılan ayar da öyledir. Kişisel irade tasarımdan bağımsız değildir.",
            "Kurumlar kullanıcıya zaman raporu, kronolojik akış ve veri seçeneği sunabilir. Tasarımın ahlaki sorumluluğu vardır.",
            "Dikkati korumak yalnız bireyin disiplin ödevi değil kamusal düzenleme sorusudur.",
        ], "DÖRDÜNCÜ KISIM · DİKKATİ GERİ ALMAK", art="designed-friction", caption="Otomatik akışa eklenen durma noktaları kullanıcıya dikkatin yönünü yeniden seçebileceği sürtünme verir."),
        entry("Postman'ın nostaljisi", [
            "Kitap basılı Amerika'yı akılcı tartışma çağı olarak idealize eder. Propaganda, sansasyon, dışlanmış gruplar ve düşük okuryazarlık bu resmi karmaşıklaştırır.",
            "Televizyon da ortak kültür, eğitim ve görünürlük sağlamıştır. Sorunları araç biçimi kadar sahiplik ve siyasi ekonomi üretir.",
            "Yine de nostalji eleştirisi temel soruyu ortadan kaldırmaz: Kamusal söylem hangi biçim altında hangi zihinsel alışkanlığı kazanıyor?",
        ], "SON DURAKLAR"),
        entry("Eğlence düşman değildir", [
            "İnsan oyun, mizah ve dinlenme olmadan yaşayamaz. Postman'ın hedefi eğlencenin varlığı değil her alanın tek ölçüsü haline gelmesidir.",
            "Bir bilim anlatısı keyifli olabilir; sorun, zor gerçek eğlenceli değil diye elendiğinde doğar.",
            "Sağlıklı medya diyeti hem neşe hem sabır taşır. Tatlı yasaklanmaz, bütün öğün olmaz.",
        ], "SON DURAKLAR"),
        entry("Yirmi dakikalık deney", [
            "Akışta yirmi dakika geçirdikten sonra gördüğünüz beş şeyi yazın. Hangisinin kaynağını, bağlamını ve sonucunu hatırlıyorsunuz?",
            "Sonra aynı sürede tek uzun metin okuyun ve üç bağlantı çıkarın. Hangi araç sizde nasıl bir düşünce izi bıraktı?",
            "Deney ekranı mahkum etmez; kendi dikkatinizin farklı kaplarda nasıl davrandığını görünür kılar.",
        ], "SON DURAKLAR"),
        entry("Bir cümlede kitabın özü", [
            "Özgür toplumda hakikat yalnız sansürle değil, her kamusal konunun hızlı, görüntülü ve eğlenceli olmak zorunda kaldığı bir ortamda ciddiyetini kaybederek de yok olabilir.",
            "Akılda kalacak görüntü haberden reklama geçiştir: Ekran bir saniyede unutur; yurttaşın görevi bağlamı ve ağırlığı yeniden kurmaktır.",
        ], "SON DURAKLAR"),
    ]))


BOOKS.append(base(211, "Fotoğraf Üzerine", "Susan Sontag",
    "Fotoğrafın yalnız dünyayı kaydetmediğini; sahiplenme, tüketme, güzelleştirme, şok etme ve hafıza kurma biçimimizi değiştirdiğini altı keskin denemeyle gösteren klasiği telefon kamerası çağında yeniden açan rehber.",
    "#66556B", "On Photography", "fotograf-uzerine",
    [
        {"id": 1, "title": "Macmillan - On Photography resmi sayfası", "url": "https://us.macmillan.com/books/9780374622442/onphotography/"},
        {"id": 2, "title": "Penguin - On Photography örnek metin", "url": "https://www.penguin.co.uk/books/57568/on-photography-by-sontag-susan/9780140053975"},
        {"id": 3, "title": "The New York Review of Books - Sontag fotoğraf denemeleri arşivi", "url": "https://www.nybooks.com/contributors/susan-sontag/"},
        {"id": 4, "title": "Library of Congress - Fotoğraf koleksiyonları ve bağlam", "url": "https://www.loc.gov/pictures/"},
    ], [
        entry("Bu kitap nasıl okunmalı?", [
            "Fotoğraf Üzerine altı denemeden oluşur; tek çizgili teori değil birbiriyle gerilim taşıyan gözlemler sunar. Sontag bazen aynı anda fotoğrafın hem bilgi hem körleşme yarattığını söyler.",
            "Kitap 1970'lerin basılı fotoğraf dünyasında yazıldı. Telefon, sosyal medya ve yapay görüntüler yoktur, fakat sahiplenme ve görüntü bolluğu eleştirisi şaşırtıcı biçimde günceldir.",
            "Rehber fotoğrafı suç aleti yapmayacak; Sontag'ın sonraki Başkalarının Acısına Bakmak kitabında düzelttiği noktaları da anacak.",
        ], "BAŞLANGIÇ"),
        entry("Platon'un mağarasındaki turistler", [
            "Sontag kitabı insanların dünyayı görüntü gölgeleri üzerinden tanıdığı Platon mağarasıyla açar. Fotoğraf bize gerçekliğin parçasını verir, fakat parçayı bütün sanabiliriz.",
            "Tatil yerinde manzaraya bakmadan önce telefonu kaldırdığınızda deneyim, kanıt üretme görevine dönüşür. Oradaydım demek için görüntü gerekir.",
            "Fotoğraf çekmek görmenin tarafsız devamı değildir. Çerçeve seçer, zamanı keser ve dışarıda kalanları susturur.",
            "Mağaradan çıkmak fotoğrafı bırakmak değil görüntünün seçilmiş gölge olduğunu hatırlamaktır.",
        ], "BİRİNCİ KISIM · KAMERA İLE SAHİPLENMEK", art="camera-cave", caption="Fotoğraf gerçek dünyadan iz taşır, fakat seçilmiş çerçeveyi bütün gerçeklik sanarsak mağaranın gölgesinde kalırız."),
        entry("Fotoğraf çekmek sahip olmaktır", [
            "Sontag'a göre fotoğraf çekmek nesneyi görüntü olarak edinmektir. İnsan, yer veya olay koleksiyona katılır ve daha sonra bakılabilir hale gelir.",
            "Müzede tabloyu görmek yerine fotoğrafını almak, deneyimi cebinize koyduğunuz hissini verir. Sahiplik fiziksel değil simgeseldir.",
            "Kamera dünyaya yaklaşma ve araya mesafe koyma işini aynı anda yapar. Fotoğrafçı olayın içindedir, fakat lensin arkasında korunur.",
            "Bu güç rıza sorusunu doğurur. Görüntüsünü almak, kişinin hikayesini kullanma hakkını otomatik vermez.",
        ], "BİRİNCİ KISIM · KAMERA İLE SAHİPLENMEK", art="image-collection", caption="Kamera insanı veya yeri taşımadan görüntüsünü koleksiyona ekleyerek simgesel sahiplik hissi yaratır."),
        entry("Turistin çalışma programı", [
            "Modern turist yabancı yerde ne yapacağını fotoğraf çekerek bilir. Kamera kaygıyı düzenler; boş boş bakmak yerine görev verir.",
            "Günde yüz fotoğrafla geziyi tamamlamak, fabrikada üretim kotası gibi olabilir. Deneyim yaşanırken gelecekteki albüm için çalışılır.",
            "Fotoğraf aynı zamanda paylaşılabilir hafıza ve aile bağı kurar. Sontag'ın eleştirisi bu yararı silmez, çekme zorunluluğunu görünür kılar.",
            "Bazen tek kareden sonra telefonu indirip sahnenin sesini ve kokusunu kayıtsız bırakmak deneyimi geri getirir.",
        ], "BİRİNCİ KISIM · KAMERA İLE SAHİPLENMEK", art="tourist-quota", caption="Turist fotoğraf kotasını tamamlarken şimdiki geziyi gelecekteki albüm için bir üretim işine çevirebilir."),
        entry("Aile albümü neyi kanıtlar?", [
            "Aile fotoğrafları birlik, büyüme ve önemli günlerin görünür tarihini kurar. Kavgalar, sıradan günler ve fotoğraf çekilmeyen kişiler çoğu zaman dışarıda kalır.",
            "Albüm yalan değildir; seçilmiş hafızadır. Doğum günü mumları aileyi temsil ederken masadan erken kalkanın öfkesi kaybolabilir.",
            "Fotoğraf geçmişi korur, aynı zamanda hangi geçmişin hatırlanacağını biçimlendirir. Tekrar baktıkça görüntü olayın kendisinin yerine geçebilir.",
            "Soru 'fotoğraf doğru mu?' kadar 'bu doğru parçayı kim, neden sakladı?' olmalıdır.",
        ], "BİRİNCİ KISIM · KAMERA İLE SAHİPLENMEK", art="family-album", caption="Aile albümü gerçek anları saklar, fakat seçtiği gülümsemelerle hangi geçmişin hatırlanacağını da kurar."),
        entry("Amerika'yı fotoğrafla toplamak", [
            "Sontag Walt Whitman'ın her şeyi kucaklayan Amerika hayali ile fotoğrafçıların ülkeyi tipler ve görüntüler halinde toplamasını ilişkilendirir.",
            "Kamera sıradan tabela, işçi, ev ve yol kenarını estetik değere yükseltebilir. Her şey fotoğraflanmaya değer hale gelir.",
            "Bu demokratik bakış aynı zamanda insanları örnek ve tipe indirgeyebilir. Çeşitlilik koleksiyoncunun vitrini olur.",
            "Fotoğrafın eşitleyici çerçevesi sınıf ve güç farkını hem görünür hem estetik olarak zararsız gösterebilir.",
        ], "İKİNCİ KISIM · ESTETİK VE GÜÇ", art="american-catalog", caption="Kamera sıradan Amerika'yı görünür kılarken insan ve yerleri koleksiyoncunun estetik kataloğuna da dönüştürebilir."),
        entry("Diane Arbus ve tuhaflığın vitrini", [
            "Arbus toplumun kenarında görülen insanları doğrudan kameraya baktırır. Sontag bu fotoğrafların izleyicide merhametten çok soğuk merak üretebileceğini savunur.",
            "Kişi kendi hayatının öznesiyken fotoğrafta 'tuhaf insan' örneğine dönüşebilir. İzleyici güvenli mesafeden farklılığı tüketir.",
            "Eleştirmenler Sontag'ın da fotoğraflanan kişileri tek kurban rolüne hapsettiğini söyler. Bazı portrelerde öznenin işbirliği ve gücü vardır.",
            "Tartışma önemli soruyu açar: Görünür kılmak saygı mı, teşhir mi ve buna kim karar verir?",
        ], "İKİNCİ KISIM · ESTETİK VE GÜÇ", art="portrait-gaze", caption="Doğrudan bakan portre görünürlük ile teşhir arasındaki gücü fotoğrafçı, özne ve izleyici arasında paylaştırır."),
        entry("Güzellik her şeyi yutabilir", [
            "Fotoğraf yıkıntı, yoksulluk veya savaş sahnesini biçim, ışık ve kompozisyonla güzel gösterebilir. Estetik dikkat gerçeğe bakmayı sağlar, ama acıyı dekor haline getirebilir.",
            "Paslı fabrika fotoğrafı duvarda şık görünürken orada işini kaybedenlerin hikayesi silinebilir. Nesnenin yarası tasarım yüzeyine dönüşür.",
            "Çirkin olanı fotoğraflamak otomatik sömürü değildir. Bağlam, niyet ve kullanım sonucu değiştirir.",
            "Sontag kameranın her şeyi görsel olarak eşdeğer ve tüketilebilir kılma eğilimine dikkat çeker.",
        ], "İKİNCİ KISIM · ESTETİK VE GÜÇ", art="beautiful-ruin", caption="Güzel kompozisyon yıkıma bakmayı kolaylaştırırken yaşanan zararı duvar süsüne dönüştürme riski taşır."),
        entry("Fotoğraf saldırı mıdır?", [
            "Kamera İngilizcede vurmak, yakalamak ve çekmek gibi saldırgan fiillerle anlatılır. Fotoğrafçı başkasının anını keser ve onu çoğaltılabilir nesneye dönüştürür.",
            "Sokakta ağlayan çocuğu izin almadan çekmek fiziksel zarar vermeyebilir, fakat mahremiyet ve hikaye sahipliğini ihlal edebilir.",
            "Her fotoğraf şiddet değildir. Rıza, ilişki ve ortak amaç kamerayı işbirliği aracına çevirebilir.",
            "Sontag'ın sert dili görünmez güç farkını hissedilir yapar: Kim bakıyor, kim bakılan ve kim görüntüyü dağıtıyor?",
        ], "İKİNCİ KISIM · ESTETİK VE GÜÇ", art="camera-power", caption="Deklanşör yalnız görüntü almaz; kimin bakma ve başkasının anını dağıtma gücüne sahip olduğunu da gösterir."),
        entry("Acı görüntüsü bizi harekete geçirir mi?", [
            "Savaş ve açlık fotoğrafı uzaktaki acıyı görünür kılabilir. Fakat izleyici ne olduğunu ve ne yapabileceğini bilmiyorsa şok kısa duyguda kalır.",
            "Her gün yeni felaket görüntüsü görmek duyarlılığı artırmak yerine uyuşturabilir. Dün sarsan kare bugün akışta bir saniye sürer.",
            "Sontag daha sonra fotoğrafların mutlaka duyarsızlaştırdığı fikrini yumuşatır. Etki sabit değildir; başlık, tarih, tekrar ve izleyicinin konumu belirleyicidir.",
            "Görüntü vicdanın yerine geçmez, onu bilgi ve eyleme çağıran kapı olabilir.",
        ], "ÜÇÜNCÜ KISIM · ACI VE BİLGİ", art="suffering-image", caption="Acı fotoğrafı vicdanın kapısını açabilir; bağlam ve eylem yolu yoksa şok kısa süre sonra akışta kaybolur."),
        entry("Şokun azalan dozu", [
            "İlk kez görülen sert görüntü alışılmış sınırı kırar. Benzeri çoğaldıkça etki azalır ve daha çarpıcı kare aranır. Görüntü ekonomisi doz yükseltir.",
            "Korku filmlerinde aynı sahnenin giderek daha sertleşmesi gibi haber ve reklam da dikkati tutmak için şoku büyütebilir.",
            "Bu süreç gerçek acıyı rekabet malzemesine çevirir. En fotojenik felaket görünür, yavaş ve görüntüsüz zarar unutulur.",
            "Duyarlılığı korumak için görüntüyü sayı, tanıklık ve süreklilikle bağlamak gerekir.",
        ], "ÜÇÜNCÜ KISIM · ACI VE BİLGİ", art="shock-escalator", caption="Dikkat için yarışan görüntüler şok dozunu yükseltirken yavaş ve fotojenik olmayan acıları görünmez bırakabilir."),
        entry("Fotoğraf kanıt mıdır?", [
            "Fotoğraf gerçekten bir anda kameranın önünde olan ışıktan iz taşır. Bu yüzden mahkeme, bilim ve haberde güçlü kanıt duygusu verir.",
            "Fakat açı, zaman, kırpma ve başlık anlamı değiştirir. Boş görünen meydanın beş dakika önce kalabalık olup olmadığını kare söylemez.",
            "Dijital düzenleme ve yapay görüntüler iz ile gerçeklik bağını daha da zorlar. Kaynak zinciri görüntünün parçası olmalıdır.",
            "Doğru soru 'fotoğraf yalan mı?' değil, 'bu kare hangi iddiayı gerçekten destekliyor ve neyi göstermiyor?' sorusudur.",
        ], "ÜÇÜNCÜ KISIM · ACI VE BİLGİ", art="cropped-evidence", caption="Fotoğraf gerçek bir anın izini taşısa da kırpma ve zaman seçimi kanıtın ne söylediğini belirler."),
        entry("Başlık görüntüyü yönetir", [
            "Aynı kalabalık fotoğrafı 'özgürlük yürüyüşü' veya 'düzensiz gösteri' başlığıyla başka anlam kazanır. Görüntü sözcüksüz olsa da yorumsuz değildir.",
            "Başlık kişileri adlandırır, yeri ve zamanı verir ya da saklar. İzleyicinin bakış yolunu çizer.",
            "Yanlış başlık doğru fotoğrafı yanlış bilgiye çevirebilir. Tersine ayrıntılı bağlam görüntünün tanıklık gücünü artırır.",
            "Fotoğraf okuryazarlığı kareye değil, çevresindeki metin ve dağıtım ağına da bakar.",
        ], "ÜÇÜNCÜ KISIM · ACI VE BİLGİ", art="two-captions", caption="Aynı kalabalık karesi farklı başlıklarla başka siyasi olay gibi okunabilir; sözcük bakışın rotasını çizer."),
        entry("Fotoğraf koleksiyonculuğu", [
            "Dünya fotoğraflanabilir parçalar toplamına dönüştüğünde arşiv sahiplik ve bilgi gücü verir. Polis, devlet, aile ve şirket farklı amaçlarla yüzleri sınıflandırır.",
            "Albüm sevgi hafızası, kimlik fotoğrafı erişim anahtarı, gözetim kamerası davranış kaydıdır. Aynı teknoloji farklı kurumda başka güç taşır.",
            "Sontag koleksiyonun gerçeği düzenlediğini vurgular. Neyin saklandığı kadar neyin silindiği önemlidir.",
            "Bugün bulut arşivi yüzleri otomatik tanıyabilir; koleksiyon artık yalnız bakmaz, karar da etkileyebilir.",
        ], "DÖRDÜNCÜ KISIM · TELEFON ÇAĞI", art="photo-archive", caption="Fotoğraf arşivi hatıra saklarken insanları sınıflandıran ve erişimi belirleyen kurumsal güce de dönüşebilir."),
        entry("Her an paylaşılabilir olduğunda", [
            "Telefon kamerası çekim ile dağıtım arasındaki süreyi yok etti. Yemek, yüz ve kaza saniyeler içinde görünür olur.",
            "Deneyim sırasında görünmez izleyici düşünülür: Bu kare nasıl karşılanacak? Kişi hayatını yaşarken aynı anda kendi basın danışmanı olur.",
            "Paylaşım dayanışma ve tanıklık sağlayabilir. Polis şiddeti gibi olaylar yurttaş kamerasıyla belgelenir.",
            "Aynı hız doğrulama, rıza ve yas için zaman bırakmaz. Teknik imkan ahlaki kararın yerine geçmez.",
        ], "DÖRDÜNCÜ KISIM · TELEFON ÇAĞI", art="instant-share", caption="Telefon çekim ile yayını birleştirince kişi anı yaşarken aynı anda görünmez izleyici için onu paketler."),
        entry("Selfie: Öznenin kamerayı tutması", [
            "Selfie, Sontag'ın fotoğrafçı ile nesne ayrımını değiştirir. Kişi kendi görüntüsünü seçer, düzeltir ve dağıtır; temsil üzerinde güç kazanır.",
            "Fakat platformun güzellik ölçüleri ve beğeni sayısı yeni baskı kurabilir. Kendi kameranızı tutarken başkasının bakışını içselleştirebilirsiniz.",
            "Selfie yalnız narsisizm değildir. Kimlik deneyi, topluluğa katılım ve uzaktaki yakına selam olabilir.",
            "Soru görüntünün kendisi değil, hangi beklenti ve ekonomi içinde üretildiğidir.",
        ], "DÖRDÜNCÜ KISIM · TELEFON ÇAĞI", art="selfie-mirror", caption="Selfie temsil gücünü özneye verirken platformun görünmez aynasını ve beğeni ölçüsünü de kadraja sokar."),
        entry("Yapay görüntü ve gerçeklik", [
            "Üretken yapay zeka kameranın önünde hiç bulunmamış sahneler yaratabilir. Fotoğraf görünümünün otomatik kanıt değeri daha da zayıflar.",
            "Bir yangın görüntüsü estetik olarak kusursuzken olay hiç yaşanmamış olabilir. Gözün ikna olması kaynak doğrulamasını gereksiz kılmaz.",
            "Yapay görüntü sanat ve tasarımda yeni imkanlar açar; sorun kurgu olduğu saklanıp haber kanıtı gibi kullanıldığında doğar.",
            "Sontag'ın 'görüntü dünyayı tüketir' uyarısı artık gerçekliğe benzer sonsuz sahne üretimine uzanır.",
        ], "DÖRDÜNCÜ KISIM · TELEFON ÇAĞI", art="synthetic-photo", caption="Kamera izi olmadan üretilen gerçekçi sahne, görüntü ile olay arasındaki eski güven bağını yeniden sınamayı gerektirir."),
        entry("Sontag'ın sonraki düzeltmesi", [
            "Sontag daha sonraki Başkalarının Acısına Bakmak kitabında fotoğrafların bizi kaçınılmaz olarak uyuşturduğu genellemesini sorgular. Görüntünün etkisi bağlama ve izleyiciye göre değişir.",
            "Bir kare yıllarca adalet mücadelesinin simgesi olabilir; başka kare hızla unutulur. Tek medya yasası yoktur.",
            "Düşünürün kendi önceki kesinliğini düzeltmesi Fotoğraf Üzerine'yi değersizleştirmez; okura eleştirinin de tarih içinde değiştiğini gösterir.",
        ], "SON DURAKLAR"),
        entry("Fotoğrafçının sorumluluğu", [
            "Çekmeden önce rıza, güç farkı ve olası zararı düşünün. Çocuk, hasta, yas ve şiddet sahnesinde görüntünün dolaşımı kişiyi yıllarca takip edebilir.",
            "Çektikten sonra başlık, kırpma ve arşiv güvenliği de ahlaki karardır. Doğru kare yanlış bağlamda zarar verebilir.",
            "Bazen kamerayı kaldırmak tanıklık, bazen indirmek saygıdır. Tek otomatik kural yerine ilişkiyi görmek gerekir.",
        ], "SON DURAKLAR"),
        entry("Dört karelik okuma", [
            "Bir haber fotoğrafı seçin. Kadrajın dışında ne olabilir, fotoğrafı kim çekti, başlığı kim yazdı ve görüntüden kim yarar sağlıyor?",
            "Sonra aynı olayın başka açılarını arayın. Tek karede kurduğunuz hikaye değişiyor mu?",
            "Bu alıştırma görüntüye güvensizlik değil daha dikkatli güven kazandırır.",
        ], "SON DURAKLAR"),
        entry("Bir cümlede kitabın özü", [
            "Fotoğraf dünyadan gerçek bir parça taşırken onu seçer, sahiplenir ve tüketilebilir görüntüye çevirir; bu yüzden her kare hem tanıklık hem güç ilişkisidir.",
            "Akılda kalacak görüntü kadrajdır: İçerideki gerçek kadar dışarıda bırakılan sessizlik de fotoğrafın anlamına aittir.",
        ], "SON DURAKLAR"),
    ]))


if __name__ == "__main__":
    write_books(BOOKS)
