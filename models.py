from enum import Enum

import sqlite3


class Person:
    user_id = -1
    nickname = ''
    level = 0
    hp = 10
    curHP = 10
    money = 50
    attack = 3
    magic_attack = 0
    xp = 0
    armour = 3
    magic_armour = 0
    location_id = -1

    def get_stats(self):
        return {'Уровень': self.level, 'Здоровье': self.curHP, 'Бабки': self.money, 'Атака': self.attack,
                'Магическая атака': self.magic_attack, 'Опыт': self.xp, 'Броня': self.armour,
                'Магическая броня': self.magic_armour}


class Warrior(Person):
    hp = 11
    attack = 4
    armour = 2



class Magician(Person):
    hp = 8
    attack = 3
    magic_attack = 2
    magic_armour = 1


class Mob:
    class Type(Enum):
        Magic = 'Magic attack'
        Physical = 'Physical attack'

    mod_id = -1
    hp = 5
    reqlevel = 0
    attack_type = Type.Physical
    magic_attack = 0
    attack = 2
    armour = 0
    magic_armour = 0

    def get_stats(self):
        return {'Здоровье': self.hp, 'Атака': self.attack, 'Магическая атака': self.magic_attack, 'Броня': self.armour,
                'Магическая броня': self.magic_armour}


class PersonDB:
    def __int__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def start(self, person: Person):
        self.cursor.execute(
            "INSERT INTO 'users' (user_id, nickname, level, HP, curHP, person.money, person.attack, person.magic_attack, person.xp, person.armour, person.magic_armour, person.location_id), VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (person.user_id, person.nickname, person.level, person.level, person.hp, person.curHP, person.money,
             person.attack, person.magic_attack, person.xp, person.armour, person.magic_armour, person.location_id))
