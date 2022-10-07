from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton

button_create_poll = KeyboardButton('Создать опрос')
button_poll_list = KeyboardButton('Список опросов')


main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
main_kb.add(button_create_poll)\
       .add(button_poll_list)

remove_kb = ReplyKeyboardRemove()