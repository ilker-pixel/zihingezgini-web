import os
import json

def create_summary():
    summary = {
        "bookNo": 3,
        "title": "Fizik Üzerine Yedi Kısa Ders",
        "author": "Carlo Rovelli",
        "subtitle": "Modern Fizik Şaheserinin Gençler İçin Eğlenceli ve Detaylı Özeti",
        "coverImage": "/images/physics_seven_lessons_cover_sketch.png",
        "meta": {
            "originalTitle": "Sette brevi lezioni di fisica",
            "compiler": "Yapay Zeka Asistanı",
            "date": "Haziran 2026",
            "language": "Türkçe"
        },
        "intro": "Carlo Rovelli'nin \"Fizik Üzerine Yedi Kısa Ders\" adlı eseri, modern fiziğin devrim niteliğindeki keşiflerini şiirsel ve son derece yalın bir dille sunan çağdaş bir başyapıttır. Bu kitapçıkta, Rovelli'nin sunduğu Genel Görelilik, Kuantum Mekaniği, Kozmoloji ve Kuantum Yerçekimi gibi ağır teorileri ortaokul düzeyindeki herkesin keyifle okuyup kavrayabileceği benzetmelerle özetledik.",
        "chapters": [
            {
                "id": "intro_text",
                "title": "GİRİŞ: Fiziğin Şiirsel Dünyası",
                "image": "/images/physics_seven_lessons_cover_sketch.png",
                "imageCaption": "Kozmos ve Fiziğin Büyüsü",
                "takeaway": "Carlo Rovelli'nin en büyük dehası, evreni sadece formüllerle değil, hislerle ve estetik kavramlarla anlatmasıdır.",
                "paragraphs": [
                    "İtalyan teorik fizikçi Carlo Rovelli'nin kaleme aldığı \"Fizik Üzerine Yedi Kısa Ders\", yirminci yüzyılın başından bu yana fizikte yaşanan büyük devrimleri en yalın ve büyüleyici şekilde anlatan modern bir başyapıttır. Rovelli, karmaşık matematiksel formüllerle dolu olan fizik teorilerini, birer şiir veya sanat eseri gibi sunarak herkesin anlamasını sağlar.",
                    "Bu özet kitapçıkta, Rovelli'nin orijinal metindeki derin felsefi ve bilimsel tezlerine tamamen sadık kalarak, evrenin en büyük sırlarını günlük hayattan eğlenceli ve anlaşılır benzetmelerle detaylandırdık. Dil seviyesi, ortaokul düzeyindeki genç meraklılardan yetişkin okurlara kadar herkesin keyifle okuyabileceği akıcılıktadır.",
                    "Kitapta yer alan yedi dersi adım adım takip ederek; Albert Einstein'ın Genel Görelilik kuramının estetik güzelliğini, Kuantum mekaniğinin gizemli mikro dünyasını, evrenin kozmik mimarisini, bizi oluşturan temel parçacıkları, uzay ve zamanın kuantum düzeyindeki taneli yapısını, kara deliklerin gizemli ısısını ve nihayetinde tüm bu tablonun içinde insanlığın nerede durduğunu keşfedeceksiniz. Şimdi, bilimin o büyüleyici dünyasına yelken açma zamanı!"
                ]
            },
            {
                "id": "chapter1",
                "title": "BÖLÜM 1: En Güzel Kuram (Albert Einstein ve Genel Görelilik)",
                "image": "/images/cosmic_trampoline_sketch.png",
                "imageCaption": "Einstein'ın Kütleçekim Trambolini",
                "takeaway": "Uzay artık nesnelerin hareket ettiği boş bir yer değil, evreni oluşturan fiziksel maddelerden biridir; bükülebilen esnek bir dokudur.",
                "paragraphs": [
                    "**Einstein'ın Gençlik Düşleri ve Dehası**\n\nAlbert Einstein, yirminci yüzyılın başlarında genç ve hayalperest bir adamdı. İsviçre'de bir patent ofisinde çalışırken, boş zamanlarında kafasını gökyüzüne ve doğanın en büyük gizemlerine yoruyordu. Newton'ın iki yüz yıldır sarsılmayan kütleçekim kuramını inceliyordu. Newton'a göre kütleçekimi, cisimlerin birbirini görünmez bir iple çekmesi gibiydi. Ancak Einstein buna inanmıyordu. Ona göre uzay ve zaman, içine nesnelerin yerleştirildiği boş ve hareketsiz bir kutu değildi. Einstein, uzay ve zamanın aslında esnek, bükülebilen ve hareket edebilen devasa bir çarşaf gibi olduğunu hayal etti. Bu hayal, insanlık tarihinin en büyük bilimsel devrimlerinden birinin, yani Genel Görelilik Kuramı'nın doğuşuna yol açtı.",
                    "**Uzay-Zaman Eğrilmesi: Kozmik Trambolin**\n\nPeki uzay ve zamanın esnek olması ne anlama gelir? Carlo Rovelli, bunu anlamamız için çok basit bir benzetme sunar: Bir trambolin düşünün. Bu trambolinin ortasına ağır bir bowling topu yerleştirelim. Bowling topunun ağırlığı nedeniyle trambolinin ortası aşağıya doğru çökecek ve bir çukur oluşturacaktır. Şimdi, bu trambolinin kenarına küçük bir bilye bırakıp onu hafifçe yuvarlayalım. Bilye düz gitmek yerine, bowling topunun oluşturduğu çukurun etrafında dönerek merkeze doğru yol alacaktır. İşte kütleçekimi tam olarak budur! Güneş (yani bowling topu), çevresindeki uzay-zaman dokusunu (trambolini) büker. Dünya (yani bilye) ise bu bükülen yolda dönmeye başlar. Kütleçekimi gizemli bir güç değil, uzay-zamanın şekil değiştirmesidir.",
                    "**Zamanın Esnemesi ve Kütleçekiminin Zamanı Bükmesi**\n\nEinstein'ın kuramının en şaşırtıcı sonuçlarından biri, zamanın her yerde aynı hızla akmamasıdır. Kütleçekimi ne kadar güçlüyse, uzay-zaman o kadar çok bükülür ve zaman o kadar yavaş akar! Örneğin, Dünya'nın merkezine daha yakın olan deniz seviyesinde kütleçekimi, yüksek bir dağın zirvesine göre biraz daha güçlüdür. Bu nedenle, deniz kenarında yaşayan birinin saati, dağda yaşayan birine göre daha yavaş çalışır. Elbette bu fark o kadar küçüklür ki günlük hayatta bunu hissedemeyiz. Ancak hassas atom saatleriyle ölçüldüğünde bu durum kanıtlanmıştır. Zaman, uzaydan bağımsız akan düz bir nehir değildir; kütleçekimi tarafından bükülebilen esnek bir örtüdür.",
                    "**Kozmik Işığın Bükülmesi ve Göreliliğin Zaferi**\n\nEinstein bu kuramı ortaya attığında birçok bilim insanı ona şüpheyle yaklaştı. Çünkü uzayın büküldüğünü gözümüzle göremiyorduk. Ancak Einstein, kuramını kanıtlamak için bir yol önerdi: Eğer uzay bükülüyorsa, yıldızlardan gelen ışık da Güneş'in yanından geçerken bu bükülmeden etkilenmeli ve eğri bir yol izlemelidir. 1919 yılında yaşanan tam Güneş tutulması sırasında, İngiliz gökbilimci Arthur Eddington liderliğindeki bir ekip, Güneş'in arkasında kalan yıldızların ışığını ölçtü. Sonuç tam Einstein'ın hesapladığı gibi çıktı: Işık, Güneş'in kütleçekim çukurundan geçerken bükülmüştü! Bu keşif, Einstein'ı bir gecede dünya çapında bir efsane haline getirdi ve Genel Görelilik kuramını fiziğin en güzel teorisi yaptı."
                ]
            },
            {
                "id": "chapter2",
                "title": "BÖLÜM 2: Kuantum (Mikro Dünyanın Gizemi)",
                "image": "/images/quantum_micro_world_sketch.png",
                "imageCaption": "Kuantum Mekaniği",
                "takeaway": "Kuantum mekaniğinde kesinliklerin yerini olasılıklar, sürekli akışların yerini kesintili kuantum sıçramaları almıştır.",
                "paragraphs": [
                    "**Max Planck ve Işığın Enerji Paketleri**\n\nFiziğin ikinci büyük devrimi, mikro dünyanın, yani atomların ve onlardan daha küçük parçacıkların dünyasını inceleyen Kuantum Mekaniği'dir. Her şey 1900 yılında Alman fizikçi Max Planck'ın garip bir keşfiyle başladı. Planck, ışığın ve enerjinin sürekli akan bir su gibi değil, kesintili küçük paketler halinde yayıldığını fark etti. Tıpkı bir sürahiden akan suyun aslında tek tek damlalardan oluşması gibi, ışık juga 'kuanta' adı verilen enerji damlacıklarından oluşuyordu. Planck bu paketlere 'kuant' adını verdi. Bu keşif, o dönemin fizik kurallarını tamamen sarsan ve doğanın en küçük yapı taşlarının sandığımızdan çok farklı davrandığını gösteren ilk işaretti.",
                    "**Einstein'ın Fotoelektrik Keşfi ve Işığın İkili Doğası**\n\nMax Planck'ın fikrini ciddiye alan ilk kişi yine Albert Einstein oldu. Einstein, ışığın sadece enerji yayarken değil, uzayda yol alırken de küçük ışık paketleri (yani fotonlar) gibi davrandığını öne sürdü. Işığın metallerden elektron sökmesi olayını (fotoelektrik etki) bu paketlerle açıkladı ve bu keşfiyle Nobel Fizik Ödülü'nü kazandı. Işık hem bir deniz dalgası gibi yayılıyor hem de fırlatılan küçük bilyeler gibi paketler halinde çarpıyordu. Bu durum, fiziğin en büyük gizemlerinden birini doğurdu: Bir şey nasıl hem dalga hem de parçacık olabilirdi?",
                    "**Niels Bohr ve Atomun Yörüngeleri**\n\nDanimarkalı fizikçi Niels Bohr, kuantum kuramını atomların yapısına uyguladı. Bohr'a göre, atomun merkezindeki çekirdeğin etrafında dönen elektronlar, Güneş etrafındaki gezegenler gibi serbestçe dolaşamazlardı. Onlar sadece belirli enerji seviyelerindeki özel yörüngelerde bulunabilirlerdi. En garip olanı ise, bir elektron bir yörüngeden diğerine geçerken, aradaki mesafeyi kat etmiyordu! Elektron, bir yörüngede yok olup, anında diğer yörüngede beliyordu. Buna 'kuantum sıçraması' denir. Elektronlar, mikro dünyada sihirbazlar gibi hareket ediyordu.",
                    "**Heisenberg'in Belirsizlik İlkesi ve Dalgaların Dansı**\n\nKuantum dünyasının en ünlü yasalarından birini genç Alman fizikçi Werner Heisenberg buldu: Belirsizlik İlkesi. Heisenberg, bir parçacığın (örneğin bir elektronun) aynı anda hem nerede olduğunu (konumunu) hem de nereye gittiğini (hızını) kesin olarak ölçmenin imkansız olduğunu kanıtladı. Eğer elektronun yerini kesin olarak görmek istersek, ona ışık göndermemiz gerekir. Gözlem yapmak için gönderdiğimiz ışık parçacığı foton, elektrona çarparak onu yerinden fırlatır ve hızını değiştirir. Dolayısıyla, kuantum dünyasında gözlem yapmak, gözlenen şeyi kaçınılmaz olarak değiştirir."
                ]
            },
            {
                "id": "chapter3",
                "title": "BÖLÜM 3: Evrenin Mimarisi (Kozmosun Düzeni)",
                "image": "/images/physics_seven_lessons_cover_sketch.png",
                "imageCaption": "Evrenin Yapısı",
                "takeaway": "Evren, sabit ve hareketsiz değildir; milyarlarca yıldır her yöne doğru büyümeye devam eden dinamik bir yapıdır.",
                "paragraphs": [
                    "**Kopernik'ten Günümüze Göklerin Haritası**\n\nİnsanlık, binlerce yıl boyunca Dünya'nın evrenin merkezinde durduğuna ve her şeyin bizim etrafımızda döndüğüne inandı. Bu çok doğaldı çünkü gökyüzüne baktığımızda Güneş'in yükselip alçaldığını görüyorduk. Ancak Polonyalı gökbilimci Mikolaj Kopernik, Güneş'i merkeze koyarak bu düzeni değiştirdi. Zamanla bilim geliştikçe, Güneş'in de özel bir yer olmadığını, Samanyolu adını verdiğimiz devasa bir yıldız şehrinin (galaksinin) kenarında sıradan bir yıldız olduğunu anladık. Bugün biliyoruz ki evren, milyarlarca galaksiden oluşan devasa bir mimariye sahiptir ve biz bu yapıda küçücük bir adanın sakinleriyiz.",
                    "**Galaksiler ve Kozmik Okyanus**\n\nUzayda yalnız değiliz derken, galaksilerden bahsediyoruz. Galaksiler, kütleçekimi sayesinde bir arada tutulan milyarlarca yıldızın, gazın ve tozun oluşturduğu devasa sistemlerdir. Bizim galaksimiz Samanyolu, spiral şeklindedir ve içinde yaklaşık 200 milyar yıldız barındırır. Güneş sistemimiz, bu devasa sarmalın kollarından birinde yer alır. Ancak Samanyolu da evrendeki tek galaksi değildir. Teleskoplarimizi uzayın en karanlık noktalarına çevirdiğimizde, her biri milyarlarca yıldız içeren yüz milyarlarca başka galaksi görürüz. Evren, galaksilerden oluşan devasa bir okyanustur.",
                    "**Genişleyen Evren ve Edwin Hubble'ın Keşfi**\n\nAmerikalı gökbilimci Edwin Hubble, 1929 yılında teleskobuyla uzak galaksileri incelerken olağanüstü bir şey keşfetti: Galaksiler bizden hızla uzaklaşıyordu! Üstelik bize en uzak olan galaksiler, en hızlı şekilde kaçıyordu. Bu keşif, evrenin sabit ve hareketsiz olmadığını, aksine sürekli genişlediğini kanıtladı. Bunu gözümüzde canlandırmak için, üzerine noktalar çizilmiş bir balonu şişirdiğimizi düşünebiliriz. Balon şiştikçe üzerindeki noktalar (yani galaksiler) birbirinden uzaklaşır.",
                    "**Kozmik Mikrodalga Arka Plan Işıması: Evrenin Bebeklik Fotoğrafı**\n\nEvrenin genişlediğini biliyorsak, zamanı geriye sardığımızda evrenin geçmişte çok daha küçük, sıcak ve yoğun olduğunu anlarız. Yaklaşık 13.8 milyar yıl önce gerçekleşen Büyük Patlama (Big Bang) ile evrenimiz doğdu. Patlamadan hemen sonra evren o kadar sıcaktı ki ışık bile serbestçe yayılamıyordu. Ancak evren soğudukça ışık serbest kaldı. İşte o ilk serbest kalan ışık, günümüzde hala uzayın her köşesinde çok zayıf bir radyo dalgası olarak yayılmaktadır. Bilim insanları buna 'kozmik mikrodalga arka plan radyasyonu' derler. Bu radyasyon, evrenin Büyük Patlama'dan hemen sonra çekilmiş ilk bebeklik fotoğrafı gibidir."
                ]
            },
            {
                "id": "chapter4",
                "title": "BÖLÜM 4: Parçacıklar (Evrenin Yapı Taşları)",
                "image": "/images/quantum_micro_world_sketch.png",
                "imageCaption": "Kozmik Parçacıklar",
                "takeaway": "Evren, boş bir uzayda duran parçacıklardan ibaret değildir; sürekli dalgalanan ve birbirleriyle etkileşen kozmik alanların dansıdır.",
                "paragraphs": [
                    "**Standart Model: Evrenin Malzeme Listesi**\n\nÇevremizdeki her şey; soluduğumuz hava, oturduğumuz sandalye, elimizdeki kitap ve kendi bedenimiz, minik yapı taşlarından oluşur. Fizikçiler, doğadaki tüm maddeleri ve kuvvetleri açıklayan devasa bir liste hazırladılar. Buna 'Standart Model' denir. Standart Model, evrenin yapım kılavuzu ve malzeme listesi gibidir. Bu modele göre evrendeki her şey, sadece birkaç çeşit temel parçacıktan oluşur. En bilinenleri, atom çekirdeğini oluşturan kuarklar ve çekirdeğin etrafında dönen elektronlardır (leptonlar). Evren, bu birkaç temel oyuncağın farklı şekillerde birleştirilmesiyle kurulmuş devasa bir Lego sarayıdır.",
                    "**Kuvvet Taşıyıcılar ve Alanların Dansı**\n\nPeki bu minik parçacıklar birbirini nasıl etkiler? Örneğin, iki mıknatıs birbirine dokunmadan nasıl çeker veya iter? Standart Model'e göre, kuvvetler de aslında parçacıklar aracılığıyla taşınır. Cisimler birbirine görünmez minik elçiler gönderir. Örneğin, elektrik ve manyetik kuvveti taşıyan elçi parçacık 'foton'dur (yani ışık taneciği). Atom çekirdeğini bir arada tutan güçlü kuvveti ise 'gluon' (yani yapıştırıcı) taşır. Fizikte bu kuvvetlerin yayıldığı alanlara 'alan' denir. Evren, boş bir uzayda duran parçacıklardan ibaret değildir; sürekli dalgalanan ve birbirleriyle etkileşen kozmik alanların dansıdır.",
                    "**Higgs Bozonu: Kütle Kazandıran Gizemli Şurup**\n\nStandart Model'in en uzun süre gizemini koruyan parçacığı Higgs Bozonu'dur. Fizikçiler, parçacıkların neden bir ağırlığa (kütleye) sahip olduğunu açıklamak için bir teori geliştirdiler: Evren, 'Higgs alanı' adı verilen görünmez ve yapışkan bir şurupla doludur. Parçacıklar bu şurubun içinden geçerken onunla etkileşime girer ve zor hareket ederler. Bu zorluk, parçacıklara kütle kazandırır. Örneğin fotonlar bu şurupla hiç etkileşime girmez, bu yüzden kütlesizdirler ve ışık hızında koşarlar. 2012 yılında CERN'deki dev laboratuvarda yapılan deneylerde Higgs Bozonu keşfedildi ve bu teorinin doğruluğu kanıtlanarak Standart Model'in eksik parçası tamamlandı.",
                    "**Madde ve Antimadde: Aynadaki İkizler**\n\nEvrenin en gizemli kurallarından biri de 'antimadde'dir. Doğadaki her temel parçacığın, tıpkı kendisi gibi ama zıt elektrik yüküne sahip bir ikizi vardır. Örneğin, negatif yüklü elektronun ikizi pozitif yüklü 'pozitron'dur. Madde ve antimadde bir araya geldiklerinde, anında birbirlerini yok ederler ve saf enerjiye (ışığa) dönüşürler. Büyük Patlama sırasında eşit miktarda madde ve antimadde oluşmuş olsaydı, hepsi birbirini yok eder ve evrende sadece ışık kalırdı. Ancak bilinmeyen bir nedenle madde, antimaddeye karşı galip geldi ve bugün gördüğümüz evreni oluşturdu."
                ]
            },
            {
                "id": "chapter5",
                "title": "BÖLÜM 5: Uzay Taneleri (Kuantum Kütleçekimi)",
                "image": "/images/space_pixels_loops_sketch.png",
                "imageCaption": "Kuantum İlmekleri",
                "takeaway": "Uzay boş bir kutu değildir; o, birbirine bağlanmış minik uzay tanelerinden oluşan dinamik ve canlı bir ağdır.",
                "paragraphs": [
                    "**Kuramların Savaşı: Genel Görelilik vs Kuantum Mekaniği**\n\nBugün modern fizikte büyük bir sorun vardır: Evreni açıklayan en iyi iki kuramımız birbiriyle anlaşamamaktadır! Einstein'ın Genel Görelilik kuramı, büyük dünyayı (uzayı, zamanı ve kütleçekimini) açıklar ve uzayın pürüzsüz, sürekli bir çarşaf gibi olduğunu söyler. Kuantum Mekaniği ise küçük dünyayı (atomları ve parçacıkları) açıklar ve her şeyin kesintili, paketler halinde olduğunu iddia eder. Ancak bu iki kuramı birleştirmeye çalıştığımızda matematik çöküyor ve anlamsız sonuçlar veriyor. Fizikçiler, evrenin tüm sırlarını birleştirecek bir 'Her Şeyin Teorisi' aramaktadır. Carlo Rovelli'nin üzerinde çalıştığı 'Döngü Kuantum Kütleçekimi' bu arayışın en güçlü adayıdır.",
                    "**Döngü Kuantum Kütleçekimi: Uzayın İlmekleri**\n\nDöngü Kuantum Kütleçekimi (Loop Quantum Gravity), uzayın yapısını tamamen yeniden tanımlar. Bu teoriye göre uzay, içine nesnelerin konulduğu boş bir kap değildir; uzayın kendisi de minik kuantlardan, yani 'uzay tanelerinden' oluşur! Bu taneler, birbirine ilmekler halinde bağlanarak devasa bir ağ oluşturur. Uzayı tıpkı yünden örülmüş bir hırkaya benzetebiliriz. Uzaktan baktığımızda pürüzsüz ve tek parça görünür. Ancak çok yakından incelediğimizde, onun aslında birbirine dolanmış minik yün ilmeklerinden oluştuğunu görürürüz. Uzay da minik ilmeklerin ördüğü kumaştır.",
                    "**Uzayın Pikselleri ve En Küçük Sınır**\n\nBilgisayar ekranındaki bir fotoğrafa çok yakından baktığınızda, görüntünün aslında küçük renk karelerinden (piksellerden) oluştuğunu fark edersiniz. Döngü Kuantum Kütleçekimi kuramına göre, uzayın kendisi de pikselleşmiştir! Doğada sonsuz küçüklük diye bir şey yoktur. Uzayın bölünebileceği en küçük bir sınır vardır ve buna Planck Uzunluğu (yaklaşık 10 üzeri -35 metre) denir. Bu sınırdan daha küçük bir alan veya hacim var olamaz. Bu keşif, fizikteki birçok matematiksel hatayı ve kara deliklerin merkezindeki sonsuz yoğunluk çıkmazını çözer.",
                    "**Zamanın Yok Oluşu: Kuantum Düzeyinde Zaman Var mıdır?**\n\nBu kuramın en sarsıcı iddiası zamanla ilgilidir. Döngü Kuantum Kütleçekimi denklemlerinde 'zaman' (t) değişkeni bulunmaz! En temel kuantum düzeyinde zaman diye bir şey yoktur. Evren, zamanın akışıyla ilerleyen bir saat gibi çalışmaz. Bunun yerine, sadece olaylar ve nesneler arasındaki ilişkiler ve değişimler vardır. Zaman, bizim gibi makroskopik canlıların evrene baktığında algıladığı bir yanılsamadır. Tıpkı sıcaklığın aslında atomların hareket hızı olması gibi, zaman da kuantum ilişkilerinin makro dünyadaki bir yansımasıdır."
                ]
            },
            {
                "id": "chapter6",
                "title": "BÖLÜM 6: Olasılık ve Kara Deliklerin Isısı (Termodinamik ve Zaman)",
                "image": "/images/hawking_radiation_sketch.png",
                "imageCaption": "Kara Deliklerin Isısı",
                "takeaway": "Zamanın akışı, aslında bizim dünyayı mikroskobik detaylarıyla göremememizden, yani cehaletimizden doğan bir illüzyondur.",
                "paragraphs": [
                    "**Isı Nedir? Sıcak Çay ve Entropi**\n\nFizikte birçok kural geçmişle geleceği birbirinden ayırmaz. Örneğin, gezegenlerin yörünge hareketlerini gösteren bir filmi geriye doğru oynatsanız, fizik kuralları açısından hiçbir gariplik görmezsiniz. Ancak ısı işin içine girdiğinde durum değişir! Sıcak bir çay bardağı masada soğur, ama soğuk çay kendi kendine ısınmaz. Isı, her zaman sıcaktan soğuğa doğru akar. Bunun nedeni 'entropi'dir, yani düzensizlik eğilimidir. Sıcak cisimlerin hızlı hareket eden atomları, soğuk cisimlerin yavaş atomlarına çarparak enerjiyi dağıtır. Bu süreç tek yönlüdür ve evrende zamanın akış yönünü (geçmişten geleceğe) belirleyen yegane şeydir.",
                    "**Kara Delikler: Kütleçekiminin Aşırı Uçları**\n\nKara delikler, evrenin en sıra dışı nesneleridir. Büyük kütleli bir yıldız öldüğünde, kütleçekimi nedeniyle kendi içine doğru çöker. Çökme o kadar güçlüdür ki, tüm kütle sıfır hacimli bir noktaya sıkışır. Bu noktanın etrafında 'olay ufku' adı verilen bir sınır oluşur. Bu sınırın içine giren hiçbir şey, ışık bile, kütleçekiminden kaçamaz. Kara delikler, uzay-zamanın yırtıldığı ve yerçekiminin sonsuz güce ulaştığı kozmik canavarlardır.",
                    "**Stephen Hawking ve Kara Deliklerin Isısı**\n\nStephen Hawking, kuantum kurallarını kara deliklere uyguladığında şaşırtıcı bir şey keşfetti: Kara delikler aslında sıcaktır ve dışarıya ısı yayarlar! Buna 'Hawking Radyasyonu' denir. Kuantum dalgalanmaları nedeniyle olay ufkunun hemen sınırında sürekli parçacık-antiparçacık çiftleri oluşur. Bunlardan biri kara deliğe düşerken, diğeri uzaya kaçar. Bu kaçan parçacıklar kara deliğin kütle kaybetmesine neden olur. Milyarlarca yıl içinde kara delikler yavaşça buharlaşarak yok olurlar.",
                    "**Termodinamik Zaman ve Algımız**\n\nCarlo Rovelli, zaman algımızın ısı ve bilgiyle doğrudan ilişkili olduğunu söyler. Kuantum seviyesinde zaman olmadığını görmüştük. Ancak biz makro dünyada yaşayan canlılar, evrendeki her atomun konumunu tek tek göremeyiz. Evrene dair bilgimiz sınırlıdır ve bu sınırlı bilgi, bizim entropiyi (düzensizliği) ve dolayısıyla ısının akışını algılamamıza neden olur. Zamanın akışı, aslında bizim dünyayı mikroskobik detaylarıyla göremememizden kaynaklanan bir durumdur."
                ]
            },
            {
                "id": "chapter7",
                "title": "BÖLÜM 7: Kendimiz (Kozmostaki Yerimiz)",
                "image": "/images/cosmic_trampoline_sketch.png",
                "imageCaption": "Kendimiz ve Kozmos",
                "takeaway": "Bizler doğadan ayrı değiliz; evrenin kendi kendisini düşünen, hisseden ve merak eden küçük parçalarıyız.",
                "paragraphs": [
                    "**Doğanın Bir Parçası Olarak İnsan**\n\nEvrenin bu devasa ve karmaşık yapısını inceledikten sonra akla şu soru gelir: Biz bu tablonun neresindeyiz? İnsanlar genellikle kendilerini doğadan ayrı, evreni dışarıdan izleyen özel varlıklar olarak görme eğilimindedirler. Ancak Carlo Rovelli bize hatırlatır ki, bizler evrenden ayrı değiliz; onun ayrılmaz bir parçasıyız! Bizi oluşturan atomlar, yıldızların içinde üretilen atomlarla aynıdır. Beynimizdeki düşünceler, kuantum kurallarına uyan parçacıkların etkileşimidir. Bizler evrenin dışındaki gözlemciler değil, evrenin kendi kendini gözlemleyen, düşünen ve hisseden küçük parçacıklarıyız.",
                    "**Bilincin Fiziksel Dokusu ve Beynimiz**\n\nDüşüncelerimiz, hayallerimiz ve bilincimiz çok gizemli görünür. Ancak modern bilim, bunların beynimizdeki milyarlarca sinir hücresi (nöron) arasındaki karmaşık elektrik ve kimyasal sinyallerden ibaret olduğunu gösterir. Beynimiz, evrendeki en karmaşık fiziksel sistemlerden biridir. Kuantum fiziğinde parçacıkların ilişkisel doğasını görmüştük; beynimiz de ilişkisel ağların en gelişmiş örneğidir. Bilinç, beynin kendi içindeki ve dış dünyayla kurduğu bu devasa bilgi ağının bir sonucudur.",
                    "**Özgür İrade ve Bilgi İşleme**\n\nÖzgür irademiz var mıdır, yoksa her hareketimiz fizik yasaları tarafından önceden belirlenmiş midir? Rovelli, özgür iradeyi fizik yasalarıyla çelişen mistik bir güç olarak görmez. Ona göre irade, beynimizin karar alırken geleceğe yönelik olasılıkları hesaplaması, hafızasındaki bilgileri değerlendirmesi ve en uygun seçeneği belirlemesi sürecidir. Bizler fizik kurallarının dışına çıkamayız, ancak beynimizin karmaşık yapısı sayesinde kendi kararlarımızı kendimiz üretebiliriz.",
                    "**Kozmik Yolculuk ve Bitmeyen Merak**\n\nİnsanlığın en büyük gücü merakıdır. Carlo Rovelli, kitabını çok dokunaklı bir şekilde bitirir. Bizler evrende çok kısa süre kalan, kırılgan ve ölümlü canlılarız. Ancak merakımız sayesinde sınırları aşıp yıldızların kalbine, kara deliklerin içine ve zamanın başlangıcına bakabiliyoruz. Bilim, sanat ve felsefe, bizim bu kozmik okyanusta yolumuzu bulmamızı sağlayan araçlardır. Rovelli'nin dediği gibi, bizler öğrenmek ve keşfetmek için doğduk. Evrenin sınırlarında bizi bekleyen daha birçok sır var ve merakımız bizi ileriye taşımaya devam edecek."
                ]
            }
        ]
    }
    
    output_path = "/Users/ilker/.gemini/antigravity-ide/scratch/zihingezgini-web/data/summaries/3.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=4)
    print("Successfully corrected and created summary for book 3 matching schema exactly!")

if __name__ == "__main__":
    create_summary()
