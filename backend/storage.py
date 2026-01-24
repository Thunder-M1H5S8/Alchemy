# backend/storage.py
import json
from pathlib import Path

# Base data directory
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "sessions"

# Ensure directory exists
DATA_DIR.mkdir(parents=True, exist_ok=True)


def session_dir(session_id: str) -> Path:
    """
    Return the directory path for a session.
    """
    return DATA_DIR / session_id


def save_session(session: dict):
    """
    Save session metadata to disk.
    """
    sdir = session_dir(session["session_id"])
    sdir.mkdir(parents=True, exist_ok=True)

    path = sdir / "session.json"
    path.write_text(json.dumps(session, indent=2))


def load_session(session_id: str) -> dict:
    """
    Load session metadata from disk.
    """
    path = session_dir(session_id) / "session.json"

    if not path.exists():
        raise FileNotFoundError(f"Session {session_id} not found")

    return json.loads(path.read_text())
