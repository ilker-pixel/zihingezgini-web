import os
import re
import json

def find_marks():
    posts_dir = "/Users/ilker/.gemini/antigravity-ide/scratch/zihingezgini-web/data/posts"
    if not os.path.exists(posts_dir):
        return
        
    post_files = [f for f in os.listdir(posts_dir) if f.endswith(".json")]
    
    for pf in post_files:
        path = os.path.join(posts_dir, pf)
        with open(path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except Exception as e:
                continue
                
        content = data.get("content", "")
        # Find all marks
        marks = re.findall(r'<mark[^>]*>(.*?)</mark>', content, re.DOTALL)
        for m in marks:
            if len(m) > 40: # If mark contains more than 40 chars
                print(f"Post '{data.get('title')}' has a long mark ({len(m)} chars): {m[:60]}...")

if __name__ == "__main__":
    find_marks()
