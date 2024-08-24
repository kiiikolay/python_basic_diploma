import json
from config_data.config import bot

def transformation(message, response):
    the_finish_inf = {}
    with open('movie.json', 'r') as source:
        data = json.load(source)
        print('data--->', data)
        for i in data:
            data_list = i
            print('i---> ',data_list)

            if 'poster' not in data_list or data_list['poster'] == '':
                the_finish_inf['poster'] = 'Нет'
            else:
                the_finish_inf['poster'] = data_list['poster']
            the_finish_inf['ageRating'] = data_list['ageRating']
            the_finish_inf['year'] = data_list['year']
            the_finish_inf['description'] = data_list['description']
#_______________________________________________________________________________
            gen_str = ''
            for i in data_list['genres']:
                gen_str += f'{i["name"]}|'
                if gen_str == '':
                    the_finish_inf['genres'] = 'Не определён'
                else:
                    the_finish_inf['genres'] = gen_str
#_______________________________________________________________________________
            rat_str = ''
            rat_str += (f'kp - {str(data_list["rating"]["kp"])} | imdb - {str(data_list["rating"]["imdb"])} | filmCritics - {str(data_list["rating"]["filmCritics"])}\n'
                        f'russianFilmCritics - {data_list["rating"]["russianFilmCritics"]} | await - {data_list["rating"]["await"]}')
            the_finish_inf['rating'] = rat_str
#_______________________________________________________________________________
            if data_list['name'] == '':
                the_finish_inf['name'] = data_list['alternativeName']
            else:
                the_finish_inf['name'] = data_list['name']
            checking_the_void(message, the_finish_inf)
            mess(message, the_finish_inf)

def checking_the_void(message, the_finish_inf):
    for i_inf in the_finish_inf:
        if isinstance(the_finish_inf[i_inf], dict):
            checking_the_void(message, the_finish_inf[i_inf])
        elif the_finish_inf[i_inf] == '' or the_finish_inf[i_inf] == None:
            the_finish_inf[i_inf] = ' Нет'



def mess(message, i_data):
    mess = (f'Название: {i_data["name"]}\n\n'
            f'Рейтинг: {i_data["rating"]}\n\n'
            f'Возрастной рейтинг: {i_data["ageRating"]}\n\n'
            f'Год выхода: {i_data["year"]}\n\n'
            f'жанр: {i_data["genres"]}\n\n'
            f'Описание: {i_data["description"]}\n'
            f'Постер: {i_data["poster"]}')
    bot.send_message(message.chat.id, '{}'.format(mess))