from Move import *
from Artifact import *
from Weapon import *
from Consumable import *
from termcolor import colored, cprint


class Shop():
    def __init__(self, customer):
        # there will be 1 or 2 weapons for sale
        num_of_weapons = min(random.randint(1, 1), len(Weapon.ALL_weapons))
        self.weapons_for_sale = random.sample(Weapon.ALL_weapons, num_of_weapons)

        # there will be 2 to 4 artifacts for sale
        num_of_artifacts = min(random.randint(2, 3), len(Artifact.ALL_artifacts))
        self.artifacts_for_sale = random.sample(Artifact.ALL_artifacts, num_of_artifacts)

        # there should be 1-2 moves on sale
        num_of_moves = min(random.randint(1, 2), len(Move.learnable_moves))
        self.moves_for_sale = random.sample(Move.learnable_moves, num_of_moves)

        # should be 5-8 consumables for sale
        self.consumables_for_sale = []
        for i in range(random.randint(5, 8)):
            consumable = random.sample(Consumable.ALL_consumables, 1)[0]
            self.consumables_for_sale.append(consumable)  # this allows for repeats

        def name(x):
            return x.name
        self.consumables_for_sale = sorted(self.consumables_for_sale, key=name)

        self.customer = customer
        self.budget = self.customer.gold

        self.dict = {
            'A': self.weapons_for_sale,
            'B': self.artifacts_for_sale,
            'C': self.moves_for_sale,
            'D': self.consumables_for_sale
        }

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

        cprint('consumables:', attrs=['underline'])
        if len(self.consumables_for_sale) == 0:
            print('(out of stock)')
        for i in range(0, len(self.consumables_for_sale)):
            consumable = self.consumables_for_sale[i]
            index = colored(f'D{i+1}:', 'green')
            cost = colored(f'[{consumable.cost}]', 'yellow')
            print(f'{index}{cost}{consumable.name} - {consumable.flavor_text}')
        print('')

    def buy_things(self):
        while True:
            error_color = 'green'

            choice = unfucked_input(
                'enter index of what you want to purchase(type "leave" to leave shop): ')
            if choice.lower() == 'leave':
                return 'leave'
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
                if len(self.consumables_for_sale) == 0:
                    cprint('ERROR: There are no consumables you can buy', error_color)
                    continue
                if index < 0 or index >= len(self.consumables_for_sale):
                    cprint('ERROR: number out of range', error_color)
                    continue

            cost = self.dict[type][index].cost
            if cost > self.customer.gold:
                cprint('You dont have enough gold to buy this!', error_color)
                continue

            if type == 'A' and self.customer.weapon is not None:
                print('If you buy a new weapon you will lose your current weapon PERMANENTLY')
                print('')
                while True:
                    x = unfucked_input(
                        'press y to buy weapon, press n to cancel transaction').upper()
                    if x in ['N', 'Y']:
                        break
                    else:
                        cprint('ERROR: type y or n', error_color)
                if x == 'N':
                    continue
            item = self.dict[type].pop(index)
            self.customer.gold -= item.cost
            self.customer.equip(item)
            return None
