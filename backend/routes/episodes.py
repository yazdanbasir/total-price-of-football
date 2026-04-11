from fastapi import APIRouter, HTTPException
from database import getDB

router = APIRouter()


@router.get("/episodes")
def listEpisodes(page: int = 1, limit: int = 50):
    offset = (page - 1) * limit
    with getDB() as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM episodes")
        total = cur.fetchone()[0]
        cur.execute(
            """
            SELECT youtube_id, title, published_at, duration, thumbnail, description
            FROM episodes
            ORDER BY published_at DESC
            LIMIT %s OFFSET %s
            """,
            (limit, offset),
        )
        rows = cur.fetchall()
        cur.close()

    episodes = [
        {
            "youtubeID": r[0],
            "title": r[1],
            "publishedAt": r[2].isoformat() if r[2] else None,
            "duration": r[3],
            "thumbnail": r[4],
            "description": r[5],
        }
        for r in rows
    ]
    return {"total": total, "page": page, "limit": limit, "episodes": episodes}


@router.get("/episodes/{youtubeID}")
def getEpisode(youtubeID: str):
    with getDB() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT youtube_id, title, published_at, duration, thumbnail, description
            FROM episodes WHERE youtube_id = %s
            """,
            (youtubeID,),
        )
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Episode not found")

        cur.execute(
            """
            SELECT c.id, c.term, cm.timestamp
            FROM concept_mentions cm
            JOIN concepts c ON c.id = cm.concept_id
            WHERE cm.episode_id = %s
            ORDER BY cm.timestamp ASC NULLS LAST
            """,
            (youtubeID,),
        )
        concepts = [
            {"id": r[0], "term": r[1], "timestamp": r[2]}
            for r in cur.fetchall()
        ]

        cur.execute(
            """
            SELECT p.id, p.name, p.type, pm.timestamp
            FROM profile_mentions pm
            JOIN profiles p ON p.id = pm.profile_id
            WHERE pm.episode_id = %s
            ORDER BY pm.timestamp ASC NULLS LAST
            """,
            (youtubeID,),
        )
        profiles = [
            {"id": r[0], "name": r[1], "type": r[2], "timestamp": r[3]}
            for r in cur.fetchall()
        ]

        cur.execute(
            """
            SELECT id, headline, summary, timestamp
            FROM stories
            WHERE episode_id = %s
            ORDER BY timestamp ASC NULLS LAST
            """,
            (youtubeID,),
        )
        stories = [
            {"id": r[0], "headline": r[1], "summary": r[2], "timestamp": r[3]}
            for r in cur.fetchall()
        ]
        cur.close()

    return {
        "youtubeID": row[0],
        "title": row[1],
        "publishedAt": row[2].isoformat() if row[2] else None,
        "duration": row[3],
        "thumbnail": row[4],
        "description": row[5],
        "concepts": concepts,
        "profiles": profiles,
        "stories": stories,
    }
