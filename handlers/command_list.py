from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.database import get_user_reminders, count_user_reminders

list_router = Router()

@list_router.message(Command('list'))
async def list(message: Message):
    user_id = message.from_user.id
    page = 1
    per_page = 1
    
    reminders = await get_user_reminders(user_id, page, per_page)
    total_count = await count_user_reminders(user_id)
    total_pages = (total_count + per_page - 1) // per_page
    
    if not reminders:
        return await message.answer('📭 У вас нет напоминаний')
    
    response = [f'📋 Ваши напоминания (страница {page}/{total_pages}):\n']
    for _, text, remind_at in reminders:
        from datetime import datetime
        
        remind_time = datetime.fromisoformat(remind_at)
        formatted_time = remind_time.strftime("%d.%m.%Y %H:%M")
        response.append(f'{text} - {formatted_time}')
        
    builder = InlineKeyboardBuilder()
    if page > 1:
        builder.button(text='⬅️ Назад', callback_data=f'prev_{page-1}')
    if page < total_pages:
        builder.button(text='Вперед ➡️', callback_data=f'next_{page+1}')
    
    await message.answer(
        '\n'.join(response),
        reply_markup=builder.as_markup() if builder.buttons else None
    )