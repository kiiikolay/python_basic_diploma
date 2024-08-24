import telebot
from asyncio import queues
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from config_data.config import bot, updater
from telebot.custom_filters import StateFilter
from handlers.search import by_name, by_ratting, by_low_budget, by_high_budget

def main():

    # Получаем диспетчер для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Регистрируем обработчики команд
    dispatcher.add_handler(CommandHandler("movie_search", by_name()))
    dispatcher.add_handler(CommandHandler("movie_by_rating", by_ratting()))
    dispatcher.add_handler(CommandHandler("low_budget_movie", by_low_budget()))
    dispatcher.add_handler(CommandHandler("high_budget_movie", by_high_budget()))

    # Запускаем бота
    updater.start_polling()

    # Замечаем когда бот остановится
    updater.idle()


if __name__ == '__main__':
    bot.add_custom_filter(StateFilter(bot))
    main()
    bot.infinity_polling()
