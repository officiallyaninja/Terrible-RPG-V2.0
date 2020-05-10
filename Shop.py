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
            item = random.sample(Item.ALL_items, 1)[0]
            self.items_for_sale.append(item)  # this allows for repeats

        def name(x):
            return x.name
        self.items_for_sale = sorted(self.items_for_sale, key=name)

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
            mana_cost = colored(f'[{move.mana_cost}]', 'blue')
            print(f'{index}{cost}{move.name}{mana_cost} - {move.flavor_text}')
        print('')

        cprint('Items:', attrs=['underline'])
        if len(self.items_for_sale) == 0:
            print('(out of stock)')
        for i in range(0, len(self.items_for_sale)):
            item = self.items_for_sale[i]
            index = colored(f'D{i+1}:', 'green')
            cost = colored(f'[{item.cost}]', 'yellow')
            print(f'{index}{cost}{item.name} - {item.flavor_text}')
        print('')

    def get_input(self):
        while True:
            error_color = 'green'
            choice = unfucked_input('enter index of what you want to purchase: ')
            if len(choice) < 2:
                cprint(
                    'ERROR: please enter a letter, and then a number to indicate what you want to buy', error_color)
                continue
            if len(choice) > 2:
                cprint(
                    'ERROR: please enter a letter, and then a number to indicate what you want to buy', error_color)
                continue

            type = choice[0].upper()
            if type not in ['A', 'B', 'C', 'D']:
                cprint('ERROR: first char should be A,B,C or D', error_color)
                continue
            try:
                index = int(choice[1]) - 1
            except ValueError:
                cprint('ERROR: second character should be a number', error_color)
                continue

            if type == 'A':
                if len(self.weapons_for_sale) == 0:
                    cprint('ERROR: There are no weapons you can buy', error_color)
                    continue
                if index < 0 or index >= len(self.weapons_for_sale):
                    cprint('ERROR: number out of range', error_color)
                    continue

            if type == 'B':
                if len(self.artifacts_for_sale) == 0:
                    cprint('ERROR: There are no artifacts you can buy', error_color)
                    continue
                if index < 0 or index >= len(self.artifacts_for_sale):
                    cprint('ERROR: number out of range', error_color)
                    continue

            if type == 'C':
                if len(self.moves_for_sale) == 0:
                    cprint('ERROR: There are no moves you can buy', error_color)
                    continue
                if index < 0 or index >= len(self.moves_for_sale):
                    cprint('ERROR: number out of range', error_color)
                    continue

            if type == 'D':
                if len(self.items_for_sale) == 0:
                    cprint('ERROR: There are no items you can buy', error_color)
                    continue
                if index < 0 or index >= len(self.items_for_sale):
                    cprint('ERROR: number out of range', error_color)
                    continue
            choice_dict = {
                'type': type,
                'index': index
            }
            return choice_dict


x = Shop()
x.items_for_sale = []
x.show_wares()
x.get_input()
