from aiogram.fsm.state import StatesGroup, State

class AddMemory(StatesGroup):
    waiting_for_time = State()