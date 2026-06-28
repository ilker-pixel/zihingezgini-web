import json

def extract():
    log_path = "/Users/ilker/.gemini/antigravity-ide/brain/f59b25b4-20b9-43ff-875f-69a0997cf420/.system_generated/logs/transcript_full.jsonl"
    output_path = "/Users/ilker/.gemini/antigravity-ide/scratch/zihingezgini-web/tools/extracted_books.txt"
    
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            if "ZİHİN GEZGİNİ 300 ESERLİK" in line:
                try:
                    data = json.loads(line)
                    # The user request is usually in data["content"] or data["tool_calls"] or similar
                    content = data.get("content", "")
                    if not content and "parts" in data:
                        content = str(data["parts"])
                    
                    with open(output_path, "w", encoding="utf-8") as out:
                        out.write(content)
                    print(f"Extracted content length: {len(content)}")
                    return
                except Exception as e:
                    print(f"Error parsing line: {e}")

if __name__ == "__main__":
    extract()
