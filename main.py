import asyncio
import os
import sqlite3
import logging

from aiogram import Router, Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram.client.bot import DefaultBotProperties

from handlers import bot_commands, bot_start

from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)

router = Router()
load_dotenv()

token = os.getenv('token')

async def main():
    dp = Dispatcher()
    bot = Bot(token, default=DefaultBotProperties(parse_mode='HTML'))
    
    async def set_commands():
        commands = [
            BotCommand(command='start', description='Ехала'),
            BotCommand(command='add', description='Добавить напоминание'),
            BotCommand(command='list', description='Все записи')
        ]
        await bot.set_my_commands(commands, BotCommandScopeDefault())
    
    dp.include_routers(
        bot_start.start_router,
        bot_commands.add_router,
    )
    
    dp.include_router(router)
    await set_commands()
    await bot.delete_webhook(drop_pending_updates=True)
    
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())