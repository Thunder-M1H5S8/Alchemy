# backend/gemini.py
import os
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_tags(prompt: str):
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=f"""
            You are helping generate visual design ideas.

            From this prompt, extract 5 short visual tags
            (1–2 words each).
            Return ONLY comma-separated tags.

            Prompt:
            {prompt}
            """
        )

        tags = [
            t.strip().lower()
            for t in response.text.split(",")
            if t.strip()
        ]
        return tags[:5]

    except Exception:
        # hard fallback – NEVER crash
        return prompt.lower().split()[:5]
