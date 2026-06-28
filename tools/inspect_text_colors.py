import os
import re
import json

def inspect_colors():
    posts_dir = "/Users/ilker/.gemini/antigravity-ide/scratch/zihingezgini-web/data/posts"
    if not os.path.exists(posts_dir):
        print("Error: posts directory not found")
        return
        
    post_files = [f for f in os.listdir(posts_dir) if f.endswith(".json")]
    
    affected_posts = []
    
    for pf in post_files:
        path = os.path.join(posts_dir, pf)
        with open(path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except Exception as e:
                continue
                
        content = data.get("content", "")
        title = data.get("title")
        
        # Search for inline style color or class override colors
        # style="color: rgb(x,y,z)" or style="color: #xxxxxx"
        style_matches = re.findall(r'style="[^"]*color:\s*[^";]+[^"]*"', content)
        class_matches = re.findall(r'class="[^"]*(has-dark-gray-color|has-black-color|has-text-color)[^"]*"', content)
        
        if style_matches or class_matches:
            affected_posts.append({
                "file": pf,
                "title": title,
                "style_matches": style_matches[:3],  # Show up to 3 matches
                "class_matches": class_matches[:3]
            })
            
    print(f"Found {len(affected_posts)} affected posts:")
    for ap in affected_posts:
        print(f"\n- Post: {ap['title']} ({ap['file']})")
        if ap['style_matches']:
            print(f"  Inline Styles: {ap['style_matches']}")
        if ap['class_matches']:
            print(f"  Class Styles: {ap['class_matches']}")

if __name__ == "__main__":
    inspect_colors()
