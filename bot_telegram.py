from aiogram.utils import executor
from Create_bot import dp
from aiogram import types
from aiogram.dispatcher.filters import Text, IDFilter, BoundFilter
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from texts import *
from states import *
from config import KEYWORD
from keyboard import main_kb, remove_kb




async def on_startup(_):
    print("Бот запущен")


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await message.answer(welcome_message)
    await StartKeywordState.waiting_for_keyword.set()

@dp.message_handler(state=StartKeywordState.waiting_for_keyword)
async def check_keyword(message: types.Message, state: FSMContext):
    if message.text == KEYWORD:
        await state.finish()
        await message.answer(right_keyword, reply_markup=main_kb)
    else:
        await message.answer(wrong_keyword)

@dp.message_handler(lambda message: "Создать опрос")
async def create_poll(poll: types.Poll):
    await




executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


