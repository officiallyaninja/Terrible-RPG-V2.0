import random
from termcolor import colored


def show_opponents(opponent_list):
    for i in range(0, len(opponent_list)):
        # we have a plus 1 to start indexing from 1 not 0
        print(colored(i + 1, 'green'), ': ', end='', sep='')
        opponent_list[i].show_healthbar()


class Move():
    def __init__(self, name, base_dmg, AoE, status_effect, accuracy, flavor_text=''):
        self.name = name
        self.flavor_text = flavor_text
        self.base_dmg = base_dmg
        self.AoE = AoE
        self.status_effect = status_effect
        self.accuracy = accuracy

    # attacks automatically removed dead/killed enemies from the opponent list(opponents)
    def use_move(self, user, opponents):  # opponents is the list of enemies the enemy has to fight
        if self.base_dmg > 0:  # checks to see if its an attacking or no attacking move
            # base damage of an attack for that character
            dmg = (((user.ATK) / 2) * (self.base_dmg))

            if user.isPlayer:  # checks if the user is the player or an enemy
                if self.AoE:  # checks if the move hits all enemies or just one Enemy
                    for enemy in opponents:
                        # hit chance cant be less that 50%
                        hit_chance = max(50, self.accuracy - enemy.evasion)
                        hit_roll = random.randint(0, 99)
                        if hit_roll > hit_chance:  # if this triggers its a miss
                            print(colored(f'{user.name} missed {enemy.name}', 'green',))
                            continue
                        dmg = dmg * random.uniform(0.9, 1.1)
                        user.deal_damage(enemy, dmg)

                # TODO: add status effect check here
                else:
                    show_opponents(opponents)

                    while True:
                        target_index = input('which enemy do you want to attack?: ')
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

                    #    target = opponents[int(input('which enemy do you want to attack?: '))]
                    hit_chance = max(50, self.accuracy - target.evasion)
                    hit_roll = random.randint(0, 99)
                    if hit_roll > hit_chance:  # if this triggers its a miss
                        print(colored(f'{user.name} missed {target.name}', 'green'))
                        return None
                    dmg = dmg * random.uniform(0.9, 1.1)
                    user.deal_damage(target, dmg)
                    # TODO: add status effect check here

                for enemy in opponents:
                    if enemy.hp <= 0:
                        enemy.dead = True
                    if enemy.dead:
                        enemy.die(opponents)

                show_opponents(opponents)
            # TODO: make enemies attack too u idiot
            else:  # this is for if the user of the attack is an enemy.
                player = opponents  # sets 'player' as the enemy's opponent
                hit_chance = max(50, self.accuracy - player.evasion)
                hit_roll = random.randint(0, 99)
                if hit_roll > hit_chance:  # this is a miss
                    print(colored(f'{user.name} missed {player.name}', 'green'))
                else:
                    user.deal_damage(player, dmg)
                    player.show_healthbar()


ALL_moves = []

strike = Move(
    name='strike',
    flavor_text='a simple strike',
    base_dmg=10,
    AoE=False,
    status_effect=None,
    accuracy=95)

weak_strike = Move(
    name='weak strike',
    flavor_text='a simple strike',
    base_dmg=5,
    AoE=False,
    status_effect=None,
    accuracy=100)

strong_strike = Move(
    name='strong strike',
    flavor_text='a strong strike, very prone to missing',
    base_dmg=20,
    AoE=False,
    status_effect=None,
    accuracy=60)

flame_blast = Move(
    name='flame blast',
    flavor_text='cast a blast of flames to burn your opponents',
    base_dmg=10,
    AoE=True,
    status_effect=None,  # should be burning here
    accuracy=75)

starting_moveset = {
    'Player': [strike, strong_strike, flame_blast],
    'Gremlin': [weak_strike],
    'Bat': [weak_strike],
    'Slime': [weak_strike]
}
