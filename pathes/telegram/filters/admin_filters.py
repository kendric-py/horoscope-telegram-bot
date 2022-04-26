from aiogram.dispatcher.filters import BaseFilter
from aiogram.types import Message

from loader import bot_cfg


class IsAdmin(BaseFilter):
    is_admin: bool

    async def __call__(self, message: Message) -> bool:
        return((message.from_user.id == bot_cfg.admin_id) == self.is_admin)