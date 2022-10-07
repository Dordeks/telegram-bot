from aiogram.dispatcher.filters.state import State, StatesGroup



class StartKeywordState(StatesGroup):
    waiting_for_keyword = State()


