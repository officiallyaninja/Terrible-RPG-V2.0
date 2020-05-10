from Move import *
from Artifact import *
from Weapon import *
from Item import *
from termcolor import colored, cprint


class Shop():
    def __init__(self):
        # there will be 1 or 2 weapons for sale
        self.weapons_for_sale = random.sample(Weapon.ALL_weapons, random.randint(1, 2))
        # there will be 2 to 4 artifacts for sale
        self.artifacts_for_sale = random.sample(Artifact.ALL_artifacts, random.randint(2, 2))
        # there should be 1-3 moves on sale
        self.moves_for_sale = random.sample(Move.learnable_moves, random.randint(1, 2))
        # should be 5-8 items for sale
        self.items_for_sale = []
        for i in range(random.randint(5, 8)):
            self.items_for_sale.append(random.sample(Item.ALL_items, 1)
                                       [0])  # this allows for repeats

    def show_wares(self):
        cprint('Weapons:', attrs=['underline'])
        if len(self.weapons_for_sale) == 0:
            print('(out of stock)')
        for i in range(0, len(self.weapons_for_sale)):
            weapon = self.weapons_for_sale[i]
            index = colored(f'A{i+1}:', 'green')
            cost = colored(f'[{weapon.cost}]', 'yellow')
            print(f'{index}{cost}{weapon.name} - {weapon.flavor_text}')
        print('')

        cprint('Artifacts:', attrs=['underline'])
        if len(self.artifacts_for_sale) == 0:
            print('(out of stock)')
        for i in range(0, len(self.artifacts_for_sale)):
            artifact = self.artifacts_for_sale[i]
            index = colored(f'B{i+1}:', 'green')
            cost = colored(f'[{artifact.cost}]', 'yellow')
            print(f'{index}{cost}{artifact.name} - {artifact.flavor_text}')
        print('')

        cprint('Moves', attrs=['underline'])
        if len(self.moves_for_sale) == 0:
            print('(out of stock)')
        for i in range(0, len(self.moves_for_sale)):
            move = self.moves_for_sale[i]
            index = colored(f'C{i+1}:', 'green')
            cost = colored(f'[{move.cost}]', 'yellow')
            mana_cost = colored(f'[{move.mana_cost}]')
            print(f'{index}{cost}{move.name}{mana_cost} - {move.flavor_text}')


Shop().show_wares()
