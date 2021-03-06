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

    def __init__(self, name, base_dmg, cost=1000, AoE=False, accuracy=100, buffs=[], debuffs=[], effects=[], mana_cost=0, flavor_text='', learnable=False):
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
        self.cost = cost
        if self.learnable:
            Move.learnable_moves.append(self)

        for effect in self.effects:
            effect.parent = self

    def copy(self):
        copy = Move(
            name=self.name,
            flavor_text=self.flavor_text,
            base_dmg=self.base_dmg,
            Aoe=self.Aoe,
            accuracy=self.accuracy,
            buffs=self.buffs,
            debuffs=self.debuffs,
            effects=self.effects,
            mana_cost=self.mana_cost,
            learnable=False
        )
        return copy

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

            if user.weapon is not None:
                dmg_multiplier = user.weapon.damage_multiplier
            else:
                dmg_multiplier = 1

            dmg = int(((user.ATK) / 10) * (self.base_dmg) * (dmg_multiplier))
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
                    dmg *= 1 - (min(player.DEF, 90) / 100)
                    user.deal_damage(player, dmg)
                    self.apply_debuffs(player)
                    player.show_healthbar()

        self.apply_buffs(user)
        for effect in self.effects:
            effect.parent = self
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
    base_dmg=15,
    AoE=False,
    accuracy=100)

strong_strike = Move(
    name='strong strike',
    flavor_text='a strong strike',
    base_dmg=25,
    AoE=False,
    accuracy=100,
    mana_cost=10)

flame_blast = Move(
    name='flame blast',
    flavor_text='cast a blast of flames to burn your opponents',
    base_dmg=10,
    AoE=True,
    debuffs=[Burning],  # should be burning here
    accuracy=90,
    mana_cost=15)

earthquake = Move(
    name='earthquake',
    flavor_text='summon an earthquake that hits all enemies',
    base_dmg=35,
    AoE=True,
    accuracy=80,
    mana_cost=40
)

# weapon moves
#####################
# the reapers_scythe

corrupted_healing = Move(
    name='Corrupted healing',
    flavor_text='lose 10 MAX HP, but fully heal HP. all enemies will miss for one turn',
    base_dmg=0,
    buffs=[{'name': 'unhittable', 'duration': 1}],
    mana_cost=10,
    effects=[MaxHpDown(10), FullHeal()],
)

murder = Move(
    name='Murder',
    flavor_text='lose 10 MAX Mana, kill 1 enemy',
    accuracy=1000,
    AoE=False,
    base_dmg=9999,
    buffs=[],
    mana_cost=10,
    effects=[MaxManaDown(10)],
)

# the shield
shield_bash = Move(
    name='shield bash',
    flavor_text='deal a decent bit of damage and weaken target enemy',
    AoE=False,
    base_dmg=20,
    buffs=[],
    debuffs=[Weakness],
    mana_cost=0,
    effects=[]
)

# LEARNABLE MOVES
#######################################
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
    mana_cost=50,
    learnable=True,
    cost=250)

sharp_shooter = Move(
    name='Sharp shooter',
    flavor_text='A strong magic attack that never misses, and is quite powerful',
    base_dmg=30,
    buffs=[],
    debuffs=[],
    AoE=False,
    accuracy=200,
    effects=[],
    mana_cost=30,
    learnable=True,
    cost=50)

hell_fire = Move(
    name='Hell fire',
    flavor_text='Rain fire from the heavens, destroying enemies and your self, deals 50 recoil damage',
    base_dmg=30,
    AoE=True,
    accuracy=100,
    effects=[Recoil(50)],
    mana_cost=40,
    debuffs=[{'name': 'burning', 'duration': 3}],
    learnable=True,
    cost=250)

# ENEMY MOVES
###########################

weak_strike = Move(
    name='weak strike',
    flavor_text='a weak strike',
    base_dmg=5,
    AoE=False,
    debuffs=[],
    accuracy=90)

starting_moveset = {
    'Player': [strike, strong_strike, flame_blast, earthquake],
    'Gremlin': [weak_strike],
    'Bat': [weak_strike],
    'Slime': [weak_strike]
}
