import asyncio
import os
import logging

from aiogram import Router, Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram.client.bot import DefaultBotProperties

from handlers import command_add, command_start
from callbacks import inline_callback
from db.database import init_db
from db.scheduler import check_reminders

from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)

router = Router()
load_dotenv()

token = os.getenv('token')

async def main():
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - $(message)s'
    )
    
    dp = Dispatcher()
    bot = Bot(token, default=DefaultBotProperties(parse_mode='HTML'))
    
    await init_db()
    asyncio.create_task(check_reminders(bot))
    
    async def set_commands():
        commands = [
            BotCommand(command='start', description='Ехала'),
            BotCommand(command='add', description='Добавить напоминание'),
            BotCommand(command='list', description='Все записи')
        ]
        await bot.set_my_commands(commands, BotCommandScopeDefault())
    
    dp.include_routers(
        command_start.start_router,
        command_add.add_router,
        inline_callback.call_router,
    )
    
    dp.include_router(router)
    await set_commands()
    await bot.delete_webhook(drop_pending_updates=True)
    
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())