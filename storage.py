import sqlite3
from typing import Optional, Dict, Any

DB_PATH = "analysis.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS analyses (
            id TEXT PRIMARY KEY,
            filename TEXT,
            query TEXT,
            verification TEXT,
            analysis TEXT,
            risk TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        )
        """
    )
    conn.commit()
    conn.close()

def save_result(
    analysis_id: str,
    filename: str,
    query: str,
    verification: str,
    analysis: str,
    risk: str,
):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        INSERT OR REPLACE INTO analyses (id, filename, query, verification, analysis, risk)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (analysis_id, filename, query, verification, analysis, risk),
    )
    conn.commit()
    conn.close()

def get_result(analysis_id: str) -> Optional[Dict[str, Any]]:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT id, filename, query, verification, analysis, risk, created_at FROM analyses WHERE id = ?",
        (analysis_id,),
    )
    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "id": row[0],
        "filename": row[1],
        "query": row[2],
        "verification": row[3],
        "analysis": row[4],
        "risk": row[5],
        "created_at": row[6],
    }