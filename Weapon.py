from Artifact import *
from Move import *


class Weapon(Artifact):
    ALL_weapons = []

    def __init__(self, name, flavor_text, cost, damage_multiplier=1, moveset=[], equip_effects=[], battle_effects=[], turn_effects=[]):
        self.name = name
        self.flavor_text = flavor_text
        self.cost = cost

        self.damage_multiplier = damage_multiplier
        self.moveset = moveset

        self.equip_effects = equip_effects
        self.battle_effects = battle_effects
        self.turn_effects = turn_effects
        self.owner = None  # what character owns this Weapon.

        for effect in self.equip_effects:
            effect.parent = self

        for effect in self.battle_effects:
            effect.parent = self

        for effect in self.turn_effects:
            effect.parent = self
        self.ALL_weapons.append(self)


flaming_sword = Weapon(
    name='Flaming Sword',
    flavor_text='a sword that makes all your attacks burn your opponents',
    damage_multiplier=1.25,
    moveset=[],
    battle_effects=[Bonfire()],
    cost=500
)

reapers_scythe = Weapon(
    name='The Reapers Scythe',
    flavor_text='PERMANENTLY lose 40 Max HP on pickup, but gain awesome power',
    damage_multiplier=2,
    moveset=[corrupted_healing, murder],
    equip_effects=[MaxHpDown(40)],
    cost=1000

)

shield = Weapon(
    name='the shield',
    flavor_text='The best offense is a good defense',
    damage_multiplier=1.1,
    moveset=[shield_bash],
    equip_effects=[DefenseUp(40)],
    cost=750
)
