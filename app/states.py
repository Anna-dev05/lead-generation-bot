from aiogram.fsm.state import State, StatesGroup

class LeadForm(StatesGroup):
    name = State()
    phone = State()
    ask_email = State()
    email = State()
    ask_telegram = State()
    telegram = State()
    message = State()
    confirm = State()
