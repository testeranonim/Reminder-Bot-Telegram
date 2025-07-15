
import re
from datetime import datetime
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from db.database import add_reminder, add_user

add_router = Router()

from datetime import datetime
import re

@add_router.message(Command('add'))
async def add_with_datetime(message: Message):
    # Убираем команду и разделяем оставшийся текст
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return await message.reply("❌ Формат: /add текст ГГГГ-ММ-ДД ЧЧ:ММ\nПример: /add Позвонить маме 2025-07-15 13:00")
    
    input_text = parts[1]
    
    # Ищем дату и время в формате ГГГГ-ММ-ДД ЧЧ:ММ (разрешаем 1-2 цифры для часов)
    match = re.search(r'(\d{4}-\d{2}-\d{2}) (\d{1,2}:\d{2})$', input_text)
    if not match:
        return await message.reply("❌ Неверный формат даты/времени. Используйте: ГГГГ-ММ-ДД ЧЧ:ММ")
    
    # Извлекаем компоненты
    date_str = match.group(1)
    time_str = match.group(2)
    reminder_text = input_text[:match.start()].strip()
    
    if not reminder_text:
        return await message.reply("❌ Текст напоминания не может быть пустым")
    
    try:
        # Нормализуем время (добавляем ведущий ноль при необходимости)
        if len(time_str.split(':')[0]) == 1:
            time_str = f"0{time_str}"  # "9:00" → "09:00"
        
        # Собираем полную дату
        remind_at = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        remind_at_str = remind_at.strftime("%Y-%m-%d %H:%M:%S")
        
        # Проверяем что дата в будущем
        if remind_at <= datetime.now():
            return await message.reply("❌ Укажите дату/время в будущем")
        
        # Сохраняем пользователя (если нужно)
        await add_user(
            user_id=message.from_user.id,
            first_name=message.from_user.first_name
        )
        
        # Сохраняем напоминание
        await add_reminder(
            user_id=message.from_user.id,
            text=reminder_text,
            remind_at=remind_at_str
        )
        
        await message.reply(
            f"✅ Напоминание сохранено!\n\n"
            f"📝 Текст: {reminder_text}\n"
            f"⏰ Когда: {remind_at.strftime('%d.%m.%Y в %H:%M')}"
        )
    
    except ValueError as e:
        error_detail = str(e)
        if "time data" in error_detail:
            await message.reply("❌ Неверный формат времени. Используйте ЧЧ:ММ (например 09:00 или 23:59)")
        else:
            await message.reply(f"❌ Ошибка в дате: {error_detail}")
    except Exception as e:
        await message.reply(f"❌ Ошибка: {str(e)}")