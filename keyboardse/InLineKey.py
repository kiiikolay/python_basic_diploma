import telebot
from telebot import types
from comfig_data import config

bot = telebot.TeleBot(config.BOT_TOKEN)


@bot.message_handlers(command=['sart'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Поиск фильма по названию')
    markup.row(btn1)
    bot.send_message(message.chat.id, 'привет', reply_markup=markup)
