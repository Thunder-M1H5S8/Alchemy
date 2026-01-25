# backend/image_gen.py
from PIL import Image, ImageDraw
from pathlib import Path

def generate_image(prompt: str, out_path: Path):
    img = Image.new("RGB", (1024, 1024), (250, 250, 250))
    draw = ImageDraw.Draw(img)

    # header bar
    draw.rectangle((0, 0, 1024, 160), fill=(30, 30, 30))
    draw.text((40, 60), "Alchemy Preview", fill=(255, 255, 255))

    # prompt preview
    draw.rectangle((0, 860, 1024, 1024), fill=(20, 20, 20))
    draw.text((40, 900), prompt[:120], fill=(255, 255, 255))

    img.save(out_path)
