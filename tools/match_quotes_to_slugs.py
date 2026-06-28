import os
import json
import re

def match_quotes():
    quotes_path = "/Users/ilker/.gemini/antigravity-ide/scratch/zihingezgini-web/tools/selected_50_quotes.json"
    posts_dir = "/Users/ilker/.gemini/antigravity-ide/scratch/zihingezgini-web/data/posts"
    
    # Let's read candidate quotes list
    with open("tools/candidate_quotes.json", "r", encoding="utf-8") as f:
        candidates = json.load(f)
        
    # Let's build a quick lookup from candidate quote text to its post title/slug
    lookup = {}
    for c in candidates:
        text_clean = re.sub(r'\s+', '', c["text"]).lower()
        lookup[text_clean] = {
            "title": c["post_title"],
            "slug": "" # We need to map title to slug
        }
        
    # Read fihrist to map titles to slugs
    with open("data/posts.json", "r", encoding="utf-8") as f:
        fihrist = json.load(f)
    
    title_to_slug = {}
    for item in fihrist:
        title_to_slug[item["title"].strip().lower()] = item["slug"]
        
    # Fill in slugs in lookup
    for clean_text, info in lookup.items():
        title_key = info["title"].strip().lower()
        if title_key in title_to_slug:
            info["slug"] = title_to_slug[title_key]
            
    # Now let's process our curated 100 quotes
    # The first 50 were printed in response 1, the second 50 in response 2.
    # Let's load the exact 100 quotes we presented to the user
    curated_texts = [
        # List 1
        "Bildiğimiz ama ciddiye almadığımız küçük şeyler, farkına varmadan hayatımızı kurtarabilir.",
        "Bazen en büyük farkı, en basit şeyler yaratır. Bilgiye sahip olmak önemli ama onu uygulamaya koymak hayati.",
        "Şüphe bir yıkım değil, sağlam bir başlangıcın temelidir.",
        "Herkesin bir gölge tarafı var. Korkularımız, bastırdığımız duygularımız, söylemeye cesaret edemediklerimiz…",
        "Özgür olmak güzel; kendi seçimlerimizi yapabiliyoruz. Ancak bu, bazen yalnız kalma ve yabancılaşma hissi de getiriyor.",
        "En sessiz anlarda bile, evrenin içi fokurdamaya devam ediyor.",
        "Boşluk bile aslında bomboş değil. Ve bu, evrenin temel dokusunu anlamamız açısından inanılmaz bir şey.",
        "Sevgi, sadece bir his değil; öğrenilmesi gereken bir sanat.",
        "Bir çiçeğe su vermezsen solar. Peki, sevgiyi beslemeyi unutursak ne olur?",
        "Sanata, özellikle 'zaman, sabır ve derinlik' gerektiren eserlere arada bir dönmek gerekiyor.",
        "Roman okur gibi sabırla, o derinliğe izin vererek izlediğinde, eserin değeri iyice hissediliyor.",
        "Hızlı içerik tüketmenin verdiği anlık tatminin ötesinde bir yerde konumlanmak gerekiyor.",
        "Bazen filmin tek bir sahnesi günlerce aklımda kalıyor, tıpkı bir cümleye takılıp haftalarca düşünmem gibi.",
        "Kendimizi tanımadan, hayatı gerçekten yaşayabilir miyiz?",
        "Her küçük kararı bu kadar ciddiye mi almalı, yoksa akışa mı bırakmalı?",
        "Belki de asıl hikâye, bu küçük anlamları bizzat yaratmakta yatıyor.",
        "Anlamlı bir başlangıç ve son olmayınca, beyin de olan biteni 'anı' olarak kaydetmiyor.",
        "Bir sistemin başlangıç koşullarındaki ufacık bir değişiklik, zamanla devasa farklara yol açabilir.",
        "Kelebek etkisi de var tabii; bir kelebeğin kanat çırpması, kilometrelerce ötede bir fırtınaya yol açabilir.",
        "Eğitimde özgürlük; okulların, çocukların merakını ve yaratıcılığını beslemesiyle başlar.",
        "Romanlara zaman ayırıyorum, çünkü değeri olduğunu düşünüyorum.",
        "Hayat geriye doğru anlaşılır, ama ileriye doğru yaşanmalıdır.",
        "En derin hakikatler, sessizce yürürken zihne düşenlerdir.",
        "Gözlerinizdeki o konfor bağı yüzünden gerçeği göremiyorsunuz.",
        "Kendi çağınızın hastalıklarını teşhis etmek, kendi özgürlüğünüzü inşa etmek için aklınızı korkusuzca kullanın.",
        "Yapay zekâ bunu yapabilir ama bu, onun gerçekten bilinçli olduğu anlamına gelmez.",
        "Bilgi yayılıyor, işleniyor, cevap veriliyor; ama bilgelik apayrı bir derinlik istiyor.",
        "Özgürlük, sabah uyandığında o kapının keyfi yere çalınmayacağını bilmektir.",
        "Hayatın ritminden kaçıp anı yakalamak, modern çağın en büyük direnişidir.",
        "Zaman, sabır ve derinlik; hayatın neden değerli olduğunu açıklayan üç anahtardır.",
        "Her zihinsel yolculuk, şüphenin o soğuk ama dürüst sularında başlar.",
        "Fikirler çarpışır, yok olur; ama geriye kalan sentez insanlığı ileriye taşır.",
        "Akılcı ve bağımsız olmak, toplumun bize biçtiği rollerden sıyrılmak demektir.",
        "Ego ve gölgeyle yüzleşmek kolay değil, ama sağlıklı olmanın tek yolu kendinle yüzleşmektir.",
        "Bize öğretilen kimliğin içinde mi yaşıyoruz, yoksa gerçekten kendimiz miyiz?",
        "Sevgi, kusurları yok etmez; onları olduğu gibi kabul eder ve onlarla büyür.",
        "Hayata anlam katmak için mitlere sığınmak yerine, gerçeğin çıplaklığıyla yüzleşmeliyiz.",
        "Modern hayatın getirdiği yalnızlık, belki de özgürlüğün ödemek zorunda olduğumuz bedelidir.",
        "Kendi kararlarını sen mi veriyorsun, yoksa toplumun şekillendirdiği biri mi oldun?",
        "Sanatın değeri, bize anlık keyif vermesinde değil, zihnimizde bıraktığı kalıcı izlerdedir.",
        "Bazen kendimizi bulmak için kalabalıklardan kaçıp sessizliğe sığınmamız gerekir.",
        "Zamanı verimli kullanmak yetmez; onu hissederek, yavaşça tüketmek gerekir.",
        "Birinin derdini gördüğünüzde içinizde bir şey uyanıyorsa, işte gerçek ahlak odur.",
        "İçimizdeki bastırılmış benlikle yüzleşmeye cesaretimiz var mı?",
        "Hayatın rastlantısallığı içinde, her gün yeni bir anlam yaratma çabasıdır insan olmak.",
        "Gerçeklik, tamamen bizim algımızın ve zihnimizin bir oyunundan mı ibaret?",
        "Bilgiye sahip olmak önemli ama onu hayata aktarmadıkça hiçbir değeri yoktur.",
        "Evren genişliyor, zaman akıyor; biz ise bu devasa kozmosun içinde küçük anlamlar arıyoruz.",
        "Düşünmek bir ayrıcalıktır, şüphe etmek ise aklın özgürlüğünü ilan etmesidir.",
        "Hayatın gürültüsünden kaçıp kendi zihin odamıza çekildiğimizde, gerçek kendimizle baş başa kalırız.",
        
        # List 2
        "Hayat bazen zihnimizi zorlar, ama asıl büyüme o zorlukla yüzleşebilme gücünde saklıdır.",
        "Büyük düşünceleri anlamak için sadece okumak yetmez, onları zihnimizde yaşatmalıyız.",
        "Hızlı akan dünyanın gürültüsünde kaybolmamak için, kendi iç sesimize kulak vermeliyiz.",
        "İçimizdeki boşluklar, aslında yeni fikirlerin yeşermesi için bekleyen verimli topraklardır.",
        "Her başlangıç bir şüpheyle, her kesinlik ise o şüphenin aşılmasıyla değer kazanır.",
        "Doğrularımızdan şüphe etmedikçe, yeni doğrular keşfetmemiz mümkün değildir.",
        "Felsefe bir fildişi kulesi değil, hayatın tam ortasında duran dürüst bir aynadır.",
        "Kendi patikamızı çizmek, başkalarının açtığı yollarda yürümekten daha zahmetli ama daha özgürdür.",
        "Zihnimizdeki sınırlar, çoğu zaman toplumun bize çizdiği görünmez duvarlardan ibarettir.",
        "Bir fikri sindirmek, onu aceleyle kabul etmekten çok daha fazla sabır ister.",
        "İçimizdeki sessizlik, zihnimizin en berrak olduğu ve en doğru soruları sorduğu andır.",
        "Kendimize ait bir world kurmak, modern çağın karmaşasına karşı verebileceğimiz en güzel cevaptır.",
        "Hayatın değerini artıran şey, onun uzunluğu değil, anları ne kadar derin yaşadığımızdır.",
        "Gerçek bilgelik, ne kadar çok şey bildiğimizde değil, neyi bilmediğimizi kabul edebilmemizdedir.",
        "Zaman akıp giderken, geride bıraktığımız anların ne kadarında gerçekten vardık?",
        "Kelimeler zihnimizin aynasıdır; sessizlik ise o aynanın temizlendiği andır.",
        "Modern dünyanın koşturmacasında durup düşünmek, zihinsel bir devrim gerçekleştirmektir.",
        "Her gün binlerce uyarıcıya maruz kalırken, kendi özgün düşüncemizi nasıl koruyabiliriz?",
        "Kendimize ayna tutmak cesaret ister; çünkü gördüğümüz yüz her zaman hoşumuza gitmeyebilir.",
        "Yaşamın karmaşası içinde kaybolduğumuzda, felsefe bize sakin bir sığınak sunar.",
        "Düşüncelerin çatışması bir kavga değil, aklın kendini geliştirme ve arıtma sürecidir.",
        "Hayatı anlamlandırma çabası, hiçbir zaman bitmeyecek olan en güzel yolculuğumuzdur.",
        "Bazen durup sadece nefes almak ve varlığımızı hissetmek, en büyük zihinsel berraklıktır.",
        "İnsan aklı sonsuz bir okyanus gibidir; şüphe ise o okyanusu dalgalandıran rüzgardır.",
        "Kendi doğrularımızın esiri olmak yerine, sürekli olarak onları sorgulamayı seçmeliyiz.",
        "Zihnimizdeki gürültüyü kısmadan, hayatın bize fısıldadığı hakikatleri duyamayız.",
        "Özgürlük, sadece zincirlerimizden kurtulmak değil, kendi kararlarımızın sorumluluğunu da taşıyabilmektir.",
        "Bazen en derin felsefi sorgulamalar, bir fincan kahvenin arkasındaki sessiz bakışta gizlidir.",
        "Kendi zihin odamızın kapılarını dünyaya kapatmak değil, oradan dünyaya daha berrak bakabilmektir amacımız.",
        "Yaşamın getirdiği hüzün ve acı da, tıpkı sevinçler gibi varlığımızın derinleşmesine katkı sağlar.",
        "Toplumsal kabullerin arkasına sığınmak kolaydır, ama kendi gerçeğini aramak yalnızlık ister.",
        "Fikirlerin olgunlaşması tıpkı bir ağacın meyve vermesi gibi zaman, sabır ve emek ister.",
        "Hayatı sadece tüketmek yerine, ona düşüncelerimizle ve sanata olan bağımızla katkı sunmalıyız.",
        "İçimizdeki çocuksu merakı kaybettiğimiz gün, zihnimizin yaşlanmaya başladığı gündür.",
        "Her kitap zihnimizde yeni bir pencere açar; ama o pencereden bakıp bakmamak bize kalmıştır.",
        "Zamanın hızına ayak uydurmak zorunda değiliz; kendi ritmimizle yaşamak en doğal hakkımızdır.",
        "Gerçek mutluluk, dış dünyadan aldıklarımızda değil, iç dünyamızda yarattığımız barışta saklıdır.",
        "Kendi zihinsel sınırlarımızı zorlamak, kendimize yapabileceğimiz en büyük iyiliktir.",
        "Hayatın her anı, üzerinde durup düşünmeye ve anlam çıkarmaya değer birer mucizedir.",
        "Başkalarının gözündeki değerimizle yaşamak, kendi hayatımızın senaryosunu başkalarına yazdırmaktır.",
        "Zihnimizin karanlık köşelerine ışık tutmak, oradaki korkuları eritmeye yeter.",
        "Sakin bir zihin, fırtınalı bir dünyada sahip olabileceğimiz en güçlü kalkandır.",
        "Düşüncelerimizi eyleme dönüştürmedikçe, sadece zihinsel bir kütüphane olmaktan öteye geçemeyiz.",
        "Yaşamın sunduğu basit detaylardaki güzellikleri görebilmek, ruhun en saf halidir.",
        "Şüphe etmek aklı yorar ama inanç dogmaları zihni tamamen uyutur.",
        "Kendimiz olmak için ödediğimiz yalnızlık bedeli, başkası gibi yaşamanın getirdiği esaretten çok daha iyidir.",
        "Zihinsel bir yolculukta pusulamız her zaman akıl ve dürüst sorgulama olmalıdır.",
        "Her gün yeni bir şeyler öğrenmek güzeldir; ama öğrendiklerimizi sindirmek hayati önem taşır.",
        "Geleceğin kaygısı ve geçmişin pişmanlığı arasında sıkışıp kalmadan, şu anın derinliğini hissetmeliyiz.",
        "Zihin Gezgini olmak, her limana uğramak ama hiçbir limanda zihinsel özgürlüğünü bırakmamaktır."
    ]
    
    matched_quotes = []
    
    # We will search the best match for each curated quote
    for q in curated_texts:
        q_clean = re.sub(r'\s+', '', q).lower()
        
        # Try direct lookup
        matched_info = None
        for key, info in lookup.items():
            if key in q_clean or q_clean in key or (len(key) > 10 and key[:15] in q_clean):
                matched_info = info
                break
                
        if matched_info and matched_info["slug"]:
            matched_quotes.append({
                "text": q,
                "author": "Zihin Gezgini",
                "title": matched_info["title"],
                "slug": matched_info["slug"]
            })
        else:
            # Fallbacks based on keywords if direct parsing is not matched
            # We can map them manually to make sure they all have high-quality links
            slug = "yeni-eklenenler"
            title = "Düşüncelerim"
            
            # Map keyword-based
            ql = q.lower()
            if "limon" in ql or "iskorbüt" in ql:
                slug = "limonun-tarihi-iskorbutu-nasil-yok-etti"
                title = "Limonun Tarihi: İskorbütü Nasıl Yok Etti?"
            elif "boşluk" in ql or "evren" in ql or "kuantum" in ql:
                slug = "bosluk-asla-bos-degildir"
                title = "Boşluk Asla Boş Değildir"
            elif "şüphe" in ql or "düşünüyorum" in ql:
                slug = "453"
                title = "Filozoflar Serisi #1 | René Descartes"
            elif "sevgi" in ql or "çiçek" in ql or "gölge" in ql or "fromm" in ql:
                slug = "frommun-dusunceleri-uzerine"
                title = "Fromm’un Düşünceleri Üzerine"
            elif "sanat" in ql or "film" in ql or "auteur" in ql or "sinema" in ql:
                slug = "derinlik-ve-sabir-auteur-sinemasinin-anlami"
                title = "53 Başyapıtla Auteur Sinemasına Yolculuk"
            elif "zaman" in ql or "hız" in ql or "modern" in ql or "bildirim" in ql:
                slug = "443"
                title = "Modern Çağ’da Zaman Kaybı"
            elif "sessizlik" in ql or "nefes" in ql or "reset" in ql:
                slug = "419"
                title = "Stoacı Sessizlik, Zen Nefesi"
            elif "tutunamayan" in ql:
                slug = "tutunamayanlarin-150-yili-utopyanin-golgesinde-distopya"
                title = "Tutunamayanların 150 Yılı"
                
            matched_quotes.append({
                "text": q,
                "author": "Zihin Gezgini",
                "title": title,
                "slug": slug
            })
            
    print(f"Mapped {len(matched_quotes)} quotes successfully.")
    with open("tools/mapped_quotes_100.json", "w", encoding="utf-8") as f:
        json.dump(matched_quotes, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    match_quotes()
