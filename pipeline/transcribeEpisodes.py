# Transcribes all downloaded MP3s using faster-whisper (local, free, CPU-based).
# Outputs one JSON file per episode to transcripts/ named by youtubeID.
# Safe to pause and re-run — already transcribed episodes are skipped.
# Requires: pip install faster-whisper
# Model: large-v3, runs on CPU (avoids MPS float64 incompatibility on Apple Silicon).

import json
import time
from pathlib import Path
from faster_whisper import WhisperModel

audioDir = Path(__file__).parent / "audio"
transcriptsDir = Path(__file__).parent / "transcripts"
episodesFile = Path(__file__).parent / "data" / "episodes.json"
logFile = Path(__file__).parent / "data" / "transcriptLog.json"
transcriptsDir.mkdir(parents=True, exist_ok=True)

with open(episodesFile) as f:
    episodes = json.load(f)

print("Loading faster-whisper large-v3 model (downloads on first run)...")
model = WhisperModel("large-v3", device="cpu", compute_type="int8")
print("Model loaded.\n")

failed = []
skipped = []

total = len(episodes)
for i, episode in enumerate(episodes, 1):
    youtubeID = episode["youtubeID"]
    title = episode["title"]
    outputFile = transcriptsDir / f"{youtubeID}.json"

    if outputFile.exists():
        print(f"[{i}/{total}] Skipping (already transcribed): {title}")
        skipped.append(youtubeID)
        continue

    audioFile = audioDir / f"{youtubeID}.mp3"
    if not audioFile.exists():
        print(f"[{i}/{total}] SKIPPED (no audio file): {title}")
        failed.append({"youtubeID": youtubeID, "title": title, "reason": "audio file not found"})
        continue

    print(f"[{i}/{total}] Transcribing: {title}")
    startTime = time.time()

    try:
        segments, info = model.transcribe(
            str(audioFile),
            language="en",
            word_timestamps=True,
        )

        outputSegments = []
        fullText = []
        for seg in segments:
            outputSegments.append({
                "start": round(seg.start, 2),
                "end": round(seg.end, 2),
                "text": seg.text.strip(),
            })
            fullText.append(seg.text.strip())

        output = {
            "youtubeID": youtubeID,
            "title": title,
            "publishedAt": episode["publishedAt"],
            "duration": episode["duration"],
            "text": " ".join(fullText),
            "segments": outputSegments,
        }

        with open(outputFile, "w") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        elapsed = time.time() - startTime
        print(f"[{i}/{total}] Done in {elapsed:.0f}s: {youtubeID}.json")

    except Exception as e:
        print(f"[{i}/{total}] FAILED: {title} — {e}")
        failed.append({"youtubeID": youtubeID, "title": title, "reason": str(e)})

with open(logFile, "w") as f:
    json.dump({"skipped": len(skipped), "failed": failed}, f, indent=2)

print(f"\nAll done. {total - len(skipped) - len(failed)} transcribed, {len(skipped)} skipped, {len(failed)} failed.")
print(f"See {logFile} for details.")
