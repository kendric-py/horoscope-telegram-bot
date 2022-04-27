from aiogram.dispatcher.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from loader import bot, db



class CheckSubscribe:
    async def __get_chanels(self):
        chanels_list = await db.get_chanels()
        return(chanels_list)


    async def __checker(self, user_id: int):
        chanels = await self.__get_chanels()
        if not(chanels): return(0)
        
        for chanel in chanels:
            try:
                result = await bot.get_chat_member(chat_id=chanel.telegram_id, user_id=user_id)
                if result.status == 'left': return(0)
            except: continue
        return(1)


    async def get_result(self, user_id: int):
        result = await self.__checker(user_id)
        print(result)
        return(bool(result))


class InChanelsMessage(BaseFilter, CheckSubscribe):
    in_chanels: bool

    async def __call__(self, message: Message) -> bool:
        check_result = await self.get_result(message.from_user.id)
        return(check_result == self.in_chanels)


class InChanelsCallback(BaseFilter, CheckSubscribe):
    in_chanels: bool

    async def __call__(self, call: CallbackQuery) -> bool:
        check_result = await self.get_result(call.from_user.id)
        return(check_result == self.in_chanels)


class InDb(BaseFilter):
    in_db: bool

    async def __call__(self, message: Message):
        user = await db.get_user(message.from_user.id)
        return(bool(user) == self.in_db)