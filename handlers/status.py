from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message

from database.requests import db_get_user

from datetime import datetime

router = Router()


@router.message(Command("status"))
async def cmd_status(message: Message):
    telegram_id = message.from_user.id

    user = await db_get_user(telegram_id)

    if user is None:
        await message.answer(
            "Ты ещё не начал бросать курить. "
            "Нажми /start, чтобы начать."
        )
        return

    _, quit_date, daily_expense = user

    if quit_date is None:
        await message.answer(
            "Ты ещё не начал бросать курить. "
            "Нажми /start, чтобы начать."
        )
        return

    quit_date = datetime.fromisoformat(quit_date)

    elapsed = datetime.now() - quit_date

    total_seconds = int(elapsed.total_seconds())

    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60

    text = (
        f"⏱️ Время без курения: "
        f"{days} дн. {hours} ч. {minutes} мин."
    )

    if daily_expense and daily_expense > 0:
        saved_money = (
            elapsed.total_seconds() * daily_expense
        ) / 86400

        text += f"\n💰 Ты сэкономил: {saved_money:.2f} ₽"

    await message.answer(text)