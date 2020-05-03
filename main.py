from Character import *
from Move import *
import os
from Misc_functions import unfucked_input
os.system('color')


p = Player()

p.opponents.append(Gremlin())
p.opponents.append(Bat())
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
    player.show_manabar()
    show_opponents(player.opponents)


while len(p.opponents) > 0 and p.hp > 0:
    # players turn
    show_fight_status(p)
    p.show_fight_options()
    choice = p.get_fight_option()
    os.system('cls')
    p.do_fight_option(choice)
    p.end_turn()

    remove_dead_enemies()
    unfucked_input('press enter to continue: ')
    os.system('cls')

    # enemies' turns
    i = 0
    while i < len(p.opponents):
        enemy = p.opponents[i]
        if enemy.newly_born:  # checks if the enemy was *just* created in current encounter
            enemy.newly_born = False
        else:
            enemy.attack(p)
            if enemy in Character.opponents:
                enemy.end_turn()
            unfucked_input('press enter to continue: ')
        os.system('cls')
        if not enemy.dead:
            i += 1

if p.hp > 0 and len(p.opponents) == 0:
    print('hurray you won')
if p.hp <= 0:
    print(colored('you died', 'red'))
