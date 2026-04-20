# Fetches all episode metadata from the Supporting Cast RSS feed and writes to data/episodes.json.
# Safe to re-run — overwrites episodes.json with the full current feed on each run.
# Requires: RSS_FEED_URL in pipeline/.env

import json
import os
import re
import xml.etree.ElementTree as ET
from datetime import timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

RSS_FEED_URL = os.getenv("RSS_FEED_URL")
if not RSS_FEED_URL:
    raise EnvironmentError("RSS_FEED_URL not set. Add it to pipeline/.env")

outputFile = Path(__file__).parent.parent / "data" / "episodes.json"
outputFile.parent.mkdir(parents=True, exist_ok=True)

ITUNES_NS = "http://www.itunes.com/dtds/podcast-1.0.dtd"


def secondsToISO(seconds: int) -> str:
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    parts = "PT"
    if h:
        parts += f"{h}H"
    if m:
        parts += f"{m}M"
    if s or len(parts) == 2:
        parts += f"{s}S"
    return parts


def cleanText(text: str) -> str:
    # Strip zero-width/invisible unicode chars used by podcast apps for hyperlinks
    cleaned = re.sub(r'[\u2060\u200b\u200c\u200d\ufeff]', '', text)
    return re.sub(r'\n{3,}', '\n\n', cleaned).strip()


print("Fetching RSS feed...")
response = requests.get(RSS_FEED_URL, timeout=30)
response.raise_for_status()

root = ET.fromstring(response.content)
items = root.findall(".//item")
print(f"Found {len(items)} items in feed.")

episodes = []
skipped = 0

for item in items:
    episodeType = item.findtext(f"{{{ITUNES_NS}}}episodeType") or "full"
    if episodeType == "trailer":
        skipped += 1
        continue

    guid = item.findtext("guid", "").strip()
    title = item.findtext("title", "").strip()
    pubDateStr = item.findtext("pubDate", "")
    description = cleanText(item.findtext("description", ""))

    enc = item.find("enclosure")
    audioURL = enc.get("url") if enc is not None else None

    durationRaw = item.findtext(f"{{{ITUNES_NS}}}duration")
    try:
        durationISO = secondsToISO(int(durationRaw)) if durationRaw else None
    except (ValueError, TypeError):
        durationISO = durationRaw

    try:
        publishedAt = parsedate_to_datetime(pubDateStr).astimezone(timezone.utc).isoformat()
    except Exception:
        publishedAt = pubDateStr

    episodes.append({
        "youtubeID": guid,
        "title": title,
        "publishedAt": publishedAt,
        "duration": durationISO,
        "thumbnail": None,
        "description": description,
        "audioURL": audioURL,
    })

episodes.sort(key=lambda e: e["publishedAt"])

with open(outputFile, "w") as f:
    json.dump(episodes, f, indent=2)

print(f"Saved {len(episodes)} episodes to {outputFile} ({skipped} trailers skipped).")
