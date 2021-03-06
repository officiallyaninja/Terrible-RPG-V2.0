from Character import *
from Move import *
import os
from Misc_functions import unfucked_input
from Consumable import *
from Weapon import *
os.system('color')

print("make sure you're running this in command line and not in python Idle")
unfucked_input('press enter to continue')
os.system('cls')


player = Player()
Character.player_character = player
player.equip(medium_mana_potion)
player.equip(big_health_potion)
player.equip(big_bomb)


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


while player.hp > 0:
    if player.next_shop == 0:
        player.encounter_shop()

    player.generate_encounter()
    # checks whether theres any battle effects to be triggered
    battle_effects = False
    for artifact in player.artifacts:
        if len(artifact.battle_effects) > 0:
            battle_effects = True
    if player.weapon is not None:
        if len(player.weapon.battle_effects) > 0:
            battle_effects = True

    if battle_effects:
        cprint("Your artifacts/weapon trigger their effects\n", attrs=['underline'])
        player.start_battle()
        unfucked_input('press enter to continue: ')
        os.system('cls')

    # fight loop
    ######################################################
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
    if player.hp > 0:
        player.end_battle()

if player.hp <= 0:
    print(colored('you died', 'red'))
    print('you killed a total of', colored(str(player.kill_count), 'red'), 'enemies')
