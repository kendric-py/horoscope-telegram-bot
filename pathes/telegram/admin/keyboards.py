from ast import In
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.keyboard_button import KeyboardButton


from loader import db




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


def render_confirm_mailing():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text='✅ Подтвердить', callback_data='admin&confirm_mailing'), 
        InlineKeyboardButton(text='❌ Отмена', callback_data='admin&cancel')
    )
    keyboard.adjust(2)
    return(keyboard.as_markup())


def render_stats_menu():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text='🔄 Обновить', callback_data='admin&refresh_stats'),
        InlineKeyboardButton(text='⬅️ Назад', callback_data='admin&cancel')
    )
    keyboard.adjust(1)
    return(keyboard.as_markup())


def render_chanels_menu(chanels: list):
    keyboard = InlineKeyboardBuilder()
    for chanel in chanels:
        keyboard.add(InlineKeyboardButton(text=chanel.name, callback_data=f'admin&chanel&del&{chanel.id}'))
        keyboard.adjust(2, repeat=True)
    if not(chanels):
        keyboard.add(InlineKeyboardButton(text='Каналы отсутствуют', callback_data='none'))
    keyboard.row(InlineKeyboardButton(text='➕ Добавить', callback_data='admin&chanel&add'))
    keyboard.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='admin&cancel'))
    return(keyboard.as_markup())


def render_back():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='⬅️ Назад', callback_data='admin&cancel'))
    return(keyboard.as_markup())


def render_cancel():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text='⬅️ Отмена', callback_data='admin&cancel')
    )
    keyboard.adjust(1)
    return(keyboard.as_markup())