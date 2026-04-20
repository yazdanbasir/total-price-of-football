# Syncs episodes, concepts, profiles, and stories from pipeline JSON into the database.
# Uses a single connection and batch inserts — safe to re-run.
# Requires: DATABASE_URL in pipeline/.env

import json
import os
from pathlib import Path

import psycopg2
from psycopg2.extras import execute_batch
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv(Path(__file__).parent.parent / ".env")

databaseURL = os.getenv("DATABASE_URL")
if not databaseURL:
    raise EnvironmentError("DATABASE_URL not set. Add it to pipeline/.env")

dataDir = Path(__file__).parent.parent / "data"

with open(dataDir / "episodes.json") as f:
    episodes = json.load(f)

with open(dataDir / "concepts.json") as f:
    concepts = json.load(f)

with open(dataDir / "profiles.json") as f:
    profiles = json.load(f)

with open(dataDir / "stories.json") as f:
    stories = json.load(f)

knownEpisodeIDs = {ep["youtubeID"] for ep in episodes}


def bestDefinition(definitions: list) -> str | None:
    if not definitions:
        return None
    return max(definitions, key=lambda d: len(d.get("text", "")))["text"]


conn = psycopg2.connect(databaseURL)
cur = conn.cursor()

# --- Episodes ---
print("Inserting episodes...")
cur.execute("DELETE FROM episodes;")
execute_batch(cur, """
    INSERT INTO episodes (youtube_id, title, published_at, duration, thumbnail, description)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (youtube_id) DO UPDATE SET
        title        = EXCLUDED.title,
        published_at = EXCLUDED.published_at,
        duration     = EXCLUDED.duration,
        thumbnail    = EXCLUDED.thumbnail,
        description  = EXCLUDED.description
""", [
    (ep["youtubeID"], ep["title"], ep["publishedAt"], ep.get("duration"), ep.get("thumbnail"), ep.get("description"))
    for ep in episodes
])
conn.commit()
print(f"  {len(episodes)} episodes inserted.")

# --- Concepts ---
print("Inserting concepts...")
cur.execute("DELETE FROM concept_mentions;")
cur.execute("DELETE FROM concepts;")
conn.commit()

conceptMentionRows = []
with tqdm(total=len(concepts), desc="Concepts", unit="concept") as bar:
    for concept in concepts:
        term = concept["term"]
        definition = bestDefinition(concept.get("definitions", []))
        cur.execute(
            "INSERT INTO concepts (term, definition) VALUES (%s, %s) RETURNING id",
            (term, definition)
        )
        conceptID = cur.fetchone()[0]
        for mention in concept.get("episodes", []):
            if mention["youtubeID"] in knownEpisodeIDs:
                conceptMentionRows.append((conceptID, mention["youtubeID"], mention.get("timestamp")))
        bar.update(1)

conn.commit()
execute_batch(cur, """
    INSERT INTO concept_mentions (concept_id, episode_id, timestamp) VALUES (%s, %s, %s)
""", conceptMentionRows)
conn.commit()
print(f"  {len(concepts)} concepts, {len(conceptMentionRows)} mentions inserted.")

# --- Profiles ---
print("Inserting profiles...")
cur.execute("DELETE FROM profile_mentions;")
cur.execute("DELETE FROM profiles;")
conn.commit()

profileMentionRows = []
with tqdm(total=len(profiles), desc="Profiles", unit="profile") as bar:
    for profile in profiles:
        name = profile["name"]
        description = bestDefinition(profile.get("descriptions", []))
        cur.execute(
            "INSERT INTO profiles (name, type, description) VALUES (%s, %s, %s) RETURNING id",
            (name, profile.get("type"), description)
        )
        profileID = cur.fetchone()[0]
        for mention in profile.get("episodes", []):
            if mention["youtubeID"] in knownEpisodeIDs:
                profileMentionRows.append((profileID, mention["youtubeID"], mention.get("timestamp")))
        bar.update(1)

conn.commit()
execute_batch(cur, """
    INSERT INTO profile_mentions (profile_id, episode_id, timestamp) VALUES (%s, %s, %s)
""", profileMentionRows)
conn.commit()
print(f"  {len(profiles)} profiles, {len(profileMentionRows)} mentions inserted.")

# --- Stories ---
print("Inserting stories...")
cur.execute("DELETE FROM stories;")
storyRows = []
for story in stories:
    if story["youtubeID"] not in knownEpisodeIDs:
        continue
    timestamp = story.get("timestamp")
    if isinstance(timestamp, list):
        timestamp = timestamp[0] if timestamp else None
    storyRows.append((story["youtubeID"], story.get("headline"), story.get("summary"), timestamp))

execute_batch(cur, """
    INSERT INTO stories (episode_id, headline, summary, timestamp) VALUES (%s, %s, %s, %s)
""", storyRows)
conn.commit()
print(f"  {len(storyRows)} stories inserted.")

cur.close()
conn.close()

print("\nAll data inserted successfully.")
