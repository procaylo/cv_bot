from answers.answers import en, ru
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

def language(code):
    if code == 'ru':
        return ru
    else:
        return en


def mk(dic):
    mk = InlineKeyboardMarkup()
    for i in dic:
        mk.add(InlineKeyboardButton(i, callback_data=dic[i]))
    return mk
