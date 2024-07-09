import telebot
from comfig_data import config
from keyboardse import InLineKey

bot = telebot.TeleBot(config.BOT_TOKEN)



if __name__ == "__main__":
    InLineKey.start(bot)
    bot.infinity_polling()

