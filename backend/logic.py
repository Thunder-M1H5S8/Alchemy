# backend/logic.py

LIKE_BOOST = 1.0
DISLIKE_PENALTY = -0.7


def apply_vote(tag_scores: dict, tags: list[str], vote: str):
    """
    Update tag scores based on user feedback.
    """
    if vote not in ("like", "dislike"):
        return

    delta = LIKE_BOOST if vote == "like" else DISLIKE_PENALTY

    for tag in tags:
        tag_scores[tag] = tag_scores.get(tag, 0.0) + delta


def build_next_prompt(base_prompt: str, tag_scores: dict) -> str:
    """
    Build the next generation prompt by reinforcing high-scoring tags.
    """
    if not tag_scores:
        return base_prompt

    sorted_tags = sorted(
        tag_scores.items(),
        key=lambda x: x[1],
        reverse=True,
    )

    strong_tags = [tag for tag, score in sorted_tags if score > 0][:4]

    if not strong_tags:
        return base_prompt

    return base_prompt + ", " + ", ".join(strong_tags)
