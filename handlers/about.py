from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F
from aiogram.types import CallbackQuery

from keyboards.start_keyboard import get_main_keyboard

router = Router()


@router.message(Command("about"))
async def cmd_about(message: Message):
    await message.answer(
        "📖 <b>О проекте</b>\n\n"
        "Этот бот разработан на личном опыте. Автор сам находится в процессе отказа от курения "
        "и прекрасно понимает, насколько это сложный путь.\n\n"
        "Будет круто, если у автора получится бросить эту вредную привычку, которая гробит здоровье "
        "и тратит деньги. И ещё круче — если этот бот поможет тебе сделать то же самое! 💪\n\n"
        "🚭 <b>Помни:</b> каждый день без сигареты — это победа. Ты не один на этом пути!",
        reply_markup=get_main_keyboard()

    )


@router.callback_query(F.data == "about_project")
async def process_about_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "📖 <b>О проекте</b>\n\n"
        "Этот бот разработан на личном опыте. Автор сам находится в процессе отказа от курения "
        "и прекрасно понимает, насколько это сложный путь.\n\n"
        "Будет круто, если у автора получится бросить эту вредную привычку, которая гробит здоровье "
        "и тратит деньги. И ещё круче — если этот бот поможет тебе сделать то же самое! 💪\n\n"
        "🚭 <b>Помни:</b> каждый день без сигареты — это победа. Ты не один на этом пути!",
        reply_markup=get_main_keyboard()
    )
    await callback.answer()
