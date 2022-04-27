from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from aiogram.dispatcher.filters.content_types import ContentTypesFilter
from aiogram import Router

from loader import bot, db, consts, hp

from pathes.telegram.filters.client_filters import InChanelsMessage, InChanelsCallback, InDb

from . import keyboards as nav

user_router = Router()
user_router.message.bind_filter(InDb)
user_router.message.bind_filter(InChanelsMessage)
user_router.callback_query_handler.bind_filter(InChanelsCallback)







# async def start_command_no_subscribe(message: Message):
    # user = await db.get_user(message.from_user.id)
    # if not(user):
    #     user = await db.create_user(message.from_user.id)
    #     ref_code = 0 if message.text[7:] == '' else message.text[7:]
    #     if ref_code: await db.create_referal(ref_code, message.from_user.id)
    # chanels, not_subscribe = await db.get_chanels(), []

    # for chanel in chanels:
    #     try:
    #         result = await bot.get_chat_member(chat_id=chanel.telegram_id, user_id=message.from_user.id)
    #         if result.status == 'left': not_subscribe.append(chanel)
    #     except: not_subscribe.append(chanel)
    # await message.answer('referal_data.message', reply_markup=nav.render_subscribe(not_subscribe))





async def start_command_no_db(message: Message):
    referal_code = '0' if message.text[7:] == '' else message.text[7:]
    await db.create_user(message.from_user.id)
    await db.create_referal(referal_code, message.from_user.id)
    chanels, not_subscribe = await db.get_chanels(), []
    referal_code = await db.search_referal_code(referal_code)
    for chanel in chanels:
        try:
            result = await bot.get_chat_member(chat_id=chanel.telegram_id, user_id=message.from_user.id)
            if result.status == 'left': not_subscribe.append(chanel)
        except: not_subscribe.append(chanel)
    await message.answer(referal_code.message, reply_markup=nav.render_subscribe(not_subscribe))


    

async def offer_chanels(call: CallbackQuery):
    referal = await db.get_referal(call.from_user.id)
    referal_code = await db.search_referal_code(referal.referal_code)
    chanels, not_subscribe = await db.get_chanels(), []
    for chanel in chanels:
        try:
            result = await bot.get_chat_member(chat_id=chanel.telegram_id, user_id=message.from_user.id)
            if result.status == 'left': not_subscribe.append(chanel)
        except: not_subscribe.append(chanel)
    await call.message.edit_text(referal_code.message, reply_markup=nav.render_subscribe(not_subscribe))


async def confirm_subscribe(call: CallbackQuery):
    await call.message.edit_text(
        '<b>✌️ Привет\
        \n\n🔮 Тут ты можешь увидеть свежий гороскоп каждый день\
        \n\nДля получения гороскопа жми на свой знак зодиака ниже 👇</b>',
        reply_markup=nav.render_horoscope()
    )


async def start_command(message: Message):
    await message.answer(
        '<b>✌️ Привет\
        \n\n🔮 Тут ты можешь увидеть свежий гороскоп каждый день\
        \n\nДля получения гороскопа жми на свой знак зодиака ниже 👇</b>',
        reply_markup=nav.render_horoscope()
    )


async def show_horoscope(message: Message):
    horoscope = await hp(consts.HOROSCOPES[message.text])
    await message.answer(
        f'<b>{horoscope}</b>'
    )
    



user_router.message.register(start_command_no_db, commands='start', in_db=False)
user_router.message.register(start_command, commands='start', in_db=True)
user_router.message.register(show_horoscope, text = list(consts.HOROSCOPES.keys()))



user_router.callback_query_handler.register(offer_chanels, text='user&check_subs', in_chanels=False)
user_router.callback_query_handler.register(confirm_subscribe, text='user&check_subs', in_chanels=True)