import json
from config_data_2.config import bot

the_finish_inf = {}
content = ["name", "rating", "ageRating", "year", "genres", "description", "poster"]
counter = 0

def check(key, data_list):
    global the_finish_inf
    if key not in data_list:
        pass
    elif data_list[key] == '':
        the_finish_inf[key] = 'Нет'
    else:
        the_finish_inf[key] = data_list[key]

def open_json(file):
    with open(file, 'r') as source:
        data_list = json.load(source)
    return data_list

def transformation(message, response, data_list):
    global the_finish_inf

    print('i---> ', data_list)

    check('poster', data_list)
    check('ageRating', data_list)
    check('year', data_list)
    check('description', data_list)
    # _______________________________________________________________________________
    gen_str = ''
    if 'genres' in data_list:
        for i in data_list['genres']:
            gen_str += f'{i["name"]}|'
            if gen_str == '':
                the_finish_inf['genres'] = 'Не определён'
            else:
                the_finish_inf['genres'] = gen_str
    # _______________________________________________________________________________
    if 'rating' in data_list:
        rat_str = ''
        rat_str += (
            f'kp - {str(data_list["rating"]["kp"])} | imdb - {str(data_list["rating"]["imdb"])} | filmCritics - {str(data_list["rating"]["filmCritics"])}\n'
            f'russianFilmCritics - {data_list["rating"]["russianFilmCritics"]} | await - {data_list["rating"]["await"]}')
        the_finish_inf['rating'] = rat_str
    # _______________________________________________________________________________
    if not 'name' in data_list or not 'alternativeName' in data_list:
        pass
    elif data_list['name'] == '':
        the_finish_inf['name'] = data_list['alternativeName']
    else:
        the_finish_inf['name'] = data_list['name']

    if len(the_finish_inf) == 7:
        checking_the_void(the_finish_inf)
        mess(message, the_finish_inf)
        the_finish_inf = {}


    # for elem in content:
    #     if elem in the_finish_inf:
    #         counter =+ 1




    return the_finish_inf

def transformation_by_kp(message, response):
    data = open_json("movie.json")
    transformation(message, response, data)

def transformation_by_name(message, response):
    data = open_json("movie.json")
    print(data)
    for i in data["docs"]:
        transformation(message, response, i)




def checking_the_void(the_finish_inf):
    for i_inf in the_finish_inf:
        if isinstance(the_finish_inf[i_inf], dict):
            checking_the_void(the_finish_inf[i_inf])
        elif the_finish_inf[i_inf] == '' or the_finish_inf[i_inf] is None:
            the_finish_inf[i_inf] = ' Нет'



def mess(message, i_data):
    print("----->>>>>", i_data)
    mess = (f'Название: {i_data["name"]}\n\n'
            f'Рейтинг: {i_data["rating"]}\n\n'
            f'Возрастной рейтинг: {i_data["ageRating"]}\n\n'
            f'Год выхода: {i_data["year"]}\n\n'
            f'жанр: {i_data["genres"]}\n\n'
            f'Описание: {i_data["description"]}\n'
            f'Постер: {i_data["poster"]}')
    bot.send_message(message.chat.id, '{}'.format(mess))