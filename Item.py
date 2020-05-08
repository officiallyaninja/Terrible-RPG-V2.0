from Effects import *


class Item():
    def __init__(self, name, flavor_text, effects):
        self.name = name
        self.flavor_text = flavor_text
        self.effects = effects
        self.owner = None
        for effect in self.effects:
            effect.parent = self

    def trigger_effects(self):
        for effect in self.effects:
            effect.trigger()


health_potion = Item(
    name='health potion',
    flavor_text='a potion that heals 30 HP',
    effects=[HealUp(30)]
)
