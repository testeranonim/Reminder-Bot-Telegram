import aiosqlite
import logging

# id - номер для юзера, который будет увеличиватся в зависимости от кол-во пользователей в бд
# user_id - айди юзера в тг
# first_name - для более удобной читабельности
# created_at - время и дата, когда должно придти уведомление

async def init_db():
    async with aiosqlite.connect('memory.db') as db:
        # Включаем поддержку внешних ключей
        await db.execute("PRAGMA foreign_keys = ON")
        
        # Создаем таблицы напрямую через db.execute
        await db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            first_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        await db.execute('''
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            remind_at TIMESTAMP NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )''')
        
        await db.commit()


async def add_user(user_id: int, first_name: str) -> None:
    """Добавления юзера, если его ещё нет в базе"""
    async with aiosqlite.connect('memory.db') as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id, first_name) VALUES (?, ?)", (user_id, first_name)
        )
        await db.commit()

async def add_reminder(user_id: int, text: str, remind_at: str):
    """Добавляем напоминание с указанной датой/временем"""
    async with aiosqlite.connect('memory.db') as db:
        await db.execute("PRAGMA foreign_keys = ON")
        await db.execute(
            "INSERT INTO reminders (user_id, text, remind_at) VALUES (?, ?, ?)",
            (user_id, text, remind_at)
        )
        await db.commit()

async def get_due_reminders():
    logger = logging.getLogger(__name__)
    """Получает напоминания, время которых наступило"""
    async with aiosqlite.connect('memory.db') as db:
        
        cursor = await db.execute("SELECT datetime('now', 'localtime')")
        current_time = await cursor.fetchone()
        logger.info(f"Текущее время в БД: {current_time[0]}")
        
        cursor = await db.execute(
            "SELECT id, user_id, text, remind_at FROM reminders "  # Пробел в конце важен!
            "WHERE datetime(remind_at) <= datetime('now', 'localtime')"
        )
        reminders = await cursor.fetchall()
        
        if reminders:
            logger.info(f"Найдено {len(reminders)} напоминаний для отправки")
            for rem in reminders:
                logger.info(f"ID: {rem[0]}, User: {rem[1]}, Text: {rem[2]}, Time: {rem[3]}")
        else:
            logger.info("Активных напоминаний для отправки не найдено")
        
        return reminders

async def delete_reminder(reminder_id: int):
    """Удаляет напоминание по ID"""
    async with aiosqlite.connect('memory.db') as db:
        await db.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
        await db.commit()