
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

async def clock_builder() -> InlineKeyboardMarkup:
    """Создает клавиатуру с выбором времени"""
    
    times = [f"{hour}:00" for hour in range(8, 24)] # динамически создаёт время с 8 утра по 23 часов
    
    builder = InlineKeyboardBuilder()
    
    for time in times:
        builder.button(text=time, callback_data=f"time_{time.replace(':', '')}")
    builder.adjust(4, 4, 4, 4)
    
    return builder.as_markup()