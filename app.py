from loader import dp, bot
from loguru import logger
import asyncio


from pathes.telegram.client.handlers import user_router
from pathes.telegram.admin.handlers import admin_router



async def main():
    logger.info('Бот успешно запущен!')
    dp.include_router(user_router)
    dp.include_router(admin_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())