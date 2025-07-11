import aiosqlite
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from db.database import add_reminder, add_user
from states.state_add import AddMemory
from keyboards import kbs

add_router = Router()

@add_router.message(Command('add'))
async def add(message: Message, state: FSMContext) -> None:
    
    parts = message.text.split(maxsplit=1) # разделить ток по первому пробелу
    
    if len(parts) < 2:
        await message.reply('Пожалуйста, укажите напоминание после команды /add')
        return
    
    text_to_save = parts[1]
    
    try:
        await add_user(
            user_id=message.from_user.id,
            first_name=message.from_user.first_name
        )
        
        await add_reminder(
            user_id=message.from_user.id,
            text=text_to_save
        )

        await message.answer(f'Ваше напоминание сохранится как:\n\n<blockquote>{text_to_save}</blockquote>', reply_markup=kbs.back)
        
        await state.set_state(AddMemory.add)
        await state.update_data(memory = text_to_save)
    
    except Exception as e:
        await message.reply(f'❌ Ошибка: {e}\n\nПопробуйте позже!')

# @add_router.message(AddMemory.add, F.text)
# async def process_add_memory(message: Message, state: FSMContext) -> None:
#     await state.update_data()
#     await 