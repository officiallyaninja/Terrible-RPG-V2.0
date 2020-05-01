from Character import *
from Move import *
import os
from time import sleep


os.system('color')

p = Player()

p.opponents.append(Gremlin())
p.opponents.append(Bat())
p.opponents.append(Bat())


def show_fight_status(player):
    player.show_healthbar()
    show_opponents(player.opponents)


while len(p.opponents) > 0:
    sleep(1)
    os.system("cls")
    show_fight_status(p)
    p.show_fight_options()
    choice = p.get_fight_option()
    p.do_fight_option(choice)

print('hurray you won')
