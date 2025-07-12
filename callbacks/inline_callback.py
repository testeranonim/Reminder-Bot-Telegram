
from aiogram import Router, F, types
from aiogram.types import InputMediaPhoto, FSInputFile
from aiogram.fsm.context import FSMContext

from db.database import add_user, add_reminder

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
        '\n/list — показать все записи'
    )
    photo = InputMediaPhoto(
        media=FSInputFile('data\\cat.jpg'), 
        caption=text_message)
    await callback.message.edit_media(media=photo, reply_markup=kbs.menu)
    await callback.answer()


# Обработка выбора времени
@call_router.callback_query(lambda c: c.data.startswith('time_'), AddMemory.waiting_for_time)
async def process_time(callback: types.CallbackQuery, state: FSMContext) -> None:

    time_digits = callback.data.replace('time_', '').zfill(4)
    time_formatted = f"{time_digits[:2]}:{time_digits[2:]}"
    
    # Сохраняем время в состояние
    await state.update_data(time=time_formatted)
    
    await callback.message.edit_text(
        f'Напоминание будет сохранено как:\n\n'
        f'<blockquote>{(await state.get_data())["text_to_save"]}</blockquote>\n'
        f'🕐 Время: {time_formatted}',
        reply_markup=kbs.complete
    )
    await callback.answer()


# Обработка записи в бд
@call_router.callback_query(F.data == 'complete', AddMemory.waiting_for_time)
async def complete_note(callback: types.CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    
    try:
        await add_user(
            user_id=callback.from_user.id,
            first_name=callback.from_user.first_name
        )
        
        # Сохраняем напоминание с временем
        await add_reminder(
            user_id=callback.from_user.id,
            text=data['text_to_save'],
            remind_at=data['time']
        )
        
        await callback.message.edit_text('✅ Напоминание успешно сохранено!')
        
    except Exception as e:
        await callback.message.edit_text(
            f'❌ Ошибка при сохранении:\n{str(e)}\n\nПопробуйте снова через /add'
        )
    
    finally:
        await state.clear()