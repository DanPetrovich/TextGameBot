from aiogram import types

chose_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

chose_menu = [types.KeyboardButton('Воин'),
              types.KeyboardButton('Маг')]

for item in chose_menu:
    chose_markup.add(item)

main_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

main_menu = [types.KeyboardButton('Начать игру')]

for item in main_menu:
    main_markup.add(item)

characteristic = types.KeyboardButton('Глянуть свои статы')

city_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
city_menu = [types.KeyboardButton('Отправится по локациям'),
             types.KeyboardButton('В магазин'), characteristic]

for item in city_menu:
    city_markup.add(item)

locations_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
loc_menu = [types.KeyboardButton('Отправиться в Последнее Подземелье'),
            types.KeyboardButton('Отправиться в Забытый Лес')]

for item in loc_menu:
    locations_markup.add(item)

fight_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
fight_menu = [types.KeyboardButton('Буду драться!'),
            types.KeyboardButton('эээ, не хочу с ним сражаться'),
              types.KeyboardButton('А насколько он силен?'), characteristic]

for item in fight_menu:
    fight_markup.add(item)
