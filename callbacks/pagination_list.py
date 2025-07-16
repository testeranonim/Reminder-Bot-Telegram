
from aiogram import Router, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from db.database import get_user_reminders, count_user_reminders

call_router = Router()

@call_router.callback_query(lambda c: c.data.startswith(("prev_", "next_")))
async def handle_pagination(callback: types.CallbackQuery):
    action, page_str = callback.data.split("_")
    page = int(page_str)
    user_id = callback.from_user.id
    per_page = 1
    
    # получение записи для новой страницы
    reminders = await get_user_reminders(user_id, page, per_page)
    total_count = await count_user_reminders(user_id)
    total_pages = (total_count + per_page - 1) // per_page
    
    # обнова соо
    response = [f"📋 Ваши напоминания (страница {page}/{total_pages}):\n"]
    for _, text, remind_at in reminders:
        from datetime import datetime
        
        remind_time = datetime.fromisoformat(remind_at)
        formatted_time = remind_time.strftime("%d.%m.%Y %H:%M")
        response.append(f'{text} - {formatted_time}')
    
    builder = InlineKeyboardBuilder()
    if page > 1:
        builder.button(text="⬅️ Назад", callback_data=f"prev_{page-1}")
    if page < total_pages:
        builder.button(text="Вперед ➡️", callback_data=f"next_{page+1}")
    
    await callback.message.edit_text(
        "\n".join(response),
        reply_markup=builder.as_markup() if builder.buttons else None
    )
    await callback.answer()