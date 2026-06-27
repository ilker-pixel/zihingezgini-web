import os
import json
from datetime import datetime

def main():
    project_dir = "/Users/ilker/.gemini/antigravity-ide/scratch/zihingezgini-web"
    index_path = os.path.join(project_dir, "data", "posts.json")
    sitemap_path = os.path.join(project_dir, "sitemap.xml")
    
    # Read the posts
    with open(index_path, "r", encoding="utf-8") as f:
        posts = json.load(f)
        
    sitemap_content = []
    sitemap_content.append('<?xml version="1.0" encoding="UTF-8"?>')
    sitemap_content.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    # Add homepage
    sitemap_content.append('  <url>')
    sitemap_content.append('    <loc>https://zihingezgini.net/</loc>')
    sitemap_content.append('    <changefreq>daily</changefreq>')
    sitemap_content.append('    <priority>1.0</priority>')
    sitemap_content.append('  </url>')
    
    # Add about page
    sitemap_content.append('  <url>')
    sitemap_content.append('    <loc>https://zihingezgini.net/#/about</loc>')
    sitemap_content.append('    <changefreq>monthly</changefreq>')
    sitemap_content.append('    <priority>0.8</priority>')
    sitemap_content.append('  </url>')
    
    # Add each post
    for post in posts:
        slug = post.get("slug")
        date_str = post.get("date", "")
        
        # Format date for sitemap (YYYY-MM-DD)
        if date_str:
            try:
                dt = datetime.fromisoformat(date_str)
                formatted_date = dt.strftime("%Y-%m-%d")
            except Exception:
                formatted_date = date_str[:10]
        else:
            formatted_date = datetime.now().strftime("%Y-%m-%d")
            
        sitemap_content.append('  <url>')
        sitemap_content.append(f'    <loc>https://zihingezgini.net/#/post/{slug}</loc>')
        sitemap_content.append(f'    <lastmod>{formatted_date}</lastmod>')
        sitemap_content.append('    <changefreq>monthly</changefreq>')
        sitemap_content.append('    <priority>0.7</priority>')
        sitemap_content.append('  </url>')
        
    sitemap_content.append('</urlset>')
    
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write("\n".join(sitemap_content))
        
    print(f"Generated sitemap with {len(posts)} posts at {sitemap_path}")

if __name__ == "__main__":
    main()
