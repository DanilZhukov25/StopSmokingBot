from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_yes_or_no_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="✅ Да, я готов", callback_data="confirm_quit_yes")
    builder.button(text="❌ Нет, позже", callback_data="confirm_quit_no")

    builder.adjust(1, 1)

    return builder.as_markup()

def get_enable_money_count_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="💰 Да, считать деньги", callback_data="enable_money_yes")
    builder.button(text="Пропустить ", callback_data="enable_money_no")

    builder.adjust(1, 1)

    return builder.as_markup()