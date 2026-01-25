# backend/app.py
import uuid
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from dotenv import load_dotenv
load_dotenv()

from gemini import generate_tags
from image_gen import generate_image
from logic import apply_vote, build_next_prompt
from storage import save_session, load_session


DATA_DIR = Path("data/sessions")
DATA_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="Alchemy Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Models ----------

class StartRequest(BaseModel):
    prompt: str

class VoteRequest(BaseModel):
    image_id: str
    vote: str  # like / dislike

# ---------- Helpers ----------

def generate_batch(session: dict):
    images = []

    for _ in range(4):
        img_id = uuid.uuid4().hex[:8]
        path = DATA_DIR / f"{session['id']}_{img_id}.png"

        generate_image(session["current_prompt"], path)
        tags = generate_tags(session["current_prompt"])

        images.append({
            "id": img_id,
            "path": str(path),
            "tags": tags
        })

    return images

# ---------- Routes ----------

@app.post("/api/session/start")
def start_session(req: StartRequest):
    session_id = uuid.uuid4().hex[:10]

    session = {
        "id": session_id,
        "base_prompt": req.prompt,
        "current_prompt": req.prompt,
        "tag_scores": {},
        "images": []
    }

    session["images"] = generate_batch(session)
    save_session(session)
    return session


@app.post("/api/session/{session_id}/vote")
def vote(session_id: str, req: VoteRequest):
    session = load_session(session_id)

    apply_vote(session, req.image_id, req.vote)
    session["current_prompt"] = build_next_prompt(session)
    session["images"] = generate_batch(session)

    save_session(session)
    return session


@app.get("/healthz")
def health():
    return {"ok": True}
