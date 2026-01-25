# backend/storage.py
import json
from pathlib import Path

SESSION_DIR = Path("data/sessions")
SESSION_DIR.mkdir(parents=True, exist_ok=True)

def _path(session_id: str):
    return SESSION_DIR / f"{session_id}.json"

def save_session(session: dict):
    _path(session["id"]).write_text(json.dumps(session, indent=2))

def load_session(session_id: str):
    path = _path(session_id)
    if not path.exists():
        raise FileNotFoundError("Session not found")
    return json.loads(path.read_text())
