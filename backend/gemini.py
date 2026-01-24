# backend/gemini.py
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

# Load environment variables from .env if present
load_dotenv()

# Create Gemini client
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY not found. "
        "Set it in PowerShell or add it to a .env file."
    )

client = genai.Client(api_key=API_KEY)


def generate_tags(prompt: str) -> list[str]:
    """
    Generate 3–5 concise visual tags for an image prompt using Gemini text model.
    """
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=(
            "Give 5 short, comma-separated visual tags for this image idea. "
            "No explanations.\n\n"
            f"{prompt}"
        ),
    )

    text = response.text or ""
    return [
        tag.strip().lower()
        for tag in text.split(",")
        if tag.strip()
    ][:5]


def generate_image(prompt: str, out_path: Path):
    """
    Generate an image using Imagen via Gemini and save it to out_path.
    """
    response = client.models.generate_images(
        model="imagen-3.0-generate-002",
        prompt=prompt,
    )

    image_bytes = response.generated_images[0].image.image_bytes
    out_path.write_bytes(image_bytes)
