from Character import *
from Move import *
import os
os.system('color')


p = Player()

# p.opponents.append(Gremlin())
# p.opponents.append(Bat())
p.opponents.append(Slime())
p.opponents.append(Slime())


def check_if_all_enemies_are_alive():
    they_are_all_alive = True
    for enemy in p.opponents:
        if enemy.dead:
            they_are_all_alive = False
    return they_are_all_alive


def remove_dead_enemies():
    for i in range(len(p.opponents)):
        if p.opponents[i].dead:
            p.opponents[i].die(p.opponents)
            break
    they_are_all_alive = check_if_all_enemies_are_alive()
    if they_are_all_alive:
        return None
    else:
        remove_dead_enemies()


def show_fight_status(player):
    player.show_healthbar()
    show_opponents(player.opponents)


while len(p.opponents) > 0:
    show_fight_status(p)
    p.show_fight_options()
    choice = p.get_fight_option()
    os.system('cls')
    p.do_fight_option(choice)
    remove_dead_enemies()
    input('press enter to continue: ')
    os.system('cls')
    for enemy in p.opponents:
        # if enemy.newly_born:  # checks if the enemy was *just* created in current encounter
        #    pass
        # else:
        enemy.attack(p)
        input('press enter to continue: ')
        os.system('cls')
print('hurray you won')
