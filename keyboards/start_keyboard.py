from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_main_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="🚭 Начать бросать курить", callback_data="start_quitting")
    builder.button(text="ℹ️ Как это работает", callback_data="how_it_works")
    builder.button(text="📖 О проекте", callback_data="about_project")

    builder.adjust(1, 1)  # 1 кнопка в ряду (вертикально)

    return builder.as_markup()

def get_main_keyboard_already_started() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="ℹ️ Как это работает", callback_data="how_it_works")
    builder.button(text="❌ Удалить профиль", callback_data="delete_account")
    builder.button(text="📖 О проекте", callback_data="about_project")

    builder.adjust(1, 1)  # 1 кнопка в ряду (вертикально)

    return builder.as_markup()