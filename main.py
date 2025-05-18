import telebot
from asyncio import queues
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from config_data.config import bot, updater
from telebot.custom_filters import StateFilter
from handlers.search import by_name, by_ratting, by_low_budget, by_high_budget



if __name__ == '__main__':
    bot.add_custom_filter(StateFilter(bot))
    bot.infinity_polling()
