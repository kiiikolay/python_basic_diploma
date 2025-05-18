import json
from loguru import logger
from config_data.config import bot

the_finish_inf = {}
content = ["name", "rating", "ageRating", "year", "genres", "description", "poster"]
counter = 0

def check(key, data_list):
    """
    Проверяет наличие ключа в словаре и присваивает значение глобальной переменной the_finish_inf.

    Если ключ отсутствует в словаре data_list, функция ничего не делает.
    Если ключ присутствует, но его значение равно пустой строке,
    в the_finish_inf[key] записывается строка 'Нет'.
    В противном случае, в the_finish_inf[key] записывается значение из data_list[key].

    Args:
        key (str): Ключ для проверки в словаре data_list.
        data_list (dict): Словарь, в котором производится поиск ключа.

    Returns:
        None
    """
    logger.debug(f"Начало проверки ключа: {key} в data_list")

    if key not in data_list:
        logger.debug(f"Ключ {key} отсутствует в data_list.")
        pass
    elif data_list[key] == '':
        the_finish_inf[key] = 'Нет'
        logger.debug(f"Ключ {key} найден, значение - пустая строка. the_finish_inf[{key}] установлено в 'Нет'.")
    else:
        the_finish_inf[key] = data_list[key]
        logger.debug(f"Ключ {key} найден, значение - {data_list[key]}. the_finish_inf[{key}] установлено в {data_list[key]}.")

    logger.debug(f"Окончание проверки ключа: {key}")

def open_json(file):
    """
        Открывает JSON файл, считывает данные и возвращает их в виде списка.

        Аргументы:
            file (str): Путь к JSON файлу.

        Возвращает:
            list: Список данных, считанных из JSON файла.
                  Возвращает пустой список в случае ошибки.
        """
    logger.info(f"Открытие JSON файла: {file}")
    try:
        with open(file, 'r') as source:
            data_list = json.load(source)
        logger.info(f"JSON файл успешно прочитан: {file}")
        return data_list
    except FileNotFoundError:
        logger.error(f"Файл не найден: {file}")
        return []
    except json.JSONDecodeError:
        logger.error(f"Ошибка декодирования JSON в файле: {file}")
        return []
    except Exception as e:
        logger.exception(f"Непредвиденная ошибка при открытии файла {file}: {e}")
        return []

def transformation(message, response, data_list):
    """
    Преобразует входящие данные о фильме, извлекает и форматирует необходимые поля,
    а затем отправляет отформатированное сообщение.

    Аргументы:
        message: Объект сообщения (предположительно, для отправки уведомлений).
        response: Объект ответа (предположительно, из API-запроса, не используется напрямую).
        data_list (dict): Словарь с данными о фильме.

    Возвращает:
        dict: Глобальный словарь 'the_finish_inf' после обработки (очищенный, если все поля обработаны,
              или содержащий частичные данные, если обработка не завершена).

    Глобальные переменные:
        the_finish_inf (dict): Используется для хранения извлеченных и отформатированных данных о фильме.
                               Очищается, если собраны все необходимые данные.
    """

    global the_finish_inf

    logger.debug(f'Входящие данные: {data_list}')

    check('poster', data_list)
    check('ageRating', data_list)
    check('year', data_list)
    check('description', data_list)

    # Обработка жанров
    gen_str = ''
    if 'genres' in data_list:
        for i in data_list['genres']:
            gen_str += f'{i["name"]}|'
        if gen_str == '':
            the_finish_inf['genres'] = 'Не определён'
            logger.warning('Жанры не определены.')
        else:
            the_finish_inf['genres'] = gen_str[:-1]  # Убираем последний символ '|'
            logger.debug(f'Жанры: {the_finish_inf["genres"]}')
    else:
        logger.warning('Ключ "genres" отсутствует в data_list.')
        the_finish_inf['genres'] = 'Не определён'

    # Обработка рейтингов
    if 'rating' in data_list:
        rat_str = (
            f'kp - {str(data_list["rating"].get("kp", "N/A"))} | imdb - {str(data_list["rating"].get("imdb", "N/A"))} | filmCritics - {str(data_list["rating"].get("filmCritics", "N/A"))}\n'
            f'russianFilmCritics - {data_list["rating"].get("russianFilmCritics", "N/A")} | await - {data_list["rating"].get("await", "N/A")}'
        )
        the_finish_inf['rating'] = rat_str
        logger.debug(f'Рейтинги: {the_finish_inf["rating"]}')
    else:
        logger.warning('Ключ "rating" отсутствует в data_list.')
        the_finish_inf['rating'] = 'Не определён'

    # Обработка имени
    if not 'name' in data_list and not 'alternativeName' in data_list:
        logger.warning('Отсутствуют ключи "name" и "alternativeName" в data_list.')
        pass  # Обработка отсутствия ключей
    elif data_list.get('name') == '':  # Использовать .get() для безопасного доступа
        the_finish_inf['name'] = data_list.get('alternativeName', 'Не определено')
        logger.info(f'Имя фильма установлено как alternativeName: {the_finish_inf["name"]}')
    else:
        the_finish_inf['name'] = data_list['name']
        logger.info(f'Имя фильма: {the_finish_inf["name"]}')

    if len(the_finish_inf) == 7:
        checking_the_void(the_finish_inf)
        mess(message, the_finish_inf)
        the_finish_inf = {}
        logger.info('Данные фильма обработаны и отправлены. the_finish_inf очищен.')
    else:
        logger.debug(
            f'the_finish_inf не содержит все необходимые данные (len = {len(the_finish_inf)}). Ожидание дополнительных данных.')
        logger.debug(f'Текущее значение the_finish_inf: {the_finish_inf}')
    return the_finish_inf

def transformation_by_kp(message, response):
    """
    Эта функция выполняет преобразование данных на основе movie.json.

    Она открывает JSON файл "movie.json", передает данные вместе с сообщением
    и ответом в функцию transformation для дальнейшей обработки.

    Args:
        message: Входное сообщение для обработки.
        response: Объект ответа, который нужно заполнить преобразованными данными.

    Returns:
        None
    """
    logger.info(f"Начало обработки с message: {message} и response: {response}")
    try:
        data = open_json("movie.json")
        logger.debug(f"Данные из movie.json успешно загружены: {data}")
        transformation(message, response, data)
        logger.info("Преобразование данных завершено.")
    except Exception as e:
        logger.error(f"Произошла ошибка во время преобразования: {e}")
        raise  # Важно перебросить исключение, чтобы оно не было проигнорировано

def transformation_by_name(message, response):
    """
    Функция выполняет преобразование данных о фильме на основе имени, полученного из входящего сообщения.
    Она открывает JSON-файл "movie.json", итерируется по документам (фильмам) в этом файле и применяет
    функцию `transformation` к каждому фильму.

    Args:
        message: Входящее сообщение, содержащее информацию для поиска фильма.
        response: Объект ответа, который будет обновляться информацией о найденном фильме.

    Returns:
        None
    """
    logger.info("Начало обработки transformation_by_name")
    data = open_json("movie.json")
    logger.debug(f"Данные из movie.json: {data}")
    print(data)
    for i in data["docs"]:
        transformation(message, response, i)
    logger.info("Завершение обработки transformation_by_name")




def checking_the_void(the_finish_inf):
    """
    Рекурсивно проверяет словарь на наличие пустых строк или значений None и заменяет их на " Нет".

    Args:
        the_finish_inf (dict): Словарь, который необходимо проверить.

    Returns:
        None: Функция изменяет словарь напрямую.
    """
    logger.debug(f"Проверка словаря: {the_finish_inf}")
    for i_inf in the_finish_inf:
        logger.debug(f"Проверка ключа: {i_inf}")
        if isinstance(the_finish_inf[i_inf], dict):
            logger.debug(f"Ключ {i_inf} является словарем, рекурсивный вызов.")
            checking_the_void(the_finish_inf[i_inf])
        elif the_finish_inf[i_inf] == '' or the_finish_inf[i_inf] is None:
            logger.warning(f"Найдено пустое значение для ключа {i_inf}, замена на ' Нет'")
            the_finish_inf[i_inf] = ' Нет'
        else:
            logger.debug(f"Ключ {i_inf} не является пустым.")



def mess(message, i_data):
    """
    Отправляет отформатированное сообщение в чат Telegram на основе переданных данных.

    Args:
        message: Объект сообщения Telegram от библиотеки pyTelegramBotAPI.
        i_data: Словарь, содержащий информацию для формирования сообщения.
                Ожидается, что словарь будет содержать ключи: "name", "rating",
                "ageRating", "year", "genres", "description", "poster".

    Returns:
        None. Функция отправляет сообщение и ничего не возвращает.
    """
    logger.info(f"Обработка данных для: {i_data['name']}")  # Логируем начало обработки
    logger.debug(f"Входные данные: {i_data}")  # Логируем входные данные (опционально, для отладки)

    try:
        mess_text = (
            f'Название: {i_data["name"]}\n\n'
            f'Рейтинг: {i_data["rating"]}\n\n'
            f'Возрастной рейтинг: {i_data["ageRating"]}\n\n'
            f'Год выхода: {i_data["year"]}\n\n'
            f'Жанр: {i_data["genres"]}\n\n'
            f'Описание: {i_data["description"]}\n'
            f'Постер: {i_data["poster"]}'
        )

        # Убираем .format(), так как f-строки уже форматируют
        bot.send_message(message.chat.id, mess_text)

        logger.info(f"Сообщение успешно отправлено для: {i_data['name']}")  # Логируем успешную отправку

    except KeyError as e:
        logger.error(f"Ошибка KeyError при обработке данных для {i_data.get('name', 'неизвестно')}: Отсутствует ключ {e}")
    except Exception as e:
        logger.exception(f"Непредвиденная ошибка при обработке данных для {i_data.get('name', 'неизвестно')}: {e}")