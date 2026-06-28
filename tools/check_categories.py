import re
from parse_pdf_books import KNOWN_CATEGORIES

def check_fallbacks():
    path = "/Users/ilker/.gemini/antigravity-ide/scratch/zihingezgini-web/tools/pdf_extracted_text.txt"
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
        
    raw_lines = text.split("\n")
    current_book_num = 1
    
    i = 0
    while i < len(raw_lines):
        line = raw_lines[i].strip()
        if line == str(current_book_num):
            block_lines = []
            j = i + 1
            while j < len(raw_lines):
                next_line = raw_lines[j].strip()
                if next_line == str(current_book_num + 1) or (current_book_num == 300 and "ZİHİN GEZGİNİ" in next_line):
                    break
                if "PAGE" in next_line or "ZİHİN GEZGİNİ" in next_line or "Fikir Sanat ve Bilim Kitapları" in next_line or "Eğitim Serüveni" in next_line:
                    j += 1
                    continue
                block_lines.append(next_line)
                j += 1
            block_lines = [l for l in block_lines if l]
            
            if block_lines:
                author = block_lines[0]
                category_idx = -1
                for idx, bl in enumerate(block_lines[1:], start=1):
                    # Check ONLY exact match first
                    if bl in KNOWN_CATEGORIES:
                        category_idx = idx
                        break
                
                if category_idx == -1:
                    # Print block lines to see what we missed in KNOWN_CATEGORIES
                    print(f"Fallback for book {current_book_num}: {block_lines}")
                
                current_book_num += 1
                i = j - 1
        i += 1

if __name__ == "__main__":
    check_fallbacks()
