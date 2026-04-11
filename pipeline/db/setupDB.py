# Creates all database tables and enables the pgvector extension.
# Safe to re-run — uses CREATE TABLE IF NOT EXISTS throughout.
# Run this once before insertData.py or embedChunks.py.
# Requires: DATABASE_URL in pipeline/.env

import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

databaseURL = os.getenv("DATABASE_URL")
if not databaseURL:
    raise EnvironmentError("DATABASE_URL not set. Add it to pipeline/.env")

conn = psycopg2.connect(databaseURL)
cur = conn.cursor()

print("Enabling pgvector extension...")
cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

print("Creating tables...")

cur.execute("""
    CREATE TABLE IF NOT EXISTS episodes (
        youtube_id   TEXT PRIMARY KEY,
        title        TEXT NOT NULL,
        published_at TIMESTAMPTZ NOT NULL,
        duration     TEXT,
        thumbnail    TEXT,
        description  TEXT
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS concepts (
        id         SERIAL PRIMARY KEY,
        term       TEXT NOT NULL UNIQUE,
        definition TEXT
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS concept_mentions (
        id         SERIAL PRIMARY KEY,
        concept_id INTEGER NOT NULL REFERENCES concepts(id) ON DELETE CASCADE,
        episode_id TEXT    NOT NULL REFERENCES episodes(youtube_id) ON DELETE CASCADE,
        timestamp  INTEGER
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS profiles (
        id          SERIAL PRIMARY KEY,
        name        TEXT NOT NULL UNIQUE,
        type        TEXT,
        description TEXT
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS profile_mentions (
        id         SERIAL PRIMARY KEY,
        profile_id INTEGER NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
        episode_id TEXT    NOT NULL REFERENCES episodes(youtube_id) ON DELETE CASCADE,
        timestamp  INTEGER
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS stories (
        id         SERIAL PRIMARY KEY,
        episode_id TEXT NOT NULL REFERENCES episodes(youtube_id) ON DELETE CASCADE,
        headline   TEXT,
        summary    TEXT,
        timestamp  INTEGER
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS chunks (
        id         SERIAL PRIMARY KEY,
        episode_id TEXT  NOT NULL REFERENCES episodes(youtube_id) ON DELETE CASCADE,
        text       TEXT  NOT NULL,
        start_time REAL,
        end_time   REAL,
        embedding  vector(384)
    );
""")

print("Creating indexes...")

cur.execute("""
    CREATE INDEX IF NOT EXISTS idx_concept_mentions_concept
    ON concept_mentions(concept_id);
""")

cur.execute("""
    CREATE INDEX IF NOT EXISTS idx_concept_mentions_episode
    ON concept_mentions(episode_id);
""")

cur.execute("""
    CREATE INDEX IF NOT EXISTS idx_profile_mentions_profile
    ON profile_mentions(profile_id);
""")

cur.execute("""
    CREATE INDEX IF NOT EXISTS idx_profile_mentions_episode
    ON profile_mentions(episode_id);
""")

cur.execute("""
    CREATE INDEX IF NOT EXISTS idx_stories_episode
    ON stories(episode_id);
""")

cur.execute("""
    CREATE INDEX IF NOT EXISTS idx_chunks_episode
    ON chunks(episode_id);
""")

conn.commit()
cur.close()
conn.close()

print("Done. All tables and indexes created.")
