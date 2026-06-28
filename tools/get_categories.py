import re

def list_categories():
    path = "/Users/ilker/.gemini/antigravity-ide/scratch/zihingezgini-web/tools/pdf_extracted_text.txt"
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
        
    raw_lines = text.split("\n")
    current_book_num = 1
    
    i = 0
    categories = []
    
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
                # Find the line that ends with the publication date (the end of the description)
                # The description is at the end.
                # Let's find the line before the description lines.
                # Description usually starts with a line that has lowercases or is long.
                # Let's search from the end for the first line that is a category.
                # A category line is usually short, capitalized, and doesn't look like a description sentence.
                # Let's print the candidate lines for each book to inspect.
                print(f"Book {current_book_num}: {block_lines}")
                
            current_book_num += 1
            i = j - 1
        i += 1

if __name__ == "__main__":
    list_categories()
