import telebot
from asyncio import queues
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from dotenv import load_dotenv, find_dotenv
import os

if not find_dotenv():
    exit('Переменные окружения не загружены т.к. отсутствует файл .env')
else:
    load_dotenv(find_dotenv())

API_KEY = os.getenv('API_KEY')
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))
my_queue = queues.Queue()
updater = Updater('BOT_TOKEN', update_queue=my_queue)

