LIKE_BOOST = 1.0
DISLIKE_PENALTY = 0.7

def apply_vote(tag_scores: dict, tags: list[str], liked: bool):
    for tag in tags:
        tag_scores.setdefault(tag, 1.0)
        if liked:
            tag_scores[tag] += LIKE_BOOST
        else:
            tag_scores[tag] *= DISLIKE_PENALTY

def build_next_prompt(base_prompt: str, tag_scores: dict) -> str:
    top_tags = sorted(tag_scores, key=tag_scores.get, reverse=True)[:3]
    return base_prompt + ", " + ", ".join(top_tags)
