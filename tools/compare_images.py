import os
from PIL import Image, ImageChops

def compare_images():
    img_dir = "/Users/ilker/.gemini/antigravity-ide/scratch/zihingezgini-web/images"
    featured = Image.open(os.path.join(img_dir, "frommun-dusunceleri-uzerine.webp")).convert("RGB")
    
    inlines = [
        "frommun-dusunceleri-uzerine-inline-0.webp",
        "frommun-dusunceleri-uzerine-inline-1.webp",
        "frommun-dusunceleri-uzerine-inline-2.webp",
        "frommun-dusunceleri-uzerine-inline-3.webp"
    ]
    
    for inf in inlines:
        path = os.path.join(img_dir, inf)
        if not os.path.exists(path):
            continue
        img = Image.open(path).convert("RGB")
        if img.size != featured.size:
            print(f"{inf} size mismatch: {img.size} vs {featured.size}")
            continue
        diff = ImageChops.difference(featured, img)
        bbox = diff.getbbox()
        if bbox is None:
            print(f"EXACT MATCH: featured is identical to {inf}")
        else:
            # Calculate sum of differences
            diff_sum = sum(sum(pixel) for pixel in diff.getdata())
            print(f"{inf} pixel diff sum = {diff_sum}")

if __name__ == "__main__":
    compare_images()
