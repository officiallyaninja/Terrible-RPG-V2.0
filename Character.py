import random
from termcolor import colored
from Move import starting_moveset


class Character():
    def __init__(self):
        self.dead = False  # checks whether player or enemy is dead
        # TODO: add a way for characters to die
        self.base_color = 'white'
        self.color = 'white'
        self.isPlayer = False
        self.evasion = 0
        self.moveset = starting_moveset[self.name]

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
        len_empty_bit = (self.maxhp - self.hp) // 10

        for i in range(len_empty_bit):
            health_bar += ' '

        # also gives a precise numeric display, in case the player needs it
        health_bar += f'] {self.hp}/{self.maxhp}'
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

    # def die(self): should remove enemies from opponents, and end game for player


class Player(Character):
    def __init__(self):
        self.name = 'Player'  # maybe i will later make this a variable that the player enters
        super().__init__()
        self.maxhp = 100
        self.hp = self.maxhp  # initially hp will be max hp
        self.ATK = 3
        self.color = 'red'  # player color is red to easily differentiate from enemies
        self.isPlayer = True
        self.moves = []
        self.opponents = []

    def show_fight_options(self):
        for i in range(0, len(self.moveset)):
            move = self.moveset[i]

            # we have i+1 here, as we want indexing to start at 1
            print(colored('A' + str(i + 1), 'green'), end='', sep='')
            print(f': {move.name} - {move.flavor_text}')

    def get_fight_option(self):  # get what option the player actually wants to do
        while True:  # error handling while loop
            # choice will be of form: A1,B1,A2,B2...A12,B12...
            choice = input('choose an attack or item: ')
            if len(choice) < 2:
                print('ERROR: you did not type anything')
                continue
            type = choice[0].upper()  # A for (A)ttack, B for item from (B)ag
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
            if index >= len(self.moveset) or index < 0:
                print('ERROR: index error, choose a valid number for attack/item index')
                continue
            choice = {
                'type': type,
                'index': index
            }

            return choice

    def do_fight_option(self, choice):  # actually do the move/ use the item the player choose
        index = choice['index']

        if choice['type'] == 'A':
            move = self.moveset[index]
            move.use_move(self, self.opponents)
        elif choice['type'] == 'B':
            print('item support has not yet been built in yet')
        else:
            print('you fucked up your error handling dude')


class Enemy(Character):
    def __init__(self):
        super().__init__()
        self.maxhp = int(self.base_maxhp * (random.uniform(0.8, 1.2))
                         )  # some variance in max health
        self.hp = self.maxhp  # initially hp will be max hp
        self.ATK = self.base_attack + random.randint(-1, 1)  # slightly varies the attack power

    def die(self, oppponents_list):  # opponents list is the list of all enemies the player has to face in the current encounter
        index = oppponents_list.index(self)
        oppponents_list.pop(index)
        print(colored(f'{self.name} died', 'red'))
    # removes the enemy from the list of opponentsthe player has to face

    def attack(self, player):
        # the [0] is there because random.sample returns a list
        move = random.sample(self.moveset, 1)[0]
        move.use_move(self, player)


class Gremlin(Enemy):
    def __init__(self):
        self.name = 'Gremlin'
        self.base_maxhp = 50
        self.base_attack = 2
        self.evasion = 5
        super().__init__()


class Bat(Enemy):
    def __init__(self):
        self.name = 'Bat'
        self.base_maxhp = 35
        self.base_attack = 4
        self.evasion = 15
        super().__init__()


class Slime(Enemy):
    def __init__(self, has_split=False, maxhp=None, newly_born=False):
        self.name = 'Slime'
        self.base_maxhp = 80
        self.base_attack = 2
        self.evasion = 0
        self.has_split = has_split
        self.newly_born = newly_born
        super().__init__()
        if maxhp is None:
            pass
        else:
            self.maxhp = maxhp
            self.hp = maxhp
            self.name = 'Small slime'

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
            player.opponents.extend([child1, child2])
            self.die(player.opponents)
            print('The slime died and split into 2 smaller slimes!')
            child1.show_healthbar()
            child2.show_healthbar()
