import random
from termcolor import colored, cprint
from Misc_functions import unfucked_input
from Status_conditions import *
import os
from Effects import *


def show_opponents(opponent_list):
    for i in range(0, len(opponent_list)):
        # we have a plus 1 to start indexing from 1 not 0
        print(colored(i + 1, 'green'), ': ', end='', sep='')
        opponent_list[i].show_healthbar()


class Move():
    learnable_moves = []

    def __init__(self, name, base_dmg, AoE, accuracy, buffs=[], debuffs=[], effects=[], mana_cost=0, flavor_text='', learnable=False):
        self.name = name
        self.flavor_text = flavor_text
        self.base_dmg = base_dmg
        self.AoE = AoE
        self.accuracy = accuracy
        self.mana_cost = mana_cost
        self.buffs = buffs
        self.debuffs = debuffs
        self.effects = effects
        self.learnable = learnable
        self.owner = None
        if self.learnable:
            Move.learnable_moves.append(self)

        for effect in self.effects:
            effect.parent = self

    def apply_debuffs(self, target):
        for status in self.debuffs:
            target.apply_status(status)

    def apply_buffs(self, user):
        for status in self.buffs:
            user.apply_status(status)

    # attacks automatically removed dead/killed enemies from the opponent list(opponents)
    def use_move(self, user, opponents):  # opponents is the list of enemies the enemy has to fight
        user.mana -= self.mana_cost
        if self.base_dmg > 0:

            # base damage of an attack for that character

            dmg = (((user.ATK) / 2) * (self.base_dmg))
            if user.has_status('Weakness'):
                dmg = int(dmg * 0.75)

            if user.isPlayer:  # checks if the user is the player or an enemy
                if self.AoE:  # checks if the move hits all enemies or just one Enemy
                    for enemy in opponents:
                        # hit chance cant be less that 50%
                        hit_chance = self.accuracy - enemy.evasion

                        if enemy.has_status('unhittable'):
                            hit_chance = 0

                        hit_roll = random.randint(0, 99)
                        if hit_roll > hit_chance:  # if this triggers its a miss
                            print(colored(f'{user.name} missed {enemy.name}', 'green',))
                            continue
                        dmg = dmg * random.uniform(0.9, 1.1)
                        # cprint(f'{user.name} used {self.name} on {enemy.name}', 'green')
                        user.deal_damage(enemy, dmg)
                        self.apply_debuffs(enemy)

                # TODO: add status effect check here
                else:
                    if len(opponents) > 1:
                        show_opponents(opponents)
                        while True:
                            target_index = unfucked_input('which enemy do you want to attack?: ')
                            try:
                                target_index = int(target_index)
                            except ValueError:
                                print('ERROR:input must be a number')
                                continue
                            try:
                                target = opponents[target_index - 1]
                                # we have a - 1 here, as indexing starts at 0 for the Player
                                # the player types a number from 1 to {number of enemies}, not 0 to {number of enemies - 1}
                                # but the opponents list indexing starts at 0
                            except IndexError:
                                print('ERROR: IndexError')
                                continue

                            break
                        os.system('cls')
                    else:
                        target = opponents[0]
                    #    target = opponents[int(input('which enemy do you want to attack?: '))]
                    hit_chance = max(50, self.accuracy - target.evasion)
                    hit_roll = random.randint(0, 99)

                    if target.has_status('unhittable'):
                        hit_chance = 0

                    if hit_roll > hit_chance:  # if this triggers its a miss
                        print(colored(f'{user.name} missed {target.name}', 'green'))
                        return None
                    dmg = dmg * random.uniform(0.9, 1.1)
                    # cprint(f'{user.name} used {self.name} on {target.name}', 'green')
                    user.deal_damage(target, dmg)
                    self.apply_debuffs(target)
                    # TODO: add status effect check here

                for enemy in opponents:
                    if enemy.hp <= 0:
                        enemy.dead = True
                    '''
                    if enemy.dead:
                        enemy.die(opponents)
                    '''
                show_opponents(opponents)
            # TODO: make enemies attack too u idiot
            else:  # this is for if the user of the attack is an enemy.
                player = opponents  # sets 'player' as the enemy's opponent
                hit_chance = max(50, self.accuracy - player.evasion)
                hit_roll = random.randint(0, 99)

                if player.has_status('unhittable'):
                    hit_chance = 0

                if hit_roll > hit_chance:  # this is a miss
                    print(colored(f'{user.name} missed {player.name}', 'green'))
                else:
                    # cprint(f'{user.name} used {self.name} on {player.name}', 'green')
                    user.deal_damage(player, dmg)
                    self.apply_debuffs(player)
                    player.show_healthbar()

        self.apply_buffs(user)
        for effect in self.effects:
            effect.trigger()
            # cprint(effect.info_text, 'cyan')


'''
move = Move(
    name='',
    flavor_text='',
    base_dmg=,
    AoE=,
    debuffs=[],
    accuracy=,
    mana_cost=)
'''

strike = Move(
    name='strike',
    flavor_text='a simple strike',
    base_dmg=10,
    AoE=False,
    accuracy=95)

weak_strike = Move(
    name='weak strike',
    flavor_text='a simple strike',
    base_dmg=5,
    AoE=False,
    debuffs=[],
    accuracy=100)

strong_strike = Move(
    name='strong strike',
    flavor_text='a strong strike, very prone to missing',
    base_dmg=20,
    AoE=False,
    accuracy=60)

flame_blast = Move(
    name='flame blast',
    flavor_text='cast a blast of flames to burn your opponents',
    base_dmg=10,
    AoE=True,
    debuffs=[Burning],  # should be burning here
    accuracy=50,
    mana_cost=10)

sharp_shooter = Move(
    name='Sharp shooter',
    flavor_text='A magic attack that never misses, and is quite powerful',
    base_dmg=20,
    buffs=[],
    debuffs=[],
    AoE=False,
    accuracy=200,
    effects=[],
    mana_cost=30)

hell_fire = Move(
    name='Hell fire',
    flavor_text='Rain fire from the heavens, destroying enemies and your self, deals 50 recoil damage',
    base_dmg=30,
    AoE=True,
    accuracy=100,
    effects=[Recoil(50)],
    mana_cost=40,
    debuffs=[
        {'name': 'burning', 'duration': 3}
    ])

gaias_blessing = Move(
    name="Gaia's blessing",
    flavor_text='heal 50 hp, and enemies cannot attack you for 1 turn',
    base_dmg=0,
    buffs=[
        {'name': 'unhittable', 'duration': 1}
    ],
    debuffs=[],
    AoE=False,
    accuracy=200,
    effects=[HealUp(50)],
    mana_cost=50)

starting_moveset = {
    'Player': [strike, flame_blast, hell_fire, gaias_blessing],
    'Gremlin': [weak_strike],
    'Bat': [weak_strike],
    'Slime': [weak_strike]
}
