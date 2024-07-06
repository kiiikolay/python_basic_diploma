import telebot
from main import bot


@bot.message_handlers(commands=['movie_search'])
def mov_search(message):
    bot.send_message(message.chat.id, 'Привет!\nНапиши название фильма')

