from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from database.requests import db_get_user
from keyboards.start_keyboard import get_main_keyboard, get_main_keyboard_already_started

router = Router()

HOW_IT_WORKS_START_TEXT = """📘 Как это работает\n

Этот бот помогает тебе бросить курить, отслеживая твой прогресс:\n

Отсчёт времени — я запомню момент, когда ты бросил курить, и буду показывать, сколько времени ты уже продержался без сигарет (дни, часы, минуты).\n

Подсчёт экономии — по желанию я буду считать, сколько денег ты сэкономил на невыкуренных сигаретах. Для этого просто укажи, сколько ты тратил в день.\n

Мотивация — каждый раз, когда захочешь проверить прогресс, напиши /status или нажми кнопку в меню.\n

Ты всегда можешь начать заново — просто напиши /start. Главное — сделать первый шаг! 🚭"""


@router.message(Command("start"))
async def cmd_start(message: Message):
    telegram_id = message.from_user.id

    user = await db_get_user(telegram_id)

    if user is not None and user[1] is not None:
        await message.answer(
            "🌱 Ты уже на пути к жизни без сигарет!\n\n"
            "Каждый день без курения — это ещё один шаг в сторону "
            "лучшего самочувствия, свободы и экономии.\n\n"
            "Я продолжаю считать твой прогресс. Не сдавайся — "
            "даже если иногда бывает тяжело. Главное — продолжать двигаться вперёд. 💪\n\n"
            "⏱️ Используй /status, чтобы посмотреть, сколько времени "
            "ты уже не куришь",
            reply_markup=get_main_keyboard_already_started(),
        )
        return

    # Новый пользователь или пользователь, который ещё не начал отсчёт
    await message.answer(
        "👋 Привет! Я рядом, чтобы помочь тебе отказаться от курения.\n\n"
        "Это не обязательно должно быть легко. Главное — начать. "
        "Каждый час и каждый день без сигарет имеют значение. 🌱\n\n"
        "Что я умею:\n"
        "• Запомню дату и время, когда ты решил бросить курить\n"
        "• Буду считать, сколько времени ты уже не куришь\n"
        "• Буду считать, сколько ты сэкономил на сигаретах\n"
        "• Показывать твой прогресс по команде /status\n\n"
        "Если ты готов попробовать — нажми кнопку ниже. "
        "Начнём с первого шага. 💪",
        reply_markup=get_main_keyboard(),
    )


@router.callback_query(F.data == "how_it_works")
async def process_how_it_works(callback: CallbackQuery):
    await callback.message.edit_text(
        HOW_IT_WORKS_START_TEXT,
        reply_markup=get_main_keyboard(),
    )
    await callback.answer()
