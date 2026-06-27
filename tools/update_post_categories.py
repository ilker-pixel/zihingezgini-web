import os
import json

def main():
    project_dir = "/Users/ilker/.gemini/antigravity-ide/scratch/zihingezgini-web"
    index_path = os.path.join(project_dir, "data", "posts.json")
    posts_dir = os.path.join(project_dir, "data", "posts")
    
    # Read the posts index
    with open(index_path, "r", encoding="utf-8") as f:
        posts = json.load(f)
        
    print(f"Loaded {len(posts)} posts from index.")
    
    updated_count = 0
    # Process each post in the index
    for post in posts:
        slug = post.get("slug")
        category = post.get("category")
        
        if not slug or not category:
            continue
            
        post_file_path = os.path.join(posts_dir, f"{slug}.json")
        if os.path.exists(post_file_path):
            # Read the individual post JSON
            with open(post_file_path, "r", encoding="utf-8") as f:
                post_data = json.load(f)
                
            # Update the category if it changed
            if post_data.get("category") != category:
                post_data["category"] = category
                
                # Write it back
                with open(post_file_path, "w", encoding="utf-8") as f:
                    json.dump(post_data, f, ensure_ascii=False, indent=4)
                
                print(f"Updated category for post '{slug}' to '{category}'")
                updated_count += 1
        else:
            print(f"Warning: Post file not found: {post_file_path}")
            
    print(f"Successfully updated {updated_count} individual post files.")

if __name__ == "__main__":
    main()
