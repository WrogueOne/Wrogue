from game_messages import Message

from random import randint

class Fighter:
    def __init__(self, hp, defense, power, xp=0, #min. intrinsic attributes for actors
                 regen=0, regen_rate=0, regen_timer=200, dodge=0, accuracy=0,
                 mana=0, willpower=0, #required for spellcasters once implemented
                 missile=0, max_missile_range=6, #required for archers
                 is_poisonous=False, poison=0, is_poisoned=False, poison_timer=0, poison_stack=0,#required for poisonous monsters
                 is_contagious=False, contagion=0, is_sick=False, sickness_timer=0, #required for contagious monsters
                 paralyzes=False, is_paralyzed=False, paralyze_timer=0, #required for monsters that paralyze
                 stuns=False, is_stunned=False, stun_timer=0, #required for monsters that stun
                 is_summoner = False, summon_strength= 0,
                 is_corruptor=False, corruption=0, corruption_count=0,
                 is_doomed=False,
                 is_cursed=False,
                 is_blessed=False,
                 poison_resistance=False, sickness_resistance=False, paralyze_resistance=False, stun_resistance=False,
                 is_archer=False, is_construct=False, is_darkling=False, is_demon=False, is_flying=False,
                 is_guardian=False, is_human=False, is_humanoid=False, is_lycan=False, is_natural=False,
                 is_undead=False  
##                 player_race=None, player_class=None
                 ):

        self.base_max_hp = hp
        self.hp = hp
        self.base_defense = defense
        self.base_power = power
        self.xp = xp

        self.base_regen = regen
        self.base_regen_rate = regen_rate
        self.base_regen_timer = regen_timer
        self.regen_timer = regen_timer
        
        self.base_dodge = dodge
        self.base_accuracy = accuracy
        self.base_mana = mana
        self.base_willpower = willpower

        self.base_missile = missile
        self.max_missile_range = max_missile_range

        self.is_poisonous = is_poisonous
        self.poison = poison
        self.is_poisoned = is_poisoned
        self.poison_timer = poison_timer
        self.poison_stack = poison_stack

        self.is_contagious = is_contagious
        self.contagion = contagion
        self.is_sick = is_sick
        self.sickness_timer = sickness_timer

        self.paralyzes = paralyzes
        self.is_paralyzed = is_paralyzed
        self.paralyze_timer = paralyze_timer

        self.stuns = stuns
        self.is_stunned = is_stunned
        self.stun_timer = stun_timer

        self.is_summoner = is_summoner
        self.max_summon_strength = summon_strength
        self.summon_strength = summon_strength

        self.is_corrputor = is_corruptor
        self.corruption = corruption
        self.corruption_count = corruption_count
        
        self.is_doomed = is_doomed
        self.is_cursed = is_cursed
        self.is_blessed = is_blessed
        
        self.is_flying = is_flying
        self.is_archer = is_archer
        self.is_undead = is_undead
        self.is_natural = is_natural
        self.is_lycan = is_lycan
        self.is_humanoid = is_humanoid
        self.is_darkling = is_darkling
        self.is_human = is_human
        self.is_construct = is_construct
        self.is_guardian = is_guardian

    @property
    def max_hp(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_hp_bonus
        else:
            bonus = 0
        return self.base_max_hp + bonus

    @property
    def power(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.power_bonus
        else:
            bonus = 0
        return self.base_power + bonus

    @property
    def defense(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.defense_bonus
        else:
            bonus = 0
        return self.base_defense + bonus

    @property
    def regen(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.regen_bonus
        else:
            bonus = 0
        return self.base_regen + bonus

    @property
    def regen_rate(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.regen_rate_bonus
        else:
            bonus = 0
        return self.base_regen_rate + bonus

    @property
    def dodge(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.dodge_bonus
        else:
            bonus = 0
        return self.base_dodge + bonus

    @property
    def accuracy(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.accuracy_bonus
        else:
            bonus = 0
        return self.base_accuracy + bonus

    @property
    def mana(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.mana_bonus
        else:
            bonus = 0
        return self.base_mana + bonus

    @property
    def willpower(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.willpower_bonus
        else:
            bonus = 0
        return self.base_willpower + bonus

    @property
    def missile(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.missile_bonus
        else:
            bonus = 0
        return self.base_missile + bonus

    def take_damage(self, amount):
        results = []
        if amount > 0:
            self.hp -= amount
        if self.hp <= 0:
            results.append({'dead': self.owner, 'xp': self.xp})
        return results

    def heal(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def regenerate(self):
        if self.regen >= 1:
            self.heal(self.regen)

    def attack(self, target):
        results = []
        hit_probability = 75
        damage = (randint(0, 2*self.power))
        thaco = hit_probability + self.accuracy - target.fighter.dodge
        attack_roll = randint(0, 100)
        message_color = (255, 0, 0)
        if self.owner.name == 'Player':
            message_color = (255, 127, 0)
        if attack_roll <= thaco:
            if damage - target.fighter.defense > 0:
                results.append({'message': Message('{0} attacks {1} for {2} hit points.'.format(
                    self.owner.name.capitalize(), target.name, str(damage)), message_color)})
                results.extend(target.fighter.take_damage(damage - target.fighter.defense))

                if self.is_poisonous == True and randint(0, 100) >= 50:
                    results.append({'message': Message('A searing pain announces the venom entering your system.', message_color)})
                    target.fighter.is_poisoned = True
                    target.fighter.poison_timer = 5
                    if self.poison >= target.fighter.poison_stack:
                        target.fighter.poison_stack = self.poison  
            else:
                results.append({'message': Message('{0} attacks {1} but does no damage.'.format(
                    self.owner.name.capitalize(), target.name))})
        elif self.owner.name == 'Player':
            results.append({'message': Message('Your wild swing completely misses your intended target.')})
        else:
            results.append({'message': Message('The {0} narrowly misses you.'.format(
                    self.owner.name.capitalize()))})

        return results                 

    def missile_attack(self, target):
        results = []
        hit_probability = 75
        damage = (randint(0, 2*(self.power + self.missile)))
        thaco = hit_probability + self.missile + self.accuracy - target.fighter.dodge
        attack_roll = randint(0, 100)
        
        if attack_roll <= thaco:
            if damage > 0:
                results.append({'message': Message('The missile fired by the {0} strikes you for {1} hit points.'.format(
                    self.owner.name.capitalize(), str(damage)), (255, 0, 0))})
                results.extend(target.fighter.take_damage(damage))
            else:
                results.append({'message': Message('The missile fired by the {0} bounces off your armor.'.format(
                    self.owner.name.capitalize()))})
        else:
            results.append({'message': Message('The missile fired by the {0} narrowly misses you.'.format(
                    self.owner.name.capitalize()))})
        return results
