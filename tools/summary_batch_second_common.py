#!/usr/bin/env python3
"""Helpers for the second twenty-book illustrated summary collection."""

from __future__ import annotations

from summary_batch_common import entry, write_books


DATE = "Ağustos 2026"


def chapter(title, section, core, example, depth, present, art, caption):
    """Create one illustrated chapter from four deliberately different angles."""
    return entry(title, [core, example, depth, present], section, art=art, caption=caption)


def make_book(
    no,
    slug,
    title,
    author,
    subtitle,
    color,
    original,
    sources,
    chapters,
    *,
    misreading,
    modern,
    questions,
    essence,
):
    if len(chapters) != 16:
        raise ValueError(f"Book {no} has {len(chapters)} illustrated chapters; expected 16")
    closing = [
        entry("Yaygın yanlış okuma", [
            misreading,
            "Bir düşünceyi tek cümlelik slogana çevirmek kolaydır; fakat bu kitapta asıl değer, iddianın hangi koşullarda geçerli olduğunu ve nerede sınırlandığını izlemektir. Okur, yazarın açıklamasını ahlaki emir ya da değişmez kader gibi almamalıdır.",
            "En güvenli okuma yöntemi, her güçlü cümlenin yanına iki küçük soru koymaktır: Burada hangi örnek kanıt sayılıyor ve hangi karşı örnek bu fikri zorlayabilir? Böylece kitap hayranlık nesnesi değil, çalışan bir düşünce aracına dönüşür.",
        ], "SON DURAKLAR"),
        entry("Bugünden bakınca", [
            modern,
            "Kitabı bugünün bilgisiyle okumak onu çöpe atmak anlamına gelmez. Eskiyen ayrıntıları ayırıp hâlâ işe yarayan soruyu korumak, klasiklerden alınabilecek en büyük verimdir.",
            "Bu nedenle rehber, yazarı son sözü söyleyen otorite gibi değil, düşünme biçimimizi değiştiren güçlü bir tartışma ortağı gibi ele alır.",
        ], "SON DURAKLAR"),
        entry("Gündelik hayatta kalan üç soru", [
            questions,
            "Bu üç soru evde, işte, haber okurken veya bir tartışmayı dinlerken kullanılabilir. Amaç her durumu kitaba uydurmak değil, gözden kaçan ilişkiyi görünür kılmaktır.",
            "Bir kavram gündelik hayatı daha dikkatli görmemizi sağlıyor ama insanları kolay etiketlere hapsetmiyorsa, gerçekten işe yarıyor demektir.",
        ], "SON DURAKLAR"),
        entry("Bir cümlede kitabın özü", [
            essence,
            "Akılda kalacak son görüntü, tek bir cevabın kapıyı kapatması değil; iyi kurulmuş bir sorunun karanlık odada yeni bir pencere açmasıdır.",
        ], "SON DURAKLAR"),
    ]
    return {
        "bookNo": no,
        "title": title,
        "author": author,
        "subtitle": subtitle,
        "coverImage": f"/images/summary-art-{no}-{slug}-v1.webp",
        "coverStyle": "artwork",
        "pdfUrl": f"/data/pdfs/{no}-{slug}-ozeti.pdf",
        "pdfLabel": "25-50 sayfalık PDF'yi indir",
        "longForm": True,
        "chapterArtStyle": "monochrome-engraving",
        "chapterArtColor": color,
        "meta": {
            "originalTitle": original,
            "compiler": "Zihin Gezgini · Yapay zeka destekli çalışma",
            "date": DATE,
            "language": "Türkçe",
        },
        "intro": (
            f"Bu çalışma, {author} tarafından yazılan {title} adlı eseri bir bakışta tüketmek yerine "
            "yirmi bir durakta yavaşça açar. Ana savı, gündelik örnekleri, tarihsel bağlamı ve güçlü "
            "itirazları birlikte izleyerek kitabın yalnız ne söylediğini değil, neden hâlâ konuşulduğunu gösterir."
        ),
        "sources": sources,
        "entries": [
            entry("Bu kitap nasıl okunmalı?", [
                subtitle,
                "Bu rehber sınav notu gibi ezberlenecek maddeler sunmaz. Kitabın ana fikrini gündelik sahneler, tarihsel olaylar ve bugünün tartışmalarıyla yavaş yavaş kurar; zor kavramları adını duyduğumuz anda değil, ne işe yaradığını gördüğümüz anda tanımlar.",
                "Yazarın güçlü yanları kadar kör noktaları da gösterilecektir. Böylece okur hem kitabın neden klasikleştiğini anlayabilir hem de her cümlesini tartışılmaz gerçek sanmadan kullanabilir.",
            ], "BAŞLANGIÇ"),
            *chapters,
            *closing,
        ],
    }


__all__ = ["chapter", "make_book", "write_books"]
