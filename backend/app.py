# backend/app.py
import uuid
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

from gemini import generate_image, generate_tags
from logic import apply_vote, build_next_prompt
from storage import save_session, load_session, session_dir

app = FastAPI(title="Alchemy Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------- Models -----------

class StartSessionRequest(BaseModel):
    prompt: str

class VoteRequest(BaseModel):
    session_id: str
    image_id: str
    vote: str  # like / dislike

class NextBatchRequest(BaseModel):
    session_id: str


# ----------- Helpers -----------

def generate_batch(session: dict):
    batch_id = session["current_batch"]
    base_prompt = session["prompt"]
    prompt = build_next_prompt(base_prompt, session["tag_scores"])

    batch_dir = session_dir(session["session_id"]) / f"batch_{batch_id}"
    batch_dir.mkdir(parents=True, exist_ok=True)

    images = []

    for _ in range(4):
        image_id = uuid.uuid4().hex[:8]
        img_path = batch_dir / f"{image_id}.png"

        generate_image(prompt, img_path)
        tags = generate_tags(prompt)

        meta = {
            "image_id": image_id,
            "tags": tags,
            "url": str(img_path)
        }

        (batch_dir / f"{image_id}.json").write_text(json.dumps(meta, indent=2))
        images.append(meta)

    session["current_batch"] += 1
    save_session(session)
    return images


# ----------- Routes -----------

@app.post("/api/session/start")
def start_session(req: StartSessionRequest):
    session_id = uuid.uuid4().hex[:10]

    session = {
        "session_id": session_id,
        "prompt": req.prompt,
        "tag_scores": {},
        "current_batch": 1
    }

    save_session(session)
    images = generate_batch(session)

    return {
        "session_id": session_id,
        "batch": 1,
        "images": images
    }


@app.post("/api/vote")
def vote(req: VoteRequest):
    session = load_session(req.session_id)

    for batch in session_dir(req.session_id).iterdir():
        meta_file = batch / f"{req.image_id}.json"
        if meta_file.exists():
            image = json.loads(meta_file.read_text())
            apply_vote(session["tag_scores"], image["tags"], req.vote)
            save_session(session)
            return {"status": "recorded"}

    raise HTTPException(status_code=404, detail="image not found")


@app.post("/api/session/next")
def next_batch(req: NextBatchRequest):
    session = load_session(req.session_id)
    images = generate_batch(session)
    return {
        "batch": session["current_batch"] - 1,
        "images": images
    }


@app.get("/healthz")
def health():
    return {"ok": True}
