import os
from PIL import Image

def make_logo_transparent():
    image_path = "/Users/ilker/.gemini/antigravity-ide/scratch/zihingezgini-web/images/zihin_gezgini_logo_sketch.png"
    if not os.path.exists(image_path):
        print(f"Error: Image not found at {image_path}")
        return
        
    img = Image.open(image_path)
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        r, g, b, a = item
        # Calculate brightness (average of RGB)
        brightness = (r + g + b) / 3.0
        
        # Threshold for transparency: anything lighter than 235 brightness becomes transparent
        if brightness > 235:
            newData.append((255, 255, 255, 0))
        else:
            # Map the alpha channel smoothly based on darkness to preserve sketch gradient/antialiasing
            # Anything darker than 235 gets progressive alpha
            alpha = int(max(0, min(255, 255 * (235.0 - brightness) / 235.0)))
            
            # Keep the dark grey/black pencil line colors but make background transparent
            newData.append((r, g, b, alpha))

    img.putdata(newData)
    img.save(image_path, "PNG")
    print("Success: Made logo background transparent while keeping graphite lines!")

if __name__ == "__main__":
    make_logo_transparent()
