import telebot
from comfig_data import config
from keyboardse import InLineKey

bot = telebot.TeleBot(config.BOT_TOKEN)

InLineKey.start(bot)

if __name__ == "__main__":
    bot.infinity_polling()

