import time
import asyncio
from loguru import logger
from loader import bot, bot_cfg, db
from aiogram.exceptions import TelegramForbiddenError

class Core:
    LOGS_PATH: str = 'data/logs/mailing/errors-{time}.log'
    SLEEP_BETWEEN: int = 1
    SIZE_CHUNK: int = 25

    FINAL_TEXT: str = 'Рассылка закончена:\
    \n - {count_succ}(Успешных)\
    \n  - {blocks}(Заблокированно)\
    \n   - {count_err}(Ошибок)'

    FINAL_TEXT_TELEGRAM: str = '<b>Рассылка закончена:\
    \n - <code>{count_succ}</code>(Успешных)\
    \n  - <code>{blocks}</code>(Заблокированно)\
    \n   - <code>{count_err}</code>(Ошибок)</b>'

    
    def __init__(self):
        logger.add(self.LOGS_PATH.format(time=time.time()), format='{level} || {message}', level='DEBUG')
        self.count_users: int = 0
        self.count_succ_send: int = 0
        self.count_err_send: int = 0
        self.count_blocks: int = 0


    def __clear_count_user(self) -> None:
        self.count_users = 0
        return

    
    def __clear_succ_send(self) -> None:
        self.count_succ_send = 0
        return


    def __clear_err_send(self) -> None:
        self.count_err_send = 0
        return

    def __clear_blocks(self) -> None:
        self.count_blocks = 0
        return

    
    def __clear_all_counters(self):
        self.__clear_count_user()
        self.__clear_succ_send()
        self.__clear_err_send()
        self.__clear_blocks()
        return


    async def __alert_admin_end_mailing(self):
        try:
            await bot.send_message(bot_cfg.admin_id, self.FINAL_TEXT_TELEGRAM.format(
                count_succ=self.count_succ_send, blocks = self.count_blocks, count_err=self.count_err_send
            ))
        except Exception as err:
            logger.error(f'Ошибка отправки отчета: {err}')
        return

    
    async def __sender_copy_message(self, chat_id: int, message_id: int, from_id: int, keyboard) -> None:
        try:
            await bot.copy_message(from_id, chat_id, message_id, reply_markup=keyboard)
            self.count_succ_send += 1
        except TelegramForbiddenError:
            self.count_blocks += 1
            logger.info('Удален пользователь, в связи с блокировкой бота!')
            await db.delete_user(from_id)
        except Exception as err:
            self.count_err_send += 1
            logger.error(f'Фиксация ошибки: {err}')
        return


    async def __chunk_preparation_and_start(self, users: list, chat_id: int, message_id: int, keyboard):
        chunk_tasks = []

        for num, user in enumerate(users):
            task = self.__sender_copy_message(chat_id, message_id, user.telegram_id, keyboard)
            chunk_tasks.append(task)
            if len(chunk_tasks) != self.SIZE_CHUNK and num+1 != self.count_users:
                continue
            try:
                await asyncio.gather(*chunk_tasks)
                await asyncio.sleep(self.SLEEP_BETWEEN)
            except Exception as err:
                self.count_err_send += 1
                logger.error(f'Ошибка при запуске gather: {err}')
            chunk_tasks.clear()
    
        await asyncio.sleep(5)
        await self.__alert_admin_end_mailing()
        print(self.FINAL_TEXT.format(count_succ=self.count_succ_send, blocks = self.count_blocks, count_err=self.count_err_send))
        return


    async def run(self, message, users):
        self.__clear_all_counters()
        self.count_users = len(users)
        await self.__chunk_preparation_and_start(users, message.chat.id, message.message_id, message.reply_markup)
        return('Рассылка запущена')


