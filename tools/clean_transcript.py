import urllib.request
import json
import ssl
import os
import sys

def clean_transcript(input_file, api_key):
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        return False
        
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            raw_text = f.read()
            
        print(f"Read {len(raw_text)} characters of raw transcript. Sending to Gemini...")
        
        # Prepare API call
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        ctx = ssl._create_unverified_context()
        
        prompt = (
            "Aşağıdaki YouTube video transkriptini temizle. Görevin sadece şunlardır:\n"
            "1. Cümleleri mantıklı yerlerden ayırıp nokta, virgül, soru işareti vb. noktalama işaretlerini koymak.\n"
            "2. Kelimelerdeki yazım hatalarını ve imla eksikliklerini düzeltmek.\n"
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
        
        req = urllib.request.Request(
            url, 
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        with urllib.request.urlopen(req, context=ctx) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            
        # Parse response
        try:
            cleaned_text = res_data['candidates'][0]['content']['parts'][0]['text']
        except (KeyError, IndexError) as e:
            print(f"Failed to parse Gemini API response: {e}")
            print(f"Response: {res_data}")
            return False
            
        # Save output
        dir_name = os.path.dirname(input_file)
        base_name = os.path.basename(input_file)
        name, ext = os.path.splitext(base_name)
        output_file = os.path.join(dir_name, f"{name}-temizlenmis{ext}")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(cleaned_text)
            
        print(f"Cleaned transcript saved successfully to: {output_file}")
        return True
        
    except Exception as e:
        print(f"Error during transcript cleaning: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanım: python clean_transcript.py <transkript_dosya_yolu> [GEMINI_API_KEY]")
        print("Not: GEMINI_API_KEY çevre değişkeni olarak tanımlıysa parametreye gerek yoktur.")
        sys.exit(1)
        
    input_path = sys.argv[1]
    
    # Get API key from argument or environment variable
    api_key = sys.argv[2] if len(sys.argv) > 2 else os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        print("Hata: Gemini API Anahtarı bulunamadı. Lütfen parametre olarak girin veya GEMINI_API_KEY çevre değişkenini ayarlayın.")
        sys.exit(1)
        
    clean_transcript(input_path, api_key)
