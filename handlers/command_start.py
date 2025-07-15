from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart

from keyboards import kbs

start_router = Router()

@start_router.message(CommandStart())
async def start(message: Message):
    photo = FSInputFile('data\\cat.jpg')
    text_message = (
        f'Привет, <b>{message.from_user.first_name}</b>!\n\nНиже предоставлен список всех активных команд'
        '\n\n/add — добавить напоминание в список'
        '\n/list — показать все записи'
        '\n\nДля использования команды /add используется следующий формат:'
        '\n<blockquote>/add Позвонить маме 2025-07-15 13:00'
        '\n/add Сварить рис 2025-07-15 9:45</blockquote>'
        '\nГОД-МЕСЯЦ-ЧИСЛО ЧЧ:ММ'
    )
    await message.answer_photo(photo=photo, caption=text_message, reply_markup=kbs.menu)