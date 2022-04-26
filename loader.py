from aiogram import Bot, Dispatcher

from data.configs.config_manager import Core
from data.database import control as db


core_cfg = Core('data/configs/config.ini')
bot_cfg = core_cfg.sections.telegram



bot = Bot(bot_cfg.token, parse_mode='HTML')
dp = Dispatcher()