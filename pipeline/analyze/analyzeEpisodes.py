# Analyzes each episode transcript using Claude Haiku.
# Extracts financial concepts, directory profiles, and news stories with timestamps.
# Outputs one JSON file per episode to pipeline/analysis/{youtubeID}.json.
# Safe to pause and re-run — already analyzed episodes are skipped.
# Requires: ANTHROPIC_API_KEY in pipeline/.env

import json
import os
import time
from pathlib import Path

import anthropic
from dotenv import load_dotenv
from json_repair import repair_json

load_dotenv(Path(__file__).parent.parent / ".env")

transcriptsDir = Path(__file__).parent.parent / "transcripts"
analysisDir = Path(__file__).parent.parent / "analysis"
episodesFile = Path(__file__).parent.parent / "data" / "episodes.json"
logFile = Path(__file__).parent.parent / "data" / "analysisLog.json"
analysisDir.mkdir(parents=True, exist_ok=True)

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise EnvironmentError("ANTHROPIC_API_KEY not set. Add it to pipeline/.env")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
MODEL = "claude-haiku-4-5-20251001"

SYSTEM_PROMPT = """You are analyzing transcripts of "The Price of Football" podcast, hosted by Kevin Day alongside Professor Kieran Maguire (University of Liverpool) and occasional guests. The show covers football finance news: transfer fees, wages, ownership structures, financial regulations (FFP, PSR, APT), league finances, and more.

Your task is to extract structured data from a transcript segment. Return ONLY valid JSON — no commentary, no markdown, no code fences.

Extract the following:

1. **concepts** — financial or regulatory terms explained or defined on this episode. Include terms where the show gives a meaningful explanation, even partial. Be thorough — include every term that gets any explanation.
   - term: the term or phrase
   - definition: a 1–3 sentence explanation derived from what was said on the show
   - timestamps: array of seconds (integers) where the term is meaningfully discussed

2. **profiles** — people, football clubs, organisations, or regulatory bodies that are meaningfully discussed (not just briefly name-dropped).
   - name: full name
   - type: one of "person", "club", "organisation", "body"
   - description: 1–2 sentence description of who/what they are and their relevance to football finance, based on the episode
   - timestamps: array of seconds (integers) where they are meaningfully discussed

3. **stories** — distinct news stories or topics covered in this episode
   - headline: short headline (max 10 words)
   - summary: 2–4 sentence summary of what was discussed
   - timestamp: integer seconds where this story begins

Return this exact JSON structure:
{
  "concepts": [...],
  "profiles": [...],
  "stories": [...]
}"""


def formatTranscript(segments: list) -> str:
    """Format segments as a timestamped transcript for the model."""
    lines = []
    for seg in segments:
        mins = int(seg["start"]) // 60
        secs = int(seg["start"]) % 60
        lines.append(f"[{mins:02d}:{secs:02d}] {seg['text']}")
    return "\n".join(lines)


def parseResponse(rawText: str) -> dict:
    """Parse model response as JSON, falling back to json_repair on failure."""
    rawText = rawText.strip()

    # Strip markdown code fences if present
    if rawText.startswith("```"):
        rawText = rawText.split("```")[1]
        if rawText.startswith("json"):
            rawText = rawText[4:]
    rawText = rawText.strip()

    try:
        return json.loads(rawText)
    except json.JSONDecodeError:
        repaired = repair_json(rawText)
        return json.loads(repaired)


def analyzeEpisode(episode: dict, transcript: dict, retry: bool = False) -> dict:
    """Send transcript to Claude Haiku and return extracted structured data."""
    formattedTranscript = formatTranscript(transcript["segments"])

    userMessage = f"""Episode: {episode['title']}
Published: {episode['publishedAt'][:10]}

Transcript:
{formattedTranscript}"""

    messages = [{"role": "user", "content": userMessage}]

    # On retry, prime the assistant with the opening brace to force clean JSON
    if retry:
        messages.append({"role": "assistant", "content": "{"})

    response = client.messages.create(
        model=MODEL,
        max_tokens=8192,
        system=SYSTEM_PROMPT,
        messages=messages,
    )

    rawText = response.content[0].text.strip()
    if retry:
        rawText = "{" + rawText

    return parseResponse(rawText)


with open(episodesFile) as f:
    episodes = json.load(f)

failed = []
skipped = []
total = len(episodes)

print(f"Analyzing {total} episodes with {MODEL}...\n")

for i, episode in enumerate(episodes, 1):
    youtubeID = episode["youtubeID"]
    title = episode["title"]
    outputFile = analysisDir / f"{youtubeID}.json"

    if outputFile.exists():
        print(f"[{i}/{total}] Skipping (already analyzed): {title}")
        skipped.append(youtubeID)
        continue

    transcriptFile = transcriptsDir / f"{youtubeID}.json"
    if not transcriptFile.exists():
        print(f"[{i}/{total}] SKIPPED (no transcript): {title}")
        failed.append({"youtubeID": youtubeID, "title": title, "reason": "transcript not found"})
        continue

    with open(transcriptFile) as f:
        transcript = json.load(f)

    print(f"[{i}/{total}] Analyzing: {title}")
    startTime = time.time()

    try:
        try:
            extracted = analyzeEpisode(episode, transcript)
        except (json.JSONDecodeError, ValueError):
            print(f"[{i}/{total}] JSON error — retrying with forced JSON prefix...")
            time.sleep(1)
            extracted = analyzeEpisode(episode, transcript, retry=True)

        output = {
            "youtubeID": youtubeID,
            "title": title,
            "publishedAt": episode["publishedAt"],
            **extracted,
        }

        with open(outputFile, "w") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        elapsed = time.time() - startTime
        conceptCount = len(extracted.get("concepts", []))
        profileCount = len(extracted.get("profiles", []))
        storyCount = len(extracted.get("stories", []))
        print(f"[{i}/{total}] Done in {elapsed:.0f}s — {conceptCount} concepts, {profileCount} profiles, {storyCount} stories")

        # Avoid rate limiting
        time.sleep(0.5)

    except Exception as e:
        print(f"[{i}/{total}] FAILED: {title} — {e}")
        failed.append({"youtubeID": youtubeID, "title": title, "reason": str(e)})

with open(logFile, "w") as f:
    json.dump({"skipped": len(skipped), "failed": len(failed), "failedEpisodes": failed}, f, indent=2)

print(f"\nDone. {total - len(skipped) - len(failed)} analyzed, {len(skipped)} skipped, {len(failed)} failed.")
