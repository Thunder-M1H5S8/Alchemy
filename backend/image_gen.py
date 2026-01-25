# backend/image_gen.py
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import random

def generate_image(prompt: str, out_path: Path):
    """
    Hackathon-safe fallback image generator.
    Always succeeds. No external APIs.
    """

    # Random dark background (looks intentional)
    bg = (
        random.randint(20, 50),
        random.randint(20, 50),
        random.randint(40, 70),
    )

    img = Image.new("RGB", (1024, 1024), bg)
    draw = ImageDraw.Draw(img)

    text = "AI Image\n\n" + prompt[:120]

    draw.text(
        (60, 400),
        text,
        fill=(220, 220, 220),
    )

    img.save(out_path)
