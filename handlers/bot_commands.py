from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from states.state_add import AddMemory

add_router = Router()

@add_router.message(Command('add'))
async def add(message: Message, state: FSMContext) -> None:
    
    parts = message.text.split(maxsplit=1) # разделить ток по первому пробелу
    
    if len(parts) < 2:
        await message.reply('Пожалуйста, укажите напоминание после команды /add')
        return
    
    text_to_save = parts[1]
    await message.answer(f'Ваше напоминание сохранится как:\n\n<code>{text_to_save}</code>')
    await state.set_state(AddMemory.add)
    await state.update_data(memory = text_to_save)
    
    # data = await state.get_data()
    # await description(message, data)

# async def description(message: Message, data: dict) -> None:
#     memory = data['memory']

#     text = f"""Проверьте свою запись ниже!
#     <code>{memory}</code>
#     """
#     await message.answer(text)
    
    
