from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import json
import os

def genre_markup():
    """
    Создает ReplyKeyboardMarkup с кнопками жанров из файла 'genre.json'.

    Функция читает данные о жанрах из JSON-файла, расположенного в поддиректории
    'data_for_marks' относительно текущего местоположения скрипта.
    На основе этих данных формируются кнопки клавиатуры, которые добавляются
    в объект ReplyKeyboardMarkup.  Кнопки добавляются построчно, по три кнопки в ряд,
    до тех пор, пока не закончатся жанры в файле.

    Returns:
        ReplyKeyboardMarkup: Объект клавиатуры с кнопками жанров.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, 'data_for_marks', 'genre.json')

    buttons = []
    markup = ReplyKeyboardMarkup(True, True)
    with open(file_path, 'r', encoding='utf8') as gen:
        data = json.load(gen)
        buttons = [KeyboardButton(i_gen['name']) for i_gen in data]
        markup.add(buttons[0], buttons[1], buttons[2])
        markup.add(buttons[3], buttons[4], buttons[5])
        markup.add(buttons[6], buttons[7], buttons[8])
        markup.add(buttons[9], buttons[10], buttons[11])
        markup.add(buttons[12], buttons[13], buttons[14])
        markup.add(buttons[15], buttons[16], buttons[17])
        markup.add(buttons[18], buttons[19], buttons[20])
        markup.add(buttons[21], buttons[22], buttons[23])
        markup.add(buttons[24], buttons[25], buttons[26])
        markup.add(buttons[27], buttons[28], buttons[29])
        markup.add(buttons[30], buttons[31])

    return markup