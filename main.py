from Character import *
from Move import *
import os


os.system('color')

p = Player()

p.opponents.append(Gremlin())
p.opponents.append(Bat())
p.opponents.append(Bat())


def show_fight_status(player):
    player.show_healthbar()
    show_opponents(player.opponents)


while len(p.opponents) > 0:
    show_fight_status(p)
    p.show_fight_options()
    choice = p.get_fight_option()
    os.system('cls')
    p.do_fight_option(choice)
    input('press enter to continue: ')
    os.system('cls')
    for enemy in p.opponents:
        enemy.attack(p)
        input('press enter to continue: ')
        os.system('cls')
print('hurray you won')
