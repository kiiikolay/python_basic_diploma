from telebot import types
from config_data_2.config import bot
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
    """
        Обработчик команды '/high_budget_movie'.

        Устанавливает значение бюджета фильма в диапазоне от 25,000,000 до 5,000,000,000,
        отправляет пользователю сообщение о фильме с высоким бюджетом и вызывает функцию
        `creating_a_url` для формирования и отправки URL с результатами поиска.

        Args:
            message (telebot.types.Message): Объект сообщения от Telegram.
    """
    global data_key, data_val
    data['budget.value'] = '25000000-5000000000'
    bot.send_message(message.chat.id, "Вот фильм с высоким бюджетом")
    creating_a_url(message, data)


@bot.message_handler(commands=['low_budget_movie'])
def by_low_budget(message):
    """
        Обработчик команды '/low_budget_movie'.

        Устанавливает значение бюджета фильма в диапазоне от 0 до 25,000,000,
        отправляет пользователю сообщение о фильме с низким бюджетом и вызывает функцию
        `creating_a_url` для формирования и отправки URL с результатами поиска.

        Args:
            message (telebot.types.Message): Объект сообщения от Telegram.
    """
    global data_key, data_val
    data['budget.value'] = '0-25000000'
    bot.send_message(message.chat.id, "Вот фильм с низким бюджетом")
    creating_a_url(message, data)


@bot.message_handler(commands=['movie_by_rating'])
def by_ratting(message):
    bot.send_message(message.from_user.id, 'Привет!\nВведи рейтинг')
    bot.set_state(message.from_user.id, UserInfoState.search_by_name_upp_rat, message.chat.id)


@bot.message_handler(commands=['movie_search'])
def by_name(message):
    """
        Обработчик команды /movie_search.

        Отправляет приветственное сообщение пользователю и запрашивает название фильма для поиска.
        Устанавливает состояние пользователя в UserInfoState.search_by_name для ожидания ввода названия фильма.

        Args:
            message: Объект сообщения от Telegram.
    """
    bot.send_message(message.from_user.id, 'Привет!\nВведи название')
    bot.set_state(message.from_user.id, UserInfoState.search_by_name, message.chat.id)


@bot.message_handler(state=UserInfoState.search_by_name)
def name(message):
    """
       Обработчик состояния UserInfoState.search_by_name.

       Получает название фильма от пользователя.
       Сохраняет предыдущие данные (если они есть).
       Отправляет пользователю клавиатуру с выбором жанра.
       Устанавливает состояние пользователя в UserInfoState.genre для ожидания выбора жанра.
       Сохраняет введенное название фильма в глобальный словарь data под ключом 'query'.

       Args:
           message: Объект сообщения от Telegram.
    """
    global data
    if data_key != '':
        with bot.retrieve_data(message.from_user.id, message.chat.id) as dat:
            data[data_key] = data_val
    bot.send_message(message.from_user.id, 'Принято. Теперь выбери жанр', reply_markup=genre_markup())
    bot.set_state(message.from_user.id, UserInfoState.genre, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as dat:
        print(dat)
        data['query'] = message.text


@bot.message_handler(state=UserInfoState.genre)
def genre(message):
    """
       Обработчик состояния UserInfoState.genre.

       Получает выбранный жанр фильма от пользователя.
       Запрашивает у пользователя количество вариантов фильмов для показа.
       Устанавливает состояние пользователя в UserInfoState.limit для ожидания ввода числа вариантов.
       Сохраняет выбранный жанр в глобальный словарь data под ключом 'genres.name'.

       Args:
           message: Объект сообщения от Telegram.
    """
    global data
    bot.send_message(message.from_user.id, 'Принято, теперь напиши сколько вариантов фильмов показать (число) ')
    bot.set_state(message.from_user.id, UserInfoState.limit, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as dat:
        data['genres.name'] = message.text

@bot.message_handler(state=UserInfoState.search_by_name_upp_rat)
def by_name_upp_rat(message):
    """
        Обработчик сообщений, принимающий рейтинг фильма (Кинопоиска).

        Функция ожидает числовое значение рейтинга Кинопоиска от пользователя.
        Если введено число, оно сохраняется в глобальном словаре `data` под ключом 'kp',
        затем вызывается функция `creating_a_url` для формирования URL-адреса с использованием введенных данных.
        После этого словарь `data` очищается.
        Если введено не число, пользователю отправляется сообщение об ошибке.

        Args:
            message: Объект `message` от Telegram API, содержащий информацию о сообщении пользователя.
    """
    global data
    if message.text.isdigit():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as dat:
            data['kp'] = message.text
        creating_a_url(message, data)
        data = {}
    else:
        bot.send_message(message.from_user.id, 'Рейтинг - это число')


@bot.message_handler(state=UserInfoState.limit)
def limit(message):
    """
       Обработчик сообщений, принимающий лимит результатов поиска.

       Функция принимает текстовое значение лимита результатов поиска от пользователя,
       сохраняет его в глобальном словаре `data` под ключом 'limit' и вызывает функцию `creating_a_url`
       для формирования URL-адреса с использованием введенных данных.
       Перед вызовом `creating_a_url` устанавливается состояние `UserInfoState.limit`.
       После вызова `creating_a_url` словарь `data` очищается.
       Пользователю отправляется подтверждающее сообщение о принятии лимита.

       Args:
           message: Объект `message` от Telegram API, содержащий информацию о сообщении пользователя.
    """
    global data
    bot.send_message(message.from_user.id, 'Принято\nВот что нашёл')
    bot.set_state(message.from_user.id, UserInfoState.limit, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as dat:
        data['limit'] = message.text
    print("start ---->",data)
    creating_a_url(message, data)
    data = {}
    print("end ---->", data)




if __name__ == '__main__':
    bot.add_custom_filter(StateFilter(bot))
    bot.infinity_polling()
