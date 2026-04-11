# Downloads audio for all episodes in data/episodes.json into audio/.
# Safe to pause and re-run — already downloaded files are skipped.
# Requires node (v22+) at /usr/local/bin/node for yt-dlp's JS challenge solver.

import json
import os
from pathlib import Path
import yt_dlp

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

total = len(episodes)
for i, episode in enumerate(episodes, 1):
    youtubeID = episode["youtubeID"]
    title = episode["title"]

    if isAlreadyDownloaded(youtubeID):
        print(f"[{i}/{total}] Skipping (already downloaded): {title}")
        continue

    url = f"https://www.youtube.com/watch?v={youtubeID}"
    print(f"[{i}/{total}] Checking formats: {title}")

    try:
        formatID = getBestAudioFormatID(url)
    except Exception as e:
        print(f"[{i}/{total}] SKIPPED (format check failed): {title} — {e}")
        skipped.append({"youtubeID": youtubeID, "title": title, "reason": f"format check failed: {e}"})
        continue

    if not formatID:
        print(f"[{i}/{total}] SKIPPED (no audio available): {title}")
        skipped.append({"youtubeID": youtubeID, "title": title, "reason": "no audio format available"})
        continue

    print(f"[{i}/{total}] Downloading: {title}")
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
        print(f"[{i}/{total}] Done: {youtubeID}.mp3")
    except Exception as e:
        print(f"[{i}/{total}] FAILED: {title} — {e}")
        failed.append({"youtubeID": youtubeID, "title": title, "reason": str(e)})

with open(logFile, "w") as f:
    json.dump({"skipped": skipped, "failed": failed}, f, indent=2)

print(f"\nAll done. {total - len(skipped) - len(failed)} downloaded, {len(skipped)} skipped, {len(failed)} failed.")
print(f"See {logFile} for details.")
