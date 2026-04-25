# Merges all per-episode analysis files into three unified datasets.
# Outputs to pipeline/data/concepts.json, profiles.json, stories.json.
# Applies fuzzy deduplication to merge near-identical terms/names across episodes.
# Run after analyzeEpisodes.py has completed.

import json
import re
from collections import defaultdict
from pathlib import Path

from rapidfuzz import fuzz

analysisDir = Path(__file__).parent.parent / "analysis"
dataDir = Path(__file__).parent.parent / "data"

# Thresholds for fuzzy merging
CONCEPT_THRESHOLD = 90
PROFILE_THRESHOLD = 88

analysisFiles = sorted(analysisDir.glob("*.json"))
print(f"Found {len(analysisFiles)} analysis files to aggregate.\n")


def normalizeProfileKey(name: str) -> str:
    """Normalize a profile name for comparison: expand 'Football Club' → 'fc',
    convert '(Women)' parentheticals to ' women', strip other context parentheticals,
    strip legal suffixes, and normalize ampersand variants."""
    s = name.lower().strip()
    s = re.sub(r"\bassociation\s+football\s+club\b", "afc", s)
    s = re.sub(r"\bfootball\s+club\b", "fc", s)
    # Convert women's parentheticals to a token rather than stripping
    s = re.sub(r"\(\s*women'?s?\s*\)", " women", s)
    # Strip remaining context parentheticals (stadium names, incidents, etc.)
    s = re.sub(r"\([^)]*\)", "", s)
    s = re.sub(r"\b(limited|ltd\.?|plc|llc|inc\.?)\b", "", s)
    s = s.replace(" & ", " and ")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def normalizeConceptKey(term: str) -> str:
    """Normalize a concept term for comparison: strip parenthetical abbreviations."""
    s = term.lower().strip()
    s = re.sub(r"\s*\([^)]*\)\s*", " ", s).strip()
    s = re.sub(r"\s+", " ", s).strip()
    return s


def hasWomen(name: str) -> bool:
    return bool(re.search(r"\bwomen\b", name, re.IGNORECASE))


def fuzzyMerge(entityMap: dict, threshold: int, normalizeKey, sameGroup=None) -> dict:
    """
    Merge entries whose normalized keys score above threshold.
    Uses max(ratio, token_sort_ratio) for profiles; ratio only for concepts.
    The entry with more episode mentions becomes the canonical name.
    sameGroup: optional callable(keyA, keyB) → bool, extra guard against merging.
    """
    canonicals: list[str] = []
    redirects: dict[str, str] = {}
    normCache: dict[str, str] = {k: normalizeKey(k) for k in entityMap}

    def score(a: str, b: str) -> float:
        na, nb = normCache[a], normCache[b]
        return max(fuzz.ratio(na, nb), fuzz.token_sort_ratio(na, nb))

    for key in entityMap:
        bestScore = 0
        bestCanonical = None
        for can in canonicals:
            if sameGroup and not sameGroup(key, can):
                continue
            s = score(key, can)
            if s > bestScore:
                bestScore = s
                bestCanonical = can

        if bestScore >= threshold:
            existingEps = len(entityMap[bestCanonical]["episodes"])
            newEps = len(entityMap[key]["episodes"])
            if newEps > existingEps:
                redirects[bestCanonical] = key
                canonicals[canonicals.index(bestCanonical)] = key
            else:
                redirects[key] = bestCanonical
        else:
            canonicals.append(key)

    result: dict[str, dict] = {}
    for key, data in entityMap.items():
        can = key
        seen = set()
        while can in redirects and can not in seen:
            seen.add(can)
            can = redirects[can]

        if can not in result:
            src = entityMap[can]
            result[can] = {
                "term":         src.get("term", ""),
                "name":         src.get("name", ""),
                "type":         src.get("type", ""),
                "definitions":  list(src.get("definitions", [])),
                "descriptions": list(src.get("descriptions", [])),
                "episodes":     list(src["episodes"]),
            }

        if key != can:
            result[can]["definitions"]  += data.get("definitions", [])
            result[can]["descriptions"] += data.get("descriptions", [])
            result[can]["episodes"]     += data["episodes"]

    return result


# --- Aggregate concepts ---
conceptMap: dict[str, dict] = defaultdict(lambda: {"term": "", "definitions": [], "episodes": []})

for analysisFile in analysisFiles:
    with open(analysisFile) as f:
        data = json.load(f)

    youtubeID   = data["youtubeID"]
    title       = data["title"]
    publishedAt = data["publishedAt"]

    for concept in data.get("concepts", []):
        term = concept.get("term", "").strip()
        if not term:
            continue
        key = term.lower()
        conceptMap[key]["term"] = term
        if concept.get("definition"):
            conceptMap[key]["definitions"].append({
                "text":      concept["definition"],
                "youtubeID": youtubeID,
            })
        for ts in concept.get("timestamps", []):
            conceptMap[key]["episodes"].append({
                "youtubeID":   youtubeID,
                "title":       title,
                "publishedAt": publishedAt,
                "timestamp":   ts,
            })

print(f"Concepts before dedup: {len(conceptMap)}")
conceptMap = fuzzyMerge(dict(conceptMap), CONCEPT_THRESHOLD, normalizeConceptKey)
print(f"Concepts after dedup:  {len(conceptMap)}")


# --- Aggregate profiles ---
profileMap: dict[str, dict] = defaultdict(lambda: {"name": "", "type": "", "descriptions": [], "episodes": []})

for analysisFile in analysisFiles:
    with open(analysisFile) as f:
        data = json.load(f)

    youtubeID   = data["youtubeID"]
    title       = data["title"]
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
                "text":      profile["description"],
                "youtubeID": youtubeID,
            })
        for ts in profile.get("timestamps", []):
            profileMap[key]["episodes"].append({
                "youtubeID":   youtubeID,
                "title":       title,
                "publishedAt": publishedAt,
                "timestamp":   ts,
            })

print(f"\nProfiles before dedup: {len(profileMap)}")
# Same-type and same women's/non-women's guard prevents false positives
def profileSameGroup(a: str, b: str) -> bool:
    return (profileMap[a]["type"] == profileMap[b]["type"] and
            hasWomen(a) == hasWomen(b))

profileMap = fuzzyMerge(dict(profileMap), PROFILE_THRESHOLD, normalizeProfileKey, sameGroup=profileSameGroup)
print(f"Profiles after dedup:  {len(profileMap)}")


# --- Collect stories (per-episode, not merged) ---
allStories = []

for analysisFile in analysisFiles:
    with open(analysisFile) as f:
        data = json.load(f)

    youtubeID   = data["youtubeID"]
    title       = data["title"]
    publishedAt = data["publishedAt"]

    for story in data.get("stories", []):
        allStories.append({
            "youtubeID":    youtubeID,
            "episodeTitle": title,
            "publishedAt":  publishedAt,
            "headline":     story.get("headline", ""),
            "summary":      story.get("summary", ""),
            "timestamp":    story.get("timestamp", 0),
        })

allStories.sort(key=lambda s: s["publishedAt"])


# --- Build final output lists ---
concepts = sorted(
    [{"term": v["term"], "definitions": v["definitions"], "episodes": v["episodes"]}
     for v in conceptMap.values()],
    key=lambda c: c["term"].lower(),
)

profiles = sorted(
    [{"name": v["name"], "type": v["type"], "descriptions": v["descriptions"], "episodes": v["episodes"]}
     for v in profileMap.values()],
    key=lambda p: p["name"].lower(),
)

with open(dataDir / "concepts.json", "w") as f:
    json.dump(concepts, f, indent=2, ensure_ascii=False)

with open(dataDir / "profiles.json", "w") as f:
    json.dump(profiles, f, indent=2, ensure_ascii=False)

with open(dataDir / "stories.json", "w") as f:
    json.dump(allStories, f, indent=2, ensure_ascii=False)

print(f"\nConcepts:  {len(concepts)} unique terms → data/concepts.json")
print(f"Profiles:  {len(profiles)} unique entries → data/profiles.json")
print(f"Stories:   {len(allStories)} stories → data/stories.json")
