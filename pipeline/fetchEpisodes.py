# Fetches all video metadata from the @POF_POD YouTube channel and writes it to data/episodes.json.

import json
import os
import re
from pathlib import Path
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

youtubeApiKey = os.getenv("YOUTUBE_API_KEY")
channelHandle = "@POF_POD"
outputFile = Path(__file__).parent / "data" / "episodes.json"


def getChannelID(youtube, handle: str) -> str:
    response = youtube.search().list(
        part="snippet",
        q=handle,
        type="channel",
        maxResults=1,
    ).execute()
    return response["items"][0]["snippet"]["channelId"]


def getUploadsPlaylistID(youtube, channelID: str) -> str:
    response = youtube.channels().list(
        part="contentDetails",
        id=channelID,
    ).execute()
    return response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]


def fetchAllVideos(youtube, playlistID: str) -> list[dict]:
    videos = []
    pageToken = None

    while True:
        response = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=playlistID,
            maxResults=50,
            pageToken=pageToken,
        ).execute()

        for item in response["items"]:
            snippet = item["snippet"]
            videos.append({
                "youtubeID": snippet["resourceId"]["videoId"],
                "title": snippet["title"],
                "publishedAt": snippet["publishedAt"],
                "description": snippet["description"],
                "thumbnail": snippet.get("thumbnails", {}).get("medium", {}).get("url"),
            })

        pageToken = response.get("nextPageToken")
        if not pageToken:
            break

    return videos


def parseDurationSeconds(iso: str) -> int:
    """Convert ISO 8601 duration (e.g. PT1H2M3S) to total seconds."""
    if not iso:
        return 0
    hours = int(m.group(1)) if (m := re.search(r'(\d+)H', iso)) else 0
    minutes = int(m.group(1)) if (m := re.search(r'(\d+)M', iso)) else 0
    seconds = int(m.group(1)) if (m := re.search(r'(\d+)S', iso)) else 0
    return hours * 3600 + minutes * 60 + seconds


def fetchVideoDurations(youtube, videos: list[dict]) -> list[dict]:
    ids = [v["youtubeID"] for v in videos]
    durations = {}

    for i in range(0, len(ids), 50):
        batch = ids[i:i + 50]
        response = youtube.videos().list(
            part="contentDetails",
            id=",".join(batch),
        ).execute()
        for item in response["items"]:
            durations[item["id"]] = item["contentDetails"]["duration"]

    for video in videos:
        video["duration"] = durations.get(video["youtubeID"])

    return videos


def main():
    if not youtubeApiKey:
        raise ValueError("YOUTUBE_API_KEY not set in .env")

    outputFile.parent.mkdir(parents=True, exist_ok=True)

    youtube = build("youtube", "v3", developerKey=youtubeApiKey)

    print(f"Looking up channel: {channelHandle}")
    channelID = getChannelID(youtube, channelHandle)
    print(f"Channel ID: {channelID}")

    playlistID = getUploadsPlaylistID(youtube, channelID)
    print(f"Uploads playlist: {playlistID}")

    print("Fetching video list...")
    videos = fetchAllVideos(youtube, playlistID)
    print(f"Found {len(videos)} videos. Fetching durations...") # should be 91?

    videos = fetchVideoDurations(youtube, videos)

    # Filter out YouTube Shorts (<=60 seconds)
    before = len(videos)
    videos = [v for v in videos if parseDurationSeconds(v["duration"]) > 60]
    print(f"Filtered out {before - len(videos)} Shorts. Keeping {len(videos)} videos.")

    videos.sort(key=lambda v: v["publishedAt"])

    with open(outputFile, "w") as f:
        json.dump(videos, f, indent=2)

    print(f"Saved {len(videos)} episodes to {outputFile}")


if __name__ == "__main__":
    main()
