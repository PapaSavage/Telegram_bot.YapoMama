from aiogram.dispatcher.filters.state import StatesGroup, State


class Start(StatesGroup):
    open = State()
    start = State()
    name = State()
    number = State()
    timetable = State()
    time = State()
    order_start = State()
    random = State()
    adress = State()
    Sets = State()