#!/usr/bin/env python3
"""Build the first five summaries in the twenty-book collection."""

from summary_batch_common import entry, write_books


DATE = "Temmuz 2026"
BOOKS = []


def base(no, title, author, subtitle, color, original, sources, entries):
    slug = {
        8: "gen-bencildir", 18: "sessiz-bahar", 34: "beden-kayit-tutar",
        38: "dil-icgudusu", 61: "kendime-dusunceler",
    }[no]
    return {
        "bookNo": no, "title": title, "author": author, "subtitle": subtitle,
        "coverImage": f"/images/summary-art-{no}-{slug}-v1.webp", "coverStyle": "artwork",
        "pdfUrl": f"/data/pdfs/{no}-{slug}-ozeti.pdf", "pdfLabel": "25-50 sayfalık PDF'yi indir",
        "longForm": True, "chapterArtStyle": "monochrome-engraving", "chapterArtColor": color,
        "meta": {"originalTitle": original, "compiler": "Zihin Gezgini · Yapay zeka destekli çalışma", "date": DATE, "language": "Türkçe"},
        "intro": subtitle, "sources": sources, "entries": entries,
    }


BOOKS.append(base(8, "Gen Bencildir", "Richard Dawkins",
    "Bedenlerimizi yöneten minik patronlardan söz etmeyen; doğal seçilime genin uzun ömürlü kopyaları açısından bakınca fedakarlık, aile, rekabet ve işbirliğinin nasıl yeni bir ışıkta göründüğünü anlatan sade rehber.",
    "#385D55", "The Selfish Gene",
    [
        {"id": 1, "title": "Oxford University Press - The Selfish Gene", "url": "https://www.oup.com.au/books/general-interest/biological-sciences/9780198788607"},
        {"id": 2, "title": "Google Books - The Selfish Gene içerik görünümü", "url": "https://books.google.com/books/about/The_Selfish_Gene.html?id=Gwe0ict60PMC"},
        {"id": 3, "title": "Nature Education - Akraba seçilimi", "url": "https://www.nature.com/scitable/knowledge/library/kin-selection-13216114/"},
        {"id": 4, "title": "Stanford Encyclopedia of Philosophy - Biyolojik özgecilik", "url": "https://plato.stanford.edu/entries/altruism-biological/"},
    ], [
        entry("Bu kitap nasıl okunmalı?", [
            "Başlıktaki bencillik ahlaki bir suçlama değildir. Gen düşünemez, plan kuramaz ve kimseye kötülük yapmaya karar veremez. Dawkins bu sözcüğü, çevrede kendi kopyalarının sürmesine yol açan genlerin zamanla çoğalmasını akılda tutmak için kullanır.",
            "Kitap canlıyı önemsiz saymaz. Tavşan, ağaç veya insan; genlerin etkileri, gelişim, çevre ve başka canlılarla ilişkilerinin buluştuğu karmaşık bir bütündür. Gen gözü, bu bütünün neden belirli biçimlere evrildiğini açıklayan bakışlardan yalnız biridir.",
            "Rehber boyunca biyolojik açıklama ile insanın nasıl yaşaması gerektiği ayrılacak. Doğada bir davranışın evrilmiş olması onu iyi, kaçınılmaz veya örnek alınacak hale getirmez.",
        ], "BAŞLANGIÇ"),
        entry("İlk kopyacının uzun gölgesi", [
            "Dawkins hikayeyi bugünkü hayvanlarla değil, yaşamdan önceki kimyasal dünyayla açar. Bazı moleküllerin çevredeki parçalardan kendine benzer kopyalar üretebildiğini düşünür. Kusursuz olmayan kopyalama, hem devamlılığı hem de farklılığı doğurur.",
            "Bir fotokopi makinesi her bin sayfada küçük bir leke bıraksın. Leke sonraki kopyalarda da basılır ve bazı kopyalar kağıdın yıpranmasına daha dayanıklı olursa arşiv zamanla onlarla dolar. Seçilimin mantığı için niyet değil, kalıcılık farkı yeterlidir.",
            "Bu başlangıç yaşamın kesin köken tarifi değildir; kitabın düşünce deneyidir. Asıl nokta şudur: Kendisini daha güvenilir, hızlı veya uygun koşullarda çoğaltan düzenler, çoğalamayanlara göre gelecekte daha çok temsil edilir.",
            "İnsan bedenine kadar uzanan hikayenin ilk sahnesi böylece bir kahraman değil, tekrar eden bir desendir. Yaşamın sürekliliğini bireyin ömründen daha uzun kopya zincirleri taşır.",
        ], "BİRİNCİ KISIM · GENİN BAKIŞI", art="first-replicator", caption="İlk kopyacı bilinçli bir canlı değil; kusurlu kopyalama sayesinde çeşitlenen, kalıcı bir kimyasal düzendir."),
        entry("Beden bir hayatta kalma makinesi mi?", [
            "Kitabın en çarpıcı benzetmesi bedeni genlerin hayatta kalma makinesi olarak görür. Bu, bedenin metal bir robot olduğu anlamına gelmez. Genlerin etkileriyle kurulmuş, çevreyi algılayan ve davranışı esnek biçimde ayarlayan canlı bir araçtan söz edilir.",
            "Bir tarif defteri mutfağı tek başına yönetemez. Malzeme, aşçı, sıcaklık ve zaman olmadan tarif yalnız işarettir. Gen de hücre, gelişim ve çevre olmadan sonuç üretmez. Buna rağmen tarifteki değişiklik yemeğin kuşaklar boyunca tekrar eden yönünü etkileyebilir.",
            "Birey ölür; gen kopyaları çocuklarda ve akrabalarda yoluna devam edebilir. Bu süre farkı, doğal seçilimin hesabını neden gen düzeyinde kurmanın yararlı olduğunu açıklar.",
            "Benzetmenin sınırı önemlidir. İnsan, genlerinden gelen eğilimleri fark edebilir, kurum kurabilir ve kararlarını değiştirebilir. Açıklanmış olmak, uzaktan kumandayla yönetilmek değildir.",
        ], "BİRİNCİ KISIM · GENİN BAKIŞI", art="living-machine", caption="Beden cansız robot değil; kalıtsal talimatların çevre ve gelişimle birlikte kurduğu esnek yaşam aracıdır."),
        entry("Gen aslında ne kadar büyük?", [
            "Dawkins geni yalnız göz rengi gibi tek bir özelliğin düğmesi olarak düşünmez. Seçilim açısından önemli olan, kopyalanırken yeterince uzun süre birlikte kalan ve sonuçlarıyla kendi aktarım olasılığını etkileyen DNA parçasıdır.",
            "Bir gazetede sürekli birlikte basılan kısa bir cümle, sayfanın tamamından daha kararlı bir birim olabilir. Kromozomlar mayoz sırasında parçaları değiş tokuş ettiği için çok uzun DNA blokları kuşaklar boyunca aynı kalmaz; daha küçük bölümler daha sadık yolculuk eder.",
            "Tek bir davranışın tek bir geni yoktur. Yuva kurmak, korkmak veya öğrenmek birçok genin, bedenin ve çevrenin ortak ürünüdür. Gen merkezli bakış, karmaşıklığı bir düğmeye indirmek değil, hangi kalıtsal farkın seçilimde sayıldığını sormaktır.",
            "Bu ayrım manşetlerdeki 'şunun geni bulundu' sözlerine karşı iyi bir frendir. Gen çoğu zaman kader yazan mühür değil, büyük bir orkestradaki etkili ama bağımlı bir çalgıdır.",
        ], "BİRİNCİ KISIM · GENİN BAKIŞI", art="gene-segment", caption="Seçilim birimi çoğu zaman tek özellik düğmesi değil, kuşaklar boyunca yeterince kararlı kopyalanan DNA bölümüdür."),
        entry("Bencillikten fedakarlık nasıl çıkar?", [
            "Bir kuş yırtıcıyı görünce bağırır ve kendi yerini belli eder. İlk bakışta gen merkezli görüşe ters düşen bu davranış, uyarılanların yakın akraba olması halinde farklı görünür. Akrabalar aynı genlerin bir bölümünü paylaşır.",
            "Bir evdeki iki yedek anahtarın farklı ceplerde olduğunu düşünün. Birini korumak, aynı kilidi açan öteki kopyanın geleceğini de koruyabilir. Bireyin maliyeti, akrabalarında bulunan ortak gen kopyalarının kazancıyla dengelenebilir.",
            "Hamilton kuralının sade fikri şudur: Yardımın akrabaya sağladığı yarar, akrabalık derecesiyle birlikte yardım edenin maliyetini aşarsa böyle bir eğilim seçilimle yayılabilir. Bu, hayvanın kafasında hesap makinesi taşıdığı anlamına gelmez.",
            "Fedakarlığın değerini küçültmek gerekmez. Kitap yalnızca bazı özgeci görünen davranışların evrimsel olarak nasıl mümkün olabildiğini açıklar; ahlaki iyiliğin bütün hikayesini bitirmez.",
        ], "İKİNCİ KISIM · ÇATIŞMA VE YARDIM", art="warning-bird", caption="Alarm veren kuşun bedeli, ortak genleri taşıyan yakınlarının daha çok yaşamasıyla evrimsel karşılık bulabilir."),
        entry("Anne, çocuk ve görünmeyen pazarlık", [
            "Anne ile yavrunun çıkarı tamamen aynı değildir. Anne bütün çocuklarına kaynak ayırmak zorundadır; yavru ise kendisi için biraz daha fazlasını ister. Sütten kesilme kavgası bu küçük çıkar ayrımının gündelik sahnesidir.",
            "Beş dilim pastayı üç çocuğa dağıtan ebeveyni düşünün. Her çocuk iki dilim isteyebilir, fakat ebeveyn yarını ve kardeşleri de hesaba katar. Sevgi gerçek olsa bile kaynak sınırlılığı pazarlığı ortadan kaldırmaz.",
            "Dawkins ebeveyn yatırımını gen kopyalarının geleceği üzerinden inceler. Yavrunun ağlaması, ebeveynin yanıtı ve kardeş rekabeti, tek taraflı bir komut zinciri değil karşılıklı ayarlanan stratejiler olabilir.",
            "Bu görüş insan ailesini soğuk muhasebeye indirgememelidir. Kültür, bilinç, bakım kurumları ve kişisel bağlılık biyolojik zeminin üstünde yeni imkanlar kurar. Yine de çatışma yaşandığında sevginin yok sayılmasına gerek olmadığını gösterir.",
        ], "İKİNCİ KISIM · ÇATIŞMA VE YARDIM", art="family-cake", caption="Ebeveyn ile yavru birbirini severken bile sınırlı kaynakların paylaşımında farklı çıkar noktalarına sahip olabilir."),
        entry("Guguk kuşunun sahte siparişi", [
            "Guguk kuşu yumurtasını başka türün yuvasına bırakabilir. Yavru çıktığında ev sahibinin yavrularını dışarı atar ve aç ağzıyla bütün bakımı kendine çeker. Bakım davranışı, onu tetikleyen işaretler taklit edildiğinde sömürülebilir.",
            "Otomatik kapının insanı değil hareketi algılaması gibi, hayvan da her durumu uzun uzun düşünmek yerine güvenilir işaretlere yanıt verir. Çoğu zaman işe yarayan kural, sıra dışı bir hile karşısında şaşabilir.",
            "Bu sahne evrimin kusursuz tasarım yapmadığını gösterir. Ev sahibi kuşun her yabancı yumurtayı ayırması da maliyetlidir; kendi yumurtasını yanlışlıkla atabilir. Savunma ile hile arasında bitmeyen bir yarış oluşur.",
            "Doğadaki davranışları 'türün iyiliği' diye açıklamak bu nedenle yetmez. Aynı ekosistemde bir canlının stratejisi diğerinin bakım düzenini kendi kopyaları lehine çevirebilir.",
        ], "İKİNCİ KISIM · ÇATIŞMA VE YARDIM", art="cuckoo-nest", caption="Guguk yavrusu bakım işaretlerini taklit ederek başka kuşların emek düzenini kendi lehine kullanır."),
        entry("Şahinler, güvercinler ve denge", [
            "Maynard Smith'in oyununda şahin sertçe saldırır, güvercin ise gösteri yapar ama ciddi dövüşten kaçar. Herkes şahin olursa yaralanma maliyeti yükselir; herkes güvercin olursa saldırgan bir şahin büyük avantaj kazanır.",
            "Dar bir sokakta bütün sürücüler zorla geçmeye çalışsa trafik kilitlenir. Herkes aşırı nazik olup sonsuza kadar beklerse ilk kural bozan ilerler. Sonuç, tek bir en iyi karakterden çok toplumdaki diğer davranışların oranına bağlıdır.",
            "Evrimsel olarak kararlı strateji, yaygın olduğunda nadir bir rakibin kolayca istila edemediği davranış düzenidir. Strateji burada bilinçli plan değil, kalıtsal eğilim veya tekrar eden davranış kuralıdır.",
            "Kitap böylece 'en saldırgan kazanır' klişesini bozar. Bazen temkin, bazen misilleme, bazen de davranışların karışımı kalıcı olur. Başarı, karşı karşıya geldiğiniz oyuncularla birlikte tanımlanır.",
        ], "İKİNCİ KISIM · ÇATIŞMA VE YARDIM", art="hawk-dove", caption="Şahin ile güvercin oyununda kazanç tek davranışa değil, rakiplerin oranına ve çatışmanın maliyetine bağlıdır."),
        entry("Tutuklunun ikilemi ve kısasa kısas", [
            "İki oyuncu işbirliği yaparsa ikisi de kazanır; biri diğerini satarsa hain daha çok alır; ikisi de satarsa ikisi de kötü sonuçla kalır. Tek karşılaşmada ihanet çekici görünür, tekrar eden oyunda ise gelecek gölgesi hesabı değiştirir.",
            "Aynı komşudan yıllarca merdiven istemekle, bir daha görmeyeceğiniz yabancıdan istemek aynı değildir. Bugünkü kabalık yarın kapınızı kapatabilir. Tekrarlanan ilişkiler güvene ekonomik bir değer kazandırır.",
            "Kitabın sonraki baskılarında öne çıkan kısasa kısas stratejisi ilk turda işbirliği yapar, sonra karşısındakinin önceki hamlesini tekrarlar. Ne safça iyidir ne de sonsuza dek kin tutar; hızlı karşılık verir ve barışa dönebilir.",
            "Gerçek yaşam oyundan daha karışıktır. Hatalı anlamalar, güç farkı ve kurumlar vardır. Yine de model, gen merkezli seçilimin işbirliğini dışlamadığını berrak biçimde gösterir.",
        ], "ÜÇÜNCÜ KISIM · İŞBİRLİĞİNİN YOLLARI", art="prisoners-dilemma", caption="Tekrarlanan karşılaşmalarda gelecekteki ilişki, kısa vadeli ihaneti pahalılaştırıp işbirliğine kapı açar."),
        entry("Karşılıklı iyilik neden çalışır?", [
            "Vampir yarasaları av bulamadığında aç kalabilir. Bazı bireyler daha önce kendilerine yardım eden yoldaşlarla kan paylaşır. Yardımın maliyeti verene küçük, aç alıcıya sağladığı kazanç büyükse karşılıklılık gelişebilir.",
            "Mahalle bakkalının veresiye defteri gibi, ilişki kusursuz muhasebe gerektirmez ama sürekli bedava alanı fark edecek kadar hafıza ister. Kimlik tanıma, tekrar karşılaşma ve hileciyi cezalandırma olmazsa sistem kolayca çöker.",
            "Dawkins'in dünyasında iyilik gökten düşmez; belirli koşullarda dayanıklı hale gelir. Bu açıklama, yardımın içtenliğini ölçmez. Bir davranışın uzak evrimsel kökeni ile kişinin bugünkü duygusu aynı soru değildir.",
            "Karşılıklılık bize kurumların önemini de düşündürür. İtibar, sözleşme ve şeffaflık geleceği görünür kılarak işbirliğini güçlendirebilir; anonimlik ve cezasızlık ise kısa vadeli sömürüyü cazip hale getirir.",
        ], "ÜÇÜNCÜ KISIM · İŞBİRLİĞİNİN YOLLARI", art="sharing-bats", caption="Tekrar karşılaşan ve birbirini tanıyan canlılarda küçük bir yardım gelecekte karşılık bulduğu için kalıcı olabilir."),
        entry("Sosyal böceklerin aile şehri", [
            "Arı ve karınca kolonilerinde birçok işçi kendi yavrusunu üretmeden kraliçenin yavrularına bakar. Bu büyük fedakarlık, akrabalık yapısı ve koloni yaşamının birlikte incelenmesiyle anlaşılır.",
            "Bir apartmanın daireleri değil, bütün binası çoğalıyormuş gibi düşünün. İşçiler yiyecek toplar, savunur ve yavru büyütür; kraliçe üreme görevinde uzmanlaşır. Koloni, görev bölümü güçlü bir aile ağıdır.",
            "Dawkins akrabalık hesabını önemli görür ama tek açıklama saymaz. Ekoloji, yuva yapısı ve koloni düzeyindeki düzen de sonucu etkiler. Modern tartışmalarda grup seçilimi ile kapsayıcı uyum yaklaşımları farklı ağırlıklar verir.",
            "Böcek şehrini insan toplumu için siyasi reçete yapmak hatadır. İnsan işbirliği yalnız genetik akrabalıkla kurulmaz; yabancılar hukuk, ortak amaç ve ahlaki ilkeler çevresinde birlikte yaşayabilir.",
        ], "ÜÇÜNCÜ KISIM · İŞBİRLİĞİNİN YOLLARI", art="ant-city", caption="Sosyal böcek kolonisi yakın akrabalık, görev bölümü ve ortak yuvanın birleştiği olağanüstü bir aile şehridir."),
        entry("Cinsiyetlerin çıkar hesabı", [
            "Yumurta büyük ve pahalı, sperm küçük ve bol olduğunda üreme yatırımları eşit başlamaz. Bu fark, eş seçimi, rekabet ve yavru bakımında farklı eğilimler oluşturabilir. Kitap bunları stratejik çatışma diliyle anlatır.",
            "Bir ortaklıkta iki kişi farklı miktarda sermaye koyuyorsa risk ve seçicilikleri değişebilir. Fakat biyolojik yatırım, toplumdaki bütün kadın ve erkeklerin aynı davranacağı anlamına gelmez. Türler ve kültürler arasında geniş çeşitlilik vardır.",
            "Dawkins'in bazı erken örnekleri bugünün okuruna fazla ikili ve kalıpçı gelebilir. Ebeveyn rolleri ekolojiye göre değişir; bireysel farklılık, cinsel seçilim ve toplumsal düzen basit bir şemaya sığmaz.",
            "Yararlı ders, cinsiyetleri karakter kutularına koymak değil, bakımın maliyetini ve seçenekleri incelemektir. Kim neyi kaybediyor, hangi koşulda eş seçebiliyor ve çevre oyunu nasıl değiştiriyor?",
        ], "ÜÇÜNCÜ KISIM · İŞBİRLİĞİNİN YOLLARI", art="parental-investment", caption="Üreme hücrelerinin ve bakımın farklı maliyetleri eş seçimi ile ebeveyn yatırımındaki eğilimleri etkileyebilir."),
        entry("Kuşaklar arası zaman makinesi", [
            "Bir gen bugünkü bedende geçmiş çevrelerin izlerini taşır. Seçilim geleceği görmez; geçmişte daha çok kopyalanan düzenler şimdi karşımızdadır. Çevre hızla değiştiğinde eski çözüm yeni soruna dönüşebilir.",
            "Tatlı ve yağlı yiyeceğe güçlü istek, kıtlık koşullarında yararlı olabilirken market raflarının dolu olduğu şehirde sağlık yükü yaratabilir. Düğme aynı kalmış, oda değişmiştir.",
            "Bu uyumsuzluk fikri her davranışa kolay hikaye uydurmak için kullanılmamalıdır. Geçmiş çevreyi, kalıtsallığı ve alternatif açıklamaları kanıtlamak gerekir. Güzel görünen evrim masalı tek başına veri değildir.",
            "Yine de zaman makinesi bakışı, bedenin neden kusursuz olmadığını açıklar. Evrim bugünün mühendisi değil; geçmişin malzemesini yamayarak çalışan, geleceğe kör bir tamircidir.",
        ], "DÖRDÜNCÜ KISIM · KÜLTÜR VE SINIRLAR", art="changed-room", caption="Geçmiş çevrede işe yarayan eğilim, dünya hızla değiştiğinde yeni odadaki eski bir düğme gibi sorun çıkarabilir."),
        entry("Mem: Fikrin kopyalanma macerası", [
            "Dawkins kitabın sonunda kültürel kopyacılar için 'mem' sözcüğünü önerir. Bir melodi, slogan, moda veya dua zihinler arasında taklit yoluyla yayılabilir. Başarılı olması doğru ya da iyi olduğunu garanti etmez.",
            "Telefonunuza yapışan kısa bir nakaratı düşünün. Bestecisini bilmeseniz de mırıldanır, başkasına geçirirsiniz. Kolay hatırlanma, duygu uyandırma ve tekrar fırsatı onun kültürel ömrünü uzatır.",
            "Mem, gen kadar kesin sınırları olan yerleşmiş bir bilimsel birim değildir. Kültürel fikirler aktarılırken bilinçli biçimde değiştirilir, birbirine karışır ve kurumlar tarafından güçlendirilir. Benzetme aydınlatıcı olduğu kadar sınırlıdır.",
            "İnternet çağında kavram yeni bir hayat kazandı. Fakat her viral içeriğe biyoloji etiketi yapıştırmak yerine, dikkat ekonomisi, platform tasarımı ve insan niyetini de hesaba katmak gerekir.",
        ], "DÖRDÜNCÜ KISIM · KÜLTÜR VE SINIRLAR", art="viral-melody", caption="Bir melodi veya slogan, doğru olduğu için değil kolay hatırlandığı ve tekrarlandığı için kültürde çoğalabilir."),
        entry("Uzatılmış fenotip: Bedenin dışındaki etki", [
            "Genin etkisi derinin bittiği yerde durmak zorunda değildir. Kunduzun barajı, kuşun yuvası veya parazitin konağında değiştirdiği davranış, genlerin çevrede bıraktığı sonuçlar olarak düşünülebilir.",
            "Bir ustayı yalnız ellerine bakarak değil, yaptığı köprüye bakarak da tanırız. Benzer biçimde seçilim, bir canlının dış dünyada kurduğu ve kendi kopyalarının başarısını etkileyen yapılara uzanabilir.",
            "Bu fikir genin uzaktan büyü yaptığı anlamına gelmez. Gen gelişimi etkiler, gelişim davranışı, davranış da çevreyi değiştirir. Nedensellik uzun bir zincirdir ve her halkada başka etkenler bulunur.",
            "Bakış açısı ekolojik bağlantıları genişletir. Organizma ile çevreyi iki ayrı kutu yerine, birbirinin koşullarını dönüştüren bir süreç olarak görmeye yardım eder.",
        ], "DÖRDÜNCÜ KISIM · KÜLTÜR VE SINIRLAR", art="beaver-dam", caption="Kunduzun barajı, genetik etkilerin davranış üzerinden bedenin dışına taşan sonuçlarını gösterir."),
        entry("Grup seçilimi tartışması", [
            "Kitap, hayvanların çoğu zaman 'türün iyiliği' için davrandığı açıklamasına karşı çıkar. Bireye sürekli maliyet yükleyen bir özellik, onu taşımayan hileciler daha çok ürerse grup yararlı olsa bile zayıflayabilir.",
            "Ortak kasaya herkes yüz lira koyunca mahalle parkı yapılacaktır. Bir kişi para vermeden parkı kullanabiliyorsa kısa vadede avantajlıdır. Denetim veya güçlü grup yapısı yoksa bedavacılık düzeni aşındırır.",
            "Bugün çok düzeyli seçilim yaklaşımları, gen, birey ve grup düzeylerindeki süreçleri birlikte inceleyebilir. Tartışma çoğu zaman aynı olayı farklı muhasebe dilleriyle anlatmanın nerede daha açıklayıcı olduğuna döner.",
            "Dawkins'in sert vurgusu önemli bir uyarı bırakır: 'Toplum için iyidir' demek, davranışın nasıl ortaya çıktığını açıklamaz. Maliyetin kimde, kazancın kimde ve aktarımın hangi düzeyde olduğunu göstermek gerekir.",
        ], "DÖRDÜNCÜ KISIM · KÜLTÜR VE SINIRLAR", art="public-fund", caption="Ortak yarar tek başına yetmez; bedavacıların avantajı denetlenmezse gruba faydalı düzen aşınabilir."),
        entry("Gen kader değildir", [
            "Genetik etkiyi değişmez yazgı sanmak kitabın en yaygın yanlış okumasıdır. Bir genin sonucu çevreye, diğer genlere, gelişime ve öğrenmeye bağlı olabilir. Boy uzunluğu kalıtsal olsa bile beslenme koşulları toplum ortalamasını değiştirir.",
            "Bir iskambil destesinin dağılımı oyunun başlangıcını etkiler, fakat masadaki kurallar ve oyuncunun hamleleri sonucu da biçimlendirir. Elinizdeki kartlar önemlidir; oyunun tamamı değildir.",
            "İnsan davranışında kültür, yasa ve özdenetim güçlü geri beslemeler kurar. Saldırganlığın evrimsel kökü olduğunu ileri sürmek saldırganlığı onaylamaz veya kaçınılmaz yapmaz.",
            "Dawkins de insanların biyolojik kopyacıların çıkarlarına karşı gelebilen bir öngörü geliştirebildiğini vurgular. Doğayı anlamak, ona teslim olmak için değil seçenekleri görmek için kullanılabilir.",
        ], "DÖRDÜNCÜ KISIM · KÜLTÜR VE SINIRLAR", art="cards-and-choices", caption="Genler başlangıç koşullarını etkileyen kartlar gibidir; çevre, kültür ve kararlar oyunun gidişini değiştirir."),
        entry("Bencil kelimesinin tuzağı", [
            "İnsan dilinde bencil sözü niyet, karakter ve kınama taşır. Molekül düzeyine geçirildiğinde kolayca yanlış anlaşılır. Bir gen yalnız sonuçları bakımından sanki kendi kopyasını koruyormuş gibi davranır.",
            "Gazete başlığı bilimsel benzetmenin dipnotlarını siler. 'Bencil gen insanı bencil yapar' cümlesi kitabın savını tersine çevirir; aynı gen merkezli süreç yardım, bakım ve işbirliği de üretebilir.",
            "Bu yüzden her bölümde iki soruyu ayırmak gerekir: Davranış hangi seçilim koşullarında yayılmış olabilir ve bugün bu davranışı ahlaken nasıl değerlendirmeliyiz? Birincinin cevabı ikincisini otomatik vermez.",
        ], "SON DURAKLAR"),
        entry("Kitabın eskittiği ve eskimediği yerler", [
            "Moleküler genetik, gelişim biyolojisi, epigenetik ve çok düzeyli seçilim tartışmaları 1976'dan beri genişledi. Kitaptaki kimi örnekler sadeleştirilmiş, cinsiyet anlatıları ise dönemin kalıplarını fazla taşır.",
            "Buna rağmen kalıcı araç güçlüdür: Evrimsel bir özelliği açıklarken kopyalanan kalıtsal farkı, maliyetleri ve alternatif stratejileri açıkça sormak. Bu bakış 'tür istedi, oldu' gibi kolay cümleleri zorlar.",
            "En iyi okuma kitabı son söz değil, tartışma başlatan bir mercek olarak görür. Mercek bazı ayrıntıları büyütür; bütün manzarayı tek başına göstermez.",
        ], "SON DURAKLAR"),
        entry("Gündelik hayatta kalan üç soru", [
            "Bir davranış gördüğünüzde önce yakın nedeni sorun: Şimdi ne tetikledi? Sonra gelişim nedenini sorun: Bu beceri nasıl öğrenildi veya oluştu? En son evrimsel soruyu ekleyin: Benzer bir eğilim geçmişte hangi koşullarda aktarılmış olabilir?",
            "Bu sıralama biyolojiyi her şeye yapıştırmayı engeller. İş arkadaşının kabalığını milyonlarca yıllık erkek rekabetiyle açıklamadan önce uykusuzluğu, iş düzenini ve kişisel sorumluluğu görürsünüz.",
            "Kitabın en verimli mirası tek cevap değil, düzeyleri karıştırmayan meraktır. Genin bakışı güçlüdür; insan hayatı ise yalnız o bakıştan daha büyüktür.",
        ], "SON DURAKLAR"),
        entry("Bir cümlede kitabın özü", [
            "Doğal seçilime gen kopyalarının uzun yolculuğundan bakınca rekabet kadar fedakarlık ve işbirliği de anlaşılır hale gelir; fakat bu açıklama insanın ahlaki kaderini yazmaz.",
            "Akılda kalacak görüntü şudur: Kuşaklar boyunca aktarılan bir tarif, her yeni mutfakta farklı malzemelerle pişer. Tarif önemlidir, mutfak önemlidir ve aşçı da masada oturmaktadır.",
        ], "SON DURAKLAR"),
    ]))


BOOKS.append(base(18, "Sessiz Bahar", "Rachel Carson",
    "Bir kasabanın kuş seslerini susturan görünmez kimyasallardan başlayıp tarım, su, toprak, beden, şirket ve kamu sorumluluğunu aynı canlı ağında buluşturan; çevre düşüncesini değiştirmiş araştırmacı anlatı.",
    "#667542", "Silent Spring",
    [
        {"id": 1, "title": "Rachel Carson Council - Silent Spring", "url": "https://www.rachelcarson.org/silent-spring"},
        {"id": 2, "title": "US EPA - DDT'nin kısa tarihi ve düzenlenmesi", "url": "https://www.epa.gov/ingredients-used-pesticide-products/ddt-brief-history-and-status"},
        {"id": 3, "title": "US Fish and Wildlife Service - DDT ve yırtıcı kuşların toparlanması", "url": "https://www.fws.gov/story/threats-birds-ddt"},
        {"id": 4, "title": "WHO - Vektör kontrolünde DDT değerlendirmesi", "url": "https://www.who.int/publications/i/item/9789241572415"},
    ], [
        entry("Bu kitap nasıl okunmalı?", [
            "Sessiz Bahar bütün kimyasalları şeytan ilan eden bir kitap değildir. Carson'ın hedefi, güçlü ve kalıcı zehirlerin etkileri anlaşılmadan geniş alanlara savrulması, zarar kanıtlarının küçümsenmesi ve halka seçim hakkı verilmemesidir.",
            "Kitap 1962'nin bilgisiyle yazıldı. Bazı maddeler ve düzenlemeler değişti, fakat temel soru canlı kaldı: Bir teknolojinin kısa vadeli yararı, uzun vadeli ve dağınık bedellerinden nasıl ayrılır?",
            "Rehber, Carson'ın bölüm yürüyüşünü izler; su, toprak, kuş, böcek ve insan bedenini ayrı dosyalar gibi değil birbirine açılan kapılar olarak anlatır.",
        ], "BAŞLANGIÇ"),
        entry("Yarın için bir masal", [
            "Carson önce adı olmayan bir Amerikan kasabası kurar. Çiftlikler, bahçeler, balık dolu dereler ve ilkbaharda kuş sesleri vardır. Sonra açıklanamayan bir gölge iner; hayvanlar ölür, çocuklar hastalanır, bahar sessizleşir.",
            "Bu kasaba haritada tek nokta değildir. Yazar, birçok gerçek yerde görülen olayları birleştirerek okura geleceğin provasını gösterir. Masalın cadısı yoktur; felaket insanların kendi uygulamalarından doğar.",
            "Bir duman alarmını düşünün. Alarm size evin kesin yanacağını söylemez; kokuyu görmezden gelirseniz ne olabileceğini gösterir. Açılış bölümü de bilimsel kanıtların yerine geçmez, onları dinlemeye hazırlar.",
            "Kuşsuz bahar görüntüsü kitabın hafıza kancasıdır. Sorunu tonlarca kimyasal adıyla değil, kaybolan bir sabah sesiyle hissederiz.",
        ], "BİRİNCİ KISIM · GÖRÜNMEZ YAĞMUR", art="silent-town", caption="Carson'ın bileşik kasabasında kimyasal serpinti sonrası ilkbahar gelir ama kuşların sabah korosu geri dönmez."),
        entry("Savaş laboratuvarından tarlaya", [
            "İkinci Dünya Savaşı sırasında geliştirilen sentetik kimyasallar, savaş sonrasında böceklerle mücadelede büyük umut yarattı. DDT gibi maddeler ucuz, etkili ve kalıcıydı. Tam da bu kalıcılık daha sonra sorunun merkezine yerleşti.",
            "Bir çiviyi çok iyi çakan çekicin her sorunu çivi gibi göstermesi mümkündür. Bir böcek ilacı kısa vadede zararlıyı azaltınca daha geniş alan, daha yüksek doz ve daha sık uygulama kolayca normalleşir.",
            "Carson doğanın kimyasal müdahaleye hazırlıksız olduğunu söyler. Yeni moleküller toprağa, suya ve yağ dokularına girer; uygulama bittikten sonra da yolculuğunu sürdürür.",
            "Kitabın itirazı yeniliğe değil, kontrolsüz ölçeğe yönelir. Laboratuvarda etkili görünen ürün, milyonlarca canlı ve değişken çevreyle karşılaşınca başka sonuçlar doğurabilir.",
        ], "BİRİNCİ KISIM · GÖRÜNMEZ YAĞMUR", art="war-to-field", caption="Savaş döneminin güçlü kimyasalları barışta tarım aracına dönüşürken kalıcılıkları görünmeyen bir çevre maliyeti yarattı."),
        entry("İksir denilen zehir", [
            "Ürünler halka mucize çözüm gibi sunulurken Carson sinir sistemini bozan, hormonlara ve hücre süreçlerine karışabilen etkileri anlatır. 'Böcek öldürücü' etiketi, maddenin yalnız hedef böceği tanıdığı yanılsamasını yaratır.",
            "Bir apartmanın zilini çalmak yerine bütün elektrik hattına yüksek voltaj vermek gibi düşünün. Zararlı hedeflenir ama aynı biyolojik temel süreçleri kullanan başka canlılar da etkilenebilir.",
            "Doz önemlidir, fakat maruz kalma yalnız tek büyük olay değildir. Küçük miktarlar besin zincirinde birikebilir; farklı maddeler birlikte beklenmedik etkiler gösterebilir.",
            "Carson'ın dili zaman zaman serttir çünkü teknik terimlerin altında saklanan ahlaki tercihi görünür kılmak ister: Kimin tarlası korunuyor, kimin suyu ve bedeni risk alıyor?",
        ], "BİRİNCİ KISIM · GÖRÜNMEZ YAĞMUR", art="elixir-bottle", caption="Böcek ilacı etiketi hedefi dar gösterse de kimyasal, ortak biyolojik süreçler nedeniyle başka canlılara da ulaşabilir."),
        entry("Toprağın altındaki şehir", [
            "Toprak boş kahverengi madde değildir. Bakteriler, mantarlar, solucanlar ve küçük canlılar organik kalıntıları parçalar, besinleri döndürür ve köklerin yaşayacağı yapıyı kurar.",
            "Bir şehrin çöpçülerini, su ekibini ve tamircilerini aynı gün ortadan kaldırdığınızı düşünün. Binalar ayakta görünür ama sistem içeriden çökmeye başlar. Toprak canlıları da tarlanın görünmeyen hizmet ağıdır.",
            "Kalıcı kimyasallar üstten püskürtülse bile yağmurla aşağı iner, parçalanma hızını ve tür dengesini etkileyebilir. Sorun yalnız o yılın hasadı değil, toprağın sonraki yıllardaki üretkenliğidir.",
            "Carson böylece 'zararlı böcek öldü mü?' sorusunu büyütür. Uygulama, ürünün dayandığı görünmez topluluğa ne yaptı?",
        ], "İKİNCİ KISIM · CANLI AĞ", art="soil-city", caption="Toprağın altındaki bakteri, mantar ve solucan şehri tarlanın besin döngüsünü sessizce ayakta tutar."),
        entry("Su hiçbir şeyi yerinde bırakmaz", [
            "Tarlaya düşen kimyasal tarla sınırında durmaz. Yağmur onu dereye, göle ve yeraltı suyuna taşıyabilir. Suda yaşayan böcekler, balıklar ve onları yiyen kuşlar yeni bir maruz kalma zincirine girer.",
            "Mutfakta yere dökülen boya su kanalına karıştığında artık tek odanın sorunu değildir. Su hareket eder, seyreltir ama aynı zamanda uzaklara taşır ve çökellerde biriktirebilir.",
            "Carson'ın örneklerinde balık ölümleri bazen uygulamadan günler sonra veya kilometreler ötede belirir. Neden ile sonuç arasındaki mesafe sorumluluğu görünmez kılar.",
            "Modern çevre yönetiminin havza yaklaşımı bu dersi taşır: Su, idari sınırları tanımaz. Bir belediyenin kararı aşağıdaki köyün içme suyuna dönüşebilir.",
        ], "İKİNCİ KISIM · CANLI AĞ", art="moving-water", caption="Yağmur kimyasalı tarla sınırından çıkarıp dere, göl, çamur ve besin zinciri boyunca uzaklara taşır."),
        entry("Biriken küçük dozlar", [
            "Bazı kalıcı maddeler canlı dokusunda kolayca parçalanmaz. Küçük su canlısı az miktar alır, onu çok sayıda yiyen balık daha fazlasını biriktirir, balığı yiyen kuşta yoğunluk daha da artar.",
            "Her biri bir damla boya taşıyan yüz süngeri tek kovada sıkarsanız renk koyulaşır. Biyobirikim ve besin zincirinde yoğunlaşma da dağınık küçük miktarların üst basamakta birleşmesini anlatır.",
            "DDT'nin parçalanma ürünü DDE, yırtıcı kuşlarda yumurta kabuğunun incelmesiyle ilişkilendirildi. Yetişkin kuş hemen ölmese bile gelecek kuşak kırılgan hale gelebilir.",
            "Bu sahne risk hesabını değiştirir. Yalnız uygulama anındaki zehirlenmeyi değil, zaman içinde biriken ve üremeyi etkileyen sonuçları da izlemek gerekir.",
        ], "İKİNCİ KISIM · CANLI AĞ", art="food-chain", caption="Dağınık küçük dozlar besin zincirinin üst basamaklarında birleşerek yırtıcı kuşların üremesini bozabilir."),
        entry("Kuşların kırılan geleceği", [
            "Carson kuş ölümlerini kitabın duygusal ve bilimsel merkezine taşır. İlaçlanan alanlarda böcek yiyen kuşlar zehirlenir, tohum yiyenler kaplanmış tohumlardan etkilenir, yırtıcılar kirlenmiş avı tüketir.",
            "Bahçede ölü bir ardıç kuşu tek olay gibi görünebilir. Aynı desen farklı kasabalarda tekrarlandığında kişisel üzüntü kamu kanıtına dönüşür. Vatandaş gözlemleri araştırmacıların dikkatini çeker.",
            "Kuşlar yalnız güzel ses değildir; böcekleri yer, tohum taşır ve ekosistemin durumunu haber verir. Sessizlik bir estetik kayıp kadar sistemin alarmıdır.",
            "Kitabın etkisi burada anlatım gücünden gelir. Carson sayıları küçümsemez; sayının temsil ettiği yaşamı tekrar görünür kılar.",
        ], "İKİNCİ KISIM · CANLI AĞ", art="broken-egg", caption="İncelmiş kabuk yalnız bir yumurtanın kırılması değil, görünmez kimyasalın gelecek kuşağa uzanan izidir."),
        entry("Hedef dışındaki dostlar", [
            "Bir zararlı böceği öldürmek için geniş etkili ilaç kullanıldığında arılar, uğur böcekleri ve zararlıyı yiyen yırtıcılar da kaybolabilir. Doğal denetim zayıflayınca yeni salgınlar ortaya çıkabilir.",
            "Bahçedeki hırsızı yakalamak için bütün güvenlik görevlilerini de binadan çıkardığınızı düşünün. İlk anda sessizlik sağlanır, sonra korumasız yapı daha büyük soruna açılır.",
            "Carson doğadaki dengeyi donmuş bir huzur hali olarak anlatmaz. Türler sürekli etkileşir; birini sertçe çekmek diğerlerinin sayısını değiştirir.",
            "Bu yüzden başarı yalnız ilk haftadaki ölü böcek sayısıyla ölçülmemelidir. Bir yıl sonra ürün, tozlaşma, doğal düşmanlar ve yeni zararlılar birlikte değerlendirilmelidir.",
        ], "ÜÇÜNCÜ KISIM · KONTROLÜN TERSİ", art="lost-pollinators", caption="Geniş etkili ilaç zararlıyla birlikte arı ve doğal avcıları da yok ederek tarlanın savunma ağını zayıflatabilir."),
        entry("Direncin dönen kapısı", [
            "Bir ilaç ilk uygulamada böceklerin çoğunu öldürür. Doğuştan daha dayanıklı az sayıdaki birey yaşar ve ürer. Sonraki kuşaklarda aynı ilaç daha az etkili olur; doz artırılır veya yeni kimyasal aranır.",
            "Antibiyotik direncinde olduğu gibi ilaç böceğe eğitim vermez. Zaten bulunan farklılıklar arasından dayanıklı olanları seçer. Uygulama, kendi gelecekteki başarısızlığının koşulunu hazırlayabilir.",
            "Bir kilidi her gece aynı anahtarla korumaya çalışırken yalnız o anahtarı aşan hırsızların kalması gibi, tek yönteme aşırı güven rakibi süzer.",
            "Carson'ın uyarısı günceldir: Evrim durmaz. Mücadele programı değişken, hedefli ve doğal düşmanları koruyan bir düzen kurmazsa kimyasal koşu bandına dönüşür.",
        ], "ÜÇÜNCÜ KISIM · KONTROLÜN TERSİ", art="resistance-wheel", caption="İlaç hassas böcekleri elerken dayanıklı olanlar ürer; aynı çözüm zamanla kendi etkisini aşındırır."),
        entry("Ateş karıncasına karşı bombardıman", [
            "Carson, ateş karıncasına karşı yürütülen geniş alanlı ilaçlama programlarını örnek verir. Büyük bütçe ve uçaklar güçlü müdahale görüntüsü yaratır, fakat hedefin zararı ile uygulamanın toplam bedeli orantılı olmayabilir.",
            "Bir mutfakta birkaç karınca gördüğü için bütün evi zehirli sisle doldurmak hızlı görünür. Oysa evcil hayvan, yiyecek ve komşu da aynı havayı solur. Ölçek büyüdükçe yan etki büyür.",
            "Kamu programlarında başarısızlığı kabul etmek zordur; yatırılan para ve itibar devam baskısı yaratır. Carson bilimsel kanıt kadar kurumların bu körlüğüne de dikkat çeker.",
            "Ders yalnız geçmişe ait değildir. Büyük proje, etkileyici teknoloji ve acil söylem bir araya geldiğinde 'daha hedefli seçenek var mı?' sorusu özellikle önem kazanır.",
        ], "ÜÇÜNCÜ KISIM · KONTROLÜN TERSİ", art="aerial-spray", caption="Uçakla geniş alanı ilaçlamak güçlü görünür, fakat hedef küçükken yan etkilerin coğrafyası çok daha büyük olabilir."),
        entry("İnsan bedeni de ağın içinde", [
            "Carson çevreyi insanın dışındaki yeşil dekor olarak görmez. İçtiğimiz su, yediğimiz ürün ve soluduğumuz hava kimyasal yolculuğun devamıdır. Doğa zarar görürken insanın cam fanusta kalması mümkün değildir.",
            "Vücudun karaciğer ve enzim sistemleri birçok maddeyi dönüştürür, fakat kapasite sınırsız değildir. Yağda çözünen kalıcı maddeler dokuda birikebilir; hassasiyet yaşa ve koşula göre değişebilir.",
            "Kitaptaki kanser ve genetik hasar tartışmaları dönemin araştırmalarını yansıtır. Bugün her madde için risk ayrı ölçülür; 'kimyasal' kelimesi tek başına zehir demek değildir.",
            "Carson'ın kalıcı katkısı maruz kalma hakkındaki sorudur: Bir ürün piyasaya çıkmadan önce güvenliği kim kanıtlamalı ve istemeyen kişi ortak hava ile sudan nasıl korunmalı?",
        ], "ÜÇÜNCÜ KISIM · KONTROLÜN TERSİ", art="body-in-web", caption="İnsan bedeni çevrenin dışında değildir; su, yiyecek ve hava canlı ağın kimyasal izlerini içeri taşır."),
        entry("İki zehrin bilinmeyen dansı", [
            "Düzenlemeler çoğu zaman tek maddeyi tek dozda inceler. Gerçek yaşamda insanlar farklı pestisitler, ilaçlar ve endüstriyel maddelerle zaman içinde karşılaşır. Birlikte etkiler basit toplam olmayabilir.",
            "İki sakin müzisyenin aynı anda çalınca gürültü çıkarması gibi, maddeler aynı enzimi kullanabilir veya birbirinin parçalanmasını yavaşlatabilir. Bu olasılık belirsizliği büyütür.",
            "Belirsizlik hiçbir şey yapmamak için mazeret de her şeyi yasaklamak için kanıt da değildir. Carson ihtiyatı, alternatifleri ve izlemeyi savunur.",
            "Bugünün risk bilimi daha gelişmiş olsa da karışım sorunu tamamen çözülmüş değildir. Kitabın 'tek şişe' yerine yaşam boyu maruz kalma bakışı bu nedenle değerlidir.",
        ], "DÖRDÜNCÜ KISIM · DEMOKRATİK SORU", art="chemical-dance", caption="Gerçek yaşamda maddeler tek tek değil karışım halinde karşılaşır; ortak etkileri basit toplamdan farklı olabilir."),
        entry("Bilgi kimin elinde?", [
            "Carson şirket raporları, kamu uzmanları ve bağımsız araştırmacılar arasındaki güç farkını görünür kılar. Ürünü satan taraf veriyi üretirken zarar gören vatandaş çoğu zaman neye maruz kaldığını bile bilmez.",
            "Bir mahkemede yalnız sanığın tuttuğu tanıkların konuştuğunu düşünün. Hepsi yalan söylemese bile eksik düzen güven yaratmaz. Bağımsız araştırma ve açık veri bu nedenle teknik ayrıntı değil demokrasi koşuludur.",
            "Yazar kendisine yönelen duygusal, bilim dışı ve ilerleme düşmanı suçlamalarına belgelerle karşılık verdi. Tartışma, bilimin çıkar çatışmasından bağımsız yürümeyeceğini gösterdi.",
            "Bugün de güven, yalnız 'uzmanlar böyle diyor' cümlesiyle kurulmaz. Yöntemin, finansmanın, belirsizliğin ve itiraz yollarının görünür olması gerekir.",
        ], "DÖRDÜNCÜ KISIM · DEMOKRATİK SORU", art="closed-files", caption="Çevre kararı güvenilir olmak için verinin, finansmanın ve belirsizliğin halka açık olduğu bir masa gerektirir."),
        entry("Başka bir yol mümkün", [
            "Carson kitabı yalnız felaketle bitirmez. Zararlının doğal düşmanlarını kullanma, erkek böcekleri kısırlaştırma, yaşam döngüsünün hassas anını hedefleme ve yalnız sorunlu bölgeye müdahale etme gibi seçenekleri anlatır.",
            "Doktorun her hastaya aynı güçlü ilacı vermek yerine tanı koyması gibi, entegre mücadele de önce türü, eşiği ve ekosistemi tanır. Kimyasal gerekirse son ve hedefli araçlardan biri olur.",
            "Alternatif yöntemler sabır ve yerel bilgi ister; gökyüzünden tek geçiş kadar gösterişli değildir. Fakat doğal denetimi koruduğu için uzun vadede daha dayanıklı olabilir.",
            "Kitabın umudu teknoloji karşıtlığı değil, daha akıllı teknoloji ve alçakgönüllü yönetimdir. İnsan doğanın dışında komutan değil, sonuçlara dahil bir katılımcıdır.",
        ], "DÖRDÜNCÜ KISIM · DEMOKRATİK SORU", art="targeted-control", caption="Hedef türü ve yaşam döngüsünü tanıyan yöntemler, bütün canlı ağı zehirlemeden sorunu azaltabilir."),
        entry("Kennedy'nin masasına ulaşan kitap", [
            "Silent Spring yayımlandığında büyük tartışma yarattı. Başkan John F. Kennedy'nin bilim danışma kurulu pestisitleri inceledi; kamuoyu çevre risklerini ulusal mesele olarak konuşmaya başladı.",
            "Tek kitap tek başına bütün kurumları kurmadı. Çevre hareketleri, bilim insanları, kuş gözlemcileri ve yurttaş örgütleri zaten çalışıyordu. Carson onların dağınık kanıtlarına ortak bir dil verdi.",
            "ABD'de DDT'nin tarımsal kullanımı daha sonra yasaklandı ve yırtıcı kuşların toparlanması önemli başarı örneklerinden biri oldu. Dünyanın bazı bölgelerinde sıtma vektörü kontrolünde sınırlı DDT kullanımı ise risk ile yarar tartışmasının bağlama bağlı kaldığını gösterir.",
            "Mirasın en dürüst anlatımı budur: Kitap sihirli düğme değildi; toplumsal yönü değiştiren güçlü bir kaldıraçtı.",
        ], "DÖRDÜNCÜ KISIM · DEMOKRATİK SORU", art="book-on-desk", caption="Carson'ın kitabı dağınık çevre kanıtlarını kamu tartışmasına taşıyan ve kurumları harekete geçiren bir kaldıraç oldu."),
        entry("Carson neyi söylemedi?", [
            "Yaygın efsanenin aksine Carson bütün pestisitlerin koşulsuz yasaklanmasını istemedi. Ayrım yapmadan, gereksiz ve geniş ölçekli kullanıma itiraz etti; biyolojik ve hedefli yöntemleri öne çıkardı.",
            "DDT sıtma taşıyan sivrisineklere karşı bazı koşullarda halk sağlığı aracı olmuştur. Bu gerçek çevre zararlarını silmez; kararın hastalık yükü, direnç, uygulama biçimi ve alternatiflerle birlikte verilmesini gerektirir.",
            "Kitabı doğru okumak iki kolay uçtan kaçınmaktır: 'Kimyasal her zaman kötüdür' ve 'ürün işe yarıyorsa yan etkisi önemsizdir.' Carson'ın asıl alanı bu iki slogan arasındaki sorumlu muhakemedir.",
        ], "SON DURAKLAR", art="balanced-scale", caption="Carson'ın savı bütün ilaçları tek kefeye koymak değil, yarar ile görünmeyen bedeli bağlama göre birlikte tartmaktır."),
        entry("Korku ile kanıt arasındaki çizgi", [
            "Carson güçlü imgeler kullanır, fakat dayanağını vaka raporları ve araştırmalardan kurar. Yine de her tarihsel örnek bugünkü her pestisite doğrudan uygulanamaz. Madde, doz ve kullanım biçimi ayrı değerlendirilmelidir.",
            "İhtiyat ilkesi bilinmeyen her şeyi yasaklama düğmesi değildir. Zararın ciddi ve geri döndürülemez olabileceği yerde kanıtın tamamlanmasını beklerken daha güvenli seçenek seçmektir.",
            "Okur için iyi kontrol sorusu şudur: İddia hangi madde, hangi doz, hangi canlı ve hangi süre için geçerli? Bu ayrıntılar korkuyu bilgiye çevirir.",
        ], "SON DURAKLAR"),
        entry("Bugünün market rafında kitap", [
            "Bir ürün 'doğal' diye otomatik güvenli, sentetik diye otomatik tehlikeli değildir. Risk, tehlikenin yanında maruz kalma miktarı ve yoluyla belirlenir. Arsenik doğaldır ama güvenli değildir.",
            "Tüketicinin tek başına bütün kimya laboratuvarını kurması beklenemez. Etiket, denetim, bağımsız araştırma ve şeffaf kurumlar kişisel seçimin altyapısıdır.",
            "Carson'ın bugüne kalan davranışı, görünmez maliyeti sormaktır: Bu kolaylığın atığı nereye gidiyor, kim maruz kalıyor ve etkisi kaç yıl sürüyor?",
        ], "SON DURAKLAR"),
        entry("Bir cümlede kitabın özü", [
            "Doğayı hedeflerden oluşan bir atış poligonu sanırsak attığımız kimyasal, su ve besin zinciri üzerinden dönüp bizi de bulur; akıllı kontrol canlı ağın bağlantılarını hesaba katar.",
            "Akılda kalacak görüntü boş bir bahar sabahıdır. Sessizlik, yalnız kaybolmuş kuşların değil, görünmeyen kararların duyulur hale gelmiş sesidir.",
        ], "SON DURAKLAR"),
    ]))


BOOKS.append(base(34, "Beden Kayıt Tutar", "Bessel van der Kolk",
    "Travmanın yalnız geçmişte kalan kötü bir anı değil, alarm sistemi, beden duyusu, ilişki ve zaman hissinde süren bir iz olabileceğini; iyileşmenin güvenli bağ ve bedensel sahiplikle nasıl desteklenebileceğini anlatan dikkatli rehber.",
    "#7A4C54", "The Body Keeps the Score",
    [
        {"id": 1, "title": "Bessel van der Kolk - Resmi kitap sayfası", "url": "https://www.besselvanderkolk.com/resources/the-body-keeps-the-score"},
        {"id": 2, "title": "US Department of Veterans Affairs - PTSD tedavileri", "url": "https://www.ptsd.va.gov/understand_tx/tx_basics.asp"},
        {"id": 3, "title": "WHO - Travma sonrası stres bozukluğu", "url": "https://www.who.int/news-room/fact-sheets/detail/post-traumatic-stress-disorder"},
        {"id": 4, "title": "NICE - PTSD değerlendirme ve tedavi rehberi", "url": "https://www.nice.org.uk/guidance/ng116"},
    ], [
        entry("Önce güvenlik notu", [
            "Bu kitap travma yaşamış kişilerden ayrıntılı öyküler içerir. Zorlanırsanız bölümü atlamak, ara vermek veya güvendiğiniz biriyle konuşmak başarısızlık değildir. Rehber sahneleri gereksiz ayrıntıya girmeden aktarır.",
            "Travma sözcüğü her üzüntünün eş anlamlısı değildir. Kişinin güvenlik, beden ve zaman algısını uzun süre bozan ezici yaşantılardan söz ediyoruz. Aynı olay herkeste aynı sonucu doğurmaz.",
            "Kitap tedavi reçetesi değildir. Belirtiler yaşamı zorluyorsa ruh sağlığı uzmanının kişiye özel değerlendirmesi gerekir; özellikle kendine zarar düşüncesi veya acil tehlikede yerel acil destek aranmalıdır.",
        ], "BAŞLANGIÇ"),
        entry("Savaş bitse de beden nöbette", [
            "Van der Kolk genç bir doktorken Vietnam gazileriyle çalışır. Askerler eve dönmüştür, fakat küçük bir ses, koku veya tartışma bedeni yeniden savaş alanına taşır. Takvim ilerler, sinir sistemi ilerlememiş gibi davranır.",
            "Gece alarmı bozuk bir dükkanda düşünün. Hırsız gitmiştir ama perde sallandığında siren çalar. Sorun alarmın zayıf olması değil, tehlike eşiğinin fazlasıyla hassaslaşmasıdır.",
            "Gazilerin öfkesi yalnız kötü karakter, uyuşukluğu yalnız isteksizlik olarak görüldüğünde asıl düzen kaçırılır. Uyku, dikkat, yakınlık ve beden tepkileri ortak bir geçmiş etrafında birleşir.",
            "Kitabın ilk büyük dönüşü budur: 'Sana ne oldu?' sorusu, 'Sende ne yanlış?' sorusundan daha açıklayıcı olabilir.",
        ], "BİRİNCİ KISIM · ALARMDA KALAN BEDEN", art="soldier-home", caption="Savaş alanı geride kalsa da ses ve kokular alarm sistemini bugünde yeniden harekete geçirebilir."),
        entry("Tehlike anında beynin hızlı yolu", [
            "Beyin tehlike işaretini önce hızlı ve kaba biçimde değerlendirir. Bedenin savaşma, kaçma veya donma hazırlığı, bilinçli düşünceden önce başlayabilir. Kalp hızlanır, kaslar gerilir, dikkat daralır.",
            "Yolda kıvrılmış hortumu bir an yılan sanmanız yararlı bir yanlış alarmdır. Önce sıçrar, sonra bakarsınız. Travmadan sonra bu hızlı sistem çok daha sık devreye girebilir.",
            "Kişi mantıken güvende olduğunu bilse bile bedeni ikna olmayabilir. Bu çelişki 'neden kendime söz geçiremiyorum?' utancını büyütür.",
            "Anlamak mazeret üretmek değildir. Tepkinin otomatik katmanını görmek, onu düzenlemek için beden, dikkat ve ilişki üzerinden yeni yollar denemeyi mümkün kılar.",
        ], "BİRİNCİ KISIM · ALARMDA KALAN BEDEN", art="false-alarm", caption="Travma sonrası hızlı alarm yolu sıradan bir hortumu bile yılan gibi algılayacak kadar hassaslaşabilir."),
        entry("Anı değil, yeniden yaşanan şimdi", [
            "Sıradan anı geçmiş zaman etiketi taşır. Travmatik anı ise parça parça görüntü, ses, koku veya beden duyusu halinde geri gelebilir. Kişi olayı hatırlamaktan çok yeniden içindeymiş gibi hisseder.",
            "Eski bir film dosyasının klasöre kaydedilmediğini ve rastgele ekrana fırladığını düşünün. Zihin 'bu olmuştu' diyemez; görüntü 'şimdi oluyor' gücüyle belirir.",
            "Bazı kişiler ayrıntıları yoğun biçimde yaşarken bazıları boşluk, kopukluk veya uyuşma hisseder. Unutma ve taşma aynı sistemin farklı korunma yolları olabilir.",
            "İyileşmenin amaçlarından biri anıyı silmek değil, onu geçmişteki yerine yerleştirebilmektir. Olay hayat hikayesinin bölümü olur; bütün kitabın kapağı olmaktan çıkar.",
        ], "BİRİNCİ KISIM · ALARMDA KALAN BEDEN", art="unfiled-film", caption="Travmatik parça geçmiş etiketi taşımadığında hatıra gibi değil, şimdide açılan bir film gibi yaşanabilir."),
        entry("Donmak da hayatta kalma tepkisidir", [
            "Tehlikede herkes savaşmaz veya kaçmaz. Kaçış mümkün görünmediğinde beden donabilir, hareketi ve duyuyu azaltabilir. Sonradan 'neden bir şey yapmadım?' diye kendini suçlayan kişi, otomatik korunma tepkisini irade eksikliği sanabilir.",
            "Elektrik sistemi aşırı yükte sigortayı indirir. Ev karanlıkta kalır ama yangın riski azalır. Donma ve kopma da bazen dayanılmaz deneyimin şiddetini kısan acil sigorta gibi çalışır.",
            "Olay bittikten sonra sigortanın sürekli kapalı kalması yaşamı daraltır. Kişi sevinç, yakınlık ve beden duyularından da uzaklaşabilir.",
            "Bu tepkiyi anlamak utancı hafifletebilir. Geçmişte işe yarayan korunma, bugün yavaş ve güvenli biçimde yeniden ayarlanabilir.",
        ], "BİRİNCİ KISIM · ALARMDA KALAN BEDEN", art="frozen-body", caption="Kaçış mümkün olmadığında donma, irade zayıflığı değil bedenin aşırı yükte indirdiği koruyucu sigorta olabilir."),
        entry("Bedenin iç haritası", [
            "Açlık, nefes, kalp atışı, kas gerilimi ve sıcaklık gibi iç sinyalleri fark etme yeteneğine iç algı denir. Travma bu sinyalleri ya dayanılmaz gürültüye ya da hissedilmeyen sessizliğe çevirebilir.",
            "Arabanın gösterge paneli ya sürekli kırmızı yanıyor ya da tamamen sönükse sürücü doğru karar veremez. Beden haritası da tehlike ile ihtiyaç arasındaki ayrımı zorlaştırabilir.",
            "Kişi korkuyu 'midemde düğüm ve hızlı nefes' diye fark edebildiğinde, duygu adsız bir felaket olmaktan çıkar. Fakat bedene dönmek bazı kişiler için başta daha zorlayıcı olabilir.",
            "Bu nedenle çalışma zorla değil, küçük dozlarda ve güvenli ilişkide ilerlemelidir. Hedef beden üzerinde yeniden merak ve seçim hissi kurmaktır.",
        ], "İKİNCİ KISIM · HAFIZA VE BENLİK", art="body-map", caption="İç beden sinyalleri güvenilir bir gösterge paneline dönüştükçe kişi alarm ile gerçek ihtiyacı ayırabilir."),
        entry("Ad koymak, fırtınayı görmek", [
            "Yoğun duyguda konuşma ve düzenleme güçleşebilir. Kişi yalnız 'kötüyüm' derken bedeni birçok ayrı sinyal taşır. Duyguya ve duyuma ad vermek, deneyim ile benlik arasına küçük bir mesafe koyar.",
            "Pencereden fırtınaya bakmakla fırtınanın içinde sürüklenmek farklıdır. 'Şu anda korku yükseliyor' cümlesi korkuyu yok etmez; onun gözlemcisini yeniden kurar.",
            "Kitap dilin önemli ama tek başına yeterli olmadığını savunur. Travma söz öncesi ve bedensel katmanlarda saklanabilir; yalnız neden-sonuç anlatmak alarmı susturmayabilir.",
            "Yine de güvenli anlatı dağınık parçaları zaman çizgisine bağlar. Söz ve beden rakip tedaviler değil, aynı hikayenin farklı kapılarıdır.",
        ], "İKİNCİ KISIM · HAFIZA VE BENLİK", art="naming-storm", caption="Duyguya ad vermek fırtınayı bitirmez, fakat kişinin onun içinde kaybolmak yerine onu görmesine yardım eder."),
        entry("Çocuklukta görünmeyen deprem", [
            "Sürekli ihmal, şiddet veya öngörülemez bakım tek bir olaydan farklıdır. Çocuk güvenliğin ne olduğunu öğrenmeden büyür; tehlike istisna değil dünyanın temel kuralı gibi yerleşebilir.",
            "Evin zemini her gün hafifçe sallanıyorsa çocuk düz yürümeyi değil dengede kalmak için sürekli kasılmayı öğrenir. Dışarıdaki sağlam zeminde bile beden eski hareketi sürdürebilir.",
            "Kitap olumsuz çocukluk deneyimlerinin sağlık, bağımlılık ve ilişki sorunlarıyla bağlantısını vurgular. Bağlantı kader değildir; risk artışı bireyin geleceğini tek başına belirlemez.",
            "Çocuğu yalnız davranış problemi olarak cezalandırmak, davranışın koruyucu işlevini kaçırabilir. Önce güven ve düzenleme, sonra beklenti ve sorumluluk daha sağlam yol sunar.",
        ], "İKİNCİ KISIM · HAFIZA VE BENLİK", art="shaking-house", caption="Öngörülemez evde büyüyen çocuk, sağlam zemine çıktığında bile sürekli denge arayan bir beden taşıyabilir."),
        entry("Bağlanma: Başkasının sinir sistemi", [
            "Bebek kendi duygusunu tek başına düzenleyemez. Sakin ses, yüz ve dokunuş yetişkinin sinir sistemini ödünç verir. Güvenli bağ, tehlike sonrası yeniden sakinleşme yolunu öğretir.",
            "İki metronomu aynı masaya koyunca zamanla birbirine yaklaşmaları gibi, insanlar da yüz, ses ve ritimle birbirini etkiler. Buna ortak düzenleme denebilir.",
            "Bakım veren aynı zamanda tehlike kaynağıysa çocuk yaklaşma ile kaçma arasında kalır. Yakınlık istenir ve korkulur; yetişkin ilişkilerinde bu çelişki tekrar edebilir.",
            "İyileştirici ilişki kusursuz ebeveyn kopyası değildir. Sınırları olan, öngörülebilir ve kişinin seçimini koruyan bir temas yeni deneyim sağlayabilir.",
        ], "İKİNCİ KISIM · HAFIZA VE BENLİK", art="shared-rhythm", caption="Güvenli bir yüz ve ses, alarmdaki kişinin kendi sakin ritmini yeniden bulmasına yardımcı olan dış metronomdur."),
        entry("Tanı etiketi ile hayat hikayesi", [
            "Depresyon, dikkat sorunu, bağımlılık veya kişilik etiketi belirtileri düzenleyebilir. Fakat tek kişinin birden çok tanı alması, alttaki travma örüntüsünün parçalar halinde görülmesine yol açabilir.",
            "Duman, ısı ve öksürüğü üç ayrı arıza sayarken odadaki yangını kaçırmak gibi, belirti listesi bazen ortak kaynağı perdeleyebilir. Tersine her sorunu travmaya bağlamak da başka hastalıkları kaçırır.",
            "Van der Kolk gelişimsel travma için daha bütünlüklü tanı tartışır. Bu öneri alanda kabul görmüş tek son söz değildir; tanı sistemleri yararları ve sınırlarıyla değişmeye devam eder.",
            "En dengeli yaklaşım hem belirtiyi ciddiye alır hem yaşam öyküsünü sorar. Etiket kapıyı açabilir, insanın tamamı değildir.",
        ], "ÜÇÜNCÜ KISIM · İYİLEŞMENİN KAPILARI", art="labels-and-story", caption="Tanı etiketleri belirtileri düzenler, fakat insanın yaşam hikayesindeki ortak yangını tek başına anlatmayabilir."),
        entry("Güvenli ilişki tedavinin zemini", [
            "Travma çoğu zaman güven ihlali içerdiği için yardım ilişkisi yalnız teknik taşımaz. Kişinin sözüne inanılması, sınırlarına saygı duyulması ve ne olacağının açıklanması tedavinin kendisidir.",
            "Kırılmış bir köprüden karşıya geçecek kişiye 'korkma' demek yetmez. Tahtaların tek tek sağlam olduğunu görmesi ve geri dönme hakkı bulunması gerekir.",
            "Terapist her şeyi bilen kurtarıcı olduğunda eski güçsüzlük tekrarlanabilir. İşbirliği, seçenek ve izin, kontrol duygusunu kişiye geri verir.",
            "Kitabın umutlu mesajı ilişkiseldir: İnsan başka insanlar içinde yaralanabilir, başka güvenli ilişkiler içinde yeniden bağlantı da kurabilir.",
        ], "ÜÇÜNCÜ KISIM · İYİLEŞMENİN KAPILARI", art="repairing-bridge", caption="Güven, korkma emriyle değil sınırların, seçeneklerin ve sağlam tahtaların birlikte sınanmasıyla yeniden kurulur."),
        entry("Travmayı anlatmak ne zaman işe yarar?", [
            "Ayrıntılı anlatım bazı kişilerde anıyı düzenlemeye yardım eder, bazılarında ise hazırlık olmadan alarmı taşırır. Önce güvenlik ve duygu düzenleme becerileri gerekebilir.",
            "Yüzme bilmeyen birini korkusunu aşsın diye derin suya atmak öğretim değildir. Havuz kenarında nefes, sığ su ve geri çıkma yolu gerekir.",
            "Kanıta dayalı travma odaklı terapiler, kaçınılan anı ve anlamlarla yapılandırılmış biçimde çalışabilir. Süreç kişinin temposu ve uzman değerlendirmesiyle yürütülmelidir.",
            "İyileşme susmak ile her ayrıntıyı tekrar etmek arasındaki zorunlu seçim değildir. Ne kadar, ne zaman ve kiminle anlatılacağı kişinin sahipliğinin parçasıdır.",
        ], "ÜÇÜNCÜ KISIM · İYİLEŞMENİN KAPILARI", art="shallow-water", caption="Travma anlatısı derin suya atlamak değil, güvenli çıkış ve düzenleme becerileriyle adım adım yüzmeyi öğrenmektir."),
        entry("EMDR ve hareket eden dikkat", [
            "EMDR, travmatik anı üzerinde çalışırken iki taraflı göz hareketleri veya başka uyarımlar kullanır. Kitap bu yöntemin bazı hastalarda anının yükünü azaltabildiğini anlatır.",
            "Sanki donmuş dosya açılırken kişi bir ayağını bugünün odasında tutar. Ama yöntemin nasıl çalıştığına dair açıklamalar tartışmalıdır; göz hareketinin özel katkısı ile yapılandırılmış maruz kalma ve dikkat süreçleri ayrıştırılmaya çalışılır.",
            "Bir tedavinin yararlı bulunması, onun hakkındaki her teorinin doğru olduğu anlamına gelmez. Araştırma sonuçları, uygulayıcı eğitimi ve kişinin uygunluğu birlikte önemlidir.",
            "Rehber burada reçete vermez. Travma tedavisinde uzmanlaşmış lisanslı profesyonelle seçenekleri konuşmak, internetten tekniği kendi kendine yoğun biçimde denemekten daha güvenlidir.",
        ], "ÜÇÜNCÜ KISIM · İYİLEŞMENİN KAPILARI", art="moving-attention", caption="EMDR anı çalışırken dikkatin bir bölümünü bugünde tutar; yararı araştırılırken mekanizması tartışılmaya devam eder."),
        entry("Yoga ve bedene geri dönmek", [
            "Kitap yoga, nefes ve yavaş hareketin beden duyularıyla güvenli temas kurmaya yardım edebileceğini savunur. Amaç performans veya esneklik değil, 'bu beden bana ait ve onu durdurabilirim' hissidir.",
            "Uzun süre başkasının kullandığı bir eve geri dönmek gibi, kişi önce odaları kısa süre gezer. Hangi hareketin iyi geldiğini, hangisinin alarmı yükselttiğini fark eder.",
            "Bedensel çalışmalar herkes için aynı değildir. Kapalı göz, belirli poz veya dokunma bazı kişileri tetikleyebilir. Travma duyarlı uygulama seçenek sunar ve hayır cevabını korur.",
            "Bu yöntemler temel tedavinin yerine otomatik geçmez. Kanıt gücü yöntemden yönteme değişir; kişinin tıbbi durumu ve tercihi hesaba katılmalıdır.",
        ], "ÜÇÜNCÜ KISIM · İYİLEŞMENİN KAPILARI", art="returning-home", caption="Yavaş hareket kişinin bedenini yeniden sahip olduğu bir ev gibi, seçim ve sınırlarla tanımasına yardım edebilir."),
        entry("Tiyatroda yeni bir son denemek", [
            "Van der Kolk psikodrama ve tiyatronun bedeni, sesi ve ilişkiyi aynı anda devreye sokmasını önemser. Kişi yalnız geçmişi anlatmaz; sahnede yeni sınır ve tepki biçimlerini deneyebilir.",
            "Hayatta donup kalan cümlenin provada tamamlandığını düşünün: 'Dur', 'yaklaşma' veya 'yardım et'. Olay değişmez, fakat beden pasif seyirci olmaktan çıkar.",
            "Grup tanıklığı utancı azaltabilir. Başkalarının benzer tepkilerini görmek, kişinin kendini bozuk ve yalnız sanmasını zorlar.",
            "Bunun da güvenli yönetilmesi gerekir. Sahne gösteri için değil sahipliği artırmak içindir; zorla canlandırma eski güçsüzlüğü tekrar edebilir.",
        ], "DÖRDÜNCÜ KISIM · YENİDEN SAHİPLENME", art="new-ending-stage", caption="Güvenli tiyatro provası geçmişi değiştirmez, fakat bedene yarım kalan sınır ve yardım hareketini tamamlama imkanı verir."),
        entry("Nörogeri bildirim: Aynadaki beyin", [
            "Nörogeri bildirimde beyin etkinliğine ilişkin ölçüm ses veya görüntüyle kişiye geri verilir. Kişi belirli düzenleri değiştirmeyi zamanla öğrenmeye çalışır. Kitap yönteme umutla yaklaşır.",
            "Kalp hızını ekranda görmek nefesi ayarlamaya yardım edebilir; nörogeri bildirim de beynin görünmeyen durumuna ayna tutmayı amaçlar. Ancak ölçüm ile anlam arasındaki yol daha karmaşıktır.",
            "Kanıtlar bazı alanlarda umut verici olsa da yöntem standart travma tedavileri kadar kesin değildir. Protokoller, karşılaştırma grupları ve uzun dönem sonuçları konusunda daha fazla araştırma gerekir.",
            "Yeni teknoloji etkileyici göründüğü için otomatik üstün sayılmamalıdır. Maliyet, erişim ve kanıt düzeyi açıkça konuşulmalıdır.",
        ], "DÖRDÜNCÜ KISIM · YENİDEN SAHİPLENME", art="brain-mirror", caption="Nörogeri bildirim görünmeyen beyin düzenine ayna tutmayı amaçlar, ancak vaat ile kanıt arasındaki mesafe dikkatle izlenmelidir."),
        entry("İç aile sistemleri ve parçalar", [
            "Kitap, insanın içinde farklı görevler üstlenen parçalar varmış gibi çalışmayı anlatır. Öfkeli parça sınırı korur, uyuşan parça acıyı kısar, eleştiren parça reddedilmeden önce hazırlık yapar.",
            "Bir şirketin kriz anında kurulmuş bölümleri barışta da yönetimi bırakmıyorsa işleyiş bozulur. Bölümleri kovmak yerine hangi felaketten koruduklarını anlamak yeni görevler buldurabilir.",
            "Bu dil herkese uymak zorunda değildir ve kelimesi kelimesine ayrı kişilikler demek değildir. Deneyimi düzenleyen terapötik bir benzetmedir.",
            "En değerli yönü iç savaşı azaltmasıdır. 'Neden kendimi sabote ediyorum?' yerine 'Bu tepki beni eskiden neden korudu?' sorusu merhamet ve sorumluluğu bir araya getirir.",
        ], "DÖRDÜNCÜ KISIM · YENİDEN SAHİPLENME", art="inner-team", caption="İç parçaları düşman değil eski kriz görevlerini sürdüren bir ekip gibi görmek, yeni iş bölümü kurmaya yardım edebilir."),
        entry("Toplumun tuttuğu kayıt", [
            "Travma yalnız terapi odasının konusu değildir. Savaş, yoksulluk, ayrımcılık, aile şiddeti ve güvensiz okul düzeni alarmı tekrar üretir. Kişiyi tedavi edip tehlikeli koşula geri göndermek eksik kalır.",
            "Sürekli su alan bodrumda yalnız pası boyamak gibi, belirtiyi azaltırken sızıntıyı görmezden gelemeyiz. Barınma, hukuk, eğitim ve sosyal destek sinir sisteminin çevresidir.",
            "Çocukların davranışını yalnız cezayla yönetmek yerine güvenli yetişkin, hareket alanı ve öngörülebilir rutin sunmak koruyucu olabilir.",
            "Kitap bireysel acının toplumsal bedelini görünür kılar. Önleme, en etkili ama en az dramatik travma tedavisidir.",
        ], "DÖRDÜNCÜ KISIM · YENİDEN SAHİPLENME"),
        entry("Kitabın güçlü ve tartışmalı yanı", [
            "Kitap travmayı beden, ilişki ve toplumla birlikte düşünerek milyonlarca okura kendini anlama dili verdi. Vaka öyküleri soyut bilgiyi canlı hale getirir.",
            "Bununla birlikte bazı tedavilere duyduğu heyecan, kanıt gücünü olduğundan kesin gösterebilir. Nörobilim görüntüleri karmaşık deneyime kolay açıklama hissi verebilir; tek tarama bir kişinin hikayesini teşhis etmez.",
            "Eleştirel okuma kitabın ana içgörüsünü atmak değildir. Umudu koruyup yöntemleri güncel klinik rehberler ve kişisel değerlendirmeyle tartmak daha güvenlidir.",
        ], "SON DURAKLAR"),
        entry("Travma her şeyi açıklamaz", [
            "Uyku sorunu, öfke, dikkat dağınıklığı veya bedensel ağrı birçok nedenden doğabilir. Travma olasılığını sormak değerlidir; her belirtiyi gizli travmanın kanıtı saymak tıbbi sorunları ve bugünkü koşulları kaçırabilir.",
            "Aynı olay iki kişide farklı iz bırakabilir. Genetik, yaş, destek, olayın süresi ve sonrasındaki güvenlik sonucu etkiler. Dayanıklılık acının yokluğu değil, destekle yeniden düzen kurabilme kapasitesidir.",
            "İyi değerlendirme hem hikayeyi dinler hem alternatif açıklamaları araştırır. Tek anahtar bütün kapıları açmaz.",
        ], "SON DURAKLAR"),
        entry("Yakınına nasıl eşlik edilir?", [
            "Kişiyi ayrıntı anlatmaya zorlamayın. 'İstersen dinlerim' demek, 'unut artık' veya 'neden kaçmadın?' cümlelerinden daha güvenlidir. Seçim hakkını küçük konularda bile geri vermek önemlidir.",
            "Sakinleşmesi için emir vermek yerine birlikte yavaşlamak, ayakların zemini hissetmesini önermek veya odadaki nesneleri saymak bazı kişilerde bugüne dönüşü destekleyebilir. Önce neyin iyi geldiğini sorun.",
            "Destek verenin de sınırı vardır. Tek başına terapist olmaya çalışmak yerine profesyonel yardım ve kendi bakımını düşünmek ilişkiyi korur.",
        ], "SON DURAKLAR"),
        entry("Bir cümlede kitabın özü", [
            "Travma geçmişte bitmiş olayın beden ve ilişkide sürmesi olabilir; iyileşme ise güvenlik, tanıklık ve seçim duygusuyla kişinin kendi bedenine ve zamanına yeniden yerleşmesidir.",
            "Akılda kalacak görüntü bozuk alarmdır. Ama alarm düşman değildir; bir zamanlar hayatı koruyan sistemin şimdi yeni koşullara göre nazikçe ayarlanması gerekir.",
        ], "SON DURAKLAR"),
    ]))


BOOKS.append(base(38, "Dil İçgüdüsü", "Steven Pinker",
    "Çocuğun birkaç yıl içinde kurallı konuşmayı nasıl başardığını, sözcüklerden cümleye ve beyinden evrime uzanan büyük bir savla açıklayan; dilin doğuştan gelen kapasite ile toplumsal öğrenmenin buluşması olduğunu tartışan rehber.",
    "#4B6476", "The Language Instinct",
    [
        {"id": 1, "title": "Steven Pinker - The Language Instinct resmi tanıtımı", "url": "https://stevenpinker.com/publications/books"},
        {"id": 2, "title": "MIT Press - Dil edinimi ve evrensel dilbilgisi tartışmaları", "url": "https://mitpress.mit.edu/9780262539747/learnability-and-cognition/"},
        {"id": 3, "title": "Max Planck Institute - Dil çeşitliliği araştırmaları", "url": "https://www.mpi.nl/research/research-databases"},
        {"id": 4, "title": "Royal Society - Dil evrimi üzerine araştırma çerçevesi", "url": "https://royalsocietypublishing.org/doi/10.1098/rstb.2014.0099"},
    ], [
        entry("Bu kitap nasıl okunmalı?", [
            "Pinker 'içgüdü' derken bebeğin hazır cümlelerle doğduğunu söylemez. İnsan beyninin dil öğrenmeye özel biçimde yatkın olduğunu, çevredeki konuşmanın bu kapasiteyi belirli bir dile dönüştürdüğünü savunur.",
            "Kitap güçlü bir görüş sunar; dilbilimde oybirliği yoktur. Doğuştan ne kadar yapı geldiği, genel öğrenme mekanizmalarının payı ve kültürel çeşitliliğin kapsamı bugün de tartışılır.",
            "Rehber savı slogan olarak değil, kanıtları ve itirazlarıyla izleyecek. Çocuk hataları, işaret dilleri, beyin hasarı, sözdizimi ve evrim aynı masaya gelecek.",
        ], "BAŞLANGIÇ"),
        entry("Üç yaşındaki dil ustası", [
            "Üç yaşındaki çocuk dilbilgisi dersi almadan daha önce duymadığı cümleler kurar. Yalnız ezberlediği kalıpları tekrarlamaz; sözcükleri yeni sırada birleştirir ve başkasının niyetini anlatır.",
            "Bir yapbozun resmini hiç görmeden yüzlerce parçayı doğru ailelere ayırmak gibi, çocuk konuşma akışından sesleri, sözcükleri ve kuralları çıkarır. Üstelik yetişkinler çoğu hatayı sistemli biçimde düzeltmez.",
            "Pinker için bu hız, beynin dil için hazırlanmış beklentileri olduğuna işarettir. Çevre malzemeyi verir; çocuk zihni malzemeyi rastgele değil belirli yollarla düzenler.",
            "Karşı görüşler ise güçlü örüntü öğrenmenin, ortak dikkatin ve sosyal etkileşimin bu başarıyı açıklamada daha büyük payı olabileceğini söyler. Mucize tek kelimeyle çözülmüş değildir.",
        ], "BİRİNCİ KISIM · ÇOCUĞUN MUCİZESİ", art="talking-child", caption="Çocuk duyduğu cümleleri kopyalamakla kalmaz; sınırlı örnekten daha önce söylenmemiş düzenli cümleler üretir."),
        entry("Bir cümlede sonsuz imkan", [
            "Dil, sınırlı sayıda sözcük ve kuraldan sınırsız sayıda cümle kurabilir. 'Kedi uyudu' içine 'komşunun gördüğü' gibi bir yapı eklenebilir; sonra o yapının içine yenisi yerleşebilir.",
            "Lego kutusundaki parça sayısı sınırlıdır, kurulabilecek evlerin sayısı değildir. Dilin üretkenliği de parçaların düzenli biçimde tekrar birleşebilmesinden gelir.",
            "Bu özellik iletişimi hazır mesaj listesinden ayırır. Dün olmayan olay, yarınki plan veya hiç var olmamış ejderha aynı sistemle anlatılabilir.",
            "Pinker dilin bu birleşim gücünü insan zihninin temel tasarımlarından biri sayar. Anlam, sözcük torbasından değil yapının içindeki ilişkilerden doğar.",
        ], "BİRİNCİ KISIM · ÇOCUĞUN MUCİZESİ", art="language-lego", caption="Sınırlı sözcük ve kurallar Lego parçaları gibi tekrar birleşerek sayısız yeni cümle kurabilir."),
        entry("Çocuğun sevimli hatası", [
            "Çocuk önce 'geldi' sözünü doğru kullanırken bir süre sonra 'gel-di' kuralını aşırı genelleyip düzensiz biçimi bozabilir. Bu gerileme aslında kural öğrendiğinin işaretidir.",
            "Usta çırağın hazır masayı iyi kopyaladıktan sonra kendi ölçüsüyle ilk masada hata yapması gibi, çocuk ezberden üretime geçmiştir. Yanlış, zihindeki düzenin penceresidir.",
            "Türkçede eklerin düzenli oluşu çocukların örüntüyü açık görmesini sağlar; yine de ses uyumu ve istisnalar öğrenilir. Her dil farklı yüzeyde aynı öğrenme sorusunu doğurur.",
            "Bu örnek yetişkinin sürekli düzeltmesinin ana motor olmadığını gösterir. Çocuk duyduğu veriden aktif varsayım kurar ve zamanla istisnaları yerleştirir.",
        ], "BİRİNCİ KISIM · ÇOCUĞUN MUCİZESİ", art="rule-error", caption="Çocuğun düzenli kuralı istisnaya uygulaması, ezberi kaybettiğini değil kendi dil düzenini kurduğunu gösterir."),
        entry("Sözcüklerin arasındaki görünmez ağaç", [
            "'Yaşlı adam ve kadın geldi' cümlesi, yaşlılığın yalnız adama mı ikisine mi ait olduğuna göre iki anlam taşır. Sözcük sırası aynı, zihindeki gruplaşma farklıdır.",
            "Market poşetinde ürünleri yan yana koymakla raflara kategori halinde yerleştirmek aynı değildir. Sözdizimi sözcükleri düz sıradan çıkarıp iç içe öbeklere düzenler.",
            "Dilbilimciler bu görünmez yapıyı ağaçlarla gösterir. Ağaç gerçek beyindeki çizim değildir; hangi parçanın hangisiyle bağlandığını açıklayan modeldir.",
            "Cümleyi anlamak bu nedenle sözlük açmaktan fazlasıdır. Zihin milisaniyeler içinde olası yapıları kurar, bağlama göre birini seçer ve bazen bahçe yolunda yanılır.",
        ], "İKİNCİ KISIM · DİLİN MAKİNESİ", art="syntax-tree", caption="Aynı sözcük sırası farklı görünmez öbekler kurduğunda cümlenin anlamı da değişebilir."),
        entry("Bahçe yolunda kaybolan zihin", [
            "Bazı cümleler ilk anda bizi yanlış yapıya götürür; son sözcük gelince başa dönmek zorunda kalırız. İngilizcedeki klasik örneklerde fiil sandığımız sözcük başka görev çıkar. Türkçede de noktalama veya vurgu belirsizliği benzer şaşkınlık yaratır.",
            "Yol tabelası sizi kısa sokağa sokar, köşede çıkmazı görünce haritayı yeniden okursunuz. Cümle işleme sistemi de en olası analizi önce dener; yanlışsa düzeltir.",
            "Bu hatalar anlama sürecinin pasif olmadığını gösterir. Zihin cümle tamamlanana kadar beklemez, her sözcükte tahmin kurar.",
            "Pinker bu küçük tökezlemeleri dil mimarisinin izleri olarak kullanır. Hızlı sistem çoğu zaman görünmezdir; yanılınca mekanizmasını fark ederiz.",
        ], "İKİNCİ KISIM · DİLİN MAKİNESİ", art="garden-path", caption="Cümleyi anlama sistemi en olası yola hızla girer; son sözcük çıkmazı gösterince yapıyı yeniden kurar."),
        entry("Sözlük kafamızda nasıl durur?", [
            "Zihinsel sözlük yalnız anlam listesi değildir. Bir fiilin hangi ekleri aldığı, hangi ögelerle kullanılabildiği ve ses biçimi de kaydedilir. 'Vermek' genellikle veren, verilen şey ve alan kişi arasında bir yapı açar.",
            "Tiyatrodaki rol kartı gibi, sözcük sahneye kaç oyuncu çağıracağını taşır. Sözdizimi bu rollerin cümledeki yerini düzenler.",
            "Düzenli biçimler kural yoluyla, sık düzensiz biçimler bellekten gelebilir. Pinker sözcükler ve kurallar arasında çift sistem savunur; bağlantıcı modeller daha ortak bir öğrenme mekanizması önerebilir.",
            "Tartışma yalnız dilbilgisi değildir. Zihnin sembolik kurallarla mı, örüntü ağlarıyla mı yoksa ikisinin karışımıyla mı çalıştığını sorgular.",
        ], "İKİNCİ KISIM · DİLİN MAKİNESİ", art="mental-lexicon", caption="Zihinsel sözlük sözcüğün anlamıyla birlikte sesini, eklerini ve cümlede açacağı rolleri de taşır."),
        entry("Ses akışını parçalara bölmek", [
            "Konuşma yazıdaki gibi sözcükler arasında boşluk bırakmaz. Sesler birbirine karışır, konuşan hızlanır ve bazı heceleri yutar. Yine de dinleyici akışı anlamlı parçalara böler.",
            "Bilmediğiniz dilde konuşma kesintisiz uğultu gibi gelir. Tanıdık dilde zihin olası sözcükleri, ses kurallarını ve bağlamı birlikte kullanarak görünmez aralıklar koyar.",
            "Bebekler sık birlikte gelen heceleri izleyebilir; ritim ve vurgu sınır ipucu sağlar. Dil edinimi yalnız sözcük ezberinden önce ses istatistiklerini öğrenmeyle başlar.",
            "Bu beceri güçlüdür ama yanılmaz değildir. Şarkı sözlerini yanlış duymamız, beynin belirsiz sesi tanıdık anlama doğru tamamladığını gösterir.",
        ], "İKİNCİ KISIM · DİLİN MAKİNESİ", art="speech-stream", caption="Konuşma kesintisiz bir ses nehri olsa da zihin istatistik, ritim ve anlamla içine sözcük sınırları çizer."),
        entry("İşaret dili de tam bir dildir", [
            "İşaret dilleri konuşulan dilin elle yazılmış kopyası değildir. Kendi sözcükleri, dilbilgisi ve anlatım imkanları vardır. El biçimi, konum, hareket ve yüz ifadesi anlam ayrımı yapabilir.",
            "Ses kanalı kapanınca dil kapasitesi yok olmaz; başka bir bedensel kanalda örgütlenir. Bu, dili ağızdan çıkan sese eşitleyen önyargıyı kırar.",
            "Sağır çocuk erişilebilir işaret dili ortamında doğal biçimde dil geliştirir. Dil girdisinden yoksun bırakılmak ise bilişsel ve sosyal gelişimde ağır bedeller yaratabilir.",
            "İşaret dilleri Pinker'ın insan türüne özgü dil kapasitesi savına güçlü örnek sunar, fakat aynı zamanda dilin topluluk içinde doğup değiştiğini gösterir.",
        ], "ÜÇÜNCÜ KISIM · BEYİN VE TOPLUM", art="sign-language", caption="İşaret dili sesin yedeği değil; bedenin görsel kanalında kurallı, üretken ve eksiksiz bir dildir."),
        entry("Beyinde tek bir dil kutusu yok", [
            "Beyin hasarı bazı kişilerde konuşma üretimini, bazılarında anlamayı veya sözcük bulmayı daha çok etkileyebilir. Broca ve Wernicke adları bu ayrımları anlatmada tarihsel rol oynar.",
            "Fakat modern görüntüleme dili iki küçük kutuya sığdırmaz. Ses, hareket, anlam, bellek ve dikkat geniş ağlarda birlikte çalışır. Görev ve kişiye göre dağılım değişebilir.",
            "Bir şehrin ulaşımı yalnız iki istasyondan ibaret olmadığı gibi, dil de bağlantılı bölgelerin dinamik işidir. Bir yol kapandığında bazen başka yollar kısmen görevi devralır.",
            "Kitaptaki nöroloji, döneminin güçlü kanıtıdır ama bugünkü ayrıntılar daha zengindir. Basit beyin haritaları öğretici başlangıç, kötü bir son söz olabilir.",
        ], "ÜÇÜNCÜ KISIM · BEYİN VE TOPLUM", art="language-network", caption="Dil iki beyin kutusundan değil ses, anlam, hareket ve bellek yollarının birlikte çalıştığı geniş ağdan doğar."),
        entry("Kritik dönem penceresi", [
            "Çocuklar dili erken yaşta olağanüstü kolaylıkla edinir. Ergenlik sonrası yeni dil öğrenmek mümkündür, fakat anadili düzeyinde ses ve sezgi kazanmak çoğu kişi için zorlaşır.",
            "Islak çamur şekli kolay alır; kurudukça değişim imkansız olmaz ama daha çok emek ister. Beyin gelişiminde bağlantıların esnekliği de zamanla farklılaşır.",
            "Kritik dönem kesin kapanan tek gün değildir. Dilin ses, sözdizimi ve sözcük bölümleri farklı zaman çizgilerine sahip olabilir; maruz kalma miktarı ve motivasyon önemlidir.",
            "En güçlü ders çocukların erken ve erişilebilir dile ihtiyacıdır. Bu özellikle sağır çocuklarda işaret diline zamanında erişim için hayati bir eğitim meselesidir.",
        ], "ÜÇÜNCÜ KISIM · BEYİN VE TOPLUM", art="open-window", caption="Erken çocukluk dili kolay alan açık pencere gibidir; pencere daralsa da yetişkin öğrenmesi sona ermez."),
        entry("Diller farklı, insan kapasitesi ortak", [
            "Diller sözcük sırası, ses, ek ve anlam ayrımlarında büyük çeşitlilik gösterir. Türkçe bilgiyi eklerle paketlerken başka diller ayrı sözcük veya sıra kullanabilir.",
            "Aynı evi taş, ahşap veya kerpiçle kurmak gibi, iletişim ihtiyaçları farklı malzemelerle çözülür. Ortaklık yüzey biçimlerinin aynı olması değildir.",
            "Evrensel dilbilgisi savı, olası insan dillerinin sınırlarını doğuştan gelen yapının daralttığını öne sürer. Eleştirmenler bazı evrensellerin genel biliş, iletişim ve kültürel evrimden çıkabileceğini savunur.",
            "Dünya dillerinin daha iyi belgelenmesi eski genellemeleri sınadı. Çeşitlilik, ortak kapasite fikrini yok etmez; ortaklığın nerede aranacağını daha dikkatli hale getirir.",
        ], "ÜÇÜNCÜ KISIM · BEYİN VE TOPLUM", art="many-houses", caption="İnsan dilleri farklı malzemelerle kurulan evler kadar çeşitlidir; ortaklık yüzeyden çok öğrenme ve iletişim kapasitesinde aranır."),
        entry("Dil düşünceyi hapseder mi?", [
            "Bir dilde sözcük olmaması o düşüncenin imkansız olduğu anlamına gelmez. Yeni kavramları tarif eder, ödünç alır veya yeni sözcük üretiriz. Pinker düşüncenin yalnız iç konuşma olmadığını savunur.",
            "Bebek ve hayvanlar sözcüksüz de nesne, sayı ve niyet hakkında bazı ayrımlar yapabilir. Ressam görüntü, müzisyen ses düzeniyle düşünebilir.",
            "Öte yandan dil dikkat ve belleği etkileyebilir. Renk adları veya yön sistemleri, insanların bazı ayrımları daha hızlı fark etmesini sağlayabilir. Etki ile hapishane aynı şey değildir.",
            "En dengeli sonuç şudur: Dil düşüncenin bütün sınırlarını çizmez, fakat sık kullandığımız yolları işaretleyen bir harita gibi algı ve hatırlamayı yönlendirebilir.",
        ], "ÜÇÜNCÜ KISIM · BEYİN VE TOPLUM", art="thought-map", caption="Dil düşünceyi kilitleyen hücre değil, bazı yolları belirginleştirip dikkati yönlendiren bir harita olabilir."),
        entry("Kreol dilinin doğuşu", [
            "Farklı dilleri konuşan yetişkinler zorunlu iletişimde sınırlı bir ortak sistem geliştirebilir. Çocuklar bu girdiyi ana dil olarak edinirken daha düzenli ve üretken bir kreol dili kurabilir.",
            "Yarım kalmış bir kulübeyi devralan çocukların kat, merdiven ve odalar eklemesi gibi, yeni kuşak iletişim malzemesini daha zengin yapıya dönüştürür.",
            "Pinker bu örnekleri doğuştan dil kurma kapasitesine kanıt sayar. Tarihçiler ve kreol uzmanları ise girdinin sanıldığından daha zengin, süreçlerin daha çeşitli olduğunu hatırlatır.",
            "Örnek yine de dilin topluluk içinde hızla sistemleşebildiğini gösterir. Çocuk pasif alıcı değil, ortak düzenin kurucusudur.",
        ], "DÖRDÜNCÜ KISIM · KÖKEN VE TARTIŞMA", art="creole-building", caption="Çocuk kuşağı sınırlı ortak konuşma malzemesini daha düzenli ve üretken bir dil yapısına dönüştürebilir."),
        entry("Dil nasıl evrilmiş olabilir?", [
            "Pinker dili doğal seçilimle şekillenmiş bir uyum olarak görür. Karmaşık sosyal bilgiyi paylaşan atalar plan, akrabalık ve tehlike hakkında avantaj kazanmış olabilir.",
            "Gözün evriminde olduğu gibi dilin de tek sıçramayla doğması gerekmez. Ses denetimi, ortak dikkat, sembol kullanımı ve birleşim kapasitesi farklı aşamalarda güçlenebilir.",
            "Fosilleşmeyen davranışın tarihini kanıtlamak zordur. Genler, beyin karşılaştırmaları, primat iletişimi ve arkeoloji parçalı ipuçları sunar; kesin senaryo yoktur.",
            "Dilin yalnız seçilim ürünü mü, daha genel beyin büyümesinin yan etkisi mi olduğu tartışılır. Muhtemel tarih birden çok kapasitenin karşılıklı güçlenmesini içerir.",
        ], "DÖRDÜNCÜ KISIM · KÖKEN VE TARTIŞMA", art="language-evolution", caption="Dil tek anda beliren armağan değil; ses, ortak dikkat ve sembol becerilerinin uzun evrimsel birleşimi olabilir."),
        entry("Hayvanlar neden konuşmuyor?", [
            "Arılar yön dansı yapar, kuşlar şarkı öğrenir, primatlar alarm çağrıları kullanır. Bu sistemler karmaşıktır, fakat insan dilindeki sınırsız birleşim ve uzak anlam çeşitliliğiyle aynı değildir.",
            "Bir trafik lambası güçlü bilgi verir ama roman yazmaz. Az sayıda işaretin belirli durumlara bağlanması ile işaretleri iç içe geçirerek yeni önerme kurmak farklı kapasitelerdir.",
            "Maymunlara işaret öğretme çalışmaları niyet ve sembol kullanımını gösterse de insan çocuğunun kendiliğinden gelişen dilbilgisi düzeyine ulaşıp ulaşmadıkları tartışmalıdır.",
            "Karşılaştırma hayvan iletişimini küçültmemelidir. Farkın nerede olduğunu dikkatle sormak, hem insan dilinin özgünlüğünü hem diğer türlerin gerçek becerilerini daha iyi görür.",
        ], "DÖRDÜNCÜ KISIM · KÖKEN VE TARTIŞMA", art="animal-signals", caption="Hayvan sinyalleri zengin bilgi taşıyabilir; insan dili ise sınırlı işaretleri açık uçlu yeni yapılara birleştirir."),
        entry("Dil polisi ve yaşayan dil", [
            "İnsanlar sık sık gençlerin dili bozduğundan yakınır. Oysa diller her kuşakta ses, sözcük ve anlam değiştirir. Bugünün kuralı dünün yeniliği olabilir.",
            "Resmi yazı standardı ortak iletişim için yararlıdır, fakat gündelik lehçeleri eksik zeka saymak yanlıştır. Her doğal lehçe karmaşık ve düzenli kurallara sahiptir.",
            "Bir kişinin 'yanlış' biçimi topluluğunda tutarlıysa dilbilimci önce o kuralı anlamaya çalışır. Sosyal prestij, dilsel karmaşıklıkla aynı şey değildir.",
            "Pinker'ın esprili itirazı dil bilgisini ezberlenen görgü kurallarından ayırır. Yine de bağlama uygun standart yazı öğrenmek kişinin kamusal imkanlarını artırabilir; betimleme ile eğitim düşman değildir.",
        ], "DÖRDÜNCÜ KISIM · KÖKEN VE TARTIŞMA", art="living-language", caption="Yaşayan dil müze vitrini değil; topluluk içinde kurallı biçimde değişen, yeni dallar veren bir ağaçtır."),
        entry("Kitabın büyük iddiası nerede zorlanıyor?", [
            "Pinker dilin doğuştan gelen özel bir modül olduğunu güçlü biçimde savunur. Kullanım temelli yaklaşımlar çocukların örüntü, benzetme, ortak niyet ve genel öğrenme becerileriyle daha fazlasını açıklayabileceğini söyler.",
            "Dillerdeki çeşitlilik bazı katı evrensel iddiaları zorlamıştır. Beyin araştırmaları da tek, yalıtılmış dil organından çok başka bilişsel ağlarla iç içe sistemler gösterir.",
            "Buna rağmen insan çocuğunun dil edinmeye olağanüstü hazırlanmış olduğu geniş ölçüde açıktır. Tartışma hazırlığın varlığından çok biçimi ve ne kadar dil-özel olduğundadır.",
        ], "SON DURAKLAR"),
        entry("Yapay zeka dil biliyor mu?", [
            "Büyük dil modelleri dev metinlerden güçlü örüntüler öğrenip yeni cümleler kurabilir. Bu başarı, istatistiksel öğrenmenin kapasitesini Pinker döneminde hayal edilenden daha görünür hale getirdi.",
            "Fakat akıcı cümle dünyada yaşamak, beden taşımak ve insan niyetine sahip olmakla aynı değildir. Modelin başarısı doğuştanlık tartışmasını tek başına bitirmez; eğitim verisi ve mimari de hazır yapıdır.",
            "Yeni soru artık yalnız 'kural mı örüntü mü?' değildir. Farklı mimariler hangi veriyle neyi öğreniyor ve insan çocuğunun az veri, ortak dikkat ve beden deneyimiyle yaptığına ne kadar benziyor?",
        ], "SON DURAKLAR"),
        entry("Çocuğa dil için ne gerekir?", [
            "Çocuğun kusursuz dil dersi değil, bol ve karşılıklı iletişim ihtiyacı vardır. Ona konuşmak kadar verdiği işarete yanıt vermek, ortak nesneye bakmak, oyun ve hikaye kurmak önemlidir.",
            "Ekrandan akan çok sözcük, canlı kişinin sırayla konuşmasıyla aynı değildir. Dil sosyal bir alışverişte anlam kazanır.",
            "Hata düzeltmek yerine cümleyi doğal biçimde genişletmek daha sıcak yol olabilir. Çocuk 'kedi git' dediğinde 'evet, kedi bahçeye gitti' cevabı hem anlamı hem modeli korur.",
        ], "SON DURAKLAR"),
        entry("Bir cümlede kitabın özü", [
            "İnsan çocuğu dili boş bir kaset gibi kopyalamaz; doğuştan gelen öğrenme yatkınlığı, toplumsal etkileşim ve belirli dilin örnekleri birleşerek sınırsız cümle kuran bir sistem yaratır.",
            "Akılda kalacak görüntü Lego kutusudur: Parçalar çevreden gelir, fakat onları açık uçlu yapılara birleştirme gücü çocuğun zihninde çalışır.",
        ], "SON DURAKLAR"),
    ]))


BOOKS.append(base(61, "Kendime Düşünceler", "Marcus Aurelius",
    "Dünyanın en güçlü insanlarından birinin başkasına ders vermek için değil, öfke, korku, görev, kayıp ve gösteriş karşısında kendi karakterini düzeltmek için tuttuğu özel notları günlük hayatın içine taşıyan sade rehber.",
    "#776044", "Meditations",
    [
        {"id": 1, "title": "Library of Congress - Meditations kamusal alan nüshası", "url": "https://www.loc.gov/item/27007869/"},
        {"id": 2, "title": "Perseus Digital Library - Marcus Aurelius metni", "url": "https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:2008.01.0641"},
        {"id": 3, "title": "Stanford Encyclopedia of Philosophy - Stoacılık", "url": "https://plato.stanford.edu/entries/stoicism/"},
        {"id": 4, "title": "Internet Encyclopedia of Philosophy - Marcus Aurelius", "url": "https://iep.utm.edu/marcus-aurelius/"},
    ], [
        entry("Bu kitap nasıl okunmalı?", [
            "Kendime Düşünceler düzenli bir ders kitabı değildir. Marcus aynı düşünceye tekrar döner, çünkü notları yayımlamak için değil kendi zihnini eğitmek için yazmıştır. Tekrarlar sayfa doldurma değil günlük alıştırmadır.",
            "Stoacı olmak duygusuz taş olmak değildir. Amaç ilk duyguyu yasaklamak değil, onun ardından gelen yargıyı incelemek ve eylemi karaktere göre seçmektir.",
            "Rehber imparatoru kusursuz bilge yapmayacak. Savaşları ve iktidarının sorunları ayrı tutulacak; notların kişisel disiplini, tarihsel yönetimin otomatik savunusu değildir.",
        ], "BAŞLANGIÇ"),
        entry("İlk kitapta bir teşekkür zinciri", [
            "Marcus kitabın başında öğretmenlerinden, ailesinden ve dostlarından öğrendiği nitelikleri sayar. Dededen yumuşaklık, anneden sadelik, öğretmenden gösterişsiz çalışma gibi karakter borçlarını kaydeder.",
            "Bir başarı konuşmasında yalnız kendi adını söylemek yerine görünmez ekibi sahneye çağırır. İmparator bile kendini tek başına yapmış değildir.",
            "Bu bölüm soyut erdem listesini canlı insanlara bağlar. Sabır bir kelime değil, belirli bir kişinin zor anda yaptığı hareket olarak hatırlanır.",
            "Gündelik uygulama basittir: Sizi etkileyen üç kişinin adını ve onlardan gördüğünüz bir davranışı yazın. Şükran geçmişi süslemek değil, bugünkü yönü seçmektir.",
        ], "BİRİNCİ KISIM · ZİHNİN EŞİĞİ", art="gratitude-chain", caption="Marcus karakterini kendi eseri saymak yerine, öğrendiği erdemleri görünmez öğretmenler zincirine bağlar."),
        entry("Sabah karşılaşacağın zor insanlar", [
            "Marcus güne başlarken nankör, kibirli, hileci veya huysuz insanlarla karşılaşacağını kendine hatırlatır. Bu karamsarlık değil, sürpriz öfkesini azaltan hazırlıktır.",
            "Yağmur beklediğiniz gün şemsiye alırsınız; buluta kişisel hakaret saymazsınız. İnsanların eksik davranışını da dünyanın beklenebilir parçası görmek tepkinin ateşini kısar.",
            "Hazırlık kötülüğe boyun eğmek değildir. Haksızlığı durdurabilir, sınır koyabilir ve yine de nefretin kendi karakterinizi yönetmesine izin vermeyebilirsiniz.",
            "Marcus ortak akıl taşıyan canlılar olduğumuzu söyler. Yanlış yapan kişi akrabadır; davranışı engellenebilir, insanlığı silinmez.",
        ], "BİRİNCİ KISIM · ZİHNİN EŞİĞİ", art="morning-people", caption="Zor insanları önceden beklemek, karşılaşmayı kişisel sürpriz olmaktan çıkarıp daha sakin bir yanıt alanı açar."),
        entry("Olay ile yargı arasındaki boşluk", [
            "Stoacıların temel ayrımı şudur: Bizi yalnız olay değil, olay hakkında verdiğimiz hüküm sarsar. Yağmur dışarıdadır; 'bütün günüm mahvoldu' cümlesi zihnin ekidir.",
            "Kargodan gelen kırık fincan gerçek bir kayıptır. 'Bana hiçbir iş düzgün gitmez' dediğinizde tek fincanı bütün hayatın kanıtına çevirirsiniz.",
            "Bu ayrım acıyı hayal saymaz. Beden hastalanır, sevilen kişi ölür ve adaletsizlik zarar verir. Yalnız olgunun üstüne eklenen felaket hikayesini incelemeye çağırır.",
            "Küçük alıştırma: Olanı kamera cümlesiyle yazın, sonra yorumunuzu ayrı satıra koyun. İkisi arasındaki boşluk seçim alanıdır.",
        ], "BİRİNCİ KISIM · ZİHNİN EŞİĞİ", art="event-and-judgment", caption="Olay ile ona eklediğimiz hükmü iki ayrı satıra yazmak, tepki içinde küçük bir seçim boşluğu açar."),
        entry("Kontrolünde olan tek kale", [
            "Marcus başkasının sözüne, havaya, ününe veya ölüm zamanına hükmedemez. Kendi niyeti, değerlendirmesi ve bugünkü eylemi üzerinde ise çalışma payı vardır.",
            "Fırtınadaki kaptan denizi durduramaz; yelkeni, rotayı ve mürettebatın düzenini yönetir. Enerjiyi denize bağırmaya harcamak tekneyi savunmasız bırakır.",
            "Kontrol ayrımı tam ikili değildir. Sağlık ve iş sonucu kısmen etkilenebilir ama garanti edilemez. Çağdaş uygulamada 'kontrolümde, etkileyebilirim, dışımda' diye üç halka düşünmek daha gerçekçidir.",
            "Stoacı sakinlik ilgisizlik değil, çabayı doğru yere yatırmaktır. Sonucu istemek serbesttir; karakterinizi sonucun rehinesi yapmak zorunlu değildir.",
        ], "BİRİNCİ KISIM · ZİHNİN EŞİĞİ", art="ship-in-storm", caption="Kaptan denizi yönetemez; yelken, rota ve kendi davranışı üzerinde çalışarak fırtınada yön tutar."),
        entry("Şimdiki anın küçük ülkesi", [
            "Geçmiş artık eylem alanında değildir, gelecek henüz gelmemiştir. Marcus insanın gerçekte yalnız şimdiki anı kaybettiğini söyler; ömrün tamamını aynı anda taşımaz.",
            "Bir masada tek tabak yiyebilirsiniz. Dün ve yarının bütün tabaklarını üst üste koyarsanız bugünkü lokma da yenmez hale gelir.",
            "Bu söz gelecek planını bırakmak değildir. Plan şimdide yapılan eylemdir; endişe ise henüz var olmayan sahneleri tekrar tekrar yaşamaktır.",
            "Zihin dağıldığında 'Şu anda yapılabilecek en doğru küçük iş nedir?' sorusu Marcus'un notlarını gündelik araca çevirir.",
        ], "İKİNCİ KISIM · GÖREV VE TOPLUM", art="single-plate", caption="İnsan dün ve yarının bütün tabaklarını aynı anda yiyemez; eylem yalnız şimdiki küçük lokmada mümkündür."),
        entry("İşin insan doğasıyla bağı", [
            "Sabah yataktan kalkmak istemediğinde Marcus kendine insan işi yapmak için doğduğunu söyler. Arı bal yapar, insan da akıl ve işbirliğiyle ortak yaşama katkıda bulunur.",
            "Bu cümle modern verimlilik patronunun sloganı değildir. Görev yalnız ücretli iş değil; çocuğa bakmak, adil karar vermek ve komşuya yardım etmek gibi toplumsal işlevdir.",
            "Dinlenme de doğanın parçasıdır. Marcus tembelliği eleştirirken bedeni yok saymayı savunmaz; kendisi hastalıklarla uğraşmıştır. Ölçü, hazdan kaçmak değil görevin önünü kapatmamasıdır.",
            "Soru 'bugün kaç iş bitirdim?' değil, 'bugün insanlara ve karakterime uygun ne yaptım?' olabilir.",
        ], "İKİNCİ KISIM · GÖREV VE TOPLUM", art="human-work", caption="Marcus için insan işi yalnız üretmek değil, akıl ve işbirliğiyle ortak yaşamın payına düşeni yapmaktır."),
        entry("Kovan iyi değilse arı da iyi değildir", [
            "Marcus bireyi toplumdan ayırmaz. Kovana zarar veren şey arıya da zarar verir der. Kişisel erdem, ortak iyiliğe kör bir iç huzur tekniği değildir.",
            "Bir apartmanda herkes kendi dairesini parlatıp merdivenin çökmesine aldırmazsa kimse güvende kalmaz. Ortak altyapı bireysel rahatlığın koşuludur.",
            "Bu düşünce yurttaşlık ve adalet sorumluluğu taşır. Başkasına zarar veren bir düzen karşısında yalnız 'kontrolümde değil' demek Stoacı görevi eksiltir; elinizdeki etkili ve doğru eylemi aramak gerekir.",
            "Marcus'un imparator oluşu burada zor soru doğurur: Notlardaki ortaklık ideali, yönetimde ne kadar gerçekleşti? Metni tarihsel eleştiriyle birlikte okumak gerekir.",
        ], "İKİNCİ KISIM · GÖREV VE TOPLUM", art="bee-and-hive", caption="Kendi hücresini koruyan arı kovanın çöküşünden kaçamaz; kişisel iyilik ortak yapıyla bağlıdır."),
        entry("Öfkeyi küçülten altı bakış", [
            "Marcus öfke geldiğinde insanın bilgisizliğini, hayatın kısalığını, kendi hatalarını ve öfkenin verdiği zararı hatırlatır. Karşı tarafın bütünü değil tek eylemi yanlıştır.",
            "Sürücü önünüze kırdığında onu bütün hayatı kötü biri ilan etmek kolaydır. Belki dikkatsizdir, belki acil durumdadır; neden ne olursa olsun sizin güvenli freniniz hakaretten daha yararlıdır.",
            "Öfke adaletsizliği fark ettiren sinyal olabilir. Stoacı alıştırma sinyali söndürmez, direksiyonu ona bırakmaz. Kararlı tepki ile intikam aynı şey değildir.",
            "En sert cezanın yanlış yapan kişiye benzememek olduğunu söyler. Başkasının kabalığı sizin karakteriniz için emir değildir.",
        ], "İKİNCİ KISIM · GÖREV VE TOPLUM", art="anger-lens", caption="Öfkeyi farklı açılardan görmek haksızlığı silmez; direksiyonu intikamdan kararlı eyleme geri verir."),
        entry("Ünün kısa ömrü", [
            "Marcus hem ünlü kişinin hem onu alkışlayanların kısa süre sonra öleceğini tekrarlar. Gelecek kuşakların da kendi dertleri vardır; adınızı doğru hatırlamaları garanti değildir.",
            "Sahilde adınızı kuma yazmak için bütün günü harcadığınızı düşünün. Dalga yazıyı silecektir; bu, güzel yazmamanız değil hayatınızı yalnız yazının kalıcılığına bağlamamanız gerektiğini söyler.",
            "Ün arzusu davranışı görünmeyen seyirciye teslim eder. Doğru işi, alkış olmadığı gün de doğru olduğu için yapmak daha sağlam ölçüdür.",
            "Modern beğeni sayıları bu notu güncel kılar. Görünürlük işe yarayabilir, fakat özdeğerin göstergesi olduğunda her sessizlik düşüş gibi yaşanır.",
        ], "ÜÇÜNCÜ KISIM · GEÇİCİLİK", art="name-in-sand", caption="Kumdaki isim dalgayla silinir; Marcus doğru eylemi ünün ömründen bağımsız kurmaya çağırır."),
        entry("Yukarıdan bakış", [
            "Marcus kendini yüksekten dünyaya bakarken hayal eder: şehirler, ordular, doğumlar, ölümler, pazarlar ve tartışmalar aynı anda görünür. Kişisel dert daha geniş ölçekte yerini bulur.",
            "Uçaktan bakınca trafikte sizi öfkelendiren araç küçük bir nokta olur. Sorun yok olmaz, fakat bütün evreni kaplamadığı anlaşılır.",
            "Bu alıştırma acıyı küçümsemek için kullanılmamalıdır. Yas tutan kişiye 'evrende küçüksün' demek merhametsizdir. Bakış, kişinin kendi zihninde ölçüyü geri kazanma aracıdır.",
            "Kozmik ölçek kibri de utancı da yumuşatabilir. Hepimiz aynı kısa hareketin içindeyiz.",
        ], "ÜÇÜNCÜ KISIM · GEÇİCİLİK", art="view-from-above", caption="Yukarıdan bakış kişisel sorunu yok etmez, fakat onu bütün dünyayı kaplayan tek gerçek olmaktan çıkarır."),
        entry("Değişimden korkmayan doğa", [
            "Yiyecek bedene, odun ateşe, çocuk yetişkine dönüşür. Marcus evreni durmadan biçim değiştiren madde olarak görür. Değişim doğanın düşmanı değil çalışma biçimidir.",
            "Sonbaharda yaprağı kayıp sayan ağaç gibi yaşasaydık her mevsim felaket olurdu. Dönüşüm, yeni biçimin koşuludur.",
            "Bu düşünce ölüm korkusuna uygulanır. Ölüm yaşama eklenen yabancı skandal değil, doğum kadar doğanın sürecidir. Yine de sevilenin kaybında yasın gerçekliği sürer.",
            "Stoacı kabul, değişimi sevmek zorunda olmak değildir. Kaçınılmaz olanla sürekli kavga etmek yerine kalan doğru eylemi seçmektir.",
        ], "ÜÇÜNCÜ KISIM · GEÇİCİLİK", art="changing-leaf", caption="Doğa yaprağı, bedeni ve mevsimi durmadan dönüştürür; değişim yaşamın arızası değil çalışma biçimidir."),
        entry("Ölüm provası değil yaşam ölçüsü", [
            "Marcus sık sık ölümün yakın olabileceğini hatırlar. Bu karanlık saplantıdan çok ertelemeyi kesen ölçüdür. Bugün son gün olsaydı küçük intikam ve gösteriş ne kadar değer taşırdı?",
            "Telefonun pilinin sınırlı olduğunu bilmek hangi uygulamayı açık tutacağınıza karar verdirir. Ömrün sınırlılığı da dikkati seçmeye zorlar.",
            "Memento mori geleceği iptal etmez; anlamsız ertelemeyi sorgular. Sevdiğiniz kişiye söylenecek söz, yapılacak adil iş ve bırakılacak kibir bugünde mümkündür.",
            "Ölüm düşüncesi yoğun kaygı yaratıyorsa alıştırmayı zorlamak gerekmez. Stoacılık ruh sağlığı desteğinin yerine geçmez; araç kişiye hizmet etmelidir.",
        ], "ÜÇÜNCÜ KISIM · GEÇİCİLİK", art="finite-battery", caption="Ömrün sınırlı pilini hatırlamak dikkati gösterişten bugün yapılabilecek değerli eyleme çevirir."),
        entry("İç kale ne demek?", [
            "Marcus insanın kendi akıl ve niyetine çekilebileceği bir iç kale anlatır. Bu, dünyadan kaçılan gizli oda değil, dış olay karşısında yargıyı yeniden düzenleme kapasitesidir.",
            "Gürültülü istasyonda kulaklık takıp anonsu dinlemek gibi, kısa içe dönüş önemli sesi ayırır. Sonra perona geri dönüp yapılacak işi yaparsınız.",
            "İç kale başkalarının zararını önemsizleştirme kalkanı olursa kötü kullanılır. İstismar karşısında yalnız düşünceyi değiştir demek mağduru suçlar; güvenlik ve adalet gerekir.",
            "Sağlıklı kale kapısı olan, gerektiğinde yardım alan ve dış dünyaya geri açılan yerdir. Hapishane değildir.",
        ], "DÖRDÜNCÜ KISIM · GÜNLÜK ANTRENMAN", art="inner-citadel", caption="İç kale dünyadan kaçış değil, yargıyı toparlayıp doğru eylem için yeniden dışarı çıkılan kısa bir duraktır."),
        entry("İzlenim kapıda beklesin", [
            "Stoacılar zihne ilk gelen görüntü veya düşünceye izlenim der. Marcus 'Sen yalnız bir izlenimsin, göründüğün şey olmayabilirsin' diye onu sınamayı önerir.",
            "Kapıyı çalan herkes eve alınmaz. Kargo mu, komşu mu, dolandırıcı mı diye bakarsınız. Zihinsel kapıda da 'Kesin mi, yorum mu, şimdi eylem gerekiyor mu?' soruları bekçilik yapar.",
            "İlk izlenim otomatik olabilir: 'Beni küçümsedi.' Onay vermeden önce ses tonunu, bağlamı ve alternatif açıklamayı incelemek mümkündür.",
            "Bu kuşkuculuk sonsuz düşünme değildir. Acil tehlikede hızlı davranırız; gündelik alınmalarda bir nefeslik kontrol çoğu zaman yeterlidir.",
        ], "DÖRDÜNCÜ KISIM · GÜNLÜK ANTRENMAN", art="mind-door", caption="Zihne gelen her izlenimi hemen içeri almak yerine kimliğini ve kanıtını kapıda kontrol etmek mümkündür."),
        entry("Engel yolun kendisi", [
            "Dış engel hedefi durdurabilir, fakat adalet, sabır ve yaratıcılık gibi erdemleri kullanma fırsatını da açar. Marcus eylemin önündeki şeyin yeni eylem malzemesi olabileceğini söyler.",
            "Yol kapanınca harita işe yaramaz hale gelmez; yeni rota arama görevi doğar. Toplantı iptal olduysa hazırlığı geliştirmek, hastalık geldiyse yardım kabul etmeyi öğrenmek mümkün olabilir.",
            "Bu söz her felakette gizli hediye arama baskısına dönüşmemelidir. Bazı kayıplar yalnız kayıptır ve yas ister. Erdem, olayı iyi ilan etmek değil elde kalan yanıtı seçmektir.",
            "Engel romantikleştirilmez; kullanabileceğiniz kısmı geri alınır.",
        ], "DÖRDÜNCÜ KISIM · GÜNLÜK ANTRENMAN", art="blocked-road", caption="Kapanan yol iyi bir olay değildir; fakat yeni rota, sabır ve yardım isteme gibi eylemler için malzeme olabilir."),
        entry("Akşam kendine hesap vermek", [
            "Marcus'un notları günlük bir öz denetim biçimidir. Ne yaptım, nerede yargıya kapıldım, yarın hangi davranışı prova etmeliyim? Amaç kendini dövmek değil zihni tekrar ayarlamaktır.",
            "Sporcu video kaydını kişiliğini aşağılamak için değil hareketini düzeltmek için izler. Günlük de karakter antrenmanının kaydı olabilir.",
            "Üç satır yeter: Bugün iyi yaptığım bir şey, düzeltmek istediğim bir an, yarın deneyeceğim tek hareket. Uzun edebiyat şart değildir.",
            "Kendine karşı dürüstlük şefkatle birlikte olmalıdır. Utanç insanı saklar; sorumluluk davranışı değiştirir.",
        ], "DÖRDÜNCÜ KISIM · GÜNLÜK ANTRENMAN", art="evening-journal", caption="Akşam notu kişiliğe hüküm vermek değil, günün hareketini izleyip yarın için tek düzeltme seçmektir."),
        entry("Sade yaşamak ve gösterişi bırakmak", [
            "Marcus mor giysinin koyun yünü ve kabuk kanı, değerli yemeğin ölü hayvan parçası olduğunu hatırlatır. Nesnenin süslü hikayesini soyup maddesine bakar.",
            "Lüks otomobilin kaportasını reklam ışıklarından çıkarıp metal, plastik ve borç olarak görmek arzunun büyüsünü azaltabilir. Bu, güzelliği yasaklamak değil fiyat ile değeri ayırmaktır.",
            "Aynı yöntem ün ve makamda da çalışır. İmparatorluk unvanı sabah yorgun uyanan, hastalanan ve ölen bir insanın üstündeki etikettir.",
            "Sadelik yoksulluğu romantikleştirmek değildir. İhtiyaç ile gösterişi ayırarak bağımlılığı azaltmayı amaçlar.",
        ], "DÖRDÜNCÜ KISIM · GÜNLÜK ANTRENMAN"),
        entry("Marcus'un tarihsel gölgesi", [
            "Marcus veba, savaş ve siyasi gerilim içinde hüküm sürdü. Kişisel notlarındaki merhamet ve ortaklık, imparatorluğun şiddetli yapısını ortadan kaldırmaz.",
            "Hristiyanlara yönelik zulümde doğrudan rolünün derecesi tartışılır; yine de en güçlü yönetici olarak döneminin sorumluluğundan tamamen ayrı düşünülemez. Oğlu Commodus'un yönetimi de bilge kişinin aile ve siyaset başarısını garanti etmediğini gösterir.",
            "Metni putlaştırmadan okumak erdem fikrini güçlendirir. Güzel cümle, sahibinin her eylemini doğru yapmaz; aynı ölçüyle onu da sınar.",
        ], "SON DURAKLAR"),
        entry("Stoacılığın kötü kullanımı", [
            "'Kontrol edemiyorsan aldırma' sözü işyerindeki sömürü veya evdeki şiddet karşısında susma emrine çevrilebilir. Oysa adalet Stoacı erdemlerin merkezindedir; birlikte hareket etmek kontrol alanını büyütür.",
            "Duyguyu bastırmak da Stoacılık değildir. Bastırılan korku beden ve davranışta sürer. Hedef duyguyu fark edip kanıtını ve eylem önerisini değerlendirmektir.",
            "Stoacı araç kişiyi daha sorumlu, adil ve bağlantılı yapıyorsa işe yarar. Daha sessiz kurban veya duygusuz yönetici yapıyorsa yönü kaçırılmıştır.",
        ], "SON DURAKLAR"),
        entry("Yedi günlük küçük uygulama", [
            "Bir gün şükran zinciri, bir gün kontrol halkaları, bir gün olay-yargı ayrımı yazın. Dördüncü gün öfke anında nefeslik boşluk, beşinci gün yukarıdan bakış deneyin.",
            "Altıncı gün gösterişli bir arzuyu maddesine ayırın. Yedinci gün haftayı suçlamadan gözden geçirip tek davranış seçin. Amaç yeni kimlik satın almak değil tekrar yoluyla dikkat kası geliştirmektir.",
            "Marcus'un notları okunacak aforizma koleksiyonundan çok yapılacak zihinsel egzersizlerdir. Küçük ve düzenli uygulama büyük sözden değerlidir.",
        ], "SON DURAKLAR"),
        entry("Bir cümlede kitabın özü", [
            "Dünya, insanlar ve ölüm sizin emrinize girmeyecek; fakat onlara vereceğiniz yargı ve bugünkü doğru eylem üzerinde çalışarak karakterinizi dış olayların oyuncağı olmaktan çıkarabilirsiniz.",
            "Akılda kalacak görüntü fırtınadaki kaptandır: Denize hükmetmez, yelkeni bırakmaz ve tekneyi yalnız kendisi için değil mürettebatla birlikte kıyıya taşır.",
        ], "SON DURAKLAR"),
    ]))


if __name__ == "__main__":
    write_books(BOOKS)
