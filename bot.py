import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import BOT_TOKEN
from database.db import db_start

from scheduler import start_scheduler

from handlers.start import router as start_router
from handlers.quitting import router as quitting_router
from handlers.status import router as status_router
from handlers.delete_account import router as delete_account_router
from handlers.about import router as about_router


logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

dp.include_router(start_router)
dp.include_router(quitting_router)
dp.include_router(status_router)
dp.include_router(delete_account_router)
dp.include_router(about_router)



async def main():
    await db_start()
    start_scheduler(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Бот остановлен")
    finally:
        bot.session.close()