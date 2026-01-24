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

@app.post("/api/generate", status_code=202)
async def generate(req: GenerateRequest, background_tasks: BackgroundTasks):
    job_id = enqueue_job(req.prompt, req.template)
    # Schedule background placeholder worker (quick demo safe fallback)
    background_tasks.add_task(run_placeholder_worker, job_id)
    return {"job_id": job_id, "status": "queued"}

@app.get("/api/status/{job_id}")
async def status(job_id: str):
    p = _job_path(job_id)
    if not p.exists():
        raise HTTPException(status_code=404, detail="job not found")
    job = json.loads(p.read_text())
    return job

@app.get("/healthz")
async def health():
    return {"ok": True}
    
# Simple placeholder worker that creates a PNG with prompt text
def run_placeholder_worker(job_id: str):
    try:
        p = _job_path(job_id)
        job = json.loads(p.read_text())
        job["status"] = "started"
        p.write_text(json.dumps(job))
        # create an image file with Pillow
        from PIL import Image, ImageDraw, ImageFont
        out_dir = JOBS_DIR.joinpath(job_id)
        out_dir.mkdir(exist_ok=True)
        img_path = out_dir.joinpath("preview.png")
        img = Image.new("RGB", (1080,1080), color=(240,240,240))
        draw = ImageDraw.Draw(img)
        text = job["prompt"][:200]
        try:
            font = ImageFont.load_default()
        except:
            font = None
        draw.text((40,40), text, fill=(20,20,20), font=font)
        img.save(img_path)
        job["status"] = "done"
        job["result"] = {"preview": str(img_path)}
        p.write_text(json.dumps(job))
    except Exception as e:
        job = {"id": job_id, "status": "failed", "error": str(e)}
        _job_path(job_id).write_text(json.dumps(job))