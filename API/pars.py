from http.client import responses

import requests
import json
import os
import sqlite3
from message_bot.mess import transformation_by_name, transformation_by_kp
from config_data_2.config import API_KEY


transform_triger: bool = False

headers = {
    "accept": "application/json",
    "X-API-KEY": API_KEY
}

inf = {
    "page": '1',
    "limit": '3',
}


def creating_a_url(message, data):
    global transform_triger, inf
    inf.update(data)
    print("pars data ------>",data)
    print("pars inf ------>",inf)
    if 'budget.value' in inf:
        url = f'https://api.kinopoisk.dev/v1.4/movie/random?page=1&limit={inf["limit"]}&budget.value={inf["budget.value"]}'
    elif 'kp' in inf:
        print("KP")
        url = f'https://api.kinopoisk.dev/v1.4/movie/random?page=1&limit={inf["limit"]}&rating.kp={inf["kp"]}'
    else:
        print("HUI")
        url = f'https://api.kinopoisk.dev/v1.4/movie/search?page={inf["page"]}&limit={inf["limit"]}&query={inf["query"]}&genres.name={[inf["genres.name"]]}'
        transform_triger = True
    data = {}
    inf = {"page": '1', "limit": '3',}
    print("pars data end ------>", data)
    print("pars inf  end------>", inf)
    pars(message, url,)

def pars(message, url):
    response = requests.get(url, headers=headers)
    print(str(response))
    json_w(message, response)


def json_w(message, response):
    global transform_triger
    ads = os.path.abspath('movie.json')
    print(ads)
    data = json.loads(response.text)
    print(type(data))
    print(transform_triger)

    with open(ads, 'w') as file:
        json.dump(data, file, indent=4)
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
    if transform_triger:
        transform_triger = False
        transformation_by_name(message, response)
    else:
        transformation_by_kp(message, response)


