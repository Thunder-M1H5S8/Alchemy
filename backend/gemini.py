from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()

def generate_tags(prompt: str) -> list[str]:
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=(
            "Give exactly 5 short, comma-separated visual tags. "
            "No explanation.\n\n"
            f"{prompt}"
        )
    )

    text = response.text or ""
    return [t.strip().lower() for t in text.split(",") if t.strip()][:5]
