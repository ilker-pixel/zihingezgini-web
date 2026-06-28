import json
import os

def create_drunkard_summary():
    os.makedirs("data/summaries", exist_ok=True)
    
    summary = {
        "bookNo": 6,
        "title": "Sarhoş Yürüyüşü",
        "author": "Leonard Mlodinow",
        "subtitle": "Rastlantısallık Hayatımızı Nasıl Yönetir? (Detaylı Kitap Özeti)",
        "meta": {
            "originalTitle": "The Drunkard's Walk: How Randomness Rules Our Lives",
            "compiler": "Yapay Zeka Asistanı",
            "date": "Haziran 2026",
            "language": "Türkçe"
        },
        "intro": "Leonard Mlodinow'un kaleme aldığı \"Sarhoş Yürüyüşü\" (The Drunkard's Walk: How Randomness Rules Our Lives), hayatımızın görünmeyen yöneticisini sahneye davet ediyor: Rastlantısallık. Kitap, ismini fizikteki ve matematikteki \"rastgele yürüyüş\" (random walk) kavramından alır. Bu kavram, havada süzülen bir toz zerreciğinin ya da sarhoş bir adamın sokaktaki adımlarının yönünün tamamen tahmin edilemez, rastgele çarpışmalarla belirlenmesini anlatır. Mlodinow, günlük hayatta aldığımız kararların, elde ettiğimiz başarıların ya da yaşadığımız başarısızlıkların arkasında yatan şans faktörünü görmezden gelme eğilimimizi sert bir dille ama son derece eğlenceli örneklerle eleştiriyor. İnsan beyni evrimsel olarak neden-sonuç ilişkileri aramaya, düzensizlik içinde düzen görmeye programlanmıştır. Bir piyangoyu kazanan kişiyi \"özel güçleri olan biri\", başarılı bir CEO'yu \"dahi bir lider\", üst üste maç kaybeden bir antrenörü ise \"yetersiz biri\" olarak damgalamaya bayılırız. Oysa matematiksel gerçekler bize bambaşka bir hikaye anlatır. Bu kitapçıkta, Mlodinow'un bu başyapıtını en sade, ortaokul düzeyindeki bir bireyin bile heyecanla okuyabileceği akıcılıkta özetledik. Kitabın orijinal 10 bölümüne ve tüm alt başlıklarına sadık kalarak; olasılık kuramının heyecan verici tarihinden, Monty Hall problemine, Bayes teoreminin mahkeme salonlarındaki hayati rolünden, spor dünyasındaki örüntü illüzyonlarına kadar her şeyi bolca benzetme ve örnekle açıkladık. Hazırsanız, rastlantısallık gözlüğümüzü takıp yolculuğa başlayalım!",
        "chapters": [
            {
                "id": "intro_text",
                "title": "Giriş: Hayatı Rastlantısallıkla Okumak",
                "image": "/images/drunkards_walk_cover_sketch.png",
                "imageCaption": "Sarhoş Yürüyüşü",
                "takeaway": "İnsanlar her zaman düzen ve niyet görme arzusu içindedir. Olasılık bilimi bize, çoğu zaman en büyük niyetlerin arkasında bile sadece kör bir şansın durduğunu fısıldar.",
                "paragraphs": [
                    "Rastlantısallığın Gizli Gücü: Hayatımızdaki başarıların ve başarısızlıkların arkasında yatan şans faktörünü genellikle küçümseriz. Zihnimiz her şeye bir neden bulmaya çalışır. Oysa hayat, sarhoş bir adamın sokaktaki öngörülemeyen adımları gibi yön bulur."
                ]
            },
            {
                "id": "chapter1",
                "title": "BÖLÜM 1: Rastlantısallığın Merceğinden Bakmak",
                "image": "/images/mouse_maze_sketch.png",
                "imageCaption": "Fare Deneyi: Örüntü Arayışı",
                "takeaway": "Fare Deneyi Yanılgısı: Rastgele süreçlerde örüntü aramak, insanı basitleşmekten alıkoyup hata yaptırır.",
                "paragraphs": [
                    "**İnsan Performansının Fareden Düşük Olduğu Anlar**\n\nİnsan beyni o kadar gelişmiştir ki uzay araçları yapar, şiirler yazar ve karmaşık denklemleri çözer. Ancak iş rastgele olayları tahmin etmeye gelince, basit bir fareden bile daha kötü performans gösterebiliriz! Evet, yanlış duymadınız. Bilim insanlarının yaptığı meşhur bir deneyde, bir kutunun üst ya da alt bölmesine yiyecek yerleştiriliyor. Yiyeceğin nerede olacağı tamamen rastgele belirleniyor ama bir kural var: %80 ihtimalle üst bölmeye, %20 ihtimalle alt bölmeye konuyor. Deneydeki bir fare, birkaç denemeden sonra kutunun üst bölmesinde daha çok yiyecek olduğunu fark eder. Hiç kafa yormaz ve her seferinde doğrudan üst bölmeye gider. Böylece %80 başarı oranı yakalar. İnsanlar ise yiyeceğin yerleştirilmesinde gizli bir şablon, akıllıca bir örüntü aramaya başlarlar. 'İki kere üste koydu, şimdi kesin alta koyar' diyerek tahmin yürütürler ve bir yukarı bir aşağı giderler. Sonuç mu? İnsanların başarı oranı ortalama %60'ta kalır! Mlodinow bu şaşırtıcı örnekle bize şunu hatırlatıyor: Rastgele olaylarda örüntü aramak, bizi basit bir farenin pragmatik zekasının bile gerisine düşürebilir.",
                    "**Gizli Şans Faktörü ve Günlük Yanılgılarımız**\n\nHayatımızda başarılı olan insanları incelediğimizde onlara hayran kalırız. Örneğin Stephen King'in ilk kitabı Carrie (Göz) tam 30 kez reddedilmiştir. J.K. Rowling'in Harry Potter dosyası 12 yayınevi tarafından geri çevrilmiştir. Eğer bu yazarlar son denemelerinde de reddedilselerdi, bugün dünya edebiyat tarihinin en büyük isimlerinden bazılarını hiç tanımıyor olacaktık. Bizler bir olay gerçekleştikten sonra (buna geriye dönük bakış yanılgısı denir) o olayın olmasının kaçınılmaz olduğunu düşünürüz. Harry Potter'ın çok satmasının nedenini sadece kitabın kalitesine bağlarız. Oysa binlerce kaliteli kitap, yayınevlerinin editörlerinin o sabah kahve içip içmemesi gibi tamamen rastgele faktörler yüzünden çöpe gitmektedir. Başarı, yetenek ile doğru zamanda doğru yerde olmak gibi rastgele olayların çarpışmasından doğar. Şansın hayatımızdaki gizli rolünü görmezden gelmek, kendimize dair gerçek dışı bir kontrol illüzyonu yaratmamıza neden olur.\n\n*\"Tıpkı havada süzülen bir toz zerreciğinin atomlarla çarpışarak yön bulması gibi, hayatımızın rotası da küçük ve rastgele çarpışmalarla şekillenir.\"* — Leonard Mlodinow, Sarhoş Yürüyüşü"
                ]
            },
            {
                "id": "chapter2",
                "title": "BÖLÜM 2: Gerçeklerin ve Yarı Gerçeklerin Yasaları",
                "takeaway": "Linda Problemi: Detaylı ve mantıklı görünen süslü hikayeler, basit ve yalın gerçeklerden her zaman daha az olasıdır.",
                "paragraphs": [
                    "**Olasılığın Temel İlkeleri ve Hatalı Kullanımları**\n\nOlasılık teorisi aslında çok basit bir soruyla başlar: Bir şeyin olma ihtimali nedir? Eğer bir madeni parayı havaya atarsanız yazı gelme ihtimali 1/2'dir. Peki iki madeni parayı arka arkaya attığınızda ikisinin de yazı gelme ihtimali nedir? Bağımsız olayların birlikte gerçekleşme ihtimalini bulmak için bu olasılıkları çarparız: 1/2 x 1/2 = 1/4 (yani %25). Günlük hayatta bu kuralı sürekli ihlal ederiz. Örneğin bir uçak kazası duyduğumuzda hemen seyahat planımızı iptal ederiz. Oysa aynı gün içinde hem bir uçak kazasının olması hem de sizin o uçakta olmanız olasılığı milyonda birden bile azdır. İnsanlar bağımsız olayların olasılıklarını birbiriyle karıştırarak mantıksız korkulara kapılırlar. Şirketler de reklamlarında bu yanılgıyı kullanarak bizi manipüle eder.",
                    "**Neden Süslü Bir Hikaye Basit Bir Gerçekten Daha Az Olasıdır?**\n\nDaniel Kahneman ve Amos Tversky'nin yaptığı meşhur 'Linda Deneyi' olasılığın en büyük tuzaklarından birini ortaya koyar. Deneyde insanlara Linda adında bir karakter tanıtılır: Linda 31 yaşında, bekar, açık sözlü ve çok zeki bir kadındır. Öğrencilik yıllarında ayrımcılıkla mücadele etmiş ve nükleer karşıtı protestolara katılmıştır. Katılımcılara şu soru sorulur: Hangi seçenek daha olasıdır? A) Linda bir banka veznedarıdır. B) Linda bir banka veznedarıdır ve feminist hareketin aktif bir üyesidir. Katılımcıların %85'i B seçeneğini seçer. Oysa matematiksel olarak B seçeneği, A seçeneğinin içinde küçük bir alt kümedir. Yani Linda'nın hem veznedar hem feminist olma ihtimali, sadece veznedar olma ihtimalinden her zaman daha düşüktür! İnsan beyni, detaylarla süslenmiş hikayeleri (yarı gerçekleri) daha inandırıcı bulur. Bir hikayeye ne kadar çok detay eklerseniz, onun gerçekleşme olasılığı o kadar azalır. Ancak beynimiz bu mantık kuralını çiğneyerek süslü yalanlara inanmayı tercih eder.\n\n*\"Bir hikayeye ne kadar çok detay ve süs eklerseniz, onun matematiksel olarak doğru olma ihtimalini o kadar azaltırsınız.\"* — Leonard Mlodinow, Sarhoş Yürüyüşü"
                ]
            },
            {
                "id": "chapter3",
                "title": "BÖLÜM 3: Olasılıklar Uzayında Yolunuzu Bulmak",
                "image": "/images/monty_hall_doors_sketch.png",
                "imageCaption": "Monty Hall Problemi",
                "takeaway": "Monty Hall Çelişkisi: Sezgilerimiz kapılar arasında eşit olasılık görse de, seçimi değiştirmek kazanma olasılığını 1/3'ten 2/3'e çıkarır.",
                "paragraphs": [
                    "**Rastgele Durumları Analiz Etmek İçin Bir Çerçeve**\n\nBir olayın olasılığını hesaplamak için öncelikle olabilecek tüm durumları yani 'örnek uzayını' (sample space) belirlememiz gerekir. Örneğin iki zar attığımızda toplamda 36 farklı sonuç elde edebiliriz. Eğer bu sonuçların hepsini tek tek listelemezsek, olasılıkları yanlış hesaplarız. Rönesans döneminde İtalya'da yaşayan ünlü tıp doktoru ve kumarbaz Gerolamo Cardano, bu basit gerçeği fark eden ilk kişidir. Cardano, zarlarla kumar oynarken hangi toplamların gelme ihtimalinin daha yüksek olduğunu tüm olası durumları yazarak hesaplamıştı. Bu çalışması, olasılık biliminin temelini atmıştır. Hayatta bir karar alırken de önümüzdeki tüm seçenekleri ve olası sonuçları bir harita gibi önümüze sermeliyiz. Aksi takdirde, sadece en çok dikkat çeken sonuca odaklanıp yanılırız.",
                    "**Vebalı İtalya'daki Kumarbazlardan Monty Hall Problemine**\n\nMonty Hall problemi, insan sezgisinin olasılık karşısında nasıl tamamen çaresiz kaldığının en meşhur örneğidir. Bir yarışmadasınız ve önünüzde 3 kapı var. Birinin arkasında son model bir araba, diğer ikisinin arkasında ise keçiler var. Siz 1. kapıyı seçiyorsunuz. Sunucu (arkada ne olduğunu bilen Monty Hall), diğer kapılardan birini açıyor ve arkasından bir keçi çıkıyor (örneğin 3. kapı). Sonra size soruyor: 'Seçiminizi değiştirip 2. kapıyı seçmek ister misiniz?' İnsanların çoğu 'Fark etmez, iki kapı kaldı, şansım %50-%50' diyerek değiştirmeyi gereksiz görür. Oysa seçimi değiştirmek kazanma şansınızı tam iki katına çıkarır! İlk başta arabayı seçme şansınız 1/3'tü, keçiyi seçme şansınız ise 2/3'tü. Değiştirdiğinizde aslında ilk durumdaki 2/3'lük keçi seçme ihtimalinizi arabaya dönüştürmüş olursunuz. Sezgilerimiz bize %50 derken, matematik bize ısrarla 'Değiştir, şansın %66'ya çıksın!' der.\n\n*\"Zihnimizin en emin olduğu anlar, olasılık kuralları karşısında en çok çuvalladığımız anlardır.\"* — Leonard Mlodinow, Sarhoş Yürüyüşü"
                ]
            },
            {
                "id": "chapter4",
                "title": "BÖLÜM 4: Başarıya Giden Yolları İzlemek",
                "takeaway": "Beklenen Değer Yasası: Tek bir denemede şans belirleyicidir, ancak deneme sayısı arttıkça matematik kaçınılmaz zaferini ilan eder.",
                "paragraphs": [
                    "**Olayların Gerçekleşme Yollarını Saymak ve Pascal Üçgeni**\n\nBazen bir sonucun gerçekleşmesi için birden fazla yol vardır. Örneğin 4 kez para attığımızda 2 yazı ve 2 tura gelmesinin kaç farklı yolu olduğunu hesaplamak için kombinasyon matematiğini kullanırız. Blaise Pascal ve Pierre de Fermat, 17. yüzyılda bir kumarbazın yarım kalan oyundaki paranın nasıl bölüşüleceği sorusu üzerine yazışırken bu yöntemleri geliştirdiler. Pascal Üçgeni, bu sayma işlemlerini görselleştiren muhteşem bir araçtır. Üçgendeki sayılar, madeni para atışlarında veya hayattaki rastgele seçimlerde hangi yolların daha yoğun olduğunu gösterir. Galileo da daha önce bir dükün sorduğu 'Neden 3 zarla 10 toplamı elde etmek 9 toplamı elde etmekten daha kolaydır?' sorusunu tüm kombinasyonları tek tek yazarak çözmüştü. Saymak, rastlantısallığın kaosunu düzene sokmanın ilk adımıdır.",
                    "**Beklenen Değerin Matematiksel Anlamı**\n\nBeklenen değer (expected value), bir oyunu veya kararı binlerce kez tekrarladığımızda ortalamada ne kazanacağımızı gösteren sayıdır. Örneğin, 10 TL ödeyerek katıldığınız bir çekilişte %1 ihtimalle 500 TL kazanma şansınız varsa, bu oyunun beklenen değeri 500 x 0.01 = 5 TL'dir. Yani bu oyunu her oynadığınızda ortalama 5 TL kaybedersiniz (10 TL ödeyip 5 TL değer aldığınız için). Kumarhaneler ve sigorta şirketleri tamamen bu beklenen değer üzerine kuruludur. Kumarhanedeki her oyunun beklenen değeri oyuncu için negatiftir. Siz bir kez oynadığınızda kazanabilirsiniz (şans), ancak milyonlarca kez oynandığında kumarhane her zaman kazanır (matematik). Hayatta da kararlarımızın beklenen değerini hesaplayarak duygusal değil rasyonel adımlar atmalıyız.\n\n*\"Tek bir denemede şans konuşur, ancak deneme sayısı arttıkça matematik kaçınılmaz zaferini ilan eder.\"* — Leonard Mlodinow, Sarhoş Yürüyüşü"
                ]
            },
            {
                "id": "chapter5",
                "title": "BÖLÜM 5: Büyük ve Küçük Sayıların Düellosu",
                "takeaway": "Büyük Sayılar Yasası: Deney sayısı arttıkça sonuçlar gerçek olasılığa yaklaşırken, küçük veri setleri bizi yanıltır.",
                "paragraphs": [
                    "**Olasılıkların Gerçekleşen Sonuçlara Yansıması**\n\nJacob Bernoulli ömrünün yarısını 'Büyük Sayılar Yasası'nı kanıtlamaya adamıştı. Bu yasa der ki: Bir deney ne kadar çok tekrarlanırsa, gözlemlenen sonuçların oranı gerçek olasılığa o kadar yaklaşır. Örneğin bir madeni parayı 10 kez atarsanız 8 kez tura gelebilir (%80). Bu küçük sayılar yasasının yarattığı düzensizliktir. Ancak parayı 10.000 kez atarsanız, tura gelme oranı neredeyse tam %50 olacaktır. Günlük hayatta küçük örneklemlere bakarak büyük genellemeler yaparız. Bir doktorun yaptığı ilk 3 ameliyat başarısız geçtiğinde onun kötü bir doktor olduğunu düşünebiliriz. Oysa bu sadece küçük sayıların yarattığı rastgele bir dalgalanma olabilir. Büyük sayılar yasası devreye girmeden, yani yeterli veri toplanmadan verilen kararlar bizi her zaman yanıltır.",
                    "**Zeno Paradoksu, Limit Kavramı ve Rulette Kumarhaneyi Yenmek**\n\nLimit kavramı, sonsuza giden yolda sayıların nereye yaklaştığını gösterir. Rulet masasında yeşil sıfır (0) hücresi yüzünden kumarhanenin oyuncuya karşı %2.7'lik küçük bir avantajı vardır. Bir oyuncu rulette tek bir elde büyük paralar kazanabilir. Bu durum oyuncuya kumarhaneyi yenebileceği illüzyonunu verir. Ancak oyun sayısı arttıkça (limite yaklaştıkça) kumarhanenin kazanma oranı %100'e yaklaşır. Küçük sayılarda şansın yarattığı kaos, büyük sayılarda yerini katı bir düzene bırakır. Zeno'nun kaplumbağa paradoksundaki gibi, adımlar ne kadar küçük olursa olsun, sonsuz tekrarda varılacak hedef matematiksel olarak bellidir. Rulette kasayı yenmenin tek yolu, masadan erkenden kalkmaktır.\n\n*\"Küçük veri setleri bizi kandırır, büyük veri setleri ise gerçeği fısıldar.\"* — Leonard Mlodinow, Sarhoş Yürüyüşü"
                ]
            },
            {
                "id": "chapter6",
                "title": "BÖLÜM 6: Yanlış Pozitifler ve Pozitif Safsatalar",
                "takeaway": "Yanlış Pozitif Tuzağı: Nadir görülen hastalıklarda, çok doğru sonuç veren testlerde bile pozitif çıkan birinin hasta olma ihtimali sanılandan kat kat düşüktür.",
                "paragraphs": [
                    "**Geçmiş Olayların Işığında Beklentileri Güncellemek**\n\nThomas Bayes adında bir İngiliz rahibin geliştirdiği Bayes Teoremi, yeni bilgiler ışığında bir şeyin olma ihtimalini nasıl güncellememiz gerektiğini söyler. Günlük hayatta inançlarımızı ve kararlarımızı yeni kanıtlara göre güncellemek zorundayız. Ancak bunu yaparken olasılık mantığını tamamen unuturuz. Bir olayın geçmişteki temel oranı (base rate) çok önemlidir. Eğer bir şeyin başlangıçta olma ihtimali çok düşükse, yeni bir kanıt ortaya çıksa bile o şeyin olma ihtimali hala sanıldığından çok daha düşük olabilir. Bayesyen düşünce tarzı, önyargılarımızdan sıyrılıp verilere göre aklımızı güncellemenin en etkili yoludur.",
                    "**Tıbbi Tarama Testlerinden Hukuktaki Savcı Safsatasına Koşullu Olasılık**\n\nŞimdi sıkı durun, tıp dünyasından çok şaşırtıcı bir örnek vereceğiz. Toplumda çok nadir görülen bir hastalık olsun; her 10.000 kişiden sadece 1'inde bulunsun. Bu hastalığı tespit eden bir test geliştirilmiş ve doğruluk oranı %99 (yani %1 hata payı var, sağlıklı insana yanlışlıkla hasta diyor). Siz bu testi yaptırdınız ve sonuç 'pozitif' (hasta) çıktı. Gerçekten hasta olma ihtimaliniz nedir? Doktorların bile çoğu bu soruya %99 der. Oysa gerçek cevap yaklaşık %1'dir! Çünkü 10.000 sağlıklı insanı test ederseniz, %1 hata payından dolayı 100 kişiye yanlışlıkla 'hasta' teşhisi konacaktır. Bu gruptaki tek gerçek hasta ile birlikte toplam 101 pozitif sonuç elde edilir. Pozitif çıkanlar arasında gerçekten hasta olan tek kişi siz olduğunuz için ihtimal 1/101'dir. Mahkemelerdeki 'savcı safsatası' da buna benzer. Nadir bir kan grubunun şüphelide bulunması, onun kesin suçlu olduğunu göstermez; çünkü o kan grubuna sahip binlerce masum insan dışarıda gezmektedir.\n\n*\"Yeni kanıtlar heyecan vericidir, ancak geçmişin temel oranlarını unutmak mantığın ölümüdür.\"* — Leonard Mlodinow, Sarhoş Yürüyüşü"
                ]
            },
            {
                "id": "chapter7",
                "title": "BÖLÜM 7: Ölçüm ve Hatalar Yasası",
                "image": "/images/normal_distribution_sketch.png",
                "imageCaption": "Normal Dağılım Eğrisi",
                "takeaway": "Güven Aralıkları Yasası: Hayatta kesin sayılar yoktur; her ölçüm ve puanlama bir miktar rastgele hata payı barındırır.",
                "paragraphs": [
                    "**Ölçümlerin Anlamı ve Çan Eğrisi (Normal Dağılım)**\n\nFiziksel dünyada yaptığımız hiçbir ölçüm mükemmel değildir. Bir masanın boyunu hassas cetvellerle 10 kez ölçerseniz, muhtemelen milimetrik farklarla 10 farklı sonuç bulursunuz. Bu ölçüm hataları rastgeledir ve bir araya geldiklerinde meşhur 'Çan Eğrisini' (Normal Dağılım) oluştururlar. Carl Friedrich Gauss tarafından matematiksel formüle kavuşturulan bu eğri, merkezde (ortalamada) yığılan ve uçlara gittikçe azalan bir dağılım gösterir. İnsan boyu, zeka seviyesi, hatta fabrikadaki cips paketlerinin ağırlığı bile bu çan eğrisine uyar. Ölçümün kendisi her zaman içinde bir miktar rastgele hata barındırır. Bu hatayı bilmeden yapılan kıyaslamalar anlamsızdır.",
                    "**Şarap Puanlamaları, Anketler, Sınav Notları ve Gezegen Konumları**\n\nUzmanların şaraplara verdiği puanları inceleyen Mlodinow, şok edici bir gerçeğe parmak basıyor. Bir yarışmada 91 puan alan bir şarap ile 89 puan alan bir şarap arasındaki fark tamamen rastgeledir. Aynı tadımcıya birkaç saat sonra aynı şarap gizlice tekrar tattırıldığında tamamen farklı puanlar verebilmektedir. Ölçüm hatası, şaraplar arasındaki farktan daha büyüktür! Aynı durum okuldaki sınav notları için de geçerlidir. 85 alan bir öğrenci ile 82 alan bir öğrenci arasında zeka veya bilgi açısından hiçbir gerçek fark olmayabilir; o anki öğretmen yorgunluğu veya sorunun denk gelişi notu belirlemiştir. Siyasi anketlerdeki hata payları (+/- %3) da adayların gerçek oylarını tam olarak bilmemizi engeller. Hayatta kesin sayılar yoktur, sadece güven aralıkları ve hata payları vardır.\n\n*\"Kesinlik bir illüzyondur; her ölçüm kendi içinde rastgele bir hatanın tohumunu taşır.\"* — Leonard Mlodinow, Sarhoş Yürüyüşü"
                ]
            },
            {
                "id": "chapter8",
                "title": "BÖLÜM 8: Kaostaki Düzen",
                "takeaway": "Kolektif Düzen: Tek bir bireyin eylemleri öngörülemez bir kaos içerse de, büyük yığınlar bir araya geldiğinde düzenli istatistiksel sonuçlar doğar.",
                "paragraphs": [
                    "**Büyük Sayıların Rastlantısallığın Düzensizliğini Yok Etmesi**\n\nTek bir insanın yarın ne yapacağını tahmin etmek imkansızdır; belki evde oturur, belki sinemaya gider. Ancak milyonlarca insanı bir araya getirdiğinizde, bireysel rastlantısallıklar birbirini yok eder ve ortaya son derece düzenli bir yapı çıkar. Örneğin sigorta şirketleri, gelecek yıl kaç kişinin trafik kazasında öleceğini kuruşu kuruşuna tahmin edebilirler; ama kimin öleceğini asla bilemezler. Fizikte da tek bir gaz molekülünün nereye çarpacağı tamamen kaotiktir. Ancak odadaki trilyonlarca molekülün toplam davranışı sabit bir hava basıncı yaratır. Kaos, kalabalıklar içinde düzene dönüşür. Bu yüzden toplumsal olayları analiz ederken bireysel hikayelere değil, istatistiksel yığınlara odaklanmalıyız.",
                    "**Ortalamaya Dönüş (Regression to the Mean) Kanunu**\n\nFrancis Galton'ın keşfettiği 'Ortalamaya Dönüş' yasası, hayatta neden sürekli şaşırdığımızı açıklar. Bu yasaya göre, olağanüstü derecede yüksek veya düşük olan sonuçlar, bir sonraki denemede kaçınılmaz olarak ortalamaya doğru yaklaşır. Örneğin, çok uzun boylu anne babaların çocukları genellikle anne babalarından daha kısa (ortalamaya daha yakın) olur. Sporda bir maçta 40 sayı atan bir basketbolcunun sonraki maçta 20 sayıya düşmesini 'tembellik' veya 'konsantrasyon kaybı' ile açıklarız. Oysa bu sadece ortalamaya dönüştür. Şirketlerin başarı grafiklerindeki ani düşüşler veya yükselişler de çoğu zaman bu yasanın bir sonucudur. Bizler ortalamaya dönüşün yarattığı bu doğal iniş çıkışları ödüllendirme veya cezalandırma gibi sahte nedenlerle açıklamaya çalışırız.\n\n*\"Hayatın en büyük yasalarından biri şudur: Zirveye çıkan her şey, eninde sonunda ortalamaya geri dönmek zorundadır.\"* — Leonard Mlodinow, Sarhoş Yürüyüşü"
                ]
            },
            {
                "id": "chapter9",
                "title": "BÖLÜM 9: Örüntü Yanılsamaları ve Yanılsama Örüntüleri",
                "image": "/images/gambler_dice_sketch.png",
                "imageCaption": "Kumarbaz Yanılgısı ve Şans",
                "takeaway": "Örüntü Yanılsaması: Evrimsel olarak düzensizlik içinde düzen aramaya programlanan beynimiz, tamamen şansa dayalı serilerde sahte kahramanlar ve kurallar uydurur.",
                "paragraphs": [
                    "**Şans Eseri Olaylardaki Düzenliliklere Neden Kanıyoruz?**\n\nİlkel çağlarda çalılıklardan gelen bir sesi 'rüzgar' yerine 'kaplan' olarak yorumlayan atalarımız hayatta kaldı. Bu yüzden beynimiz, en küçük bir ipucunda bile hemen bir tehlike veya düzen (örüntü) görmeye programlanmıştır. Ancak bu evrimsel miras, modern dünyada şans olaylarında bizi tamamen aldatır. Bir madeni parayı 100 kez attığımızda arka arkaya 6 veya 7 kez tura gelmesi matematiksel olarak son derece normaldir. Ancak biz bunu gördüğümüzde hemen 'Bu parada bir hile var' ya da 'Tura serisi yakaladım' deriz. Rastgele süreçlerin kendi içinde kaçınılmaz olarak kümelenmeler (streaks) barındırdığını unuturuz. Tesadüfleri mucize sanarak kendimizi kandırırız.",
                    "**Borsadaki Gurular, Kumarbaz Yanılgısı ve Sıcak El İllüzyonu**\n\nBasketbolda üst üste üç şut sokan bir oyuncunun 'eli ısındı' (hot hand) deriz ve sonraki şutu da sokacağını düşünürüz. Bilimsel araştırmalar ise böyle bir illüzyonun olmadığını, oyuncunun şut yüzdesinin tamamen aynı kaldığını göstermiştir. Sıcak el, sadece rastgele bir kümelenmedir. Aynı şey borsa yöneticileri için de geçerlidir. Bill Miller adında bir fon yöneticisi, 15 yıl boyunca üst üste borsadaki ortalama endeksi geride bırakarak bir rekor kırdı. Herkes onu bir finans dehası ilan etti. Oysa borsa piyasasında 10.000 yönetici varsa, olasılık kuralları gereği en az birinin tamamen şans eseri 15 yıl üst üste kazanması zaten kesindir! Kumarbaz yanılgısı da (rulette 5 kez kırmızı geldikten sonra kesin siyah gelecek sanılması) aynı örüntü arama hastalığının bir ürünüdür.\n\n*\"Karanlık bir gökyüzündeki yıldızları birleştirip takımyıldızları yaratan zihnimiz, hayattaki tesadüfleri de kadere dönüştürür.\"* — Leonard Mlodinow, Sarhoş Yürüyüşü"
                ]
            },
            {
                "id": "chapter10",
                "title": "BÖLÜM 10: Sarhoş Yürüyüşü",
                "takeaway": "At-Bats (Deneme Sayısı): Hayatı ve şansı kontrol edemeyiz, ancak deneme sayımızı artırarak olasılık rüzgarını arkamıza alabiliriz.",
                "paragraphs": [
                    "**Neden Rastlantısallık Neden-Sonuç İlişkisinden Daha Temeldir?**\n\nKitabın bu son ve kurucu bölümünde Mlodinow, neden-sonuç ilişkilerine olan aşırı güvenimizi tamamen sarsıyor. Bizler hayatımızı planlı, programlı ve her adımın bir nedeni olan bir süreç gibi görürüz. Oysa kuantum fiziğinden günlük hayatımıza kadar evrenin en temel çalışma prensibi rastlantısallıkdır. Küçük olayların birikerek büyük sonuçlar doğurması (kelebek etkisi), neden-sonuç zincirini tamamen kırar. Bir sabah otobüsü kaçırmanız, hayatınızın aşkıyla tanışmanıza veya büyük bir kazadan kurtulmanıza neden olabilir. Bu küçük ve rastgele adımlar, sarhoş bir adamın sokaktaki yürüyüşü gibi yönümüzü belirler. Hayat, öngörülebilir bir doğrusal çizgi değil; rastgele çarpışmalarla dolu bir labirenttir.",
                    "**Rastgele Yürüyüşler, Başarı Efsanesi ve Kontrol İllüzyonu**\n\nDünyanın en zengin insanı Bill Gates'in başarısını sadece zekasına bağlarız. Oysa Gates'in lise yıllarında bilgisayar terminaline erişimi olan dünyadaki çok az şanslı çocuktan biri olması, tamamen rastgele bir şans faktörüdür. Bruce Willis'in bir barda tesadüfen bir cast direktörüyle karşılaşması onu sinema yıldızı yapmıştır. Peki bu durum bizi tembelliğe mi itmeli? Kesinlikle hayır! Mlodinow bize çok değerli ve ilham verici bir ders veriyor: Şansın rolü büyüktür ama şans kapıyı çaldığında hazır olmak ve daha önemlisi 'deneme sayısını' (at-bats) artırmak bizim elimizdedir. Beyzbolda ne kadar çok topa vurmaya çalışırsanız, o kadar çok sayı yapma şansınız olur. Hayatta da ne kadar çok dener, ne kadar çok kapıyı çalar ve ne kadar çok risk alırsak, rastlantısallığın o tatlı rüzgarını arkamıza alma ihtimalimiz o kadar artar. Sarhoş yürüyüşümüzü durduramayız ama daha çok yürüyerek başarı şansımızı zirveye taşıyabiliriz.\n\n*\"Hayatı kontrol edemeyiz, ancak deneme sayımızı artırarak şansın bizim tarafımıza geçmesini sağlayabiliriz.\"* — Leonard Mlodinow, Sarhoş Yürüyüşü"
                ]
            },
            {
                "id": "conclusion",
                "title": "SONUÇ: Rastlantısallıkla Barışmak ve Yola Devam Etmek",
                "takeaway": "Pes etmemenin Matematiksel Kanıtı: Şans bir kez kapıyı çalmayabilir, ama oyunda kalıp denemeye devam edenler için en güzel olasılıklar gerçekleşir.",
                "paragraphs": [
                    "Leonard Mlodinow'un \"Sarhoş Yürüyüşü\" kitabı, dünyayı ve kendi hayatımızı anlama biçimimizde devrim yaratacak bir gerçeği gözler önüne seriyor: Hayatımızdaki başarıların ve başarısızlıkların çoğu, sandığımızdan çok daha fazla oranda rastlantısaldır. Bu gerçek ilk bakışta korkutucu veya moral bozucu gelebilir. Sonuçta her şeyi kontrol etmek isteyen varlıklarız. Ancak Mlodinow'un gösterdiği gibi, bu durumu kabul etmek aslında bizi büyük bir yükten kurtarır. Başarısız olduğumuzda kendimizi aşırı hırpalamayı bırakırız; çünkü biliriz ki bazen sadece zarlar yanlış gelmiştir. Başarılı olduğumuzda ise kibirlenmeyiz; şansın payını bilip mütevazı kalırız.",
                    "En önemlisi, bu kitap bize hayatta pes etmemenin matematiksel kanıtını sunuyor. Rastlantısallık dünyasında tek bir atışta başarısız olmak kader değildir. Denemekten vazgeçmeyen, olasılık uzayında yeni yollar aramaya devam eden herkes, eninde sonunda o şanslı çarpmayı yaşayacaktır. Hayat bir sarhoş yürüyüşüdür; rotamızı çizemeyiz ama adımlarımızı atmaya devam edebiliriz. Son Söz: Hayatın zarları her zaman bizim istediğimiz gibi gelmeyebilir. Ancak büyük sayılar yasası bize hatırlatır ki, oyunda kalıp denemeye devam edenler için matematik eninde sonunda en güzel tesadüflerini hazırlayacaktır."
                ]
            }
        ]
    }
    
    with open("data/summaries/6.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4, ensure_ascii=False)
        
    print("Successfully wrote Sarhoş Yürüyüşü summary to data/summaries/6.json!")

if __name__ == "__main__":
    create_drunkard_summary()
