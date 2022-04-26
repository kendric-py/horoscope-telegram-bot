from ast import In
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.keyboard_button import KeyboardButton




def render_menu():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text='📊 Статистика', callback_data='admin&stats'),
        InlineKeyboardButton(text='📑 Каналы', callback_data='admin&chanels'),
        InlineKeyboardButton(text='📝 Рассылка', callback_data='admin&mailing'),
        InlineKeyboardButton(text='👨‍💻 Реферальная система', callback_data='admin&referal'),
        InlineKeyboardButton(text='📥 Выгрузить', callback_data='admin&upload')
    )
    keyboard.adjust(1, 2, 1, 1)
    return(keyboard.as_markup())