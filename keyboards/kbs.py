from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

back = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Отменить ❌', callback_data='back')
        ]
    ]
)

menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='GitHub 👾', url='https://github.com/testeranonim')
        ]
    ]
)

complete = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Записать 📝', callback_data='complete')
        ]
    ]
)