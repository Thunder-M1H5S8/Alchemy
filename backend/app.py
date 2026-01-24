# backend/app.py
import uuid
import os
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from pathlib import Path
import json
from datetime import datetime

BASE = Path(__file__).resolve().parent
DATA_DIR = BASE.parent.joinpath("data")
JOBS_DIR = DATA_DIR.joinpath("jobs")
JOBS_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="Hackathon Backend - MVP")

class GenerateRequest(BaseModel):
    prompt: str
    template: str = "insta_square"

def _job_path(job_id: str) -> Path:
    return JOBS_DIR.joinpath(job_id + ".json")

def enqueue_job(prompt: str, template: str) -> str:
    job_id = uuid.uuid4().hex[:12]
    job = {
        "id": job_id,
        "prompt": prompt,
        "template": template,
        "status": "queued",
        "created_at": datetime.utcnow().isoformat(),
        "result": None,
        "error": None
    }
    p = _job_path(job_id)
    p.write_text(json.dumps(job))
    return job_id

