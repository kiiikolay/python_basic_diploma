import requests
import json
import os
import sqlite3
from message_bot.mess import transformation
from config_data.config import API_KEY


headers = {
    "accept": "application/json",
    "X-API-KEY": API_KEY
}

inf = {
    "page": '1',
    "limit": '3',
}


def creating_a_url(message, data):
    inf.update(data)
    print(data)
    print(inf)
    if 'budget.value' in inf:
        url = f'https://api.kinopoisk.dev/v1.4/movie/random?page=1&limit={inf["limit"]}&budget.value={inf["budget.value"]}'
    elif 'kp' in inf:
        url = f'https://api.kinopoisk.dev/v1.4/movie/random?page=1&limit={inf["limit"]}&rating.kp={inf["kp"]}'
    else:
        url = f'https://api.kinopoisk.dev/v1.4/movie/search?page={inf["page"]}&limit={inf["limit"]}&query={inf["query"]}&genres.name={[inf["genres.name"]]}'
    pars(message, url)

def pars(message, url):
    response = requests.get(url, headers=headers)
    print(str(response))
    json_w(message, response)


def json_w(message, response):
    ads = os.path.abspath('movie.json')
    print(ads)
    data = json.loads(response.text)
    min_data = data['docs']
    with open(ads, 'w') as file:
        json.dump(min_data, file, indent=4)
    # with sqlite3.connect('movie.db') as db:
    #     cur = db.cursor()
    #     Q = (""" CREATE TABLE story (
    #   id bigint PRIMARY KEY,
    #   status varchar(20) NOT NULL,
    #   amount number(10) NOT NULL,
    #   fee number(10) NOT NULL,
    #   shop_id number(10) NOT NULL,
    #   type_pay varchar(20)
    #  """)
    transformation(message, response)


