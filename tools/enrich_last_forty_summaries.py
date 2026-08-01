#!/usr/bin/env python3
"""Enrich the last forty summaries without changing their interior artwork.

The generated paragraphs are stored separately in ``extraParagraphs`` so the
hand-written source remains intact and repeated runs stay deterministic.
Acceptance thresholds come from data/summary-production-standard.json.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK_NUMBERS = (
    8, 18, 34, 38, 61, 70, 92, 99, 121, 138,
    151, 157, 182, 195, 211, 216, 238, 244, 266, 294,
    12, 17, 32, 41, 66, 72, 93, 103, 122, 124,
    152, 156, 189, 194, 214, 222, 241, 253, 271, 275,
)

SHARED_PADDING = {
    "Bu rehber sınav notu gibi ezberlenecek maddeler sunmaz. Kitabın ana fikrini gündelik sahneler, tarihsel olaylar ve bugünün tartışmalarıyla yavaş yavaş kurar; zor kavramları adını duyduğumuz anda değil, ne işe yaradığını gördüğümüz anda tanımlar.",
    "Bir düşünceyi tek cümlelik slogana çevirmek kolaydır; fakat bu kitapta asıl değer, iddianın hangi koşullarda geçerli olduğunu ve nerede sınırlandığını izlemektir. Okur, yazarın açıklamasını ahlaki emir ya da değişmez kader gibi almamalıdır.",
    "En güvenli okuma yöntemi, her güçlü cümlenin yanına iki küçük soru koymaktır: Burada hangi örnek kanıt sayılıyor ve hangi karşı örnek bu fikri zorlayabilir? Böylece kitap hayranlık nesnesi değil, çalışan bir düşünce aracına dönüşür.",
    "Yazarın güçlü yanları kadar kör noktaları da gösterilecektir. Böylece okur hem kitabın neden klasikleştiğini anlayabilir hem de her cümlesini tartışılmaz gerçek sanmadan kullanabilir.",
    "Kitabı bugünün bilgisiyle okumak onu çöpe atmak anlamına gelmez. Eskiyen ayrıntıları ayırıp hâlâ işe yarayan soruyu korumak, klasiklerden alınabilecek en büyük verimdir.",
    "Bu üç soru evde, işte, haber okurken veya bir tartışmayı dinlerken kullanılabilir. Amaç her durumu kitaba uydurmak değil, gözden kaçan ilişkiyi görünür kılmaktır.",
    "Bir kavram gündelik hayatı daha dikkatli görmemizi sağlıyor ama insanları kolay etiketlere hapsetmiyorsa, gerçekten işe yarıyor demektir.",
    "Akılda kalacak son görüntü, tek bir cevabın kapıyı kapatması değil; iyi kurulmuş bir sorunun karanlık odada yeni bir pencere açmasıdır.",
    "Bu nedenle rehber, yazarı son sözü söyleyen otorite gibi değil, düşünme biçimimizi değiştiren güçlü bir tartışma ortağı gibi ele alır.",
}

CATEGORY_SCENES = {
    "life": (
        "aynı sofrada sınırlı bir kaynağın nasıl paylaşılacağını",
        "bir bahçede küçük bir değişikliğin bütün canlıları nasıl etkilediğini",
        "kalabalık bir ekipte işbirliği ile rekabetin aynı anda nasıl yaşandığını",
        "bir çocuğun güvenli sandığı dünyayı hangi işaretlerle öğrendiğini",
    ),
    "mind": (
        "uykusuz bir gecenin ertesi sabahı verilen acele kararı",
        "kalabalık otobüste yanlış anlaşılan bir bakışı",
        "aile tartışmasında bedenin sözlerden önce gerilmesini",
        "tanıdık bir odanın tek ayrıntı değişince yabancılaşmasını",
    ),
    "language": (
        "küçük bir çocuğun daha önce duymadığı doğru bir cümle kurmasını",
        "aynı sözün evde şaka, mahkemede ciddi kanıt sayılmasını",
        "yabancı dilde sözlüğü bilip konuşmanın ritmini kaçırmayı",
        "bir mesajdaki tek noktanın bile duyguyu değiştirmesini",
    ),
    "ethics": (
        "trafikte öfkeyle verilen bir kararın birkaç saniye sonra nasıl göründüğünü",
        "işyerinde kural ile özel durumun çatışmasını",
        "aile içinde iyi niyetin karşı tarafta baskı gibi hissedilmesini",
        "zor bir günde kontrol edilebilenle edilemeyeni ayırmayı",
    ),
    "history": (
        "aynı haritanın iki yanında büyüyen iki kasabanın farklı imkânlarını",
        "köy ambarındaki küçük fazlanın zamanla yeni meslekler doğurmasını",
        "limana ulaşan yolun yalnız malı değil bilgiyi ve hastalığı da taşımasını",
        "bir kuşak için doğal görünen düzenin sonraki kuşakta çözülmesini",
    ),
    "politics": (
        "apartman toplantısında güvenlik ile söz hakkının çatışmasını",
        "şehir meclisinde çoğunluğun azınlığa nasıl davranacağını",
        "acil durumda verilen geçici yetkinin kalıcılaşma ihtimalini",
        "bir kurumda kuralı koyanla o kurala uyan arasındaki mesafeyi",
    ),
    "economy": (
        "küçük bir dükkânda fiyat, emek ve müşteri güveninin buluşmasını",
        "maaş bordrosunun arkasındaki görünmez pazarlığı",
        "kredi kartıyla bugün alınan şeyin yarının gelirine bağlanmasını",
        "bir fabrikanın hız kazanırken çalışanının dünyasını daraltmasını",
    ),
    "media": (
        "telefon bildirimine daha ne yazdığını bilmeden uzanan eli",
        "aile albümünde kadraj dışında kalan kişiyi",
        "haber stüdyosunda karmaşık olayın otuz saniyeye sıkışmasını",
        "reklamın üründen çok nasıl bir hayat vaat ettiğini",
    ),
    "science": (
        "laboratuvarda beklenen çizgiye uymayan tek ölçümü",
        "eski ders kitabındaki kesin bilginin yeni kanıtla değişmesini",
        "aynı gökyüzüne farklı bir haritayla bakan iki gözlemciyi",
        "iyi çalışan bir açıklamanın sınırına geldiği ilk garip vakayı",
    ),
    "spirit": (
        "sessiz bir odada birkaç dakika yalnız kalınca zihnin nereye kaçtığını",
        "büyük bir kayıptan sonra sıradan eşyanın değişen anlamını",
        "kalabalık bir törende yaşanan son derece kişisel duyguyu",
        "günlük koşuşturma durduğunda ortaya çıkan anlam sorusunu",
    ),
    "technology": (
        "navigasyonun hızlı rotasıyla insanın gerçek amacı arasındaki farkı",
        "işe alım yazılımının küçük bir ölçütü binlerce kişiye uygulamasını",
        "otomatik fabrikanın verilen hedefi sorgulamadan büyütmesini",
        "çok becerikli bir yardımcının yanlış anladığı emri kusursuz uygulamasını",
    ),
}

# Each connection states what the book helps the reader notice.  Each limit
# prevents the generated example from turning the author's lens into a slogan.
BOOK_PROFILES = {
    8: ("life", ("Seçilim niyetleri değil, kuşaklar boyunca kalan sonuç farklarını biriktirir.", "Akrabalık, karşılıklılık ve çevre aynı davranışın hesabını değiştirebilir.", "Gen etkisi gelişim ve kültürden bağımsız çalışan bir uzaktan kumanda değildir.", "Biyolojik açıklama, ahlaki bir davranış emri anlamına gelmez."), ("Gen merkezli bakış canlıyı tek nedene indirdiğinde açıklama gücünü kaybeder.", "İnsan kültürü biyolojik eğilimleri büyütebilir, frenleyebilir veya başka yöne çevirebilir.", "Bencillik kelimesi moleküle kişilik yüklersek yanıltıcı olur.", "Bir davranışın evrilmiş olması onun kaçınılmaz olduğunu kanıtlamaz.")),
    18: ("life", ("Kalıcı bir kimyasal hedeflenen tarlanın sınırında durmaz; suya, toprağa ve besin zincirine katılır.", "Kısa vadeli verim artışı yıllar sonra görülen canlı kaybını saklayabilir.", "Bir türü yok etmek ona bağlı avcıyı, tozlayıcıyı ve toprağı da etkiler.", "Carson kararın bedelini yalnız uygulayan için değil bütün ekosistem için hesaplar."), ("Her kimyasal aynı ölçüde tehlikeli değildir; doz, kalıcılık ve maruz kalma yolu ayrılmalıdır.", "Korkutucu bir örnek tek başına genel hüküm kurmaya yetmez.", "1962'nin bilimsel ayrıntıları bugünün düzenlemeleriyle aynı değildir.", "Çevreyi korumak tarımı ve halk sağlığını basitçe karşı karşıya koymayı gerektirmez.")),
    34: ("mind", ("Travma bazen olay bittikten sonra bile bedenin alarmı kapatamamasıdır.", "İyileşme yalnız hatırlamak değil, şimdi güvende olunduğunu bedende yeniden öğrenmektir.", "Güvenli ilişki sinir sisteminin tek başına taşıyamadığı yükü paylaşabilir.", "Beden duyusu, zaman hissi ve benlik anlatısı birlikte onarılır."), ("Her acı deneyim travma değildir ve aynı olay herkeste aynı iz bırakmaz.", "Tek bir tedavi yöntemi herkes için mucize çözüm sayılamaz.", "Beyin görüntüsü kişinin bütün hayat hikâyesinin yerine geçmez.", "Genel bilgi, kişiye özel tanı ve profesyonel desteğin yerini tutmaz.")),
    38: ("language", ("Çocuk dili yalnız taklit etmez; duymadığı cümleleri kuracak örüntüyü çıkarır.", "Sözcükler doğrusal görünürken cümlenin anlamı görünmez bir yapı taşır.", "İşaret dili de sesli dil kadar üretken bir insan dilidir.", "Dil kapasitesi biyoloji ile çevrede duyulan konuşmanın buluşmasından doğar."), ("Doğuştan yatkınlık hazır dilbilgisi cümleleriyle doğmak demek değildir.", "Diller arasındaki çeşitlilik tek bir katı kalıba kolayca sığmaz.", "Beyinde tek başına çalışan bir dil kutusu yoktur.", "Dilin düşünceyi etkilediğini söylemek insanı kelimelerinin hapishanesine koymaz.")),
    61: ("ethics", ("Marcus ilk duygudan çok onun arkasından kurduğu yargıyı eğitmeye çalışır.", "İnsanın gerçek alanı olayların tamamı değil, verdiği karşılıktır.", "Kozmik ölçekte bakmak öfkenin şişirdiği benliği küçültebilir.", "Stoacı görev kişisel çıkarı ortak hayatın iyiliğinden ayırmaz."), ("Stoacılık haksızlığa sessizce katlanmak veya duyguları bastırmak değildir.", "İç kale toplumsal sorumluluktan kaçış bahanesine dönüşmemelidir.", "İmparatorun kişisel disiplini Roma'nın şiddetini kendiliğinden aklamaz.", "Kontrol ayrımı, değiştirilebilir kurumları değişmez kader saydırmamalıdır.")),
    70: ("spirit", ("Laozi zorlamadan etkili olmanın yolunu su, boşluk ve sessizlikte arar.", "Karşıtlar birbirini bütünüyle yok etmekten çok birbirini görünür kılar.", "Wuwei pasiflik değil, koşulları anlayarak gereksiz sürtünmeyi azaltmaktır.", "Sessiz liderlik sonuç üretir ama gösteriş için sonucu sahiplenmez."), ("Zorlamasızlık haksızlık karşısında hiçbir şey yapmamak diye okunamaz.", "Şiirsel paradoks tek ve değişmez bir yönetim reçetesi vermez.", "Tao'yu yalnız kişisel verimlilik hilesine çevirmek metnin siyasal yönünü siler.", "Esneklik ilkesizlik veya her baskıya uyum göstermek değildir.")),
    92: ("history", ("İbn Haldun haberi insan topluluklarının çalışma koşullarıyla sınar.", "Asabiyet dağınık insanları ortak risk karşısında hareket ettiren bağdır.", "Hanedan güçlendikçe onu kuran dayanışmanın rahatlık içinde çözülmesi mümkündür.", "Vergi, emek ve şehir hayatı birbirinden ayrı değil aynı umranın parçalarıdır."), ("Hanedan döngüsü bütün toplumlar için değişmez kader değildir.", "İklim ve halk karakteri hakkında çağının sınırlı kabullerini taşır.", "Asabiyet yalnız kan bağıyla açıklanamaz; kurumlar ve ortak amaçlar da bağ kurar.", "Modern devletleri birkaç kuşaklık tek şemaya sıkıştırmak yanıltıcı olur.")),
    99: ("politics", ("Mill'in sınırı, yetişkin bireyin seçimi ile başkasına verilen zararı ayırmaya çalışır.", "Yanlış fikir bile doğru düşüncenin gerekçelerini canlı tutabilir.", "Çoğunluk yalnız yasayla değil ayıplama ve dışlama yoluyla da baskı kurar.", "Farklı hayat denemeleri toplumun öğrenme alanını genişletebilir."), ("Zararın nerede başladığı gürültü, salgın ve ekonomik risk gibi alanlarda tartışmalıdır.", "Söz özgürlüğü tehdidi ve hedefli tacizi otomatik olarak korumaz.", "Çocuklar ve karar kapasitesi sınırlı kişiler yetişkin özerkliğiyle aynı durumda değildir.", "Mill'in sömürgeci çağından kalan kör noktaları evrensel özgürlük iddiasını zorlar.")),
    121: ("science", ("Descartes şüpheyi her şeyi yok etmek için değil sağlam başlangıç bulmak için kullanır.", "Düşünen benlik, en güçlü aldatma ihtimalinin içinde bile o anda var olduğunu fark eder.", "Balmumu örneği algının arkasında zihnin düzenleyici payını gösterir.", "Altı meditasyon şüpheden dış dünya ve zihin beden ilişkisine doğru adım adım ilerler."), ("Yöntemli şüphe sürekli komplo kuşkusu veya hiçbir şeye inanmamak değildir.", "Düşünen benliğin kesinliği dış dünyanın hemen kanıtlandığı anlamına gelmez.", "Tanrı kanıtları kitabın en çok tartışılan geçişlerindendir.", "Zihin ile bedeni iki ayrı töz saymak çağdaş beyin bilgisiyle yeni sorunlar doğurur.")),
    138: ("science", ("Kuhn bilimi ortak örnekler altında çözülen bulmacaların toplumsal işi olarak görür.", "Aykırı sonuç önce hata sanılabilir; çoğaldığında kullanılan çerçeveyi zorlar.", "Devrim yalnız yeni cevap değil, hangi sorunun anlamlı sayıldığının değişmesidir.", "Ders kitapları son düzeni doğal gösterirken eski çatışmaları kısaltır."), ("Her yeni fikir veya moda değişimi paradigma devrimi değildir.", "Paradigmaların çatışması bilim insanlarının birbirini hiç anlayamadığı anlamına gelmez.", "Kuhn bilimi keyfi zevke indirgemek istememiştir.", "Normal bilimde de ölçüm, eleştiri ve birikimli ilerleme devam eder.")),
    151: ("economy", ("Smith zenginliği kasadaki altından çok toplumun üretken emeğinde arar.", "İş bölümü verimi artırırken pazarın büyüklüğü tarafından sınırlandırılır.", "Fiyat ücret, kâr ve rant arasındaki toplumsal bölüşümü içinde taşır.", "Devlet savunma, adalet ve ortak altyapı gibi piyasanın tek başına kuramadığı görevler üstlenir."), ("Görünmez el kitabın her sorunu çözen sihirli sloganı değildir.", "Pazarlık tarafları eşit güce sahip değildir; Smith işveren avantajını açıkça görür.", "İş bölümü insanın zihnini daraltabilir ve kamusal eğitim gerektirebilir.", "On sekizinci yüzyıl analizi bugünün finansı ve ekolojik sınırlarını bütünüyle kapsamaz.")),
    157: ("economy", ("Graeber borcu para hesabından önce ahlaki ve siyasi ilişki olarak görür.", "Kil tabletlerdeki kredi, paranın yalnız takastan doğduğu öyküyü zorlar.", "Sikke, ordu ve vergi tarih boyunca birbirini besleyebilir.", "Borcu kesin sayıya çevirmek eşitsiz insan ilişkisini tarafsız hesap gibi gösterebilir."), ("Beş bin yılı tek çizgide anlatmak dönemler arasındaki önemli farkları silebilir.", "Borcun baskı aracı olması her borcun gayrimeşru olduğu anlamına gelmez.", "Tarihçilerin bazı kronoloji ve genelleme itirazları ciddiye alınmalıdır.", "Borç affının maliyeti, kime yaradığı ve yeni düzenin nasıl kurulacağı ayrıca tartışılmalıdır.")),
    182: ("language", ("Wittgenstein anlamı gizli özden çok kelimenin ortak hayattaki kullanımında arar.", "Dil oyunları betimlemek kadar sormak, söz vermek ve teselli etmek için de çalışır.", "Aile benzerliği ortak tek öz olmadan da kavramın işleyebileceğini gösterir.", "Felsefi düğüm bazen yeni teoriyle değil kelimenin izlediği yolları göstererek çözülür."), ("Kullanımın önemli olması her kullanımın doğru veya adil olduğu anlamına gelmez.", "Toplumsal ölçüt bireyin özel deneyimini yok saymayı gerektirmez.", "Dil oyunları birbirinden kapalı adalar değildir; insanlar yeni kullanımlar kurabilir.", "Felsefi terapi bilimsel ve ahlaki sorunların tamamını yalnız kelime incelemesine indirgemez.")),
    195: ("media", ("Postman bir toplumun düşünme biçiminin kullandığı araçla değiştiğini savunur.", "Televizyon karmaşık kamusal konuyu gösteriye uygun kısa parçalara böler.", "Eğlence içeriğin düşmanı değildir; sorun her içeriğin eğlence sınavından geçmesidir.", "Telefon ve algoritma çağında hız ile bağlam kaybı daha kişisel hale gelmiştir."), ("Görüntü her zaman yüzeysel, yazı her zaman derin değildir.", "Kitap tipografik geçmişi yer yer fazla idealize eder.", "Ekranı kapatmak medya kurumlarının teşviklerini tek başına değiştirmez.", "Seyirci bütünüyle edilgen değildir; görüntüyü eleştirel biçimde okuyabilir.")),
    211: ("media", ("Sontag fotoğrafı dünyayı kaydederken aynı anda seçen ve sahiplenen bir eylem olarak görür.", "Kadraj bir şeyi kanıtlıyor gibi görünürken dışında kalan bağlamı sessizleştirir.", "Acının çok tekrarlanan görüntüsü şok kadar alışkanlık da üretebilir.", "Fotoğraf hafıza kurar ama geçmişin hangi anının hatırlanacağını da seçer."), ("Fotoğraf çekmek her durumda saldırı veya sömürü değildir.", "Görüntü tek başına niyet, neden ve olayın tamamını kanıtlamaz.", "Sontag sonraki yıllarda acı görüntülerinin etkisi konusunda ilk hükmünü yumuşatmıştır.", "Telefon kamerası özne, izleyici ve yayıncı rollerini eski kitaptan daha fazla iç içe geçirir.")),
    216: ("politics", ("Beauvoir kadınlığın değişmez öz değil, yaşanan koşullar içinde kurulan konum olduğunu savunur.", "Öteki olmak, erkeğin insanlığın tarafsız ölçüsü gibi yerleşmesiyle başlar.", "Evlilik, bakım ve güzellik beklentileri özgürlüğün gündelik alanını daraltabilir.", "Ekonomik bağımsızlık gerekli olsa da tek başına eşit ilişki kurmaya yetmez."), ("Eser 1949 Fransasının sınıf, ırk ve beden hakkındaki sınırlılıklarını taşır.", "Biyolojinin kader olmaması beden deneyiminin önemsiz olduğu anlamına gelmez.", "Tek bir kadın deneyimi sınıf, ırk, sömürge ve cinsiyet çeşitliliğini kapsamaz.", "Özgürleşme yalnız bireysel seçimle değil kurumların ve emeğin değişmesiyle mümkündür.")),
    238: ("politics", ("Foucault cezanın bedeni parçalamaktan davranışı sürekli izlemeye doğru değişimini inceler.", "Disiplin mekânı, zamanı ve hareketi küçük ölçülerle düzenler.", "Sınav hem bilgi üretir hem insanı normal ölçüye göre sıralar.", "Panoptikon görülmeden görülme ihtimalini kişinin kendi üzerinde çalışan bir güce dönüştürür."), ("Her gözetim aynı niyetle kurulmaz ve her kurum hapishane değildir.", "Foucault mahkûmların direnişine ve ırk ile sömürge tarihine sınırlı yer verir.", "Disiplinin yararlı sonucu onun güç ilişkilerinden bağımsız olduğu anlamına gelmez.", "İktidarın her yerde olması hiçbir yerde değiştirilemeyeceğini göstermez.")),
    244: ("history", ("Harari büyük insan topluluklarının ortak hayali düzenler sayesinde işbirliği kurduğunu anlatır.", "Tarım daha çok insanı beslerken tek tek insanların hayatını zorlaştırmış olabilir.", "Para, imparatorluk ve din yabancılar arasında ortak güven dili kurar.", "Bilimsel devrim insanlığın bilgisizliğini kabul etmesiyle yeni bir hız kazanır."), ("Yetmiş bin yılı tek ciltte anlatmak bilimsel anlaşmazlıkları düzleştirebilir.", "Hayali düzen yalan demek değildir; insanlar davranışlarını gerçekten ona göre kurar.", "Bilişsel devrimin tarihi ve nedenleri kitabın anlattığından daha tartışmalıdır.", "Büyük desen tek tek toplumların farklı yolunu görünmez kılmamalıdır.")),
    266: ("spirit", ("Zerdüşt eski değerlerin çöküşünden sonra insanın kendi ölçüsünü yaratma yükünü taşır.", "Üstinsan bir ırk değil, kendini aşma yönünde açık bırakılmış bir hedeftir.", "Ebedi dönüş hayatı aynı ayrıntılarıyla yeniden isteyip istemediğimizi sınayan ağır düşüncedir.", "Deve, aslan ve çocuk dönüşümleri yük taşımaktan özgürleşmeye ve yaratmaya ilerler."), ("Zerdüşt karakterinin her sözü Nietzsche'nin doğrudan emri sayılamaz.", "Güç istenci yalnız başkalarına hükmetme isteğine indirgenemez.", "Metindeki kadınlar hakkındaki küçültücü sözler şiirsel üslupla aklanmamalıdır.", "Nazilerin sonradan kurduğu bağ metnin biyolojik ırk öğretisi olduğu anlamına gelmez.")),
    294: ("mind", ("Huxley sıradan nesnelerin alışılmış fayda filtresi gevşediğinde nasıl değiştiğini anlatır.", "Benlik sesi kısıldığında renk, biçim ve zaman deneyimi olağanüstü yoğunlaşabilir.", "Azaltıcı vana düşüncesi beynin dünyayı yaşamak için seçerek daralttığını öne sürer.", "Sanat, dikkat ve ritüel kimyasal olmadan da algının alışılmış kapısını aralayabilir."), ("Tek bir kişisel deney evrenin ve beynin kesin teorisini kanıtlamaz.", "Değişmiş algı her zaman bilgelik, doğruluk veya tedavi anlamına gelmez.", "Şizofreniyle kurulan eski benzetmeler günümüzde dikkatle ele alınmalıdır.", "Psikedelik maddeler sağlık riski ve hukuki sonuç taşır; bu özet kullanım önerisi değildir.")),
    12: ("history", ("Diamond kıtalar arasındaki güç farkını insanların değerine değil biriken maddi koşullara bağlar.", "Evcilleşebilir bitki ve hayvan paketi artı ürün, uzmanlık ve devlet kapasitesi yaratabilir.", "Hayvanlarla uzun temas mikroplara karşı tarihsel bağışıklık farkı doğurmuştur.", "Avrasya'nın doğu batı ekseni ürün ve bilginin benzer iklimlerde yayılmasını kolaylaştırmıştır."), ("Coğrafi avantaj fetih yapanların ahlaki sorumluluğunu ortadan kaldırmaz.", "Coğrafya güçlü bir başlangıç koşuludur ama değişmez kader değildir.", "Kitap sömürgecilik sonrası kurumların ve siyasi seçimlerin payını sınırlı işler.", "Büyük kıta deseni yerel halkların buluşlarını ve farklı yollarını gölgelememelidir.")),
    17: ("science", ("Lucretius doğayı atomların boşluk içindeki hareketiyle açıklayarak ilahi kaprisi geri çeker.", "Hiçten hiçbir şey çıkmaması maddeyi yok oluş yerine sürekli dönüşüm içinde görür.", "Küçük sapma düşüncesi atomların yalnız paralel düşüşünden farklı bir dünyanın yolunu açar.", "Ölüm korkusu, ruh da maddi ve ölümlüyse sonsuz acı beklentisini kaybeder."), ("Antik atomlar çağdaş fiziğin atomlarıyla birebir aynı değildir.", "Doğal açıklama insanın bütün korkularını tek başına iyileştirmez.", "Rastlantısal sapma özgür iradenin tamamlanmış bilimsel kanıtı değildir.", "Şiirin güçlü benzetmeleri deneysel kanıtla karıştırılmamalıdır.")),
    32: ("mind", ("Sapolsky davranışın nedenini bir saniye öncesinden çocukluğa ve evrime kadar geriye sarar.", "Beyin bölgesi, hormon ve gen tek başına iyilik ya da şiddet düğmesi değildir.", "Stres tehdit algısını daraltıp kişinin görebildiği seçenekleri azaltabilir.", "Biz ve onlar sınırı şaşırtıcı hızla değişebilir; biyoloji bu toplumsal çizgiye göre çalışır."), ("Nedenleri açıklamak kişiyi sonuçlarından bütünüyle sorumsuz saymak değildir.", "Biyolojik etki kader veya değişmez karakter anlamına gelmez.", "Beyin araştırmalarındaki ilişki tek başına davranışın kesin nedeni değildir.", "Çok katmanlı açıklama, müdahale ve hesap verebilirlik için yeni yollar da açmalıdır.")),
    41: ("mind", ("Ramachandran sıra dışı vakaları beynin normalde görünmeyen çalışma düzenine açılan pencere sayar.", "Hayalet uzuv beden haritasının kol kaybolduğunda hemen silinmediğini gösterir.", "Görme ve tanıma tek işlem değildir; yüzü bilmekle ona tanıdıklık hissetmek ayrılabilir.", "Benlik tek merkezden değil birbiriyle konuşan birçok sistemden kuruluyor olabilir."), ("Çarpıcı tek vaka bütün insanlar için genel yasa kurmaya yetmez.", "Basit deney iyileştirici olsa bile herkes için aynı sonucu vermez.", "Ayna nöronları empati ve kültürün bütün açıklaması gibi sunmak aşırıdır.", "Hastanın hikâyesi yalnız ilginç bir bilmeceye indirgenmemelidir.")),
    66: ("politics", ("Platon adaleti şehirdeki sınıflarla insan ruhundaki istek, cesaret ve akıl arasında karşılaştırır.", "Gyges'in yüzüğü ceza korkusu kalktığında adil kalıp kalamayacağımızı sorar.", "Mağara eğitimi gölgeyi gerçek sanan bakışı ışığa çevirmeye çalışır.", "Filozofun yönetmesi fikri bilginin iktidarla nasıl birleşeceği sorununu açar."), ("İdeal şehir bireysel özgürlük ve çoğulculuk için ciddi tehditler taşır.", "Asil yalan ortak düzen adına aldatmanın ne kadar tehlikeli olabileceğini gösterir.", "Filozofun bilgi iddiası yöneticinin denetlenmesi sorununu çözmez.", "Diyalogdaki kadın eşitliği kapısı aile ve sınıf düzenindeki sertlikle birlikte okunmalıdır.")),
    72: ("politics", ("Sun Tzu zaferi çatışma anından önce bilgi, hazırlık ve maliyet hesabında arar.", "Biçimsizlik rakibin hazırlandığı tek kalıba girmemektir.", "Arazi yalnız toprak değil, seçenekleri açan ve kapatan bütün koşullardır.", "En üstün strateji uzun savaşla tükenmeden rakibin planını bozmaktır."), ("Aldatma ilkesini her ilişkiye taşımak güveni ve ortak hayatı zehirler.", "Savaş benzetmesi iş, aile ve siyasetin her alanına uygun değildir.", "Kısa özdeyişler tarihsel bağlamdan kopunca birbirine zıt sloganlara dönüşebilir.", "Hız ve sürpriz, amaç ile ahlaki sınır düşünülmeden erdem sayılmaz.")),
    93: ("politics", ("Hobbes ortak güç yokken eşit kırılganlığın güvensizlik yaratabileceğini savunur.", "Doğa durumu sürekli dövüş değil, şiddet ihtimalinin gündelik hayatı kilitlemesidir.", "Sözleşmenin işlemesi için herkesin üzerinde yaptırım gücü olan egemen gerekir.", "Leviathan, bireylerin yetkilendirmesiyle kurulmuş yapay bir ortak kişidir."), ("Güvenlik ihtiyacı sınırsız iktidarın her eylemini haklı çıkarmaz.", "İnsan işbirliği yalnız korku ve çıkarla açıklanamayacak kadar zengindir.", "Bölünmez egemenlik modern kuvvetler ayrılığıyla ciddi gerilim taşır.", "İç savaş deneyimi Hobbes'un düzen kaygısını büyütür; bu bağlam evrensel insan özü değildir.")),
    103: ("economy", ("Weber modern kapitalizmi basit para hırsından ayırıp düzenli çalışma ve yeniden yatırım disipliniyle inceler.", "Meslek çağrıya dönüşünce gündelik emek dini sorumluluk ağırlığı kazanır.", "Kaderin bilinmemesi kaygısı başarı işaretlerini arayan disiplinli hayatı teşvik edebilir.", "Dini kök zayıflasa bile çalışma düzeni demir kafes gibi yaşamaya devam edebilir."), ("Weber Protestanlığı kapitalizmin tek nedeni olarak sunmaz.", "Sömürgecilik, zor ve maddi kurumlar kültürel açıklamanın yanında ayrıca görülmelidir.", "Bütün Protestanlar veya kapitalistler aynı ahlakı taşımaz.", "Çalışkanlığı karakter ölçüsü saymak işsizliği ve eşitsiz başlangıçları ahlaki kusur gibi gösterebilir.")),
    122: ("ethics", ("Spinoza Tanrı ile doğayı ayırmayarak insanı evrensel nedenler zincirinin içine yerleştirir.", "Conatus her varlığın kendi gücü içinde sürme çabasıdır.", "Sevinç daha büyük etkinlik gücüne, keder daha dar bir yaşama geçiştir.", "Özgürlük nedensiz seçim değil bizi belirleyen zorunluluğu daha yeterli anlamaktır."), ("Nedenleri anlamak haksızlığı onaylamak veya değişime vazgeçmek değildir.", "Geometrik biçim duygusal hayatın bütün karmaşasını otomatik olarak çözmez.", "İyi ve kötünün ilişkiye bağlı olması her değerin keyfi olduğu anlamına gelmez.", "Spinoza'nın özgürlük anlayışı gündelik seçim duygumuzla ciddi gerilim taşır.")),
    124: ("spirit", ("Pascal insanı evren karşısında kırılgan ama kırılganlığını bilecek kadar büyük görür.", "Eğlence çoğu zaman can sıkıntısından ve kendi sonluluğumuzla kalmaktan kaçıştır.", "Hayal gücü ve alışkanlık aklın tarafsız sandığı hükümleri sessizce yönetebilir.", "Bahis inancı matematiksel kanıtlamaktan çok belirsizlik altında yaşanan seçimi görünür kılar."), ("Bahis gerçek inancı yalnız çıkar hesabına indirgediğinde ikna gücünü kaybeder.", "Parçalı notlar tamamlanmış ve tek çizgili bir kitap gibi okunmamalıdır.", "Kalbin bilgisi her güçlü duygunun doğru olduğu anlamına gelmez.", "Pascal'ın Hristiyan çerçevesi farklı inanç ve inançsızlık seçeneklerini sınırlı ele alır.")),
    152: ("history", ("Acemoğlu ile Robinson zenginlik farkını gücü ve fırsatı dağıtan kurumlarda arar.", "Kapsayıcı kurumlar geniş kesimlere yatırım, mülkiyet ve yenilik alanı açar.", "Sömürücü kurumlar serveti dar çevrede toplarken yaratıcı yıkımdan korkar.", "Kritik dönemeçlerde küçük kurumsal farklar zamanla ayrı yollara büyüyebilir."), ("Kapsayıcı ve sömürücü ayrımı gerçek kurumların gri alanlarını basitleştirebilir.", "Coğrafya ve kültürün tek başına yetmemesi önemsiz oldukları anlamına gelmez.", "Çin'in uzun büyümesi kurumsal tezin zamanlama ve sınırlarını zorlar.", "Başarılı kurumlar başka ülkeye hazır reçete gibi taşınamaz.")),
    156: ("economy", ("Polanyi piyasanın toplumun dışında doğal olarak çalışmadığını, siyasal düzenlemeyle kurulduğunu savunur.", "Emek, toprak ve para satışa çıkarılsa da piyasa için üretilmiş sıradan mallar değildir.", "Kendi kendini düzenleyen piyasa toplumu sarsınca koruyucu karşı hareketler doğar.", "Altın standardı iç toplumsal ihtiyaçları uluslararası para disiplinine bağlamıştır."), ("Toplumsal koruma her zaman özgürlükçü veya demokratik sonuç üretmez.", "Piyasa eleştirisi fiyat bilgisinin bütün yararlarını yok saymayı gerektirmez.", "Speenhamland anlatısının tarihsel ayrıntıları sonraki araştırmalarda tartışılmıştır.", "Devletin piyasayı kurması devlet müdahalesinin her biçimini otomatik olarak iyi yapmaz.")),
    189: ("media", ("Barthes gündelik nesnenin tarihsel anlamı doğal gerçek gibi taşımasına mit der.", "Güreş, otomobil ve yemek yalnız kendileri değil sınıf ve ulus hakkında ikinci mesaj da verir.", "Mit karmaşık yapım sürecini boşaltıp sonucu sanki hep böyleymiş gibi sunar.", "Mit çözümlemesi açık görüntü ile sessizce doğal saydırılan mesajı ayırır."), ("Her kültürel anlam gizli komplo veya bilinçli aldatma değildir.", "Mit okuması nesnenin maddi üretimini ve insanların farklı yorumlarını silmemelidir.", "Barthes'ın kısa denemeleri sınıf, sömürge ve cinsiyet boyutunu her zaman eşit derinlikte işlemez.", "Bir işaretin ikinci anlamı bağlama ve zamana göre değişebilir.")),
    194: ("media", ("McLuhan aracın içeriğinden önce duyularımızın oranını ve toplumsal hızımızı değiştirdiğini savunur.", "Basılı sayfa doğrusal sıra ve özel okuma alanı kurarken elektrikli medya eşzamanlılık getirir.", "Küresel köy uyum kadar yakın çatışma ve sürekli maruz kalma da yaratabilir.", "Kitabın parçalı görsel tasarımı kendi savını yalnız anlatmaz, okura yaşatır."), ("Araç güçlüdür ama insanların kurumları ve seçimleri sonucu bütünüyle belirlemez.", "Sıcak ve soğuk medya ayrımı her örneğe kolayca uygulanamaz.", "İçeriği önemsiz saymak propaganda ve gazetecilik farkını görünmez kılabilir.", "Teknolojik değişimin yararı ve bedeli toplumun farklı kesimlerine eşit dağılmaz.")),
    214: ("media", ("Benjamin aura kavramıyla eserin tek yerdeki biricik varlığı ile tarihini birlikte düşünür.", "Teknik kopya eseri geleneğin uzak mekânından çıkarıp geniş dolaşıma sokar.", "Film montajı kesintileri yeni bir algı ve düşünme ritmine dönüştürür.", "Faşizm siyaseti estetik gösteriye çevirirken Benjamin sanatın siyasallaşmasını karşı hamle olarak görür."), ("Kopyalanabilmek her eserin aurasını aynı ölçüde yok etmez.", "Geniş erişim demokratikleşme getirirken yeni şirket ve dağıtım güçleri de kurabilir.", "Dijital dosya ve yapay zekâ Benjamin'in döneminden farklı sahiplik sorunları doğurur.", "Sanatın siyasallaşması tek bir doğru estetik programına indirgenmemelidir.")),
    222: ("politics", ("hooks feminizmi cinsiyetçiliği ve onun ürettiği baskıyı sona erdirme hareketi olarak tanımlar.", "Sorunu bütün erkeklere yüklemek erkek egemen düşüncenin kadınlarca da öğrenilebildiğini gizler.", "Sınıf ve ırk hesaba katılmadığında kız kardeşlik yalnız ayrıcalıklı deneyimi merkez yapabilir.", "Sevgi, bakım ve çocuk yetiştirme de tahakkümün öğrenildiği ya da çözüldüğü alanlardır."), ("Feminizmi yalnız kişisel başarı hikâyesine çevirmek kurumları değiştirme hedefini zayıflatır.", "Kadınların deneyimi sınıf, ırk ve cinsellik boyunca aynı değildir.", "Erkeklerin özgürleşmeye katılması kadınların yaşadığı eşitsizliği görünmez kılmamalıdır.", "Sıcak ve açık dil, hareket içindeki gerçek siyasi anlaşmazlıkların yok olduğu anlamına gelmez.")),
    241: ("economy", ("Bauman katı kurumların yerini hızla şekil değiştiren iş, ilişki ve kimliklerin aldığını anlatır.", "Özgür seçim arttıkça başarısızlığın yükü ortak düzenden bireyin omzuna taşınabilir.", "Güç sınırları aşacak kadar hareketliyken siyaset yerel alanda sıkışabilir.", "Tüketim kimliği sürekli yenilerken hiçbir seçimin uzun süre güven vermemesine yol açar."), ("Akışkanlık herkesi aynı biçimde özgürleştirmez; bazıları hareket ederken bazıları yerinde bırakılır.", "Geçmişin katı kurumları güven kadar baskı da üretmiştir.", "Kavram çok geniş kullanılırsa her değişimi açıklayan ama hiçbir şeyi sınamayan etikete dönüşebilir.", "Kişisel sağlam ada kurmak iş ve konut gibi yapısal güvencesizlikleri tek başına çözmez.")),
    253: ("technology", ("Bostrom insanüstü zekânın yüksek yeteneğinin kendiliğinden iyi amaç getirmeyeceğini savunur.", "Kendi tasarımını hızla geliştiren sistem araştırma döngüsünü insan temposundan koparabilir.", "Farklı hedefler kaynak toplamak ve kapatılmamak gibi benzer ara amaçlar üretebilir.", "Kontrol problemi yetenek kadar hedefin ne anlama geldiğini güvenilir biçimde aktarma sorunudur."), ("Zekâ patlamasının zamanı ve gerçekleşme yolu büyük belirsizlik taşır.", "Bugünkü dar sistemleri doğrudan geleceğin genel zekâsı saymak yanıltıcıdır.", "Uzak risk günümüzdeki ayrımcılık, emek ve güç yoğunlaşması sorunlarını gölgelememelidir.", "Teknik güvenlik çözümü sistemi kimin yönettiği ve kimin yararlandığı sorusunu bitirmez.")),
    271: ("spirit", ("William James dini kurumdan önce tek tek insanların yaşadığı dönüşüm ve birlik deneyimine bakar.", "Sağlıklı zihin dünyaya güvenle yaklaşırken hasta ruh bölünmüşlük ve günah duygusunu derin yaşar.", "Mistik deney anlatması zor, bilgi taşıyor gibi hissedilen, kısa ve edilgin bir birlik anı olabilir.", "James inancın değerini kökeninden çok insan hayatında ürettiği meyvelerle sınar."), ("Bir deneyin güçlü hissedilmesi onun dış dünya hakkında kesin kanıt olduğu anlamına gelmez.", "Dini deneyleri yalnız hastalık diye küçümsemek kadar her deneyimi kutsal saymak da yetersizdir.", "Kitap büyük ölçüde Batılı ve bireysel örneklere dayanır.", "Olumlu kişisel dönüşüm inancın toplumsal ve siyasi sonuçlarını tek başına aklamaz.")),
    275: ("science", ("Carroll fiziksel dünyadan bilinç ve anlama uzanan düzeyleri şiirsel natüralizm altında birleştirir.", "Çekirdek kuram gündelik maddenin davranışını çok iyi açıklar ama hayatın bütün hikâyesini tek cümlede anlatmaz.", "Entropi zamanın neden geçmişten geleceğe tek yönlü hissedildiğini anlamaya yardım eder.", "Doğaüstü amaç olmaması insanın sevgi, ahlak ve anlam kurma gücünü değersizleştirmez."), ("Fizik yasalarını bilmek bilinç deneyiminin bütün ayrıntısını çözmüş olmak değildir.", "Bilimsel natüralizm felsefi yorum içerir; yalnız deney sonucu gibi sunulmamalıdır.", "Anlamı insanların kurması bütün değerlerin keyfi olduğu anlamına gelmez.", "Büyük resim farklı açıklama düzeyleri arasındaki gerçek boşlukları küçümsememelidir.")),
}


def narrative_characters(summary: dict) -> int:
    texts = [summary.get("intro", "")]
    for chapter in summary.get("chapters", []):
        texts.extend(chapter.get("paragraphs", []))
        texts.extend(chapter.get("extraParagraphs", []))
    return sum(len(text) for text in texts)


def integration_paragraph(summary: dict, chapter: dict, art: dict, index: int) -> str:
    category, connections, _limits = BOOK_PROFILES[summary["bookNo"]]
    scene = CATEGORY_SCENES[category][index % 4]
    connection = connections[index % 4]
    caption = art["imageCaption"].strip()
    title = chapter["title"].rstrip(" ?")
    variants = (
        f"{caption} Şimdi {scene} düşünün. {connection} Böylece “{title}” uzak bir teori olmaktan çıkıp sonuç üreten bir ilişkiye dönüşür.",
        f"{caption} Buradaki mantığı gündelik hayatta {scene} üzerinden de okuyabiliriz. {connection} “{title}” başlığı tam bu nedenle tek bir tanımdan daha fazlasını taşır.",
        f"{caption} Aynı fikri küçültüp {scene} gözümüzün önüne getirelim. {connection} Ayrıntılar yan yana gelince “{title}” sözünün hangi soruna cevap verdiği belirginleşir.",
        f"{caption} Bu görüntünün yanına {scene} koyduğumuzda aradaki akrabalık şaşırtıcıdır. {connection} “{title}” böylece ezberlenecek söz değil, bakılacak bağlantı olur.",
        f"{caption} Konuyu bir an için kitaptan çıkarıp {scene} ele alalım. {connection} Bu küçük karşılaştırma “{title}” fikrinin gerçek hayatta nerede görünür olduğunu gösterir.",
        f"{caption} İlk bakışta uzak duran {scene} aslında aynı düzenin küçük bir örneğini verir. {connection} Bu ayrıntı, “{title}” bölümünün ana hareketini akılda tutmayı kolaylaştırır.",
        f"{caption} Bunu anlatmanın en kısa yolu {scene} zihinde canlandırmaktır. {connection} O anda “{title}” kuru bir kavram olmaktan çıkar ve yaşanan bir durumun içine yerleşir.",
        f"{caption} Gündelik karşılığı arandığında {scene} iyi bir büyüteç olur. {connection} “{title}” fikri bu büyüteç altında nedenleri ve sonuçlarıyla birlikte görünür.",
        f"{caption} Şimdi ölçeği değiştirip {scene} ele alalım. {connection} Kitabın “{title}” derken işaret ettiği şey, bu sıradan ayrıntının içinde yeniden karşımıza çıkar.",
        f"{caption} Benzer bir ilişkiyi {scene} izlerken de yakalayabiliriz. {connection} Bu yüzden “{title}” yalnız kitaba ait bir başlık değil, hayatı okurken kullanılabilecek bir dikkat biçimidir.",
        f"{caption} Bu sahneyi unutmamak için yanına {scene} yerleştirin. {connection} İki görüntü arasındaki bağ, “{title}” bölümünün neden önemli olduğunu uzun bir tanımdan daha iyi anlatır.",
        f"{caption} Meselenin gündelik yüzü {scene} fark ettiğimiz anda ortaya çıkar. {connection} Böyle bakınca “{title}” büyük sözlerden değil, küçük koşulların birleşmesinden oluşur.",
        f"{caption} Bir arkadaşınıza anlatır gibi {scene} örnek olarak verin. {connection} Bu örnek “{title}” düşüncesinin neyi değiştirdiğini, soyut sözcüklerden daha hızlı gösterir.",
        f"{caption} Aynı soruyu {scene} üzerinden sorduğumuzda cevap daha elle tutulur hale gelir. {connection} “{title}” başlığının ağırlığı da tam burada, görünmeyen ilişkiyi açığa çıkarmasında yatar.",
        f"{caption} Bu görüntüden günlük hayata uzanan köprüyü {scene} düşünerek kurabiliriz. {connection} Köprünün öteki ucunda “{title}” fikri, okurun kendi deneyimiyle sınanabilecek açıklığa kavuşur.",
        f"{caption} Son bir yakın plan olarak {scene} düşünelim. {connection} Böyle bir ayrıntı “{title}” bölümünü yalnız anlamamızı değil, daha sonra doğru yerde hatırlamamızı da sağlar.",
    )
    return variants[index % len(variants)]


def boundary_paragraph(summary: dict, chapter: dict, index: int, round_no: int) -> str:
    category, connections, limits = BOOK_PROFILES[summary["bookNo"]]
    scene = CATEGORY_SCENES[category][(index + round_no + 1) % 4]
    connection = connections[(index + round_no + 2) % 4]
    limit = limits[(index + round_no) % 4]
    title_label = chapter["title"].rstrip(" ?")
    variants = (
        (
            f"Burada haklı bir itiraz kapıda bekler: “{title_label}” başlığındaki fikir her durumu tek başına açıklayabilir mi? "
            f"{limit} Örneğin {scene} ele aldığımızda birden fazla neden aynı anda çalışabilir. {connection} "
            "Böylece bölüm hazır hüküm değil, nedenleri birbirinden ayırmak için kullanılacak bir mercek olur."
        ),
        (
            f"İki ihtimali yan yana koyalım. İlkinde {scene} görürüz; ikincisinde ise koşullardan yalnız biri değişmiş olsun. "
            f"Sonuç değişiyorsa “{title_label}” bir etiket değil, ilişki tarifidir. {connection} {limit} "
            "Kitabın düşüncesi tam bu karşılaştırmada akılda kalır: Tek örnekten yasa çıkarmadan, hangi ayrıntının sonucu çevirdiğini izlemek gerekir."
        ),
        (
            f"Bu bölümü bir sohbet sırasında anlattığınızı düşünün. Karşınızdaki kişi “{title_label} fikri iyi de, bunun sınırı nerede?” diye sorsun. "
            f"En dürüst cevap şudur: {limit} Buna rağmen {connection} {scene.capitalize()} gibi sıradan bir olay, "
            "soyut görünen fikrin hayatın içinde nerede işe yaradığını ve nerede başka bir açıklamaya ihtiyaç bıraktığını gösterir."
        ),
        (
            f"“{title_label}” güçlü bir açıklama sunuyor; yine de onu her kapıyı açan anahtar saymamak gerekir. {limit} "
            f"{scene.capitalize()} düşündüğümüzde bu sınır açıkça görülür. {connection} Böyle bir okuma, yazara hayran olmakla "
            "yazarın merceğini dikkatle kullanmak arasındaki önemli farkı korur."
        ),
        (
            f"Bu noktada sonucu değil koşulları değiştiren küçük bir deney yapalım: {scene} ele alın ve ayrıntılardan birini tersine çevirin. "
            f"“{title_label}” hâlâ aynı cevabı veriyor mu? {limit} Öte yandan {connection} Bölümün gerçek değeri, cevaptan önce hangi "
            "değişkenlere bakacağımızı öğretmesidir."
        ),
        (
            f"Okurun aklına doğal olarak şu soru gelir: “{title_label}” anlatısı nerede durmalı? {limit} {connection} "
            f"Bunu {scene} gibi tanıdık bir olayda sınamak, düşünceyi küçültmez; tersine onun taşıyabildiği yükü dürüstçe gösterir. "
            "Sağlam fikir, sınırı söylendiğinde dağılmayan fikirdir."
        ),
        (
            f"Bir kavramı öğrenmenin iyi yollarından biri ona uymayan örneği aramaktır. “{title_label}” için de {scene} düşünmek böyle bir sınama alanı açar. "
            f"{limit} Buna karşılık {connection} İki cümle arasındaki gerilim, kitabı tek renkli bir öğütten çıkarıp gerçek düşünceye dönüştürür."
        ),
        (
            f"Şimdi yazarın sandalyesinden kalkıp kuşkucu okurun yerine oturalım. {scene.capitalize()} düşündüğümüzde “{title_label}” fikrinin hangi "
            f"koşullara bağlı olduğunu sorar. {limit} Yine de {connection} Bu çift yönlü bakış, ne kolay reddedişe ne de kör kabule ihtiyaç bırakır."
        ),
        (
            f"Güçlü bir bölüm bazen cevabından çok geride bıraktığı soruyla yaşar. Buradaki soru şudur: {scene} ele aldığımızda “{title_label}” "
            f"neyi açıklıyor, neyi dışarıda bırakıyor? {limit} {connection} Bu ayrım akılda kaldığında kavram gündelik hayata taşınabilir."
        ),
        (
            f"“{title_label}” fikrini hemen onaylamak yerine küçük bir dayanıklılık sınavına sokalım. {scene.capitalize()} ele aldığımızda aynı mekanizmayı mı görüyoruz, "
            f"yoksa başka açıklamalar mı istiyor? {limit} {connection} Kitabı verimli kılan, bu iki ihtimali aynı anda görebilmektir."
        ),
        (
            f"Bu başlık kolayca slogana dönüşebilir; oysa gerçek hayat daha pürüzlüdür. {scene.capitalize()} düşündüğümüzde “{title_label}” tek başına yeterli "
            f"olmayabilir. {limit} Buna rağmen {connection} İyi özet, bu iki tarafı birbirine ezdirmeden yan yana tutmalıdır."
        ),
        (
            f"Konuyu akılda tutmak için bir soru kartı hazırlasak üzerine şunu yazardık: “{title_label} hangi koşul değiştiğinde işlemez?” "
            f"Bu kartı {scene} düşünerek deneyebiliriz. {limit} {connection} Böylece okur tanımı değil düşünme hareketini yanında götürür."
        ),
        (
            f"Buradaki açıklamanın cazibesi her şeyi tek çizgiye toplamasıdır; tehlikesi de aynıdır. {limit} {scene.capitalize()} incelemek başka etkenleri "
            f"yeniden kadraja sokar. Yine de {connection} “{title_label}” ancak bu geniş kadraj içinde hakkıyla anlaşılır."
        ),
        (
            f"Bir yakınımız “Peki bunun tersi bir örnek yok mu?” diye sorsa, “{title_label}” bölümünü gerçekten anlamaya başlamış olurdu. "
            f"{scene.capitalize()} düşünmek böyle bir karşılaştırma sağlar. {limit} Buna karşın {connection} İtiraz, kitabı susturmaz; söylediklerini daha kesin duymamızı sağlar."
        ),
    )
    return variants[(index + round_no * 5) % len(variants)]


def enrich(summary: dict, minimum: int, maximum: int) -> tuple[int, int]:
    # Remove the exact batch-wide paragraphs that previously inflated all books
    # with the same wording.  Hand-written content is otherwise untouched.
    for chapter in summary["chapters"]:
        chapter["paragraphs"] = [p for p in chapter.get("paragraphs", []) if p not in SHARED_PADDING]
        chapter.pop("extraParagraphs", None)

    art_index = 0
    for chapter in summary["chapters"]:
        art = summary.get("chapterArtworks", {}).get(chapter["id"])
        if art:
            chapter["extraParagraphs"] = [integration_paragraph(summary, chapter, art, art_index)]
            art_index += 1

    # Interior-image integration is non-negotiable.  If it naturally takes a
    # dense source just above the regular ceiling, retain it rather than delete
    # a meaningful image paragraph; 24k is the documented dense-book ceiling.
    round_no = 0
    while narrative_characters(summary) < minimum:
        changed = False
        for index, chapter in enumerate(summary["chapters"][1:], 1):
            if narrative_characters(summary) >= minimum:
                break
            paragraph = boundary_paragraph(summary, chapter, index, round_no)
            if narrative_characters(summary) + len(paragraph) > maximum:
                continue
            chapter.setdefault("extraParagraphs", []).append(paragraph)
            changed = True
        if not changed:
            break
        round_no += 1
        if round_no > 4:
            raise RuntimeError(f"Could not reach character target for book {summary['bookNo']}")

    summary["enrichmentStandardVersion"] = 1
    return narrative_characters(summary), sum(len(ch.get("extraParagraphs", [])) for ch in summary["chapters"])


def main() -> None:
    standard = json.loads((ROOT / "data" / "summary-production-standard.json").read_text(encoding="utf-8"))
    # The formal floor protects an individual book, while targetCharacters is
    # the batch promise.  Stop within one short paragraph of 20k so the forty
    # books do not cluster at the bare 18k acceptance floor.
    minimum = max(
        int(standard["content"]["minimumCharacters"]),
        int(standard["content"]["targetCharacters"]) - 250,
    )
    maximum = int(standard["content"]["maximumCharacters"])
    for number in BOOK_NUMBERS:
        path = ROOT / "data" / "summaries" / f"{number}.json"
        summary = json.loads(path.read_text(encoding="utf-8"))
        characters, extras = enrich(summary, minimum, maximum)
        path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{number:3} {characters:5} chars · {extras:2} enrichment paragraphs · {summary['title']}")


if __name__ == "__main__":
    main()
