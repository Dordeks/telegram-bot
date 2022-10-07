from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton

button_create_poll = KeyboardButton('Создать опрос')
button_poll_list = KeyboardButton('Список опросов')


main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
main_kb.add(button_create_poll)\
       .add(button_poll_list)

yes_no_kb = ReplyKeyboardMarkup(resize_keyboard=True)
yes_no_kb.add(KeyboardButton('Да'))
yes_no_kb.add(KeyboardButton('Нет'))


create_new_or_not = ReplyKeyboardMarkup(resize_keyboard=True)
create_new_or_not.add(KeyboardButton('Добавить новый ответ'))
create_new_or_not.add(KeyboardButton('Закончить с ответами'))


remove_kb = ReplyKeyboardRemove()