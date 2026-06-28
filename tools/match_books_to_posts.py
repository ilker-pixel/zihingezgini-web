import json

def match_books():
    books_path = "data/books.json"
    
    with open(books_path, "r", encoding="utf-8") as f:
        books = json.load(f)
        
    # Manual mappings for his existing philosophical post articles
    # mapping book number -> post slug
    mappings = {
        59: "frommun-dusunceleri-uzerine",                        # Erich Fromm - Özgürlükten Kaçış
        85: "arthur-schopenhauer-mutluluk-yalanı",                # Schopenhauer - İsteme ve Tasarım Olarak Dünya
        86: "soren-kierkegaard-inanc-sicramasi",                  # Kierkegaard - Ya/Ya da
        93: "thomas-hobbes-leviathanin-dogusu",                   # Thomas Hobbes - Leviathan
        121: "453",                                               # René Descartes - Meditasyonlar
        123: "wilhelm-leibniz-newtonun-golgesinde-kalan-deha",    # Leibniz - Monadoloji
        125: "john-locke-tabula-rasa",                            # John Locke - İnsan Anlığı Üzerine Deneme
        127: "david-hume-neden-sonuc-bir-masal-mi",                # David Hume - İnsan Doğası
        131: "friedrich-hegel-aklin-kurnazligi-ve-diyalektik",    # Hegel - Tinin Fenomenolojisi
        155: "karl-marx-koleligin-yeni-adi",                      # Karl Marx - Kapital
        200: "tutunamayanlarin-150-yili-utopyanin-golgesinde-distopya"  # Oğuz Atay - Tutunamayanlar
    }
    
    matched_count = 0
    for b in books:
        num = b["no"]
        if num in mappings:
            b["link"] = f"#/post/{mappings[num]}"
            matched_count += 1
            print(f"Matched Book {num}: {b['title']} -> {b['link']}")
            
    with open(books_path, "w", encoding="utf-8") as f:
        json.dump(books, f, indent=4, ensure_ascii=False)
        
    print(f"Successfully matched and updated {matched_count} books in books.json!")

if __name__ == "__main__":
    match_books()
