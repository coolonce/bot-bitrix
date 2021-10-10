from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


accept_btn = InlineKeyboardButton('Да', callback_data='accept')


decline = InlineKeyboardButton('Нет', callback_data='decline')

keyboard_ysnNo = InlineKeyboardMarkup().add(accept_btn, decline)