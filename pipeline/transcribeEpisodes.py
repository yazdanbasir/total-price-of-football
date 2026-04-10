# Transcribes all downloaded MP3s using mlx-whisper (Apple MLX, M-series GPU).
# Outputs one JSON file per episode to transcripts/ named by youtubeID.
# Safe to pause and re-run — already transcribed episodes are skipped.
# Requires: pip install mlx-whisper
# Model: mlx-community/whisper-large-v3-turbo (distilled large-v3, ~8x faster, M-series GPU)

import json
import time
from pathlib import Path
import mlx_whisper

audioDir = Path(__file__).parent / "audio"
transcriptsDir = Path(__file__).parent / "transcripts"
episodesFile = Path(__file__).parent / "data" / "episodes.json"
logFile = Path(__file__).parent / "data" / "transcriptLog.json"
transcriptsDir.mkdir(parents=True, exist_ok=True)

MODEL = "mlx-community/whisper-large-v3-turbo"

with open(episodesFile) as f:
    episodes = json.load(f)

print(f"Using mlx-whisper model: {MODEL}")
print("Model will be downloaded on first run.\n")

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
        result = mlx_whisper.transcribe(
            str(audioFile),
            path_or_hf_repo=MODEL,
            word_timestamps=True,
            language="en",
        )

        outputSegments = []
        fullText = []
        for seg in result["segments"]:
            outputSegments.append({
                "start": round(seg["start"], 2),
                "end": round(seg["end"], 2),
                "text": seg["text"].strip(),
            })
            fullText.append(seg["text"].strip())

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
