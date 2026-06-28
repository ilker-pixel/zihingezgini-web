import os
import hashlib
from PIL import Image

def analyze_images():
    img_dir = "/Users/ilker/.gemini/antigravity-ide/scratch/zihingezgini-web/images"
    files = [
        "frommun-dusunceleri-uzerine.webp",
        "frommun-dusunceleri-uzerine-inline-0.webp",
        "frommun-dusunceleri-uzerine-inline-1.webp",
        "frommun-dusunceleri-uzerine-inline-2.webp",
        "frommun-dusunceleri-uzerine-inline-3.webp"
    ]
    
    for f in files:
        path = os.path.join(img_dir, f)
        if not os.path.exists(path):
            print(f"{f}: Not found")
            continue
        img = Image.open(path)
        # Get md5 of image content
        with open(path, "rb") as fh:
            h = hashlib.md5(fh.read()).hexdigest()
        print(f"{f}: size={img.size}, format={img.format}, md5={h}")

if __name__ == "__main__":
    analyze_images()
