#!/usr/bin/env python3
"""Compact, book-specific input helpers for the sixth twenty-book collection."""

from __future__ import annotations

import zlib

from summary_batch_common import slugify
from next_twenty_common import write_specs


NUANCE_PATTERNS = (
    "Bu fikir tek başına bütün kitabı açıklayan sihirli anahtar değildir. {title} başlığını bir eğilim ve soru olarak tutmak, onu her olaya zorla uygulamaktan daha doğrudur.",
    "Burada anlatılan mekanizma kaçınılmaz bir kader gibi okunmamalıdır. Koşullar, kurumlar ve insanların tepkileri değiştiğinde {title} bambaşka sonuçlar verebilir.",
    "Yazar güçlü bir karşıtlık kurar, fakat gerçek hayat iki kutup arasında birçok ara ton taşır. {title} bu tonları silmek için değil, görünür kılmak için kullanılmalıdır.",
    "Bu örnek iddiayı anlaşılır kılar ama tek başına kanıtlamaz. {title} için farklı dönemlerden ve toplumlardan karşı örnekler aramak düşünceyi daha sağlam hale getirir.",
    "Betimleme ile onay birbirine karıştırılmamalıdır. Kitap {title} düzeninin nasıl çalıştığını gösterirken, bunun ahlaken doğru olduğunu söylemiş olmaz.",
    "Kavramın sınırı özellikle önemlidir: {title} bazı olaylarda merkezdeyken bazılarında yalnız küçük bir etkendir. Ölçüyü bağlam belirler.",
    "Kitabın yazıldığı dönem seçilen kelimeleri ve örnekleri etkiler. {title} bugün okunurken daha yeni bilgilerle sınanmalı, ama açtığı temel soru kaybedilmemelidir.",
    "Benzetme akılda kalıcıdır fakat gerçek dünyanın yerini tutmaz. {title} fikrini kullanırken benzetmenin nerede bittiğini ayrıca görmek gerekir.",
    "Bu açıklama kişisel niyeti tümüyle yok saymaz; yalnız sonucun niyetten daha büyük olabileceğini gösterir. {title} birey ile düzeni birlikte düşünmeyi ister.",
    "Aynı kavram hem aydınlatıcı hem de kötüye kullanılmaya açık olabilir. {title} insanlara etiket yapıştırmak için değil, ilişkileri daha dikkatli çözmek için işe yarar.",
    "Yazarın dili yer yer kesin olsa da sonuç olasılıklar dünyasında işler. {title} konusunda belirsizlik payını korumak, fikri zayıflatmak değil dürüstleştirmektir.",
    "Karşı çıkanların itirazı çoğu zaman ana soruya değil, iddianın genişliğine yönelir. {title} en verimli biçimde, neyi açıkladığı kadar neyi açıklamadığı da söylenince anlaşılır.",
    "Bu bölümdeki tarihsel sahne bugünün birebir kopyası değildir. {title} benzerliği kadar dönemler arasındaki farkları da hesaba kattığımızda gerçek bir düşünme aracına dönüşür.",
    "Kavramı yalnız olumlu ya da yalnız olumsuz görmek eksik kalır. {title} aynı anda imkân, maliyet ve beklenmeyen yan etki üretebilir.",
    "Bir olayın ardından kurulan düzgün hikâye, yaşanırken var olan belirsizliği gizleyebilir. {title} geriye dönük kolaycılığa karşı dikkatle okunmalıdır.",
    "Kitap okuru etkileyici sonuçlara hızla götürür; yine de {title} için kanıt, yorum ve değer yargısını ayrı ayrı tutmak gerekir.",
)

TODAY_PATTERNS = (
    "Bugün benzer bir durumla karşılaştığınızda, önce {title} fikrinin hangi somut ayrıntıda göründüğünü ve kimin hayatını değiştirdiğini sorun.",
    "Bir haber okurken {title} başlığını aklınıza getirin; görünen olayın arkasındaki kuralı, teşviki ve sessiz kalan kişiyi ayrı ayrı arayın.",
    "Gündelik bir karar öncesinde {title} açısından kısa vadeli kazancı ve uzun vadeli bedeli iki ayrı sütuna yazmak şaşırtıcı bir açıklık sağlar.",
    "İşyerinde ya da evde {title} benzeri bir gerilim çıktığında kişileri suçlamadan önce davranışı üreten koşulu değiştirmeyi deneyin.",
    "Sosyal medyada kesin bir hüküm gördüğünüzde {title} için hangi kanıtın eksik olduğunu sormak, heyecan verici fakat yanlış genellemeyi durdurabilir.",
    "Bir hafta boyunca {title} fikrinin küçük örneklerini not edin; kavramın gerçekten açıklayıcı mı, yoksa yalnız kulağa etkileyici mi geldiği ortaya çıkar.",
    "Bugünkü teknolojiler sahneyi değiştirmiş olabilir. Yine de {title} içindeki güç, korku, umut veya alışkanlık ilişkisini yeni araçların içinde yeniden arayın.",
    "Bir tartışmada {title} kavramını karşı tarafa yapıştırmadan önce kendi davranışınızda aynı mekanizmanın daha küçük bir örneğini bulun.",
    "Kamusal bir karar değerlendirilirken {title} yalnız ortalama sonucu değil, bedeli kimin ödediğini ve kimin söz sahibi olduğunu sormayı gerektirir.",
    "Kendinize şu küçük deneyi verin: {title} etkisini azaltan tek bir kural değişse insanların davranışı nasıl farklılaşırdı?",
    "Bir kurumun açıklamasını dinlerken {title} açısından söylenen amaç ile ortaya çıkan gerçek sonucu karşılaştırın.",
    "Geçmişteki örneği bugüne kopyalamak yerine {title} sorusunu koruyun; kişiler ve araçlar değişse de ilişkinin biçimi yeniden ortaya çıkabilir.",
    "Bir seçim yaparken {title} fikrinin size hangi görünmez varsayımı fark ettirdiğini tek cümleyle yazın.",
    "Çevrenizdeki sıradan bir nesneye {title} merceğiyle bakın; o nesneyi mümkün kılan insanları, zamanı ve sistemi izleyin.",
    "Bir iddia çok rahatlatıcı geliyorsa {title} konusunda onu yanlışlayabilecek olayı da düşünün. İyi fikir sınanmaktan korkmaz.",
    "Bölümü hayata taşımanın en sade yolu, {title} için 'başka türlü olsaydı ne değişirdi?' sorusunu gerçek bir sahneye uygulamaktır.",
)


def topic(title: str, section: str, claim: str, scene: str, nuance: str = "", today: str = ""):
    """Create an illustrated chapter while keeping repetitive scaffolding varied."""
    slot = zlib.crc32(title.encode("utf-8")) % len(NUANCE_PATTERNS)
    nuance = nuance or NUANCE_PATTERNS[slot].format(title=title.lower())
    today = today or TODAY_PATTERNS[(slot * 7 + 3) % len(TODAY_PATTERNS)].format(title=title.lower())
    art = slugify(title)[:42]
    caption = f"{title} fikrini tek bakışta hatırlatan simgesel sahne."
    return (title, section, claim, scene, nuance, today, art, caption)


__all__ = ["topic", "write_specs"]
