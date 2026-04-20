# Downloads audio for all episodes in data/episodes.json into audio/.
# Safe to re-run — already downloaded files are skipped.
# Uses direct HTTP download from the RSS feed audioURL.

import json
from pathlib import Path

import requests
from tqdm import tqdm

episodesFile = Path(__file__).parent.parent / "data" / "episodes.json"
audioDir = Path(__file__).parent.parent / "audio"
logFile = Path(__file__).parent.parent / "data" / "downloadLog.json"
audioDir.mkdir(parents=True, exist_ok=True)

with open(episodesFile) as f:
    episodes = json.load(f)

skipped = []
failed = []
downloaded = 0

with tqdm(total=len(episodes), desc="Episodes", unit="ep") as bar:
    for episode in episodes:
        episodeID = episode["youtubeID"]
        title = episode["title"]
        shortTitle = title[:50]
        audioURL = episode.get("audioURL")
        outputPath = audioDir / f"{episodeID}.mp3"

        if outputPath.exists():
            bar.set_postfix(status="skip", ep=shortTitle)
            skipped.append({"episodeID": episodeID, "title": title, "reason": "already downloaded"})
            bar.update(1)
            continue

        if not audioURL:
            tqdm.write(f"SKIPPED (no audioURL): {title}")
            skipped.append({"episodeID": episodeID, "title": title, "reason": "no audioURL in episodes.json"})
            bar.update(1)
            continue

        bar.set_postfix(status="downloading", ep=shortTitle)
        try:
            with requests.get(audioURL, stream=True, timeout=120) as r:
                r.raise_for_status()
                with open(outputPath, "wb") as f:
                    for chunk in r.iter_content(chunk_size=65536):
                        f.write(chunk)
            downloaded += 1
            tqdm.write(f"Downloaded: {title}")
        except Exception as e:
            outputPath.unlink(missing_ok=True)
            tqdm.write(f"FAILED: {title} — {e}")
            failed.append({"episodeID": episodeID, "title": title, "reason": str(e)})

        bar.update(1)

with open(logFile, "w") as f:
    json.dump({"skipped": skipped, "failed": failed}, f, indent=2)

print(f"\nAll done. {downloaded} downloaded, {len(skipped)} skipped, {len(failed)} failed.")
print(f"See {logFile} for details.")
