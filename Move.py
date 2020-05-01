import random
from termcolor import colored


def show_opponents(opponent_list):
    for i in range(0, len(opponent_list)):
        if i == 0:
            print(colored(i, 'green').rjust(20), ': ', end='', sep='')
            opponent_list[i].show_healthbar(x=1)
        else:
            print(colored(i, 'green').rjust(40), ': ', end='', sep='')
            opponent_list[i].show_healthbar()


class Move():
    def __init__(self, name, flavor_text, base_dmg, AoE, status_effect, accuracy):
        self.name = name
        self.flavor_text = flavor_text
        self.base_dmg = base_dmg
        self.AoE = AoE
        self.status_effect = status_effect
        self.accuracy = accuracy

    # attacks automatically removed dead/killed enemies from the opponent list(opponents)
    def use_move(self, user, opponents):  # opponents is the list of enemies the enemy has to fight
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

                while True:
                    target_index = input('which enemy do you want to attack?: ')
                    try:
                        target_index = int(target_index)
                    except ValueError:
                        print('ERROR:input must be a number')
                        continue
                    try:
                        target = opponents[target_index]
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

        # TODO: make enemies attack too u idiot


ALL_moves = []

strike = Move(
    name='strike',
    flavor_text='a simple strike',
    base_dmg=10,
    AoE=False,
    status_effect=None,
    accuracy=95)

flame_blast = Move(
    name='flame blast',
    flavor_text='cast a blast of flames to burn your opponents',
    base_dmg=5,
    AoE=True,
    status_effect=None,  # should be burning here
    accuracy=95)

starting_moveset = {
    'Player': [strike, flame_blast, strike],
    'Gremlin': [],
    'Bat': []
}
