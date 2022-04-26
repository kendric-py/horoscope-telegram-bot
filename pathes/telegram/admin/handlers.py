from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery

from aiogram.dispatcher.filters.content_types import ContentTypesFilter
from aiogram import Router

from pathes.telegram.filters.admin_filters import IsAdmin

import copy

from .states import Mailing, Chanel
from .mailing_system import Core
from . import keyboards as nav
from loader import bot, db

ml = Core()
admin_router = Router()


async def open_menu(message: Message):
    await message.answer(
        '<b>✅ Успешный вход в админ-панель</b>',
        reply_markup=nav.render_menu()
    )


async def cancel_action(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.delete()
    await call.message.answer(
        '<b>⚙️ Вы вернулись в админ-панель</b>',
        reply_markup=nav.render_menu()
    )


async def open_stats_menu(call: CallbackQuery):
    count_users = await db.get_count_users()
    try:
        await call.message.edit_text(
            f'<b>Всего пользователей:</b> <code>{count_users}</code>\
            \n\n<b>📈Информация по текущей/прошлой рассылке</b>\
            \n\n<b>Пользователей в рассылке:</b> <code>{ml.count_users}</code>\
            \n<b>Успешных отправок:</b> <code>{ml.count_succ_send}</code>\
            \n<b>Заблокировали:</b> <code>{ml.count_blocks}</code>\
            \n<b>Ошибок при отправке:</b> <code>{ml.count_err_send}</code>',
            reply_markup=nav.render_stats_menu()
        )
    except TelegramBadRequest:
        await call.answer('💡 Актуальная информация')


async def chanels_menu(call: CallbackQuery):
    chanels = await db.get_chanels()
    await call.message.edit_text(
        '<b>Список каналов</b>\n\nДля удаления, сделайте клик по нужному каналу',
        reply_markup=nav.render_chanels_menu(chanels)
    )


async def start_add_chanel(call: CallbackQuery, state: FSMContext):
    await state.set_state(Chanel.wait_name)
    await call.message.edit_text(
        '<b>Отправьте название канала(Которое будет отоброжено при просьбе подписаться)</b>',
        reply_markup=nav.render_cancel()
    )


async def asking_link_chanel(message: Message, state: FSMContext):
    await message.delete()
    await state.update_data(chanel_name = message.text)
    await state.set_state(Chanel.wait_link)
    await message.answer(
        '<b>Отправьте ссылку для пользователей, который будут переходить по ней</b>',
        reply_markup=nav.render_cancel()
    )


async def asking_chanel_link(message: Message, state: FSMContext):
    await message.delete()
    await state.update_data(chanel_link = message.text)
    await state.set_state(Chanel.wait_telegram_id)
    await message.answer(
        '<b>Отправьте <code>ID</code> канала</b>',
        reply_markup=nav.render_cancel()
    )


async def create_chanel_record(message: Message, state: FSMContext):
    state_data = await state.get_data()
    await message.delete()
    await state.clear()
    await message.answer(
        '<b>Канал успешно добавлен!</b>'
    )
    




async def start_mailing(call: CallbackQuery, state: FSMContext):
    await state.set_state(Mailing.wait_content)
    await call.message.edit_text(
        '<b>🧾 Для продолжения, требуется контент</b>',
        reply_markup=nav.render_cancel()
    )


async def take_mailing_content(message: Message, state: FSMContext):
    await state.update_data(copy_message = message)
    await state.set_state(Mailing.wait_confirm)
    nested_keyboard = copy.deepcopy(message.reply_markup)
    if nested_keyboard:
        nested_keyboard.inline_keyboard.append([
            InlineKeyboardButton(text='✅ Подтвердить', callback_data='admin&confirm_mailing'), 
            InlineKeyboardButton(text='❌ Отмена', callback_data='admin&main')
        ])
    else: nested_keyboard = nav.render_confirm_mailing()
    await bot.copy_message(message.from_user.id, message.chat.id, message.message_id, reply_markup=nested_keyboard)


async def run_mailing(call: CallbackQuery, state: FSMContext):
    users, state_data = await db.get_users(), await state.get_data()
    await state.clear()
    await call.message.delete()
    await call.message.answer('<b>🟢 Рассылка запущена!</b>\n\nДля подробной информации перейдите в раздел <b>«📊 Статистика»</b>')
    await ml.run(state_data['copy_message'], users)






#bind filters
admin_router.message.bind_filter(IsAdmin)

#register message handlers
admin_router.message.register(open_menu, commands='admin', is_admin=True)
admin_router.message.register(take_mailing_content, state=Mailing.wait_content) #Рассылка


#register callback handlers
admin_router.callback_query_handler.register(cancel_action, text='admin&cancel', state='*') #Отмена какого-либо действия
admin_router.callback_query_handler.register(start_mailing, text='admin&mailing') #Рассылка
admin_router.callback_query_handler.register(run_mailing, text='admin&confirm_mailing', state=Mailing.wait_confirm) # Запуск рассылки
admin_router.callback_query_handler.register(open_stats_menu, text='admin&stats') #Панель статистики
admin_router.callback_query_handler.register(open_stats_menu, text='admin&refresh_stats') #Обновление статистики
admin_router.callback_query_handler.register(chanels_menu, text='admin&chanels')



