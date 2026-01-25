from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from backend.logic import generate_visual_tags
from backend.image_gen import generate_images


app = FastAPI(title="Alchemy API", version="1.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=3)
    contentType: str | None = None
    count: int = Field(default=3, ge=1, le=6)


class GenerateResponse(BaseModel):
    tags: list[str]
    images: list[str]


@app.post("/generate", response_model=GenerateResponse)
def generate(req: GenerateRequest):
    try:
        tags = generate_visual_tags(req.prompt, req.contentType)
        images = generate_images(req.prompt, tags, req.count)
        return {"tags": tags, "images": images}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))