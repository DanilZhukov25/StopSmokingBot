import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from config import DAILY_NOTIFICATION_HOUR, DAILY_NOTIFICATION_MINUTE, NOTIFICATION_DELAY
from database.requests import db_get_all_users
from aiogram import Bot
from datetime import datetime

scheduler = AsyncIOScheduler()


async def send_daily_motivation(bot: Bot):
    users = await db_get_all_users()  # список telegram_id с quit_date

    for i, user in enumerate(users):
        telegram_id = user[0]
        quit_date_str = user[1]

        if not quit_date_str:
            continue  # пользователь ещё не начал бросать

        # Расчёт времени без курения (для персонализации)
        quit_date = datetime.fromisoformat(quit_date_str)
        elapsed = datetime.now() - quit_date
        days = elapsed.days

        # Мотивационное сообщение
        if days == 0:
            motivation = "🎉 Первый день без курения — самый сложный, и ты уже справился! Держись!"
        elif days < 3:
            motivation = f"🔥 Уже {days} дн. без сигарет! Самый трудный период позади, ты молодец!"
        elif days < 7:
            motivation = f"💪 {days} дн. без курения — твой организм уже благодарит тебя! Продолжай!"
        elif days < 30:
            motivation = f"🏆 {days} дн. без сигарет — это серьёзный результат! Ты на правильном пути!"
        else:
            motivation = f"🌟 {days} дн. без курения — ты настоящий герой! Гордись собой!"

        try:
            await bot.send_message(
                telegram_id,
                f"☀️ Доброе утро! Время проверить твой прогресс.\n\n"
                f"{motivation}\n\n"
                f"Напиши /status, чтобы увидеть актуальный отсчёт."
            )
        except Exception as e:
            logging.error(f"Не удалось отправить сообщение пользователю {telegram_id}: {e}")

        # Задержка между сообщениями (0.1 сек = 100 мс, ~10 сообщений в секунду)
        if i < len(users) - 1:  # не спать после последнего сообщения
            await asyncio.sleep(NOTIFICATION_DELAY)


def start_scheduler(bot: Bot):
    trigger = CronTrigger(
        hour=DAILY_NOTIFICATION_HOUR,
        minute=DAILY_NOTIFICATION_MINUTE,
        second=0
    )

    scheduler.add_job(
        send_daily_motivation,
        trigger=trigger,
        args=[bot],
        id="daily_motivation",
        replace_existing=True
    )

    scheduler.start()