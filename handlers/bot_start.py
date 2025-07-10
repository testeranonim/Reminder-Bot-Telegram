from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart

start_router = Router()

@start_router.message(CommandStart())
async def start(message: Message):
    photo = FSInputFile('data\\cat.jpg')
    text_message = (
        f'Привет, <b>{message.from_user.first_name}</b>!\n\nНиже предоставлен список всех активных команд'
        '\n\n/add — добавить напоминание в список'
        '\n/list — показать все записи'
    )
    await message.answer_photo(photo=photo, caption=text_message)