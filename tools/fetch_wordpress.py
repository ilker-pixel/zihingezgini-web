import urllib.request
import json
import ssl
import os
import re
from datetime import datetime

# Configuration
SITE_URL = "https://public-api.wordpress.com/wp/v2/sites/zihingezgini.wordpress.com/posts?per_page=100"
DATA_DIR = "/Users/ilker/.gemini/antigravity-ide/scratch/zihingezgini-web/data"
POSTS_DIR = os.path.join(DATA_DIR, "posts")
IMAGES_DIR = "/Users/ilker/.gemini/antigravity-ide/scratch/zihingezgini-web/images"

# Ensure directories exist
os.makedirs(POSTS_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

# SSL context to bypass verification if needed
ctx = ssl._create_unverified_context()

def sanitize_slug(title):
    # Convert Turkish characters
    tr_map = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosucgiosu")
    title = title.translate(tr_map).lower()
    # Remove non-alphanumeric characters, replace spaces with dashes
    slug = re.sub(r'[^a-z0-9\s-]', '', title)
    slug = re.sub(r'[\s-]+', '-', slug).strip('-')
    return slug

def download_image(url, slug):
    if not url:
        return None
    try:
        # Determine file extension
        ext = ".png"
        if ".jpg" in url or ".jpeg" in url:
            ext = ".jpg"
        elif ".gif" in url:
            ext = ".gif"
        elif ".webp" in url:
            ext = ".webp"
            
        filename = f"{slug}{ext}"
        filepath = os.path.join(IMAGES_DIR, filename)
        
        # Download and save
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx) as response, open(filepath, 'wb') as out_file:
            out_file.write(response.read())
        print(f"Downloaded image: {filename}")
        return f"/images/{filename}"
    except Exception as e:
        print(f"Failed to download image {url}: {e}")
        return url # fallback to original URL if download fails

def fetch_and_save():
    req = urllib.request.Request(SITE_URL, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            posts = json.loads(response.read().decode('utf-8'))
            
        posts_index = []
        
        print(f"Processing {len(posts)} posts...")
        for post in posts:
            title = post['title']['rendered']
            # Decode HTML entities in title
            title = html_unescape(title)
            
            date_str = post['date']
            # Format date: e.g. "2025-11-04T15:48:19" to "4 Kasım 2025" or similar in JS, keep ISO string for parsing
            
            slug = post.get('slug') or sanitize_slug(title)
            
            # Content
            content = post['content']['rendered']
            
            # Featured Image (if exists in API)
            featured_media_url = None
            if 'jetpack_featured_media_url' in post and post['jetpack_featured_media_url']:
                featured_media_url = post['jetpack_featured_media_url']
            
            # Categories & Tags
            categories = []
            # We can request terms if needed, but categories/tags are often in JSON.
            # WordPress public API posts have 'categories' as ID list or embedded.
            # Let's check categories if we can map them, otherwise default to "Felsefe" or check tags.
            # A simple regex search for classes in body or categories field
            
            # Let's download featured image
            local_image_path = None
            if featured_media_url:
                local_image_path = download_image(featured_media_url, slug)
            
            # Extract other images inside content and download them too
            img_urls = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', content)
            for idx, img_url in enumerate(img_urls):
                # Ignore tiny icons/gravatars
                if "gravatar.com" in img_url or "s.w.org" in img_url:
                    continue
                local_path = download_image(img_url, f"{slug}-inline-{idx}")
                if local_path:
                    content = content.replace(img_url, local_path)
            
            # Also clean up WordPress block comments and Gutenberg styles if needed
            # For simplicity, keeping content as HTML structure for rich viewing
            
            post_data = {
                "title": title,
                "date": date_str,
                "slug": slug,
                "featuredImage": local_image_path,
                "content": content,
                "category": "Düşünce" # default fallback
            }
            
            # Save single post JSON
            post_filename = f"{slug}.json"
            with open(os.path.join(POSTS_DIR, post_filename), "w", encoding="utf-8") as f:
                json.dump(post_data, f, indent=4, ensure_ascii=False)
                
            # Add to index list (exclude content for lightweight listing)
            posts_index.append({
                "title": title,
                "date": date_str,
                "slug": slug,
                "featuredImage": local_image_path,
                "category": "Düşünce"
            })
            
        # Save posts index
        # Sort index by date descending
        posts_index.sort(key=lambda x: x['date'], reverse=True)
        with open(os.path.join(DATA_DIR, "posts.json"), "w", encoding="utf-8") as f:
            json.dump(posts_index, f, indent=4, ensure_ascii=False)
            
        print("Migration completed successfully!")
        
    except Exception as e:
        print(f"Error during migration: {e}")

def html_unescape(s):
    # Basic HTML unescaping for common characters
    s = s.replace("&nbsp;", " ")
    s = s.replace("&#8217;", "’")
    s = s.replace("&#8216;", "‘")
    s = s.replace("&#8220;", "“")
    s = s.replace("&#8221;", "”")
    s = s.replace("&#8212;", "—")
    s = s.replace("&#8211;", "–")
    s = s.replace("&amp;", "&")
    s = s.replace("&quot;", '"')
    s = s.replace("&#039;", "'")
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    return s

if __name__ == "__main__":
    fetch_and_save()
