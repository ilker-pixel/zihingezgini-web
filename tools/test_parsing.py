import re

def test_parse():
    path = "/Users/ilker/.gemini/antigravity-ide/scratch/zihingezgini-web/tools/pdf_extracted_text.txt"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Let's find all numbered lines
    # Usually a line starts with a number like "1", "30", "150", etc.
    # Let's see if we can match: "1 Stephen Hawking Zamanın Kısa Tarihi Fizik & Kozmoloji ..."
    # Wait, the column names are: No | Yazar & Eser Adı | Kategori | Açıklama / Güncel Değer
    # Sometimes it extracts like: "No Yazar & Eser Adı Kategori Açıklama / Güncel Değer"
    # Followed by: "1 Stephen Hawking Zamanın Kısa Tarihi Fizik & Kozmoloji ..."
    
    # Let's write a script that looks for numbers at the start of sentences or lines
    lines = content.split("\n")
    print(f"Total lines in text: {len(lines)}")
    
    numbered_lines = []
    for line in lines:
        match = re.match(r'^\s*(\d+)\s+(.*)', line)
        if match:
            num = int(match.group(1))
            rest = match.group(2)
            if 1 <= num <= 300:
                numbered_lines.append((num, rest))
                
    print(f"Total numbered lines found: {len(numbered_lines)}")
    print("First 10 numbered lines:")
    for num, rest in numbered_lines[:10]:
        print(f"[{num}] {rest[:100]}...")
        
    print("Last 10 numbered lines:")
    for num, rest in numbered_lines[-10:]:
        print(f"[{num}] {rest[:100]}...")

if __name__ == "__main__":
    test_parse()
