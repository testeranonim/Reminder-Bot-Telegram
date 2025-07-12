import aiosqlite

# id - номер для юзера, который будет увеличиватся в зависимости от кол-во пользователей в бд
# user_id - айди юзера в тг
# first_name - для более удобной читабельности
# created_at - время и дата, когда должно придти уведомление

async def init_db():
    async with aiosqlite.connect('memory.db') as db:
        cursor = await db.cursor()
        
        await db.execute("PRAGMA foreign_keys = ON")
        
        # Таблица пользователей
        await cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            first_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # Таблица напоминаний
        await cursor.execute('''
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            remind_at TEXT NOT NULL,
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

async def add_reminder(user_id: int, text: str, remind_at: str) -> None:
    """Добавление напоминания с указанием времени"""
    async with aiosqlite.connect('memory.db') as db:
        await db.execute("PRAGMA foreign_keys = ON")
        await db.execute(
            "INSERT INTO reminders (user_id, text, remind_at) VALUES (?, ?, ?)",
            (user_id, text, remind_at)
        )
        await db.commit()