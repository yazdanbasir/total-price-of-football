# Inserts episodes, concepts, profiles, and stories into the database.
# Safe to re-run — clears and repopulates all tables each time (except chunks).
# Run setupDB.py first, then this, then embedChunks.py.
# Requires: DATABASE_URL in pipeline/.env

import json
import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

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

conn = psycopg2.connect(databaseURL)
cur = conn.cursor()


def bestDefinition(definitions: list) -> str | None:
    """Pick the longest definition as the canonical one."""
    if not definitions:
        return None
    return max(definitions, key=lambda d: len(d.get("text", "")))["text"]


# --- Episodes ---
print(f"Inserting {len(episodes)} episodes...")
cur.execute("DELETE FROM episodes;")
for ep in episodes:
    cur.execute("""
        INSERT INTO episodes (youtube_id, title, published_at, duration, thumbnail, description)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (youtube_id) DO NOTHING;
    """, (
        ep["youtubeID"],
        ep["title"],
        ep["publishedAt"],
        ep.get("duration"),
        ep.get("thumbnail"),
        ep.get("description"),
    ))

conn.commit()
print(f"  Done.")

# --- Concepts ---
print(f"Inserting {len(concepts)} concepts...")
cur.execute("DELETE FROM concept_mentions;")
cur.execute("DELETE FROM concepts;")

for concept in concepts:
    term = concept["term"]
    definition = bestDefinition(concept.get("definitions", []))

    cur.execute("""
        INSERT INTO concepts (term, definition)
        VALUES (%s, %s)
        ON CONFLICT (term) DO UPDATE SET definition = EXCLUDED.definition
        RETURNING id;
    """, (term, definition))

    conceptID = cur.fetchone()[0]

    for mention in concept.get("episodes", []):
        cur.execute("""
            INSERT INTO concept_mentions (concept_id, episode_id, timestamp)
            VALUES (%s, %s, %s);
        """, (conceptID, mention["youtubeID"], mention.get("timestamp")))

conn.commit()
print(f"  Done.")

# --- Profiles ---
print(f"Inserting {len(profiles)} profiles...")
cur.execute("DELETE FROM profile_mentions;")
cur.execute("DELETE FROM profiles;")

for profile in profiles:
    name = profile["name"]
    description = bestDefinition(profile.get("descriptions", []))

    cur.execute("""
        INSERT INTO profiles (name, type, description)
        VALUES (%s, %s, %s)
        ON CONFLICT (name) DO UPDATE SET description = EXCLUDED.description
        RETURNING id;
    """, (name, profile.get("type"), description))

    profileID = cur.fetchone()[0]

    for mention in profile.get("episodes", []):
        cur.execute("""
            INSERT INTO profile_mentions (profile_id, episode_id, timestamp)
            VALUES (%s, %s, %s);
        """, (profileID, mention["youtubeID"], mention.get("timestamp")))

conn.commit()
print(f"  Done.")

# --- Stories ---
print(f"Inserting {len(stories)} stories...")
cur.execute("DELETE FROM stories;")

for story in stories:
    cur.execute("""
        INSERT INTO stories (episode_id, headline, summary, timestamp)
        VALUES (%s, %s, %s, %s);
    """, (
        story["youtubeID"],
        story.get("headline"),
        story.get("summary"),
        story.get("timestamp"),
    ))

conn.commit()
print(f"  Done.")

cur.close()
conn.close()

print("\nAll data inserted successfully.")
