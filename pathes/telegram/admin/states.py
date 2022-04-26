from aiogram.dispatcher.fsm.state import State, StatesGroup



class Mailing(StatesGroup):
    wait_content = State()
    wait_confirm = State()


class Chanel(StatesGroup):
    wait_name = State()
    wait_link = State()
    wait_telegram_id = State()