import sqlite3
import time
from errors import ExecutionError

DB_PATH = "data.db"


def execute(sql: str) -> dict:
    t0 = time.perf_counter()
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        conn.close()
        elapsed = (time.perf_counter() - t0) * 1000
        return {"columns": columns, "rows": rows, "time_ms": round(elapsed, 2)}
    except sqlite3.Error as e:
        raise ExecutionError(f"Database error: {e}")
