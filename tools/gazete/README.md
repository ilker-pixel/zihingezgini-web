# Gazete entegrasyonu

Yalnız `/gazete/` ve ona özel üretim/test dosyaları. Ana Zihin Gezgini sitesi değişmez.
Geliştirme dalı: `codex/gazete-four-feeds-sanitized`. Bu çalışma yayın veya push yapmaz.

## Tamamlanmış bülten sözleşmesi

`bundle.schema.json` resmi alan sözleşmesidir. Python importer ek olarak zaman sırasını,
Türkiye yayın slotunu, kimlikleri, tekrarları ve URL'leri denetler. JSON şeması tek başına
iş kurallarının yerine geçmez. Paket 1–4 tamamlanmış bülten içerebilir:

| feed_id | Türkiye saati | Anlam |
|---|---|---|
| morning | 08.00 | Sabah gündemi |
| ai | 21.00 | AI gündemi |
| youtube_am | 10.00 | YouTube sabah |
| youtube_pm | 22.00 | YouTube akşam |

`scheduled_for`: bültenin ait olduğu tarih/slot; `completed_at`: gerçekten tamamlandığı an.
`prepared_at`: veri paketinin hazırlanması; tamamlanma saati değildir. Tamamlanma saati bilinmiyorsa
`completed_at` null ve ayrı `prepared_at` gerekir. Kesin dönem bilinmiyorsa `coverage_start/end` null.
Bilinen dönemlerde bu alanlar kaynakların kapsandığı aralığı belirtir. Saatler ISO 8601 ve açık UTC offset ile
gelmeli; farklı offset aynı Türkiye slotuna dönüşüyorsa kabul edilir. Kaynak yayın tarihi
ayrı `sources[].published_at` alanındadır: saat dilimli datetime, gerçek tarih yalnız gün
biliniyorsa YYYY-MM-DD, kaynak belirtmiyorsa null. Bilinmeyen saat/tarih uydurulmaz.

Her konu: güvenli/stabil `id`, doğal konu `category`, kısa `title`, tek cümle `summary`,
mevcut kısa yazı `what_happened`, `sources`. Kategoriler: bilim, teknoloji, ekonomi, dunya, turkiye,
kultur, saglik, cevre, spor, felsefe, hava. Kategori üreticinin tamamlanmış paketinde verilmelidir;
bu araç haber veya kategori için AI çağırmaz. Yeni kategori sözleşme güncellemesi gerektirir.
Kaynak çekinceleri `what_happened` içinde korunur. Metin düz UTF-8, paragraflar boş satırla.
HTML metin olarak kaçırılır. Kaynaklar gerçek HTTP(S) URL, ad ve gerçek tarih taşır.
PDF, MP3, Ekşi ve ekonomi uygulamasının eski bağımsız bülteni bu sözleşmede yoktur.
Ekonomi konuları bu dört kaynağın içinden gelebilir.

## Yerel / bulut komutları

```sh
python3 tools/build_gazete.py --check-bundle /path/to/completed-bundle.json
python3 tools/build_gazete.py --import-bundle /path/to/completed-bundle.json
python3 tools/gazete/check_site.py
python3 tools/test_gazete.py
```

Yalnız render: `python3 tools/build_gazete.py --render`. Bu da mevcut gazete dizinini
yeniden oluşturur, internet yayını yapmaz. `--now` yalnız test/önizleme saati içindir;
rutin importta kullanmayın. Python 3.12 ve standart kitaplık yeterlidir; API anahtarı,
TTS, üçüncü taraf paket veya Mac servisi gerekmez.

## Yenileme, hatalar ve saklama

Önce paketin tamamı doğrulanır. Aynı kimlik/aynı içerik etkisiz tekrar; aynı kimlik/farklı
içerik hata; daha eski slot/tamamlanma etkisiz eski girdi. Aynı slot düzeltmesi yeni
bulletin_id ve daha sonraki paket hazırlama zamanı (yoksa completed_at) ile gelir.
Aynı içeriğin yeniden paketlenmesi prepared_at değişse de etkisizdir. Eksik kaynak eski halinde kalır.
Yeni kaynak bülteni kendi eski yazılarının tamamını değiştirir; konu kategorisi değişen
yazı eski kategorisinden çıkar. Başka kaynaklar dokunulmadan korunur.

Depodaki tek durum `gazete/data/current.json`: en çok dört son bülten, bülten başına
30 konu, tüm paket en çok 4 MB. Önceki gazete baskıları/PDF/MP3 kopyaları üretime eklenmez.
Ayrı bekleme havuzu bu sürümde kullanılmaz; böylece bir aylık üst sınır da aşılmaz.
Git'in mevcut metin geçmişi korunur; force push/purge yapılmaz. Büyük dosya veya
her baskıya ayrı klasör tasarımı yoktur. Eski gazete HTML'leri normal Git değişikliğinde
kaldırılır, geri alınabilir.

Import kilidiyle okuma/birleştirme/render sıraya alınır. Tüm sayfalar geçici dizinde
tamamlanır; sonra çalışma ağacı değiştirilir. Yerel dizin değiştirme iki rename içerir;
canlı yerel HTTP servisinde sıfır boşluk garantisi verilmez. `.gazete-previous` geri
dönüşü destekler. Kamuya yayın bütün dosyaları ve silmeleri içeren TEK Git commit ve
tek Pages deployment ile yapılmalıdır; tek tek Contents API yazıları uygun değildir.
Çalışma bitince kalıcı dizin yedeği tutulmaz. Render/import hatası eski yayını korur.
Tarayıcı, yayın slotundan sonra yeni paket gelmemişse güncellik etiketini dakika başı
salt okunur günceller; eski yazı yerinde kalır.

## Mac olmadan sonraki yayın

Hedef: `ilker-pixel/zihingezgini-web`, `main`. Bulut parent güncel main'i okur,
tamamlanmış paketi import eder, kontrolleri çalıştırır ve yalnız izinli gazete değişikliği
için tek Git tree/commit oluşturur. Güncel main SHA'yı esas alın; kaynak durumunu eski
checkout'tan yeniden kurmayın. Başka işlem main'i değiştirmişse yeniden okuyup importu
yenileyin; ref'i zorlamayın. İki yayın aynı anda çalışmasın. Yeni bültenin tamamlanmış
olması tetikleyicidir; saat geldi diye boş paket veya yeni haber üretilmez.

`.github/workflows/gazete-check.yml` yalnız doğrulama yapar, deployment veya secret
oluşturmaz. Mevcut genel site workflow'u değişmez. GitHub Pages'in branch/dizin yayın
ayarını ve mevcut connector'ın repo yazma yetkisini parent doğrulamalıdır. Depo main
branch kaynağından yayın yapıyorsa onaylı atomik commit sonrası mevcut Pages akışı
beklenir. Connector commit Pages'i tetiklemiyorsa veya Pages özel deployment istiyorsa
mevcut yetkilerle desteklenen yol ayrıca doğrulanmadan yayın başarılı sayılmaz.
Bu sürüm yeni token/OAuth/billing/Actions security izni oluşturmaz.

## Yerel Mac yayıncısının ezmesini önleme — henüz uygulanmadı

`GUNDEM_APP_HOME`, kurulu Gündem Pro uygulamasının veri/kod dizinini belirtir.
Aktif dosya `<GUNDEM_APP_HOME>/publisher.py`; bu yer tutucu hedef Mac'te çözülür.
`mac-publisher-guard.patch` export_site'in EN BAŞINA salt marker kontrolü ekler.
Marker: `<GUNDEM_APP_HOME>/.gazete-cloud-managed`.
Parent yayına hazır olduğunda, önce kod patch'ini doğrulayıp uygular, sonra marker'ı
oluşturur. Patch VE marker birlikte gereklidir; yalnız marker eski kodda işe yaramaz.
Kontrol SQLite init, dosya silme/oluşturma veya git işlemlerinden önce çalışır.
Diğer uygulamalar ve yerel bülten üretimi kapanmaz. Geri almak için yalnız marker
kaldırılır; patch işlevsiz halde kalabilir. Marker kalkınca eski yayıncı yeniden
gazeteyi yazabilir; bulut yönetimi sürerken kaldırmayın.

Gündem Pro kartının yeni gazeteyi göstermesi için yalnız `modules.json` içindeki
`id=newspaper` kaydının `url` değeri `https://zihingezgini.net/gazete/` yapılabilir.
Mevcut değer `http://127.0.0.1:8787/kapak`. Diğer kartlar/kimlik ayarları değişmez.
Bu iki canlı Mac ayarı bu geliştirme sırasında değiştirilmemiştir.

## Yayın doğrulaması

Yayın onayına kadar push/main merge/deploy yok. Onay sonrası Pages deployment ve
canlı konu/yazı/data URL'leri doğrulanır; Mac kapalıyken gerçek yeni bülten yayını ayrı
son testtir. Yerel birim testler bunu kanıtlamaz.

## Kaynak paket adaptörü ve gerçek veriler

`adapt_source_bundle.py SOURCE OUTPUT --sha256 EXPECTED` yalnız
`gundemgazetesi-source-bundle/1` paketini normalleştirir. Kaynak bültenler zaten
tamamlanmış olmalıdır. Kaynak saatlerini, paragraf dizisinin TAMAMINI, tüm kaynak
URL/adlarını ve publication/event_time/cutoff notlarını korur. Kaynak URL
listesindeki her adresin kendi yayın tarihi verilmediğinden o adrese genel bir
makale tarihi atanmaz; kayıt/yayın zamanı ayrı metaveri olarak gösterilir.
Kaynak alanları metadata ile aktarılır, haber veya TTS yeniden üretilmez.

3 Ekim paketinin SHA256 değeri:
`b38fe60a7a031b6d919103c6139a7c8d47e198b64590d9e34ef8ad59027dd406`.
41 makale: 9 sabah, 19 AI, 8 YouTube sabah, 5 YouTube akşam.
Kamuya açık üretim dosyasında yalnız normalleştirilmiş konu metinleri/metaveri
vardır; ham paket, Library kimlikleri ve PDF/audio dosyaları kopyalanmaz.

İsteğe bağlı tarayıcı QA: mevcut Playwright ve Chrome ile
`python3 tools/gazete/browser_qa.py --artifacts /tmp/gazete-qa`.
Bu test yerel loopback HTTP önizlemesi kullanır; deployment veya Mac kapalı test değildir.

## Detaylı oku ve Kaynaklar

Mevcut `id`, `category`, `title`, `summary`, `what_happened`, `sources` ve konu
metaverisi değiştirilmeden korunur. İsteğe bağlı `full_text` özgün kaynak anlatımını
ayrı tutar (en çok 200.000 karakter). `full_text_sources` ek kaynak listesi,
`full_text_sections` zaman kodu/başlık/URL/paragraflar ve varsa özgün warning işareti,
`full_text_metadata` özgün başlık, kaynak yayın/olay bilgisi, genel bakış,
Bir çırpıda sayfaları ve halka açık provenance taşır. Bu ek alanlar `full_text`
gerektirir; toplam 4 MB sınırı devam eder. Kaynak anlatımı kısa yazıyla eşit veya
daha kısa olabilir: sırf uzun görünmesi için içerik üretilmez. Daha kısa/eşit
anlatımda bu durum açıkça belirtilir. Kaynak anlatımı hiç yoksa en kapsamlı mevcut
metin, ayrı uzun anlatım bulunmadığı notuyla sunulur.

Her kartta ve kısa yazıda Detaylı oku bağlantısı vardır. Adres:
`/gazete/yazi/<feed_id>/<id>/detay/`. Detay sayfasında kısa yazıya ve gazete ana
sayfasına dönüş, özgün zaman kodlu video bölümleri ve varsa Bir çırpıda bölümü
bulunur. Eski kısa metnin çekinceleri ek açılır alanda korunur. Kaynak metnindeki
güvenli Markdown bağlantıları tıklanabilir; HTML çalıştırılmaz. Video zaman kodu
yayın/olay tarihi değildir. Bir bölümün URL'si kaynakta yoksa gerçek kaynak video
URL'si ve mevcut zaman kodundan yalnız gezinme bağlantısı oluşturulur.

Kaynak URL listeleri yazıların altına konmaz. Genel navigasyondaki
`/gazete/kaynaklar/` sayfasında güncel yazı başlığı/kimliğiyle ilişkili gruplar
bulunur; yazılar bu grubun sabit anchor'ına bağlanır. Tarih, kapsam ve kaynak kaydı
açılır alandadır. Bir kaynağın kendi yayın tarihi bilinmiyorsa ona yazının veya
paketin tarihi atanmaz. Yazı ve kaynak sayfası aynı atomik render/import işleminde
yenilenir; eski yazı kaldırılınca kaynak grubu da kaldırılır.

Ana sayfa konu gruplarına ayrılır: her grupta en çok üç yazı ve Tümünü gör,
kategori sayfasında tüm yazılar. Telefon tek sütundur; başlık/giriş küçültülmüş,
bülten durumları tek Güncelleme bilgisi açılır alanında toplanmıştır. Kontroller
en az 44 px, okuma metni 17,4 px / 31 px'tir. Diğer site bölümleri değişmez.

Özgün kaynak eşlemesini hazırlama (yayın yapmaz):

```sh
python3 tools/gazete/add_full_details.py ORIGINAL_MAPPING.json COMPLETED.json --sha256 EXPECTED_SHA256
python3 tools/build_gazete.py --import-bundle COMPLETED.json
python3 tools/test_gazete.py
python3 tools/gazete/check_site.py
python3 tools/gazete/verify_details.py --baseline BEFORE_CURRENT.json --source ORIGINAL_MAPPING.json
python3 tools/gazete/browser_qa.py --artifacts /tmp/gazete-qa --browser /usr/bin/chromium
```

Adaptör yalnız `gundemgazetesi-full-details/1` içindeki `details_by_article_id`
eşlemesini kabul eder. Güncel tüm yazı kimlikleri ve feed'ler eşleşmelidir; girdi
SHA256 ve varsa özgün haber metni SHA256 kontrol edilir. Kısa alanları yazmaz.
Detay eklenmesi düzeltilmiş bülten kabul edilir; yeni deterministik bulletin_id
ve kaynağın gerçek assembled_at değeri prepared_at olur. Planlanan/tamamlanma
ve kapsam zamanları değiştirilmez. Aynı girdi tekrarında aynı kimlik oluşur.
Eski kaynağın düzeltmesi daha yeni bir bülteni ezmez. Library kimlikleri üretime
kopyalanmaz; yalnız halka açık kaynak kökeni korunur.

3 Ekim özgün detay eşlemesi SHA256:
`3abd27bc323909b0716399210dbded0ef7bd62e97abf374605369eca61f844fe`.
41 yazı, 13 YouTube yazısında 145 zaman kodlu bölüm ve 21 Bir çırpıda sayfası.
Bu feature çalışması push/merge/deploy yapmaz; teslim patch'i güncel main ile
karşılaştırılarak parent tarafından incelenir ve buluttan yayımlanır.
