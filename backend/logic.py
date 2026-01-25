# backend/logic.py

LIKE_BOOST = 1.0
DISLIKE_PENALTY = 0.7

def apply_vote(session: dict, image_id: str, vote: str):
    image = next(img for img in session["images"] if img["id"] == image_id)

    for tag in image["tags"]:
        session["tag_scores"].setdefault(tag, 0)

        if vote == "like":
            session["tag_scores"][tag] += LIKE_BOOST
        else:
            session["tag_scores"][tag] -= DISLIKE_PENALTY


def build_next_prompt(session: dict):
    base = session["base_prompt"]

    sorted_tags = sorted(
        session["tag_scores"].items(),
        key=lambda x: x[1],
        reverse=True
    )

    top_tags = [t for t, score in sorted_tags[:3] if score > 0]

    if not top_tags:
        return base

    return base + ", " + ", ".join(top_tags)
