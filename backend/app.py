import uuid
from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from gemini import generate_tags
from image_gen import generate_image
from logic import apply_vote, build_next_prompt
from storage import save_session, load_session

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class StartReq(BaseModel):
    prompt: str

class VoteReq(BaseModel):
    image_id: str
    liked: bool

def generate_batch(session: dict):
    images = []
    base = session["current_prompt"]
    for i in range(4):
        img_id = uuid.uuid4().hex[:8]
        path = Path(f"data/sessions/{session['id']}_{img_id}.png")
        generate_image(base, path)
        tags = generate_tags(base)
        images.append({
            "id": img_id,
            "path": str(path),
            "tags": tags
        })
    return images

@app.post("/api/session/start")
def start_session(req: StartReq):
    session = {
        "id": uuid.uuid4().hex[:10],
        "base_prompt": req.prompt,
        "current_prompt": req.prompt,
        "tag_scores": {},
        "images": []
    }
    session["images"] = generate_batch(session)
    save_session(session)
    return session

@app.post("/api/session/{sid}/vote")
def vote(sid: str, req: VoteReq):
    session = load_session(sid)
    img = next(i for i in session["images"] if i["id"] == req.image_id)
    apply_vote(session["tag_scores"], img["tags"], req.liked)
    save_session(session)
    return {"ok": True}

@app.post("/api/session/{sid}/next")
def next_batch(sid: str):
    session = load_session(sid)
    session["current_prompt"] = build_next_prompt(
        session["base_prompt"], session["tag_scores"]
    )
    session["images"] = generate_batch(session)
    save_session(session)
    return session
