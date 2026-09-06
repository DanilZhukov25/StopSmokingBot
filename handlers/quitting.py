from datetime import datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from keyboards.choise_keyboard import get_yes_or_no_keyboard, get_enable_money_count_keyboard
from database.requests import db_add_user, update_user_column
from states.quitting import QuitSetup

router = Router()


@router.callback_query(F.data == "start_quitting")
async def process_progress_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "Ты готов бросить курить прямо сейчас? Это действие запустит отсчёт времени без сигарет.",
        reply_markup=get_yes_or_no_keyboard())
    await callback.answer()


@router.callback_query(F.data == "confirm_quit_yes")
async def confirm_quit(callback: CallbackQuery):
    await db_add_user(
        callback.from_user.id,
        datetime.now().isoformat()
    )
    await callback.message.edit_text(
        text="Отлично!\nХочешь, я буду считать, сколько денег ты экономишь на невыкуренных сигаретах? Для этого укажи, сколько ты тратил в день на сигареты (в рублях/евро/долларах)",
        reply_markup=get_enable_money_count_keyboard())
    await callback.answer()


@router.callback_query(F.data == "confirm_quit_no")
async def refuse_quit(callback: CallbackQuery):
    await callback.message.edit_text(
        "Хорошо, я здесь, когда будешь готов. Нажми /start, чтобы начать заново.")
    await callback.answer()


@router.callback_query(F.data == "enable_money_no")
async def refuse_money_checker(callback: CallbackQuery):
    await callback.message.edit_text(
        "Хорошо! Я буду считать только твоё время без курения. Используй /status, чтобы проверить прогресс.")


@router.callback_query(F.data == "enable_money_yes")
async def enable_money_yes(
        callback: CallbackQuery,
        state: FSMContext,
):
    await state.set_state(QuitSetup.waiting_for_daily_expense)

    await callback.message.edit_text(
        "Напиши сумму, которую ты тратил на сигареты в день "
        "(только число, например: 200)."
    )

    await callback.answer()


@router.message(QuitSetup.waiting_for_daily_expense)
async def process_daily_expense(
        message: Message,
        state: FSMContext,
):
    try:
        daily_expense = float(message.text.replace(",", "."))
    except (ValueError, AttributeError):
        await message.answer(
            "Пожалуйста, введи корректное число."
        )
        return

    if daily_expense < 0:
        await message.answer(
            "Пожалуйста, введи корректное число."
        )
        return

    await update_user_column(
        message.from_user.id,
        "daily_expense",
        daily_expense,
    )

    await state.clear()

    await message.answer(
        "Отлично! Теперь я считаю твоё время без курения "
        "и сэкономленные деньги. Используй /status, "
        "чтобы проверить прогресс."
    )
