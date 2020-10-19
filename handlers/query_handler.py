from misc import dp, db, bot
from func import mk, language, en, ru
import re
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton


@dp.callback_query_handler(lambda call: True)
async def query_handler(call):
    if "contacts" in call.data:
        if "ru" in call.data:
            dic = {ru.get_string(8):ru.get_string(13)}
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=ru.get_string(10)+"\n"+ru.get_string(11), reply_markup=mk(dic))
        else:
            dic = {en.get_string(8):en.get_string(13)}
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=en.get_string(10)+"\n"+en.get_string(11), reply_markup=mk(dic))

    elif "back" in call.data:
        if "ru" in call.data:
            dic = {ru.get_string(7): ru.get_string(12)}
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=ru.get_string(9), reply_markup=mk(dic))
        else:
            dic = {en.get_string(7): en.get_string(12)}
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=en.get_string(9), reply_markup=mk(dic))

    elif "start_chat" in call.data:
        user =re.sub("start_chat_", "",str(call.data))
        if db.check_status(user) == 1 or db.check_status(user) == 0:
            dic = {"Закончить чат":"finish_chat_"+str(user)}
            db.set_admin(user=user,admin=call.message.chat.id)
            await bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,
                                        text="Чат начат. Напишите первое сообщение пользователю", reply_markup=mk(dic))
        else:
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text= "Другой админ уже начал чат")

    elif "finish_chat" in call.data:
        user = re.sub("finish_chat_", "",str(call.data))
        db.free_admin(call.message.chat.id)
        db.finish_chat(user)
        await bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,
                                        text="Вы завершили чат")