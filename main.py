from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
import logging
import config
import inline_keyboard
import sqlite3
import time
import random
import models
import math

logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=config.bot_token)
dp = Dispatcher(bot, storage=storage)

person = models.Person()
mob = models.Mob()

images = {
    'shop': 'https://cdnb.artstation.com/p/assets/images/images/035/267/853/large/grant-hall-screenshot00014.jpg?1614548439',
    'forest': 'https://www.renderhub.com/zames1992d/cartoon-tree-forest/cartoon-tree-forest-03.jpg',
    'cave': 'https://img-new.cgtrader.com/items/258244/d56bce4c70/cave-3d-model-max.jpg'}


class dialog(StatesGroup):
    fither_type = State()
    fight = State()
    win_fight = State()


def up_level():
    global person
    if person.xp >= person.level * 5 + 5:
        person.xp -= person.level * 5 + 5
        person.level += 1
    print(person.xp, person.level)


def create_enemy():
    global person
    global mob
    mob_type = 0
    if person.magic_attack > 1:
        mob_type = random.randint(0, 1)
    if mob_type == 1:
        mob.attack_type = mob.Type.Magic
        mob.attack = max(person.attack - random.randint(0, 2), 1)
        mob.magic_attack = person.magic_attack + random.randint(0, 2)
        mob.armour = max(person.armour - random.randint(0, 2), 0)
        mob.magic_armour = max(person.magic_attack + random.randint(-1, 1), 0)
        mob.hp = max(person.hp - random.randint(-1, 2), 5)
    else:
        mob.attack_type = mob.Type.Physical
        mob.attack = person.attack + random.randint(0, 2)
        mob.magic_attack = max(person.magic_attack - random.randint(0, 2), 0)
        mob.armour = person.armour + random.randint(0, 2)
        mob.magic_armour = max(person.magic_armour - random.randint(0, 2), 0)
        mob.hp = person.hp + random.randint(-2, 3)


def probability():
    global person
    global mob
    print(mob.get_stats())
    print(mob.attack_type)
    prob = 0.5
    magic_attack_dif = person.magic_attack - mob.magic_attack
    magic_arm_dif = person.magic_armour - mob.magic_armour
    magic_dif = magic_arm_dif + magic_attack_dif
    physical_dif = person.attack - mob.attack + person.armour - mob.armour

    if mob.attack_type == mob.Type.Magic:
        prob += ((magic_dif + 2) / 4) * 0.6
        prob += ((physical_dif + 2) / 4) * 0.2
    else:
        prob += ((magic_dif + 2) / 4) * 0.2
        prob += ((physical_dif + 2) / 4) * 0.6
    prob += ((person.hp - mob.hp + 2) / 4) * 0.2

    return max(0.0, prob)


def get_enemy_stats():
    global mob
    text = f'Ухх, у этого гада такие характеристики\n'
    for name, val in mob.get_stats().items():
        text += f'{name} - {val}\n'
    return text


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    text = 'Здравствуй, отважный воин и безрассудный искатель приключений\n' \
           'Здесь тебя ждет увлекательное путешествие в мир, полный опастностей и увлекательных созданий'
    await message.answer(text=text)
    time.sleep(2.5)
    text = "Сначала надо выбрать класс бойца. Воин или Маг?"
    await message.answer(text=text)
    text = f'У Воина такие характеристики: \n' \
           f'Здоровье - {models.Warrior.hp}\n' \
           f'Атака - {models.Warrior.attack} \n' \
           f'Броня - {models.Warrior.armour}'
    await message.answer(text=text)
    text = f'У Мага такие характеристики: \n' \
           f'Здоровье - {models.Magician.hp}\n' \
           f'Атака - {models.Magician.attack} \n' \
           f'Магическая атака - {models.Magician.magic_attack}\n ' \
           f'Магическая броня - {models.Magician.magic_armour}'
    await message.answer(text=text, reply_markup=inline_keyboard.chose_markup)
    await dialog.fither_type.set()


@dp.message_handler(state=dialog.fither_type)
async def magician(message: types.Message, state: FSMContext):
    global person
    if message.text == "Маг":
        person = models.Magician()
    else:
        person = models.Warrior()

    person.nickname = message.from_user.username
    person.user_id = message.from_user.id

    text = 'Отличный выбор! Уверен, эти навки понадобятся тебе в твоем путешествии'
    await message.answer(text=text)
    text = 'Король отправил тебя за головой старой ведьмы, которая отравляет жизнь славным жителям КорольГрада\n' \
           'Готов ли ты начать свое путешествие?'
    await message.answer(text=text, reply_markup=inline_keyboard.main_markup)

    await state.finish()


@dp.message_handler(content_types='text', text='Начать игру')
async def start_game(message: types.Message):
    output = 'Свое путешествие ты начинаешь в городе КорольГрад, ' \
             'здесь ты можешь купить кое-какое снаряжение, восстановить здоровье и ману\n' \
             'Так же ты всегда можешь посмотреть свои навыки и характеристики'
    await message.answer(text=output, reply_markup=inline_keyboard.city_markup)


@dp.message_handler(content_types='text', text='В магазин')
async def shop(message: types.Message):
    text = 'Сори, у нас на прошлой неделе от чумы помер кассир, теперь СанПин заставил все тут чистить...\n' \
           'так что пока можешь просто полюбоваться видом'
    await bot.send_photo(message.chat.id, photo=images['shop'], caption=text)


@dp.message_handler(content_types='text', text='Глянуть свои статы')
async def skills(message: types.Message):
    global person
    text = f'Твои характеристики:\n'
    for name, val in person.get_stats().items():
        text += f'{name} - {val}\n'

    await message.answer(text=text, reply_markup=inline_keyboard.city_markup)


@dp.message_handler(content_types='text', text='Отправится по локациям')
async def location(message: types.Message):
    text = 'Ну что ж, твое приключение начинается!\n' \
           'Куда отправишься сначала?'
    await message.answer(text=text, reply_markup=inline_keyboard.locations_markup)


@dp.message_handler(content_types='text', text='Отправиться в Последнее Подземелье')
async def underground(message: types.Message):
    global mob
    text = 'Ты вышел за стены города и отправился в подземелье'
    await message.answer(text=text, reply_markup=types.ReplyKeyboardRemove())

    time.sleep(3)

    text = 'Через полтора дня пути ты достиг входа в мрачные пещеры'
    await bot.send_photo(message.chat.id, photo=images['cave'],
                         caption=text)

    text = 'Опаньки! Ты нашел прикольный сундук'
    await message.answer(text=text)

    create_enemy()

    await message.answer(text='но вот незадача, его охраняет злобный, мелкий гоблин',
                         reply_markup=inline_keyboard.fight_markup)

    await dialog.fight.set()


@dp.message_handler(state=dialog.fight)
async def fight(message: types.Message, state: FSMContext):
    global person
    if message.text == 'Глянуть свои статы':

        text = f'Твои характеристики:\n'
        for name, val in person.get_stats().items():
            text += f'{name} - {val}\n'

        await message.answer(text=text, reply_markup=inline_keyboard.fight_markup)
    else:
        global mob
        if message.text == 'А насколько он силен?':
            await message.answer(text=get_enemy_stats(), reply_markup=inline_keyboard.fight_markup)
        else:
            prob = probability()
            if message.text == 'Буду драться!':
                if prob >= 0.55:
                    await message.answer(text="Это было просто, он повержен)")
                    magic_attack_dif = person.magic_attack - mob.magic_attack
                    magic_arm_dif = person.magic_armour - mob.magic_armour
                    magic_dif = magic_arm_dif + magic_attack_dif
                    physical_dif = person.attack - mob.attack + person.armour - mob.armour
                    dif = magic_dif + physical_dif
                    person.xp += math.ceil((dif + 11) / 13 * 7 + 3)
                    up_level()
                else:
                    await message.answer(text="О нет, а он-то оказался сильнее...\n ты проиграл")

            else:
                if prob > 0.2:
                    await message.answer(text="Ухх, да ты еле ноги унес")
                else:
                    await message.answer(text="Опаньки, а убежать-то не получилось, этот гад догнал тебя и побил(")

        await state.finish()


@dp.message_handler(content_types='text', text='Отправиться в Забытый Лес')
async def forest(message: types.Message):
    await bot.send_photo(message.chat.id, photo=images['forest'],
                         caption='Упс, ты пришел слишком рано, лес еще не вырос')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
