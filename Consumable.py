from Effects import *


class Consumable():
    ALL_consumables = []

    def __init__(self, name, flavor_text, effects, cost):
        self.name = name
        self.flavor_text = flavor_text
        self.effects = effects
        self.owner = None
        self.cost = cost
        for effect in self.effects:
            effect.parent = self
        self.ALL_consumables.append(self)

    def trigger_effects(self):
        for effect in self.effects:
            effect.trigger()


small_health_potion = Consumable(
    name='small health potion',
    flavor_text='a potion that heals 20 HP',
    effects=[HealUp(20)],
    cost=25
)

medium_health_potion = Consumable(
    name='medium health potion',
    flavor_text='a potion that heals 50 HP',
    effects=[HealUp(50)],
    cost=50
)

big_health_potion = Consumable(
    name='big health potion',
    flavor_text='a potion that heals 100 HP',
    effects=[HealUp(100)],
    cost=75
)

Consumable.ALL_consumables.extend([small_health_potion, medium_health_potion, big_health_potion])

small_mana_potion = Consumable(
    name='small mana potion',
    flavor_text='a potion that gives 30 mana',
    effects=[ManaUp(30)],
    cost=25
)

medium_mana_potion = Consumable(
    name='medium mana potion',
    flavor_text='a potion that gives 30 mana',
    effects=[ManaUp(50)],
    cost=50
)

big_mana_potion = Consumable(
    name='big mana potion',
    flavor_text='a potion that gives 100 mana',
    effects=[ManaUp(100)],
    cost=100
)

small_bomb = Consumable(
    name='small bomb',
    flavor_text='deal 25 damage to all enemies',
    effects=[DealDamage(25)],
    cost=25
)

big_bomb = Consumable(
    name='big bomb',
    flavor_text='deal 50 damage to all enemies',
    effects=[DealDamage(50)],
    cost=40
)

potion_of_weakness = Consumable(
    name='potion of weakness',
    flavor_text='inflict weakness onto all opponents for 3 turns',
    effects=[WeakenEnemies(3)],
    cost=50
)

molotov_cocktail = Consumable(
    name='Molotov cocktail',
    flavor_text='burn all opponents 3 turns',
    effects=[BurnEnemies(3)],
    cost=50
)


class GetConsumables(Effect):
    def __init__(self, number):
        self.info_text = f'you recieve {number} consumables'
        self.number = number

    def trigger(self):
        for i in range(0, self.number):
            consumable = random.choice(Consumable.ALL_consumables)
            user.equip(consumable)
