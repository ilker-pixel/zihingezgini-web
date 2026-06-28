import os
import re
import json

def clean_html(html_content):
    # Strip HTML tags
    clean = re.sub(r'<[^>]*>', ' ', html_content)
    # Normalize whitespaces
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean

def extract_top_sentences(content_html, title, slug, num_quotes=5):
    clean_text = clean_html(content_html)
    
    # Split into sentences using punctuation (. ! ?)
    sentences = re.split(r'(?<=[.!?])\s+', clean_text)
    
    keywords = ["zaman", "hayat", "insan", "düşünce", "sevgi", "özgürlük", "sessiz", "sabır", "kendi", "karar", "dünya", "gerçek", "anlam", "bilgi", "ruhum", "yolculuk", "sakin", "yaşam", "keşif", "değer", "ruh", "felsefe", "bilim", "doğru", "şüphe", "yalnız", "söz", "eser", "sanat", "birey", "toplum"]
    exclude_words = ["ben ", "benim ", "bana ", "kendimi ", "yazarın notu", "youtube", "http", "okurlar", "serisi", "abone", "kanal", "tarihsel"]
    
    candidates = []
    
    for s in sentences:
        s = s.strip()
        # Clean formatting artifacts
        s = s.replace(" ", " ").replace("  ", " ").strip()
        
        # Filter rules
        if len(s) < 45 or len(s) > 115:
            continue
        if any(w in s.lower() for w in exclude_words):
            continue
        if not s[0].isupper():
            continue
            
        # Score sentence based on keywords
        score = sum(1 for kw in keywords if kw in s.lower())
        candidates.append((score, s))
        
    # Sort by score descending, then by length descending
    candidates.sort(key=lambda x: (-x[0], -len(x[1])))
    
    # Take the top ones
    results = []
    for score, text in candidates[:num_quotes]:
        results.append({
            "text": text,
            "author": "Zihin Gezgini",
            "title": title,
            "slug": slug
        })
        
    # If we found less than requested, fill with longest filtered sentences
    if len(results) < num_quotes:
        all_filtered = [s for s in sentences if 40 <= len(s) <= 120 and not any(w in s.lower() for w in exclude_words)]
        all_filtered.sort(key=len, reverse=True)
        for s in all_filtered:
            if len(results) >= num_quotes:
                break
            s_clean = s.strip().replace(" ", " ").replace("  ", " ")
            if not any(r["text"] == s_clean for r in results):
                results.append({
                    "text": s_clean,
                    "author": "Zihin Gezgini",
                    "title": title,
                    "slug": slug
                })
                
    return results

def run_build():
    posts_dir = "data/posts"
    fihrist_path = "data/posts.json"
    quotes_path = "data/quotes.json"
    
    print("🚀 Starting Zihin Gezgini Build Automation...")
    
    if not os.path.exists(posts_dir):
        print("Error: data/posts directory not found!")
        return
        
    # 1. Read all post details from files
    post_files = [f for f in os.listdir(posts_dir) if f.endswith(".json")]
    all_details = []
    
    for pf in post_files:
        path = os.path.join(posts_dir, pf)
        with open(path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                all_details.append(data)
            except Exception as e:
                print(f"Warning: Failed to parse {pf}: {e}")
                
    # Sort posts by date descending
    all_details.sort(key=lambda x: x.get("date", ""), reverse=True)
    
    # 2. Build the main fihrist (data/posts.json)
    fihrist_posts = []
    youtube_regex = r'(https?://(?:www\.)?youtu(?:be\.com/watch\?v=|\.be/)([\w-]+))'
    
    for post in all_details:
        content = post.get("content", "")
        # Detect YouTube link inside content
        has_audio = bool(re.search(youtube_regex, content))
        
        fihrist_posts.append({
            "title": post.get("title", ""),
            "date": post.get("date", ""),
            "slug": post.get("slug", ""),
            "featuredImage": post.get("featuredImage", None),
            "category": post.get("category", "Düşünce"),
            "hasAudio": has_audio
        })
        
    with open(fihrist_path, "w", encoding="utf-8") as f:
        json.dump(fihrist_posts, f, indent=4, ensure_ascii=False)
    print(f"✓ Successfully compiled fihrist of {len(fihrist_posts)} posts.")
    
    # 3. Handle auto-generation of quotes (data/quotes.json)
    existing_quotes = []
    if os.path.exists(quotes_path):
        with open(quotes_path, "r", encoding="utf-8") as f:
            try:
                existing_quotes = json.load(f)
            except Exception as e:
                print(f"Warning: Failed to load quotes.json: {e}")
                existing_quotes = []
                
    # Keep set of slugs that already have quotes
    existing_slugs = set(q.get("slug") for q in existing_quotes if q.get("slug"))
    
    new_quotes_count = 0
    
    for post in all_details:
        slug = post.get("slug")
        title = post.get("title")
        content = post.get("content", "")
        
        # If this post is new and doesn't have quotes yet
        if slug not in existing_slugs:
            print(f"🔍 Extracting 5 quotes from new post: {title}")
            new_quotes = extract_top_sentences(content, title, slug)
            existing_quotes.extend(new_quotes)
            new_quotes_count += len(new_quotes)
            
    with open(quotes_path, "w", encoding="utf-8") as f:
        json.dump(existing_quotes, f, indent=4, ensure_ascii=False)
        
    print(f"✓ Done. Quotes pool updated in data/quotes.json (added {new_quotes_count} new quotes, total pool is {len(existing_quotes)}).")
    print("🎉 Build successfully completed.")

if __name__ == "__main__":
    run_build()
