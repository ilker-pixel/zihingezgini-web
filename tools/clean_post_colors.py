import os
import re
import json

def clean_colors():
    posts_dir = "/Users/ilker/.gemini/antigravity-ide/scratch/zihingezgini-web/data/posts"
    if not os.path.exists(posts_dir):
        print("Error: posts directory not found")
        return
        
    post_files = [f for f in os.listdir(posts_dir) if f.endswith(".json")]
    
    cleaned_count = 0
    
    for pf in post_files:
        path = os.path.join(posts_dir, pf)
        with open(path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except Exception as e:
                continue
                
        content = data.get("content", "")
        original_content = content
        
        # 1. Strip inline colors/background styles
        # e.g., style="color: rgb(54, 55, 55);font-size: 19px" -> font size can be kept, but color should be stripped.
        # To be clean, let's strip color declarations: style="color: rgb(...);" or style="color: ...;"
        # Or let's strip the entire style attribute if it contains color/background-color since the browser defaults are better.
        content = re.sub(r'style="[^"]*color:\s*[^";]+;?[^"]*"', '', content)
        content = re.sub(r'style="background-color:[^"]*"', '', content)
        
        # 2. Strip specific class color overrides
        content = re.sub(r'\s*class="[^"]*(has-dark-gray-color|has-black-color|has-text-color)[^"]*"', '', content)
        
        # 3. Clean up empty styles and tags if any
        content = content.replace('style=""', '')
        
        # Strip wordpress custom tags style/class cleanups
        content = re.sub(r'<mark[^>]*>', '<mark>', content)
        
        if content != original_content:
            data["content"] = content
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"Cleaned styles in: {data.get('title')} ({pf})")
            cleaned_count += 1
            
    print(f"Total cleaned posts: {cleaned_count}")

if __name__ == "__main__":
    clean_colors()
