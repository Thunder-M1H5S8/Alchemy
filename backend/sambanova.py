# backend/sambanova.py
import os
from openai import OpenAI

# IMPORTANT:
# export SAMBANOVA_API_KEY="4190ac3c-a2e4-4bdd-9d6f-c1c9f97c9bca"
# NEVER hardcode keys in source files

client = OpenAI(
    api_key=os.getenv("SAMBANOVA_API_KEY"),
    base_url="https://api.sambanova.ai/v1"
)

def generate_tags(prompt: str):
    try:
        response = client.chat.completions.create(
            model="Meta-Llama-3.1-8B-Instruct",  # example SambaNova-supported model
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You help generate visual design ideas. "
                        "Extract exactly 5 short visual tags "
                        "(1–2 words each). "
                        "Return ONLY comma-separated tags."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.3,
            max_tokens=50,
        )

        text = response.choices[0].message.content

        tags = [
            t.strip().lower()
            for t in text.split(",")
            if t.strip()
        ]

        return tags[:5]

    except Exception:
        # hard fallback – NEVER crash
        return prompt.lower().split()[:5]
