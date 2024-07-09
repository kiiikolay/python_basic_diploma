from comfig_data.config import bot
import telebot
from comfig_data import config
from keyboardse import InLineKey


if __name__ == "__main__":
    InLineKey.start(bot)
    bot.infinity_polling()

