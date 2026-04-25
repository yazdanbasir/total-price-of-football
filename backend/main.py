import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent / ".env")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from limiter import limiter
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
app.state.limiter = limiter
app.state.getEmbedModel = getEmbedModel
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

allowedOrigins = [
    o.strip()
    for o in os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")
    if o.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowedOrigins,
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
