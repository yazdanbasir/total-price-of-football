# Transcribes all downloaded MP3s using mlx-whisper (Apple MLX, M-series GPU).
# Outputs one JSON file per episode to transcripts/ named by youtubeID.
# Safe to pause and re-run — already transcribed episodes are skipped.
# Requires: pip install mlx-whisper
# Model: mlx-community/whisper-large-v3-turbo (distilled large-v3, ~8x faster, M-series GPU)

import json
import time
from pathlib import Path
import mlx_whisper
from tqdm import tqdm

audioDir = Path(__file__).parent.parent / "audio"
transcriptsDir = Path(__file__).parent.parent / "transcripts"
episodesFile = Path(__file__).parent.parent / "data" / "episodes.json"
logFile = Path(__file__).parent.parent / "data" / "transcriptLog.json"
transcriptsDir.mkdir(parents=True, exist_ok=True)

MODEL = "mlx-community/whisper-large-v3-turbo"

with open(episodesFile) as f:
    episodes = json.load(f)

print(f"Using mlx-whisper model: {MODEL}")
print("Model will be downloaded on first run.\n")

failed = []
skipped = []
done = 0
totalTime = 0

with tqdm(total=len(episodes), desc="Episodes", unit="ep") as bar:
    for episode in episodes:
        youtubeID = episode["youtubeID"]
        title = episode["title"]
        shortTitle = title[:50]
        outputFile = transcriptsDir / f"{youtubeID}.json"

        if outputFile.exists():
            skipped.append(youtubeID)
            bar.set_postfix(status="skip", ep=shortTitle)
            bar.update(1)
            continue

        audioFile = audioDir / f"{youtubeID}.mp3"
        if not audioFile.exists():
            tqdm.write(f"SKIPPED (no audio file): {title}")
            failed.append({"youtubeID": youtubeID, "title": title, "reason": "audio file not found"})
            bar.update(1)
            continue

        bar.set_postfix(status="transcribing", ep=shortTitle)
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
            done += 1
            totalTime += elapsed
            avgTime = totalTime / done
            remaining = len(episodes) - (done + len(skipped) + len(failed))
            eta = int(avgTime * remaining)

            tqdm.write(f"Done in {elapsed:.0f}s: {title[:60]}")
            bar.set_postfix(
                status="done",
                avg=f"{avgTime:.0f}s/ep",
                eta=f"{eta//60}m{eta%60:02d}s"
            )

        except Exception as e:
            tqdm.write(f"FAILED: {title} — {e}")
            failed.append({"youtubeID": youtubeID, "title": title, "reason": str(e)})

        bar.update(1)

with open(logFile, "w") as f:
    json.dump({"skipped": len(skipped), "failed": failed}, f, indent=2)

print(f"\nAll done. {done} transcribed, {len(skipped)} skipped, {len(failed)} failed.")
print(f"See {logFile} for details.")
