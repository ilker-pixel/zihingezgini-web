import json
import re

def inject_quotes():
    app_js_path = "/Users/ilker/.gemini/antigravity-ide/scratch/zihingezgini-web/app.js"
    mapped_quotes_path = "/Users/ilker/.gemini/antigravity-ide/scratch/zihingezgini-web/tools/mapped_quotes_100.json"
    
    with open(mapped_quotes_path, "r", encoding="utf-8") as f:
        quotes = json.load(f)
        
    # Format the quotes list as formatted JS code
    js_quotes_lines = []
    for q in quotes:
        # Escape any single quotes in text or title
        text = q["text"].replace('"', '\\"')
        title = q["title"].replace('"', '\\"')
        slug = q["slug"]
        js_quotes_lines.append(f'      {{ text: "{text}", author: "Zihin Gezgini", title: "{title}", slug: "{slug}" }}')
        
    js_quotes_block = "    const quotes = [\n" + ",\n".join(js_quotes_lines) + "\n    ];"
    
    with open(app_js_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # We want to replace the existing quotes block.
    # It starts with "const quotes = [" and ends with "];" inside setupQuoteWidget
    # Let's locate setupQuoteWidget and replace the quotes array
    pattern = r'(const quotes = \[\s*\{.*?\}\s*\];)'
    # Since the match could span multiple lines, let's use regex with DOTALL flag
    match = re.search(r'const quotes = \[\s*\{.*?\n\s*\}\s*\];', content, re.DOTALL)
    if not match:
        print("Error: Could not find quotes block in app.js using simple pattern. Trying fallback.")
        # Try a more general search for the quotes block inside setupQuoteWidget
        match = re.search(r'function setupQuoteWidget\(\)\s*\{\s*const widget =.*?\s*const quotes = \[\s*.*?\s*\];', content, re.DOTALL)
        if not match:
            print("Failed to find block.")
            return
            
    # Clean replacement targeting the specific const quotes block
    content_new = re.sub(r'const quotes = \[\s*\{.*?\n\s*\}\s*\];', js_quotes_block, content, flags=re.DOTALL)
    
    with open(app_js_path, "w", encoding="utf-8") as f:
        f.write(content_new)
        
    print("Injected quotes successfully into app.js.")

if __name__ == "__main__":
    inject_quotes()
