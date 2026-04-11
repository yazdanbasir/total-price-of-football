import os
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import anthropic
from database import getDB

router = APIRouter()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL = "claude-sonnet-4-6"
TOP_K = 8

SYSTEM_PROMPT = """You are an assistant for "The Price of Football" — a podcast hosted by Kevin Day with Professor Kieran Maguire (University of Liverpool) and occasional guests. The show covers football finance: transfer fees, wages, ownership structures, financial regulations (FFP, PSR, APT), and more.

You answer questions strictly based on transcript excerpts from the podcast provided to you. Do not use any outside knowledge.

Rules:
- Answer only from the provided transcript context
- Always cite your sources by mentioning the episode title and timestamp (formatted as MM:SS, e.g. "at 14:32")
- If the context doesn't contain enough information to answer the question, say so clearly — do not speculate
- Keep answers focused and useful for someone trying to understand football finance
- Do not make up information or fill gaps with general knowledge"""


class ChatRequest(BaseModel):
    message: str


def embeddingToPg(embedding: list) -> str:
    return "[" + ",".join(f"{v:.8f}" for v in embedding) + "]"


def formatTimestamp(seconds) -> str:
    if seconds is None:
        return ""
    s = int(seconds)
    return f"{s // 60:02d}:{s % 60:02d}"


@router.post("/chat")
def chat(req: ChatRequest, request: Request):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    embedModel = request.app.state.embedModel
    embedding = embedModel.encode([req.message.strip()])[0].tolist()
    embeddingStr = embeddingToPg(embedding)

    with getDB() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT c.episode_id, c.text, c.start_time, e.title, e.published_at
            FROM chunks c
            JOIN episodes e ON e.youtube_id = c.episode_id
            ORDER BY c.embedding <=> %s::vector
            LIMIT %s
            """,
            (embeddingStr, TOP_K),
        )
        chunks = cur.fetchall()
        cur.close()

    if not chunks:
        return {"answer": "No relevant podcast content found for your question.", "sources": []}

    contextParts = []
    sources = []
    for episodeID, text, startTime, title, publishedAt in chunks:
        timestamp = formatTimestamp(startTime)
        dateStr = publishedAt.strftime("%Y-%m-%d") if publishedAt else ""
        contextParts.append(f'[Episode: "{title}" ({dateStr}) at {timestamp}]\n{text}')
        sources.append({
            "episodeID": episodeID,
            "title": title,
            "publishedAt": publishedAt.isoformat() if publishedAt else None,
            "timestamp": int(startTime) if startTime else None,
            "timestampFormatted": timestamp,
        })

    context = "\n\n---\n\n".join(contextParts)
    userMessage = f"Context from podcast transcripts:\n\n{context}\n\n---\n\nQuestion: {req.message.strip()}"

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": userMessage}],
    )

    return {
        "answer": response.content[0].text,
        "sources": sources,
    }
