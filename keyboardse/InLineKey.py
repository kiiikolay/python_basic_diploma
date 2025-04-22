from comfig_data.config import bot
import telebot
from telebot import types
from comfig_data import config


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('По названию')
    btn2 = types.KeyboardButton('По жанру')
    btn3 = types.KeyboardButton('По рейтингу')
    markup.row(btn1, btn2, btn3)
    bot.send_message(message.chat.id, 'привет', reply_markup=markup)
