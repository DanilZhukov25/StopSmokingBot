import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env файле!")

DAILY_NOTIFICATION_HOUR = 9
DAILY_NOTIFICATION_MINUTE = 0
DAILY_NOTIFICATION_SECOND = 0

NOTIFICATION_DELAY = 0.1