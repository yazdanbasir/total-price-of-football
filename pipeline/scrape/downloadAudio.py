# Downloads audio for all episodes in data/episodes.json into audio/.
# Safe to pause and re-run — already downloaded files are skipped.
# Requires node (v22+) at /usr/local/bin/node for yt-dlp's JS challenge solver.

import json
import os
from pathlib import Path
import yt_dlp
from tqdm import tqdm

os.environ["PATH"] = f"/usr/local/bin:{os.environ.get('PATH', '')}"

episodesFile = Path(__file__).parent.parent / "data" / "episodes.json"
audioDir = Path(__file__).parent.parent / "audio"
logFile = Path(__file__).parent.parent / "data" / "downloadLog.json"
audioDir.mkdir(parents=True, exist_ok=True)

with open(episodesFile) as f:
    episodes = json.load(f)

baseOptions = {
    "cookiesfrombrowser": ("brave",),
    "js_runtimes": {"node": {}},
    "quiet": True,
    "no_warnings": True,
}

def isAlreadyDownloaded(youtubeID: str) -> bool:
    return any(audioDir.glob(f"{youtubeID}.*"))

def getBestAudioFormatID(url: str) -> str | None:
    """Return the format ID of the best available audio-only stream, or None."""
    with yt_dlp.YoutubeDL({**baseOptions, "format": "bestaudio"}) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info.get("formats", [])
        audioOnly = [f for f in formats if f.get("vcodec") == "none" and f.get("acodec") not in (None, "none")]
        if audioOnly:
            return max(audioOnly, key=lambda f: f.get("abr") or 0)["format_id"]
        withAudio = [f for f in formats if f.get("acodec") not in (None, "none")]
        if withAudio:
            return max(withAudio, key=lambda f: f.get("abr") or 0)["format_id"]
        return None

skipped = []
failed = []
downloaded = 0

with tqdm(total=len(episodes), desc="Episodes", unit="ep") as bar:
    for episode in episodes:
        youtubeID = episode["youtubeID"]
        title = episode["title"]
        shortTitle = title[:50]

        if isAlreadyDownloaded(youtubeID):
            bar.set_postfix(status="skip", ep=shortTitle)
            skipped.append({"youtubeID": youtubeID, "title": title, "reason": "already downloaded"})
            bar.update(1)
            continue

        url = f"https://www.youtube.com/watch?v={youtubeID}"
        bar.set_postfix(status="checking", ep=shortTitle)

        try:
            formatID = getBestAudioFormatID(url)
        except Exception as e:
            tqdm.write(f"SKIPPED (format check failed): {title} — {e}")
            skipped.append({"youtubeID": youtubeID, "title": title, "reason": f"format check failed: {e}"})
            bar.update(1)
            continue

        if not formatID:
            tqdm.write(f"SKIPPED (no audio available): {title}")
            skipped.append({"youtubeID": youtubeID, "title": title, "reason": "no audio format available"})
            bar.update(1)
            continue

        bar.set_postfix(status="downloading", ep=shortTitle)
        try:
            with yt_dlp.YoutubeDL({
                **baseOptions,
                "format": formatID,
                "outtmpl": str(audioDir / "%(id)s.%(ext)s"),
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "128",
                }],
            }) as ydl:
                ydl.download([url])
            downloaded += 1
            tqdm.write(f"Downloaded: {title}")
        except Exception as e:
            tqdm.write(f"FAILED: {title} — {e}")
            failed.append({"youtubeID": youtubeID, "title": title, "reason": str(e)})

        bar.update(1)

with open(logFile, "w") as f:
    json.dump({"skipped": skipped, "failed": failed}, f, indent=2)

print(f"\nAll done. {downloaded} downloaded, {len(skipped)} skipped, {len(failed)} failed.")
print(f"See {logFile} for details.")
