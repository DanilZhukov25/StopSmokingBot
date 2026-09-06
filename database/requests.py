import aiosqlite
from database.db import DB_PATH


async def db_add_user(telegram_id: int, quit_date: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (telegram_id, quit_date) VALUES (?, ?)",
            (telegram_id, quit_date)
        )
        await db.commit()


async def db_get_user(telegram_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            """
            SELECT telegram_id, quit_date, daily_expense
            FROM users
            WHERE telegram_id = ?
            """,
            (telegram_id,),
        )

        return await cursor.fetchone()


async def update_user_column(
        telegram_id: int,
        column: str,
        value,
):
    allowed_columns = {
        "telegram_id",
        "quit_date",
        "created_at",
        "daily_expense"
    }

    if column not in allowed_columns:
        raise ValueError(f"Недопустимая колонка: {column}")

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            f"""
            UPDATE users
            SET {column} = ?
            WHERE telegram_id = ?
            """,
            (value, telegram_id),
        )
        await db.commit()


async def db_delete_user(telegram_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "DELETE FROM users WHERE telegram_id = ?",
            (telegram_id,),
        )
        await db.commit()


async def db_get_all_users():
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT telegram_id, quit_date FROM users WHERE quit_date IS NOT NULL"
        )
        return await cursor.fetchall()
