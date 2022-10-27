from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


b1 = KeyboardButton('Поиск по лицевому счету')
b2 = KeyboardButton('Поиск по ФИО, названию')
b3 = KeyboardButton('Поиск по адресу')
b4 = KeyboardButton('Выборка на номеру ТП')

a1 = KeyboardButton('Добавить в отключенные')
a2 = KeyboardButton('Удалить из отключенных')
a3 = KeyboardButton('Обновить базу данных')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.add(b1, b2).row(b3, b4)

kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)
kb_admin.add(a1, a2).row(a3)
