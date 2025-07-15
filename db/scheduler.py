import asyncio
from aiogram import Bot
from db.database import get_due_reminders, delete_reminder
import logging

logger = logging.getLogger(__name__)

async def check_reminders(bot: Bot):
    """Фоновая задача для проверки и отправки напоминаний"""
    
    logger.info("Планировщик напоминаний запущен")
    
    while True:
        try:
            # получение напоминаний, время которых наступило
            reminders = await get_due_reminders()
            
            if reminders:
                logger.info(f"Найдено {len(reminders)} напоминаний для отправки")
                
            for reminder in reminders:
                reminder_id, user_id, text, remind_at_time = reminder
                try:
                    await bot.send_message(
                        chat_id=user_id,
                        text=f"⏰ Напоминание: {text}"
                    )
                    # удалиение 
                    await delete_reminder(reminder_id)
                    logger.info(f"Отправлено и удалено напоминание {reminder_id} (время: {remind_at_time})")
                except Exception as e:
                    logger.error(f"Ошибка отправки напоминания {reminder_id}: {str(e)}")
            
            await asyncio.sleep(60) # паузы
        
        except Exception as e:
            logger.critical(f"Критическая ошибка в планировщике: {str(e)}")
            await asyncio.sleep(60)  # Перезапуск после паузы