from fastapi import APIRouter, HTTPException, Query
from database import getDB

router = APIRouter()


@router.get("/concepts")
def listConcepts(search: str = Query("", max_length=200), page: int = 1, limit: int = Query(50, ge=1, le=10000)):
    offset = (page - 1) * limit
    with getDB() as conn:
        cur = conn.cursor()
        if search:
            pattern = f"%{search}%"
            cur.execute(
                "SELECT COUNT(*) FROM concepts WHERE term ILIKE %s",
                (pattern,),
            )
            total = cur.fetchone()[0]
            cur.execute(
                """
                SELECT id, term, definition
                FROM concepts
                WHERE term ILIKE %s
                ORDER BY term ASC
                LIMIT %s OFFSET %s
                """,
                (pattern, limit, offset),
            )
        else:
            cur.execute("SELECT COUNT(*) FROM concepts")
            total = cur.fetchone()[0]
            cur.execute(
                """
                SELECT id, term, definition
                FROM concepts
                ORDER BY term ASC
                LIMIT %s OFFSET %s
                """,
                (limit, offset),
            )
        rows = cur.fetchall()
        cur.close()

    concepts = [
        {"id": r[0], "term": r[1], "definition": r[2]}
        for r in rows
    ]
    return {"total": total, "page": page, "limit": limit, "concepts": concepts}


@router.get("/concepts/{conceptID}")
def getConcept(conceptID: int):
    with getDB() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, term, definition FROM concepts WHERE id = %s",
            (conceptID,),
        )
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Concept not found")

        cur.execute(
            """
            SELECT e.youtube_id, e.title, e.published_at, e.thumbnail, cm.timestamp
            FROM concept_mentions cm
            JOIN episodes e ON e.youtube_id = cm.episode_id
            WHERE cm.concept_id = %s
            ORDER BY e.published_at ASC
            """,
            (conceptID,),
        )
        mentions = [
            {
                "episodeID": m[0],
                "title": m[1],
                "publishedAt": m[2].isoformat() if m[2] else None,
                "thumbnail": m[3],
                "timestamp": m[4],
            }
            for m in cur.fetchall()
        ]
        cur.close()

    return {
        "id": row[0],
        "term": row[1],
        "definition": row[2],
        "mentions": mentions,
    }
