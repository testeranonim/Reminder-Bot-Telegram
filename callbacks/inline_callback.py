
from aiogram import Router, F, types
from aiogram.types import InputMediaPhoto, FSInputFile
from aiogram.fsm.context import FSMContext

from keyboards import kbs
from states.state_add import AddMemory

call_router = Router()

# Изменение текста, добавив фото
@call_router.callback_query(F.data == 'back')
async def back(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    text_message = (
        f'Привет, <b>{callback.from_user.first_name}</b>!\n\nНиже предоставлен список всех активных команд'
        '\n\n/add — добавить напоминание в список'
        '\n/list — показать все активные записи'
        '\n\nДля использования команды /add используется следующий формат:'
        '\n<blockquote>/add Позвонить маме 2025-07-15 13:00</blockquote>'
        '\nГОД-МЕСЯЦ-ЧИСЛО ЧЧ:ММ'
    )
    photo = InputMediaPhoto(
        media=FSInputFile('data\\cat.jpg'), 
        caption=text_message)
    await callback.message.edit_media(media=photo, reply_markup=kbs.menu)
    await callback.answer()