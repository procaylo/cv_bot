from misc import dp, db, bot
from func import language, mk, en, ru
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton


@dp.message_handler(content_types="text")
async def handle_text(message):
    if message.text == en.get_string(4) or message.text == ru.get_string(4):
        dic = {language(message.from_user.language_code).get_string(7): language(message.from_user.language_code).get_string(12)}
        await bot.send_message(message.from_user.id, language(message.from_user.language_code).get_string(9), reply_markup=mk(dic))

    elif message.text == en.get_string(5) or message.text == ru.get_string(5):
        db.start_chat(message.from_user.id)
        admins = db.admin_list()
        for i in admins:
            dic = {"Начать чат":"start_chat_"+str(message.from_user.id)}
            await bot.send_message(int(i[0]),"Пользователь @"+str(message.from_user.username) + " хочет начать чат \n\n Язык: " +str(message.from_user.language_code), reply_markup=mk(dic))

        await bot.send_message(message.from_user.id, language(message.from_user.language_code).get_string(14))
    else:
        if db.check_status(message.from_user.id) !=0:
            if db.is_admin(message.chat.id):
                user = db.check_status(message.chat.id)
                await bot.send_message(user, message.text)
            else:
                admin = db.check_status(message.chat.id)
                await bot.send_message(admin, message.text)