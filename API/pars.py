from http.client import responses

import requests
import json
import os
from loguru import logger
from telebot.types import Message
import sqlite3
from message_bot.mess import transformation_by_name, transformation_by_kp
from config_data.config import API_KEY


transform_triger: bool = False

headers = {
    "accept": "application/json",
    "X-API-KEY": API_KEY
}

inf = {
    "page": '1',
    "limit": '3',
}


def creating_a_url(message: Message, data):
    """
    Создает URL для запроса к API Kinopoisk на основе входящих данных и параметров.

    Функция принимает сообщение и словарь данных, обновляет глобальный словарь `inf`
    этими данными, а затем формирует URL для API Kinopoisk в зависимости от наличия
    определенных ключей в `inf`. URL используется для случайного выбора фильмов
    с учетом бюджета, рейтинга или для поиска фильмов по запросу, странице, лимиту и жанру.
    Также функция изменяет глобальную переменную `transform_triger` в случае поиска по запросу.
    В конце функция сбрасывает словари `data` и `inf` к начальным значениям и вызывает функцию pars с сообщением и созданным URL.

    Args:
        message: Сообщение, передаваемое в функцию `pars`.
        data (dict): Словарь с данными для обновления глобального словаря `inf`.

    Returns:
        None. Функция вызывает другую функцию `pars` и не возвращает значения напрямую.

    Global Variables:
        transform_triger (bool): Глобальный триггер, который устанавливается в True,
                                  если выполняется поиск по запросу.
        inf (dict): Глобальный словарь, содержащий параметры для формирования URL.
                    Изначально содержит параметры страницы и лимита.
    """
    global transform_triger, inf
    logger.debug(f"Начало creating_a_url c data: {data} и inf: {inf}")
    inf.update(data)
    logger.debug(f"Обновленный inf: {inf}")

    if 'budget.value' in inf:
        logger.info("Формирование URL на основе бюджета.")
        url = f'https://api.kinopoisk.dev/v1.4/movie/random?page=1&limit={inf["limit"]}&budget.value={inf["budget.value"]}'
    elif 'kp' in inf:
        logger.info("Формирование URL на основе рейтинга КР.")
        url = f'https://api.kinopoisk.dev/v1.4/movie/random?page=1&limit={inf["limit"]}&rating.kp={inf["kp"]}'
    else:
        logger.info("Формирование URL на основе запроса, страницы, лимита и жанра.")
        url = f'https://api.kinopoisk.dev/v1.4/movie/search?page={inf["page"]}&limit={inf["limit"]}&query={inf["query"]}&genres.name={inf["genres.name"]}'
        transform_triger = True
        logger.debug(f"transform_triger установлен в True")

    logger.debug(f"Сформированный URL: {url}")

    data = {}
    inf = {"page": '1', "limit": '3',}
    logger.debug(f"Сброс data: {data} и inf: {inf}")

    logger.info("Вызов функции pars с message и url.")
    pars (message, url,)
    logger.debug("Завершение creating_a_url")

def pars(message: Message, url):
    """
    Выполняет GET-запрос к указанному URL-адресу, логирует ответ и обрабатывает полученные данные.

    Args:
        message (Message): Объект сообщения (например, из aiogram), который может использоваться
                           для передачи дополнительной информации или контекста операции. На данный
                           момент не используется внутри функции, но может быть полезен для расширения
                           функциональности в будущем (например, логирование ID чата).
        url (str): URL-адрес для выполнения GET-запроса.

    Returns:
        None. Функция записывает логи и вызывает функцию json_w для обработки ответа.

    Raises:
        requests.exceptions.RequestException: Если при выполнении GET-запроса возникла ошибка,
                                               например, сетевая проблема или неверный URL. Логируется.
        Exception: Любая другая ошибка, возникшая при обработке, также логируется.

    Пример использования:
    """
    try:
        logger.info(f"Выполняется GET-запрос к URL: {url}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Проверка на НТТР ошибки (4xx, 5xx)
        logger.debug(f"Получен ответ: {response}")  # Более подробный лог, который можно отключить в production

        json_w(message, response)  # Предполагается, что json_w обрабатывает response
        logger.info(f"Успешно обработан ответ от {url}")

    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при выполнении GET-запроса к {url}: {e}")
    except Exception as e:
        logger.exception(f"Произошла ошибка при обработке ответа от {url}: {e}")


def json_w(message, response):
    """
    Сохраняет JSON-ответ в файл movie.json и выполняет трансформацию данных.
    Функция получает объект сообщения и ответ от API, сохраняет JSON-ответ в файл
    movie.json с отступами для читаемости. После сохранения вызывает одну из функций
    трансформации данных в зависимости от значения глобальной переменной transform_triger.

    Аргументы:
        message: Объект сообщения (тип не указан, необходимо смотреть контекст использования).
        response: Объект ответа от API, содержащий JSON-данные.

    Глобальные переменные:
        transform_triger: Флаг, определяющий, какую функцию трансформации использовать.
                            Изменяется внутри функции.

    Логика:
    1. Определяет абсолютный путь к файлу movie.json.
    2. Загружает JSON-данные из текста ответа.
    3. Записывает JSON-данные в файл movie.json c отступами.
    4. В зависимости от значения transform_triger, вызывает одну из функций трансформации:
        - Если transform_triger равен True, вызывает transformation_by_name и устанавливает transform_triger в False.
        - Если transform_triger paвен False, вызывает transformation_by_kp.
    """
    global transform_triger  # Используем глобальную переменную

    ads = os.path.abspath('movie.json')
    logger.debug(f"Абсолютный путь к movie.json: {ads}")  # Логируем абсолютный путь

    try:
        data = json.loads(response.text)
        logger.debug(f"Тип данных: {type(data)}")  # Логируем тип данных
    except json.JSONDecodeError as e:
        logger.error(f"Не удалось декодировать JSON: {e}")
        return  # Или другое адекватное поведение при ошибке

    logger.debug(f"transform_triger: {transform_triger}")  # Логируем значение transform_triger

    try:
        with open(ads, 'w', encoding='utf-8') as file:  # Указываем кодировку utf-8
            json.dump(data, file, indent=4, ensure_ascii=False)  # Отключаем ASCII кодирование
        logger.info(f"Успешно записаны данные в {ads}")  # Логируем успешную запись
    except Exception as e:
        logger.error(f"Не удалось записать в файл: {e}")
        return  # Или другое адекватное поведение при ошибке

    if transform_triger:
        transform_triger = False
        logger.info("Вызов transformation_by_name")
        transformation_by_name(message, response)
    else:
        logger.info("Вызов transformation_by_kp")
        transformation_by_kp(message, response)


