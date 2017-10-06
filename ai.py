from random import randint, shuffle

from game_messages import Message

class BasicMonster:
    def take_turn(self, target, game_map, entities):
        results = []
        monster = self.owner

        if game_map.fov[monster.x, monster.y]:
            if monster.distance_to(target) >= 2:
                monster.move_towards(target.x, target.y, game_map, entities)
            elif target.fighter.hp > 0:
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)

        monster.fighter.regen_timer -= monster.fighter.regen_rate
        if monster.fighter.regen_timer <= 0:
            monster.fighter.regenerate()
            monster.fighter.regen_timer = monster.fighter.base_regen_timer
            
        return results
    
class ArcherMonster:
    def take_turn(self, target, game_map, entities):
        results = []
        monster = self.owner
        
        if game_map.fov[monster.x, monster.y]:
            if monster.distance_to(target) > monster.fighter.max_missile_range:
                monster.move_towards(target.x, target.y, game_map, entities)
            elif monster.distance_to(target) <= 2: 
                random_x = self.owner.x + randint(0, 2) - 1
                random_y = self.owner.y + randint(0, 2) - 1
                if random_x != self.owner.x and random_y != self.owner.y:
                    self.owner.move_towards(random_x, random_y, game_map, entities)
            elif target.fighter.hp > 0:
                missile_attack_results = monster.fighter.missile_attack(target)
                results.extend(missile_attack_results)

        monster.fighter.regen_timer -= monster.fighter.regen_rate
        if monster.fighter.regen_timer <= 0:
            monster.fighter.regenerate()
            monster.fighter.regen_timer = monster.fighter.base_regen_timer
            
        return results

class CowardlyMonster:
    def take_turn(self, target, game_map, entities):
        results = []
        monster = self.owner
        
        if game_map.fov[monster.x, monster.y]:
            if monster.distance_to(target) >= 2:
                monster.move_away(target.x, target.y, game_map, entities)
            elif target.fighter.hp > 0:
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)

        else:
            random_x = self.owner.x + randint(0, 2) - 1
            random_y = self.owner.y + randint(0, 2) - 1
            if random_x != self.owner.x and random_y != self.owner.y:
                self.owner.move_towards(random_x, random_y, game_map, entities)

        monster.fighter.regen_timer -= monster.fighter.regen_rate
        if monster.fighter.regen_timer <= 0:
            monster.fighter.regenerate()
            monster.fighter.regen_timer = monster.fighter.base_regen_timer
            
        return results
                
class NaturalMonster:
    def __init__(self, aggressive=False):
        self.aggressive = aggressive

    def take_turn(self, target, game_map, entities):
        results = []
        animal = self.owner

        if not self.aggressive:
            random_x = self.owner.x + randint(0, 2) - 1
            random_y = self.owner.y + randint(0, 2) - 1
            if random_x != self.owner.x and random_y != self.owner.y:
                self.owner.move_towards(random_x, random_y, game_map, entities)

        if randint(0, 100) > 99 or animal.fighter.hp < animal.fighter.max_hp:
            self.aggressive = True
            aggressive_ai = BasicMonster()
            aggressive_ai.owner = animal
            animal.ai = aggressive_ai
            
            results.append({'message': Message('The feral cry echoes in the distance!'.format(self.owner.name),
                                               (255, 127, 0))})

        return results       

class ConfusedMonster:
    def __init__(self, previous_ai, duration=10):
        self.previous_ai = previous_ai
        self.duration = duration

    def take_turn(self, target, game_map, entities):
        results = []

        if self.duration > 0:
            random_x = self.owner.x + randint(0, 2) - 1
            random_y = self.owner.y + randint(0, 2) - 1

            if random_x != self.owner.x and random_y != self.owner.y:
                self.owner.move_towards(random_x, random_y, game_map, entities)

            self.duration -= 1
        else:
            self.owner.ai = self.previous_ai
            results.append({'message': Message('The {0} is no longer confused!'.format(self.owner.name),
                                               (114, 255, 114))})

        return results

class FrozenMonster:
    def __init__(self, previous_ai, duration=3):
        self.previous_ai = previous_ai
        self.duration = duration

    def take_turn(self, target, game_map, entities):
        results = []

        if self.duration > 0:
            self.owner.move(0, 0)
            self.duration -= 1
        else:
            self.owner.ai = self.previous_ai
            results.append({'message': Message('The ice around the {0} melts!'.format(self.owner.name))})

        return results
