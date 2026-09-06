from aiogram.fsm.state import State, StatesGroup


class QuitSetup(StatesGroup):
    waiting_for_daily_expense = State()
