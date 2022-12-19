import random
from enum import Enum


'''
Чисто файлик, чтобы посчитать вероятности'''

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


hero = Person()
mob = Mob()


def create_enemy():
    global hero
    global mob
    mob_type = 0
    if hero.magic_attack > 1:
        mob_type = random.randint(0, 1)
    if mob_type == 1:
        mob.attack_type = mob.Type.Magic
        mob.attack = max(hero.attack - random.randint(0, 2), 1)
        mob.magic_attack = hero.magic_attack + random.randint(0, 2)
        mob.armour = max(hero.armour - random.randint(0, 2), 0)
        mob.magic_armour = max(hero.magic_attack + random.randint(-1, 1), 0)
        mob.hp = max(hero.hp - random.randint(0, 2), 5)
    else:
        mob.attack_type = mob.Type.Physical
        mob.attack = hero.attack + random.randint(0, 2)
        mob.magic_attack = max(hero.magic_attack - random.randint(0, 2), 0)
        mob.armour = hero.armour + random.randint(0, 2)
        mob.magic_armour = max(hero.magic_armour - random.randint(0, 2), 0)
        mob.hp = hero.hp + random.randint(-1, 3)

def probability():
    global hero
    global mob
    prob = 0.5
    magic_attack_dif = hero.magic_attack - mob.magic_attack
    magic_arm_dif = hero.magic_armour - mob.magic_armour
    magic_dif = magic_arm_dif + magic_attack_dif
    physical_dif = hero.attack - mob.attack + hero.armour - mob.armour

    if mob.attack_type == mob.Type.Magic:
        prob += ((magic_dif + 2) / 4) * 0.6
        prob += ((physical_dif + 2) / 4) * 0.2
    else:
        prob += ((magic_dif + 2) / 4) * 0.2
        prob += ((physical_dif + 2) / 4) * 0.6

    prob += ((hero.hp - mob.hp + 2) / 4) * 0.2

    if prob > 0.55:
        return 1
    else:
        return -1

wins = 0
loose = 0
for i in range(10000):
    if i < 5000:
        hero = Warrior()
    else:
        hero = Magician()

    create_enemy()
    if probability() == 1:
        wins += 1
    else:
        loose +=1


print(wins, ' ', loose)
