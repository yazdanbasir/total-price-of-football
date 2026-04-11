import os
import psycopg2
import psycopg2.pool
from contextlib import contextmanager
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent / ".env")

databaseURL = os.getenv("DATABASE_URL")
if not databaseURL:
    raise EnvironmentError("DATABASE_URL not set in backend/.env")

pool = psycopg2.pool.SimpleConnectionPool(1, 10, databaseURL)


@contextmanager
def getDB():
    conn = pool.getconn()
    try:
        yield conn
    finally:
        pool.putconn(conn)
