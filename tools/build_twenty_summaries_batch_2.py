#!/usr/bin/env python3
"""Build summaries six through ten in the twenty-book collection."""

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


BOOKS.append(base(70, "Tao Te Ching", "Laozi",
    "Zorlayarak yönetmek yerine su gibi yol bulmayı, doluluğun yanında boşluğun değerini ve gösterişli güç yerine sessiz etkiyi anlatan 81 kısa şiirin çelişkili görünen bilgeliğini gündelik hayata açan rehber.",
    "#4D7068", "Daodejing", "tao-te-ching",
    [
        {"id": 1, "title": "Stanford Encyclopedia of Philosophy - Laozi", "url": "https://plato.stanford.edu/entries/laozi/"},
        {"id": 2, "title": "Chinese Text Project - Dao De Jing", "url": "https://ctext.org/dao-de-jing"},
        {"id": 3, "title": "Stanford Encyclopedia of Philosophy - Çin metafiziği", "url": "https://plato.stanford.edu/entries/chinese-metaphysics/"},
        {"id": 4, "title": "Internet Encyclopedia of Philosophy - Daoism", "url": "https://iep.utm.edu/daoism/"},
    ], [
        entry("Bu kitap nasıl okunmalı?", [
            "Tao Te Ching bir kullanım kılavuzu gibi tek anlam vermez. Kısa şiirler, paradokslar ve görüntüler okuru yavaşlatır. Aynı satır yönetim, kişisel tutum veya doğa hakkında farklı yorumlara açılabilir.",
            "Laozi'nin tek tarihsel kişi olup olmadığı ve metnin nasıl derlendiği tartışmalıdır. Rehber efsane ile tarihsel kesinliği ayıracak, metni ortak bir erken Çin düşüncesi ürünü olarak ele alacak.",
            "Çince kavramların Türkçede tek karşılığı yoktur. Dao yol ve işleyiş, de etkili erdem, wuwei ise pasiflikten çok zorlamasız eylem olarak açıklanacak.",
        ], "BAŞLANGIÇ"),
        entry("Adı söylenen yol, yolun tamamı değildir", [
            "Kitap daha ilk satırda söylediği şeyin sözcüklere tam sığmayacağını bildirir. Bir dağın haritası yürüyüş için gereklidir, fakat rüzgarı, yokuşu ve ayaktaki ağrıyı taşımaz.",
            "Ad koymak dünyayı düzenler: Ağaç, iyi, başarılı, düşman. Ama etiket nesnenin bütün değişimini dondurur. Çocuk bugün utangaç diye hayat boyu aynı kutuda kalmaz.",
            "Laozi dili çöpe atmaz; zaten kitap yazar. Bizi işaret ile gerçekliği karıştırmamaya çağırır. Sözcük parmağıdır, ay değildir.",
            "Bu başlangıç kesinlik gösterisini kırar. Bir fikri adlandırınca ona sahip olduğumuzu sanmak yerine, deneyimin geri kalanına açık kalırız.",
        ], "BİRİNCİ KISIM · YOLU GÖRMEK", art="map-and-mountain", caption="Harita yürüyüşü yönlendirir ama dağın tamamı değildir; ad da gerçekliği işaret eder, tüketmez."),
        entry("Karşıtlar birbirini doğurur", [
            "Güzel dediğimiz anda çirkin, uzun dediğimiz anda kısa belirir. Kavramlar tek başına değil ilişkide anlam kazanır. Cetvel olmadan uzunluk yoktur.",
            "Sessiz bir oda, az önceki gürültü sayesinde daha sessiz hissedilir. Başarı da başarısızlık ihtimaliyle belirginleşir. Bir kutbu yok ederek diğerini saf halde tutamayız.",
            "Bu, her şeyin aynı olduğu anlamına gelmez. Acı ile sevinç farklıdır; fakat deneyimde birbirini tanımamıza ve dönüştürmemize yardım eder.",
            "Laozi'nin bakışı aşırı yargıyı yumuşatır. Bugünün kaybı yarının yönünü, bugünün zaferi yarının kibrini doğurabilir; hikaye tek kare değildir.",
        ], "BİRİNCİ KISIM · YOLU GÖRMEK", art="opposite-hills", caption="Uzun ile kısa, ses ile sessizlik tek başına değil birbirini görünür kılan ilişkiler içinde anlam kazanır."),
        entry("Su neden bilgedir?", [
            "Su herkesin kaçındığı alçak yerlere gider, sert kayayı zamanla aşındırır ve girdiği kabın biçimini alır. Laozi bu yüzden en yüksek iyiliği suya benzetir.",
            "Esneklik omurgasızlık değildir. Nehir engelle karşılaşınca kimliğini bırakmaz; yön değiştirip akmaya devam eder. Hedef ile yöntem arasındaki farkı bilir.",
            "İşyerinde tek cümleyi kabul ettirmek için toplantıyı kilitlemek yerine asıl ihtiyacı koruyup başka yol bulmak su gibi davranmaktır.",
            "Su görüntüsü gücü yeniden tanımlar. Gürültülü çarpma yerine süreklilik, yüksek mevki yerine yarar ve sertlik yerine uyum öne çıkar.",
        ], "BİRİNCİ KISIM · YOLU GÖRMEK", art="water-and-rock", caption="Su biçimini değiştirerek özünü kaybetmez; sert kayayı zorla değil yön, süre ve devamlılıkla aşar."),
        entry("Boşluğun işe yaradığı yer", [
            "Tekerleğin göbeğindeki boşluk olmasa mil dönmez. Testinin içi dolu kil değil boş hacim olduğu için su taşır. Odanın yararı duvar kadar kapı ve iç açıklıktadır.",
            "Takvimde hiç boşluk bırakmayan kişi her saati doldurur ama yeni olaya yanıt veremez. Sessizlik konuşmanın, mola çalışmanın ve bekleme kararın kullanılabilir alanıdır.",
            "Batı dillerinde boşluk eksiklik gibi duyulabilir. Laozi boşluğu üretken imkan olarak gösterir; kullanılmayan alan işlevin koşuludur.",
            "Soru şudur: Hayatınızda neyi eklemek değil, neyi boş bırakmak bütünü çalıştırır?",
        ], "BİRİNCİ KISIM · YOLU GÖRMEK", art="useful-emptiness", caption="Testiyi işe yaratan yalnız kil değil, suyu kabul eden iç boşluktur; hayat da açıklıkla nefes alır."),
        entry("Wuwei: Hiçbir şey yapmamak değil", [
            "Wuwei çoğu zaman eylemsizlik diye çevrilir, fakat metindeki anlamı zorlayıcı, yapay ve aşırı müdahaleci eylemden kaçınmaya daha yakındır. Usta hareket eder ama hareketi sürtünme üretmez.",
            "Bisiklete yeni binen gidonu her saniye sertçe düzeltir ve yalpalar. Deneyimli sürücü küçük ayarlamalarla dengeyi takip eder. Daha az zorlama, daha iyi sonuç verir.",
            "Bahçıvan bitkiyi çekerek büyütemez; toprağı, suyu ve ışığı düzenler. Wuwei koşulları kurup sürecin kendi gücüne alan açmaktır.",
            "Pasiflik haksızlık karşısında susmak olabilir; bu otomatik olarak Dao değildir. Ölçü, eylemin yaşamın akışını anlayıp anlamadığıdır.",
        ], "İKİNCİ KISIM · ZORLAMASIZ EYLEM", art="balanced-bicycle", caption="Usta bisikletçi dengeyi sert komutlarla değil, hareketin akışını hisseden küçük ayarlamalarla korur."),
        entry("Çamurlu su nasıl durulur?", [
            "Laozi çamurlu suyun bekleyince kendiliğinden berraklaşmasını sorar. Her karışıklık daha fazla karıştırılarak çözülmez. Bazı cevaplar acele durduğunda görünür.",
            "Öfkeli mesajı gece yazıp sabah göndermemek basit bir örnektir. Sorun kaçılmamıştır; duygunun çamuru çökerken asıl ihtiyaç belirginleşir.",
            "Beklemek sonsuz erteleme değildir. Acil durumda hareket gerekir. Fakat sırf kaygıyı azaltmak için verilen hızlı karar daha büyük düğüm oluşturabilir.",
            "Metin sabrı boş zaman değil, algının temizlenme süresi olarak görür.",
        ], "İKİNCİ KISIM · ZORLAMASIZ EYLEM", art="settling-water", caption="Çamurlu suyu daha çok karıştırmak yerine bir süre bırakmak, zaten içindeki berraklığı ortaya çıkarabilir."),
        entry("Yumuşak serti yenebilir", [
            "Dil dişten yumuşaktır ama dişler dökülürken dil kalır. Filiz beton çatlağında yol bulur. Laozi dayanıklılığı katılıkta değil uyum yeteneğinde görür.",
            "Her tartışmada son sözü söylemek kısa vadede güç hissi verir, uzun vadede ilişkiyi kırılganlaştırır. Dinlemek bazen daha etkili yön değiştirme aracıdır.",
            "Yumuşaklık sınırsız taviz değildir. Bambu eğilir ama kökünden vazgeçmez. Sınır, bağırmadan da sınırdır.",
            "Krizde katı planı korumak yerine amacı koruyup yöntemi değiştiren ekip bu paradoksu yaşar: Esneyen sistem ayakta kalır.",
        ], "İKİNCİ KISIM · ZORLAMASIZ EYLEM", art="bamboo-wind", caption="Bambu rüzgarda eğildiği için ayakta kalır; esneklik köksüzlük değil kırılmadan yön değiştirme gücüdür."),
        entry("Az konuşan lider", [
            "Laozi'nin ideal yöneticisi her başarıda kendi adını bağırmaz. Koşulları öyle kurar ki iş tamamlandığında insanlar 'biz yaptık' diyebilir.",
            "İyi orkestra şefi tek başına bütün sesi üretmez. Zamanı ve ortaklığı düzenler, sonra müzisyenlerin becerisi duyulur.",
            "Bu görüş liderliği görünür kahramanlıktan sistem kurmaya çevirir. Güven, açık sınır ve doğru kaynak, sürekli emirden daha kalıcı olabilir.",
            "Yine de sessiz lider hesap vermekten kaçmamalıdır. Görünmez etki, görünmez sorumluluk demek değildir.",
        ], "İKİNCİ KISIM · ZORLAMASIZ EYLEM", art="quiet-conductor", caption="İyi lider bütün sesi kendisi çıkarmaz; ortak ritmi kurar ve başarıyı ekibin sahiplenmesine izin verir."),
        entry("Çok yasa neden çok hile doğurabilir?", [
            "Metin, yönetim ne kadar ince ayrıntıya karışırsa insanların o kadar kurnazlaştığını söyler. Her davranışı kural altına almak güven değil kural çevresinde oyun üretebilir.",
            "Bir işyerinde performans tek sayıyla ölçülürse çalışanlar gerçek hizmet yerine sayıyı yükseltmeyi öğrenir. Ölçü hedefe dönüştüğünde hedef bozulur.",
            "Laozi'nin küçük yönetim ideali tarihsel bağlam taşır ve modern büyük toplumlara aynen aktarılamaz. Sağlık, çevre ve haklar için ayrıntılı kurumlar gerekebilir.",
            "Kalıcı soru yine değerlidir: Kural gerçek amacı mı koruyor, yoksa insanları yalnız görünüşü düzeltmeye mi itiyor?",
        ], "ÜÇÜNCÜ KISIM · YÖNETİM VE ARZU", art="rule-maze", caption="Kural çoğaldıkça insanlar amacı gerçekleştirmek yerine ölçünün çevresinde yeni yollar ve hileler bulabilir."),
        entry("Dolu kaseyi taşırmamak", [
            "Kase ağzına kadar dolduğunda yeni şey kabul etmez ve kolayca taşar. Laozi başarıdan sonra durmayı, keskin bıçağı sürekli bilememeyi öğütler.",
            "İş büyürken her fırsata evet demek kazanç gibi görünür; bir noktadan sonra kalite, uyku ve ilişki dökülür. Daha fazlası daha iyi olma sınırını geçmiştir.",
            "Tam zamanında geri çekilmek yenilgi değildir. Ürünü teslim etmek, konuşmayı bitirmek ve yeter demek tamamlamanın parçasıdır.",
            "Metin arzunun kendi kendini büyüten yapısını fark eder. Sınır dışarıdan ceza değil, kabın biçimini koruyan bilgeliktir.",
        ], "ÜÇÜNCÜ KISIM · YÖNETİM VE ARZU", art="overflowing-bowl", caption="Ağzına kadar dolu kase yeni şeyi kabul etmez; zamanında durmak emeği taşmaktan korur."),
        entry("Büyük ülkeyi küçük balık gibi pişirmek", [
            "Laozi büyük ülkeyi küçük balık gibi yönetmeyi söyler: Çok çevirirseniz dağılır. Sürekli reform ve müdahale toplumun dokusunu bozabilir.",
            "Yeni yönetici her hafta ekip düzenini değiştirirse kimse işine yerleşemez. İyi niyetli hareket bile istikrar maliyeti yaratır.",
            "Bu benzetme değişime karşı donukluk değildir. Balığı hiç pişirmemek de çözüm olmaz. Müdahalenin sıklığı, dozu ve yan etkisi düşünülmelidir.",
            "Modern yönetimde pilot uygulama, geri bildirim ve aşamalı değişim bu eski sezginin kurumsal karşılığı olabilir.",
        ], "ÜÇÜNCÜ KISIM · YÖNETİM VE ARZU", art="small-fish", caption="Küçük balığı sürekli çevirmek onu dağıtır; büyük sistemi de her an yeniden kurmak dokusunu bozabilir."),
        entry("Silahın zaferi yasla karşılanır", [
            "Metin savaşı gösterişli kahramanlık olarak sunmaz. Silah uğursuz araçtır; zorunlu zafer bile cenaze ciddiyetiyle karşılanmalıdır.",
            "Bir çatışmayı kazanıp insanların ölümünü kutlamak, başarı ölçüsünü insan hayatından koparır. Laozi kazananın kibrini yasla sınırlar.",
            "Bu yaklaşım pasifist yorumlara açıktır, fakat metin tarihsel olarak yöneticilere de seslenir. Savunma gerekse bile savaşın ahlaki maliyeti silinmez.",
            "Bugün de 'temiz operasyon' dili ekran görüntüsünün arkasındaki bedenleri unutabilir. Metin zaferin fiyatını görünür tutar.",
        ], "ÜÇÜNCÜ KISIM · YÖNETİM VE ARZU", art="victory-mourning", caption="Laozi için zorunlu savaşta bile zafer şenliği değil, kaybedilen hayatların ağırlığını taşıyan yas gerekir."),
        entry("Az arzu, daha geniş dikkat", [
            "Sürekli parlak nesne peşinde koşmak duyuları köreltir der Laozi. Çok renk gözü, çok ses kulağı ve hızlı av zihni yorar.",
            "Telefon bildirimleri her dakika küçük ödül sunar. Dikkat bir pazarda parçalara bölünürken önünüzdeki insanın yüzü görünmez hale gelir.",
            "Arzuyu tümden yok etmek gerçekçi değildir. Metin ihtiyacın üstüne eklenen gösteriş ve kıyas zincirini azaltmayı önerir.",
            "Azlık yoksunluk değil seçilmiş açıklık olabilir. Daha az seçenek, sahip olunanın tadını geri getirebilir.",
        ], "DÖRDÜNCÜ KISIM · GÜNDELİK DAO", art="quiet-attention", caption="Parlak uyaranların pazarı sakinleştiğinde dikkat önündeki insanı ve anın gerçek ihtiyacını yeniden görebilir."),
        entry("Bilmeyen bildiğini sanmasın", [
            "Gerçek bilgi kendi sınırını fark eder. Bilmeyip bildiğini sanmak hastalık, bilmediğini bilmek ise iyileşmenin başlangıcıdır.",
            "Doktorun emin olmadığı tanıyı söylemesi güveni azaltmaz; doğru testin kapısını açar. Sahte kesinlik kısa süreli rahatlık, uzun süreli hata üretir.",
            "Laozi'nin bilgesi kendini sergilemez. Bu, uzmanlığı küçümsemek değil uzmanlığın bilinmeyenle çevrili olduğunu unutmamaktır.",
            "Gündelik cümle güçlüdür: 'Şu kısmı biliyorum, buradan sonrasını tahmin ediyorum.' Bilginin sınırı görünür olunca konuşma dürüstleşir.",
        ], "DÖRDÜNCÜ KISIM · GÜNDELİK DAO", art="edge-of-knowledge", caption="Bilginin nerede bittiğini söylemek zayıflık değil, yanlış kesinliğin önünü kesen dürüst bir sınırdır."),
        entry("Kendini bilmek, başkasını yenmek", [
            "Başkalarını bilmek zeka, kendini bilmek aydınlanmadır; başkasını yenmek güç, kendini aşmak kudrettir der metin.",
            "Tartışmada rakibin zayıf noktasını bulmak kolay olabilir. Kendi öfkenizin hangi korkuyu koruduğunu görmek daha zor ve daha dönüştürücüdür.",
            "Kendini yenmek kendine savaş açmak değildir. Alışkanlığın otomatik yolunu fark edip daha uygun hareket seçmektir.",
            "Dış zafer başkasının davranışına bağlıdır; iç çalışma her gün küçük ölçekte mümkündür.",
        ], "DÖRDÜNCÜ KISIM · GÜNDELİK DAO", art="inner-mirror", caption="Rakibi görmek zekayı, kendi öfkesinin arkasındaki korkuyu görmek daha derin bir açıklığı gerektirir."),
        entry("Bin kilometrelik yol", [
            "Uzun yol ayağın altındaki tek adımla başlar. Dev hedef zihni dondururken küçük hareket süreci gerçek kılar.",
            "Yüz sayfa yazmak yerine bugün iki paragraf, yıllık sağlık hedefi yerine akşam on dakika yürüyüş. Küçük adım önemsiz değil zincirin tek gerçek halkasıdır.",
            "Laozi aceleyle son basamağa atlamayı değil şeyleri kolayken ele almayı öğütler. Küçük çatlak erken onarılırsa duvarı yıkmak gerekmez.",
            "Sabır burada yavaşlık tutkusu değil, büyük sonucun küçük nedenlerden büyüdüğünü bilmektir.",
        ], "DÖRDÜNCÜ KISIM · GÜNDELİK DAO", art="first-step", caption="Uzak yol hayaldeki son çizgide değil, ayağın altındaki ilk küçük ve gerçek adımda başlar."),
        entry("Metnin tarihsel ve siyasi sınırı", [
            "Tao Te Ching erken Çin'in savaş ve yönetim tartışmaları içinden gelir. Köye dönüş, az bilgi ve az araç gibi özlemleri modern toplum için doğrudan program yapmak mümkün değildir.",
            "Yönetilenlerin pasif ve bilgisiz tutulmasını öven yorumlar otoriterliğe kapı açabilir. Sessizlik bazen bilgelik, bazen iktidarın talebidir; aradaki fark güç ilişkisinde aranmalıdır.",
            "Metin en iyi, tek reçete olarak değil aşırı zorlama ve gösterişe karşı düzeltici ses olarak okunur.",
        ], "SON DURAKLAR"),
        entry("Tao'yu verimlilik hilesine çevirmemek", [
            "Wuwei'yi daha çok iş bitirme tekniği yaparsak metnin arzu eleştirisini kaçırırız. Amaç yalnız daha verimli makine olmak değil, gereksiz yarışın kendisini sorgulamaktır.",
            "Su gibi olmak herkese evet demek değildir. Su gerektiğinde yatağını değiştirir, taşar ve sınır çizer. Zorlamasızlık edilgen boyun eğme değildir.",
            "Bir kavram sizi daha sakin ama daha adaletsiz yapıyorsa eksik uygulanmıştır. Dao ilişkilerin bütününü gözetir.",
        ], "SON DURAKLAR"),
        entry("Bir haftalık su deneyi", [
            "Bir gün konuşmada boşluk bırakın, bir gün çamurlu kararı sabaha erteleyin, bir gün hedefi koruyup yöntemi esnetin. Sonra takvimde işe yarayan bir boşluk açın.",
            "Bir nesne veya unvan arzusunu reklamından ayırıp gerçek ihtiyacı sorun. Bir tartışmada son sözü değil ortak yolu arayın.",
            "Deneyin amacı Laozi rolü yapmak değil, daha az zorlama ile hangi işlerin daha doğal ilerlediğini görmek.",
        ], "SON DURAKLAR"),
        entry("Bir cümlede kitabın özü", [
            "Hayatın her parçasını sertçe yönetmeye çalışmak akışı bozar; suyun esnekliği, kabın boşluğu ve zamanında durmak, daha sessiz ama dayanıklı bir güç yaratır.",
            "Akılda kalacak görüntü su ile kayadır: Su kavga etmez, yolundan vazgeçmez ve zamanla en sert yüzeyde bile iz bırakır.",
        ], "SON DURAKLAR"),
    ]))


BOOKS.append(base(92, "Mukaddime", "İbn Haldun",
    "Tarihi hükümdarların isim dizisi olmaktan çıkarıp göçebe dayanışması, şehir rahatlığı, vergi, emek, eğitim ve iktidarın tekrar eden hareketleriyle açıklamaya çalışan 14. yüzyıl dehasının büyük laboratuvarına sade giriş.",
    "#77583F", "Al-Muqaddimah", "mukaddime",
    [
        {"id": 1, "title": "Encyclopaedia Britannica - Ibn Khaldun", "url": "https://www.britannica.com/biography/Ibn-Khaldun"},
        {"id": 2, "title": "Muslim Philosophy - Muqaddimah metni", "url": "https://www.muslimphilosophy.com/ik/Muqaddimah/"},
        {"id": 3, "title": "Internet Encyclopedia of Philosophy - Ibn Khaldun", "url": "https://iep.utm.edu/ibn-khaldun/"},
        {"id": 4, "title": "UNESCO - Ibn Khaldun ve düşünsel mirası", "url": "https://en.unesco.org/courier/2019-4/ibn-khaldun-historian-future"},
    ], [
        entry("Bu kitap nasıl okunmalı?", [
            "Mukaddime aslında büyük bir dünya tarihinin girişidir, fakat giriş eserin en ünlü kısmına dönüşmüştür. İbn Haldun haberleri doğrulama, toplumların nasıl kurulduğu ve devletlerin neden zayıfladığı üzerine genel bir bilim tasarlar.",
            "Metin 14. yüzyılın Kuzey Afrika ve İslam dünyasında doğmuştur. Evrensel görünen kimi yargıları çağının coğrafya, cinsiyet ve kölelik kabullerini taşır.",
            "Rehber onu modern sosyolojiyi tek başına icat eden kahin yapmayacak; olağanüstü yöntemini, isabetli sezgilerini ve tarihsel sınırlarını birlikte gösterecek.",
        ], "BAŞLANGIÇ"),
        entry("Saraydan çöle uzanan hayat", [
            "İbn Haldun yönetici ailelerle çalıştı, hapse girdi, diplomasi yaptı, kabilelerle görüştü ve şehirlerin el değiştirmesini gördü. Teorisi kitaplık sessizliğinden değil siyasi çalkantının içinden çıktı.",
            "Bir hakem hem soyunma odasını hem tribünü hem yönetim masasını görürse oyunun yalnız kurallardan ibaret olmadığını anlar. İbn Haldun da iktidarın görünen unvanı ile onu taşıyan bağları ayırdı.",
            "Timur'la görüşmesi, tarih yazarının incelediği güçle yüz yüze geldiği simgesel andır. O yalnız eski hikayeleri derlemez, yaşayan toplumu gözler.",
            "Bu hareketli hayat teorisine temkin verir: Devletler kalıcı görünür, fakat onları kuran insanlar ve dayanışmalar değişir.",
        ], "BİRİNCİ KISIM · TARİHİ SINAMAK", art="court-and-desert", caption="Saray, kabile ve savaş arasında dolaşan İbn Haldun iktidarın vitrinini ve görünmeyen dayanaklarını birlikte gördü."),
        entry("Her habere inanma", [
            "Tarihçiler imkansız ordu sayıları, abartılı servetler ve övgü dolu saray hikayeleri aktarabilir. İbn Haldun bir haberin yalnız zincirine değil, toplum düzeninde mümkün olup olmadığına bakar.",
            "Nüfusu on bin olan kasabada yüz bin askerin aylarca beslendiği yazıyorsa hesap yapın. Su, yol, vergi ve yiyecek bu iddiayı taşıyor mu?",
            "Bu yöntem günümüz doğrulamasına şaşırtıcı biçimde benzer. Kaynak kim, çıkarı ne, başka kanıt var mı ve olay gerçek dünyanın sınırlarına uyuyor mu?",
            "Tarihin ilk görevi güzel hikayeyi tekrar etmek değil, olabilirlik testinden geçirmektir.",
        ], "BİRİNCİ KISIM · TARİHİ SINAMAK", art="impossible-army", caption="Büyük sayıların görkemine kapılmadan nüfus, yiyecek ve yol hesabı yapmak tarih haberini gerçeklikte sınar."),
        entry("Umran: İnsanların birlikte yaşama bilimi", [
            "İbn Haldun toplum için umran kavramını kullanır. İnsan tek başına yiyecek, savunma ve üretim ihtiyaçlarını karşılayamaz; işbirliği zorunludur.",
            "Bir ekmekte çiftçi, değirmenci, fırıncı, taş ustası ve taşıyıcının emeği birleşir. Sofradaki basit dilim görünmez bir toplumsal örgüttür.",
            "İşbirliği güç üretir, güç de yönetim ihtiyacı doğurur. Çünkü aynı insanlar birbirine yardım edebilirken birbirine saldırabilir.",
            "Umran hem maddi üretimi hem gelenek, eğitim ve iktidarı kapsar. Tarihi anlamak için insan tabiatı kadar birlikte yaşama biçimine bakmak gerekir.",
        ], "BİRİNCİ KISIM · TARİHİ SINAMAK", art="bread-network", caption="Bir ekmek dilimi bile birçok meslek ve güven ilişkisini birleştiren görünmez toplum ağının ürünüdür."),
        entry("Asabiyet: Birlikte hareket etme bağı", [
            "Asabiyet yalnız akrabalık veya milliyetçilik değildir. Bir grubun birbirini savunmasını, ortak risk almasını ve tek beden gibi hareket etmesini sağlayan dayanışma gücüdür.",
            "Yangında birbirini tanıyan mahalleli kovaları elden ele daha hızlı geçirir. Yalnız komut değil güven ve ortak kader hareket yaratır.",
            "Akrabalık bağı güçlü başlangıç olabilir, fakat ittifak, koruma ve ortak inanç da asabiyeti genişletebilir. Din dağınık grupları daha büyük amaç çevresinde birleştirebilir.",
            "İbn Haldun için devletin ilk yakıtı kılıçtan önce bu bağdır. Ordu, vergi ve saray daha sonra kurulur.",
        ], "İKİNCİ KISIM · DEVLETİN DÖNGÜSÜ", art="bucket-chain", caption="Asabiyet, yangında kovayı elden ele geçirten ortak güven gibi grubun tek hareket üretmesini sağlar."),
        entry("Göçebe sertliği, şehir rahatlığı", [
            "Çöl ve kır yaşamı az kaynak, tehlike ve karşılıklı bağımlılık yüzünden dayanıklılık ile asabiyeti güçlendirebilir. Şehir ise iş bölümü, sanat ve rahatlık üretir.",
            "Kamp yapan ekip herkesin çadırını ve suyunu düşünür; otele geçince hizmet satın alınır ve ortak iş azalır. Rahatlık kötülük değildir, bağın kullanılma biçimini değiştirir.",
            "İbn Haldun bedevi ile yerleşik ayrımını ahlaki ırk sınıflaması değil, yaşam biçimi karşılaştırması olarak kurar. Yine de genellemeleri her topluma uymayabilir.",
            "Şehir uygarlığın zirvesi ve zayıflama riskinin aynı yeridir: İncelik artarken kurucu dayanışma gevşeyebilir.",
        ], "İKİNCİ KISIM · DEVLETİN DÖNGÜSÜ", art="camp-and-city", caption="Kamp ortak emeği zorunlu kılarken şehir hizmet ve incelik üretir; rahatlık dayanışmanın biçimini değiştirir."),
        entry("Hanedan nasıl kurulur?", [
            "Güçlü asabiyete sahip grup dağınık rakipleri aşar, yönetimi ele geçirir ve düzen kurar. İlk kuşak yoksunluğu hatırlar, savaş ve paylaşım alışkanlığını taşır.",
            "Aile şirketinin kurucusu depoda çalışır, müşteriyi tanır ve ekiple aynı sofraya oturur. Yetki ile emek arasındaki mesafe küçüktür.",
            "Devletin başarısı yalnız liderin zekası değildir. Onu taşıyan grubun fedakarlığı, ekonomik imkanlar ve rakiplerin durumu birlikte belirler.",
            "İbn Haldun kahraman tarihini böyle toplumsal mekanizmaya çevirir. Tahtın altında görünmeyen bir omuzlar topluluğu vardır.",
        ], "İKİNCİ KISIM · DEVLETİN DÖNGÜSÜ", art="founding-generation", caption="İlk kuşağın devleti tek kahramanın değil, ortak risk ve emeği taşıyan dayanışma grubunun omuzlarında yükselir."),
        entry("Beş kuşağın gevşeyen yayı", [
            "Kurucu kuşak mücadeleyi yaşar. Sonraki kuşak başarıyı öğrenir ama bedelini daha az hisseder. Daha sonra saray, lüks ve aracılar yönetici ile halk arasına girer.",
            "Bahçeyi kuran dede toprağı bilir, baba işi yönetir, torun yalnız meyvenin masaya geldiğini görürse bakım bilgisi kaybolabilir.",
            "İbn Haldun döngüyü kesin saat gibi vermez. Kuşak sayısı ve süreç koşullara göre değişir; ana fikir kurucu dayanışmanın mirasla otomatik aktarılmamasıdır.",
            "Kurumlar kişisel hafıza kaybını telafi edebilirse ömür uzayabilir. Şeffaflık ve yetenek seçimi, saray körlüğüne karşı modern cevaplar sunar.",
        ], "İKİNCİ KISIM · DEVLETİN DÖNGÜSÜ", art="generational-bow", caption="Kurucu kuşağın gerdiği dayanışma yayı, bedeli yaşamayan kuşaklarda bakım görmezse yavaşça gevşer."),
        entry("Lüks neden yalnız zevk değildir?", [
            "Lüks arttıkça sarayın masrafı, vergi ihtiyacı ve gösteriş rekabeti büyür. Yönetici çevresi halkın gündelik hayatından uzaklaşır ve sadakati parayla satın almaya çalışır.",
            "Başta aynı çadırda kalan ekip, sonra kat kat güvenlik kapılarının arkasında yaşarsa kötü haberi duyamaz. Konfor bilgi akışını kesebilir.",
            "İbn Haldun yoksulluğu kutsamaz; şehir sanatı ve bilimi mümkün kılar. Sorun rahatlığın üretimden ve sorumluluktan kopmasıdır.",
            "Lüks, ekonomik kalem kadar siyasi sinyaldir: Yönetimin asabiyet yerine masrafla ayakta durmaya başladığını gösterir.",
        ], "İKİNCİ KISIM · DEVLETİN DÖNGÜSÜ", art="palace-gates", caption="Sarayın çoğalan kapıları konfor kadar halktan ve kötü haberden uzaklaşan yönetimin işaretidir."),
        entry("Vergiyi artırınca gelir neden düşebilir?", [
            "Hanedanın başında vergi düşük, çalışma isteği ve ticaret canlı olabilir. Harcama büyüdükçe oranlar artar; üretici kazancın çoğunu kaybedeceğini düşünürse yatırım azalır ve vergi tabanı daralır.",
            "Pazarcının her satışından dokuz elma alınırsa ertesi hafta tezgah açmayabilir. Oranı yükseltmek kasa gelirini otomatik yükseltmez.",
            "Bu gözlem daha sonra modern vergi tartışmalarında ünlü oldu. Fakat İbn Haldun her vergi indiriminin geliri artıracağını söylemez; başlangıç koşulu ve kamu ihtiyacı önemlidir.",
            "Asıl ders davranışsal tepkidir. İnsanlar kural karşısında sabit taş değil, kararını değiştiren aktörlerdir.",
        ], "ÜÇÜNCÜ KISIM · EMEK VE ŞEHİR", art="tax-market", caption="Pazarcının kazancının çoğu alınırsa oran yükselse bile tezgahlar kapanır ve toplam gelir daralabilir."),
        entry("Emek değeri nasıl büyütür?", [
            "Doğadaki ham madde insan emeği ve becerisiyle kullanılır hale gelir. Taş, ustanın bilgisiyle eve; yün, dokumacının işiyle kumaşa dönüşür.",
            "Bir fincanın fiyatında kil kadar şekil verme, fırın, taşıma ve pazar düzeni vardır. Değer toplumsal iş bölümünde katmanlanır.",
            "İbn Haldun kazanç ve geçim arasında emek bağını vurgular, fakat modern emek değer teorisini tam haliyle kurmuş değildir. Onu sonraki düşünürlerin aynısı yapmak tarihsel farkı siler.",
            "Yine de servetin sandıkta duran altın değil, üretim yapan insan ve şehir kapasitesi olduğunu güçlü biçimde görür.",
        ], "ÜÇÜNCÜ KISIM · EMEK VE ŞEHİR", art="clay-to-cup", caption="Kil tek başına fincan değildir; emek, beceri, ateş ve pazar düzeni ham maddeye kullanılır değer ekler."),
        entry("İş bölümü şehri büyütür", [
            "Tek kişinin yalnız geçimine yetecek emeği, insanlar uzmanlaşınca fazlalık üretebilir. Artık ürün nüfusu, zanaatı, eğitimi ve pazarı besler.",
            "Herkes kendi ayakkabısını yapmaya çalışırsa gün biter. Usta ayakkabıcı yüz kişiye hizmet eder, diğerleri kendi işinde uzmanlaşır.",
            "Şehir büyüdükçe ince meslekler ve sanatlar doğar. Fakat bu zenginlik güvenli yol, hukuk ve talebe bağlıdır.",
            "İbn Haldun ekonomik canlılığı yalnız para miktarıyla değil, insanların birbirine bağlanan üretken becerileriyle açıklar.",
        ], "ÜÇÜNCÜ KISIM · EMEK VE ŞEHİR", art="craft-city", caption="Uzmanlaşan zanaatlar birbirine bağlandığında tek tek emeğin ötesinde şehir ölçeğinde üretkenlik doğar."),
        entry("Fiyatın içinde şehir vardır", [
            "Malın fiyatı talep, kıtlık, vergi, ücret ve taşıma koşullarına göre değişir. Büyük şehirde temel gıda ucuzlayabilirken lüks hizmet pahalılaşabilir.",
            "Aynı domates kurak köyde, liman şehrinde ve kuşatma altındaki kentte başka fiyat taşır. Fiyat yalnız nesnenin içinde duran özellik değildir.",
            "Devlet piyasaya keyfi müdahale ettiğinde üretici çekilebilir; fakat güvenlik ve adil düzen olmadan pazar da çalışmaz. İbn Haldun basit devlet yokluğu savunmaz.",
            "Ekonomi, siyasi istikrar ve toplumsal güvenle birlikte hareket eder. Bozuk para üzerindeki hükümdar resmi, arkasındaki kuruma duyulan inancı temsil eder.",
        ], "ÜÇÜNCÜ KISIM · EMEK VE ŞEHİR", art="many-prices", caption="Aynı malın fiyatı kıtlık, yol, vergi ve güven koşullarıyla değişir; etikette bütün şehrin düzeni saklıdır."),
        entry("Eğitimde sertlik ne üretir?", [
            "İbn Haldun aşırı sert eğitimin öğrenciyi yalancı, korkak ve kurnaz yapabileceğini söyler. Sürekli cezadan kaçan çocuk gerçeği değil yetişkinin görmek istediği yüzü göstermeyi öğrenir.",
            "Her hata için bağırılan sınıfta sessizlik başarı sanılır, merak ölür. Öğrenci soruyu çözmek yerine cezayı nasıl önleyeceğini hesaplar.",
            "Öğretim basitten karmaşığa, tekrar ve anlayışla ilerlemelidir. Ağır metni bir anda yüklemek zihni geliştirmek yerine bunaltabilir.",
            "Bu gözlem, kitabın en sıcak ve güncel sayfalarındandır. Bilgi zorla doldurulan çuval değil, aşama aşama kurulan beceridir.",
        ], "DÖRDÜNCÜ KISIM · BİLGİ VE SINIR", art="harsh-classroom", caption="Sert eğitim çocuğa hakikati değil cezadan kaçacak yüzü öğretir; korku sessizlik üretir, anlayış değil."),
        entry("Bilimler neden şehirde gelişir?", [
            "Bilim için boş zaman, öğretmen, kitap, kurum ve öğrenci zinciri gerekir. Bunlar ancak üretim fazlası ve istikrarlı şehir yaşamıyla uzun süre korunabilir.",
            "Tek bir dahinin defteri yetmez; kütüphane, kopyacı, tartışma ve sonraki kuşak gerekir. Bilgi de iş bölümü içinde yaşar.",
            "Şehir çöktüğünde binalarla birlikte eğitim geleneği de dağılır. Bir kitabın kaybı değil, onu okuyacak dil ve yöntem zincirinin kopması asıl yıkımdır.",
            "İbn Haldun kültürü süs değil, ekonomik ve siyasi altyapıya bağlı canlı kurum olarak görür.",
        ], "DÖRDÜNCÜ KISIM · BİLGİ VE SINIR", art="knowledge-chain", caption="Bilim tek dahinin kıvılcımıyla değil, öğretmen, kitap, kurum ve kuşakların koruduğu uzun bir zincirle yaşar."),
        entry("Coğrafya ve iklim açıklamaları", [
            "İbn Haldun iklim, beslenme ve coğrafyanın toplumlara etkisini tartışır. Çevrenin yaşam biçimini etkilediğini görmesi değerlidir, fakat bazı insan grupları hakkındaki genellemeleri bugün bilimsel ve ahlaki olarak kabul edilemez.",
            "Çevre etkisi kader değildir. Aynı iklimde farklı kurumlar ve tarihler oluşabilir; insan kültürü çevreyi de dönüştürür.",
            "Tarihsel metni dürüst okumak, parlak fikirleri alıp önyargılı bölümleri gizlemek değildir. Büyük düşünürler çağlarının sınırlarını taşıyabilir.",
            "Bu bölüm bize yöntemi yazarına da uygulamayı öğretir: İddia toplum düzeninde ve kanıtta gerçekten mümkün mü?",
        ], "DÖRDÜNCÜ KISIM · BİLGİ VE SINIR", art="climate-map", caption="Çevre yaşam biçimini etkileyebilir, fakat toplumları tek renge boyayan kader haritası olamaz."),
        entry("Döngü kader midir?", [
            "Devletlerin yükselip zayıflaması İbn Haldun'da güçlü örüntüdür, fakat her devlet aynı sayıda kuşakla aynı sona gitmez. Kurumlar, teknoloji ve dış dünya döngüyü değiştirebilir.",
            "Aile şirketi profesyonel yönetim, açık hesap ve yenilenmiş ortak amaçla kurucunun hafızasını kuruma çevirebilir. Döngü uyarıdır, takvim değildir.",
            "Teorinin gücü tekrar eden riskleri göstermesidir: Güç merkezileşir, masraf büyür, dayanışma zayıflar ve yeni kenar gruplar yükselir.",
        ], "SON DURAKLAR", art="cycle-not-clock", caption="Devlet döngüsü kesin saat değil, dayanışma ve kurumlar zayıfladığında yaklaşan riskleri gösteren bir uyarı çemberidir."),
        entry("Modern kelimeleri geriye yapıştırmamak", [
            "İbn Haldun'a sosyolojinin, ekonominin veya Laffer eğrisinin mucidi demek ilgi çekicidir ama benzerlikleri abartabilir. O kendi dini, hukuki ve tarihsel dünyasında başka sorularla çalışır.",
            "Öncülük değeri, bugünkü teoriyi eksiksiz söylemesinde değil toplumsal neden arama cesaretindedir. Hükümdarın karakteri yerine vergi, üretim ve dayanışmayı inceler.",
            "Onu gerçekten onurlandırmak, heykel yapmak değil iddialarını kendi yöntemiyle sınamaktır.",
        ], "SON DURAKLAR"),
        entry("Bugünün kurumuna üç soru", [
            "Bu kurumu gerçekten birlikte tutan asabiyet nedir: Korku, çıkar, güven veya ortak amaç? Kurucu kuşaktan hangi bilgi kayboldu? Masraf ile üretkenlik arasındaki denge nasıl değişti?",
            "Sonra kötü haberin yöneticiye ulaşıp ulaşmadığını sorun. Saray kapıları çoğaldıkça raporlar güzelleşebilir.",
            "Son olarak sayıları olabilirlik testine sokun. Büyük hedefin insan, zaman ve kaynak hesabı var mı? Mukaddime'nin yöntemi bu üç soruda yaşamaya devam eder.",
        ], "SON DURAKLAR"),
        entry("Bir cümlede kitabın özü", [
            "Tarih yalnız büyük adamların iradesiyle değil, toplumları birlikte hareket ettiren dayanışma, üretim, vergi ve kurumların zamanla değişen dengesiyle akar.",
            "Akılda kalacak görüntü sarayın altındaki omuzlardır: Taht görünür, onu taşıyan asabiyet ve emek görünmez; omuzlar çekilince altın koltuk havada kalamaz.",
        ], "SON DURAKLAR"),
    ]))


BOOKS.append(base(99, "Özgürlük Üzerine", "John Stuart Mill",
    "Çoğunluğun da bir zorba olabileceğini, yanlış fikrin bile hakikate hizmet edebileceğini ve yetişkin bireyin kendi hayat deneyine hangi sınırda karışılmaması gerektiğini günlük çatışmalarla anlatan özgürlük rehberi.",
    "#68506F", "On Liberty", "ozgurluk-uzerine",
    [
        {"id": 1, "title": "Project Gutenberg - On Liberty tam metni", "url": "https://www.gutenberg.org/files/34901/34901-h/34901-h.htm"},
        {"id": 2, "title": "Stanford Encyclopedia of Philosophy - John Stuart Mill", "url": "https://plato.stanford.edu/entries/mill/"},
        {"id": 3, "title": "Internet Encyclopedia of Philosophy - Mill", "url": "https://iep.utm.edu/milljs/"},
        {"id": 4, "title": "Liberty Fund - On Liberty", "url": "https://oll.libertyfund.org/title/mill-on-liberty-and-the-subjection-of-women-1879-ed"},
    ], [
        entry("Bu kitap nasıl okunmalı?", [
            "Mill irade özgürlüğünü değil toplumun birey üzerindeki meşru gücünü inceler. Soru şudur: Devlet veya çoğunluk bir yetişkinin davranışına ne zaman haklı olarak karışabilir?",
            "Cevabı zarar ilkesidir, fakat zarar sözcüğü kolay değildir. Hakaret, ekonomik kayıp, risk, incinme ve ortak sorumluluk arasındaki sınırlar tartışma ister.",
            "Kitap 1859'un erkek merkezli ve sömürgeci kabullerini taşır. Rehber güçlü özgürlük savını günümüz eşitlik ve güç sorunlarıyla birlikte sınayacak.",
        ], "BAŞLANGIÇ"),
        entry("Kral gidince zorbalık bitmedi", [
            "Eski özgürlük mücadelesi hükümdarın gücünü sınırlamak üzerineydi. Demokrasi gelince halkın kendi kendini yönettiği ve artık baskı sorunu kalmadığı sanılabilirdi. Mill çoğunluğun azınlığa baskısını gösterir.",
            "Apartman toplantısında yirmi kişi bir kişinin evinde hangi kitabı okuyacağına karar verirse oy çokluğu müdahaleyi doğru yapmaz.",
            "Toplumsal zorbalık bazen yasadan daha derine işler. İş kaybı, dışlanma ve itibarsızlaştırma insanı resmi ceza olmadan susturabilir.",
            "Özgürlük bu yüzden yalnız sandık ve anayasa değildir. Farklı yaşamın nefes alabileceği kültürel alan da gerekir.",
        ], "BİRİNCİ KISIM · ÇOĞUNLUĞUN GÖLGESİ", art="majority-shadow", caption="Oy çokluğu ortak kararı meşrulaştırabilir, fakat bir kişinin özel hayatına sınırsız girme hakkı vermez."),
        entry("Zarar ilkesi", [
            "Mill'e göre medeni toplum bir yetişkine kendi iyiliği için zor kullanmamalıdır. Müdahalenin temel gerekçesi başkalarına zararı önlemektir.",
            "Kask takmayan bisikletçi ağırlıkla kendi riskini alır; kalabalıkta tehlikeli hızla sürmek başkasını da riske sokar. Sınır davranışın etkisinde belirir.",
            "Nasihat, ikna ve eleştiri serbesttir. Yasak ve ceza için daha yüksek eşik gerekir. Birinin seçimini beğenmemek zarar kanıtı değildir.",
            "İlke pusuladır, otomatik hesap makinesi değil. Salgın, çevre kirliliği ve finansal risk gibi dağınık zararlar daha karmaşık uygulama gerektirir.",
        ], "BİRİNCİ KISIM · ÇOĞUNLUĞUN GÖLGESİ", art="harm-boundary", caption="Kişisel risk ile başkasına taşan zarar arasındaki sınır, müdahalenin meşru olup olmadığını belirleyen pusuladır."),
        entry("Kendi iyiliğin için seni zorlamak", [
            "Paternalizm, yetişkini kendi iyiliği için zorlamaktır. Mill kişinin yanlış seçim yapma hakkını savunur; çünkü kendi hayatının acısını, değerini ve koşullarını en yakından o bilir.",
            "Arkadaşınız kötü bulduğunuz mesleği seçebilir. Onu uyarabilirsiniz, diplomasını saklayıp kararını engellemek başka şeydir.",
            "Bunun istisnaları bilgi ve özgürlük eksikliğinde ortaya çıkar. Çökmek üzere olan köprüye bilmeden yürüyen kişiyi durdurmak, seçimini ezmek değil gerekli bilgiyi ulaştırmaktır.",
            "Bağımlılık, çocukluk ve ağır bilişsel bozulma gibi durumlar özerklik kapasitesini zor soruya çevirir. Mill'in sade ilkesi uygulamada dikkat ister.",
        ], "BİRİNCİ KISIM · ÇOĞUNLUĞUN GÖLGESİ", art="dangerous-bridge", caption="Tehlikeyi bilmeyeni köprüde durdurmak onun değerini seçmek değil, özgür karar için eksik bilgiyi tamamlamaktır."),
        entry("Susturulan fikir doğru olabilir", [
            "Bir fikri susturursak yanlışlanabilir olduğumuzu unutmuş oluruz. Tarihte çoğunluk ve otorite defalarca yanılmıştır. Kesinlik hissi, yanılmazlık kanıtı değildir.",
            "Mahkemede tek tanığı dinleyip hüküm vermek kolaydır. Karşı tanık rahatsız edici olsa bile olayın eksik yönünü gösterebilir.",
            "Fikir yanlışsa bile konuşması doğru görüşün gerekçelerini sınar. Tartışılmayan hakikat canlı anlayıştan ezberlenmiş slogana dönüşür.",
            "Mill'in güçlü iddiası budur: İfade özgürlüğü yalnız konuşanın hakkı değil, dinleyenin gerçeği arama imkanına aittir.",
        ], "İKİNCİ KISIM · FİKİRLERİN PAZARI", art="silenced-witness", caption="Rahatsız edici tanığı susturmak yalnız onun sesini değil, dinleyenin gerçeğin eksik parçasına ulaşma imkanını da alır."),
        entry("Yanlış fikirdeki doğru parça", [
            "Çatışan görüşlerin biri tamamen doğru, diğeri tamamen yanlış olmayabilir. Her biri deneyimin başka parçasını taşıyabilir; tartışma daha geniş hakikati kurar.",
            "İşyerinde biri hız, diğeri güvenlik ister. Tek taraf kazanırsa ya teslimat kaçar ya kaza riski büyür. Çözüm karşıtların taşıdığı gerçek ihtiyaçları birleştirir.",
            "Mill özellikle siyasal kampların birbirinin kör noktasını düzelttiğini düşünür. Düzen ile ilerleme, eşitlik ile özgürlük tek kutupta tamamlanmayabilir.",
            "Bu her orta yolun doğru olduğu anlamına gelmez. Kanıt bir tarafı açıkça destekleyebilir; yine de karşı görüşü anlamadan kararın sınırı görülmez.",
        ], "İKİNCİ KISIM · FİKİRLERİN PAZARI", art="two-lamps", caption="Karşıt görüşler aynı odanın farklı köşelerini aydınlatabilir; geniş görüntü iki ışığın sınanmasıyla oluşur."),
        entry("Ölü dogma ile yaşayan hakikat", [
            "Bir inancı doğru olduğu için tartışmadan korumak, zamanla onun neden doğru olduğunu unutturur. İnsan cümleyi tekrarlar ama yeni duruma uygulayamaz.",
            "Ezberlediği formülü sorunun biçimi değişince kullanamayan öğrenci gibi, toplum da sınanmayan ilkeleri taşıyamaz.",
            "Karşı görüş hakikatin spor partneridir. İtiraz gerekçeyi zorlar, zayıf ifadeyi düzeltir ve inancı bilinçli seçime dönüştürür.",
            "Mill için düşünce huzuru değil zihinsel canlılık önemlidir. Rahatsızlık bazen öğrenmenin fiyatıdır.",
        ], "İKİNCİ KISIM · FİKİRLERİN PAZARI", art="living-truth", caption="İtiraz görmeyen doğru fikir kullanılmayan kas gibi zayıflar; tartışma gerekçeyi canlı tutar."),
        entry("Söz ne zaman eyleme dönüşür?", [
            "Mill aynı cümlenin bağlama göre farklı sonuç doğurabileceğini söyler. Tahıl tüccarlarının yoksulları aç bıraktığını gazetede yazmak ile öfkeli kalabalığın önünde tüccarın evini göstererek bağırmak aynı değildir.",
            "Sözcük hava boşluğunda durmaz. Hedef, yakın tehlike, kalabalığın durumu ve konuşanın niyeti zarar ihtimalini değiştirir.",
            "Bu ayrım ifade özgürlüğünün sınırsız ses çıkarma olmadığını gösterir. Doğrudan şiddet tehdidi, taciz ve kişisel hedef gösterme başkasının güvenliğini bozar.",
            "Yine de belirsiz 'rahatsızlık' gerekçesi eleştiriyi susturmak için kullanılmamalıdır. Eşik somut ve açıklanabilir olmalıdır.",
        ], "İKİNCİ KISIM · FİKİRLERİN PAZARI", art="words-in-crowd", caption="Aynı fikir makalede tartışma, öfkeli kalabalık önünde hedef gösterme olduğunda yakın zarar doğurabilir."),
        entry("Hayat bir deney alanıdır", [
            "Mill insanların farklı yaşam biçimlerini denemesini insan gelişiminin koşulu sayar. Herkese tek doğru elbise giydirmek karakteri köreltir.",
            "Bir bahçede yalnız tek tohum yetiştirirseniz iklim değiştiğinde bütün ürün kaybolabilir. Çeşitli hayat deneyleri toplumun öğrenme yedekleridir.",
            "Deneyin bedeli ağırlıkla deneyene ait olmalıdır. Başkasını rızası dışında malzeme yapmak özgürlük değildir.",
            "Farklı yaşayan kişi yalnız kendisi için değil, başkalarının görmediği yeni imkanları gösterdiği için de toplumsal değer taşır.",
        ], "ÜÇÜNCÜ KISIM · BİREYSELLİK", art="many-seeds", caption="Farklı yaşam deneyleri tek ürünlü tarlaya karşı toplumun öğrenme ve dayanıklılık çeşitliliğini korur."),
        entry("Karakter seçimle büyür", [
            "Doğru kararın hazır listesiyle yaşayan kişi itaatkar olabilir, gelişmiş karakter sahibi olmayabilir. Muhakeme, tercih yaparak ve sonucunu taşıyarak güçlenir.",
            "Spor salonunda başkasının kaldırdığı ağırlığı izlemek kas yapmaz. Ahlaki ve pratik yetiler de kişisel seçim olmadan gelişmez.",
            "Bu yüzden iyi niyetli aşırı koruma insanı çocuklaştırabilir. Hata ihtimali özgürlüğün maliyetidir, fakat ağır ve geri döndürülemez risklerde bilgi ile güvenlik ağı gerekir.",
            "Mill bireyselliği bencil keyif değil, insan kapasitesinin işlenmesi olarak görür.",
        ], "ÜÇÜNCÜ KISIM · BİREYSELLİK", art="choice-muscle", caption="Karakter hazır doğruyu seyrederek değil, seçim yapıp sonucundan öğrenerek güçlenen bir kas gibidir."),
        entry("Gelenek pusula mı zincir mi?", [
            "Gelenek geçmiş kuşakların deneyimini taşır ve her şeyi sıfırdan keşfetme yükünü azaltır. Fakat kişi nedenini bilmeden uyguladığında yaşayan rehber zincire dönüşebilir.",
            "Ailede herkes aynı mesleği seçmiş olabilir. Bu yol size de uygun olabilir; yalnız 'bizde böyledir' cümlesi uygunluğun kanıtı değildir.",
            "Mill geleneği yakmayı değil sınamayı ister. Kendi koşulunuzda işe yarıyorsa bilinçli biçimde sahiplenirsiniz.",
            "Özgünlük sırf farklı görünmek değildir. Kopya ile isyan arasında, düşünüp seçilmiş hayat vardır.",
        ], "ÜÇÜNCÜ KISIM · BİREYSELLİK", art="compass-and-chain", caption="Gelenek yön gösteren pusula olabilir; nedenini sormadan bağlanınca hareketi kısıtlayan zincire dönüşür."),
        entry("Eksantrik insanın toplumsal değeri", [
            "Toplumda güçlü karakter azaldıkça sıra dışılık kuşkuyla karşılanır. Mill eksantrikliğin bazen canlılık ve bağımsız düşünce işareti olduğunu savunur.",
            "Mahallede yağmur suyu toplayan tuhaf komşu yıllar sonra kuraklıkta işe yarayan yöntemi göstermiş olabilir. İlk farklılık çoğu zaman gereksiz görünür.",
            "Her tuhaflık değerli değildir; zarar ve kanıt yine ölçüdür. Fakat yalnız alışılmadık olduğu için bastırmak toplumu kendi yenilik laboratuvarından mahrum bırakır.",
            "Hoşgörü yalnız sevdiğimiz çeşitlilik için değil anlamadığımız zararsız hayatlar için sınanır.",
        ], "ÜÇÜNCÜ KISIM · BİREYSELLİK", art="unusual-neighbor", caption="Bugün tuhaf görünen zararsız deney, yarının ortak sorununa beklenmedik bir çözüm gösterebilir."),
        entry("Kendine ilişkin ve başkasına ilişkin eylem", [
            "Mill bazı eylemleri ağırlıkla kişinin kendisini, bazılarını doğrudan başkalarını etkileyen alanlara ayırır. Gerçek hayatta sınır geçirgendir; borç, bakım yükümlülüğü ve kamu kaynakları bağlantı yaratır.",
            "Gece yüksek sesle müzik dinlemek evde yalnızsanız kişisel tercih, duvarın öte yanında bebek uyurken başkasının alanına taşan etkidir.",
            "Her dolaylı etki yasak gerekçesi olursa özgür alan kalmaz. Toplum somut, ciddi ve makul biçimde öngörülebilir zararı ayırt etmelidir.",
            "İlke komşuluğu görünür kılar: Özgürlüğünüz vardır, fakat başkasının eşit özgürlüğüyle aynı koridorda yürür.",
        ], "DÖRDÜNCÜ KISIM · UYGULAMA", art="shared-wall", caption="Kişisel tercih ortak duvardan geçip başkasının uykusunu bozduğunda özgürlük alanları birbirine temas eder."),
        entry("Sözleşme ve yükümlülük", [
            "Bir kişi özgürce söz verdiğinde eylemi artık yalnız kendisini ilgilendirmeyebilir. İş sözleşmesi, çocuk bakımı veya borç başkalarının planını o söze bağlar.",
            "Arkadaşınıza havaalanına götürme sözü verip son anda keyfim değişti demek kişisel özgürlük değil, başkasına yüklenen maliyettir.",
            "Yine de her söz sonsuza dek kölelik yaratmaz. Koşullar değişebilir, adaletsiz sözleşme ve güç eşitsizliği rızayı sakatlayabilir.",
            "Mill özgürlüğü bağsızlık olarak değil, seçilmiş yükümlülüklerin sorumluluğuyla birlikte düşünür.",
        ], "DÖRDÜNCÜ KISIM · UYGULAMA", art="promise-rope", caption="Özgürce verilen söz başkasının planını size bağladığında seçim, yeni bir sorumluluk ipi oluşturur."),
        entry("Ticaret, risk ve düzenleme", [
            "Satıcı ile alıcı arasındaki ilişki başkasına etki ettiği için tamamen özel değildir. Sahte ürün, gizli tehlike ve bilgi eşitsizliği müdahaleyi haklı kılabilir.",
            "Zehirli madde şeker paketi gibi satılıyorsa 'alıcı özgürce seçti' denemez. Etiket ve güvenlik standardı seçimi mümkün kılan altyapıdır.",
            "Mill aşırı düzenlemenin yenilik ve kişisel sorumluluğu boğabileceğini de düşünür. Sorun kuralın varlığı değil amacıyla orantısıdır.",
            "Bugün platformlar ve finansal ürünlerde aynı soru sürer: Bilgi verilmesi yeterli mi, yoksa tasarım insanın zayıflığını sistemli biçimde sömürüyor mu?",
        ], "DÖRDÜNCÜ KISIM · UYGULAMA", art="market-label", caption="Doğru etiket ve güvenlik standardı seçimi yok etmez; alıcının gerçek seçim yapabilmesi için zemin kurar."),
        entry("Eğitim ve çocuklar", [
            "Mill zarar ilkesini tam kapasite sahibi yetişkinlere uygular. Çocukların gelecekte özgür birey olabilmesi için eğitim ve korunma gerekir.",
            "Yüzme bilmeyen çocuğu özgürlük adına derin suya bırakmak özerklik değil ihmaldir. Ama onu hayat boyu kıyıda tutmak da yetisini engeller.",
            "Eğitimin devletçe sağlanmasını desteklerken tek tip devlet eğitiminin zihinleri aynı kalıba sokmasından çekinir. Ortak temel ile çoğul yöntem arasında denge arar.",
            "Çocuğun bugünkü güvenliği ve yarının seçim kapasitesi aynı anda korunmalıdır.",
        ], "DÖRDÜNCÜ KISIM · UYGULAMA", art="learning-to-swim", caption="Çocuğu korumak onu sonsuza dek kıyıda tutmak değil, güvenli destekle kendi yüzme kapasitesini kurmaktır."),
        entry("Mill'in kör noktaları", [
            "Mill özgürlük ilkesini 'barbar' saydığı toplumlara tam uygulamaz ve sömürge yönetimini belli koşullarda savunur. Bu, evrensel özgürlük iddiasıyla ciddi çelişkidir.",
            "Ayrıca maddi yoksulluk, cinsiyet ve işveren gücü seçimleri kağıt üzerinde özgür, gerçekte zorunlu hale getirebilir. Yalnız devlet müdahalesine bakmak özel iktidarı kaçırır.",
            "Harriet Taylor Mill'in düşünsel katkısı uzun süre gölgede kalmıştır. Kitabın özgür bireyi, bakım ve bağımlılık ilişkileriyle daha zengin düşünülmelidir.",
        ], "SON DURAKLAR", art="liberty-blind-spots", caption="Özgürlük ilkesi sömürge, yoksulluk ve özel güç karşısındaki kör noktaları görülmeden gerçekten evrensel olamaz."),
        entry("Sosyal medyada fikir pazarı", [
            "Mill karşıt fikirlerin çarpışmasının hakikati güçlendireceğini düşünür. Fakat bugünün platformları doğruyu değil dikkati ödüllendirebilir; öfke ve yalan hız avantajı kazanabilir.",
            "Fikir pazarı iyi işlemek için erişim, güvenilir bilgi ve yanıt imkanına ihtiyaç duyar. Tek şirketin algoritması görünürlük kapısını kontrol ediyorsa pazar nötr değildir.",
            "Çözüm kolay sansür de sınırsız dağıtım da değildir. Şeffaf kurallar, itiraz yolları ve medya okuryazarlığı özgür tartışmanın altyapısıdır.",
        ], "SON DURAKLAR"),
        entry("Gündelik özgürlük kontrolü", [
            "Bir davranışı yasaklamak istediğinizde dört soru sorun: Somut zarar ne, kime, ne kadar yakın ve daha hafif çözüm var mı? Yalnız rahatsızlık veya ahlaki beğenmeme mi var?",
            "Bir fikri susturmak istediğinizde onu çürütecek kanıtı ve dinleyenin karar hakkını düşünün. Tehdit ile eleştiriyi ayırın.",
            "Kendi hayatınızda ise tek bir küçük deney seçin. Başkasına zarar vermeden size uygun yaşamı yalnız gelenek yüzünden ertelediğiniz yer neresi?",
        ], "SON DURAKLAR"),
        entry("Bir cümlede kitabın özü", [
            "Yetişkin bireyin düşüncesi ve hayat deneyi, başkasına somut zarar vermediği sürece çoğunluğun beğenisine teslim edilemez; çünkü hakikat ve karakter ancak özgür sınamada gelişir.",
            "Akılda kalacak görüntü farklı tohumların bahçesidir: Tek tip düzen temiz görünür, fakat toplumun öğrenme ve yenilenme gücü çeşitlilikte saklıdır.",
        ], "SON DURAKLAR"),
    ]))


BOOKS.append(base(121, "Meditasyonlar", "René Descartes",
    "Şüpheyi her şeyi yıkmak için değil sağlam bir temel bulmak için kullanan; rüya, aldatıcı cin, düşünen benlik, Tanrı ve dış dünya üzerinden altı günlük zihinsel yolculuğu gündelik örneklerle açan rehber.",
    "#52667A", "Meditationes de Prima Philosophia", "meditasyonlar-descartes",
    [
        {"id": 1, "title": "Cambridge - Meditations on First Philosophy içeriği", "url": "https://www.cambridge.org/highereducation/books/the-philosophical-writings-of-descartes/618B16C4C0116CBB0B39211F93E2BCB3/meditations-on-first-philosophy/5F229195B38C9D9C78CCF46DFC393283"},
        {"id": 2, "title": "Toronto Metropolitan University - Kamusal alan metni", "url": "https://pressbooks.library.torontomu.ca/meditationsonfirstphilosophy/"},
        {"id": 3, "title": "Stanford Encyclopedia of Philosophy - Descartes", "url": "https://plato.stanford.edu/entries/descartes/"},
        {"id": 4, "title": "Early Modern Texts - Meditations", "url": "https://www.earlymoderntexts.com/assets/pdfs/descartes1641_1.pdf"},
    ], [
        entry("Bu kitap nasıl okunmalı?", [
            "Descartes altı meditasyonu altı ayrı zihinsel gün gibi kurar. Amaç her sabah bir önceki adımı hatırlayıp şüphenin içinden kesinliğe doğru ilerlemektir.",
            "Metin 'her şey yalandır' sonucuna varmaz. Geçici ve yöntemli şüphe kullanır: Sağlam bina için eğri temeli söküp güvenilir nokta arar.",
            "Tanrı kanıtları ve zihin-beden ayrımı kitabın merkezindedir, fakat en çok tartışılan yerleridir. Rehber argümanı anlaşılır kuracak, eleştirileri gizlemeyecek.",
        ], "BAŞLANGIÇ"),
        entry("Eski evin temelini sökmek", [
            "Descartes gençliğinden beri doğru sandığı birçok fikrin yanlış çıktığını fark eder. Üstüne kurulan inançlar da sallanıyorsa tek tek duvar boyamak yetmez; temele dönmek gerekir.",
            "Eğri zemindeki kitaplığı her ay düzeltmek yerine zemini ölçmek gibi, bütün bilgi kaynaklarını sınamaya karar verir.",
            "Her inancı ayrı ayrı kanıtlamak imkansızdır. Bunun yerine inançları besleyen duyular ve akıl yürütme gibi kökleri test eder.",
            "Yöntem gündelik kuşkuculuk değil kontrollü düşünce deneyidir. Alışverişe giderken dünyanın varlığını sorgulamaz; felsefi temeli ararken askıya alır.",
        ], "BİRİNCİ KISIM · ŞÜPHENİN MERDİVENİ", art="old-foundation", caption="Descartes eğri duvarları tek tek düzeltmek yerine bütün inanç binasının temelini sınamaya karar verir."),
        entry("Duyular bazen aldatır", [
            "Uzak kule yuvarlak görünürken yakından köşeli çıkabilir. Suya giren çubuk kırılmış gibi görünür. Duyular en azından bazı koşullarda yanılır.",
            "Bir kez yanlış adres veren navigasyonu tamamen çöpe atmayız, fakat kritik yol ayrımında ek kontrol yaparız. Descartes daha sert davranır: Kesin temel için bazen yanılan kaynağı yeterli bulmaz.",
            "Yakındaki elleri ve ateşi görmenin daha güvenilir olduğu söylenebilir. Bu itiraz onu bir sonraki, daha geniş şüpheye taşır.",
            "Duyuların yanılması onların işe yaramadığını değil mutlak kesinlik sağlamadığını gösterir.",
        ], "BİRİNCİ KISIM · ŞÜPHENİN MERDİVENİ", art="bent-stick", caption="Suda kırık görünen düz çubuk duyuların işe yaramazlığını değil, kesinlik için tek başına yetmediğini gösterir."),
        entry("Şu an rüyada olabilir misin?", [
            "Rüyada masa, beden ve oda gerçek görünür. Uyandığınızda sahnenin zihinde kurulduğunu anlarsınız. Şimdi uyanık olduğunuzu kesin olarak ayıran işaret var mı?",
            "Rüya savı her an gerçekten rüyada olduğumuzu söylemez. Duyusal deneyimin kendi başına dış dünyayı mutlak garanti etmediğini gösterir.",
            "Rüyadaki ejderha bile renk, şekil ve uzam gibi daha basit parçalardan kurulmuş olabilir. Bu yüzden matematiksel doğrular şüpheden kurtulacak gibi görünür.",
            "Descartes şüphe merdivenini yükseltir: Önce tek algı, sonra bütün sahne sorgulanır.",
        ], "BİRİNCİ KISIM · ŞÜPHENİN MERDİVENİ", art="dream-room", caption="Rüya gerçek bir oda gibi hissedebildiğine göre, duyusal sahne kendi gerçekliğini tek başına mühürleyemez."),
        entry("Aldatıcı cin ve son şüphe", [
            "Descartes çok güçlü bir aldatıcının en basit hesapta bile zihnini yanıltığını hayal eder. Bu bir varlık inancı değil, şüpheyi son sınırına taşıyan araçtır.",
            "Bilgisayardaki bütün girişleri değiştiren kötü amaçlı yazılım düşünün. Ekran, klavye ve hesap aynı sistemden geçiyorsa hangi çıktıya güveneceksiniz?",
            "Bu hipotez matematiği bile geçici olarak askıya alır. Okur artık tutunacak hiçbir şey kalmadığını hisseder.",
            "Tam bu boşlukta Descartes, aldatılabilmek için bile var olması gereken bir şeyi bulur: Şüphe eden etkinliğin kendisi.",
        ], "BİRİNCİ KISIM · ŞÜPHENİN MERDİVENİ", art="deceiver-system", caption="Her çıktıyı değiştiren hayali aldatıcı, şüpheyi duyulardan matematiğe kadar en son sınıra taşır."),
        entry("Düşünüyorum, öyleyse varım", [
            "Aldatıcı beni her konuda yanıltabilir, fakat yanıltılan bir etkinlik olmadan aldatma gerçekleşmez. Şüphe ettiğim anda en azından düşünen bir şey olarak varlığım kesindir.",
            "Bir odadaki bütün eşyalar sahte olabilir; 'şu anda kuşku var' olgusu kuşkunun içinde doğrulanır. Kanıt dışarıdan değil eylemin kendisinden gelir.",
            "Cogito uzun bir kıyas değildir. 'Düşünen her şey vardır, ben düşünüyorum' hesabından önce, düşünme anında yakalanan doğrudan kesinliktir.",
            "Bu kesinlik sürekli kimlik veya beden hakkında henüz çok şey söylemez. İlk sağlam taş küçüktür: Düşündüğüm sürece varım.",
        ], "İKİNCİ KISIM · DÜŞÜNEN BEN", art="first-stone", caption="Bütün sahne şüpheli olsa bile şüphe eylemi, o anda düşünen varlığın ilk sağlam taşı olur."),
        entry("Ben neyim?", [
            "Descartes bedenin varlığını henüz geri kazanmamıştır. Kendini şüphe eden, anlayan, isteyen, hayal eden ve duyan bir düşünce etkinliği olarak tanır.",
            "Telefonun dış kasası hakkında her şeyden kuşku duyarken ekranda işlem sürdüğünü bilmek gibi, işleyen zihin bedenden önce kesinleşir.",
            "Buradan zihin ile bedenin ayrı tözler olduğu sonucu daha sonra kurulacaktır. Cogito tek başına ayrılığı tamamlamaz.",
            "Benliği yalnız düşünceye bağlamak bedenlenmiş deneyimi küçümseyebilir. Modern felsefe ve bilim, zihnin beden ile çevreye sıkı bağını vurgular.",
        ], "İKİNCİ KISIM · DÜŞÜNEN BEN", art="thinking-flame", caption="Beden şüphedeyken bile kuşku, isteme ve hayal etme etkinliği sönmeyen bir düşünce alevi olarak kalır."),
        entry("Balmumu parçası", [
            "Yeni balmumu bal kokar, serttir ve belirli biçimdedir. Ateşe yaklaşınca kokusu, rengi, şekli ve dokusu değişir; yine de aynı balmumu olduğunu söyleriz.",
            "Duyular her özelliği değişmiş gösterdiğine göre nesnenin sürekliliğini yalnız duyuyla tanımıyoruz. Zihin onun değişebilir uzamlı bir şey olduğunu kavrıyor.",
            "Bu örnek aklın algıdaki rolünü gösterir. Görmek pasif fotoğraf çekmek değil, değişim içinde nesne tanımaktır.",
            "Eleştirmenler bunun zihni bedenden bağımsız kanıtlamadığını söyler. Yine de algının yorum içeren etkinlik olduğunu canlı biçimde açar.",
        ], "İKİNCİ KISIM · DÜŞÜNEN BEN", art="melting-wax", caption="Balmumunun bütün duyusal özellikleri değişse de zihin onu aynı değişebilir nesne olarak tanır."),
        entry("Açık ve seçik fikir ölçüsü", [
            "Cogito'nun kesinliğini veren şey, Descartes'a göre açık ve seçik kavranmasıdır. Açık fikir zihnin önündedir; seçik fikir başkasıyla karışmaz.",
            "Temiz camdan görünen tek nesne gibi, düşünce bulanıklık taşımadan belirir. Fakat bu ölçünün güvenilirliği Tanrı kanıtına bağlanınca daire itirazı doğar.",
            "Bir fikrin size çok açık gelmesi doğru olduğunu garanti etmeyebilir. Önyargılar da apaçık hissedilebilir; ortak sınama gerekir.",
            "Descartes kişisel kesinlik hissinden daha sıkı bir akıl ölçüsü arar, fakat ölçüyü temellendirmek kitabın zor düğümüdür.",
        ], "İKİNCİ KISIM · DÜŞÜNEN BEN", art="clear-window", caption="Açık ve seçik fikir temiz penceredeki nesne gibi görünür, fakat pencerenin güvenilirliği ayrıca temellendirilmelidir."),
        entry("Sonsuzluk fikri nereden geldi?", [
            "Descartes sınırlı ve kusurlu kendisinde sonsuz, kusursuz varlık fikrinin bulunduğunu söyler. Nedende en az sonuç kadar gerçeklik olmalıysa bu fikrin kaynağı kendisinden üstün olmalıdır.",
            "Boş bardağın kendi başına okyanus fikri üretemeyeceği benzetmesi çekicidir. Descartes buradan Tanrı'nın varlığına gider.",
            "Eleştirmenler sonsuzluğu sonlunun sınırını kaldırarak kurabileceğimizi ve fikirdeki içerik için dış varlık gerekmediğini savunur.",
            "Argümanın ikna gücü ne olursa olsun kitabın mimarisinde görevi büyüktür: İyi Tanrı sistemli aldatmanın önünü kesecektir.",
        ], "ÜÇÜNCÜ KISIM · DÜNYAYI GERİ KURMAK", art="cup-and-ocean", caption="Descartes sınırlı zihindeki sonsuzluk fikrini boş bardakta beliren okyanusa benzeterek kaynağını sorgular."),
        entry("Tanrı aldatır mı?", [
            "Kusursuz varlık aldatıcı olamaz, çünkü aldatma eksikliktir der Descartes. Böylece doğru kullandığımız açık ve seçik düşüncelerin sürekli hileye uğramadığına güven kazanır.",
            "Bankanın ana sistemi güvenilir olunca tek tek işlemleri kontrol etmek anlam kazanır. Tanrı, Descartes'ın bilgi bankasındaki güven sertifikasıdır.",
            "Burada ünlü Kartezyen daire eleştirisi çıkar: Açık ve seçik fikirle Tanrı kanıtlanır, sonra Tanrı açık ve seçik fikri güvenceye alırsa kanıt dönüyor mu?",
            "Descartes farklı anlarda kesinlik ayrımıyla yanıt vermeye çalışır; tartışma bugün de metnin kırılma noktasıdır.",
        ], "ÜÇÜNCÜ KISIM · DÜNYAYI GERİ KURMAK", art="trust-certificate", caption="İyi Tanrı bilgi sisteminin güven sertifikası olur, fakat sertifikanın hangi ölçüyle doğrulandığı daire tartışmasını doğurur."),
        entry("Hata neden var?", [
            "İyi Tanrı bizi yaratmışsa neden yanılırız? Descartes anlayışımızın sınırlı, irademizin ise verilen kanıtın ötesine uzanabildiğini söyler.",
            "Fener yalnız birkaç metreyi aydınlatırken koşarak karanlığa giderseniz çukura düşersiniz. Sorun ışığın verdiği alanda değil hükmün onun ötesine geçmesindedir.",
            "Hata bir nesne değil yanlış kullanım eksikliğidir. Açık kanıt yoksa yargıyı askıya almak özgür iradenin doğru kullanımıdır.",
            "Gündelik ders güçlüdür: Bilmediğini söylemek düşüncenin durması değil, yanlış kesinliğin önlenmesidir.",
        ], "ÜÇÜNCÜ KISIM · DÜNYAYI GERİ KURMAK", art="lantern-limit", caption="Anlayışın feneri sınırlıyken irade karanlığa koşarsa hata doğar; yargıyı bekletmek düşmeyi önler."),
        entry("Üçgen ve varlık kanıtı", [
            "Beşinci meditasyonda Descartes üçgenin iç açılarının özüne bağlı olması gibi, varlığın da kusursuz Tanrı'nın özüne ait olduğunu savunur.",
            "Üç köşesi olmayan üçgen düşünülemez; Descartes var olmayan kusursuz varlığın da çelişki olduğunu ileri sürer.",
            "Kant'ın daha sonraki ünlü itirazı varlığın bir özellik olmadığıdır. Hayali yüz altın ile gerçek yüz altının kavramı aynı, cebinizdeki sonucu farklıdır.",
            "Ontolojik kanıt kısa olduğu için kolay değildir. Kavramdan gerçek varlığa geçişin mümkün olup olmadığını sınar.",
        ], "ÜÇÜNCÜ KISIM · DÜNYAYI GERİ KURMAK", art="triangle-existence", caption="Descartes varlığı kusursuz Tanrı kavramına üç köşenin üçgene ait olduğu kadar zorunlu bağlamaya çalışır."),
        entry("Dış dünya geri dönüyor", [
            "İnsanda duyusal fikirleri kendi isteği dışında alma eğilimi vardır. İyi Tanrı bizi sürekli yanıltmayacağına göre bu fikirlerin kaynağı maddi dünya olmalıdır.",
            "Kapıya her gün siz istemeden paket geliyorsa dışarıda bir gönderici olduğu sonucuna varırsınız. Yine de paketin üstündeki resim içeriği tam göstermeyebilir.",
            "Descartes dış dünyanın varlığını geri kazanır, fakat duyuların her niteliği nesnede olduğu gibi verdiğini söylemez. Ölçü, şekil ve hareket daha temel kabul edilir.",
            "Şüphe yolculuğu başladığı masaya döner, fakat artık masa alışkanlıkla değil argümanla kabul edilmiştir.",
        ], "ÜÇÜNCÜ KISIM · DÜNYAYI GERİ KURMAK", art="returned-table", caption="Descartes şüpheyle kaybettiği masaya geri döner; dış dünya artık alışkanlığın değil kurduğu güven zincirinin sonucudur."),
        entry("Zihin ile beden gerçekten ayrı mı?", [
            "Zihin düşünen, uzamsız şey; beden uzamlı, düşünmeyen şey olarak açık ve seçik kavranabiliyorsa birbirinden ayrılabilir der Descartes.",
            "Yazılım ile donanım benzetmesi ilk anda yardımcıdır: Aynı işlev farklı maddede çalışabilir gibi görünür. Fakat insan zihni bedensiz çalışan program olduğuna dair kanıt değildir.",
            "Ayrılık kişisel ölümsüzlük ve modern zihin felsefesi için büyük etki yarattı. Aynı zamanda zihnin bedeni nasıl hareket ettirdiği etkileşim sorununu doğurdu.",
            "Bugünkü sinirbilim zihinsel süreçlerin beyin hasarı, hormon ve beden durumuyla güçlü bağını gösterir; katı ikicilik ciddi zorluk taşır.",
        ], "DÖRDÜNCÜ KISIM · BEDEN VE GÜNÜMÜZ", art="mind-body-bridge", caption="Zihin ile bedeni iki ayrı kıyı yapmak, aralarındaki etkileşimin hangi köprüden geçtiği sorununu doğurur."),
        entry("Hayalet uzuv ve beden birliği", [
            "Descartes insanın bedeninde kaptanın gemide bulunması gibi yalnız gözlemci olmadığını söyler. Açlık, acı ve susuzluk zihin ile bedenin sıkı birleşimini gösterir.",
            "Ayağı kesilen kişinin hayalet ağrı duyması, sinir yollarının zihne yanlış yer bildirimi yapabileceğini gösterir. Duygu gerçek, işaret edilen uzuv yoktur.",
            "Bu örnek duyuların amacı kesin bilim vermek değil bedeni korumak olabilir. Sistem çoğu zaman işe yarar, özel durumda yanılır.",
            "Descartes'ın beden birliği kabulü, kaba 'zihin hayalet, beden makine' özetinden daha karmaşıktır.",
        ], "DÖRDÜNCÜ KISIM · BEDEN VE GÜNÜMÜZ", art="phantom-limb", caption="Hayalet uzuv ağrısı deneyimin gerçekliğiyle onun işaret ettiği beden parçasının doğruluğunu birbirinden ayırır."),
        entry("Şüphe ile komplo arasındaki fark", [
            "Descartes kanıtı güçlendirmek için kendi inançlarını geçici sınar. Komplo düşüncesi ise karşı kanıtı da komplonun parçası sayarak kendini kapatabilir.",
            "Bilimsel şüphe hangi kanıtla fikrini değiştireceğini söyler. Sınırsız kuşku hiçbir cevabı kabul etmez ve araştırmayı durdurur.",
            "Aldatıcı cin internet çağında simülasyon ve sahte görüntü tartışmalarına benzer, fakat Descartes orada yaşamayı amaçlamaz; çıkış arar.",
            "Sağlıklı yöntem şudur: Kaynağı kontrol et, alternatif açıklama kur, doğrulama eşiği belirle ve yeterli kanıtta geçici karar ver.",
        ], "DÖRDÜNCÜ KISIM · BEDEN VE GÜNÜMÜZ", art="open-doubt", caption="Yöntemli şüphe hangi kanıtla duracağını bilir; kapalı komplo her cevabı yeni kuşkuya çevirir."),
        entry("Descartes'ın büyük kazancı", [
            "Kitabın bütün kanıtları ikna etmese bile birinci kişi deneyiminin kesinlik arayışındaki rolünü değiştirdi. Bilginin öznesi modern felsefenin merkezine geldi.",
            "Yöntem, otoriteyi tekrar etmek yerine gerekçeyi kişinin kendi aklında yeniden kurmasını ister. Bu, bilimsel devrim çağının güçlü ruhudur.",
            "Aynı hareket benliği dünyadan fazla ayırma riski taşır. Zihin yalnız içerideki seyirci değil, dil, beden ve başkalarıyla ilişkide gelişir.",
        ], "SON DURAKLAR"),
        entry("Tanrı kanıtı olmadan ne kalır?", [
            "Birçok çağdaş okur Descartes'ın Tanrı kanıtlarını kabul etmez, fakat cogito, rüya savı ve hata analizi önemini korur. Kitabın mimarisinde ise Tanrı çıkarılırsa dış dünya güven zincirinde boşluk oluşur.",
            "Sonraki filozoflar bu boşluğu deneyim, olasılık, dil ve ortak doğrulamayla farklı biçimde doldurmaya çalıştı.",
            "Meditasyonlar bu yüzden bitmiş bina değil, yüzyıllar süren tartışmanın temel kazısıdır.",
        ], "SON DURAKLAR"),
        entry("Gündelik Descartes alıştırması", [
            "Kesin sandığınız bir iddiayı seçin. Bilgi kaynağı ne, hangi koşulda yanılır, hangi kanıt fikrinizi değiştirir? Sonra olgu ile yorumunuzu ayırın.",
            "Her şeyi birden şüpheye atmayın. Yöntemli kuşku sınırlı süre ve amaç taşır; aksi halde karar veremez hale getirir.",
            "Son olarak 'bilmiyorum' alanını işaretleyin. Yargıyı askıya almak, zihnin feneri yetişene kadar iradeyi bekletmektir.",
        ], "SON DURAKLAR"),
        entry("Bir cümlede kitabın özü", [
            "Her inancı şüpheyle söktüğümüzde bile şüphe eden düşüncenin varlığı kalır; Descartes bu ilk taştan Tanrı, dünya ve beden bilgisini yeniden kurmaya çalışır.",
            "Akılda kalacak görüntü eski evdir: Temel sökülür, ilk sağlam taş cogito olur, fakat üst katların bazı bağlantıları hala tartışmalıdır.",
        ], "SON DURAKLAR"),
    ]))


BOOKS.append(base(138, "Bilimsel Devrimlerin Yapısı", "Thomas S. Kuhn",
    "Bilimin yalnız gerçeğe eklenen tuğlalardan değil, ortak örnekler altında çözülen bulmacalardan, büyüyen aykırılıklardan ve dünyayı farklı görmeye başlayan topluluklardan ilerlediğini anlatan paradigma rehberi.",
    "#5C6250", "The Structure of Scientific Revolutions", "bilimsel-devrimlerin-yapisi",
    [
        {"id": 1, "title": "University of Chicago Press - The Structure of Scientific Revolutions", "url": "https://press.uchicago.edu/ucp/books/book/chicago/S/bo13179781.html"},
        {"id": 2, "title": "Stanford Encyclopedia of Philosophy - Thomas Kuhn", "url": "https://plato.stanford.edu/entries/thomas-kuhn/"},
        {"id": 3, "title": "Internet Encyclopedia of Philosophy - Scientific Change", "url": "https://iep.utm.edu/sci-change/"},
        {"id": 4, "title": "Encyclopaedia Britannica - Paradigm shift", "url": "https://www.britannica.com/science/paradigm-shift"},
    ], [
        entry("Bu kitap nasıl okunmalı?", [
            "Kuhn bilimin akıldışı olduğunu söylemez. Bilim insanlarının hangi soruyu önemli, hangi çözümü kabul edilebilir gördüğünü ortak eğitim ve örneklerin şekillendirdiğini anlatır.",
            "Paradigma kelimesi kitapta birden çok anlam taşır. Sonraki baskıda Kuhn bunu disipliner matris ve örnek problem çözümleriyle netleştirmeye çalıştı.",
            "Rehber 'paradigma değişti' sözünü moda sloganından kurtarıp normal bilim, aykırılık, kriz, devrim ve karşılaştırılamazlık zincirine yerleştirecek.",
        ], "BAŞLANGIÇ"),
        entry("Ders kitabındaki düz çizgi", [
            "Bilim ders kitapları geçmişi bugünkü doğruya giden düz yol gibi anlatır. Yanlış teoriler kenarda bırakılır, başarılı sonuçlar sanki aynı hedefe yürüyormuş gibi sıralanır.",
            "Bir şehrin yalnız bugünkü ana caddesini gösterip yıkılan mahalleleri silerseniz geçmiş planlı görünür. Bilim tarihi de kazanan kavramlarla yeniden yazılabilir.",
            "Kuhn eski bilim insanlarını bugünkü sorulara eksik cevap veren kişiler gibi değil, kendi kavramsal dünyalarında çalışan araştırmacılar olarak okumayı önerir.",
            "Tarih böyle bakılınca bilgi birikiminin yanında yön değişimleri ve kopuşlar görünür hale gelir.",
        ], "BİRİNCİ KISIM · NORMAL BİLİM", art="straight-textbook", caption="Ders kitabının düz caddesi bugünkü sonuca uymayan eski yolları silerek bilim tarihini olduğundan pürüzsüz gösterebilir."),
        entry("Paradigma nedir?", [
            "Paradigma bir alandaki bilim insanlarının paylaştığı büyük teori, yöntem, değer ve örnek çözümler bütünüdür. Neyin problem sayılacağını ve iyi cevabın nasıl görüneceğini belirler.",
            "Satranç öğrenen çocuk yalnız kuralları değil usta oyunlarını inceleyerek hangi hamlenin anlamlı olduğunu kavrar. Bilim öğrencisi de örnek problemler çözer.",
            "Newton mekaniği denklem kadar ölçüm alışkanlığı ve kabul edilebilir açıklama biçimi sunar. Aynı veri başka paradigma içinde başka soruya dönüşebilir.",
            "Paradigma göz bağı değildir; verimli araştırma için ortak zemin sağlar. Her gün temeli tartışmak yerine ayrıntılı bulmacalar çözülür.",
        ], "BİRİNCİ KISIM · NORMAL BİLİM", art="shared-puzzle-box", caption="Paradigma bilim topluluğuna hangi parçaların önemli ve tamamlanmış resmin nasıl olması gerektiğini gösteren ortak kutudur."),
        entry("Normal bilim bir bulmaca atölyesi", [
            "Normal bilim büyük teoriyi her deneyde devirmeye çalışmaz. Paradigmanın doğru çalıştığını varsayıp ölçümleri hassaslaştırır, sabitleri bulur ve yeni alanlara uygular.",
            "Sudoku çözerken kuralları sorgulamaz, verilen düzen içinde doğru sayıyı ararsınız. Çözüm çıkmazsa önce kendi hatanızdan şüphe edersiniz.",
            "Bu tutuculuk kötü değildir. Ortak çerçeve olmadan uzun ve ayrıntılı çalışma yapılamaz. Bilimin olağan başarısının büyük kısmı bu sabırlı atölyede doğar.",
            "Fakat aynı bağlılık aykırılıkları uzun süre küçük teknik sorun olarak görmeye de yol açar.",
        ], "BİRİNCİ KISIM · NORMAL BİLİM", art="puzzle-workshop", caption="Normal bilim ortak kuralları devirmekten çok, onların açtığı ayrıntılı ve zor bulmacaları çözerek ilerler."),
        entry("Kuralsız ustalık", [
            "Bilim insanları her karar için açık yöntem kitabı kullanmaz. Eğitimde gördükleri örnekler, benzer yeni durumlarda nasıl davranacaklarını öğretir.",
            "Usta doktor her hastayı tek algoritmayla görmez; yıllar içinde örneklerden oluşan bir sezgi geliştirir. Bu sezgi gizem değil eğitimle biçimlenmiş örüntü tanımadır.",
            "Kuhn bu yüzden bilimi yalnız mantık kuralları listesine indirgemez. Topluluğun paylaştığı uygulama bilgisi önemlidir.",
            "Bunun riski dışarıdan eleştirinin zorlaşmasıdır. Ne sayılacağını bilen içeridekiler aynı zamanda kör noktayı paylaşabilir.",
        ], "BİRİNCİ KISIM · NORMAL BİLİM", art="apprentice-scientist", caption="Bilim çırağı yalnız kural ezberlemez; örnek çözerek topluluğun sessiz problem görme becerisini edinir."),
        entry("Aykırılık: Çekmeceye sığmayan sonuç", [
            "Deney sonucu paradigmanın beklediği yere oturmadığında aykırılık doğar. İlk tepki teoriyi atmak değil cihazı, hesabı veya özel koşulu kontrol etmektir.",
            "Terazi bir gün yanlış gösterirse yerçekimi teorisini değiştirmezsiniz; pili ve zemini incelersiniz. Bu makul direnç bilimi her gürültüde savrulmaktan korur.",
            "Bazı aykırılıklar yıllarca çözülmeden kalabilir. Paradigma başka alanlarda güçlü sonuç veriyorsa topluluk sabreder.",
            "Aykırılığın önemi yalnız büyüklüğüne değil alanın temel beklentisine dokunup dokunmadığına bağlıdır.",
        ], "İKİNCİ KISIM · KRİZİN DOĞUŞU", art="wrong-drawer", caption="Beklenmeyen sonuç önce bozuk terazi gibi incelenir; her aykırılık teoriyi hemen devirecek deprem değildir."),
        entry("Kriz ne zaman başlar?", [
            "Temel aykırılıklar çoğalır, çözüm girişimleri dağılır ve genç araştırmacılar alternatif çerçeveler denerse normal güven gevşer. Alanın kuralları yeniden tartışmaya açılır.",
            "Aynı tamircinin her gün başka parçayı değiştirdiği ama motorun çalışmadığı araçta, sorun tek parça değil model olabilir.",
            "Kriz sırasında farklı okullar ve felsefi tartışmalar artar. Daha önce sessiz kabul edilen kavramlar görünür hale gelir.",
            "Yine de kriz otomatik devrim yaratmaz. Eski paradigma açık kusurlarına rağmen rakipsizse yaşamaya devam edebilir.",
        ], "İKİNCİ KISIM · KRİZİN DOĞUŞU", art="failing-engine", caption="Tek tek onarımlar temel arızayı çözmeyince araştırmacılar parçadan önce motor modelini tartışmaya başlar."),
        entry("Kopernik göğü neden hareket ettirdi?", [
            "Batlamyus sistemi gezegen konumlarını karmaşık ek dairelerle açıklıyordu. Kopernik Güneş merkezli düzen önerdi, fakat ilk hesapları her bakımdan hemen daha doğru ve kolay değildi.",
            "Mobilyaları taşımak yerine odanın merkezini değiştirmek gibi, Dünya gözlemci tahtından bir gezegene dönüştü. Aynı gökyüzü yeni ilişkilerle görüldü.",
            "Kepler'in elipsleri, Galileo'nun gözlemleri ve Newton'un mekaniği yeni sistemin gücünü zamanla büyüttü. Devrim tek gecelik fikir değil kuşaklar süren yeniden kurmadır.",
            "Kuhn için yeni paradigma yalnız eski veriye başka cevap vermez; hangi verinin önemli olduğunu da değiştirir.",
        ], "İKİNCİ KISIM · KRİZİN DOĞUŞU", art="moving-center", caption="Kopernik aynı gökyüzündeki mobilyaları değil, odanın merkezini değiştirerek Dünya'nın yerini yeniden tanımladı."),
        entry("Oksijen mi, filojiston mu?", [
            "Yanma eskiden maddeden filojiston adlı ilkenin çıkmasıyla açıklanıyordu. Lavoisier ölçüm ve yeni kavramlarla yanmayı oksijenle birleşme olarak yeniden kurdu.",
            "Bir muhasebeci eksilen para ararken diğeri ağırlığın arttığını fark eder. Ne ölçtüğünüz, olayın hikayesini değiştirir.",
            "Yeni dil element, bileşik ve kütle hesabını farklı düzenledi. Eski kelimeleri yeni sözlükte bire bir çevirmek zorlaştı.",
            "Devrim yalnız yeni madde keşfi değil kimyasal dünyanın sınıflandırılma biçimindeki dönüşümdü.",
        ], "İKİNCİ KISIM · KRİZİN DOĞUŞU", art="burning-scale", caption="Yanma olayı aynı kalırken ölçüm ve kavram düzeni değişti; çıkan öz yerine oksijenle birleşme görüldü."),
        entry("Yeni paradigma nasıl seçilir?", [
            "Rakip paradigmaları tek bir tarafsız kural hemen sıralamayabilir. Doğruluk, kapsam, sadelik, verimlilik ve yeni problem açma gücü birlikte değerlendirilir.",
            "İki şehir planından biri bugünkü trafiği iyi çözer, diğeri gelecekte büyümeye alan açar. Hangi değere ne ağırlık verileceği bilim insanları arasında değişebilir.",
            "Kuhn seçimde ikna, örnek başarı ve topluluk güveninin rolünü vurgular. Bu, kanıtın önemsiz olduğu anlamına gelmez; kanıt değerlerle yorumlanır.",
            "Yeni paradigma yeterli sayıda araştırmacıya çözebileceği verimli bulmacalar gösterdiğinde devrim kök salar.",
        ], "ÜÇÜNCÜ KISIM · DEVRİM", art="two-city-plans", caption="Rakip paradigmalar doğruluk yanında kapsam, sadelik ve gelecekte açtıkları araştırma yollarıyla karşılaştırılır."),
        entry("Dünya değişti mi, bakış mı?", [
            "Devrim sonrası bilim insanı aynı laboratuvarda çalışır, fakat nesneleri başka ilişkiler içinde görür. Kuhn bunu ördek-tavşan gibi algı değişimine benzetir.",
            "Gökyüzündeki parlak nokta bir paradigma içinde gezegen, diğerinde farklı hareket düzeninin üyesidir. Veri tamamen çıplak gelmez.",
            "Kuhn dış dünyanın zihne göre sihirle değiştiğini söylemez. Gözlem dili, araç ve beklentinin dünyayı nasıl parçaladığını vurgular.",
            "Bu ifade en çok yanlış anlaşılan yerdir. Bilim insanı keyfine göre gerçeklik yaratmaz; farklı çerçeve aynı direnen dünyayla başka deneyler kurar.",
        ], "ÜÇÜNCÜ KISIM · DEVRİM", art="duck-rabbit", caption="Aynı çizgiler ördek veya tavşan olarak örgütlenebilir; paradigma verinin hangi nesne olarak görüldüğünü etkiler."),
        entry("Karşılaştırılamazlık ne demek?", [
            "Rakip paradigmalar bazı temel terimleri farklı anlamda kullanır, farklı sorunları önemli sayar ve farklı ölçüler uygular. Tam ortak cetvel bulmak güçleşir.",
            "Farklı para birimleri yalnız kurla değil, alınabilen mallarla da değişiyorsa tek sayı karşılaştırmayı bitirmez. Çeviri mümkündür ama kayıpsız olmayabilir.",
            "Karşılaştırılamazlık iletişimin imkansızlığı veya her görüşün eşitliği değildir. Bilim insanları kanıt sunar, fakat tartışma bütünüyle nötr dilde yapılmaz.",
            "Kuhn sonraki yazılarında kavramı daha sınırlı, yerel anlam farklılıkları olarak netleştirdi.",
        ], "ÜÇÜNCÜ KISIM · DEVRİM", art="different-rulers", caption="Rakip paradigmalar farklı cetveller kullandığında karşılaştırma sona ermez, fakat tek ölçü bütün farkı kapatmaz."),
        entry("Bilim insanları neden direnç gösterir?", [
            "Eski paradigmaya bağlılık yalnız yaşlıların inadı değildir. Araştırmacı yıllarca araç, dil ve başarı biriktirmiştir; yeni çerçevenin henüz çözemediği sorunları görür.",
            "Usta haritacıya bütün koordinat sistemini değiştir dediğinizde geçmiş işinin çevrilebilmesi gerekir. Geçiş gerçek maliyet taşır.",
            "Direnç yeni fikrin ciddi sınanmasını sağlar. Her yenilik alkışlansaydı bilim moda akımlarına dağılırdı.",
            "Fakat kuşak değişimi bazen dönüşümü hızlandırır; gençler eski yatırımın yükünü daha az taşır ve yeni bulmacalarda yetişir.",
        ], "ÜÇÜNCÜ KISIM · DEVRİM", art="old-map-new-grid", caption="Eski haritada ustalaşmış araştırmacı için yeni koordinat sistemi yalnız fikir değil, bütün mesleki yatırımın dönüşümüdür."),
        entry("Ders kitapları devrimi nasıl gizler?", [
            "Yeni paradigma yerleşince ders kitapları alanı baştan yazar. Eski bilim insanları bugünkü kavramların erken ve eksik kullanıcıları gibi gösterilir.",
            "Kazanan takım sezon özetini yalnız golleriyle hazırlarsa tereddütler ve kaybedilen maçlar görünmez. Sonuç kaçınılmaz sanılır.",
            "Bu yeniden yazım eğitim için verimlidir; öğrenci her tarihsel çıkmazı tekrar yaşamaz. Fakat bilimin insan, tartışmalı ve değişebilir yönünü saklar.",
            "Kuhn'un kitabı ders kitabının arka odasını açar. Bilim gücünü hatasızlıktan değil hatalarla kurumsal biçimde uğraşabilmesinden alır.",
        ], "DÖRDÜNCÜ KISIM · YANLIŞ OKUMALAR", art="rewritten-history", caption="Yeni ders kitabı zafer yolunu düzleştirirken devrimin tereddütlerini, çıkmazlarını ve alternatiflerini arka odada bırakır."),
        entry("Paradigma her fikir değişimi değildir", [
            "Bir şirketin logosunu yenilemesi veya kişinin kahve markasını değiştirmesi paradigma devrimi değildir. Kavram, alanın temel problem, yöntem ve örnek düzeninin dönüşümünü anlatır.",
            "Moda dilde kelime etkileyici değişimin eş anlamına dönüştü. Bu kullanım kitabın aykırılık, kriz ve topluluk boyutunu siler.",
            "Gerçek kontrol sorusu şudur: Yeni görüş yalnız cevabı mı değiştirdi, yoksa hangi sorunun anlamlı ve hangi kanıtın geçerli olduğunu da mı?",
            "Kavramı dar tutmak onun açıklama gücünü korur.",
        ], "DÖRDÜNCÜ KISIM · YANLIŞ OKUMALAR", art="not-every-change", caption="Yeni renk veya slogan değil, bir alanın soru ve kanıt düzeninin dönüşmesi paradigma değişimidir."),
        entry("Kuhn relativist miydi?", [
            "Eleştirmenler paradigmalar arasında tarafsız ölçü yoksa bilimin ilerlemesinin yalnız kalabalık tercihi olacağını söyledi. Kuhn bunu reddetti.",
            "Yeni teoriler genellikle daha çok ve daha hassas problem çözer. İlerleme vardır; fakat tek, tarihten bağımsız doğruya ne kadar yaklaşıldığını ölçen cetvel yoktur.",
            "Darwinci benzetmeyle bilimsel gelişim bir hedefe önceden çizilmiş yürüyüşten çok çevrede daha iyi problem çözen dalların seçilmesine benzer.",
            "Bu yaklaşım gerçekliğin önemsizliği değil, ilerleme dilinin daha alçakgönüllü kurulmasıdır.",
        ], "DÖRDÜNCÜ KISIM · YANLIŞ OKUMALAR", art="branching-progress", caption="Bilim önceden çizilmiş tek merdiven yerine daha çok problem çözen dalların seçildiği bir gelişim ağacı olabilir."),
        entry("Devrim dışında birikim yok mu?", [
            "Kuhn'un çarpıcı devrim anlatısı normal bilimin büyük birikimini gölgede bırakabilir. Ölçüm hassasiyeti, araç ve veri kuşaklar boyunca gerçekten birikir.",
            "Ayrıca bilimler aynı ölçüde paradigma yapısına sahip olmayabilir. Fizik tarihinden çıkarılan model biyoloji, tıp veya sosyal bilimlere aynen uymayabilir.",
            "Kitap en iyi bütün bilimlerin yasası değil, bilimsel değişimin ihmal edilen topluluk ve tarih boyutunu gösteren güçlü model olarak okunur.",
        ], "SON DURAKLAR", art="revolution-and-accumulation", caption="Bilimsel gelişim devrimlerle yön değiştirirken normal bilimin ölçü, araç ve veri birikimini de yanında taşır."),
        entry("Bilim ve toplum", [
            "Kuhn topluluğun rolünü gösterdi diye sonuçların siyasi oylamayla belirlendiğini söylemez. Dünya deneyde direnç gösterir, cihazlar sonuç üretir ve tahminler başarısız olabilir.",
            "Yine de fon, kurum, eğitim ve itibar hangi problemlerin çalışılacağını etkiler. Bilim toplumsal kurumdur; bu onu otomatik olarak güvenilmez yapmaz.",
            "Daha iyi bilim, bu etkileri gizlemek yerine yöntem, veri ve eleştiri kanallarını görünür kılar.",
        ], "SON DURAKLAR"),
        entry("Bir aykırılığı nasıl düşünmeli?", [
            "Beklenmeyen sonuç gördüğünüzde hemen devrim ilan etmeyin. Önce ölçümü, tekrarı ve alternatif açıklamayı kontrol edin. Sonucun paradigmanın temel noktasına dokunup dokunmadığını sorun.",
            "Aynı zamanda sırf çerçeve başarılı diye aykırılığı sonsuza dek çekmeceye atmayın. Hangi koşulda kriz sayılacağını önceden belirtmek dürüstlüktür.",
            "Kuhn'un dengesi budur: Bilim hem çerçeveye sadakat hem gerektiğinde çerçeveyi değiştirme kapasitesiyle çalışır.",
        ], "SON DURAKLAR"),
        entry("Bir cümlede kitabın özü", [
            "Bilim çoğu zaman ortak paradigma içinde bulmaca çözer; temel aykırılıklar krize dönüştüğünde yeni paradigma yalnız cevapları değil, soruları ve dünyayı görme biçimini de değiştirir.",
            "Akılda kalacak görüntü ördek-tavşandır: Çizgiler aynı kalır, fakat topluluk yeni düzeni gördüğünde eski görüntüye basitçe bir parça eklenmiş olmaz.",
        ], "SON DURAKLAR"),
    ]))


if __name__ == "__main__":
    write_books(BOOKS)
