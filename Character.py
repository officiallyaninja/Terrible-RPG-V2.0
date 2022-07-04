import random
from termcolor import colored, cprint
from Move import starting_moveset
from Misc_functions import unfucked_input
from Status_conditions import *
from Artifact import *
from Weapon import *
from Shop import *
import os


class Character():
    opponents = []  # list of all the enemies the player has to fight in current encounter
    gold_from_battle = 0
    player_character = None  # this should contain the player object

    @staticmethod
    def show_opponents():
        for i in range(0, len(Character.opponents)):
            # we have a plus 1 to start indexing from 1 not 0
            print(colored(i + 1, 'green'), ': ', end='', sep='')
            Character.opponents[i].show_healthbar()

    @classmethod
    def end_everyones_turn(self):
        line = "_" * 30

        print('END TURN EFFECTS')
        print('================')
        print(line)
        cprint('Player:', 'green')
        player = self.player_character
        player.end_turn()

        for enemy in player.opponents:
            print(line)
            cprint(f'{enemy.name}:', 'green')
            enemy.end_turn()
        print(line)
        unfucked_input('press enter to continue: ')
        os.system('cls')

    @classmethod
    def spawn_enemy(self, list_of_enemies):
        r = random.randint(0, len(list_of_enemies) - 1)
        Character.opponents.append(list_of_enemies[r]())

    @classmethod
    def generate_encounter(self):
        spawnable_enemies = [Gremlin, Bat, Slime]  # all enemies the player could fight
        num_of_enemies = random.randint(2, 4)
        for i in range(0, num_of_enemies):
            Character.spawn_enemy(spawnable_enemies)

    def __init__(self):
        self.dead = False  # checks whether player or enemy is dead
        # TODO: add a way for characters to die
        self.base_color = 'white'
        self.color = 'white'
        self.isPlayer = False
        self.evasion = 0
        self.base_moveset = []
        for move in starting_moveset[self.name]:
            self.base_moveset.append(move)

        for move in self.base_moveset:
            move.owner = self
        # self.inactive = False  # if an enemy is inactive, then its removed from combat without dying
        self.mana = 0
        self.max_mana = 100
        self.mana_regen = 0
        self.status_conditions = []
        self.artifacts = []
        self.weapon = None
        self.bag = []
        self.gold = 0
        self.base_DEF = 1
        self.DEF = self.base_DEF

    def has_status(self, status_name):
        for status_condition in self.status_conditions:
            if status_condition['name'].lower() == status_name.lower():
                return True
        return False

    def get_status_index(self, status):
        for i in range(0, len(self.status_conditions)):
            status_condition = self.status_conditions[i]
            if status['name'] == status_condition['name']:
                return i
        return None

    def apply_status(self, status):
        index = self.get_status_index(status)
        if index is not None:
            self.status_conditions[index]['duration'] += status['duration']
        else:
            self.status_conditions.append(status.copy())
        name = status['name']
        cprint(f'{self.name} now has the status effect "{name}"', 'cyan')

    def get_health_percent(self):  # gives percent of health remaining as a float b/w 0 and 1
        return self.hp / self.maxhp

    def show_healthbar(self):  # prints a healthbar
        health_bar = "["
        if self.hp != 0:
            # every 10 hit points corresponds to 1 'block' of health
            len_filled_in_bit = (self.hp // 10) + 1
        else:
            len_filled_in_bit = 0

        for i in range(len_filled_in_bit):
            health_bar += '■'

        # calculates how much health has been lost and hence the empty space in the bar
        # len_empty_bit = (self.maxhp - self.hp) // 10

        # for i in range(len_empty_bit):
        while len(health_bar) < (self.maxhp // 10) + 2:
            health_bar += ' '

        # also gives a precise numeric display, in case the player needs it
        display_hp = max(0, self.hp)  # this is so health is never shown to be -ve
        health_bar += f'] {display_hp}/{self.maxhp}'
        # health is set to be red in colour for the player, and white for enemies
        # this is to make it easy to distinguish and see
        print(self.name)
        print(colored(health_bar, self.color))

    def deal_damage(self, other, dmg):  # code to make moves easily deal damage enemies and check if dead
        damage = int(dmg)
        other.hp -= damage
        print(colored(f'{self.name} dealt {damage} damage to {other.name}',
                      'green'), (colored('', 'white', 'on_grey')))
        if other.hp <= 0:
            other.dead = True

    def end_turn(self):
        printed_something = False  # checks whether anything has been printed in this function
        self.mana = min(self.max_mana, self.mana + self.mana_regen)
        if self.isPlayer:
            cprint(f'Player gained {self.mana_regen} mana', 'blue')
            printed_something = True

        if self.has_status('burning') and self.hp > 0:
            cprint(f'{self.name} takes 10 burning damage', 'red')
            printed_something = True
            self.hp -= 10

        for i in range(0, len(self.status_conditions)):
            status = self.status_conditions[i]
            if status['duration'] != 'inf':
                status['duration'] -= 1
            duration = status['duration']
            name = status['name']
            print(f'{duration} turns of{name} left')
            if status['duration'] <= 0:
                name = status['name']
                cprint(f'{self.name} no longer has status effect "{name}"', 'cyan')
                printed_something = True
                self.status_conditions[i] = None

        i = 0
        while None in self.status_conditions:
            if self.status_conditions[i] is None:
                self.status_conditions.pop(i)
            else:
                i += 1

        for artifact in self.artifacts:
            artifact.trigger_turn_effects()

        if self.dead or self.hp <= 0:
            self.die(Character.opponents)
            printed_something = True
        if printed_something is False:
            cprint('(None)', 'yellow')

    def unequip_weapon(self):
        if self.weapon is None:
            pass
        else:
            for effect in self.weapon.equip_effects:
                effect.untrigger()
            self.moveset = self.base_moveset
            self.weapon = None

    def equip_weapon(self, weapon):
        weapon.owner = self
        self.weapon = weapon
        self.moveset.extend(weapon.moveset)
        for move in self.moveset:
            move.owner = self
        weapon.trigger_equip_effects()

    def equip_artifact(self, artifact):
        artifact.owner = self
        self.artifacts.append(artifact)
        artifact.trigger_equip_effects()

    def equip_consumable(self, consumable):
        consumable.owner = self
        self.bag.append(consumable)

    def use_consumable(self, consumable):
        consumable.owner = self
        consumable.trigger_effects()

    def learn_move(self, move):
        self.base_moveset.append(move)
        self.moveset.append(move)

    def equip(self, thing_to_equip):
        thing_to_equip.owner = self
        if isinstance(thing_to_equip, Weapon):
            self.unequip_weapon()
            self.equip_weapon(thing_to_equip)

        elif isinstance(thing_to_equip, Artifact):
            self.equip_artifact(thing_to_equip)

        elif isinstance(thing_to_equip, Consumable):
            self.equip_consumable(thing_to_equip)

        elif isinstance(thing_to_equip, Move):
            self.learn_move(thing_to_equip)
        else:
            print('you done fucked up, you tried to equip something that isnt a weapon artifact or consumable')


class Player(Character):
    def __init__(self):
        self.name = 'Player'  # maybe i will later make this a variable that the player enters
        super().__init__()

        self.maxhp = 100
        self.hp = self.maxhp  # initially hp will be max hp

        self.max_mana = 100
        self.mana = 100

        self.base_mana_regen = 5
        self.mana_regen = self.base_mana_regen

        self.base_ATK = 15
        self.ATK = self.base_ATK

        self.base_evasion = 15
        self.evasion = self.base_evasion

        self.weapon = None
        self.artifacts = []
        self.gold = 150

        self.color = 'red'  # player color is red to easily differentiate from enemies
        self.isPlayer = True
        self.moveset = self.base_moveset.copy()
        self.kill_count = 0
        self.next_shop = 3

    def die(self, dummy_var):  # dummy var is needed because enemies death function needs 2 args
        pass

    def show_manabar(self):
        mana_bar = "["
        if self.mana != 0:
            # every 10 mana points corresponds to 1 'block' of mana
            len_filled_in_bit = (self.mana // 10) + 1
        else:
            len_filled_in_bit = 0

        for i in range(len_filled_in_bit):
            mana_bar += '■'

        # calculates how much mana has been lost and hence the empty space in the bar
        # len_empty_bit = (self.max_mana - self.mana) // 10

        # for i in range(len_empty_bit):
        while len(mana_bar) < (self.max_mana // 10) + 2:
            mana_bar += ' '

        # also gives a precise numeric display, in case the player needs it
        mana_bar += f'] {self.mana}/{self.max_mana}'
        # health is set to be red in colour for the player, and white for enemies
        # this is to make it easy to distinguish and see
        print(colored(mana_bar, 'blue'))

    def show_fight_status(self):
        self.show_healthbar()
        self.show_manabar()
        self.show_opponents()

    def show_fight_options(self):
        for i in range(0, len(self.moveset)):
            move = self.moveset[i]
            if move.mana_cost <= self.mana:
                # we have i+1 here, as we want indexing to start at 1
                print(colored('A' + str(i + 1) + ':', 'green'), end='', sep='')
                print(colored(f'[{move.mana_cost}]', 'blue'), end='', sep='')
                print(f'{move.name} - {move.flavor_text}')
            else:
                print(colored('A' + str(i + 1) + ':', 'red'), end='', sep='')
                print(colored(f'[{move.mana_cost}]', 'red'), end='', sep='')
                print(colored(f'{move.name} - {move.flavor_text}', 'red'))
        print('')

        for i in range(0, len(self.bag)):
            consumable = self.bag[i]
            print(colored('B' + str(i + 1) + ':', 'green'), end='', sep='')
            print(f'{consumable.name} - {consumable.flavor_text}')
        print('')

    def get_fight_option(self):  # get what option the player actually wants to do
        while True:  # error handling while loop
            # choice will be of form: A1,B1,A2,B2...A12,B12...
            choice = unfucked_input('choose an attack or consumable: ')

            if choice.lower() == 'pass':
                return 'pass'
            if len(choice) < 2:
                print(
                    'ERROR: please type a letter, A for attack or B for consumable, and then the index of the attack/consumable')
                continue
            type = choice[0].upper()  # A for (A)ttack, B for consumable from (B)ag
            index = choice[1:]
            if type not in ['A', 'B']:
                print('ERROR: first character should be A or B')
                continue

            try:
                index = int(index) - 1
                # we have a -1 here, as the player input will be one more than the index, as list indexing starts at 0
            except ValueError:
                print('ERROR: you should have a number after the first character')
                continue

            if type.upper() == 'B':  # if the option choses is an consumable
                if index >= len(self.bag) or index < 0:
                    # because we subtracted 1 from the player submitted index, we check index < 0 and not index < 1
                    print('ERROR: index error, choose a valid number for consumable index')
                    continue
                else:
                    consumable = self.bag.pop(index)
                    self.use_consumable(consumable)
                    os.system('cls')
                    self.show_fight_status()
                    self.show_fight_options()
                    continue

            if index >= len(self.moveset) or index < 0:
                # because we subtracted 1 from the player submitted index, we check index < 0 and not index < 1
                print('ERROR: index error, choose a valid number for attack index')
                continue
            if self.moveset[index].mana_cost > self.mana:
                print('you dont have enough mana for that')
                continue

            choice = {
                'type': type,
                'index': index
            }

            return choice

    def do_fight_option(self, choice):  # actually do the move/ use the consumable the player choose
        if choice == 'pass':
            cprint('you decide to do nothing, and bide your time', 'green')
            return None

        index = choice['index']

        if choice['type'] == 'A':
            move = self.moveset[index]
            move.use_move(self, self.opponents)
        elif choice['type'] == 'B':
            print('ERROR: YOU DIDNT LOOP AFTER ACTIVATING THE Consumable')
        else:
            print('you fucked up your error handling dude')

    def encounter_shop(self):

        shop = Shop(customer=self)
        player_action = ''
        while player_action != 'leave':
            self.show_healthbar()
            self.show_manabar()
            print('gold:', colored(str(self.gold), 'yellow'))
            print('')
            print('SHOP:')
            shop.show_wares()
            player_action = shop.buy_things()
            os.system('cls')
        self.next_shop = random.randint(5, 7)

    def start_battle(self):
        def mana_cost(x):
            return x.mana_cost
        self.moveset = sorted(self.moveset, key=mana_cost)

        for artifact in self.artifacts:
            artifact.trigger_battle_effects()
        if self.weapon is not None:
            self.weapon.trigger_battle_effects()  # write code for this in Artifacts

    def end_battle(self):
        self.status_conditions.clear()
        self.ATK = self.base_ATK
        self.mana_regen = self.base_mana_regen
        self.evasion = self.base_evasion
        self.DEF = self.base_DEF

        self.gold += Character.gold_from_battle

        print('you gained', colored(f'{self.gold_from_battle} gold',
                                    'yellow'), 'from that encounter')

        Character.gold_from_battle = 0
        self.next_shop -= 1

        print('you now have', colored(f'{self.gold} gold', 'yellow'))

        drop = random.choice(Consumable.ALL_consumables)
        self.equip(drop)
        cprint(f'you found a {drop.name}', 'green')

        unfucked_input('press ented to continue: ')
        os.system('cls')


class Enemy(Character):
    def __init__(self):
        super().__init__()
        kill_count = Character.player_character.kill_count
        self.maxhp = int(self.base_maxhp * (random.uniform(0.8, 1.2) * (1 + (kill_count / 50)))
                         )  # some variance in max health
        self.hp = self.maxhp  # initially hp will be max hp
        self.ATK = self.base_attack + random.randint(-3, 3)  # slightly varies the attack power
        self.gold = int(self.base_gold * random.uniform(0.8, 1.25))
        self.moveset = self.base_moveset
        self.newly_born = False

    # opponents list is the list of all enemies the player has to face in the current encounter
    def die(self, oppponents_list=Character.opponents):
        self.dead = True
        index = oppponents_list.index(self)
        oppponents_list.pop(index)
        print(colored(f'{self.name} died', 'red'))
        Character.gold_from_battle += self.gold
        Character.player_character.kill_count += 1
    # removes the enemy from the list of opponents the player has to face

    def attack(self, player):
        # the [0] is there because random.sample returns a list
        move = random.sample(self.moveset, 1)[0]
        move.use_move(self, player)


class Gremlin(Enemy):
    def __init__(self):
        self.name = 'Gremlin'
        self.base_maxhp = 50
        self.base_attack = 15
        self.evasion = 0
        self.base_gold = 40
        super().__init__()


class Bat(Enemy):
    def __init__(self):
        self.name = 'Bat'
        self.base_maxhp = 35
        self.base_attack = 20
        self.evasion = 5
        self.base_gold = 20
        super().__init__()


class Slime(Enemy):
    def __init__(self, has_split=False, maxhp=None, newly_born=False):
        self.name = 'Slime'
        self.base_maxhp = 80
        self.base_attack = 10
        self.evasion = 0
        self.has_split = has_split
        self.base_gold = 35
        super().__init__()
        if maxhp is None:
            pass
        else:
            self.maxhp = maxhp
            self.hp = maxhp
            self.name = 'Small slime'
            self.newly_born = newly_born

    def attack(self, player):
        if self.newly_born:
            self.newly_born = False
            print('the newly born slime wriggles around')
            print("it appears as if it's too small to split again.")

        elif self.hp > (self.maxhp / 2) or self.has_split:
            super().attack(player)
        else:
            child1 = Slime(has_split=True, maxhp=self.hp, newly_born=True)
            child2 = Slime(has_split=True, maxhp=self.hp, newly_born=True)
            child1.gold = 0
            child2.gold = 0
            child1.ATK /= 2
            child2.ATK /= 2
            player.opponents.extend([child1, child2])
            self.die(player.opponents)
            print('The slime died and split into 2 smaller slimes!')
            child1.show_healthbar()
            child2.show_healthbar()
