from Effects import *
from Consumable import GetConsumables


class Artifact():
    ALL_artifacts = []

    def __init__(self, name, flavor_text, cost, equip_effects=[], battle_effects=[], turn_effects=[]):
        self.name = name
        self.flavor_text = flavor_text
        self.equip_effects = equip_effects
        self.battle_effects = battle_effects
        self.turn_effects = turn_effects
        self.cost = cost
        self.owner = None  # what character owns this artifact.

        for effect in self.equip_effects:
            effect.parent = self

        for effect in self.battle_effects:
            effect.parent = self

        for effect in self.turn_effects:
            effect.parent = self
        self.ALL_artifacts.append(self)

    def trigger_equip_effects(self):
        for effect in self.equip_effects:
            effect.trigger()

    def trigger_battle_effects(self):
        for effect in self.battle_effects:
            effect.trigger()

    def trigger_turn_effects(self):
        for effect in self.turn_effects:
            effect.trigger()


amulet_of_life = Artifact(
    name='Amulet of Life',
    flavor_text='an amulet that grants +50 Max HP',
    equip_effects=[MaxHpUp(50)],
    battle_effects=[],
    cost=400
)

amulet_of_power = Artifact(
    name='Amulet Of mana',
    flavor_text='grants the wearer a boost of magical ability, + 5 mana regen',
    equip_effects=[ManaRegenUp(5)],
    battle_effects=[],
    cost=250
)

pendant_of_magic = Artifact(
    name='pendant of magic',
    flavor_text='allows for the storage of magical energy within it. max mana +25',
    equip_effects=[MaxManaUp(25)],
    cost=200
)

intimidating_mask = Artifact(
    name='Intimidating Mask',
    flavor_text='a mask with a twisted visage, sure to strike fear into your enemies(weaken all enemies for 2 turns)',
    battle_effects=[WeakenEnemies(2)],
    cost=300
)

treasure_chest = Artifact(
    name='treasure chest',
    flavor_text='obtain 5 random consumables',
    equip_effects=[GetConsumables(5)],
    cost=150
)
