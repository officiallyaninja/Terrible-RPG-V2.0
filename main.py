from Character import *
from Move import *
import os


os.system('color')

p = Player()

p.opponents.append(Gremlin())
p.opponents.append(Bat())
p.opponents.append(Bat())

while len(p.opponents) > 0:
    p.show_healthbar()
    show_opponents(p.opponents)
    p.show_fight_options()
    choice = p.get_fight_option()
    p.do_fight_option(choice)

print('hurray you won')
