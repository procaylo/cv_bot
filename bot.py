#!venv/bin/python
from config import *
from aiogram import Bot, Dispatcher, executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
import sqlite3 as sq
import re

bot = Bot(token=token)
dp = Dispatcher(bot)

#Инлайн-Клавиатура
def mk(dic):
    mk = InlineKeyboardMarkup()
    for i in dic:
        mk.add(InlineKeyboardButton(i, callback_data=dic[i]))
    return mk

#Ответы
class Answer:
    def __init__(self, file):
        self.open = open(file,"r", encoding='UTF-8')

    def get_string(self, n):
        l = self.open.read().split("\n")
        self.open.seek(0)
        if n <= len(l):
            return l[n]
        else:
            print("No such string number")

en = Answer('answers.txt')
ru = Answer("answers_ru.txt")

#База
class Database:

    def __init__(self, database):
        self.conection = sq.connect(database)
        self.cursor = self.conection.cursor()

    def new_user(self, user):
        with self.conection:
            return self.cursor.execute("INSERT INTO users (id, name, tel, status) VALUES (?,?,?,?)",
                                       (user, None, None, 0))

    def new_admin(self, admin):
        with self.conection:
            return self.cursor.execute("INSERT INTO users (id, status) VALUES (?,?)", (admin, 0))

    def get_contact(self, contact):
        id = contact['user_id']
        name = contact["first_name"]
        tel = contact["phone_number"]
        with self.conection:
            return self.cursor.execute("UPDATE users SET tel = ?, name = ? WHERE id = ?", (tel, name, id,))

    def check_user(self, id):
        with self.conection:
            a = self.cursor.execute("SELECT * FROM users WHERE id = ?", (id,)).fetchall()
            if len(a) > 0:
                return True
            else:
                return False

    def start_chat(self, user):
        with self.conection:
            return self.cursor.execute("UPDATE users SET status = 1 WHERE id = ?", (user,))

    def finish_chat(self, user):
        with self.conection:
            return self.cursor.execute("UPDATE users SET status = 0 WHERE id = ?", (user,))

    def admin_list(self):
        with self.conection:
            return self.cursor.execute("SELECT id FROM admins WHERE status = 0").fetchall()

    def set_admin(self, user, admin):
        with self.conection:
            return self.cursor.execute("UPDATE admins SET status = ? WHERE id = ?", (user, admin,)) and self.cursor.execute("UPDATE users SET status = ? WHERE id = ?", (admin, user))

    def check_status(self, user):
        with self.conection:
            return self.cursor.execute("SELECT status FROM users WHERE id = ?", (user,)).fetchall()[0][0]

    def is_admin(self, user):
        with self.conection:
            a = self.cursor.execute("SELECT * FROM admins WHERE id = ?", (user,)).fetchall()
            if len(a) > 0:
                return True
            else:
                return False
    def free_admin(self, admin):
        with self.conection:
            return self.cursor.execute("UPDATE admins SET status = 0 WHERE id = ?", (admin,))

    def close(self):
        self.conection.close()


db = Database('cv_bot.db')

#Язык
def language(code):
    if code == 'ru':
        return ru
    else:
        return en


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


@dp.message_handler (content_types="contact")
async def handle_contact(message):
    db.get_contact(contact=message.contact)
    await bot.send_message(message.from_user.id, language(message.from_user.language_code).get_string(3),reply_markup=ReplyKeyboardRemove())


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

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
