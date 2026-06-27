import re
import urllib.request
import json
import ssl

# Bypass SSL certificate verification for macOS Python
ssl._create_default_https_context = ssl._create_unverified_context

def get_channel_videos(channel_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    
    # Force the /videos tab
    if not channel_url.endswith('/videos'):
        channel_url = channel_url.rstrip('/') + '/videos'
        
    req = urllib.request.Request(channel_url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching channel page: {e}")
        return []
        
    # Find ytInitialData JSON in HTML
    pattern = re.compile(r'var ytInitialData\s*=\s*({.+?});\s*</script>')
    match = pattern.search(html)
    if not match:
        # Try another common pattern
        pattern = re.compile(r'window\["ytInitialData"\]\s*=\s*({.+?});')
        match = pattern.search(html)
        
    if not match:
        print("Could not find ytInitialData in HTML. Let's try direct regex search for videoId.")
        # Fallback to direct regex extraction
        video_ids = re.findall(r'"videoId"\s*:\s*"([^"]+)"', html)
        titles = re.findall(r'"title"\s*:\s*\{\s*"runs"\s*:\s*\[\s*\{\s*"text"\s*:\s*"([^"]+)"', html)
        # Deduplicate and zip
        unique_ids = []
        for vid in video_ids:
            if vid not in unique_ids:
                unique_ids.append(vid)
        print(f"Found {len(unique_ids)} unique video IDs via fallback regex.")
        return unique_ids
        
    try:
        data = json.loads(match.group(1))
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        return []
        
    # Let's extract video information from the parsed json data
    # Traverse standard path:
    # data -> contents -> twoColumnBrowseResultsRenderer -> tabs -> [tab index for videos] -> content -> richGridRenderer -> contents
    videos = []
    try:
        tabs = data['contents']['twoColumnBrowseResultsRenderer']['tabs']
        video_tab = None
        for tab in tabs:
            tab_renderer = tab.get('tabRenderer', {})
            if 'videos' in tab_renderer.get('endpoint', {}).get('browseEndpoint', {}).get('params', '').lower() or tab_renderer.get('title', '').lower() in ['videos', 'videolar']:
                video_tab = tab_renderer
                break
        
        # If not found by name, try second tab (usually Videos)
        if not video_tab and len(tabs) > 1:
            video_tab = tabs[1].get('tabRenderer', {})
            
        if video_tab:
            contents = video_tab['content']['richGridRenderer']['contents']
            for item in contents:
                rich_item = item.get('richItemRenderer', {})
                content = rich_item.get('content', {})
                video_renderer = content.get('videoRenderer', {})
                if video_renderer:
                    video_id = video_renderer.get('videoId')
                    title = ""
                    title_runs = video_renderer.get('title', {}).get('runs', [])
                    if title_runs:
                        title = title_runs[0].get('text', '')
                    if video_id and title:
                        videos.append({"id": video_id, "title": title})
    except Exception as e:
        print(f"Error traversing JSON structure: {e}")
        
    # If standard traversal failed or empty, try direct regex on ytInitialData string
    if not videos:
        print("Standard JSON traversal returned empty. Trying regex on ytInitialData string.")
        yt_str = match.group(1)
        video_ids = re.findall(r'"videoId"\s*:\s*"([^"]+)"', yt_str)
        # Let's clean up duplicate IDs
        seen = set()
        unique_ids = []
        for vid in video_ids:
            if vid not in seen:
                seen.add(vid)
                unique_ids.append(vid)
        
        # Let's match titles close to the video IDs
        for vid in unique_ids:
            # Look for video renderer with this ID and extract its title
            # This is a simple approximation
            idx = yt_str.find(vid)
            if idx != -1:
                # Look for title in the surrounding area
                surr = yt_str[idx:idx+2000]
                title_match = re.search(r'"title"\s*:\s*\{\s*"runs"\s*:\s*\[\s*\{\s*"text"\s*:\s*"([^"]+)"', surr)
                title = title_match.group(1) if title_match else "YouTube Video"
                videos.append({"id": vid, "title": title})
                
    return videos

if __name__ == "__main__":
    channel_url = "https://www.youtube.com/@Zihin_Gezgini"
    videos = get_channel_videos(channel_url)
    print(json.dumps(videos, indent=4, ensure_ascii=False))
