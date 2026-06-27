import os
import re
import ssl
import json
import sys
import subprocess
import urllib.request
import urllib.parse
from datetime import datetime

# Disable SSL verification for macOS Python environment
try:
    ssl._create_default_https_context = ssl._create_unverified_context
except AttributeError:
    pass

def get_video_details(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'tr-TR,tr;q=0.9'
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
        
        # Get Title
        title_match = re.search(r'<title>(.*?) - YouTube</title>', html)
        title = "YouTube Video"
        if title_match:
            import html as html_parser
            title = html_parser.unescape(title_match.group(1))
            
        # Get Upload Date
        date_match = re.search(r'<meta itemprop="uploadDate" content="([^"]+)"', html)
        upload_date = datetime.now().isoformat()
        if date_match:
            upload_date = date_match.group(1)
            
        return title, upload_date
    except Exception as e:
        print(f"Video bilgileri alınırken hata ({video_id}): {e}")
        return f"YouTube Video {video_id}", datetime.now().isoformat()

def clean_transcript_with_gemini(raw_text, api_key):
    print("Metin Gemini ile temizleniyor ve düzenleniyor...")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    prompt = (
        "Aşağıdaki YouTube video transkriptini temizle. Görevin sadece şunlardır:\n"
        "1. Cümleleri mantıklı yerlerden ayırıp nokta, virgül, soru işareti vb. noktalama işaretlerini koymak.\n"
        "2. Kelimelerdeki yazım hatalarını ve Türkçe imla eksikliklerini düzeltmek.\n"
        "3. Metni okumayı kolaylaştıracak şekilde mantıklı paragraflara bölmek.\n"
        "4. Metnin içeriğini, üslubunu, kelimelerini ve anlamını kesinlikle DEĞİŞTİRMEMEK, yeni bilgi eklememek.\n\n"
        f"Transkript Metni:\n{raw_text}"
    )
    
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }
    
    try:
        req = urllib.request.Request(
            url, 
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
        
        cleaned = res_data['candidates'][0]['content']['parts'][0]['text']
        return cleaned
    except Exception as e:
        print(f"Gemini API hatası: {e}")
        return None

def slugify(text):
    text = text.lower()
    # Turkish character translation
    translations = str.maketrans("çğışöüı", "cgisoui")
    text = text.translate(translations)
    # Replace non-alphanumeric with hyphen
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text)
    return text.strip('-')

def clean_vtt_content(vtt_text):
    """Parses WEBVTT subtitle files and extracts clean concatenated text."""
    lines = vtt_text.split('\n')
    text_lines = []
    
    for line in lines:
        line = line.strip()
        # Skip header metadata and timecode lines
        if (not line or 
            line.startswith('WEBVTT') or 
            line.startswith('Kind:') or 
            line.startswith('Language:') or 
            '-->' in line or 
            line.isdigit()):
            continue
            
        # Strip simple HTML formatting like <c> or </c> if present
        line = re.sub(r'<[^>]+>', '', line)
        
        # Remove consecutive duplicate lines (YouTube scrolls captions)
        if not text_lines or text_lines[-1] != line:
            text_lines.append(line)
            
    # Combine lines and clean up whitespace
    full_text = " ".join(text_lines)
    full_text = re.sub(r'\s+', ' ', full_text).strip()
    return full_text

def main():
    print("=" * 60)
    print("           ZİHİN GEZGİNİ YOUTUBE TRANSKRİPT AKTARICI (v3)")
    print("=" * 60)
    
    # Get Gemini API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Gemini API anahtarı bulunamadı.")
        print("Eğer metinlerin imlasını, noktalamasını ve paragraflarını")
        print("otomatik düzeltmek istiyorsanız bir API Anahtarı girin.")
        print("Ücretsiz API anahtarı almak için: https://aistudio.google.com/")
        print("-" * 60)
        api_key = input("Gemini API Anahtarı (Boş bırakmak için Enter'a basın): ").strip()
        
    # Project paths
    tools_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(tools_dir)
    posts_dir = os.path.join(project_dir, 'data', 'posts')
    posts_index_path = os.path.join(project_dir, 'data', 'posts.json')
    raw_dir = os.path.join(project_dir, 'data', 'youtube', 'raw')
    
    os.makedirs(posts_dir, exist_ok=True)
    os.makedirs(raw_dir, exist_ok=True)
    
    # Load current posts.json to avoid duplicates
    existing_posts = []
    if os.path.exists(posts_index_path):
        try:
            with open(posts_index_path, 'r', encoding='utf-8') as f:
                existing_posts = json.load(f)
        except Exception:
            existing_posts = []
            
    existing_slugs = {p['slug'] for p in existing_posts}
    
    # Videos list
    videos = [
        "LPXdm7-FBT0", "EpOmfiMPLqM", "qsoWa7pkrkk", "hhewbiULR4k",
        "iAMNBSGynLA", "3o7nv6CeyCs", "zVJ67mwmwdw", "1cOmOcbMX7c",
        "6QVHkingpis", "nPdeKNPCEKs", "AMo6ECm0Qwk", "HlPQaLJnWug",
        "adGsTP1rYtE", "nJsyHyfeWvs", "42U6gyXUZ-I", "XtqEZR8NfXk"
    ]
    
    # Check yt-dlp path in local venv
    ytdlp_path = os.path.abspath(os.path.join(project_dir, '..', 'venv', 'bin', 'yt-dlp'))
    if not os.path.exists(ytdlp_path):
        # Fallback to system yt-dlp
        ytdlp_path = "yt-dlp"
        
    new_posts_added = 0
    
    # Try different browsers on Mac to fetch active cookies
    browsers = ["safari", "chrome", "firefox", "edge", "brave", "opera", None]
    
    for vid_id in videos:
        print(f"\n[{vid_id}] İşleniyor...")
        
        # Get details
        title, upload_date = get_video_details(vid_id)
        
        # Format slug from title
        clean_title = title.split(" - YouTube")[0].split(" | ")[0]
        # Clean specific prefixes like "Filozoflar Serisi #X" if any
        clean_title = re.sub(r'Filozoflar Serisi\s*#\d+\s*[-|:]?\s*', '', clean_title).strip()
        slug = slugify(clean_title)
        
        if not slug:
            slug = f"video-{vid_id}"
            
        # Check if already exists
        if slug in existing_slugs:
            print(f"-> Atlanıyor (Bu yazı zaten sitede var: '{slug}')")
            continue
            
        print(f"Başlık: {clean_title}")
        print(f"Yükleme Tarihi: {upload_date}")
        
        # Download subtitle using yt-dlp (trying different cookies options to bypass 429)
        vtt_output_pattern = os.path.join(raw_dir, f"{vid_id}")
        vtt_file = None
        
        for browser in browsers:
            cmd = [
                ytdlp_path,
                "--write-auto-subs",
                "--skip-download",
                "--sub-format", "vtt",
                "--sub-lang", "tr",
                "--output", vtt_output_pattern
            ]
            
            if browser:
                print(f"-> {browser.capitalize()} çerezleri ile indirme deneniyor...")
                cmd.extend(["--cookies-from-browser", browser])
            else:
                print("-> Çerezsiz indirme deneniyor...")
                
            cmd.append(f"https://www.youtube.com/watch?v={vid_id}")
            
            # Execute
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Look for the file in raw dir
            temp_file = None
            for filename in os.listdir(raw_dir):
                if filename.startswith(vid_id) and filename.endswith('.vtt'):
                    temp_file = os.path.join(raw_dir, filename)
                    break
                    
            if temp_file and os.path.exists(temp_file):
                vtt_file = temp_file
                print(f"-> Başarılı (Metot: {browser or 'çerezsiz'})!")
                break
            else:
                # If blocked or failed, try next browser
                reason = "Bilinmeyen hata"
                if "HTTP Error 429" in result.stderr or "HTTP Error 429" in result.stdout:
                    reason = "HTTP 429 Too Many Requests (Bloke)"
                elif "Could not find browser" in result.stderr:
                    reason = "Tarayıcı bulunamadı"
                print(f"   Deneme başarısız ({browser or 'çerezsiz'}): {reason}")
                
        if not vtt_file or not os.path.exists(vtt_file):
            print(f"-> HATA: Hiçbir tarayıcı çerezi ile transkript indirilemedi!")
            continue
            
        try:
            with open(vtt_file, 'r', encoding='utf-8') as f:
                vtt_text = f.read()
                
            raw_text = clean_vtt_content(vtt_text)
            print(f"-> Transkript başarıyla ayrıştırıldı ({len(raw_text)} karakter).")
            
            # Clean temporary file
            os.remove(vtt_file)
        except Exception as e:
            print(f"-> Hata (Subtitle okunamadı veya silinemedi: {e})")
            continue
            
        # Clean with Gemini or fallback to basic splitting
        cleaned_text = None
        if api_key:
            cleaned_text = clean_transcript_with_gemini(raw_text, api_key)
            
        if not cleaned_text:
            print("-> Düzeltme yapılmadan ham transkript kaydediliyor.")
            cleaned_text = raw_text
            
        # Format as HTML paragraphs
        paragraphs = cleaned_text.split("\n\n")
        html_content = ""
        for p in paragraphs:
            p_text = p.strip()
            if p_text:
                # Wrap quote blocks if they start with quotation mark or markdown
                if p_text.startswith(">") or p_text.startswith('"') or p_text.startswith('“'):
                    quote_clean = p_text.lstrip("> ").strip('"“’')
                    html_content += f'<blockquote class="wp-block-quote"><p class="wp-block-paragraph"><em>{quote_clean}</em></p></blockquote>\n'
                else:
                    html_content += f'<p class="wp-block-paragraph">{p_text}</p>\n'
                    
        # Add a note with original YouTube link at the end
        html_content += f'\n<hr class="wp-block-separator" />\n<p class="wp-block-paragraph"><em>Bu yazı, Zihin Gezgini YouTube kanalındaki <a href="https://www.youtube.com/watch?v={vid_id}" target="_blank">"{title}"</a> başlıklı videonun transkriptinden derlenmiştir.</em></p>'
        
        # Save JSON post file
        post_json = {
            "title": clean_title,
            "date": upload_date,
            "slug": slug,
            "featuredImage": None,
            "content": html_content,
            "category": "Düşünce"
        }
        
        post_path = os.path.join(posts_dir, f"{slug}.json")
        with open(post_path, 'w', encoding='utf-8') as f:
            json.dump(post_json, f, indent=4, ensure_ascii=False)
            
        # Append to index
        existing_posts.insert(0, {
            "title": clean_title,
            "date": upload_date,
            "slug": slug,
            "featuredImage": None,
            "category": "Düşünce"
        })
        existing_slugs.add(slug)
        new_posts_added += 1
        print(f"-> Başarıyla eklendi: data/posts/{slug}.json")
        
    if new_posts_added > 0:
        # Sort posts by date descending
        existing_posts.sort(key=lambda x: x.get('date', ''), reverse=True)
        with open(posts_index_path, 'w', encoding='utf-8') as f:
            json.dump(existing_posts, f, indent=4, ensure_ascii=False)
        print(f"\nSİTE GÜNCELLENDİ: {new_posts_added} yeni yazı eklendi!")
    else:
        print("\nYeni eklenen yazı bulunmuyor. Tüm yazılar güncel.")

if __name__ == "__main__":
    main()
