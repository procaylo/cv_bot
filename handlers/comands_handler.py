from func import language, mk
from misc import dp, db, bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

@dp.message_handler(commands='start')
async def handle_start(message):
    def start_mk():
        start_mk = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        start_mk.add(InlineKeyboardButton(language(message.from_user.language_code).get_string(4)))
        start_mk.add(InlineKeyboardButton(language(message.from_user.language_code).get_string(5)))
        start_mk.add(InlineKeyboardButton(language(message.from_user.language_code).get_string(6), request_contact=True))
        return start_mk
    if db.check_user(message.from_user.id) == True:
        await bot.send_message(message.from_user.id,language(message.from_user.language_code).get_string(1), reply_markup=start_mk())
    else:
        db.new_user(message.from_user.id)
        await bot.send_message(message.from_user.id,language(message.from_user.language_code).get_string(0), reply_markup=start_mk())
