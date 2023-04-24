from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMWeather(StatesGroup):
    weather = State()


class FSMRate(StatesGroup):
    rate = State()
    amount = State()


class FSMPoll(StatesGroup):
    poll = State()