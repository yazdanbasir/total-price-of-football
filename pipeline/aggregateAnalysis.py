# Merges all per-episode analysis files into three unified datasets.
# Outputs to pipeline/data/concepts.json, profiles.json, stories.json.
# Cross-references mentions across all 91 episodes for each concept and profile.
# Run after analyzeEpisodes.py has completed.

import json
from collections import defaultdict
from pathlib import Path

analysisDir = Path(__file__).parent / "analysis"
dataDir = Path(__file__).parent / "data"

analysisFiles = sorted(analysisDir.glob("*.json"))
print(f"Found {len(analysisFiles)} analysis files to aggregate.\n")

# Aggregate concepts — group by normalised term
conceptMap: dict[str, dict] = defaultdict(lambda: {"term": "", "definitions": [], "episodes": []})

for analysisFile in analysisFiles:
    with open(analysisFile) as f:
        data = json.load(f)

    youtubeID = data["youtubeID"]
    title = data["title"]
    publishedAt = data["publishedAt"]

    for concept in data.get("concepts", []):
        term = concept.get("term", "").strip()
        if not term:
            continue
        key = term.lower()
        conceptMap[key]["term"] = term
        if concept.get("definition"):
            conceptMap[key]["definitions"].append({
                "text": concept["definition"],
                "youtubeID": youtubeID,
            })
        for ts in concept.get("timestamps", []):
            conceptMap[key]["episodes"].append({
                "youtubeID": youtubeID,
                "title": title,
                "publishedAt": publishedAt,
                "timestamp": ts,
            })

# Aggregate profiles — group by normalised name
profileMap: dict[str, dict] = defaultdict(lambda: {"name": "", "type": "", "descriptions": [], "episodes": []})

for analysisFile in analysisFiles:
    with open(analysisFile) as f:
        data = json.load(f)

    youtubeID = data["youtubeID"]
    title = data["title"]
    publishedAt = data["publishedAt"]

    for profile in data.get("profiles", []):
        name = profile.get("name", "").strip()
        if not name:
            continue
        key = name.lower()
        profileMap[key]["name"] = name
        profileMap[key]["type"] = profile.get("type", "")
        if profile.get("description"):
            profileMap[key]["descriptions"].append({
                "text": profile["description"],
                "youtubeID": youtubeID,
            })
        for ts in profile.get("timestamps", []):
            profileMap[key]["episodes"].append({
                "youtubeID": youtubeID,
                "title": title,
                "publishedAt": publishedAt,
                "timestamp": ts,
            })

# Collect all stories (stories are per-episode, not merged)
allStories = []

for analysisFile in analysisFiles:
    with open(analysisFile) as f:
        data = json.load(f)

    youtubeID = data["youtubeID"]
    title = data["title"]
    publishedAt = data["publishedAt"]

    for story in data.get("stories", []):
        allStories.append({
            "youtubeID": youtubeID,
            "episodeTitle": title,
            "publishedAt": publishedAt,
            "headline": story.get("headline", ""),
            "summary": story.get("summary", ""),
            "timestamp": story.get("timestamp", 0),
        })

# Sort stories by date
allStories.sort(key=lambda s: s["publishedAt"])

# Build final output lists
concepts = sorted(
    [{"term": v["term"], "definitions": v["definitions"], "episodes": v["episodes"]} for v in conceptMap.values()],
    key=lambda c: c["term"].lower(),
)

profiles = sorted(
    [{"name": v["name"], "type": v["type"], "descriptions": v["descriptions"], "episodes": v["episodes"]} for v in profileMap.values()],
    key=lambda p: p["name"].lower(),
)

with open(dataDir / "concepts.json", "w") as f:
    json.dump(concepts, f, indent=2, ensure_ascii=False)

with open(dataDir / "profiles.json", "w") as f:
    json.dump(profiles, f, indent=2, ensure_ascii=False)

with open(dataDir / "stories.json", "w") as f:
    json.dump(allStories, f, indent=2, ensure_ascii=False)

print(f"Concepts:  {len(concepts)} unique terms → data/concepts.json")
print(f"Profiles:  {len(profiles)} unique entries → data/profiles.json")
print(f"Stories:   {len(allStories)} stories → data/stories.json")
