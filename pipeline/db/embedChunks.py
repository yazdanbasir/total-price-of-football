# Chunks all transcripts, generates embeddings, and inserts into the chunks table.
# This powers the RAG chatbot — each chunk is a ~300-word segment of a transcript
# with a vector embedding for semantic similarity search.
# Safe to re-run — clears and repopulates the chunks table each time.
# Requires: DATABASE_URL in pipeline/.env
# Model: all-MiniLM-L6-v2 (384 dimensions, runs locally, no API key needed)

import json
import os
import time
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

load_dotenv(Path(__file__).parent.parent / ".env")

databaseURL = os.getenv("DATABASE_URL")
if not databaseURL:
    raise EnvironmentError("DATABASE_URL not set. Add it to pipeline/.env")

transcriptsDir = Path(__file__).parent.parent / "transcripts"
episodesFile = Path(__file__).parent.parent / "data" / "episodes.json"

CHUNK_SIZE = 300    # target words per chunk
CHUNK_OVERLAP = 50  # words of overlap between chunks
EMBED_MODEL = "all-MiniLM-L6-v2"
EMBED_BATCH = 64    # segments to embed at once

with open(episodesFile) as f:
    episodes = json.load(f)


def chunkSegments(segments: list) -> list[dict]:
    """
    Split transcript segments into overlapping chunks of ~CHUNK_SIZE words.
    Each chunk records the start/end time of its constituent segments.
    """
    chunks = []
    currentWords = []
    currentSegments = []

    for seg in segments:
        words = seg["text"].split()
        currentWords.extend(words)
        currentSegments.append(seg)

        if len(currentWords) >= CHUNK_SIZE:
            chunkText = " ".join(currentWords)
            chunks.append({
                "text": chunkText,
                "startTime": currentSegments[0]["start"],
                "endTime": currentSegments[-1]["end"],
            })
            # Overlap: keep last CHUNK_OVERLAP words worth of segments
            overlapWords = 0
            overlapSegments = []
            for s in reversed(currentSegments):
                overlapWords += len(s["text"].split())
                overlapSegments.insert(0, s)
                if overlapWords >= CHUNK_OVERLAP:
                    break
            currentWords = " ".join(s["text"] for s in overlapSegments).split()
            currentSegments = overlapSegments

    # Flush remaining
    if currentWords:
        chunks.append({
            "text": " ".join(currentWords),
            "startTime": currentSegments[0]["start"],
            "endTime": currentSegments[-1]["end"],
        })

    return chunks


print(f"Loading embedding model: {EMBED_MODEL}...")
model = SentenceTransformer(EMBED_MODEL)
print("Model loaded.\n")

conn = psycopg2.connect(databaseURL)
cur = conn.cursor()

print("Clearing existing chunks...")
cur.execute("DELETE FROM chunks;")
conn.commit()

# Pre-calculate total chunks for the overall progress bar
print("Counting chunks across all episodes...")
episodeChunkCounts = []
for episode in episodes:
    transcriptFile = transcriptsDir / f"{episode['youtubeID']}.json"
    if transcriptFile.exists():
        with open(transcriptFile) as f:
            segments = json.load(f).get("segments", [])
        episodeChunkCounts.append(len(chunkSegments(segments)))
    else:
        episodeChunkCounts.append(0)

totalExpected = sum(episodeChunkCounts)
print(f"Total chunks to embed: ~{totalExpected}\n")

totalChunks = 0
startTime = time.time()

with tqdm(total=len(episodes), desc="Episodes", unit="ep") as episodeBar:
    with tqdm(total=totalExpected, desc="Chunks ", unit="chunk", leave=True) as chunkBar:
        for i, episode in enumerate(episodes):
            youtubeID = episode["youtubeID"]
            title = episode["title"]
            transcriptFile = transcriptsDir / f"{youtubeID}.json"

            if not transcriptFile.exists():
                episodeBar.set_postfix(status="no transcript")
                episodeBar.update(1)
                continue

            with open(transcriptFile) as f:
                transcript = json.load(f)

            segments = transcript.get("segments", [])
            if not segments:
                episodeBar.set_postfix(status="empty")
                episodeBar.update(1)
                continue

            chunks = chunkSegments(segments)
            texts = [c["text"] for c in chunks]
            embeddings = model.encode(texts, batch_size=EMBED_BATCH, show_progress_bar=False)

            for chunk, embedding in zip(chunks, embeddings):
                cur.execute("""
                    INSERT INTO chunks (episode_id, text, start_time, end_time, embedding)
                    VALUES (%s, %s, %s, %s, %s);
                """, (
                    youtubeID,
                    chunk["text"],
                    chunk["startTime"],
                    chunk["endTime"],
                    embedding.tolist(),
                ))

            conn.commit()
            totalChunks += len(chunks)

            elapsed = time.time() - startTime
            rate = totalChunks / elapsed if elapsed > 0 else 0
            remaining = (totalExpected - totalChunks) / rate if rate > 0 else 0

            episodeBar.set_postfix(
                ep=f"{i+1}/{len(episodes)}",
                chunks=len(chunks),
                eta=f"{int(remaining//60)}m{int(remaining%60):02d}s"
            )
            episodeBar.update(1)
            chunkBar.update(len(chunks))

cur.close()
conn.close()

elapsed = time.time() - startTime
print(f"\nDone. {totalChunks} chunks embedded and inserted in {int(elapsed//60)}m{int(elapsed%60):02d}s.")
