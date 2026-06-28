import pypdf

def extract_pdf():
    pdf_path = "/Users/ilker/Downloads/Zihin_Gezgini_300_Eser_Yol_Haritasi.pdf"
    txt_path = "/Users/ilker/.gemini/antigravity-ide/scratch/zihingezgini-web/tools/pdf_extracted_text.txt"
    
    reader = pypdf.PdfReader(pdf_path)
    print(f"Total pages: {len(reader.pages)}")
    
    all_text = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        all_text.append(f"--- PAGE {i+1} ---")
        all_text.append(text)
        
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(all_text))
        
    print("Done extracting PDF text!")

if __name__ == "__main__":
    extract_pdf()
