from termcolor import cprint
import random
from Consumable import *


class Effect():
    def __init__(self):
        self.info_text = ''  # explains what the effect did/does
        self.parent = None  # the move/artifact/weapon the effect is on

    def trigger(self):
        cprint(self.info_text, 'cyan')
        # this is the actual user (usually player) on whom the effect is triggered
        global user
        user = self.parent.owner

    def untrigger(self):  # when you need to undo the effects of the trigger
        pass


class MaxHpUp(Effect):
    def __init__(self, strength, permanent=False):
        self.info_text = f'+ {strength} max HP'
        self.strength = strength  # this is how much max hp is gained
        self.permanent = permanent

    def trigger(self):
        super().trigger()
        user.maxhp += self.strength
        user.hp += self.strength

    def untrigger(self):
        if not self.permanent:
            user.maxhp -= self.strength
            user.hp = min(user.hp, user.maxhp)


class MaxHpDown(Effect):
    def __init__(self, strength, permanent=False):
        self.info_text = f'- {strength} max HP'
        self.strength = strength  # this is how much max hp is lost
        self.permanent = permanent

    def trigger(self):
        super().trigger()
        user.maxhp -= self.strength
        user.hp = min(user.hp, user.maxhp)

    def untrigger(self):
        user.maxhp += self.strength


class HealUp(Effect):
    def __init__(self, strength):
        self.info_text = f'+ {strength} HP'
        self.strength = strength

    def trigger(self):
        super().trigger()
        user.hp = min(user.hp + self.strength, user.maxhp)


class FullHeal(Effect):
    def __init__(self):
        self.info_text = f'Healed up to full'

    def trigger(self):
        super().trigger()
        user.hp = user.maxhp


class Recoil(Effect):
    def __init__(self, strength):
        self.info_text = f"took {strength} recoil damage"
        self.strength = strength

    def trigger(self):
        super().trigger()
        user.hp -= self.strength


class ManaRegenUp(Effect):
    def __init__(self, strength):
        self.info_text = f"gained {strength} mana regen"
        self.strength = strength

    def trigger(self):
        super().trigger()
        user.base_mana_regen += self.strength
        user.mana_regen += self.strength


class ManaUp(Effect):
    def __init__(self, strength):
        self.info_text = f'gained {strength} Mana'
        self.strength = strength

    def trigger(self):
        super().trigger()
        user.mana = min(
            user.mana + self.strength, user.maxhp)


class MaxManaDown(Effect):
    def __init__(self, strength):
        self.info_text = f'lost {strength} Max Mana'
        self.strength = strength

    def trigger(self):
        super().trigger()
        user.max_mana = max(0, user.max_mana - self.strength)
        user.mana = min(user.mana, user.max_mana)


class MaxManaUp(Effect):
    def __init__(self, strength, permanent=False):
        self.info_text = f'gained{strength} Max Mana'
        self.strength = strength
        self.permanent = permanent

    def trigger(self):
        super().trigger()
        user.max_mana += self.strength
        user.mana += self.strength

    def untrigger(self):
        if not self.permanent:
            user.max_mana = max(0, user.max_mana - self.strength)
            user.mana = min(user.mana, user.max_mana)


class DefenseUp(Effect):
    def __init__(self, strength):
        self.info_text = f'gained {strength} defense'
        self.strength = strength

    def trigger(self):
        super().trigger()
        user.DEF += self.strength

    def untrigger(self):
        user.DEF -= self.strength


class Bonfire(Effect):
    def __init__(self):
        self.info_text = 'All attacks now have burning'

    def trigger(self):
        super().trigger()
        for move in user.moveset:
            move_has_burning = False

            for debuff in move.debuffs:
                if debuff['name'] == 'burning':
                    move_has_burning = True

            if move_has_burning:
                pass
            else:
                move.debuffs.append(
                    {'name': 'burning', 'duration': 3}
                )


class GetConsumables(Effect):
    def __init__(self, number):
        self.info_text = f'you recieve {number} consumables'
        self.number = number

    def trigger(self):
        for i in range(0, self.number):
            consumable = random.choice(Consumable.ALL_consumables)
            user.equip(consumable)


class WeakenEnemies(Effect):
    def __init__(self, duration):
        self.info_text = f'all enemies have been weakened for {duration} turns'
        self.duration = duration

    def trigger(self):
        super().trigger()
        for enemy in user.opponents:
            enemy.apply_status({'name': 'Weakness', 'duration': self.duration})


class BurnEnemies(Effect):
    def __init__(self, duration):
        self.info_text = f'all enemies have been burned for {duration} turns'
        self.duration = duration

    def trigger(self):
        super().trigger()
        for enemy in user.opponents:
            enemy.apply_status({'name': 'burning', 'duration': self.duration})


class DealDamage(Effect):
    def __init__(self, strength):
        self.info_text = f'dealt {strength} damage to all enemies'
        self.strength = strength

    def trigger(self):
        super().trigger()
        for enemy in user.opponents:
            user.deal_damage(enemy, self.strength)
