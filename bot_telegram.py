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
    poll = await message.answer_poll(question=data["question"], options=data["answers"], is_anonymous=data["is_anonymous"],
                              allows_multiple_answers=data["allows_multiple_answers"], reply_markup=remove_kb)
    print(poll.poll)
    await asyncio.sleep(60)
    print(poll.poll)


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




# async def just_poll_answer(active_quiz: types.Poll):
#     """
#     Реагирует на закрытие опроса/викторины. Если убрать проверку на poll.is_closed == True,
#     то этот хэндлер будет срабатывать при каждом взаимодействии с опросом/викториной, наравне
#     с poll_answer_handler
#     Чтобы не было путаницы:
#     * active_quiz - викторина, в которой кто-то выбрал ответ
#     * saved_quiz - викторина, находящаяся в нашем "хранилище" в памяти
#     Этот хэндлер частично повторяет тот, что выше, в части, касающейся поиска нужного опроса в нашем "хранилище".
#     :param active_quiz: объект Poll
#     """
#     quiz_owner = quizzes_owners.get(active_quiz.id)
#     if not quiz_owner:
#         logging.error(f"Не могу найти автора викторины с active_quiz.id = {active_quiz.id}")
#         return
#     for num, saved_quiz in enumerate(quizzes_database[quiz_owner]):
#         if saved_quiz.quiz_id == active_quiz.id:
#             # Используем ID победителей, чтобы получить по ним имена игроков и поздравить.
#             congrats_text = []
#             for winner in saved_quiz.winners:
#                 chat_member_info = await bot.get_chat_member(saved_quiz.chat_id, winner)
#                 congrats_text.append(chat_member_info.user.get_mention(as_html=True))
#
#             await bot.send_message(saved_quiz.chat_id, "Викторина закончена, всем спасибо! Вот наши победители:\n\n"
#                                    + "\n".join(congrats_text), parse_mode="HTML")
#             # Удаляем викторину из обоих наших "хранилищ"
#             del quizzes_owners[active_quiz.id]
#             del quizzes_database[quiz_owner][num]