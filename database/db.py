import aiosqlite
from pathlib import Path
from config import BASE_DIR

DB_PATH = BASE_DIR / "bot_database.db"

async def db_start():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER PRIMARY KEY,
                quit_date TEXT NOT NULL,
                daily_expense FLOAT DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        await db.commit()