from aiogram import Bot, Dispatcher

from data.configs.config_manager import Core
from data.database import control as db
from data import consts


from pathes.analyzer import core


core_cfg = Core('data/configs/config.ini')
bot_cfg = core_cfg.sections.telegram


hp = core.Manager()
bot = Bot(bot_cfg.token, parse_mode='HTML')
dp = Dispatcher()