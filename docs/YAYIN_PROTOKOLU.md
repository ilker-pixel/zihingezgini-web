# Zihin Gezgini Tek Seferlik Yayın Protokolü

Bu protokol, 300 kitaplık arşivin içerik, hız, erişilebilirlik ve kullanım kalitesini tek teslimatta doğrular. Her yayın aynı sırayı izler; herhangi bir zorunlu kapı başarısız olursa canlıya çıkış durur.

## 1. Editoryal kapı

- Okuma Haritası açıklamalarında çalışma notu, aşama metni ve `No Kategori` kalıntısı bulunamaz.
- Aynı hazır cümle 100 veya daha fazla kez kullanılamaz.
- Bir araştırma dosyasında aynı alıntı iki bölümde tekrarlanamaz.
- Kaynak metin eksikse yeni bilgi uydurulmaz; tekrar kaldırılır ve özgün içerik korunur.
- Okuyucu arayüzünde derleyen, yapay zekâ durumu veya güncelleme tarihi gösterilmez.

## 2. İçerik bütünlüğü kapısı

- 300 kitabın tamamı geçerli bir özet adresine sahip olmalıdır.
- Her özet en az iki dış kaynak içermelidir.
- PDF bağlantısı verilen her dosya fiziksel olarak bulunmalıdır.
- Sapiens ve Yapay Zekâ başlıkları tam biçimleriyle kalmalıdır.
- Arama dizini yazı, özet ve araştırma arşivinin tamamını kapsamalıdır.

## 3. Okuma deneyimi kapısı

- Uzun özetlerde fihrist, okuma ilerlemesi, kaldığın yere dönme, yazı boyutu, satır genişliği ve yazdırma görünümü bulunmalıdır.
- Haritada kategori, evre, durum ve PDF filtreleri; numaraya gitme, rastgele seçim ve ilerleme yedeği bulunmalıdır.
- Beş başlangıç rotası özgün kitap sırasını değiştirmeden çalışmalıdır.

## 4. Performans ve erişilebilirlik kapısı

- Logo ve ilk ekrandaki görseller sınırlandırılmış WebP kopyalarından yüklenir.
- Görseller genişlik ve yükseklik bilgisi taşır.
- Harici yazı tipi ilk görüntüyü engellemez.
- Ana sayfada tek görünür H1 ve tek ana içerik alanı bulunur.
- Klavye atlama bağlantısı, yeterli kontrast ve en az 24 x 24 piksel etkileşim alanı korunur.

## 5. Operasyon kapısı

- Statik sayfalar yeniden üretilir.
- Editoryal protokol, yerel bağlantılar, meta veriler, site haritası ve dosya bütçesi test edilir.
- Haftalık dış bağlantı denetimi 404 ve 410 yanıtlarını raporlar; 403 ve 429 geçici kabul edilir.
- Büyük medya dosyaları için 900 MB yayın eşiği uygulanır. Eşik aşılmadan önce PDF ve görseller ayrı nesne depolamaya taşınır; Git LFS yayın çözümü olarak kullanılmaz.

## Tek komut sırası

1. `python3 tools/editorial_protocol.py --fix`
2. `python3 tools/optimize_site_images.py`
3. `python3 tools/build_legacy_summary_pdfs.py`
4. `python3 tools/build_static.py`
5. `python3 tools/editorial_protocol.py`
6. `python3 tools/test_static_site.py`
7. `python3 tools/check_asset_budget.py`

Bu yedi adımın tamamı başarılı olmadan yayın onaylanmış sayılmaz.
