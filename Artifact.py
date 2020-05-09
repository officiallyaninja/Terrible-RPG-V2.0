from Effects import *


class Artifact():
    def __init__(self, name, flavor_text, equip_effects=[], battle_effects=[], turn_effects=[]):
        self.name = name
        self.flavor_text = "lorem ipsum"
        self.equip_effects = equip_effects
        self.battle_effects = battle_effects
        self.turn_effects = turn_effects
        self.owner = None  # what character owns this artifact.

        for effect in self.equip_effects:
            effect.parent = self

        for effect in self.battle_effects:
            effect.parent = self

    def trigger_equip_effects(self):
        for effect in self.equip_effects:
            effect.trigger()

    def trigger_battle_effects(self):
        for effect in self.battle_effects:
            effect.trigger()

    def trigger_turn_effects(self):
        for effect in self.turn_effects:
            effect.trigger()


AmuletOfLife = Artifact(
    name='Amulet of Life',
    flavor_text='an amulet that grants +50 Max HP',
    equip_effects=[MaxHpUp(50)],
    battle_effects=[]
)

AmuletOfMana = Artifact(
    name='Amulet Of mana',
    flavor_text='grant + 5 mana regen',
    equip_effects=[],
    battle_effects=[ManaRegenUp(5)]
)
