from misc import dp, db, bot
from func import language, mk
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton


@dp.message_handler (content_types="contact")
async def handle_contact(message):
    db.get_contact(contact=message.contact)
    await bot.send_message(message.from_user.id, language(message.from_user.language_code).get_string(3),reply_markup=ReplyKeyboardRemove())

