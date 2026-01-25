# backend/logic.py
# Extended logic layer – minimal, accurate, production-safe

from backend.deepai import generate_tags

# Small vocabulary for deterministic style grounding
STYLE_HINTS = {
    "instagram": ["square", "bold text", "high contrast"],
    "twitter": ["minimal", "flat", "clean"],
    "linkedin": ["professional", "corporate", "neutral colors"],
    "web": ["responsive", "modern UI", "layout focus"],
}


def normalize_content_type(content_type: str) -> str:
    if not content_type:
        return "generic"
    ct = content_type.lower()
    if "insta" in ct:
        return "instagram"
    if "twitter" in ct or "x" in ct:
        return "twitter"
    if "linkedin" in ct:
        return "linkedin"
    if "web" in ct:
        return "web"
    return "generic"


def extend_prompt(prompt: str, content_type: str | None = None) -> str:
    """
    Light prompt enrichment without hallucination.
    Keeps original user intent intact.
    """
    enriched = prompt.strip()

    key = normalize_content_type(content_type)
    hints = STYLE_HINTS.get(key)

    if hints:
        enriched += ". Visual style: " + ", ".join(hints)

    return enriched


def generate_visual_tags(prompt: str, content_type: str | None = None):
    """
    Core logic used by API layer
    """
    final_prompt = extend_prompt(prompt, content_type)
    tags = generate_tags(final_prompt)

    # Post-process: enforce 1–2 word tags
    clean_tags = []
    for t in tags:
        t = t.strip().lower()
        if 0 < len(t.split()) <= 2:
            clean_tags.append(t)

    return clean_tags[:5]
