from telebot import types
from config_data.config import bot
from states.st import UserInfoState
from telebot.custom_filters import StateFilter
from markups.markups import genre_markup
from API.pars import creating_a_url

del_mark = types.ReplyKeyboardRemove()
data_key = ''
data_val = ''
data = {}


@bot.message_handler(commands=['high_budget_movie'])
def by_high_budget(message):
    global data_key, data_val
    data['budget.value'] = '25000000-5000000000'
    bot.send_message(message.from_user.id, 'Привет!\nБудем искать с высоким бюджетом\nВведи сколько вариантов показать')
    bot.set_state(message.from_user.id, UserInfoState.limit, message.chat.id)


@bot.message_handler(commands=['low_budget_movie'])
def by_low_budget(message):
    global data_key, data_val
    data['budget.value'] = '0-25000000'
    bot.send_message(message.from_user.id, 'Привет!\nБудем искать с низким бюджетом\nВведи сколько вариантов показать')
    bot.set_state(message.from_user.id, UserInfoState.limit, message.chat.id)


@bot.message_handler(commands=['movie_by_rating'])
def by_ratting(message):
    bot.send_message(message.from_user.id, 'Привет!\nВведи рейтинг')
    bot.set_state(message.from_user.id, UserInfoState.search_by_name_upp_rat, message.chat.id)


@bot.message_handler(commands=['movie_search'])
def by_name(message):
    bot.send_message(message.from_user.id, 'Привет!\nВведи название')
    bot.set_state(message.from_user.id, UserInfoState.search_by_name, message.chat.id)


@bot.message_handler(state=UserInfoState.search_by_name)
def name(message):
    if data_key != '':
        with bot.retrieve_data(message.from_user.id, message.chat.id) as dat:
            data[data_key] = data_val
    bot.send_message(message.from_user.id, 'Принято. Теперь выбери жанр', reply_markup=genre_markup())
    bot.set_state(message.from_user.id, UserInfoState.genre, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as dat:
        data['query'] = message.text


@bot.message_handler(state=UserInfoState.genre)
def genre(message):
    bot.send_message(message.from_user.id, 'Принято, теперь напиши сколько вариантов фильмов показать (число) ')
    bot.set_state(message.from_user.id, UserInfoState.limit, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as dat:
        data['genres.name'] = message.text

@bot.message_handler(state=UserInfoState.search_by_name_upp_rat)
def by_name_upp_rat(message):
    if message.text.isdigit():
        bot.send_message(message.from_user.id, 'Принято, теперь напиши сколько вариантов фильмов показать (число) ')
        bot.set_state(message.from_user.id, UserInfoState.limit, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as dat:
            data['kp'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Рейтинг - это число')


@bot.message_handler(state=UserInfoState.limit)
def limit(message):
    bot.send_message(message.from_user.id, 'Принято\nВот что нашёл')
    bot.set_state(message.from_user.id, UserInfoState.limit, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as dat:
        data['limit'] = message.text
    creating_a_url(message, data)


if __name__ == '__main__':
    bot.add_custom_filter(StateFilter(bot))
    bot.infinity_polling()
