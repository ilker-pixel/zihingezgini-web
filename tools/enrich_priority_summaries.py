#!/usr/bin/env python3
"""Add approved concept-specific context to guides below the depth floor.

The operation is deliberately narrow and idempotent: it can only append the
listed paragraph to the listed chapter in ``data/summaries``. Personal posts,
philosopher biographies and research-archive material are outside its scope.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY_DIR = ROOT / "data" / "summaries"

EXPANSIONS: dict[int, dict[str, str]] = {
    29: {
        "durak-03-kendini-adlandirmak": "Barth için kategori ancak toplumsal karşılaşmalarda kullanıldığında etkilidir; soy anlatısı tek başına değil, üyeliği tanıyan gündelik ilişkilerle sınır üretir.",
        "durak-04-baskalarinin-verdigi-ad": "Bu yüzden etnik sınır iki taraflıdır: grubun kendisi hakkındaki anlatısı ile çevresinin ona açtığı veya kapattığı roller birbirini sürekli biçimlendirir.",
        "durak-10-tamamlayicilik-ve-esitsizlik": "Tamamlayıcı roller sınırı kalıcılaştırabilir; taraflar birbirine muhtaçken görev, ücret ve statü farkları kuşaktan kuşağa yeniden üretilebilir.",
        "durak-13-kimligi-sahnelemek": "Öne çıkan aidiyet bağlama göre değişse de seçim sınırsız değildir; geçmiş deneyimler, çevrenin beklentisi ve olası yaptırımlar hangi kimliğin kullanılabildiğini belirler.",
        "durak-15-devletin-cizdigi-kutular": "Resmî sınıflandırma kaynak ve temsil sağlayabilirken, geçici bir ayrımı değişmez köken gibi kayda geçirip ileride siyasal rekabetin zemini de yapabilir.",
    },
    53: {
        "durak-02-bebek-bos-levha-degildir": "Gopnik'in vurgusu hazır yetişkin fikirleri değil, deneyimle hızla güncellenen güçlü öğrenme düzenekleridir; bebek hem beklenti kurar hem şaşırınca onu değiştirir.",
        "durak-03-besikteki-bilim-insani": "Benzetmenin gücü sonuçtan çok yöntemdedir: çocuk müdahale eder, beklenmedik sonucu fark eder ve hangi nedenin işe yaradığına dair tahminini yeniler.",
        "durak-05-bakistan-niyet-okumak": "Taklit böylece yalnız hareket kopyalamak değildir; çocuk görünür davranışın arkasındaki hedefi seçerek gereksiz adımları eleyebilir veya yeni bir yol deneyebilir.",
        "durak-06-yanlis-inanci-anlamak": "Bu kavrayış ortak dünyada farklı bakışların birlikte bulunabileceğini gösterir; başkasının davranışını açıklamak için onun gördüğü ve bildiği geçmişi izlemek gerekir.",
        "durak-07-karsi-olgusal-dunya": "Olmayan senaryo gerçekliği terk etmekten çok onu karşılaştırmalı anlamanın yoludur; değişen tek koşulun sonucu nasıl etkilediği böylece zihinde sınanabilir.",
        "durak-10-cocukluk-neden-uzun": "Gecikmiş uzmanlaşma çocuğa çevrenin tek çözümüne erken bağlanmadan farklı araç, ilişki ve açıklamaları deneme zamanı verir; maliyeti ise uzun bakım gereksinimidir.",
        "durak-14-yardim-etmenin-ilk-izleri": "Erken yardım, ahlaki yaşamın yalnız ödül ve ceza öğretimiyle başlamadığını düşündürür; yine de niyet, sonuç ve grup tercihi gelişim boyunca ayrışır.",
        "durak-16-ebeveynlik-marangozluk-degildir": "Gopnik buna bahçıvanlık karşılığını verir: amaç tek bir sonuç üretmek değil, çocuğun farklı yönlerde gelişebileceği güvenli ve zengin bir çevre kurmaktır.",
    },
    56: {
        "durak-13-bir-insan-bircok-bellege-aittir": "Bu çerçeveler bazen birbirini destekler, bazen aynı olaya farklı anlamlar verir; kişisel hatırlama da aralarındaki geçiş ve gerilim içinde yeniden düzenlenir ve bazen itirazla karşılaşır.",
    },
    57: {
        "durak-02-algiya-geri-donmek": "Bu dönüş, nesnel bilginin üzerine kurulduğu görünme koşullarını açığa çıkarır: ölçmeden önce yönelir, seçer ve dünyayı zaten anlamlı bir alan olarak buluruz.",
        "durak-03-duyum-atomu-yoktur": "Şekil-zemin ilişkisi bunu gösterir; aynı çizgi çevresindeki örüntü değişince başka bir nesnenin sınırı olur ve duyusal anlamı bütünle birlikte dönüşür.",
        "durak-04-onyargilarin-perdesi": "Fenomenolojik betimleme bu örtük kabulleri geçici olarak askıya alır; nesnenin hazır olduğu fikrinden önce, görünürlük ve kesinlik deneyiminin nasıl oluştuğuna bakar.",
        "durak-05-beden-nesne-degildir": "Yaşanan beden ile ölçülen beden aynı varlığın iki görünümüdür; ilki hareketin 'yapabilirim' ufkunu, ikincisi dışarıdan belirlenebilen yapıyı anlatır.",
        "durak-06-beden-semasi": "Bu harita tek tek uzuvların zihinsel resmi değildir; bakış, duruş ve hedefi tek bir eylem alanında eşzamanlı düzenleyen pratik bütünlüktür.",
        "durak-07-fantom-uzuv": "Bedenin eski alışkanlık ufku fiziksel değişimden sonra da sürebilir; dünya hâlâ uzanılabilecek şeyler sunarken güncel beden artık o yanıtı veremez.",
        "durak-08-aliskanlik-bilgi-tasir": "Öğrenilen hareket bedene yeni bir çevre açar; nota okuyan müzisyen işaretleri tek tek çevirmek yerine onları doğrudan çalınabilir yönelimler olarak görür.",
        "durak-09-baston-beden-olur": "Ustalık sırasında dikkat sapın temasından çevredeki engele kayar; aracın sınırı beden şemasına katıldığı için algılanan alan fiilen genişler.",
        "durak-10-mekan-yasanir": "Yakınlık yalnız metreyle belirlenmez; kolayca ulaşılabilen yer bedensel olarak yakın, önünde korku veya engel bulunan yer geometrik olarak yakınken yaşantıda uzak olabilir.",
        "durak-11-nesne-perspektifler-ufkudur": "Görmediğimiz yüzler boşluk değildir; hareket ettiğimizde doğrulanabilecek beklentiler olarak mevcut görünüşe eşlik eder ve nesnenin sürekliliğini kurar.",
        "durak-12-cinsellik-varolusun-tonu": "Burada söz konusu olan yalıtılmış bir işlev değil, kişinin yakınlık, utanç, çekim ve gelecek imkânlarını kavrayışına yayılan bedensel anlam örgüsüdür.",
        "durak-13-soz-dusuncenin-bedenidir": "İfade, belirsiz yönelimi paylaşılabilir bir anlama dönüştürür; konuşan da dinleyen de tamamlanmış bir içeriği taşımak yerine söz içinde yeni bir kavrayış kurabilir.",
        "durak-14-baskasi-nasil-gorunur": "Canlı hareket daha baştan bir dünyaya yöneliş taşır; başkasının jesti bu nedenle önce nötr veri, sonra eklenen zihinsel tahmin olarak deneyimlenmez.",
        "durak-15-zaman-disaridan-akmaz": "Şimdiki an noktasal değildir: biraz önceyi tutan iz ile biraz sonrasına yönelen beklenti olmadan ne hareketi ne de bir cümleyi bütün olarak algılarız.",
    },
    114: {
        "durak-04-hukuk-yoneticiden-once-mi": "Kuralların öngörülebilirliği yurttaşa devlet karşısında güvenli bir alan açar; asıl sınav, güçlü aktörlerin kendi çıkarlarına aykırı karara da uymasıdır.",
        "durak-05-hesap-verebilirlik": "Hesap verme yalnız cezalandırılma ihtimali değildir; yönetenin kararını açıklaması, bilginin denetlenebilmesi ve yurttaş talebinin sonraki kararı etkileyebilmesidir.",
        "durak-08-burokrasinin-dogusu": "Liyakat düzeni makamı kişisel mülk olmaktan çıkarır; görevlinin belirli usule göre seçilmesi ve yükselmesi, devlet bilgisinin yönetim değişiklikleri boyunca korunmasını sağlar.",
        "durak-09-prusya-nin-guclu-devleti": "Bu sıra modernleşmenin tek yolunun önce demokrasi olmadığını gösterir; fakat erken kurulan özerk devlet aygıtı sonradan toplumsal denetime direnebilecek kendi çıkarlarını da geliştirir.",
        "durak-15-siyasi-gerileme": "Gerileme ani çöküşten çok kurumsal katılaşmadır; geçmişte işe yarayan düzen, yeni toplumsal güçleri temsil edemediğinde biçimsel olarak sürerken işlevini yitirebilir.",
    },
    116: {
        "durak-14-ordu-vatandasi-degistirir": "Devlet geniş kitlelerden can ve kaynak istediğinde karşılığında aidiyet, koruma ve temsil talepleriyle yüzleşir; savaş kapasitesi böylece yurttaşlık pazarlığını dönüştürebilir.",
    },
    123: {
        "durak-03-monadin-penceresi-yoktur": "Leibniz böylece gerçek birliği dış etkilere bölünmeyen basit tözde arar; gördüğümüz etkileşim ise monadların karşılıklı uyumlu iç değişimleri olarak yorumlanır.",
        "durak-05-algi-monadin-ic-durumudur": "Algı monadın evreni kendi bakış noktasından ifade etmesidir; monadlar aynı bütünü temsil ederken açıklık ve seçiklik dereceleri bakımından ayrılır.",
        "durak-06-istah-degisimi-tasir": "İştah her zaman hedefe tam ulaşmaz; bir sonraki algıya doğru yönelim sağlarken ardışık durumların kesintisizliğini ve monadın iç etkinliğini açıklar.",
        "durak-07-kucuk-algilar": "Bilinçli deneyimin sürekliliği bu fark edilmeyen geçişlere dayanır; eşik altındaki değişimler biriktiğinde dikkatimizde nitel bir fark olarak belirir.",
        "durak-09-celismezlik-ilkesi": "Bu ilke akıl yürütmenin eleme ölçüsüdür: bir iddia kendi kavramıyla çelişiyorsa gerçekleşip gerçekleşmediğine bakmadan reddedilir.",
        "durak-11-akil-dogrulari-ve-olgu-dogrulari": "İlk türün gerekçesi sonlu çözümlemeyle gösterilebilir; ikinci türde ise nedenler zinciri dünyanın tüm düzenine uzandığı için tam açıklama yalnız Tanrı'ya açıktır.",
        "durak-13-mumkun-dunyalar": "Dünya tek tek olayların rastgele toplamı değil, birlikte gerçekleşebilir durumların bütünüdür; bir seçeneğin değişmesi başka olayların bağdaşma düzenini de etkiler.",
        "durak-15-onceden-kurulmus-uyum": "Beden ile ruh arasındaki uygunluk da bu modelle açıklanır: biri diğerine komut vermez, fakat iki ayrı gelişim dizisi karşılık gelecek biçimde ilerler.",
    },
    125: {
        "durak-02-anligin-sinirini-olcmek": "Bu soruşturma, insanın hangi konularda kesinlik bekleyebileceğini ve gündelik yaşamda hangi konularda iyi temellendirilmiş olasılıkla yetinmesi gerektiğini belirlemeyi amaçlar.",
        "durak-04-bos-levha-ne-demektir": "Basit fikirleri duyum ve iç gözlem sağlar; zihin bu malzemeyi edilgin biçimde depolamaz, birleştirme, karşılaştırma ve soyutlama işlemleriyle karmaşık düşünceler kurar.",
    },
    129: {
        "durak-03-maksim-kendime-koydugum-kural": "Ahlaki değerlendirme görünen davranıştan önce bu ilkeye yönelir; aynı yardım eylemi görev duygusu, çıkar veya beğenilme isteği gibi farklı maksimlerden doğabilir.",
        "durak-04-kosullu-buyruk": "Koşullu buyruk beceri ve ihtiyat alanında etkilidir; istenen sonuca götüren yolu gösterir, fakat herkes için bağlayıcı bir ahlaki gerekçe üretmez.",
        "durak-06-yalniz-evrensel-yasa-olabilecek-bicimde-davran": "Test, kendimize tanıdığımız istisnanın ortak kuralı imkânsızlaştırıp imkânsızlaştırmadığını açığa çıkarır; kişi kendi çıkarını herkesin kullanamayacağı ayrıcalıkla koruyamaz.",
        "durak-08-yaderklik": "Kant'ın itirazı duygunun varlığına değil, iradenin yasasını dış ödül veya eğilimden almasına yönelir; bu durumda davranış koşul değişince bağlayıcılığını kaybeder.",
        "durak-17-yildizli-gok-ve-ahlak-yasasi": "İki deneyim insanı farklı yönde yerinden eder: doğa fiziksel önemsizliğimizi, ahlak yasası ise özgür ve sorumlu bir özne olarak değerimizi gösterir.",
    },
    150: {
        "durak-03-akilsal-gercek": "Bu doğrular siyasal ikna ve çoğunluk kararından bağımsız geçerlilik ister; iktidar onları yasaklayabilir, fakat oyla yanlış veya doğru hâle getiremez.",
        "durak-05-kanaat-ne-zaman-mesrudur": "Çoğulluk, aynı dünyayı farklı konumlardan gören yurttaşların yargılarıyla oluşur; tartışmanın anlamlı kalması için bu konumların dayandığı ortak olgu zemini korunmalıdır.",
        "durak-11-yalanci-kendi-yalanina-inanirsa": "İmaj gerçekliğin yerine geçtiğinde propaganda yalnız halkı aldatmaz; yönetim de kendi ürettiği kurguya göre hareket ederek olgulara uyum sağlama yeteneğini kaybeder.",
        "durak-13-tanigin-kirilganligi": "Olay başka türlü gerçekleşebilirdi ve geride zorunlu bir kanıt bırakmayabilir; bu nedenle tanıklık, belge ve arşiv olgusal dünyanın sürekliliği için kurucu önem taşır.",
        "durak-14-tarihci-ve-gazeteci": "Bu mesleklerin siyasal değeri tarafsızlık iddiasından çok olguyu kanaatten ayıran usullerdedir; kaynak karşılaştırma ve düzeltme imkânı kamusal dünyayı onarır.",
    },
    167: {
        "durak-03-mesafe-arzuyu-kurar": "Değer nesnenin içinde hazır bulunmaz; ona ulaşmak için aşılması gereken uzaklık ile öznenin bu uzaklığı aşabileceğine dair beklentisi arasındaki ilişkide doğar.",
        "durak-04-degisim-karsilikli-fedakarliktir": "Değişim, öznel değerleri karşılaşmaya zorlar: her taraf verdiğini alacağından daha az önemli saydığı anda işlem mümkün olur.",
        "durak-05-para-ortak-olcu-olur": "Bu soyutlama dolaşımı büyük ölçüde kolaylaştırır; aynı anda şeylerin özgül hikâyesini, üretim koşulunu ve kişi için taşıdığı eşsiz anlamı geri plana iter.",
        "durak-07-para-neden-tarafsiz-gorunur": "Kişiden bağımsız ölçü, modern ilişkileri genişletir; buna karşılık işlemin görünür eşitliği servet, ihtiyaç ve pazarlık gücündeki farkları kendiliğinden düzeltmez.",
        "durak-09-arac-amaca-donusur": "Para belirli bir ihtiyaca bağlı olmadığı için her gelecek amacın olasılığı gibi görünür; tam da bu sınırsız potansiyel, biriktirmeyi kendi başına hedefe çevirebilir.",
        "durak-10-para-ozgurlestirir": "Bağın kişisizleşmesi bireye eski topluluk denetiminden hareket alanı açar; fakat ilişkiler daha değiştirilebilir oldukça süreklilik ve karşılıklı sorumluluk da zayıflayabilir.",
        "durak-13-kesinlik-ve-dakiklik": "Metropolün çok sayıda yabancı arasındaki işlemleri ancak ortak saat, hesap ve karşılaştırma düzeniyle yürür; bu düzen kişisel ritimleri kurumsal takvime uyarlar.",
        "durak-15-kulturun-nesnel-buyumesi": "Simmel'in kültür trajedisi bu açıklıkta belirir: insanların yarattığı nesnel dünya bağımsızca genişlerken tek kişinin onu öznel gelişimine katma olanağı daralır.",
        "durak-16-isbolumu-ve-parca-insan": "Birey daha büyük ve karmaşık üretime katılır, fakat katkısının anlamını bütünde göremeyebilir; nesnel başarının artışı öznel kültürün artışını garanti etmez.",
    },
    187: {
        "durak-02-dil-dusunceyi-hapseder-mi": "Dil aşılmaz duvar değil, dikkati belirli ayrımlara tekrar tekrar yönelten alışkanlıktır; konuşur bazı özellikleri hızla fark ederken başkalarını ifade etmek için ek çaba harcayabilir ve yeni anlatım yolları arar.",
        "durak-07-kultur-dogaya-cizgi-cizer": "Kategoriler süreklilik içindeki bazı farkları iletişim için belirginleştirir; adlandırma fiziksel dünyayı yaratmaz, fakat benzerlikleri hatırlama ve ayırt etme hızımızı etkileyebilir.",
    },
    188: {
        "durak-09-gayrimesrulastirma": "Bu strateji tartışmanın eşiğini değiştirir: rakip meşru konuşmacı sayılmadığında onun kanıtına cevap vermek yerine söz hakkını baştan reddetmek mümkün olur.",
        "durak-12-siyasi-roportajin-oyunu": "Her hamle sonraki konuşma alanını daraltır veya genişletir; sorunun biçimi kabul edilebilir yanıtı, yanıtın kaçışı da muhabirin takip seçeneğini belirler.",
    },
    209: {
        "durak-03-yuksek-ile-alcak-ayrimi": "Lefebvre için gündelik, büyük yapıların dışında kalan tortu değil onların gerçekleştiği zemindir; ekonomi ve ideoloji evde, sokakta ve çalışma ritminde somutlaşır.",
        "durak-08-reklamin-cift-dili": "Mesaj bir yandan gündelik eksikliği kabul eder, öte yandan çözümü satın alınabilir bir işarete bağlar; böylece eleştiri tüketim çağrısına dönüştürülür.",
        "durak-09-bos-zaman-gercekten-bos-mu": "Boş zaman işin karşıtı görünürken aynı üretim düzeninin hız, bütçe ve hazır eğlence seçenekleriyle biçimlenebilir; özgürlük derecesi bu bağlarda aranır.",
        "durak-10-tekrarin-iki-yuzu": "Eleştiri tekrarın kendisini yok etmeyi değil, hangi tekrarın yaşamı yeniden ürettiğini ve hangisinin seçenekleri kapattığını ayırt etmeyi gerektirir.",
        "durak-11-kadinlarin-gorunmez-gundeligi": "Ücret hesabına girmeyen bu emek, çalışanların ve kuşakların her gün yeniden üretimini sağlar; görünmezliği ekonomik değersizliğinden değil ölçüm düzeninden kaynaklanır.",
        "durak-12-teror-gundelikte-nasil-isler": "Baskı tek merkezden verilen emir gibi değil, normal sayılan küçük ölçütlerin içselleştirilmesiyle yayılır; kişi dış denetimi kendi kendini yargılamaya çevirebilir.",
        "durak-15-programlanmis-gundelik": "Programlama seçimleri kaldırmak zorunda değildir; seçeneklerin sırasını, görünürlüğünü ve zahmetini ayarlayarak hangi davranışın doğal veya kaçınılmaz hissedileceğini belirler.",
        "durak-17-sasirtici-olan-siradanin-icindedir": "Dönüşüm de burada başlar; insanlar dayatılmış kullanım biçimlerini değiştirip mekânı, zamanı ve nesneleri ortak ihtiyaçlara göre yeniden sahiplenebilir.",
    },
    210: {
        "durak-08-kipling-ve-hizmet-gorevi": "Bu anlatı egemenliği ahlaki fedakârlık gibi sunar; yönetilenlerin kendi ihtiyaçlarını tanımlama yetkisi yerine imparatorluk merkezinin uygarlık ölçüsünü doğal kabul eder.",
        "durak-13-ulusal-kurtulusun-gucu": "Said direnişin zorunlu enerjisini kabul ederken kültürü kapalı ve saf bir öz hâline getirmeye karşı çıkar; sömürge geçmişi iç içe geçmiş tarihleri bütünüyle ayıramaz ve yeni dışlamalar üretebilir.",
    },
    245: {
        "durak-02-soz-neden-tehlikelidir": "Foucault'nun sorusu yalnız söylenen içeriğe değil, sözün ortaya çıkmasını yöneten düzene gider; dolaşım hakkı bazı ifadeleri olay ve otorite hâline getirir.",
        "durak-06-yorum-tukenmez-donus": "Yorum hem metnin henüz söylenmemiş anlamını açma vaadi taşır hem de yeni sözün değerini ilk metne bağlı tutarak söylem alanını düzenler.",
        "durak-07-yazar-islevi": "Bu işlev her söylemde aynı çalışmaz; bilimsel önermede doğrulanabilirlik öne çıkarken edebiyatta ad, metinleri bir bütün ve mülkiyet alanı olarak kurabilir.",
        "durak-08-disiplin": "Bir önerme doğru olmadan önce disiplinin tanıdığı kavram, nesne ve tekniklerle kurulmuş olmalıdır; aksi hâlde değerlendirme alanına bile kabul edilmeyebilir.",
        "durak-10-konusan-oznenin-seyreltilmesi": "Böylece söylem sınırsız bireysel ifade olarak değil, belirli konumların doldurulmasıyla işler; kişi konuşur ama sözün yetkisi kurumsal rolle birlikte oluşur.",
        "durak-11-rituel": "Ritüel kimin konuşacağını, hangi söz dizisini kullanacağını ve dinleyenin nasıl karşılık vereceğini önceden düzenleyerek söylemin etkisini tekrarlanabilir kılar.",
        "durak-12-soylem-cemaatleri": "Bilginin içeride dolaşımı aidiyeti güçlendirirken dışarı aktarımı sınırlar; üyelik yalnız bilgiye sahip olmak değil, onu uygun biçimde kullanmayı öğrenmektir.",
        "durak-13-doktrin": "Doktrin iki yönlü denetim kurar: cümleleri ortak ölçüte bağlarken konuşanları da kabul ettikleri cümleler üzerinden birbirine tanıtır ve sınırlar.",
        "durak-14-egitimin-dagitim-gucu": "Okul yalnız bilgiyi aktaran nötr kanal değildir; söylemle birlikte onu kullanma hakkını, yeterlilik belgesini ve toplumsal konumu da paylaştırır.",
        "durak-15-tersine-cevirme": "Bu ilke görünürde üretken olan yazar, disiplin ve yorumun aynı zamanda eleme yaptığını gösterir; bolluğun arkasındaki sınırlama işlemleri araştırmanın nesnesi olur.",
    },
    258: {
        "durak-03-dinamik-sistem": "Analizin odağı tek bir denge noktası değil, durumların izlediği yörüngedir; küçük geri bildirimler zaman içinde durağanlık, salınım veya büyüme üretebilir.",
        "durak-04-kaos-ve-kelebek-etkisi": "Sistem kurallı olsa bile başlangıç koşulunu sonsuz kesinlikle ölçemeyiz; hata büyüdüğünde tek sonuç tahmini yerine olası davranış aralıkları önem kazanır.",
        "durak-05-bilgi-nedir": "Shannon ölçüsü, nadir mesajın daha çok şaşırtması fikrine dayanır; olası seçeneklerin dağılımı bilinmeden bir işaretin taşıdığı bilgi miktarı hesaplanamaz.",
        "durak-07-evrim-kor-tasarimci": "Karmaşık yapı tek adımda hedeflenmez; işe yarayan küçük değişimler korunur, mevcut yapı yeni işlevlere uyarlanır ve tasarım tarihsel kısıtlarla ilerler.",
        "durak-08-genler-tek-basina-program-degildir": "Genler sabit bir çıktı listesi yerine başka süreçlerle birlikte çalışan kaynaklar sunar; gelişim, aynı talimatın bağlama göre farklı sonuçlar vermesidir.",
        "durak-09-kendini-kopyalayan-program": "Kurucu mekanizma hem betimi taşımalı hem bu betimi okuyacak düzeni üretmelidir; kopyalama sorunu talimat ile uygulayıcı arasındaki döngüyü görünür kılar.",
        "durak-10-genetik-algoritma": "Yöntem her olasılığı taramak yerine başarılı adayların parçalarını yeni birleşimlerde dener; çeşitlilik erken tek çözüme sıkışmayı önleyen temel kaynaktır.",
        "durak-11-hucresel-otomatlar": "Ortaya çıkan düzen herhangi bir hücrenin planında bulunmaz; zaman boyunca yinelenen yerel etkileşim, üst ölçekte kalıcı ve hareketli yapılar oluşturur.",
        "durak-13-parcaciklarla-hesaplamak": "Hesap burada simgeleri sırayla işleyen merkez değil, etkileşen öğelerin ortak sonucu olarak düşünülür; bilgi sistem boyunca taşınır ve dönüştürülür.",
        "durak-14-canli-sistem-bilgi-isler": "Dağıtık işlem tek bir öğenin bütünü bilmesini gerektirmez; yerel tepkiler birbirini etkileyerek çevreye uyarlanmış ortak bir davranış oluşturabilir.",
        "durak-15-benzetme-yapmak": "İyi benzetme nesneleri değil ilişkiler sistemini eşler; bir alandaki neden-sonuç yapısı diğer alana taşındığında hem keşif hem yanlış genelleme ihtimali doğar.",
        "durak-16-ag-bilimi": "Aynı düğüm sayısı farklı bağlantı düzenlerinde bambaşka davranır; bu yüzden karmaşıklık öğelerin özellikleri kadar aralarındaki yol ve kümelenmelerde aranır.",
    },
    259: {
        "durak-14-askeri-laboratuvardan-gundelik-urune": "Askerî öncelikler hangi problemin araştırmaya değer, hangi hata türünün kabul edilebilir ve hangi öznenin izlenebilir sayıldığını belirleyerek sivil ürüne gömülü varsayımlar bırakabilir.",
    },
}


def main() -> int:
    changed_files = 0
    added_paragraphs = 0
    for book_no, chapter_expansions in EXPANSIONS.items():
        path = SUMMARY_DIR / f"{book_no}.json"
        summary = json.loads(path.read_text(encoding="utf-8"))
        chapters = {chapter["id"]: chapter for chapter in summary.get("chapters", [])}
        missing = sorted(set(chapter_expansions) - set(chapters))
        if missing:
            raise SystemExit(f"{path.name}: missing chapter ids: {', '.join(missing)}")

        changed = False
        for chapter_id, paragraph in chapter_expansions.items():
            paragraphs = chapters[chapter_id].setdefault("paragraphs", [])
            if paragraph not in paragraphs:
                paragraphs.insert(2, paragraph)
                added_paragraphs += 1
                changed = True
        if changed:
            path.write_text(
                json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            changed_files += 1

    print(f"Added {added_paragraphs} concept paragraphs across {changed_files} summaries.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
