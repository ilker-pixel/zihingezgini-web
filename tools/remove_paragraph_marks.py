import os
import json

def strip_marks():
    files = [
        "/Users/ilker/.gemini/antigravity-ide/scratch/zihingezgini-web/data/posts/limonun-tarihi-iskorbutu-nasil-yok-etti.json",
        "/Users/ilker/.gemini/antigravity-ide/scratch/zihingezgini-web/data/posts/derinlik-ve-sabir-auteur-sinemasinin-anlami.json"
    ]
    
    for path in files:
        if not os.path.exists(path):
            print(f"File not found: {path}")
            continue
            
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        content = data.get("content", "")
        # Remove <mark> and </mark> tags completely
        cleaned_content = content.replace("<mark>", "").replace("</mark>", "")
        
        # If it was the auteur quote, let's wrap it in blockquote to make it look elegant!
        if "derinlik-ve-sabir" in path:
            cleaned_content = cleaned_content.replace(
                '<p class="has-text-align-justify wp-block-paragraph"><strong><em>Hayatın bir sanat olduğunu kabul eden bir insan beyni, bir süre sonra kalbinin yerini alır. Oscar Wilde</em></strong></p>',
                '<blockquote>"Hayatın bir sanat olduğunu kabul eden bir insan beyni, bir süre sonra kalbinin yerini alır." – Oscar Wilde</blockquote>'
            )
            
        if cleaned_content != content:
            data["content"] = cleaned_content
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"Successfully cleaned marks from: {data.get('title')}")

if __name__ == "__main__":
    strip_marks()
