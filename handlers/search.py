from telebot import types
from telebot.types import Message
from loguru import logger
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
def by_high_budget(message: Message):
    """
        Обработчик команды '/high_budget_movie'.

        Устанавливает значение бюджета фильма в диапазоне от 25,000,000 до 5,000,000,000,
        отправляет пользователю сообщение о фильме с высоким бюджетом и вызывает функцию
        `creating_a_url` для формирования и отправки URL с результатами поиска.

        Args:
            message (telebot.types.Message): Объект сообщения от Telegram.
    """
    logger.info(f"Пользователь {message.from_user.id} запросил фильм с высоким бюджетом.")
    global data_key, data_val
    data['budget.value'] = '25000000-5000000000'
    logger.debug(f"Установлен бюджет фильма: {data['budget.value']}")
    bot.send_message(message.chat.id, "Вот фильм с высоким бюджетом")
    logger.debug(f"Отправлено сообщение пользователю {message.from_user.id}.")
    creating_a_url(message, data)
    logger.info(f"Функция создания URL вызвана для пользователя {message.from_user.id}.")


@bot.message_handler(commands=['low_budget_movie'])
def by_low_budget(message: Message):
    """
        Обработчик команды '/low_budget_movie'.

        Устанавливает значение бюджета фильма в диапазоне от 0 до 25,000,000,
        отправляет пользователю сообщение о фильме с низким бюджетом и вызывает функцию
        `creating_a_url` для формирования и отправки URL с результатами поиска.

        Args:
            message (telebot.types.Message): Объект сообщения от Telegram.
    """
    logger.info(f"Пользователь {message.from_user.id} запросил фильм с высоким бюджетом.")
    global data_key, data_val
    data['budget.value'] = '0-25000000'
    logger.debug(f"Установлен бюджет фильма: {data['budget.value']}")
    bot.send_message(message.chat.id, "Вот фильм с низким бюджетом")
    logger.debug(f"Отправлено сообщение пользователю {message.from_user.id}.")
    creating_a_url(message, data)
    logger.info(f"Функция создания URL вызвана для пользователя {message.from_user.id}.")


@bot.message_handler(commands=['movie_by_rating'])
def by_ratting(message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    logger.info(f"Пользователь {user_id} (чат {chat_id}) инициировал команду /movie_by_rating.")

    try:
        bot.send_message(user_id, 'Привет!\nВведи рейтинг')
        bot.set_state(user_id, UserInfoState.search_by_name_upp_rat, chat_id)
        logger.debug(f"Состояние пользователя {user_id} (чат {chat_id}) установлено в UserInfoState.search_by_name_upp_rat.")

    except Exception as e:
        logger.error(f"Ошибка при обработке /movie_by_rating для пользователя {user_id} (чат {chat_id}): {e}")
        # Отправка сообщения об ошибке пользователю (опционально)
        bot.send_message(user_id, "Произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте позже.")


@bot.message_handler(commands=['movie_search'])
def by_name(message):
    """
    Обработчик команды /movie_search.

    Отправляет приветственное сообщение пользователю и запрашивает название фильма для поиска.
    Устанавливает состояние пользователя в UserInfoState.search_by_name для ожидания ввода названия фильма.

    Args:
        message: Объект сообщения от Telegram.
    """
    user_id = message.from_user.id
    chat_id = message.chat.id

    logger.info(f"Пользователь {user_id} (чат {chat_id}) инициировал команду /movie_search.")

    try:
        bot.send_message(user_id, 'Привет!\nВведи название')
        bot.set_state(user_id, UserInfoState.search_by_name, chat_id)
        logger.debug(f"Состояние пользователя {user_id} установлено в UserInfoState.search_by_name")
    except Exception as e:
        logger.error(f"Ошибка при обработке команды /movie_search для пользователя {user_id}: {e}")


@bot.message_handler(state=UserInfoState.search_by_name)
def name(message: Message):
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
    user_id = message.from_user.id
    chat_id = message.chat.id

    logger.info(f"Пользователь {user_id} в чате {chat_id} ввел название фильма: {message.text}")

    if data_key != '':
        try:
            with bot.retrieve_data(user_id, chat_id) as dat:
                data[data_key] = data_val
                logger.debug(f"Сохранены предыдущие данные: data[{data_key}] = {data_val}")
        except Exception as e:
            logger.error(f"Ошибка сохранения предыдущих данных: {e}")

    try:
        bot.send_message(user_id, 'Принято. Теперь выбери жанр', reply_markup=genre_markup())
        bot.set_state(user_id, UserInfoState.genre, chat_id)
        logger.debug(f"Пользователь {user_id} перешел в состояние UserInfoState.genre")
    except Exception as e:
        logger.error(f"Ошибка отправки сообщения выбора жанра или установки состояния: {e}")

    try:
        with bot.retrieve_data(user_id, chat_id) as dat:
            logger.debug(f"Получены данные: {dat}")
            data['query'] = message.text
            logger.debug(f"Сохранено название фильма в data['query']: {message.text}")
    except Exception as e:
        logger.error(f"Ошибка сохранения названия фильма в data['query']: {e}")


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
    user_id = message.from_user.id
    chat_id = message.chat.id

    logger.info(f"Пользователь {user_id} в чате {chat_id} вошел в обработчик жанра.")

    try:
        bot.send_message(user_id, 'Принято, теперь напиши, сколько вариантов фильмов показать (число).')
        bot.set_state(user_id, UserInfoState.limit, chat_id)

        with bot.retrieve_data(user_id, chat_id) as dat:
            data['genres.name'] = message.text
            logger.info(f"Пользователь {user_id} выбрал жанр: {message.text}. Сохранено в data['genres.name'].")

    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
        bot.send_message(user_id, f"Произошла ошибка: {e}")

    finally:
        logger.debug(f"Пользователь {user_id} перешел в состояние UserInfoState.limit.")

@bot.message_handler(state=UserInfoState.search_by_name_upp_rat, func=lambda message: True)
def by_name_upp_rat(message: Message):
    """
    Обработчик сообщений, принимающий рейтинг фильма (Кинопоиска).

    Функция ожидает числовое значение рейтинга Кинопоиска от пользователя.
    Если введено число, оно сохраняется в глобальном словаре data под ключом 'kp',
    затем вызывается функция creating_a_url для формирования URL-адреса с использованием введенных данных.
    После этого словарь data очищается.
    Если введено не число, пользователю отправляется сообщение об ошибке.

    Args:
        message: Объект message от Telegram API, содержащий информацию о сообщении пользователя.
    """

    global data

    logger.info(f"Получено сообщение от пользователя {message.from_user.id}: {message.text}")

    if message.text.isdigit():
        logger.debug(f"Введено число: {message.text}. Сохраняем рейтинг.")
        with bot.retrieve_data(message.from_user.id, message.chat.id) as dat:
            # Достаём данные из хранилища
            data = dat  # Теперь data это локальная переменная, которая ссылается на данные из хранилища
            data['kp'] = message.text
            logger.debug(f"Данные из хранилища: {data}")
        bot.set_state(message.from_user.id, UserInfoState.search_by_name_upp_rat, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as dat:
            dat['kp'] = message.text
            logger.debug(f"Данные из хранилища после обновления: {dat}")

        logger.info("Вызываем функцию creating_a_url.")
        creating_a_url(message, data)
        logger.info("Функция creating_a_url завершена.")

        # Очищаем данные в хранилище
        logger.info("Очищаем данные пользователя и хранилище.")
        bot.delete_state(message.from_user.id, message.chat.id)
        data = {}  # Очищаем локальную переменную
        logger.debug("Данные пользователя и хранилище очищены.")
    else:
        logger.warning(f"Введено не число: {message.text}. Отправляем сообщение об ошибке.")
        bot.send_message(message.from_user.id, 'Рейтинг - это число!')
        logger.info("Сообщение об ошибке отправлено пользователю.")


@bot.message_handler(state=UserInfoState.limit)
def limit(message):
    """
    Обработчик сообщений, принимающий лимит результатов поиска.

    Функция принимает текстовое значение лимита результатов поиска от пользователя,
    сохраняет его в глобальном словаре data под ключом 'limit' и вызывает функцию creating_a_url
    для формирования URL-адреса с использованием введенных данных.
    Перед вызовом creating_a_url устанавливается состояние UserInfoState.limit.
    После вызова creating_a_url словарь data очищается.
    Пользователю отправляется подтверждающее сообщение о принятии лимита.

    Args:
        message: Объект message от Telegram API, содержащий информацию о сообщении пользователя.
    """

    global data
    user_id = message.from_user.id
    chat_id = message.chat.id
    limit_value = message.text

    logger.info(f"Пользователь {user_id} в чате {chat_id} ввел лимит: {limit_value}")
    bot.send_message(user_id, 'Принято\nВот что нашёл')
    logger.debug(f"Пользователю {user_id} отправлено подтверждающее сообщение.")

    bot.set_state(user_id, UserInfoState.limit, chat_id)
    logger.debug(f"Для пользователя {user_id} установлено состояние UserInfoState.limit.")

    with bot.retrieve_data(user_id, chat_id) as dat:
        data['limit'] = limit_value
        logger.debug(f"B data['limit'] сохранено значение: {limit_value}.")

    logger.debug(f"Значение data перед вызовом creating_a_url: {data}")

    creating_a_url(message, data)
    logger.info(f"Вызвана функция creating_a_url для пользователя {user_id}.")

    data = {}
    logger.debug("Словарь data очищен.")
    logger.debug(f"Значение data после очистки: {data}")
    logger.info(f"Обработка лимита для пользователя {user_id} завершена.")





