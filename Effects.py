from termcolor import cprint


class Effect():
    def __init__(self):
        self.info_text = ''  # explains what the effect did/does
        self.parent = None  # the move/artifact/weapon the effect is on

    def trigger(self):
        cprint(self.info_text, 'cyan')

    def untrigger(self):  # when you need to undo the effects of the trigger
        pass


class MaxHpUp(Effect):
    def __init__(self, strength):
        self.info_text = f'+{strength} max HP'
        self.strength = strength  # this is how much max hp is gained

    def trigger(self):
        super().trigger()
        self.parent.owner.maxhp += self.strength
        self.parent.owner.hp += self.strength

    def untrigger(self):
        self.parent.owner.maxhp -= self.strength
        self.parent.owner.hp = min(self.parent.owner.hp, self.parent.owner.maxhp)


class HealUp(Effect):
    def __init__(self, strength):
        self.info_text = f'+{strength} HP'
        self.strength = strength

    def trigger(self):
        super().trigger()
        self.parent.owner.hp = min(
            self.parent.owner.hp + self.strength, self.parent.owner.maxhp)


class Recoil(Effect):
    def __init__(self, strength):
        self.info_text = f"took {strength} recoil damage"
        self.strength = strength

    def trigger(self):
        super().trigger()
        self.parent.owner.hp -= self.strength


class ManaRegenUp(Effect):
    def __init__(self, strength):
        self.info_text = f"gained {strength} mana regen"
        self.strength = strength

    def trigger(self):
        super().trigger()
        self.parent.owner.mana_regen += self.strength


class ManaUp(Effect):
    def __init__(self, strength):
        self.info_text = f'+{strength} Mana'
        self.strength = strength

    def trigger(self):
        super().trigger()
        self.parent.owner.mana = min(
            self.parent.owner.mana + self.strength, self.parent.owner.maxhp)
