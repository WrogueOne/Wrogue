class Equippable:
    def __init__(self, slot, power_bonus=0, defense_bonus=0, max_hp_bonus=0,
                 accuracy_bonus=0, dodge_bonus=0, mana_bonus=0, willpower_bonus=0,
                 missile_bonus=0, regen_bonus=0, regen_rate_bonus=0):
        self.slot = slot
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
        self.max_hp_bonus = max_hp_bonus
        self.accuracy_bonus = accuracy_bonus
        self.dodge_bonus = dodge_bonus
        self.mana_bonus = mana_bonus
        self.willpower_bonus = willpower_bonus
        self.missile_bonus = missile_bonus
        self.regen_bonus = regen_bonus
        self.regen_rate_bonus = regen_rate_bonus
