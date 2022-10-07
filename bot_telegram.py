from aiogram.utils import executor
from Create_bot import dp
from aiogram import types
from aiogram.dispatcher.filters import Text

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from texts import *
from states import *
from config import KEYWORD
from keyboard import main_kb, remove_kb, yes_no_kb, create_new_or_not




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

@dp.message_handler(Text(equals='Создать опрос', ignore_case=True))
async def create_poll(message: types.Message):
    await message.answer(createpoll_is_anonymous, reply_markup=yes_no_kb)
    await CreatePollState.is_anonymous.set()

@dp.message_handler(state=CreatePollState.is_anonymous)
async def poll_is_anonymous(message: types.Message, state: FSMContext):
    if message.text == "Да":
        await state.update_data(is_anonymous=True)
        await message.answer(createpoll_allows_multiple_answers, reply_markup=yes_no_kb)
        await state.set_state(CreatePollState.allows_multiple_answers)
    elif message.text == "Нет":
        await state.update_data(is_anonymous=False)
        await message.answer(createpoll_allows_multiple_answers, reply_markup=yes_no_kb)
        await state.set_state(CreatePollState.allows_multiple_answers)
    else:
        await message.answer("Выберите вариант из предложенных")

@dp.message_handler(state=CreatePollState.allows_multiple_answers)
async def poll_allows_multiple_answers(message: types.Message, state: FSMContext):
    if message.text == "Да":
        await state.update_data(allows_multiple_answers=True)
        await message.answer(createpoll_question, reply_markup=remove_kb)
        await state.set_state(CreatePollState.question)
    elif message.text == "Нет":
        await state.update_data(allows_multiple_answers=False)
        await message.answer(createpoll_question, reply_markup=remove_kb)
        await state.set_state(CreatePollState.question)
    else:
        await message.answer("Выберите вариант из предложенных")

@dp.message_handler(state=CreatePollState.question)
async def poll_question(message: types.Message, state: FSMContext):
    await state.update_data(question=message.text)
    await message.answer(createpoll_answers)
    await state.set_state(CreatePollState.answers)
    await state.update_data(answers=[])


@dp.message_handler(Text(equals='Добавить новый ответ', ignore_case=True), state=CreatePollState.answers)
async def poll_answers_add_another(message: types.Message, state: FSMContext):
    await message.answer(createpoll_answers_2, reply_markup=remove_kb)

@dp.message_handler(Text(equals='Закончить с ответами', ignore_case=True), state=CreatePollState.answers)
async def poll_answers_end(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.finish()
    await message.answer_poll(question=data["question"], options=data["answers"], is_anonymous=data["is_anonymous"],
                              allows_multiple_answers=data["allows_multiple_answers"])


@dp.message_handler(state=CreatePollState.answers)
async def poll_answers(message: types.Message, state: FSMContext):
    data = await state.get_data()
    answers = data["answers"]
    answers.append(message.text)
    if len(answers) < 2:
        await message.answer(createpoll_answers_1)
    else:
        await message.answer(reply_markup=create_new_or_not)
    state.update_data(answers=answers)




executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


