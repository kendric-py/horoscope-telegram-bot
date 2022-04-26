from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from aiogram.dispatcher.filters.content_types import ContentTypesFilter
from aiogram import Router

from pathes.telegram.filters.admin_filters import IsAdmin

from . import keyboards as nav

admin_router = Router()



async def open_menu(message: Message):
    await message.answer('<b>✅ Успешный вход в админ-панель</b>', reply_markup=nav.render_menu())





#bind filters
admin_router.message.bind_filter(IsAdmin)

#register message handlers
admin_router.message.register(open_menu, commands='admin', is_admin=True)

#register callback handlers