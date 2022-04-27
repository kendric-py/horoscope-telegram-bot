from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.keyboard_button import KeyboardButton



def render_subscribe(chanels: list):
    keyboard = InlineKeyboardBuilder()
    for chanel in chanels:
        keyboard.add(InlineKeyboardButton(text=chanel.name, url=chanel.url))
    keyboard.adjust(2, repeat=True)
    keyboard.row(InlineKeyboardButton(text='🔄 Проверить', callback_data='user&check_subs'))
    return(keyboard.as_markup())


def render_horoscope():
    horoscopes = [
        '♈️ Овен', '♉️ Телец', '♊️ Близнецы', 
        '♋️ Рак', '♌️ Лев', '♍️ Дева', '♎️ Весы', 
        '♏️ Скорпион', '♐️ Стрелец', '♑️ Козерог',
        '♒️ Водолей', '♓️ Рыбы'
    ]
    keyboard = ReplyKeyboardBuilder()
    for horoscope in horoscopes:
        keyboard.add(KeyboardButton(text=horoscope))
    keyboard.adjust(3, repeat=True)
    return(keyboard.as_markup(resize_keyboard=True))
