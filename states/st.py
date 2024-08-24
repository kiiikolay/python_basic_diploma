from telebot.handler_backends import State, StatesGroup

class UserInfoState(StatesGroup):
    search_by_name = State()
    genre = State()
    limit = State()
    search_by_budget = State()
    search_by_rating = State()
    search_by_name_upp_rat = State()

