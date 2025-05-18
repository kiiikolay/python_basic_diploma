from telebot.handler_backends import State, StatesGroup

class UserInfoState(StatesGroup):
    """
    Этот класс представляет собой набор состояний, используемых для управления
    диалогом с пользователем при поиске фильмов.  Каждое состояние соответствует
    определенному этапу сбора информации от пользователя.

    Атрибуты:
        search_by_name: Состояние ожидания ввода названия фильма для поиска.
        genre: Состояние ожидания выбора жанра фильма.
        limit: Состояние ожидания ввода количества фильмов для отображения.
        search_by_budget: Состояние ожидания ввода бюджета фильма.
        search_by_rating: Состояние ожидания ввода рейтинга фильма.
        search_by_name_upp_rat: Состояние ожидания ввода названия фильма для поиска с последующей фильтрацией по рейтингу.
        end_budget: Состояние ожидания ввода верхней границы бюджета фильма.
    """
    search_by_name = State()
    genre = State()
    limit = State()
    search_by_budget = State()
    search_by_rating = State()
    search_by_name_upp_rat = State()
    end_budget = State()

