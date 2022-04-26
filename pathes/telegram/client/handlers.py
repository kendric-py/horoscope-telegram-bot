from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from aiogram.dispatcher.filters.content_types import ContentTypesFilter
from aiogram import Router

from loader import db


user_router = Router()




async def start_command(message: Message):
    await message.answer('Ку')



user_router.message.register(start_command, commands='start')