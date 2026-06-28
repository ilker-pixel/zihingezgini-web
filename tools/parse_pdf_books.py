import ast
import re
import json

# Strictly true category names in the PDF
KNOWN_CATEGORIES = {
    "Fizik & Kozmoloji", "Fizik", "Fizik & Karmaşıklık", "Matematik & Şüphecilik", "Biyoloji & Evrim",
    "Antropoloji & Evrim", "Tarih & Antropoloji", "Tarih & Kozmoloji", "Bilişsel Antropoloji",
    "Tarih & Sosyoloji", "Klasik Felsefe", "Ekoloji & Çevre", "Ekoloji Felsefesi",
    "Ekoloji Felsefesi & Estetik", "Bilim Sosyolojisi", "Antropoloji", "Antropoloji & Ekonomi",
    "Sosyoloji & Antropoloji", "Sosyoloji & Zaman", "Sinirbilim & Uyku", "Sinirbilim & Biyoloji",
    "Bilişsel Sinirbilim", "Psikoloji & Nörobiyoloji", "Sinirbilim & Bilinç", "Bilişsel Psikoloji",
    "Nöroloji & Zihin", "Bilişsel Dilbilim", "Bilişsel Bilim & Psikoloji", "Sinirbilim & Zihin",
    "Sinirbilim Korku", "Bilinç Felsefesi", "Zihin Felsefesi", "Bilişsel Bilim", "Sinirbilim",
    "Tıp Felsefesi & Bilim", "Sosyoloji", "Bilişsel Gelişim", "Ahlak Felsefesi", "Sosyoloji & Bellek",
    "Fenomenoloji", "Felsefeye Giriş", "Psikoloji & Sosyoloji", "Psikoloji & Felsefe", "Stoacı Felsefe",
    "Tarih & Biyografi", "Doğu Felsefesi", "Doğu Felsefesi & Strateji",
    "Dinler Tarihi", "Din Felsefesi", "Mitoloji",
    "Sosyoloji & Din", "Uygulamalı Etik", "Varoluşçu Psikoloji", "Varoluşçu Felsefe", "Tarih",
    "Siyaset Felsefesi", "Siyasi Sosyoloji & Tarih", "Siyasi Sosyoloji", "Siyaset Sosyolojisi",
    "Tarih & Siyaset", "Epistemoloji & Felsefe", "Estetik Felsefesi",
    "Felsefe & Mantık", "Bilim Felsefesi", "Bilimsel Okuryazarlık", "Epistemoloji & Şüphecilik",
    "Zihin Felsefesi & Biliş", "Fizik Felsefesi", "Fizik & Kaos", "Sosyal Bilimler Felsefesi",
    "Ekonomi Politik", "Sosyoloji & Ekonomi", "Sosyoloji & Coğrafya", "Coğrafya & Sosyoloji",
    "Kültür Analizi", "Sosyoloji & Kültür", "Kültür & Estetik", "Kültür & Göstergebilim",
    "Sanat & Estetik", "Sanat Sosyolojisi", "Feminist Felsefe",
    "Tarih & Feminizm", "Feminist Kuram", "Sosyal Kuram & Sosyoloji", "Eleştirel Teori & Sosyoloji",
    "Beden Sosyolojisi", "Sosyoloji & Irk", "Post-Kolonyal Kuram", "Kültürel İncelemeler",
    "Sanat Felsefesi & Sosyoloji", "Sanat Sosyolojisi & Politika", "Sosyoloji & Mekan",
    "Görsel Kültür", "Görsel Kültür & Medya", "Görsel Kültür & Gözetim", "Medya Çalışmaları",
    "Postmodern Felsefe & Kültür", "Geç Modernite Sosyolojisi", "Teknoloji Sosyolojisi",
    "Yapay Zeka Felsefesi", "Bilişsel Bilim & Yapay Zeka", "Teknoloji ve Toplum",
    "Teknoloji Sosyolojisi & Etik", "Gelecek Çalışmaları & Felsefe", "Sistem Kuramı & Felsefe",
    "Bütüncül Bilim & Felsefe", "Bilim Felsefesi & Sentez", "Ekolojik Sentez & Felsefe",
    "Felsefi Sentez", "Kozmik Sentez", "Felsefe", "Karşılaştırmalı Mistik Felsefe",
    "Mistik Felsefe & Psikoloji", "Felsefi Manifesto", "Varoluşçu Felsefe & Sentez",
    "Dilbilim", "Göstergebilim", "Medya Teorisi", "Siyaset & Medya", "Gazetecilik Tarihi",
    "Sosyoloji & İletişim", "Edebiyat / Klasik", "Postmodern Felsefe", "Post-Yapısalcı Felsefe",
    "Edebi Teori", "Estetik & Politika", "Siyaset & Estetik", "Sosyoloji & Felsefe",
    "Sentez Çalışması", "Kişisel Bildiri", "Kritik Teori", "Dilbilim & Siyaset",
    "Sanat & Göstergebilim", "Sanat Felsefesi", "Post-kolonyal Teori", "Kültürel Çalışmalar",
    "Sosyoloji & Cinsellik", "Sosyoloji & İktidar", "Estetik & Felsefe", "Modern Felsefe",
    "İnsanlık Tarihi", "Kılavuz", "Feminist Felsefe & Bilim", "Yapay Zeka & Felsefe",
    "Sanat & Felsefe", "Popüler Bilim & Sosyoloji", "Ekonomi & Sistemler", "Sosyal Bilimler",
    "Analitik Felsefe", "İslam Felsefesi", "Zaman Sosyolojisi", "Teknoloji & Fizik",
    "Sosyoloji & Teknoloji", "Yapay Zeka & Fütürizm", "Karmaşıklık Bilimi", "Yapay Zeka & Siyaset",
    "Varoluşçuluk", "Mistisizm & Tasavvuf", "Mistisizm & Felsefe", "Bilişsel Psikoloji & Etik",
    "Yönetim & Toplum", "Eğitim Felsefesi", "Edebiyat / Bilim", "Zihin & Ekoloji",
    "Bütünsel Felsefe", "Sistemler Teorisi", "Mistisizm & Nöroloji", "Ekonomi & Etik",
    "Popüler Fizik & Kozmoloji", "Tıp Felsefesi & Bilim",
    "Felsefe & Sosyoloji"
}

def parse_blocks():
    blocks_path = "/Users/ilker/.gemini/antigravity-ide/scratch/zihingezgini-web/tools/blocks.txt"
    books = []
    
    with open(blocks_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line.startswith("Book "):
                continue
                
            num_match = re.match(r'^Book (\d+):\s*(.*)', line)
            if not num_match:
                continue
                
            num = int(num_match.group(1))
            list_str = num_match.group(2)
            
            try:
                raw_block = ast.literal_eval(list_str)
            except Exception as e:
                print(f"Error parsing block for book {num}: {e}")
                continue
                
            # Merge elements ending with '&'
            block = []
            skip = False
            for k in range(len(raw_block)):
                if skip:
                    skip = False
                    continue
                current_item = raw_block[k].strip()
                if current_item.endswith('&') and k + 1 < len(raw_block):
                    merged = current_item + " " + raw_block[k+1].strip()
                    block.append(merged)
                    skip = True
                else:
                    block.append(current_item)
            
            # Clean page metadata
            cleaned_block = []
            for item in block:
                if re.match(r'^Sayfa\s+\d+\s+/\s+\d+$', item) or "Evre " in item or "Tüm okumaların" in item or "Birey, önce" in item or "No Yazar" in item or "Açıklama /" in item or "Dış dünyayı ve" in item or "Zihinsel yapıyı" in item or "Bireyden topluma" in item or "Düşünsel araçları" in item or "Gerçek dünyayı yöneten" in item or "Maddi dünyayı" in item or "Temsil araçlarının" in item or "Tüm okumaların" in item or "Yazar & Eser" in item or "Açıklama / Güncel Değer" in item:
                    continue
                cleaned_block.append(item)
                
            block = cleaned_block
            
            if len(block) >= 3:
                author = block[0]
                
                # Find category index
                category_idx = -1
                for idx in range(1, len(block)):
                    if block[idx] in KNOWN_CATEGORIES:
                        category_idx = idx
                        break
                        
                if category_idx != -1:
                    title = " ".join(block[1:category_idx])
                    category = block[category_idx]
                    description = " ".join(block[category_idx+1:])
                else:
                    # Fallback
                    title = block[1]
                    category = block[2]
                    description = " ".join(block[3:])
                    
                pub_match = re.search(r'\((İlk Basım|Yazım|Basım|Yayın|Sentez Çalışması):\s*([^)]+)\)', description)
                pub_date = pub_match.group(2) if pub_match else ""
                
                if pub_match:
                    description = description.replace(pub_match.group(0), "").strip()
                    
                description = re.sub(r'Sayfa\s+\d+\s+/\s+\d+.*$', '', description).strip()
                
                evre = (num - 1) // 30 + 1
                
                books.append({
                    "no": num,
                    "author": author,
                    "title": title,
                    "category": category,
                    "description": description,
                    "pubDate": pub_date,
                    "evre": evre,
                    "link": None
                })
            else:
                print(f"Error: Block too short for book {num}: {block}")
                
    print(f"Total parsed books: {len(books)}")
    
    # Save output
    output_path = "/Users/ilker/.gemini/antigravity-ide/scratch/zihingezgini-web/data/books.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(books, f, indent=4, ensure_ascii=False)
        
if __name__ == "__main__":
    parse_blocks()
