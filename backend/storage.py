import json
from pathlib import Path

session_dir = Path("data/sessions")
session_dir.mkdir(parents=True, exist_ok=True)

def save_session(session: dict):
    path = session_dir / f"{session['id']}.json"
    path.write_text(json.dumps(session, indent=2))

def load_session(session_id: str) -> dict:
    path = session_dir / f"{session_id}.json"
    return json.loads(path.read_text())
