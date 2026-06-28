import os
import re
import json

def find_duplicates():
    posts_dir = "/Users/ilker/.gemini/antigravity-ide/scratch/zihingezgini-web/data/posts"
    img_dir = "/Users/ilker/.gemini/antigravity-ide/scratch/zihingezgini-web/images"
    
    if not os.path.exists(posts_dir):
        print("Error: posts directory not found")
        return
        
    post_files = [f for f in os.listdir(posts_dir) if f.endswith(".json")]
    print(f"Total posts found: {len(post_files)}")
    
    duplicates_found = []
    
    for pf in post_files:
        path = os.path.join(posts_dir, pf)
        with open(path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except Exception as e:
                print(f"Error loading {pf}: {e}")
                continue
                
        featured = data.get("featuredImage")
        content = data.get("content", "")
        slug = data.get("slug")
        
        if not featured or not content:
            continue
            
        # Find first image src in content HTML
        img_match = re.search(r'<img\s+[^>]*src="([^"]+)"', content)
        if img_match:
            first_inline = img_match.group(1)
            
            # Extract basenames
            feat_base = os.path.basename(featured)
            inline_base = os.path.basename(first_inline)
            
            # Simple check: do they share the same base slug?
            # Or is first inline named slug-inline-0?
            is_possible_dup = False
            
            # Check size similarity or naming convention
            feat_img_path = os.path.join(img_dir, feat_base)
            inline_img_path = os.path.join(img_dir, inline_base)
            
            if os.path.exists(feat_img_path) and os.path.exists(inline_img_path):
                # If they are exactly the same size in bytes, or if the filenames indicate duplication
                feat_size = os.path.getsize(feat_img_path)
                inline_size = os.path.getsize(inline_img_path)
                
                # Check naming convention (e.g. frommun-dusunceleri-uzerine.webp and frommun-dusunceleri-uzerine-inline-0.webp)
                # Remove extension and check if one is a prefix of the other with "inline-0"
                feat_name = os.path.splitext(feat_base)[0]
                inline_name = os.path.splitext(inline_base)[0]
                
                # If the featured image name is a prefix of the inline image name
                # (e.g. "frommun-dusunceleri-uzerine" is in "frommun-dusunceleri-uzerine-inline-0")
                if inline_name == f"{feat_name}-inline-0" or inline_name == f"{feat_name}-inline-1" or feat_name == inline_name:
                    is_possible_dup = True
                # Or if sizes are very close (within 10%) and they share the slug name
                elif slug in feat_name and slug in inline_name and abs(feat_size - inline_size) / max(1, feat_size) < 0.3:
                    is_possible_dup = True
            
            if is_possible_dup:
                duplicates_found.append({
                    "post_file": pf,
                    "title": data.get("title"),
                    "featured": featured,
                    "first_inline": first_inline,
                    "img_match_tag": img_match.group(0)
                })
                
    print(f"\nPotential duplicate images found in {len(duplicates_found)} posts:")
    for d in duplicates_found:
        print(f"\n- Title: {d['title']} ({d['post_file']})")
        print(f"  Featured: {d['featured']}")
        print(f"  First Inline: {d['first_inline']}")
        
    # Write report of duplicates
    with open("tools/duplicates_report.json", "w", encoding="utf-8") as f:
        json.dump(duplicates_found, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    find_duplicates()
