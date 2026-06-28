import os
import re
import json

def extract_candidates():
    posts_dir = "/Users/ilker/.gemini/antigravity-ide/scratch/zihingezgini-web/data/posts"
    if not os.path.exists(posts_dir):
        print("Error: posts directory not found")
        return
        
    post_files = [f for f in os.listdir(posts_dir) if f.endswith(".json")]
    
    sentence_candidates = []
    
    for pf in post_files:
        path = os.path.join(posts_dir, pf)
        with open(path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except Exception as e:
                continue
                
        content = data.get("content", "")
        title = data.get("title")
        
        # Clean HTML tags
        clean_text = re.sub(r'<[^>]*>', ' ', content)
        # Normalize whitespace
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        
        # Split into sentences using punctuation (. ! ?)
        sentences = re.split(r'(?<=[.!?])\s+', clean_text)
        
        for s in sentences:
            s = s.strip()
            # Basic filters: length, check if it's not a quote block signature or author mention
            if 35 <= len(s) <= 120:
                # Exclude sentences containing typical citation names
                exclude_words = ["rené", "descartes", "kierkegaard", "schopenhauer", "hobbes", "hegel", "fromm", "wilde", "ceylan", "grok", "ai", "youtube", "kanal", "abone", "yazarın notu", "tarihsel", "http", "www"]
                if not any(w in s.lower() for w in exclude_words):
                    # Exclude typical question prompts or empty ones
                    if not s.startswith("🔮") and not s.startswith("💡") and not s.startswith("🎭"):
                        sentence_candidates.append({
                            "text": s,
                            "post_title": title
                        })
                        
    print(f"Extracted {len(sentence_candidates)} candidate sentences from personal writings.")
    
    # Save candidates to inspect
    with open("tools/candidate_quotes.json", "w", encoding="utf-8") as f:
        json.dump(sentence_candidates, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    extract_candidates()
