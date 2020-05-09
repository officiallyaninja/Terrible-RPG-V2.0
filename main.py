from Character import *
from Move import *
import os
from Misc_functions import unfucked_input
from Item import *
os.system('color')


player = Player()
Character.player_character = player

player.opponents.append(Gremlin())
player.opponents.append(Bat())
player.opponents.append(Slime())
player.bag.extend([health_potion, health_potion, mana_potion])
print(player.bag)


def check_if_all_enemies_are_alive():
    they_are_all_alive = True
    for enemy in player.opponents:
        if enemy.dead:
            they_are_all_alive = False
    return they_are_all_alive


def remove_dead_enemies():
    for i in range(len(player.opponents)):
        if player.opponents[i].dead:
            player.opponents[i].die(player.opponents)
            break
    they_are_all_alive = check_if_all_enemies_are_alive()
    if they_are_all_alive:
        return None
    else:
        remove_dead_enemies()


# fight loop
######################################################
if len(player.artifacts) > 0 or player.weapon is not None:
    cprint("Your artifacts/weapon trigger their effects\n", attrs=['underline'])
    player.start_battle()
    unfucked_input('press enter to continue: ')
    os.system('cls')

while len(player.opponents) > 0 and player.hp > 0:
    # players turn
    player.show_fight_status()
    player.show_fight_options()
    choice = player.get_fight_option()
    os.system('cls')
    player.do_fight_option(choice)

    remove_dead_enemies()
    unfucked_input('press enter to continue: ')
    os.system('cls')

    # enemies' turns
    i = 0
    while i < len(player.opponents):
        enemy = player.opponents[i]
        if enemy.newly_born:  # checks if the enemy was *just* created in current encounter
            enemy.newly_born = False
        else:
            enemy.attack(player)
            unfucked_input('press enter to continue: ')
        os.system('cls')
        if not enemy.dead:
            i += 1
    Character.end_everyones_turn()

if player.hp > 0 and len(player.opponents) == 0:
    print('hurray you won')
if player.hp <= 0:
    print(colored('you died', 'red'))
