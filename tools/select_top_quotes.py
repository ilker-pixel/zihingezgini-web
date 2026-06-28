import json
import random

def select_quotes():
    with open("tools/candidate_quotes.json", "r", encoding="utf-8") as f:
        candidates = json.load(f)
        
    # We want 50 premium quotes. Let's filter for high-impact keywords
    keywords = ["zaman", "hayat", "insan", "düşünce", "sevgi", "özgürlük", "sessiz", "sabır", "kendi", "karar", "dünya", "gerçek", "anlam", "bilgi", "ruhum", "yolculuk", "sakin", "yaşam", "keşif", "değer"]
    
    impactful = []
    others = []
    
    seen = set()
    
    for c in candidates:
        text = c["text"]
        # Basic cleanups
        text = text.replace(" ", " ").replace("  ", " ").strip()
        
        # Skip duplicates or very similar
        if text.lower() in seen or len(text) < 40 or len(text) > 110:
            continue
            
        seen.add(text.lower())
        
        # Check if it has impact keywords
        if any(kw in text.lower() for kw in keywords):
            impactful.append(text)
        else:
            others.append(text)
            
    # Combine lists
    random.seed(42) # For reproducibility
    random.shuffle(impactful)
    random.shuffle(others)
    
    selected = impactful[:40] + others[:15]
    random.shuffle(selected)
    selected = selected[:50]
    
    print(f"Selected {len(selected)} high-quality quotes from personal posts:")
    for idx, q in enumerate(selected, 1):
        print(f"{idx}. {q}")
        
    with open("tools/selected_50_quotes.json", "w", encoding="utf-8") as f:
        json.dump(selected, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    select_quotes()
