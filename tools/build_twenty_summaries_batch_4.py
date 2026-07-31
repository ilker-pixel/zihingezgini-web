#!/usr/bin/env python3
"""Build the final five summaries in the twenty-book collection."""

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


BOOKS.append(base(216, "İkinci Cins", "Simone de Beauvoir",
    "Kadının değişmez bir özle doğmadığını; biyoloji, tarih, efsane, çocukluk, aşk, evlilik, iş ve yaşlılık içinde 'öteki' konumuna getirildiğini gösteren büyük feminist klasiğin sade ve eleştirel rehberi.",
    "#795160", "Le Deuxième Sexe", "ikinci-cins",
    [
        {"id": 1, "title": "Encyclopaedia Britannica - The Second Sex", "url": "https://www.britannica.com/topic/The-Second-Sex"},
        {"id": 2, "title": "Stanford Encyclopedia of Philosophy - Simone de Beauvoir", "url": "https://plato.stanford.edu/entries/beauvoir/"},
        {"id": 3, "title": "Internet Encyclopedia of Philosophy - Beauvoir", "url": "https://iep.utm.edu/simone-de-beauvoir/"},
        {"id": 4, "title": "Penguin Random House - The Second Sex", "url": "https://www.penguinrandomhouse.com/books/10350/the-second-sex-by-simone-de-beauvoir/"},
    ], [
        entry("Bu kitap nasıl okunmalı?", [
            "İkinci Cins iki büyük ciltte biyoloji, tarih ve mitlerden çocukluk, evlilik, annelik, iş ve bağımsızlığa uzanır. Tek slogan değil geniş bir soruşturmadır.",
            "Beauvoir 1949 Fransasının dilini ve sınırlı kaynaklarını taşır. Trans deneyimleri, ırk ve sömürge bağları ile farklı aile biçimleri bugünkü tartışmalarda daha geniş düşünülür.",
            "Rehber 'kadın doğulmaz, kadın olunur' cümlesini biyolojinin yokluğu değil, biyolojik farkın toplumsal yazgıya nasıl çevrildiği olarak açacak.",
        ], "BAŞLANGIÇ"),
        entry("Kadın neden ikinci sayılır?", [
            "Erkek kendini tarafsız insan, kadını ise özel ve farklı cins olarak tanımlar. Erkek özne, kadın öteki olur. Cetvelin kendisi görünmez, ölçülen kişi sapma sayılır.",
            "Toplantıda erkek yönetici yalnız yönetici, kadın yönetici 'kadın yönetici' diye anılıyorsa varsayılan insanın kim olduğu ortaya çıkar.",
            "Ötekilik her farkın doğal sonucu değildir. İki grup birbirini farklı görebilir; sorun bir tarafın evrensel merkez ve güç sahibi olmasıdır.",
            "Kitap kadının deneyimini merkeze alarak insan kelimesinin gizli erkek ölçüsünü görünür yapar.",
        ], "BİRİNCİ KISIM · ÖTEKİ NASIL KURULUR", art="default-human", caption="Erkek tarafsız insan, kadın özel durum sayıldığında görünmez cetvel toplumsal merkezi belirler."),
        entry("Biyoloji kader değildir", [
            "Beden gerçektir: Üreme, adet, gebelik ve fiziksel farklar yaşamı etkiler. Beauvoir bunların tek başına toplumsal rolü zorunlu kılmadığını savunur.",
            "Gebelik kapasitesi bir kadının anne olmasını, bütün bakımı üstlenmesini veya işten çekilmesini mantıksal olarak belirlemez. Kurumlar kapasiteyi yazgıya çevirir.",
            "Beden yalnız makine değil yaşanan bedendir. Aynı fiziksel durum eğitim, gelir, sağlık hizmeti ve kişisel projeye göre başka anlam taşır.",
            "Biyolojiyi yok saymak kadar onu kaçınılmaz kader yapmak da insan özgürlüğünü eksiltir.",
        ], "BİRİNCİ KISIM · ÖTEKİ NASIL KURULUR", art="body-not-destiny", caption="Biyolojik kapasite gerçek olsa da hangi hayat rolüne dönüşeceğini kurum, imkan ve kişisel proje belirler."),
        entry("Tarih kimin elindeydi?", [
            "Beauvoir mülkiyet, miras, savaş ve üretim düzenlerinin erkek gücünü nasıl kalıcılaştırdığını inceler. Ekonomik bağımlılık ötekiliği günlük hayata bağlar.",
            "Evi ve toprağı adına kaydedemeyen, ücret kazanamayan kişi kötü ilişkiye hayır deme gücünü kağıt üzerinde taşısa da kullanamayabilir.",
            "Tarih tek nedenle açıklanmaz. Teknoloji, sınıf, din ve hukuk birlikte çalışır; kadınlar yalnız pasif kurban değildir.",
            "Temel ders, gelenek diye görünen düzenin yapılmış ve bu nedenle değiştirilebilir olduğudur.",
        ], "BİRİNCİ KISIM · ÖTEKİ NASIL KURULUR", art="property-keys", caption="Mülkiyet ve gelir anahtarları kimdeyse aile ve toplum içindeki hayır deme gücü de orada yoğunlaşabilir."),
        entry("Efsanelerde kadın", [
            "Kadın edebiyat ve dinde aynı anda anne, bakire, şeytan, doğa, ilham ve bilinmez olarak resmedilir. Gerçek kişi çelişkili simgelerin altında kaybolur.",
            "Bir çalışanı 'ofisin annesi' diye övmek sıcak görünür, fakat ondan görünmez bakım bekleyip yetkisini azaltabilir.",
            "Efsane erkeğin korku ve arzusunu kadının özü gibi dışarı yansıtır. Kadın konuşan özne değil anlam taşıyan ekran olur.",
            "Beauvoir tek tek erkekleri suçlamaktan çok kültürel resmin nasıl tekrarlandığını çözer.",
        ], "BİRİNCİ KISIM · ÖTEKİ NASIL KURULUR", art="myth-screen", caption="Anne, melek veya şeytan efsaneleri gerçek kadını konuşan özne yerine başkasının arzusunu taşıyan ekrana çevirebilir."),
        entry("Kız çocuk olmayı öğrenmek", [
            "Küçük çocuk başta dünyaya bedeniyle uzanır. Zamanla kıza dikkatli, güzel, uslu ve bakılan olması; oğlana hareket, risk ve özne olma öğretilir.",
            "Biri ağaca tırmanınca cesur, diğeri eteğin kirlenir diye indirilirse kas kadar imkan duygusu da farklı gelişir.",
            "Oyuncak, kıyafet ve yetişkin tepkisi gelecekteki rolün provasını yapar. Çocuk yalnız emri değil kendisine bakan gözün beklentisini içselleştirir.",
            "Bu süreç mutlak değildir. Çocuklar direnir, aileler değişir ve aynı kültürde farklı deneyimler oluşur.",
        ], "İKİNCİ KISIM · KADIN OLMAK", art="tree-climbing", caption="Aynı ağaca uzanan çocuklara farklı cesaret ve görünüş kuralları verildiğinde imkan duyguları da ayrışır."),
        entry("Genç kız ve ayna", [
            "Ergenlikle kız kendi bedenini yaşayan araç kadar başkalarının baktığı nesne olarak görmeye başlayabilir. Ayna dış bakışın içeri taşındığı yere dönüşür.",
            "Koşarken güçlü hisseden beden, fotoğrafta nasıl göründüğü sorusuyla hareketini kısabilir. Özne ile görüntü arasında gerilim oluşur.",
            "Güzellik zevki başlı başına baskı değildir. Değerin tek kapısı olduğunda kişi zaman ve güvenliğini sürekli değerlendirmeye verir.",
            "Beauvoir'ın analizi bugün sosyal medya filtresi ve beğeni ekonomisinde yeni yoğunluk kazanır.",
        ], "İKİNCİ KISIM · KADIN OLMAK", art="girl-and-mirror", caption="Ayna bedeni yaşamaktan başkalarının gözünde nasıl göründüğünü denetlemeye geçişin simgesi olabilir."),
        entry("Aşkta kendini kaybetmek", [
            "Kendi projesi ve ekonomik alanı daraltılan kadın, sevgiliyi hayatının mutlak merkezi yapabilir. Kendi geleceğini onun bakışında arar.",
            "Bütün yatırımı tek hisseye koymak gibi, benliğin tamamını ilişkiye vermek sevgiyi ağır bir bağımlılığa çevirir.",
            "Beauvoir sevgiyi reddetmez. İki özgür öznenin birbirini amaçlarına dahil ettiği karşılıklı aşkı mümkün görür.",
            "Sorun 'sensiz hiçim' romantizminin eşitsizliği güzelleştirmesidir. Sevgi iki hayatı büyütmeli, birini ötekinde eritmemelidir.",
        ], "İKİNCİ KISIM · KADIN OLMAK", art="love-orbit", caption="Bir kişi kendi merkezini kaybedip tamamen sevgilinin yörüngesine girerse aşk karşılıklılıktan bağımlılığa dönebilir."),
        entry("Evlilikte görünmeyen emek", [
            "Ev işi her gün tekrar eder ve kalıcı ürün bırakmaz. Temizlenen oda yeniden kirlenir, hazırlanan yemek yenir; emek görünmezleşir.",
            "Fabrikada ürün sayılır, evde düzen doğal hal sanılır. İşi yapan kişi dinlenmek için evden çıkamaz; evi aynı zamanda çalışma yeridir.",
            "Ekonomik bağımlılık ve toplumsal beklenti evliliği eşit ortaklık yerine hizmet düzenine çevirebilir.",
            "Bugün ücretli çalışma artsa da bakım yükünün paylaşımı temel soru olarak sürer. Sevgi emeği otomatik ve sınırsız yapmaz.",
        ], "İKİNCİ KISIM · KADIN OLMAK", art="invisible-housework", caption="Her gün yeniden başlayan ev işi ürünü hemen tüketildiği için doğal düzen sanılır ve emeği görünmez kalır."),
        entry("Annelik tek duygu değildir", [
            "Beauvoir anneliği kutsal ve otomatik mutluluk efsanesinden çıkarır. Sevgi, yorgunluk, kaygı, güç ve pişmanlık aynı deneyimde bulunabilir.",
            "Toplum bütün anlamı anneliğe yükleyip destek sağlamazsa kadın hem idealin altında ezilir hem zor duygularını söyleyemez.",
            "Çocuk annenin mülkü veya tamamlanma aracı değildir. İki ayrı özgürlük zamanla birbirinden ayrılır.",
            "Üreme hakkı yalnız çocuk sahibi olma değil, olmama ve bakım için toplumsal destek hakkını da içerir.",
        ], "İKİNCİ KISIM · KADIN OLMAK", art="complex-motherhood", caption="Annelik tek renkli kutsal resim değil sevgi, yorgunluk, korku ve ayrışmanın birlikte yaşandığı karmaşık ilişkidir."),
        entry("Fahişe ve namuslu kadın ayrımı", [
            "Toplum erkek cinselliğini hoş görürken kadını namus ve damga arasında sınıflandırabilir. Aynı düzen talebi üretir, hizmeti satanı dışlar.",
            "Bir kapıdan gizlice giren müşteri, çıkınca içerideki kadını ahlaksız ilan edebilir. Çifte standart gücü görünmez kılar.",
            "Beauvoir ekonomik zorunluluk ve bedenin metalaşmasını inceler. Bugünkü seks işçiliği tartışmaları rıza, şiddet ve haklar konusunda daha çeşitli görüşler taşır.",
            "Yargıyı yalnız kadına yöneltmek onu çevreleyen piyasa ve erkek talebini saklar.",
        ], "ÜÇÜNCÜ KISIM · ÇIKIŞ YOLLARI", art="double-standard", caption="Aynı cinsel düzen erkeğin talebini görünmez, kadının bedenini damgalı hale getirerek çifte standart kurabilir."),
        entry("Narsist ve mistik kaçış", [
            "Dış dünyada eylem alanı bulamayan kişi kendi görüntüsünü, hayali sevgiyi veya mutlak manevi birleşmeyi tek anlam kaynağı yapabilir.",
            "Kapıları kapalı evde aynayı büyütmek alanı genişletmez. Benlik sürekli kendine bakarken dünya ile proje kurma gücünü kaybeder.",
            "Beauvoir bu tipleri kadın doğası değil kısıtlanmış koşullara verilen yollar olarak anlatır.",
            "Çözüm kişiyi küçümsemek değil eğitim, iş ve ortak eylem kapılarını açmaktır.",
        ], "ÜÇÜNCÜ KISIM · ÇIKIŞ YOLLARI", art="mirror-room", caption="Dış dünyaya kapılar kapanınca büyüyen ayna benliği meşgul eder, fakat gerçek eylem alanını genişletmez."),
        entry("Çalışmak neden yetmez ama gereklidir?", [
            "Ücretli iş kadına ekonomik bağımsızlık ve ortak dünyada proje kurma imkanı verir. Kötü ilişkiden çıkış ve söz hakkı için maddi zemin sağlar.",
            "Kendi anahtarını ve gelirini taşımak seçim alanını büyütür. Fakat düşük ücret ve evde ikinci vardiya özgürlüğü eksik bırakabilir.",
            "İş piyasası erkek ölçüsünde kurulmuşsa katılmak eşitlik sağlamaz. Bakım hizmeti, eşit ücret ve tacizden korunma gerekir.",
            "Beauvoir özgürlüğü yalnız iş sahibi olmak değil kendi geleceğine etkili biçimde yön vermek olarak görür.",
        ], "ÜÇÜNCÜ KISIM · ÇIKIŞ YOLLARI", art="own-key", caption="Kendi geliri ve anahtarı seçim alanını açar; eşitlik için işyerinin ve bakım düzeninin de değişmesi gerekir."),
        entry("İçkinlik ve aşkınlık", [
            "İçkinlik insanı tekrar, kapanma ve verilmiş durum içinde tutar. Aşkınlık geleceğe proje kurma, dünyayı değiştirme ve kendini aşma hareketidir.",
            "Ev işi yalnız döngüye hapsolduğunda içkinlik, yeni beceri ve ortak karar alanı açıldığında aşkınlık imkanı doğar.",
            "Her insan iki yönü de yaşar; yemek, uyku ve bakım olmadan proje olmaz. Sorun bir cinsin sürekli tekrar işine, diğerinin kamusal yaratmaya ayrılmasıdır.",
            "Özgürlük bedensiz uçuş değil, somut koşullar içinden imkan açmaktır.",
        ], "ÜÇÜNCÜ KISIM · ÇIKIŞ YOLLARI", art="repetition-and-project", caption="Yaşam tekrar eden bakım ile geleceğe açılan proje arasında akar; eşitsizlik bir cinsi tek tarafa hapseder."),
        entry("Karşılıklı özgürlük", [
            "Beauvoir'ın hedefi kadınların erkeklere dönüşmesi veya cinsiyet farkının silinmesi değildir. Her kişinin hem özne hem başkasına açık varlık olarak tanınmasıdır.",
            "İki müzisyen biri yalnız eşlikçi kalmadan birbirinin melodisine cevap verdiğinde ortak eser oluşur.",
            "Özgürlük tek başına sahip olunan eşya değil başkasının özgürlüğüyle güçlenen ilişkidir. Baskı kuran kişi kendini de efendi rolüne hapseder.",
            "Eşitlik aynı hayatı zorlamak değil imkan ve söz hakkını cinsiyetten bağımsızlaştırmaktır.",
        ], "ÜÇÜNCÜ KISIM · ÇIKIŞ YOLLARI", art="two-musicians", caption="Karşılıklı özgürlük birinin sürekli eşlikçi olmadığı, iki öznenin ortak melodiyi birlikte kurduğu ilişkidir."),
        entry("Sınıf, ırk ve sömürge", [
            "Beauvoir kadınları tek deneyim altında birleştirirken beyaz, eğitimli Fransız kadının konumunu sık sık merkez alır. Yoksulluk, ırkçılık ve sömürgecilik cinsiyetle kesişir.",
            "Aynı işyerinde yönetici kadın ile göçmen temizlik işçisinin baskısı ve imkanı aynı değildir. Ortak cinsiyet farklı güç konumlarını silmez.",
            "Sonraki feminist düşünce kesişimsellik kavramıyla bu katmanları daha sistemli ele aldı.",
            "Kitabı geliştirmek ana tezini terk etmek değil, 'hangi kadın?' sorusunu her bölümde sormaktır.",
        ], "DÖRDÜNCÜ KISIM · BUGÜNKÜ SINAMA", art="intersecting-roads", caption="Cinsiyet yolu sınıf, ırk ve göç yollarıyla kesişir; herkes aynı kavşaktan aynı imkanla geçmez."),
        entry("Trans deneyimi ve 'olmak'", [
            "Beauvoir cinsiyetin toplumsal oluşunu güçlü biçimde gösterir, fakat trans kimlikleri bugünkü kavramlarla ayrıntılı incelemez. Metni doğrudan destek veya ret sloganına çevirmek anakronik olur.",
            "Beden, kimlik, toplumsal tanınma ve kişisel özgürlük arasındaki ilişki kitabın açtığı ama tamamlamadığı alandır.",
            "Bugünkü okuma trans kişilerin kendi deneyim ve hak sözünü merkeze almalı, 1949 kavramlarını son sınır saymamalıdır.",
            "'Olunur' sözü basit keyfi seçim değil, beden ve toplum içinde süren karmaşık oluşu anlatır.",
        ], "DÖRDÜNCÜ KISIM · BUGÜNKÜ SINAMA", art="identity-path", caption="Cinsiyet oluşu tek anlık seçim değil beden, toplumsal tanınma ve kişisel hayatın kesiştiği uzun bir yoldur."),
        entry("Güzellik ekonomisi bugün", [
            "Filtre, estetik işlem ve influencer pazarı bedeni sürekli geliştirilecek proje olarak satar. Seçim özgürlüğü ile görünmez zorunluluk birbirine karışır.",
            "Herkes aynı yüz ölçüsüne yaklaşmaya çalışıyorsa bireysel seçimlerin arkasında güçlü ortak pazar vardır.",
            "Kişinin süslenmeden zevk alması küçümsenmemelidir. Soru maliyet, ceza ve değer ölçüsüdür: Yapmayan ne kaybediyor?",
            "Beauvoir'ın ayna analizi artık algoritmik ve ticari bir odaya taşınmıştır.",
        ], "DÖRDÜNCÜ KISIM · BUGÜNKÜ SINAMA"),
        entry("Kitabın dili ve çeviri sorunu", [
            "İlk İngilizce çeviri metni ciddi biçimde kısaltıp bazı felsefi kavramları bozdu. Yeni tam çeviri kitabın kapsamını daha doğru gösterdi.",
            "Bir düşünürün dünya çapındaki ünü bazen eksik metin üzerinden kurulur. Çevirmen görünmez değildir; kavramın kapısını seçer.",
            "Türkçe baskılarda da terim ve tamlık farkına dikkat etmek gerekir. Uzun özet özgün metnin ritmini ve kanıtını tamamen taşıyamaz.",
        ], "SON DURAKLAR"),
        entry("Beauvoir'ın kör noktaları", [
            "Bazı biyoloji ve psikanaliz değerlendirmeleri eskimiştir. Annelik ve yaşlılık anlatısı zaman zaman karamsar ve genelleyicidir.",
            "Kadınların kültürel farklarını tek çizgide anlatmak, Batılı deneyimi evrensel kılabilir. Lezbiyenlik bölümü de bugünün diliyle sorunlu yerler taşır.",
            "Büyük eser olmak eleştiriden muaf olmak değildir. Kalıcı gücü, bütün cevaplarında değil kadınlığın doğal yazgı sanılmasına açtığı gediktedir.",
        ], "SON DURAKLAR"),
        entry("Gündelik hayatta görünmez cetvel", [
            "Bir hafta boyunca 'normal' sayılan kişiyi izleyin. Toplantı saati kimin bakım yüküne göre, iş kıyafeti hangi bedene göre, güvenlik tavsiyesi kimin hareketini kısıtlıyor?",
            "Sonra görünmez emeği yazın: Kim hatırlatıyor, temizliyor, duyguyu yatıştırıyor ve bunun karşılığını alıyor?",
            "Cetvel görünür olduğunda kişisel yetersizlik gibi yaşanan şeyin kurumsal tarafı anlaşılır.",
        ], "SON DURAKLAR"),
        entry("Bir cümlede kitabın özü", [
            "Kadınlık biyolojiden çıkan hazır kader değil, erkeği varsayılan özne yapan tarih, efsane, eğitim ve ekonomik bağımlılık içinde kurulur; özgürlük bu koşulları karşılıklı öznelik yönünde değiştirmektir.",
            "Akılda kalacak görüntü görünmez cetveldir: Ölçünün kendisi erkek olduğunda kadın sürekli eksik veya fazla görünür.",
        ], "SON DURAKLAR"),
    ]))


BOOKS.append(base(238, "Hapishanenin Doğuşu", "Michel Foucault",
    "Meydandaki işkenceden gözetlenen hücreye geçişi basit insanileşme hikayesi olarak değil, bedeni daha yararlı ve uysal kılan yeni bir iktidar teknolojisinin doğuşu olarak okuyan çarpıcı rehber.",
    "#4E6062", "Surveiller et punir: Naissance de la prison", "hapishanenin-dogusu",
    [
        {"id": 1, "title": "Penguin Random House - Discipline and Punish", "url": "https://www.penguinrandomhouse.com/books/55026/discipline-and-punish-by-michel-foucault-and-alan-sheridan/"},
        {"id": 2, "title": "Stanford Encyclopedia of Philosophy - Michel Foucault", "url": "https://plato.stanford.edu/entries/foucault/"},
        {"id": 3, "title": "Internet Encyclopedia of Philosophy - Foucault", "url": "https://iep.utm.edu/foucault/"},
        {"id": 4, "title": "Foucault.info - Panopticism", "url": "https://foucault.info/documents/foucault.disciplineAndPunish.panOpticism/"},
    ], [
        entry("Bu kitap nasıl okunmalı?", [
            "Foucault hapishanenin iyi mi kötü mü olduğunu tek ahlaki cümleyle tartışmaz. Ceza biçimlerinin hangi bilgi, kurum ve beden teknikleriyle mümkün olduğunu tarihsel olarak inceler.",
            "Panoptikon kitabın ünlü ama tek konusu değildir. İşkence, reform, asker, okul, sınav, normalleştirme ve hapishanenin başarısızlığı aynı zincirdedir.",
            "Rehber iktidarı yalnız kötü hükümdar iradesi saymayacak; gündelik düzeneklerde çalışan, üretken ve karşı konabilir ilişkiler olarak açıklayacak.",
        ], "BAŞLANGIÇ"),
        entry("Damiens'in parçalanan bedeni", [
            "Kitap 1757'de kralı öldürmeye teşebbüs eden Damiens'in halka açık, ayrıntılı işkencesiyle başlar. Ceza hükümranın yaralanmış gücünü suçlunun bedeninde gösterir.",
            "Meydan tiyatrosunda acı yalnız suçluya verilmez; halka kralın üstünlüğü seyrettirilir. Beden siyasi mesaj panosudur.",
            "Fakat gösteri ters tepebilir. Kalabalık mahkuma acır, cellada öfkelenir veya isyana dönüşür. Hükümdarın zafer sahnesi denetimsizdir.",
            "Foucault bu sert açılışı modern cezanın görünmezliğini karşılaştırmak için kullanır.",
        ], "BİRİNCİ KISIM · BEDENDEN RUHA", art="public-execution", caption="Halka açık işkence suçlunun bedeninde hükümdarın yaralanmış gücünü yeniden sahneleyen siyasi tiyatrodur."),
        entry("Seksen yıl sonra sessiz çizelge", [
            "Kitabın ikinci belgesi genç mahkumların gününü dakika dakika düzenleyen cezaevi programıdır. Uyanma, çalışma, dua ve yemek sessiz kurala bağlanır.",
            "Kanlı meydandan çizelgeye geçiş daha yumuşak görünür. Fakat iktidar yok olmamış, bedeni sürekli işleyen ayrıntılı düzene dönüşmüştür.",
            "Bir kez döven güç yerine her gün oturuşu, zamanı ve alışkanlığı biçimlendiren güç gelir.",
            "Foucault'nun sorusu 'ceza insancıl oldu mu?' kadar 'hangi yeni denetim daha etkili hale geldi?' sorusudur.",
        ], "BİRİNCİ KISIM · BEDENDEN RUHA", art="prison-timetable", caption="Meydandaki tek büyük şiddetin yerini mahkumun her dakikasını biçimlendiren sessiz ceza çizelgesi alır."),
        entry("Suçtan suçlu ruha", [
            "Eski ceza belirli eyleme karşılık verirken modern mahkeme kişinin karakteri, geçmişi, tehlikeliliği ve düzeltilebilirliğini de yargılar.",
            "'Ne yaptı?' sorusuna psikiyatrist, sosyal hizmet ve kriminoloji 'nasıl biri?' sorusunu ekler. Ceza ruhun bilimine açılır.",
            "Bu bilgi daha uygun karar sağlayabilir, fakat cezanın sınırını belirsizleştirir. Gelecekte tehlikeli olma ihtimali bugünkü yaptırımı uzatabilir.",
            "Foucault suçlu kimliğinin hukuk ile uzman bilginin ortak ürünü olduğunu gösterir.",
        ], "BİRİNCİ KISIM · BEDENDEN RUHA", art="judged-soul", caption="Modern ceza yalnız eylemi değil uzman raporlarıyla kişinin karakterini ve gelecekteki tehlikesini de yargılar."),
        entry("Reformcuların ekonomik cezası", [
            "On sekizinci yüzyıl reformcuları keyfi ve aşırı işkenceye karşı orantılı, düzenli cezalar önerir. Her suç toplumsal sözleşmeye zarar verir, ceza caydırıcı işaret olmalıdır.",
            "Bir mağazadaki fiyat etiketi gibi, suçun cezası önceden bilinir ve hükümdarın öfkesinden bağımsızlaşır.",
            "Amaç daha az değil daha iyi dağıtılmış cezadır. Yasadışı davranışların tamamına ulaşan düzenli ağ kurulur.",
            "İnsanileşme gerçek olabilir, fakat aynı anda iktidarın hesaplı ve sürekli hale gelmesini görmek gerekir.",
        ], "BİRİNCİ KISIM · BEDENDEN RUHA", art="penalty-signs", caption="Reformcu ceza hükümdarın öfkesini azaltırken suçlara önceden hesaplanmış ve toplum geneline yayılan işaretler koyar."),
        entry("Uysal beden nasıl üretilir?", [
            "Disiplin bedeni hem daha yararlı hem daha itaatkar yapar. Asker daha hızlı ateş eder, öğrenci daha düzenli yazar, işçi hareketi ölçülü tekrarlar.",
            "Hamur gibi ezmek yerine makine parçasını hassas ayarlamak düşünün. Beden yok edilmez; kapasitesi artırılır ve denetime bağlanır.",
            "Foucault iktidarın yalnız yasaklamadığını burada gösterir. Beceri, verim ve bilgi üretirken özgürlüğü biçimlendirir.",
            "Modern kurumların başarısı ve baskısı aynı teknik içinde bulunabilir.",
        ], "İKİNCİ KISIM · DİSİPLİNİN ARAÇLARI", art="docile-body", caption="Disiplin bedeni kırıp atmaz; hareketini hassaslaştırırken onu yararlı ve kolay denetlenebilir hale getirir."),
        entry("Mekanda herkese bir yer", [
            "Kışla, sınıf ve atölye kişileri sıraya, hücreye, masaya ve göreve dağıtır. Kim nerede belli olduğunda karşılaştırma ve gözetim kolaylaşır.",
            "Açık pazarda kalabalığı izlemek zordur; numaralı masalarda devamsızlık ve hız anında görünür.",
            "Mekan tarafsız kabuk değildir. Duvar, koridor ve oturma planı davranışı önceden düzenler.",
            "Bugün açık ofis, turnike ve dijital konum sistemi aynı soruyu taşır: Yerleşim kimin görmesini ve kimin hareketini kolaylaştırıyor?",
        ], "İKİNCİ KISIM · DİSİPLİNİN ARAÇLARI", art="ranked-space", caption="Numaralı yerler insanları yalnız barındırmaz; yoklama, karşılaştırma ve gözetimi mümkün kılan düzen kurar."),
        entry("Zamanın ince parçaları", [
            "Disiplin günü saatlere, görevi hareketlere böler. İşin yalnız bitmesi değil nasıl ve ne kadar sürede yapıldığı ölçülür.",
            "Ustanın serbest ritmi, kronometreyle standart harekete dönüşür. Boş saniye verimsizlik olarak görünür.",
            "Bu düzen büyük koordinasyon sağlar; tren, hastane ve okul ortak zaman olmadan işlemez. Aynı zamanda bedenin ritmini dış çizelgeye bağlar.",
            "Foucault ilerlemeyi inkar etmez, üretkenliğin hangi itaat tekniğiyle geldiğini sorar.",
        ], "İKİNCİ KISIM · DİSİPLİNİN ARAÇLARI", art="fragmented-time", caption="Günün küçük zaman kutularına bölünmesi ortak üretimi hızlandırırken bedenin ritmini dış çizelgeye bağlar."),
        entry("Egzersiz ve basamak", [
            "Asker veya öğrenci kolay hareketten zora, sınıftan rütbeye ilerleyen seri egzersizlerle kurulur. Kişi yalnız değerlendirilmez, aşama aşama üretilir.",
            "Piyano gamı tekrarı beceri kazandırır. Aynı teknik not, sıra ve ceza ile normal davranış ölçüsü de kurabilir.",
            "Disiplin tek büyük emir değil küçük tekrarların toplamıdır. İnsan alışkanlık içinde biçimlenir.",
            "Eğitim ile denetim bu yüzden kolay ayrılmaz; sorulması gereken hedef, söz hakkı ve ölçünün kimde olduğudur.",
        ], "İKİNCİ KISIM · DİSİPLİNİN ARAÇLARI", art="graded-exercise", caption="Basamaklı egzersiz beceri üretirken kişiyi rütbe, not ve normal ilerleme çizgisi içinde şekillendirir."),
        entry("Hiyerarşik bakış", [
            "İyi disiplin sürekli görebilen bir bakış ister. Mimari, üst gözetmeni ve alt sıraları görünürlük içinde düzenler.",
            "Fabrika penceresi ışık kadar ustabaşının bütün tezgahları görmesini sağlar. Görünür olmak davranışı değiştirir.",
            "Gözetmen her an bakmasa bile bakabilme ihtimali düzen üretir. İktidar fiziksel müdahaleden önce olasılık olarak çalışır.",
            "Günümüz kamera ve performans panelleri bu bakışı insan gözünün ötesine taşır.",
        ], "İKİNCİ KISIM · DİSİPLİNİN ARAÇLARI", art="hierarchical-gaze", caption="Her an bakılma ihtimali gözetmenin fiilen müdahale etmediği anlarda bile davranışı düzenleyebilir."),
        entry("Normalleştirici ceza", [
            "Disiplin yalnız yasak eylemi cezalandırmaz; geç kalma, dağınıklık, düşük hız ve beklenenden sapmayı küçük yaptırımlarla düzeltir.",
            "Hukuk hırsızlık oldu mu diye sorar, normalleştirme 'diğerlerinden ne kadar geridesin?' diye sorar.",
            "Ödül ve ceza sıralama oluşturur. İyi öğrenci, riskli mahkum, verimli işçi gibi kimlikler ölçüden doğar.",
            "Normal yararlı karşılaştırma olabilir, fakat farklılığı kusur haline getirirse görünmez baskı kurar.",
        ], "ÜÇÜNCÜ KISIM · PANOPTİKON", art="normalizing-curve", caption="Normalleştirme yasayı çiğnemeyi değil ortalamadan sapmayı ölçerek kişileri iyi, geri veya riskli diye sıralar."),
        entry("Sınavın çift yüzü", [
            "Sınav gözetim ile bilgiyi birleştirir. Öğrenciye not verirken onun hakkında dosya üretir; birey karşılaştırılabilir vaka olur.",
            "Doktor muayenesi yardım sağlar, aynı anda bedenleri sınıflandıran veri toplar. Bilmek ve yönetmek iç içe geçer.",
            "Foucault bilgi sahte olduğu için değil, kurum içindeki güç ilişkisiyle üretildiği için bunu vurgular.",
            "Sınavın adaleti sorunun kalitesi kadar kaydın kimde olduğu ve kişiyi ne kadar süre izlediğiyle ilgilidir.",
        ], "ÜÇÜNCÜ KISIM · PANOPTİKON", art="exam-file", caption="Sınav kişiyi ölçerken onun hakkında kalıcı dosya üretir; bilgi ve yönetim aynı masada birleşir."),
        entry("Panoptikon: Görünmeden görmek", [
            "Bentham'ın tasarımında merkez kule çevredeki hücreleri görür, mahkum kulede biri olup olmadığını bilemez. Bu belirsizlik gözetimi kişinin içine taşır.",
            "Kamera çalışıyor mu bilmediğiniz koridorda davranışınızı yine ayarlarsınız. Sürekli gerçek bakış yerine sürekli ihtimal yeterlidir.",
            "Panoptikon belirli hapishane kadar iktidar diyagramıdır. Okul, hastane ve fabrika farklı amaçlarla aynı görünürlük mantığını kullanabilir.",
            "Foucault modern toplumun her yerinin tek kule olduğunu söylemez; aktarılabilir bir tekniği gösterir.",
        ], "ÜÇÜNCÜ KISIM · PANOPTİKON", art="panopticon", caption="Merkez kulede göz olup olmadığı bilinmediğinde mahkum gözetimi kendi davranışına yerleştirir."),
        entry("Veba şehri ve cüzzamlı", [
            "Cüzzamlı toplum dışına atılır; veba şehrinde ise herkes evine kapatılır, kayıt ve yoklamayla tek tek izlenir. Dışlama ile ayrıntılı disiplin iki iktidar modelidir.",
            "Biri kapının dışına çizgi çeker, diğeri içeride her odayı numaralar. Modern kurumlar ikisini birleştirebilir: Normal olmayanı ayırıp sürekli inceler.",
            "Salgın önlemi hayat kurtarabilir. Foucault tıbbi gereği inkar etmez; acil düzenin nasıl kalıcı yönetim tekniğine dönüşebildiğini sorar.",
            "Kriz sırasında kurulan veri ve yetkinin kriz sonrası kaderi demokratik sorudur.",
        ], "ÜÇÜNCÜ KISIM · PANOPTİKON", art="plague-grid", caption="Veba düzeni insanları dışarı atmak yerine ev ve kayıt hücrelerinde tek tek görünür hale getirir."),
        entry("Hapishane neden hemen yayıldı?", [
            "Hapishane özgürlüğü elinden aldığı için eşit ve ölçülebilir ceza gibi görünür. Ayrıca çalışma, eğitim ve gözetimle kişiyi dönüştürme vaadi taşır.",
            "Para cezası zenginle yoksula eşit değildir; bir yıl zaman herkese aynı görünür. Oysa yaşam koşulları ve sonuçlar yine eşit değildir.",
            "Hapishane disiplin tekniklerinin yoğunlaştığı kurumdur. Suçu yalnız ödetmek değil kişiyi düzeltmek ister.",
            "Bu doğal ceza biçimi değildir; belirli tarihsel tekniklerin buluşmasıdır.",
        ], "DÖRDÜNCÜ KISIM · HAPİSHANE VE BUGÜN", art="measured-time", caption="Hapishane özgürlüğü zaman birimiyle ölçerek eşit ceza görüntüsü verir, fakat hayatlar üzerindeki sonuç eşit olmayabilir."),
        entry("Başarısızlık mı, işlev mi?", [
            "Hapishanenin suçu azaltmadığı, tekrar suça ve suçlu çevresine yol açtığı daha başından bilinir. Buna rağmen kurum sürer.",
            "Sürekli aynı sonucu vermeyen makine neden atılmaz? Foucault görünür başarısızlığın başka işlev ürettiğini sorar.",
            "Hapishane belirli bir 'suçlu' sınıfı ayırır, gözetilebilir hale getirir ve diğer yasa dışılık türlerinden dikkati uzaklaştırabilir.",
            "Başarısızlık reform çağrılarını da besler; kurum kendi eleştirisiyle birlikte yeniden kurulur.",
        ], "DÖRDÜNCÜ KISIM · HAPİSHANE VE BUGÜN", art="failing-machine", caption="Suçu azaltmadığı söylenen hapishanenin sürmesi, görünür amaç dışında hangi işlevleri ürettiğini sormayı gerektirir."),
        entry("Karceral toplum", [
            "Hapishane duvarları dışındaki okul, fabrika, kışla ve hastane aynı değildir. Fakat kayıt, sınav, sıra ve normalleştirme tekniklerini paylaşabilir.",
            "Foucault toplumun bütünü hapishanedir demez; ceza mantığının geniş bir disiplin ağı içinde anlaşılması gerektiğini gösterir.",
            "Çocuk davranış puanı, çalışan performans paneli ve risk skoru farklı amaçlarla benzer karşılaştırma düzeni kurar.",
            "Kurumun yararı, tekniğin güç etkisini sorgulamamayı gerektirmez.",
        ], "DÖRDÜNCÜ KISIM · HAPİSHANE VE BUGÜN", art="carceral-network", caption="Okul, fabrika ve hastane hapishane değildir, fakat kayıt ve normalleştirme teknikleri kurumlar arasında dolaşabilir."),
        entry("Telefondaki küçük kule", [
            "Konum, tıklama, hız ve yüz verisi günümüz gözetimini merkez kuleden dağıtık platformlara taşır. Kişi yalnız izlenmez, tahmin edilir ve yönlendirilir.",
            "Adım sayacı sağlık motivasyonu verirken sigorta veya işveren ölçüsüne dönüşebilir. Aynı veri bakım ve denetim arasında hareket eder.",
            "Foucault'nun modeli dijital dünyayı tam açıklamaz; şirket, algoritma ve gönüllü paylaşım yeni boyutlardır.",
            "Yine de görünürlük ile öz düzenleme bağlantısı güçlüdür: Puanı gören kişi kendini ölçünün dilinde yönetir.",
        ], "DÖRDÜNCÜ KISIM · HAPİSHANE VE BUGÜN"),
        entry("Foucault'nun eksik bıraktıkları", [
            "Kitap disiplinin yayılışını güçlü anlatır, fakat reformların gerçek acı azaltımını ve mahkumların direniş deneyimini bazen arka plana iter.",
            "Fransa merkezli tarih başka ülkelerin ceza yollarına aynen uymaz. Irk, sömürge ve cinsiyet farkları daha geniş çalışma ister.",
            "İktidarın her yerde görünmesi değişimin nereden geleceğini belirsizleştirebilir. Foucault direniş imkanı kabul eder, fakat bu kitap ayrıntılı program sunmaz.",
        ], "SON DURAKLAR"),
        entry("Disiplinin yararı olabilir mi?", [
            "Cerrahi hijyen, uçuş kontrol listesi ve okul rutini disiplin olmadan zarar görebilir. Sorun her düzenin baskı olması değildir.",
            "Kontrol soruları şunlardır: Kuralın amacı açık mı, ölçülen kişi söz sahibi mi, veri itiraz edilebilir mi ve sapma otomatik kusur sayılıyor mu?",
            "Foucault bizi düzeni reddetmeye değil masum görünen tekniğin güç yapısını incelemeye çağırır.",
        ], "SON DURAKLAR"),
        entry("Bir kurumu Foucault gibi gezmek", [
            "Kapıdan girince kim görünür, kim görünmeden görür? Zaman nasıl bölünür, bedenler nereye yerleştirilir, hangi davranış kayda girer?",
            "Sınav veya puan yalnız sonuç mu ölçüyor, kişi hakkında kalıcı kimlik mi üretiyor? Veriyi kim saklıyor ve nasıl itiraz edilir?",
            "Duvar ve çizelge böylece iktidarın sessiz cümleleri olarak okunur.",
        ], "SON DURAKLAR"),
        entry("Bir cümlede kitabın özü", [
            "Modern ceza işkenceyi azaltırken iktidarı ortadan kaldırmadı; bedeni zaman, mekan, gözetim, sınav ve normalleştirmeyle sürekli biçimlendiren daha sessiz bir disiplin ağı kurdu.",
            "Akılda kalacak görüntü boş gözetleme kulesidir: Orada göz olmasa bile görülme ihtimali insanı kendi gardiyanına çevirebilir.",
        ], "SON DURAKLAR"),
    ]))


BOOKS.append(base(244, "Sapiens: Hayvanlardan Tanrılara", "Yuval Noah Harari",
    "Önemsiz bir Afrika primatının ortak hikayeler kurarak gezegene hükmetmesini; bilişsel, tarımsal ve bilimsel devrimler boyunca para, imparatorluk, din, mutluluk ve gelecek sorularıyla anlatan geniş tarihin sade ve eleştirel rehberi.",
    "#6D6346", "Sapiens: A Brief History of Humankind", "sapiens",
    [
        {"id": 1, "title": "Yuval Noah Harari - Sapiens resmi sayfası", "url": "https://www.ynharari.com/book/sapiens/"},
        {"id": 2, "title": "Smithsonian Human Origins - İnsan evrimi", "url": "https://humanorigins.si.edu/evidence"},
        {"id": 3, "title": "Nature Education - Tarımın kökenleri", "url": "https://www.nature.com/scitable/knowledge/library/the-development-of-agriculture-10026280/"},
        {"id": 4, "title": "Our World in Data - Uzun dönem insanlık verileri", "url": "https://ourworldindata.org/"},
    ], [
        entry("Bu kitap nasıl okunmalı?", [
            "Sapiens yaklaşık yetmiş bin yılı tek ciltte anlatır. Bu ölçek berrak büyük desenler verir, ayrıntı ve bilimsel anlaşmazlıkları kaçırabilir.",
            "Harari canlı, kesin ve kışkırtıcı cümleler kurar. Rehber kitabın savını korurken bazı açıklamaların kanıtlanmış sonuç değil yorum olduğunu işaretleyecek.",
            "Eser dört eksende ilerler: Bilişsel devrim, tarım devrimi, insanlığın birleşmesi ve bilimsel devrim. Mutluluk ile gelecek bu tarihin terazisidir.",
        ], "BAŞLANGIÇ"),
        entry("Bir zamanlar birçok insan türü", [
            "Bugün insan deyince tek tür düşünürüz. Oysa geçmişte Neandertal, Denisovalı ve başka insan toplulukları aynı dünyada yaşadı.",
            "Aile ağacında yalnız kalan son dal kendini ağacın tamamı sanabilir. Fosil ve DNA diğer dalların gerçekliğini geri getirir.",
            "Sapiens bazı gruplarla çiftleşti; bugünkü insanlarda bu akrabaların gen izleri bulunur. Yer değiştirme ve yok oluşun payı bölgelere göre değişir.",
            "Harari'nin açılışı insanı yaratılışın tek basamağı değil evrimsel çalılığın hayatta kalan dalı yapar.",
        ], "BİRİNCİ KISIM · BİLİŞSEL DEVRİM", art="many-humans", caption="Homo sapiens geçmişte tek insan değildi; bugün yalnız kalan dal, eski insan çalılığının tamamı değildir."),
        entry("Dedikodu neden büyük güçtür?", [
            "Dil yalnız aslanın yerini bildirmek için değil, gruptaki kimin güvenilir olduğunu konuşmak için de kullanılır. Sosyal bilgi işbirliğini büyütür.",
            "Yirmi kişilik ekipte herkesi doğrudan tanırsınız; yüzlerce kişide itibar hikayeleri gerekir. Dedikodu toplumsal kredi raporu gibi çalışır.",
            "Bu sistem yalan ve dışlama da üretebilir. Dil güven kurarken itibar silahına dönüşebilir.",
            "Harari bilişsel devrimi yaklaşık yetmiş bin yıl önce yeni dil ve hayal gücü kapasitesiyle ilişkilendirir; tarih ve nedenler bilimsel tartışmaya açıktır.",
        ], "BİRİNCİ KISIM · BİLİŞSEL DEVRİM", art="campfire-gossip", caption="Ateş başındaki sosyal hikayeler kimin güvenilir olduğunu taşıyarak doğrudan tanışmanın ötesinde işbirliği kurabilir."),
        entry("Var olmayan şeylere birlikte inanmak", [
            "Şirket, devlet, para ve insan hakkı taş veya ağaç gibi fiziksel nesne değildir; birçok insanın paylaştığı kurallar içinde gerçek etki üretir.",
            "Bir banknot kağıttır, fakat milyonlarca kişi aynı hikayeyi kabul ettiği için yemek ve emekle değişir. Ortak inanç sahte demek değildir.",
            "Harari bu hayali düzenlerin büyük yabancı grupları esnek biçimde birleştirdiğini savunur. Arılar büyük koloni kurar ama kurallarını hızlı değiştiremez.",
            "İnsan üstünlüğünün anahtarı yalnız bireysel zeka değil paylaşılan kurgu etrafında örgütlenebilme gücüdür.",
        ], "BİRİNCİ KISIM · BİLİŞSEL DEVRİM", art="shared-fiction", caption="Banknot ve devlet ortak hikaye olduğu için etkisiz değil; milyonlar aynı kurala göre davrandığı için güçlüdür."),
        entry("Avcı toplayıcının zengin bilgisi", [
            "Avcı toplayıcı küçük gruplar bitki, hayvan, mevsim ve arazi hakkında geniş bilgi taşır. Günleri bugünkü iş saatinden farklı ritimlerde olabilir.",
            "Market listesi bilen şehirli, çevresindeki yüz yenebilir bitkiyi ayıramayabilir. Uzmanlık biçimi değişmiştir.",
            "Harari bazı avcı yaşamlarını görece sağlıklı ve çeşitli gösterebilir, fakat gruplar arasında şiddet, beslenme ve emek büyük fark taşır.",
            "Geçmişi cennet veya sefalet diye tek renge boyamadan, kaybedilen bilgi ve kazanılan güvenliği birlikte düşünmek gerekir.",
        ], "BİRİNCİ KISIM · BİLİŞSEL DEVRİM", art="forager-knowledge", caption="Avcı toplayıcının çevre bilgisi kitapta değil yüzlerce bitki, iz ve mevsimi bedenle tanımakta saklıdır."),
        entry("Büyük hayvanların kaybı", [
            "Sapiens yeni kıtalara ulaştığında büyük hayvan türlerinin yok oluşuyla zaman bakımından çakışmalar görülür. Avcılık, iklim ve üreme hızı birlikte etkili olabilir.",
            "Az yavrulayan dev hayvan için yılda birkaç ek ölüm bile kuşaklar içinde nüfusu çökertir. İnsan etkisi ilk sanayi bacasından çok önce başlamış olabilir.",
            "Harari insanı ekolojik seri katil diye sert adlandırır. İfade dikkat çeker, her kıtadaki neden payı aynı kesinlikte değildir.",
            "Ders, doğayla uyumlu masum geçmiş efsanesini sınamaktır.",
        ], "BİRİNCİ KISIM · BİLİŞSEL DEVRİM", art="megafauna-loss", caption="Yavaş üreyen büyük hayvanlarda küçük av baskısı bile kuşaklar boyunca geri dönülmez kayıp yaratabilir."),
        entry("Buğday insanı evcilleştirdi mi?", [
            "Tarım daha çok yiyecek üretti, fakat bireyin daha iyi beslendiğini veya az çalıştığını garanti etmedi. Harari kışkırtıcı biçimde insanın buğdayı değil buğdayın insanı evcilleştirdiğini söyler.",
            "İnsan ormanı temizledi, taş taşıdı, suladı ve tarlanın yanında yaşadı; buğday dünya alanını büyüttü. Tür başarısı ile birey refahı ayrıldı.",
            "Nüfus arttıkça eski yaşama dönmek zorlaştı. Fazla yiyecek daha çok ağız yarattı ve lüks tuzağı oluştu.",
            "Tarım tek anda ve her yerde felaket değildi; süreç, ürün ve toplumlar farklıydı. Ama ilerleme eşittir mutluluk varsayımını sarsar.",
        ], "İKİNCİ KISIM · TARIM VE DÜZEN", art="wheat-domesticates", caption="Buğdayın alanı büyürken insanın çalışma yükü de arttı; tür ölçeğindeki başarı bireyin refahı olmayabilir."),
        entry("Lüks tuzağı", [
            "Yeni kolaylık önce hayatı rahatlatır, sonra standart hale gelir ve geri dönüş imkansızlaşır. Daha çok ürün daha çok çocuk ve daha çok iş doğurabilir.",
            "E-posta mektubu hızlandırdı, sonra herkes anında cevap bekledi. Kazanılan zaman yeni mesajlarla doldu.",
            "Harari tarımın bu tuzağa büyük örnek olduğunu söyler. Birey küçük kararlarla ilerler, kimse toplam sonucu seçmez.",
            "Teknolojiyi değerlendirirken ilk fayda yanında yeni bağımlılık ve beklentiyi de sormak gerekir.",
        ], "İKİNCİ KISIM · TARIM VE DÜZEN"),
        entry("Hayali düzenin taş binaları", [
            "Büyük toplumlar yasa, din ve hiyerarşi hikayeleriyle örgütlenir. Hammurabi eşitsiz sınıfları, Amerikan Bağımsızlık Bildirgesi eşit bireyleri doğal sayar.",
            "İki metin farklı düzen kurar; ikisi de biyolojiden doğrudan okunmaz. İnsanların birlikte kabul ettiği normlardır.",
            "Hayali düzen zihinde kalmaz. Saray, mahalle, okul ve kıyafet olarak taşa ve bedene yerleşir.",
            "Bir düzenin yapılmış olması kolayca değişeceği anlamına gelmez. Milyonların beklentisi onu katı gerçekliğe dönüştürür.",
        ], "İKİNCİ KISIM · TARIM VE DÜZEN", art="imagined-order", caption="Ortak hukuk hikayesi yalnız kağıtta kalmaz; şehir planı, okul ve beden davranışı olarak maddi dünyaya yerleşir."),
        entry("Yazı ve sayıların hafızası", [
            "Küçük grup borç ve akrabalığı hatırlayabilir; büyük krallık vergi, tarla ve nüfusu kayıtla yönetir. Yazı insan beyninin dış hafızası olur.",
            "Tablet bir çiftçiyi isimden çok arpa miktarı ve borç satırı olarak görür. Bürokrasi kişiyi veri kategorisine çevirir.",
            "Kayıt büyük sulama ve dağıtım sağlar, aynı anda sınıflandırma gücü kurar. Yazı yalnız edebiyatın değil verginin de aracıdır.",
            "Bugünkü veri tabanı bu mantığı büyütür: Sistem yalnız kaydedebildiği kişiyi görebilir.",
        ], "İKİNCİ KISIM · TARIM VE DÜZEN", art="written-memory", caption="Yazı büyük topluma dış hafıza verirken kişiyi vergi, tarla ve borç satırlarına dönüştüren bürokrasi kurar."),
        entry("Hiyerarşi nasıl doğal görünür?", [
            "Toplumlar zengin-yoksul, özgür-köle, kadın-erkek ayrımlarını doğa veya tanrı iradesi diye açıklayabilir. Tarihsel düzen değişmez gerçek gibi sunulur.",
            "Merdiveni yapanlar üst basamağın daha değerli olduğunu söyler; sonra yükseklik değerin kanıtı sayılır.",
            "Harari hiyerarşilerin bazı biyolojik farkları kullanabileceğini, fakat ayrıntılı rol ve değerin kültürel olduğunu vurgular.",
            "Doğallaştırmayı görmek eşitsizliği tek hamlede çözmez, eleştirinin ilk kapısını açar.",
        ], "İKİNCİ KISIM · TARIM VE DÜZEN"),
        entry("Para en evrensel güven", [
            "Birbirinin dinine ve diline güvenmeyen insanlar aynı parayı kabul edebilir. Para nesneye değil başkalarının da kabul edeceğine duyulan güvene dayanır.",
            "Tüccar banknotu yemek için değil yarın başkasına verebileceği için alır. Güven kişisel değil ağsaldır.",
            "Para esnek işbirliği sağlar, fakat her değeri fiyata çevirebilir. Orman kutsal yerden kereste tutarına dönüşebilir.",
            "Harari parayı ahlaksız değil güçlü ve çift yüzlü ortak hikaye olarak görür.",
        ], "ÜÇÜNCÜ KISIM · İNSANLIĞIN BİRLEŞMESİ", art="universal-money", caption="Para yabancıların birbirine değil, ağdaki herkesin yarın aynı işareti kabul edeceğine güvenmesini sağlar."),
        entry("İmparatorluk yalnız zor mu?", [
            "İmparatorluk fetih ve sömürü taşır, aynı zamanda hukuk, dil, yol ve kültürleri geniş alanda birleştirir. Bugünkü kimlikler çoğu kez eski imparatorluk karışımlarından doğmuştur.",
            "Fatihin yolunda asker kadar tüccar ve fikir de hareket eder. Mağdur toplum bile zamanla imparatorluk dilini kendi kültürünün parçası yapabilir.",
            "Bu karmaşıklık şiddeti aklamaz. Kültürel miras fethin rıza ile olduğu anlamına gelmez.",
            "Harari saf kültür fikrini sarsar; tarih karışım ve güçle kurulmuştur.",
        ], "ÜÇÜNCÜ KISIM · İNSANLIĞIN BİRLEŞMESİ", art="imperial-road", caption="İmparatorluk yolu zorla açılırken asker, mal, dil ve fikirleri birlikte taşıyan kalıcı karışımlar üretir."),
        entry("Din ortak düzen kurar", [
            "Din insanüstü düzene inanarak davranış normları kurar. Yerel ruhlardan evrensel tanrılara geçiş büyük toplumları ortak ahlakta birleştirebilir.",
            "Harari liberalizm ve komünizm gibi modern ideolojileri de insanüstü değer düzenleri açısından dine benzetir. Bu geniş tanım tartışmalıdır.",
            "Din yalnız inanç listesi değil ritüel, topluluk ve deneyimdir. Tek işleve indirgemek çeşitliliği kaçırır.",
            "Kitabın amacı doğruluk hükmünden çok büyük işbirliğini nasıl taşıdığını göstermektir.",
        ], "ÜÇÜNCÜ KISIM · İNSANLIĞIN BİRLEŞMESİ", art="shared-ritual", caption="Ortak ritüel yabancıları aynı ahlaki düzenin üyeleri yaparak büyük ölçekli güven ve kimlik kurabilir."),
        entry("Bilgisizliği keşfetmek", [
            "Modern bilim 'bilmiyoruz' diyerek başlar. Haritalardaki boş alanlar canavar resmiyle değil araştırma çağrısıyla doldurulur.",
            "Bilgisizliği kabul etmek zayıflık değil yeni gözlem ve matematik yöntemine yatırım gerekçesidir.",
            "Bilim tek başına hangi hedefin iyi olduğunu söylemez; imparatorluk ve sermaye hedef, kaynak ve kullanım sağlar.",
            "Bilimsel devrim bilgi kadar bilgi-iktidar ortaklığıdır.",
        ], "DÖRDÜNCÜ KISIM · BİLİM VE GELECEK", art="blank-map", caption="Haritadaki boşluğu bilginin sonu değil araştırma çağrısı saymak modern bilimin güçlü başlangıcıdır."),
        entry("Bilim, imparatorluk ve harita", [
            "Avrupalı seferler asker, tüccar ve bilim insanını aynı gemide taşıdı. Yeni bitki, dil ve coğrafya bilgisi fetih kapasitesini artırdı.",
            "Harita keşif aracı ve yönetim aracıdır. Ölçülen toprak vergiye, sınıra ve mülke daha kolay çevrilir.",
            "Bilim yalnız sömürge ürünü değildir, fakat bazı disiplinlerin kaynak ve koleksiyonları imparatorlukla büyümüştür.",
            "Bilginin doğruluğu ile üretildiği güç koşulunu birlikte incelemek gerekir.",
        ], "DÖRDÜNCÜ KISIM · BİLİM VE GELECEK", art="science-empire-ship", caption="Keşif gemisi bilgi, ticaret ve fetih amaçlarını aynı güvertede taşıyarak haritayı iktidar aracına dönüştürebilir."),
        entry("Kredi büyümeyi nasıl hızlandırdı?", [
            "Gelecekte üretimin artacağına güvenen yatırımcı bugünkü projeye kredi verir. Kâr yeniden yatırıma döner ve ekonomik pasta büyüyebilir.",
            "Henüz müşteri gelmemiş fırın krediyle ocak alır; gelecek ekmek bugünün makinesini finanse eder.",
            "Büyüme yaşam standardını yükseltir, fakat kaynak tüketimi ve eşitsizlik yaratabilir. Sonsuz büyümenin ekolojik sınırı vardır.",
            "Harari kapitalizmi inanç ve kurum sistemi olarak okur; başarıları yanında sürekli büyüme zorunluluğunu sorgular.",
        ], "DÖRDÜNCÜ KISIM · BİLİM VE GELECEK"),
        entry("Hayvanların görünmeyen bedeli", [
            "Sanayi tarımı milyarlarca hayvanı yüksek verim için dar sistemlerde yetiştirir. Tür olarak tavuk çoğalır, birey olarak tavuğun yaşamı kötüleşebilir.",
            "Harari tarih başarısını gen kopyası sayısıyla ölçmenin ahlaki yetersizliğini gösterir. Çok olmak iyi yaşamak değildir.",
            "İnsan refahı da ucuz etin arkasındaki acıyı görünmez kılabilir. Hayvan duyarlılığı tarih hesabına girmelidir.",
            "Bu bölüm kitabın en güçlü ahlaki çağrılarından biridir.",
        ], "DÖRDÜNCÜ KISIM · BİLİM VE GELECEK", art="factory-animals", caption="Bir türün sayıca çoğalması, dar üretim sistemindeki bireylerin iyi yaşadığı anlamına gelmez."),
        entry("Daha güçlü, daha mutlu mu?", [
            "İnsanlık enerji, sağlık ve üretimde büyük güç kazandı. Harari bu ilerlemenin öznel mutluluğu aynı oranda artırıp artırmadığını sorar.",
            "Yeni rahatlık beklenti standardını yükseltir. Dünün lüksü bugünün zorunluluğu olur ve kıyas duygusu sonucu etkiler.",
            "Mutluluk biyokimya, anlam, ilişki ve beklentiyle bağlıdır; tek tarihsel ölçüye indirgenemez. Bu bölümde Harari farklı görüşleri yan yana getirir.",
            "Tarihin başarısını yalnız imparatorluk büyüklüğü veya milli gelirle ölçmek yaşayan kişinin deneyimini kaçırır.",
        ], "DÖRDÜNCÜ KISIM · BİLİM VE GELECEK", art="power-happiness-scale", caption="İnsanlığın güç terazisi yükselirken günlük mutluluk aynı hızda artmayabilir; başarı ölçüsü yeniden sorulmalıdır."),
        entry("Tanrılar yaratmaya yaklaşmak", [
            "Gen mühendisliği, yapay organlar ve bilgisayar sistemleri doğal seçilimin sınırlarını değiştirebilir. Sapiens kendi beden ve zihin tasarımına müdahale ediyor.",
            "Sorun yalnız ne yapabileceğimiz değil ne istememiz gerektiğidir. Gücü artan ama arzusunu anlamayan insan tehlikelidir.",
            "Harari geleceği kesin tahmin etmez; tarih kitabını etik soruyla bitirir. Yeni insan türleri ve eşitsizlik olasılığına dikkat çeker.",
            "Teknoloji kader değildir. Araştırma, erişim ve sınır kararları bugünkü siyasi seçimlerdir.",
        ], "DÖRDÜNCÜ KISIM · BİLİM VE GELECEK", art="human-design", caption="Beden ve zekayı tasarlama gücü büyüdükçe insanlığın ne isteyeceği sorusu teknik imkan kadar önemli hale gelir."),
        entry("Sapiens'in eleştirilen büyük cümleleri", [
            "Bilişsel devrimin tarihi, tarımın herkese tuzak oluşu ve imparatorlukların birleştirici rolü uzmanlar arasında daha karmaşıktır. Harari bazen tartışmalı görüşü kesin sonuç gibi yazar.",
            "Büyük tarih ayrıntıyı feda ederek desen kurar. Tek örnek bütün kıtayı temsil edemez; arkeolojik kanıt değişmeye devam eder.",
            "Kitap başlangıç haritası olarak güçlü, son akademik kaynak olarak yetersizdir. Her büyük sav ek okumayla sınanmalıdır.",
        ], "SON DURAKLAR"),
        entry("Hayali demek yalan demek değildir", [
            "İnsan haklarına ortak kurgu demek değersiz oldukları anlamına gelmez. Tersine fiziksel doğada hazır bulunmadıkları için onları kurum ve eylemle korumak gerekir.",
            "Köprü de insan yapımıdır ama gerçektir ve hayat taşır. Yapılmış düzenler sonuçları bakımından güçlüdür.",
            "Harari'nin dili bazen ahlaki değerleri yalnız hikaye gibi duyurabilir. Ortak köken ile gerekçelendirilmiş değer ayrılmalıdır.",
        ], "SON DURAKLAR"),
        entry("Bir günlük Sapiens haritası", [
            "Cüzdanınızdaki para, işyerinizdeki şirket, kimlik kartındaki devlet ve takvimdeki hafta hangi ortak hikayelere dayanıyor?",
            "Sonra bu hikayelerin hangi bina, yazılım ve alışkanlıkla maddileştiğini bulun. İnanmayı bıraksanız tek başınıza değişir mi?",
            "Bu alıştırma toplumsal gerçekliği küçültmez; nasıl kurulduğunu ve nereden değişebileceğini gösterir.",
        ], "SON DURAKLAR"),
        entry("Bir cümlede kitabın özü", [
            "Homo sapiens gezegene tek tek daha güçlü olduğu için değil, para, devlet ve din gibi ortak hikayeler çevresinde çok sayıda yabancıyla esnek işbirliği kurabildiği için hükmetti.",
            "Akılda kalacak görüntü ortak haritadır: Kağıt fiziksel, sınır hayalidir; milyonlar ona göre hareket ettiğinde ikisi birlikte tarih yapar.",
        ], "SON DURAKLAR"),
    ]))


BOOKS.append(base(266, "Böyle Buyurdu Zerdüşt", "Friedrich Nietzsche",
    "Dağdan insanlara inen Zerdüşt'ün tanrının ölümü, üstinsan, sürü, beden, yaratma, güç istenci ve ebedi dönüşle yüzleştiği şiirsel yolculuğu karakterleri ve sahneleri kaybetmeden sadeleştiren rehber.",
    "#6E4C3D", "Also sprach Zarathustra", "boyle-buyurdu-zerdust",
    [
        {"id": 1, "title": "Project Gutenberg - Thus Spake Zarathustra tam metni", "url": "https://www.gutenberg.org/files/1998/1998-h/1998-h.htm"},
        {"id": 2, "title": "Stanford Encyclopedia of Philosophy - Nietzsche", "url": "https://plato.stanford.edu/entries/nietzsche/"},
        {"id": 3, "title": "Cambridge - Thus Spoke Zarathustra içindekiler", "url": "https://assets.cambridge.org/97805218/41719/toc/9780521841719_toc.pdf"},
        {"id": 4, "title": "Internet Encyclopedia of Philosophy - Nietzsche", "url": "https://iep.utm.edu/nietzsche/"},
    ], [
        entry("Bu kitap nasıl okunmalı?", [
            "Böyle Buyurdu Zerdüşt roman, şiir, vaaz parodisi ve felsefi deneydir. Zerdüşt her zaman Nietzsche'nin doğrudan sözcüsü değildir; karakter yanılır, yalnız kalır ve kendi öğretisiyle sınanır.",
            "Üstinsan biyolojik ırk veya siyasi efendi değildir. Eski değerlerin yıkıldığı dünyada kendi hayatına yaratıcı biçim verme ideali olarak okunmalıdır.",
            "Rehber olay yolunu koruyacak ve eserin Nazi ideolojisiyle sonradan çarpıtılmasını açıkça ayıracak.",
        ], "BAŞLANGIÇ"),
        entry("Dağdaki on yıl", [
            "Zerdüşt otuz yaşında dağa çekilir, on yıl yalnız yaşar ve bilgeliği taşınca güneş gibi vermek için insanlara inmeye karar verir.",
            "Dolu bardak paylaşılmadığında ağırlığa dönüşür. Bilgelik tek başına saklanan hazine değil ilişki içinde sınanan şeydir.",
            "Güneşe 'aydınlatacağın kimse olmasa mutluluğun ne olurdu?' diye sorar. Veren de alıcıya ihtiyaç duyar.",
            "İniş kitabın temel hareketidir: Yüksekte bulunan fikir pazar yerinde, dostlukta ve hayal kırıklığında denenmelidir.",
        ], "BİRİNCİ KISIM · İNİŞ VE İLK ÖĞRETİ", art="mountain-descent", caption="On yıl dağda biriken bilgelik, ancak insanlara doğru inip paylaşım ve dirençle sınandığında canlı hale gelir."),
        entry("Aziz ile tanrının ölümü", [
            "Ormanda yaşayan yaşlı aziz hala Tanrı'ya şarkı söyler. Zerdüşt ayrıldıktan sonra onun Tanrı'nın öldüğünü duymamasına şaşar.",
            "Tanrının ölümü gökyüzündeki varlığın biyolojik ölümü değil, Batı'nın ortak ahlaki ve anlam temelinin güvenilirliğini kaybetmesidir.",
            "Eski pusula çalışmazken yönsüzlük ve yeni değer yaratma sorumluluğu doğar. Yalnız inançsızlık değil kültürel depremdir.",
            "Nietzsche bu ölümü basit zafer diye kutlamaz; boşluğu nihilizmin doldurabileceğini görür.",
        ], "BİRİNCİ KISIM · İNİŞ VE İLK ÖĞRETİ", art="dead-compass", caption="Tanrının ölümü eski anlam pusulasının çalışmaması ve insanın yeni yön yaratma yüküyle kalmasıdır."),
        entry("Pazar yerinde üstinsan", [
            "Zerdüşt halka insanın aşılması gereken bir köprü olduğunu söyler. Üstinsan hazır tür değil, kendini dönüştürme ve dünyaya evet deme hedefidir.",
            "Tohum ağaca dönüşürken tohumu küçümsemez; içindeki imkanı aşar. İnsan da mevcut alışkanlığını son biçim saymamalıdır.",
            "Kalabalık öğretiden çok ip cambazını bekler ve Zerdüşt'le alay eder. Büyük kavram kamusal gösteride anlaşılmaz kalır.",
            "Üstinsanı başkalarını ezme ruhsatı yapmak metnin öz yaratım ve kendini aşma yönünü tersine çevirir.",
        ], "BİRİNCİ KISIM · İNİŞ VE İLK ÖĞRETİ", art="bridge-overman", caption="Üstinsan başkalarının üstünde efendi değil, insanın kendi verilmiş değerlerini aşmaya yöneldiği açık köprüdür."),
        entry("Son insanın rahat hapishanesi", [
            "Kalabalık üstinsan yerine son insanı ister. Son insan risk, büyük tutku ve yaratım istemez; küçük hazlar ve güvenli konforla yetinir.",
            "Her akşam aynı eğlence, hiçbir güçlü evet veya hayır yoktur. Acı azaltılmış, imkan da küçülmüştür.",
            "Nietzsche rahatlığı bütünüyle kötü saymaz; hayatın tek amacı olduğunda insanın ufkunu daralttığını gösterir.",
            "Bugünün sonsuz akış ve kişiselleştirilmiş konfor dünyası son insan görüntüsünü rahatsız edici biçimde günceller.",
        ], "BİRİNCİ KISIM · İNİŞ VE İLK ÖĞRETİ", art="last-man", caption="Son insan acıdan kaçarken büyük yaratım ve risk imkanını da bırakıp rahat ama dar bir hayat seçer."),
        entry("İp cambazının düşüşü", [
            "Üstinsan ile son insan konuşması sırasında ip cambazı kuleler arasında yürür. Soytarı onu korkutur, cambaz düşer ve ölür. Zerdüşt yanında kalır.",
            "İnsan hayvan ile aşılma imkanı arasındaki iptir; altındaki uçurum başarısızlık ve nihilizmdir.",
            "Kalabalık gösteri bitince dağılır. Zerdüşt büyük insanlık yerine tek ölen insana karşı sorumlulukla karşılaşır.",
            "Sahne felsefeyi bedene indirir: Aşılma sloganı gerçek düşme ve ölüm riskini taşır.",
        ], "BİRİNCİ KISIM · İNİŞ VE İLK ÖĞRETİ", art="tightrope-fall", caption="İnsan köprü olmak isterken uçurum ve düşme riski taşır; Zerdüşt soyut öğretinin yanında gerçek ölümü görür."),
        entry("Üç dönüşüm: Deve, aslan, çocuk", [
            "Ruh önce deve gibi ağır görevleri yüklenir ve dayanıklılık kazanır. Sonra aslan olur, 'yapmalısın' ejderhasına karşı özgürlük için hayır der.",
            "Ama aslan yeni değer yaratamaz; yalnız zinciri kırar. Çocuk unutma, oyun ve kutsal evet ile yeni başlangıç kurar.",
            "Bir sanatçı önce geleneği öğrenir, sonra ustasına karşı çıkar, en son yalnız tepki vermeden kendi dilini yaratır.",
            "Özgürlük yükten kaçmak değil, disiplin ve isyandan geçerek yaratıcı evete ulaşmaktır.",
        ], "İKİNCİ KISIM · DEĞERLERİ YARATMAK", art="camel-lion-child", caption="Ruh yük taşıyan deveden hayır diyen aslana, oradan yeni oyun ve değer kuran çocuğa dönüşür."),
        entry("Bedenini küçümseyenler", [
            "Zerdüşt bedeni ruhun aşağı hapishanesi sayanlara karşı çıkar. Benlik yalnız akıl değil, duyu, dürtü ve bedenin büyük aklıdır.",
            "Karar verdiğinizi sanırken uykusuzluk, korku ve beden ritmi düşüncenizi biçimlendirir. Zihin gövdesiz komutan değildir.",
            "Bu beden vurgusu kaba hazcılık değildir. Beden yaratma ve değer vermenin koşuludur.",
            "Kendini küçümseyen ahlak yaşamı öte dünya adına değersizleştirirse nihilizmi besler.",
        ], "İKİNCİ KISIM · DEĞERLERİ YARATMAK", art="body-wisdom", caption="Beden aklın taşıdığı yük değil, duygu ve düşüncenin içinden doğduğu büyük canlı zekadır."),
        entry("Bin bir amaç", [
            "Toplumlar iyi ve kötü cetvellerini kendileri yaratır; savaşçı halk cesareti, tüccar halk güveni yüceltebilir. Değerler gökten hazır düşmez.",
            "Aynı davranış bir kültürde onur, diğerinde ayıp olabilir. Bu fark her değerin eşit olduğu anlamına gelmez; yaratılmışlığını gösterir.",
            "Tanrının ölümü sonrası görev yalnız eski cetveli kırmak değil hayatı güçlendiren yeni ölçü kurmaktır.",
            "Değer yaratmak keyfi canının istediğini yapmak değil sonucu bütün hayatıyla üstlenmektir.",
        ], "İKİNCİ KISIM · DEĞERLERİ YARATMAK", art="many-value-tablets", caption="Halklar farklı iyi ve kötü levhaları yapar; yeni değer yaratmak eski taşı kırmaktan daha ağır sorumluluktur."),
        entry("Pazar yerindeki sinekler", [
            "Zerdüşt şöhret ve küçük saldırıların pazar yerinden uzak durmayı öğütler. Kalabalık yaratıcıyı överken aynı anda ısırır ve ölçüsüne çeker.",
            "Sosyal medyada her yorumla kavga eden kişi eserini başkalarının küçük tepkisine teslim eder.",
            "Yalnızlık kibirli kaçış değil yeni düşüncenin gürültüden korunma alanı olabilir.",
            "Ama sürekli dağda kalmak da sınanmayı engeller. Zerdüşt'ün hareketi yalnızlık ile dönüş arasında gidip gelir.",
        ], "İKİNCİ KISIM · DEĞERLERİ YARATMAK", art="market-flies", caption="Pazarın küçük övgü ve sokmaları yaratıcı dikkati parçalayabilir; yalnızlık eserin korunma odası olur."),
        entry("Dost ve düşman", [
            "Nietzsche'nin dostluğu rahat onay değil birbirini daha yükseğe çağıran gerilimdir. Gerçek dost bazen iyi bir düşman gibi karşı koyar.",
            "Her fikrinize evet diyen kişi aynadır; gerekçenizi zorlayan dost kasınızı geliştirir.",
            "Bu dil kötü ilişkiyi romantikleştirmek için kullanılmamalıdır. Şiddet ve aşağılama gelişim değil zarar üretir.",
            "Değerli karşı koyuş karşılıklı saygı ve kişinin kendi yolunu güçlendirmesiyle ölçülür.",
        ], "İKİNCİ KISIM · DEĞERLERİ YARATMAK", art="worthy-friend", caption="İyi dost yalnız onaylamaz; saygılı karşı koyuşla kişinin kendi düşünce ve gücünü daha yüksek sınar."),
        entry("Güç istenci yalnız iktidar mı?", [
            "Zerdüşt'te yaşam kendini aşan, biçim veren ve dirençle büyüyen güç olarak anlatılır. Güç istenci yalnız başkasını yönetme arzusu değildir.",
            "Müzisyen zor eseri çalışırken kendi kapasitesini örgütler. Bahçıvan bitkiye biçim verirken çevreyle yaratıcı ilişki kurar.",
            "Kavram Nietzsche'nin notlarında farklı anlamlar taşır ve kız kardeşinin derlediği sonraki kitapla yanlış biçimde tek sistem yapılmıştır.",
            "Gücü tahakküm diye okumak metni faşist slogana açar; kendini aşma ve yaratma boyutu merkezde tutulmalıdır.",
        ], "ÜÇÜNCÜ KISIM · EN AĞIR DÜŞÜNCE", art="creative-power", caption="Güç istenci yalnız başkasına hükmetmek değil, direnç içinde kendi kapasitesine biçim veren yaratıcı enerji olabilir."),
        entry("Ebedi dönüşün kapısı", [
            "Zerdüşt bir geçitte biri geçmişe, biri geleceğe uzanan iki sonsuz yol düşünür. Bütün anların tekrar dönmesi ihtimali en ağır düşünce olarak belirir.",
            "Hayatınızı sonsuz kez aynı ayrıntıyla yaşayacağınız söylense bunu lanet mi, armağan mı sayardınız?",
            "Ebedi dönüş kozmolojik teori veya yaşamı sınayan düşünce deneyi olarak yorumlanır. Kitap kesin teknik açıklama vermez.",
            "Ölçü gelecekte ödül değil bu hayatı tekrar isteyebilecek kadar sahiplenmektir.",
        ], "ÜÇÜNCÜ KISIM · EN AĞIR DÜŞÜNCE", art="eternal-gateway", caption="Geçmiş ve gelecek yollarının buluştuğu kapı, bu anı sonsuz kez istemeye hazır olup olmadığımızı sorar."),
        entry("Çoban ve yılan", [
            "Zerdüşt bir çobanın boğazına yılan girdiğini görür. Çobana yılanın başını ısırmasını söyler; çoban kurtulup insanüstü bir kahkahayla ayağa kalkar.",
            "Yılan Zerdüşt'ün boğucu ebedi dönüş düşüncesi olabilir. Ondan kaçmak değil onu ısırıp içselleştirmek dönüşüm yaratır.",
            "Korku dışarıdan çıkarılacak nesne değil kendi evetinizle değiştirilecek yük haline gelir.",
            "Sahne şiddetli ve semboliktir; tek doğru açıklamaya kapanmaz. Etkisi kavramdan önce bedene ulaşır.",
        ], "ÜÇÜNCÜ KISIM · EN AĞIR DÜŞÜNCE", art="shepherd-serpent", caption="Çoban boğucu yılanı ısırdığında en ağır düşünce kurbanı olmaktan onu dönüştüren kişiye geçer."),
        entry("Gece şarkısı ve verenin yalnızlığı", [
            "Zerdüşt ışık saçan ama ışık alamayan güneş gibi kendi vericiliğinin yalnızlığını söyler. Sürekli öğretmen olmak karşılıklılığı kaybettirir.",
            "Herkese destek veren kişinin yardım istemeyi unutması gibi, güç görüntüsü ihtiyaçların görünmesini engelleyebilir.",
            "Nietzsche'nin kahramanı yalnız zafer sesi değildir; kıskançlık, özlem ve yorgunluk taşır.",
            "Kendi değerini yaratmak başkasına ihtiyaç duymamak demek değildir.",
        ], "ÜÇÜNCÜ KISIM · EN AĞIR DÜŞÜNCE"),
        entry("Cüce, soytarı ve ağırlık ruhu", [
            "Zerdüşt'ün cücesi her yükselişi aşağı çeken alaycı ağırlıktır. Soytarı tehlikeli sıçrayışla başkasını düşürür. Karakterler iç sesler ve kültürel güçler gibi çalışır.",
            "Yeni fikre 'zaten her şey boş' diyen ses eleştiri değil başlamayı engelleyen ağırlık olabilir.",
            "Nietzsche hafifliği yüzeysellik değil ağır kaderi dansla taşıma gücü olarak över.",
            "Ciddiyetin her zaman derinlik, kahkahanın her zaman kaçış olmadığını gösterir.",
        ], "ÜÇÜNCÜ KISIM · EN AĞIR DÜŞÜNCE", art="spirit-of-gravity", caption="Ağırlık ruhu her yükselişi alayla aşağı çeker; yaratıcı hafiflik ağır hayatı inkar etmeden onunla dans eder."),
        entry("Yüksek insanlar mağarada", [
            "Son bölümlerde kral, papa, büyücü, en çirkin insan ve başka 'yüksek insanlar' Zerdüşt'ün mağarasına gelir. Eski değerleri aşmış ama yeniye ulaşamamış ara tiplerdir.",
            "Diploması bitmiş ama mesleğini bulamamış mezun gibi, eski evden çıkmış ve yeni evi kuramamışlardır.",
            "Zerdüşt onları teselli eder, fakat üstinsan saymaz. Yüksek olmak son durak değil geçiştir.",
            "Kitap kahraman topluluğunu bile parodi ve kahkahayla sınar.",
        ], "DÖRDÜNCÜ KISIM · YANLIŞ OKUMALAR", art="higher-men-cave", caption="Yüksek insanlar eski değerlerden çıkmış ama yenisini yaratamamış, mağarada bekleyen geçiş figürleridir."),
        entry("Eşek bayramı", [
            "Mağaradakiler bir eşeğe tapınmaya başlar. Eski Tanrı'nın boşluğu yeni ve komik putla hemen dolar. İnanç biçimi değişir, ihtiyaç sürer.",
            "Bir ideolojiyi bırakıp sorgulamadan başka lidere bağlanmak eşeğin önünde diz çökmeye benzer.",
            "Zerdüşt öfkelenir, sonra kahkaha ve kutlamanın iyileştirici yönünü de görür. Sahne yalnız alay değildir.",
            "Değer yaratmanın tehlikesi, eski itaati yeni logoyla tekrar etmektir.",
        ], "DÖRDÜNCÜ KISIM · YANLIŞ OKUMALAR", art="donkey-festival", caption="Eski put yıkılınca boşluk hemen yeni ve komik bir putla dolabilir; itaat yalnız logosunu değiştirir."),
        entry("Kartal ve yılan", [
            "Zerdüşt'ün hayvanları kartal ile yılandır: yükseklik ve gurur, toprak bilgeliği ve döngü. Birlikte tek taraflı kahramanlığı dengelerler.",
            "Yalnız yükselen kartal toprağı, yalnız sürünen yılan ufku kaybedebilir. Zerdüşt iki hareketi bir arada taşır.",
            "Hayvanlar ebedi dönüşü Zerdüşt'ten önce dile getirir, fakat onun kişisel dehşetini tam yaşamaz. Bilmek ile bedende üstlenmek farklıdır.",
            "Kitabın imgeleri kavramları tanımlamak yerine aralarında hareket alanı açar.",
        ], "DÖRDÜNCÜ KISIM · YANLIŞ OKUMALAR"),
        entry("Nazizmle kurulan sahte bağ", [
            "Nietzsche Alman milliyetçiliğini ve antisemitizmi eleştirmişti. Ölümünden sonra kız kardeşi Elisabeth yazılarını seçip düzenleyerek Nazi yorumuna uygun bir görüntü kurdu.",
            "Üstinsan biyolojik üstün ırk, güç istenci totaliter fetih programı değildir. Metnin sert ve hiyerarşik dili kötüye kullanıma açık olsa da bu eşitleme yanlıştır.",
            "Düşünürü aklamak için her sorunlu cümleyi silmek de gerekmez. Demokrasi ve eşitlik karşıtı yönleri eleştirel okunmalıdır.",
        ], "SON DURAKLAR"),
        entry("Kadınlar hakkındaki sorunlu sözler", [
            "Kitapta kadınlar hakkında küçümseyici, stereotip ve rahatsız edici bölümler bulunur. Bunları yalnız ironi diyerek geçmek metnin tarihsel cinsiyetçiliğini gizleyebilir.",
            "Zerdüşt karakterinin sözü ile Nietzsche'nin görüşü ayrımı yorum gerektirir, fakat okurun eleştirisini iptal etmez.",
            "Kendini aşma çağrısı, kadınları başkasının gelişim aracı yapan dilin de aşılmasını gerektirir.",
        ], "SON DURAKLAR"),
        entry("Bir ebedi dönüş alıştırması", [
            "Bugünkü bir seçimi sonsuz kez tekrar edeceğiniz varsayımıyla düşünün. Bu, her şeyi sevmek zorunda olduğunuz anlamına gelmez; hangi hayat parçasının değişim istediğini keskinleştirir.",
            "Sonra deve, aslan ve çocuk aşamalarını sorun: Hangi disiplini öğrenmeniz, hangi buyruğa hayır demeniz ve hangi yeni eveti yaratmanız gerekiyor?",
            "Alıştırma büyük kahramanlık değil küçük hayat biçimi için kullanılabilir.",
        ], "SON DURAKLAR"),
        entry("Bir cümlede kitabın özü", [
            "Eski Tanrı ve değerler güvenini kaybettiğinde insan ya son insanın rahatlığına çekilir ya da deve, aslan ve çocuk dönüşümünden geçerek bu hayatı tekrar isteyebileceği yeni değerler yaratır.",
            "Akılda kalacak görüntü iptir: İnsan tamamlanmış son değil, hayvan ile yaratıcı aşılma arasında düşme riskini taşıyan bir geçittir.",
        ], "SON DURAKLAR"),
    ]))


BOOKS.append(base(294, "Algı Kapıları", "Aldous Huxley",
    "Mescalin deneyinde çiçek, kumaş, mekan ve benlik algısının nasıl değiştiğini anlatan kısa ama etkili denemeyi sanat, mistisizm, beyin ve güncel güvenlik bilgisiyle; özendirmeden ve abartmadan açan rehber.",
    "#596D5B", "The Doors of Perception", "algi-kapilari",
    [
        {"id": 1, "title": "Encyclopaedia Britannica - The Doors of Perception", "url": "https://www.britannica.com/topic/The-Doors-of-Perception"},
        {"id": 2, "title": "NIDA - Psychedelic and Dissociative Drugs", "url": "https://nida.nih.gov/research-topics/psychedelic-dissociative-drugs"},
        {"id": 3, "title": "NIH - Psikedelik araştırmalarında güvenlik", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3056407/"},
        {"id": 4, "title": "Johns Hopkins Center for Psychedelic Research", "url": "https://hopkinspsychedelic.org/"},
    ], [
        entry("Önce açık güvenlik notu", [
            "Bu rehber mescalin veya başka bir psikedelik maddeyi kullanma talimatı vermez ve özendirmez. Etkiler kişiye, doza, sağlık durumuna ve ortama göre değişebilir; yoğun korku, kaza ve psikiyatrik sorun riski vardır.",
            "Huxley'nin 1953 deneyimi tıbbi gözetim altında yapılmış tek kişilik edebi tanıklıktır. Tek deney güvenlik veya tedavi kanıtı değildir.",
            "Güncel araştırmalar kontrollü klinik ortamda olası yararları inceler. Bu, denetimsiz kullanımın aynı sonucu vereceği anlamına gelmez.",
        ], "BAŞLANGIÇ"),
        entry("Bir bahar sabahındaki deney", [
            "Huxley psikiyatrist Humphry Osmond'un gözetiminde mescalin alır. Beklentisi renkli hayaller görmektir; karşılaştığı şey gündelik nesnelerin olağanüstü varlık yoğunluğudur.",
            "Oturma odası laboratuvar ve sahne olur. Sorular sorulur, ses kaydı alınır ve Huxley çevresine bakar.",
            "Bu bilimsel kontrollü deneyden çok yapılandırılmış gözlemdir. Beklenti, kişilik ve araştırmacıyla ilişki sonucu etkiler.",
            "Kitabın gücü genellemeden önce birinci kişi deneyimini ayrıntılı dile çevirmesidir.",
        ], "BİRİNCİ KISIM · DEĞİŞEN GÖRÜŞ", art="spring-experiment", caption="Huxley'nin oturma odası, gözetim altında gündelik nesnelerin değişen algısını izlediği tek kişilik deney sahnesine dönüşür."),
        entry("Çiçekler yalnız çiçek olmaktan çıkınca", [
            "Vazodaki çiçeklere bakarken onları tür ve fayda etiketiyle değil çıplak varoluş yoğunluğuyla gördüğünü anlatır. Renk ve biçim kendi başına yeterli görünür.",
            "Normalde 'çiçek' deyip geçtiğimiz nesneye ressam gibi uzun bakınca damar, gölge ve kıvrım belirir. Mescalin bu seçici alışkanlığı radikal biçimde değiştirir.",
            "Huxley deneyimi mistik 'olduğu gibi oluş' kavramına bağlar. Bu yorum deneyimin kendisinden ayrı felsefi adımdır.",
            "Yoğunluk gerçeğin nihai hali mi, beynin başka düzeni mi? Kitap soruyu açık bıraksa da çoğu yerde metafiziğe yaklaşır.",
        ], "BİRİNCİ KISIM · DEĞİŞEN GÖRÜŞ", art="intense-flowers", caption="Gündelik 'çiçek' etiketi geri çekildiğinde renk, damar ve biçim olağanüstü bir varlık yoğunluğu kazanır."),
        entry("Pantolondaki sonsuz kıvrımlar", [
            "Huxley gri pantolonunun kumaş kıvrımlarına bakar ve eski ustaların resimlerindeki kumaşların neden büyüleyici olduğunu anladığını söyler.",
            "Normal bakış kıyafeti 'giyilecek şey' diye hızla sınıflandırır. Değişen algı faydayı arka plana, ışık ile dokuyu öne alır.",
            "Bir nesnenin pratik işlevini kaybetmeden estetik varlığını görmek sanatın da yaptığı şeydir.",
            "Ancak yoğun dikkat her zaman yararlı değildir. Pantolon kıvrımında kaybolan kişi randevusuna yetişemez; algı seçimi yaşam için gereklidir.",
        ], "BİRİNCİ KISIM · DEĞİŞEN GÖRÜŞ", art="fabric-folds", caption="Sıradan kumaş işlev etiketi geri çekilince ışık, gölge ve kıvrımlardan oluşan zengin bir manzaraya dönüşür."),
        entry("Mekan ve zamanın değişmesi", [
            "Nesneler arasındaki mesafe alışılmış ölçüsünü kaybedebilir, zaman önemsiz veya geniş hissedilebilir. Saat aynı hızla ilerlerken yaşanan süre değişir.",
            "Sıkıcı bekleyişte beş dakika uzun, sevilen uğraşta bir saat kısa gelir. Psikedelik deney bu esnekliği çok daha güçlü hale getirebilir.",
            "Huxley sonsuz şimdiden söz eder. Plan ve geçmiş geri çekilince mevcut duyusal alan büyür.",
            "Bu deney felsefi zamanın kanıtı değildir; beynin zaman hissini nasıl kurduğuna dair kişisel ipucudur.",
        ], "BİRİNCİ KISIM · DEĞİŞEN GÖRÜŞ", art="expanded-time", caption="Saat değişmese de geçmiş ve gelecek geri çekildiğinde yaşanan şimdi geniş ve zamansız hissedilebilir."),
        entry("Benlik sesi kısıldığında", [
            "Huxley gündelik benliğin öneminin azaldığını, nesnelerin kendi varlığıyla öne çıktığını anlatır. Kişisel kaygıların merkez tahtı boşalır.",
            "Fotoğrafta sürekli kendi yüzünü izleyen pencere kapanınca oda fark edilir. Benlik filtresi çevreyi düzenleyen ama daraltan çerçeve olabilir.",
            "Benlik çözülmesi huzur kadar korku da yaratabilir. Kontrol kaybı bazı kişiler için yoğun panik veya dağılma hissidir.",
            "Huxley'nin olumlu deneyimi herkes için evrensel sonuç değildir.",
        ], "BİRİNCİ KISIM · DEĞİŞEN GÖRÜŞ", art="quiet-self", caption="Benlik sesi kısıldığında çevre daha geniş görünebilir; aynı çözülme başka kişide korku ve kontrol kaybı yaratabilir."),
        entry("Beyin azaltıcı vana mı?", [
            "Huxley, Bergson ve Broad'dan etkilenerek beynin geniş bir gerçeklik zihnini hayatta kalmak için daralttığını öne sürer. Mescalin bu azaltıcı vanayı gevşetiyor olabilir.",
            "Baraj kapağı bütün suyu bırakırsa şehir taşar; günlük zihin işe yarayan küçük akışı seçer. Filtre yaşamı mümkün kılar.",
            "Bu etkileyici metafor yerleşmiş nörobilim teorisi değildir. Beynin sonsuz dış zihin akışını filtrelediğine dair doğrudan kanıt yoktur.",
            "Modern araştırma algının seçici ve tahmine dayalı olduğunu destekler, fakat Huxley'nin metafizik sonucunu zorunlu kılmaz.",
        ], "İKİNCİ KISIM · ZİHİN VE SANAT", art="reducing-valve", caption="Azaltıcı vana metaforu beynin yaşamak için algı akışını daralttığını söyler, fakat bilimsel kanıtlanmış model değildir."),
        entry("Algı neden zaten filtredir?", [
            "Oda gözünüze milyonlarca ayrıntı sunar, siz kapı kolu ve aradığınız anahtarı seçersiniz. Dikkat görevle ilgili olanı öne çıkarır.",
            "Beyin pasif kamera değil geçmiş deneyimle tahmin kuran düzenleyicidir. Aynı gölgeyi bağlama göre yüz veya leke görebiliriz.",
            "Psikedelikler beyin ağları ve tahmin ağırlıklarını değiştirerek sıradan önem sıralamasını gevşetebilir; araştırma sürmektedir.",
            "Daha çok ayrıntı otomatik olarak daha doğru gerçeklik değildir. Filtre azalınca gürültü de artabilir.",
        ], "İKİNCİ KISIM · ZİHİN VE SANAT", art="attention-filter", caption="Dikkat anahtar ararken odayı seçer; filtre gevşediğinde ayrıntı artar ama önem ve gürültü de birbirine karışabilir."),
        entry("Sanatçılar kapıyı nasıl aralar?", [
            "Huxley ressamların kumaş, mücevher, manzara ve yüzlerde gündelik faydanın ötesini gösterdiğini düşünür. Sanat kimyasal olmadan algı alışkanlığını sarsabilir.",
            "Vermeer'in odası veya Van Gogh'un sandalyesi sıradan nesneyi yeni dikkatle kurar. Çerçeve, renk ve ritim seçici filtreyi değiştirir.",
            "Sanatçı her zaman mistik gerçekliği görmüş değildir; tarih, teknik ve emek de eseri açıklar.",
            "Yine de kitap sanat müzesini algı laboratuvarı olarak yeniden görmemizi sağlar.",
        ], "İKİNCİ KISIM · ZİHİN VE SANAT", art="art-opens-door", caption="Sanat gündelik nesnenin fayda etiketini geri çekip bakış alışkanlığında kimyasalsız bir kapı aralayabilir."),
        entry("Mücevher ve vitray neden büyüler?", [
            "Parlak taş, vitray ve altın ışığı yoğunlaştırır. Huxley bunların başka dünyaya açılan görsel deneyim sağladığını söyler.",
            "Karanlık kilisede renkli cam günlük sokak ışığını dönüştürür; mimari dikkati kutsal anlam yönünde düzenler.",
            "Lüks eşya ile mistik görüntü arasındaki bağ sınıf sorununu doğurur. Parlaklık zenginliğin gücünü de sergiler.",
            "Estetik yoğunluk toplumsal bağlamdan bağımsız değildir; sarayın taşı ile hacının ışığı aynı anda görülebilir.",
        ], "İKİNCİ KISIM · ZİHİN VE SANAT", art="stained-glass", caption="Vitray gündelik ışığı dönüştürerek başka dünya hissi verir, aynı zamanda kurum ve zenginliğin gücünü taşır."),
        entry("Şizofreni benzetmesinin sorunu", [
            "Huxley bazı değişmiş algıları şizofreni deneyimiyle karşılaştırır. Döneminde yaygın olan bu yaklaşım bugün aşırı ve damgalayıcı bulunabilir.",
            "Kısa süreli, seçilmiş ve destekli madde deneyimi ile istem dışı, uzun süreli psikoz aynı değildir. Kontrol ve işlev kaybı temel farktır.",
            "Psikedelikler bazı kişilerde psikotik belirtileri tetikleyebilir; kişisel veya ailevi risk özellikle önemlidir.",
            "Edebi benzerlik klinik eşitlik değildir. Güncel tıbbi bilgi romantik benzetmenin önüne geçmelidir.",
        ], "ÜÇÜNCÜ KISIM · MİSTİSİZM VE RİSK", art="different-experiences", caption="Seçilmiş kısa madde deneyimi ile istem dışı psikoz aynı kapı değildir; klinik farklar romantik benzetmeyle silinmemelidir."),
        entry("Mistik deney kanıt mıdır?", [
            "Birlik, zamansızlık ve kutsallık hissi yaşayan kişi için son derece gerçek olabilir. Fakat yoğun kesinlik hissi dış dünyanın metafizik yapısını tek başına kanıtlamaz.",
            "Rüyada da ikna edici anlam yaşayabiliriz. Deneyimin psikolojik değeri ile ontolojik iddia ayrı sorudur.",
            "Huxley farklı dinlerde benzer deneyimler görür ve ortak çekirdek düşünür. Kültür, beklenti ve dil yaşantının biçimini etkileyebilir.",
            "En dürüst tutum ne küçümsemek ne otomatik vahiy saymaktır; deneyimi ve iddiayı iki sütunda incelemektir.",
        ], "ÜÇÜNCÜ KISIM · MİSTİSİZM VE RİSK", art="mystical-certainty", caption="Mistik kesinlik deneyim olarak gerçek olabilir; dış dünyanın nihai yapısı hakkındaki iddia ayrıca gerekçe ister."),
        entry("Cennet ve cehennem aynı kapıda", [
            "Huxley sonraki denemelerinde değişmiş bilincin yalnız cennet gibi görüntüler değil korku, yalnızlık ve cehennem deneyimleri de açabileceğini anlatır.",
            "Algı filtresi gevşediğinde bastırılmış korku da yoğunlaşabilir. Kapının arkasında ne olduğunu kişi tam seçemez.",
            "Ortam, ruh hali ve destek sonucu etkiler; risk ortadan kalkmaz. Bedensel tehlike, etkileşim ve yasal durum ayrıca önemlidir.",
            "Kitabın güzel dili deneyimin karanlık ihtimalini gizlememelidir.",
        ], "ÜÇÜNCÜ KISIM · MİSTİSİZM VE RİSK", art="heaven-hell-door", caption="Aynı algı kapısı hayranlık kadar korku ve dağılma da açabilir; deneyimin yönü tam kontrol edilemez."),
        entry("Set ve setting", [
            "Kişinin beklentisi, ruh hali ve geçmişi 'set'; fiziksel ve sosyal çevre 'setting' diye anılır. Etki yalnız molekülden gelmez.",
            "Aynı müzik güvenli odada sakin, tehdit altında korkutucu duyulabilir. Değişmiş algıda bağlamın etkisi büyür.",
            "Klinik araştırmalar tarama, hazırlık, gözetim ve takip kullanır. Bunlar tedavinin dış süsü değil güvenliğin parçasıdır.",
            "Bu bilgi evde uygulama reçetesi değildir; kontrolsüz kullanım ile araştırma sonucunun neden eşit olmadığını açıklar.",
        ], "ÜÇÜNCÜ KISIM · MİSTİSİZM VE RİSK", art="set-and-setting", caption="Molekülün etkisi kişinin zihinsel durumu ve çevresiyle birleşir; klinik destek sonucun ayrılmaz parçasıdır."),
        entry("Huxley'nin iyimserliği", [
            "Huxley uygun kullanımla insanların daha az benmerkezci ve daha açık olabileceğini umar. Tek deneyin toplumu dönüştürme gücüne yaklaşır.",
            "Yoğun içgörü ertesi gün davranışa dönüşmeyebilir. Alışkanlık, ilişki ve kurumlar aynı kalırsa parlak anı hatıra olur.",
            "Bugünkü araştırmalar deneyim sonrası entegrasyonun önemini vurgular. Değişim yalnız kapıyı açmak değil görüleni yaşama taşımaktır.",
            "Kimyasal kısa yol, etik emeğin ve sosyal reformun yerine geçmez.",
        ], "DÖRDÜNCÜ KISIM · BUGÜNKÜ ARAŞTIRMA", art="insight-to-life", caption="Yoğun içgörü gündelik alışkanlık ve ilişkilere çevrilmezse parlak ama etkisiz bir hatıra olarak kalabilir."),
        entry("Tedavi araştırmaları ne söylüyor?", [
            "Psilosibin ve benzeri maddeler depresyon, bağımlılık ve yaşam sonu kaygısında kontrollü çalışmalarla araştırılıyor. Bazı sonuçlar umut vericidir.",
            "Çalışmalar seçilmiş katılımcı, ölçülü doz, eğitimli ekip ve uzun destek içerir. Plasebo körlüğü ve beklenti etkisi araştırmayı zorlaştırır.",
            "Umut verici, herkes için güvenli ve kesin tedavi demek değildir. Uzun dönem etki, karşılaştırma ve erişim soruları sürer.",
            "Huxley'nin tanıklığı tarihsel esin olabilir, klinik kılavuz değildir.",
        ], "DÖRDÜNCÜ KISIM · BUGÜNKÜ ARAŞTIRMA", art="clinical-research", caption="Umut verici klinik sonuçlar seçilmiş katılımcı ve yoğun destek içinde doğar; denetimsiz kullanıma doğrudan çevrilemez."),
        entry("Mikrodoz iddiaları", [
            "Günümüzde çok düşük dozların yaratıcılık ve ruh halini artırdığı iddia edilir. Anketler olumlu deneyim bildirirken kontrollü çalışmalarda beklenti etkisi önemli olabilir.",
            "Kişi aldığına inanarak daha dikkatli çalışabilir. Sonuç gerçek hissedilir, nedeni yalnız madde olmayabilir.",
            "Uzun dönem güvenlik ve ilaç etkileşimleri yeterince açık değildir. Popülerlik kanıt gücü değildir.",
            "Huxley'nin yüksek yoğunluklu deneyimini mikrodoz kültürüyle aynı şey saymak da tarihsel hatadır.",
        ], "DÖRDÜNCÜ KISIM · BUGÜNKÜ ARAŞTIRMA", art="microdose-claims", caption="Mikrodoz deneyiminde madde, beklenti ve davranış değişikliği birbirine karışabilir; popüler anlatı kontrollü kanıt değildir."),
        entry("Kimyasalsız algı kapıları", [
            "Meditasyon, sanat, doğa, nefes, müzik ve yoğun dikkat gündelik sınıflandırmayı gevşetebilir. Etkileri psikedelikle aynı değildir, fakat algının alışkanlık olduğunu gösterir.",
            "Bir nesneye beş dakika ad vermeden bakmak renk ve biçimi geri getirir. Müzede tek eser önünde kalmak hız filtresini yavaşlatır.",
            "Bu yollar da herkes için tamamen risksiz değildir; yoğun uygulama bazı kişilerde zorlayıcı olabilir. Ölçü ve destek önemlidir.",
            "Kitabın en güvenli mirası, dünyayı otomatik etiketlerin ötesinde yeniden görme merakıdır.",
        ], "DÖRDÜNCÜ KISIM · BUGÜNKÜ ARAŞTIRMA"),
        entry("Tek deneyden evren teorisi", [
            "Huxley kendi yoğun yaşantısından zihnin ve gerçekliğin yapısı hakkında geniş sonuçlar çıkarır. Edebi denemede bu cesaret etkileyicidir, bilimde ek kanıt ister.",
            "Azaltıcı vana, sonsuz zihin ve ortak mistik çekirdek kanıtlanmış gerçekler değil yorum çerçeveleridir.",
            "Kitabı değerli kılmak için her metafiziğini kabul etmek gerekmez. Algının seçici olduğunu güçlü biçimde hissettirir.",
        ], "SON DURAKLAR"),
        entry("Kültürel etkisi ve yanlış mirası", [
            "Kitap 1960'ların karşı kültürünü ve The Doors grubunun adını etkiledi. Psikedelik deneyin sanatsal ve manevi imgesi genişledi.",
            "Popüler miras çoğu zaman Huxley'nin gözetim, entelektüel hazırlık ve risk ayrıntısını atıp yalnız kapı açma heyecanını aldı.",
            "Bir eserin kültürel etkisi yazarın kontrolünü aşar. Okur etkileyici imgeyi güncel güvenlik bilgisiyle dengelemelidir.",
        ], "SON DURAKLAR"),
        entry("Beş dakikalık görme alıştırması", [
            "Güvenli ve sıradan bir nesne seçin. Adını, fiyatını ve işlevini düşünmeden yalnız renk, kenar, gölge ve dokusuna beş dakika bakın.",
            "Sonra normal dikkatin hangi ayrıntıları elediğini yazın. Filtrenin düşman değil işlevsel seçim olduğunu da hatırlayın.",
            "Amaç değişmiş bilinç taklidi değil gündelik görmenin ne kadar hızlı sınıflandırdığını fark etmektir.",
        ], "SON DURAKLAR"),
        entry("Bir cümlede kitabın özü", [
            "Huxley mescalin deneyinde gündelik benlik ve fayda filtresi gevşediğinde sıradan nesnelerin olağanüstü yoğun göründüğünü anlatır; bu tanıklık algıya açılan soru, güvenlik veya metafizik için son kanıt değildir.",
            "Akılda kalacak görüntü pantolon kıvrımıdır: Her gün gördüğümüz şey değişmez, onu eleyen ve önem sırasına koyan zihin değiştiğinde dünya başka görünür.",
        ], "SON DURAKLAR"),
    ]))


if __name__ == "__main__":
    write_books(BOOKS)
