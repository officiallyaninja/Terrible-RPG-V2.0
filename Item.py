from Effects import *


class Item():
    ALL_items = []

    def __init__(self, name, flavor_text, effects, cost):
        self.name = name
        self.flavor_text = flavor_text
        self.effects = effects
        self.owner = None
        self.cost = cost
        for effect in self.effects:
            effect.parent = self
        self.ALL_items.append(self)

    def trigger_effects(self):
        for effect in self.effects:
            effect.trigger()


health_potion = Item(
    name='health potion',
    flavor_text='a potion that heals 30 HP',
    effects=[HealUp(30)],
    cost=250
)

mana_potion = Item(
    name='mana potion',
    flavor_text='a potion that gives 30 mana',
    effects=[ManaUp(30)],
    cost=350
)
