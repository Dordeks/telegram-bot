from aiogram.dispatcher.filters.state import State, StatesGroup

class StartKeywordState(StatesGroup):
    waiting_for_keyword = State()

class CreatePollState(StatesGroup):
    is_anonymous = State()
    question = State()
    answers = State()
    allows_multiple_answers = State()
    expire_time = State()

