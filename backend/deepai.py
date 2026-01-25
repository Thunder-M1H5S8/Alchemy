import os
import requests

DEEPAI_TEXT_URL = "https://api.deepai.org/api/text-generator"
DEEPAI_IMAGE_URL = "https://api.deepai.org/api/text2img"

def _headers():
    api_key = os.getenv("DEEPAI_API_KEY")
    if not api_key:
        raise RuntimeError("DEEPAI_API_KEY not set")
    return {"api-key": api_key}


def generate_tags(prompt: str) -> list[str]:
    """
    Use DeepAI text generator to extract visual tags
    """
    response = requests.post(
        DEEPAI_TEXT_URL,
        headers=_headers(),
        data={"text": f"Generate 5 short visual design tags: {prompt}"}
    )

    response.raise_for_status()
    text = response.json().get("output", "")

    tags = [
        t.strip().lower()
        for t in text.replace("\n", ",").split(",")
        if t.strip()
    ]

    return tags[:5]


def generate_images(prompt: str, count: int = 3) -> list[str]:
    """
    Generate images using DeepAI text2img
    """
    images = []

    for _ in range(count):
        res = requests.post(
            DEEPAI_IMAGE_URL,
            headers=_headers(),
            data={"text": prompt}
        )
        res.raise_for_status()
        images.append(res.json()["output_url"])

    return images
