import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent / ".env")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from routes.concepts import router as conceptsRouter
from routes.profiles import router as profilesRouter
from routes.episodes import router as episodesRouter
from routes.chat import router as chatRouter

_embedModel = None

def getEmbedModel():
    global _embedModel
    if _embedModel is None:
        from sentence_transformers import SentenceTransformer
        _embedModel = SentenceTransformer("all-MiniLM-L6-v2")
    return _embedModel


app = FastAPI(title="Total Price of Football API")
app.state.getEmbedModel = getEmbedModel

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(conceptsRouter, prefix="/api")
app.include_router(profilesRouter, prefix="/api")
app.include_router(episodesRouter, prefix="/api")
app.include_router(chatRouter, prefix="/api")


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


@app.get("/api/health")
def health():
    return {"status": "ok"}
