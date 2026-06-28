# Zihin Gezgini - Yazı ve İçerik Ekleme Kılavuzu

Bu kılavuz, **Zihin Gezgini** web sitesine yeni felsefi yazılar, sesli monologlar eklemek veya alıntı listesini güncellemek isteyen geliştiriciler ve Yapay Zekâ (AI) asistanları için hazırlanmış teknik bir yönergedir.

---

## 📂 Dosya ve Klasör Yapısı

Sitenin veri tabanı tamamen statik JSON dosyalarından oluşur:
*   `/data/posts.json` -> Ana sayfadaki yazıları, tarihleri ve kategorileri listeleyen **fihrist dosyası**.
*   `/data/posts/` -> Her yazının detaylı HTML içeriğini barındıran **detay dosyaları klasörü** (örn: `data/posts/453.json`).
*   `/images/` -> Yazıların kapak resimlerinin ve satır içi çizimlerinin bulunduğu klasör.
*   `/app.js` -> Sitenin tüm çalıştırıcı JavaScript motoru ve yönlendirmeleri (routing).
*   `/style.css` -> Tema ve bileşenlerin stil kuralları.

---

## ✍️ Adım 1: Yeni Yazı Detay Dosyasını Oluşturmak

Yeni bir yazı eklemek için öncelikle `/data/posts/` klasörü altında yazının slug ismiyle uyumlu yeni bir `.json` dosyası oluşturun (Örn: `data/posts/yeni-yazi-basligi.json`).

### JSON Şablonu:
```json
{
  "title": "Yazının Tam Başlığı",
  "date": "2026-06-28T15:00:00",
  "slug": "yeni-yazi-basligi",
  "featuredImage": "/images/yazi-kapak-gorseli.png",
  "content": "\n<p class=\"wp-block-paragraph\">Yazının ilk paragrafı buraya gelecek...</p>\n\n<p class=\"wp-block-paragraph\">İkinci paragraf buraya gelecek...</p>\n",
  "category": "Felsefe"
}
```

### ⚠️ JSON Oluştururken Dikkat Edilmesi Gereken Kritik Kurallar (AI Talimatları):
1.  **Çift Tırnak Kaçırma (Escaping):** `content` alanı içindeki tüm HTML etiketlerinde bulunan çift tırnak işaretleri (`"`) ters eğik çizgi ile kaçırılmalıdır (`\"`). Aksi halde JSON formatı bozulur.
    *   *Hatalı:* `<a href="https://example.com">Link</a>`
    *   *Doğru:* `<a href=\"https://example.com\">Link</a>`
2.  **Yazar Notu ve Video Bağlantıları:** Eğer yazının bir YouTube videosu/monoloğu varsa, yazar notunu paragrafın en başına şu etiketlerle ekleyin:
    `\"<p class=\\\"wp-block-paragraph\\\"><strong><em>Yazarın Notu:</em></strong>... YouTube kanalımda izleyebilirsiniz: <a href=\\\"YOUTUBE_URL\\\" target=\\\"_blank\\\"><strong>YouTube Video</strong></a></p>\"`
3.  **Kişiselleştirilmiş Çizimler:** Eğer yazı içine çizim eklenecekse resimler `/images/` klasörüne yüklenmeli ve içerik alanında `<figure class=\"wp-block-image\"><img src=\"/images/resim-adi.png\" alt=\"\" /></figure>` formatında çağrılmalıdır.

---

## 📋 Adım 2: Fihrist Dosyasını (`data/posts.json`) Güncellemek

Yeni eklenen yazının ana sayfada görünebilmesi için `/data/posts.json` dosyası açılmalı ve en üste (en yeni yazı olacak şekilde) yeni yazının meta verileri eklenmelidir.

### Fihrist Satır Şablonu:
```json
  {
    "title": "Yazının Tam Başlığı",
    "date": "2026-06-28T15:00:00",
    "slug": "yeni-yazi-basligi",
    "featuredImage": "/images/yazi-kapak-gorseli.png",
    "category": "Felsefe",
    "hasAudio": true
  }
```
*   **`hasAudio` Parametresi:** Eğer yazıda bir sesli monolog (YouTube videosu) bağlantısı bulunuyorsa, bu değer `true` yapılmalıdır. Bu sayede "Monologlar" filtresinde yazı otomatik olarak listelenir.

---

## 🎧 Adım 3: YouTube Monolog Entegrasyonu

Eğer yazı detay içeriğinde (`content`) bir YouTube video bağlantısı bulunuyorsa, sitenin motoru (`app.js`) bunu otomatik olarak tespit eder ve başlığın hemen altına dinamik bir **"🎧 Monoloğu Dinle"** butonu ekler.
*   Butona tıklandığında video sayfa yüklenmesini yavaşlatmayacak şekilde dinamik olarak `iframe` ile gömülür ve oynatılır.
*   Bu sistemin hatasız çalışması için yazı detay JSON'ındaki YouTube linkinin standart formatta olması yeterlidir (`https://www.youtube.com/watch?v=VIDEO_ID` veya `https://youtu.be/VIDEO_ID`).

---

## 💬 Adım 4: Tam Otomatik Derleme (Git Pre-commit Hook Altyapısı)

Yazınızı `/data/posts/yazı-adi.json` dosyasına ekledikten sonra manuel fihrist veya alıntı ekleme işlemleriyle uğraşmanıza gerek yoktur. Sizin için tüm süreci otomatikleştiren bir **Git pre-commit kancası (hook)** kurdum.

Bu sayede:
*   Siz (veya bir yapay zekâ) terminalde `git commit` komutunu çalıştırdığı an, Git arka planda otomatik olarak `python3 tools/build.py` scriptini koşturur.
*   Yazılar taranır, fihrist güncellenir ve yeni yazılardan **en güzel 5 alıntı otomatik ayıklanıp** `/data/quotes.json` dosyasına işlenir.
*   Tüm bu güncellenen dosyalar otomatik olarak commite dahil edilir. Siz ekstra hiçbir manuel komut çalıştırmazsınız!

### 💻 Bilgisayarınız Değişirse Bu Otomasyonu Nasıl Geri Getirirsiniz?
Git kancaları (`.git/hooks/` klasörü) GitHub'a yüklenmez. Eğer bilgisayarınız bozulur ve projeyi yeni bir bilgisayara kurarsanız, bu otomatik sistemi tek tıkla yeniden aktifleştirmek için terminalde şu komutu çalıştırmanız yeterlidir:
```bash
cp tools/pre-commit .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
```

---

## 🔄 Adım 5: Yayınlama ve Önbellek (Cache) Temizliği

Yazı dosyasını ekledikten sonra sitenizi yayına almak için sadece standart Git komutlarını girmeniz yeterlidir:
1.  Değişiklikleri GitHub'a gönderin (Otomasyon commit esnasında kendiliğinden çalışacaktır):
    ```bash
    git add .
    git commit -m "Yayınla: [Yazı Başlığı]"
    git push
    ```
2.  Script veya CSS dosyalarında kod bazlı bir değişiklik yaptıysanız tarayıcıların bunu anında algılaması için `/index.html` içindeki sürüm numaralarını (örn: `app.js?v=24` değerini `v=25` yaparak) artırın.
