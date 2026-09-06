from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from database.requests import db_delete_user


router = Router()


@router.message(Command("delete_account"))

async def process_delete_account(message: Message):
    telegram_id = message.from_user.id

    await db_delete_user(telegram_id)

    await message.answer(
        "👋 Твой аккаунт и все сохранённые данные удалены.\n\n"
        "Спасибо, что доверился мне на этом пути. "
        "Помни: решение бросить курить — уже важный шаг. 🌱\n\n"
        "Если когда-нибудь захочешь начать снова, я буду здесь. "
        "Береги себя и не сдавайся. 💪"
    )


@router.callback_query(F.data == "delete_account")
async def process_delete_account_callback(callback: CallbackQuery):
    telegram_id = callback.from_user.id
    await db_delete_user(telegram_id)

    await callback.message.edit_text(
        "👋 Твой аккаунт и все сохранённые данные удалены.\n\n"
        "Спасибо, что доверился мне на этом пути. "
        "Помни: решение бросить курить — уже важный шаг. 🌱\n\n"
        "Если когда-нибудь захочешь начать снова, я буду здесь. "
        "Береги себя и не сдавайся. 💪"
    )
    await callback.answer()
