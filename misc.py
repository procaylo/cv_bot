from aiogram import Bot, Dispatcher
from config import token
from classes import Database
bot = Bot(token=token)
dp = Dispatcher(bot)
db = Database('cv_bot.db')