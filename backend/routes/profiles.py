from fastapi import APIRouter, HTTPException
from database import getDB

router = APIRouter()

VALID_TYPES = {"person", "club", "organisation", "body"}


@router.get("/profiles")
def listProfiles(search: str = "", type: str = "", page: int = 1, limit: int = 50):
    offset = (page - 1) * limit
    conditions = []
    params = []

    if search:
        conditions.append("name ILIKE %s")
        params.append(f"%{search}%")
    if type and type in VALID_TYPES:
        conditions.append("type = %s")
        params.append(type)

    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""

    with getDB() as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT COUNT(*) FROM profiles {where}", params)
        total = cur.fetchone()[0]
        cur.execute(
            f"""
            SELECT id, name, type, description
            FROM profiles
            {where}
            ORDER BY name ASC
            LIMIT %s OFFSET %s
            """,
            params + [limit, offset],
        )
        rows = cur.fetchall()
        cur.close()

    profiles = [
        {"id": r[0], "name": r[1], "type": r[2], "description": r[3]}
        for r in rows
    ]
    return {"total": total, "page": page, "limit": limit, "profiles": profiles}


@router.get("/profiles/{profileID}")
def getProfile(profileID: int):
    with getDB() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, name, type, description FROM profiles WHERE id = %s",
            (profileID,),
        )
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Profile not found")

        cur.execute(
            """
            SELECT e.youtube_id, e.title, e.published_at, e.thumbnail, pm.timestamp
            FROM profile_mentions pm
            JOIN episodes e ON e.youtube_id = pm.episode_id
            WHERE pm.profile_id = %s
            ORDER BY e.published_at ASC
            """,
            (profileID,),
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
        "name": row[1],
        "type": row[2],
        "description": row[3],
        "mentions": mentions,
    }
