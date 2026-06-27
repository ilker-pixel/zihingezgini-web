import os
import re
import ssl
import json
import urllib.request
from youtube_transcript_api import YouTubeTranscriptApi

ssl._create_default_https_context = ssl._create_unverified_context

def get_video_title(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
        title_match = re.search(r'<title>(.*?) - YouTube</title>', html)
        if title_match:
            title = title_match.group(1)
            # Decode HTML entities if any
            import html as html_parser
            title = html_parser.unescape(title)
            return title
    except Exception as e:
        print(f"Error fetching title for {video_id}: {e}")
    return f"YouTube Video {video_id}"

def fetch_and_save_transcripts(video_list, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'raw'), exist_ok=True)
    
    api = YouTubeTranscriptApi()
    
    metadata_path = os.path.join(output_dir, 'metadata.json')
    if os.path.exists(metadata_path):
        try:
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
        except Exception:
            metadata = {}
    else:
        metadata = {}

    results = []
    
    for vid_id in video_list:
        print(f"\nProcessing video: {vid_id}...")
        
        # Get title
        title = get_video_title(vid_id)
        print(f"Title: {title}")
        
        # Check if already fetched
        raw_file_path = os.path.join(output_dir, 'raw', f"{vid_id}.txt")
        transcript_text = ""
        
        if os.path.exists(raw_file_path):
            print(f"Raw transcript already exists locally at {raw_file_path}")
            with open(raw_file_path, 'r', encoding='utf-8') as f:
                transcript_text = f.read()
            status = "fetched"
        else:
            try:
                # Try getting Turkish transcript
                transcript_list = api.list(vid_id)
                
                # Try to find Turkish transcript first (manually created or auto)
                try:
                    transcript = transcript_list.find_transcript(['tr'])
                except Exception:
                    # If not found, try to find any transcript and translate to Turkish
                    try:
                        transcript = transcript_list.find_transcript(['en']).translate('tr')
                    except Exception:
                        # Grab whatever is available
                        transcript = transcript_list.find_generated_transcript(['tr'])
                
                transcript_data = transcript.fetch()
                transcript_text = " ".join([item['text'] for item in transcript_data])
                
                with open(raw_file_path, 'w', encoding='utf-8') as f:
                    f.write(transcript_text)
                
                print(f"Fetched and saved raw transcript ({len(transcript_text)} characters)")
                status = "fetched"
            except Exception as e:
                print(f"Could not retrieve transcript for {vid_id}: {e}")
                status = f"failed: {str(e)}"
        
        metadata[vid_id] = {
            "id": vid_id,
            "title": title,
            "status": status,
            "char_count": len(transcript_text) if transcript_text else 0,
            "url": f"https://www.youtube.com/watch?v={vid_id}"
        }
        
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)
        
    print(f"\nMetadata updated at {metadata_path}")

if __name__ == "__main__":
    # Video list extracted in the previous step
    video_list = [
        "LPXdm7-FBT0", "EpOmfiMPLqM", "qsoWa7pkrkk", "hhewbiULR4k",
        "iAMNBSGynLA", "3o7nv6CeyCs", "zVJ67mwmwdw", "1cOmOcbMX7c",
        "6QVHkingpis", "nPdeKNPCEKs", "AMo6ECm0Qwk", "HlPQaLJnWug",
        "adGsTP1rYtE", "nJsyHyfeWvs", "42U6gyXUZ-I", "XtqEZR8NfXk"
    ]
    
    output_dir = "/Users/ilker/.gemini/antigravity-ide/scratch/zihingezgini-web/data/youtube"
    fetch_and_save_transcripts(video_list, output_dir)
