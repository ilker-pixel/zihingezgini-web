import os
import re
import json

def update_audio_index():
    posts_dir = "/Users/ilker/.gemini/antigravity-ide/scratch/zihingezgini-web/data/posts"
    index_path = "/Users/ilker/.gemini/antigravity-ide/scratch/zihingezgini-web/data/posts.json"
    
    if not os.path.exists(posts_dir) or not os.path.exists(index_path):
        print("Error: posts dir or index file not found")
        return
        
    # Read index file
    with open(index_path, "r", encoding="utf-8") as f:
        posts_index = json.load(f)
        
    yt_regex = r'https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)[a-zA-Z0-9_-]+'
    
    slug_has_audio = {}
    
    # Scan post detail files
    for filename in os.listdir(posts_dir):
        if not filename.endswith(".json"):
            continue
        path = os.path.join(posts_dir, filename)
        with open(path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                continue
                
        slug = data.get("slug")
        content = data.get("content", "")
        
        # Check if content has a youtube monologue link
        has_audio = bool(re.search(yt_regex, content))
        if slug:
            slug_has_audio[slug] = has_audio
            
    # Update index entries
    updated_count = 0
    for entry in posts_index:
        slug = entry.get("slug")
        has_audio = slug_has_audio.get(slug, False)
        entry["hasAudio"] = has_audio
        if has_audio:
            updated_count += 1
            
    # Write updated index
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(posts_index, f, indent=4, ensure_ascii=False)
        
    print(f"Updated index with audio flag. Total audio posts: {updated_count}/{len(posts_index)}")

if __name__ == "__main__":
    update_audio_index()
