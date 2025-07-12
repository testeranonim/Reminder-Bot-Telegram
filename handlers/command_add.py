
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards.clock import clock_builder
from states.state_add import AddMemory

add_router = Router()

@add_router.message(Command('add'))
async def add(message: Message, state: FSMContext) -> None:
    
    parts = message.text.split(maxsplit=1) # разделить ток по первому пробелу
    
    await state.update_data(text_to_save=parts[1]) # сохранение текста в состояние
    
    if len(parts) < 2:
        await message.reply('Пожалуйста, укажите напоминание после команды /add')
        return
    
    keyboard = await clock_builder()
    await message.answer(
        f'Ваше напоминание:\n\n<blockquote>{parts[1]}</blockquote>\n\n'
        'Выберите время уведомления:',
        reply_markup=keyboard
    )
    
    await state.set_state(AddMemory.waiting_for_time)