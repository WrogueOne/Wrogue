from equipment_slots import EquipmentSlots


class Equipment:
    def __init__(self, main_hand=None, off_hand=None, head=None, body=None,
                 arms=None, boots=None, amulet=None, ring_a=None, ring_b=None,
                 girdle=None, missile_weapon=None, missile_ammunition=None,
                 tool=None):
        self.main_hand = main_hand
        self.off_hand = off_hand
        self.head = head
        self.body = body
        self.arms = arms
        self.boots = boots
        self.amulet = amulet
        self.ring_a = ring_a
        self.ring_b = ring_b
        self.girdle = girdle
        self.missile_weapon = missile_weapon
        self.missile_ammunition = missile_ammunition
        self.tool = tool

    @property
    def max_hp_bonus(self):
        bonus = 0
        equipment_slots = [self.main_hand, self.off_hand, self.head, self.body,
                           self.arms, self.boots, self.amulet, self.ring_a,
                           self.ring_b, self.girdle, self.missile_weapon,
                           self.missile_ammunition, self.tool]
        for slot in equipment_slots:
            if slot and slot.equippable:
                bonus += slot.equippable.max_hp_bonus
        return bonus

    @property
    def power_bonus(self):
        bonus = 0

        equipment_slots = [self.main_hand, self.off_hand, self.head, self.body,
                           self.arms, self.boots, self.amulet, self.ring_a,
                           self.ring_b, self.girdle, self.missile_weapon,
                           self.missile_ammunition, self.tool]
        for slot in equipment_slots:
            if slot and slot.equippable:
                bonus += slot.equippable.power_bonus
        return bonus

    @property
    def accuracy_bonus(self):
        bonus = 0

        equipment_slots = [self.main_hand, self.off_hand, self.head, self.body,
                           self.arms, self.boots, self.amulet, self.ring_a,
                           self.ring_b, self.girdle, self.missile_weapon,
                           self.missile_ammunition, self.tool]
        for slot in equipment_slots:
            if slot and slot.equippable:
                bonus += slot.equippable.accuracy_bonus
        return bonus

    @property
    def defense_bonus(self):
        bonus = 0

        equipment_slots = [self.main_hand, self.off_hand, self.head, self.body,
                           self.arms, self.boots, self.amulet, self.ring_a,
                           self.ring_b, self.girdle, self.missile_weapon,
                           self.missile_ammunition, self.tool]
        for slot in equipment_slots:
            if slot and slot.equippable:
                bonus += slot.equippable.defense_bonus
        return bonus

    @property
    def dodge_bonus(self):
        bonus = 0

        equipment_slots = [self.main_hand, self.off_hand, self.head, self.body,
                           self.arms, self.boots, self.amulet, self.ring_a,
                           self.ring_b, self.girdle, self.missile_weapon,
                           self.missile_ammunition, self.tool]
        for slot in equipment_slots:
            if slot and slot.equippable:
                bonus += slot.equippable.dodge_bonus
        return bonus

    @property
    def mana_bonus(self):
        bonus = 0

        equipment_slots = [self.main_hand, self.off_hand, self.head, self.body,
                           self.arms, self.boots, self.amulet, self.ring_a,
                           self.ring_b, self.girdle, self.missile_weapon,
                           self.missile_ammunition, self.tool]
        for slot in equipment_slots:
            if slot and slot.equippable:
                bonus += slot.equippable.mana_bonus
        return bonus

    @property
    def willpower_bonus(self):
        bonus = 0

        equipment_slots = [self.main_hand, self.off_hand, self.head, self.body,
                           self.arms, self.boots, self.amulet, self.ring_a,
                           self.ring_b, self.girdle, self.missile_weapon,
                           self.missile_ammunition, self.tool]
        for slot in equipment_slots:
            if slot and slot.equippable:
                bonus += slot.equippable.willpower_bonus
        return bonus

    @property
    def missile_bonus(self):
        bonus = 0

        equipment_slots = [self.main_hand, self.off_hand, self.head, self.body,
                           self.arms, self.boots, self.amulet, self.ring_a,
                           self.ring_b, self.girdle, self.missile_weapon,
                           self.missile_ammunition, self.tool]
        for slot in equipment_slots:
            if slot and slot.equippable:
                bonus += slot.equippable.missile_bonus
        return bonus

    @property
    def regen_bonus(self):
        bonus = 0

        equipment_slots = [self.main_hand, self.off_hand, self.head, self.body,
                           self.arms, self.boots, self.amulet, self.ring_a,
                           self.ring_b, self.girdle, self.missile_weapon,
                           self.missile_ammunition, self.tool]
        for slot in equipment_slots:
            if slot and slot.equippable:
                bonus += slot.equippable.regen_bonus
        return bonus

    @property
    def regen_rate_bonus(self):
        bonus = 0

        equipment_slots = [self.main_hand, self.off_hand, self.head, self.body,
                           self.arms, self.boots, self.amulet, self.ring_a,
                           self.ring_b, self.girdle, self.missile_weapon,
                           self.missile_ammunition, self.tool]
        for slot in equipment_slots:
            if slot and slot.equippable:
                bonus += slot.equippable.regen_rate_bonus
        return bonus

    def toggle_equip(self, equippable_entity):
        results = []

        slot = equippable_entity.equippable.slot

        if slot == EquipmentSlots.MAIN_HAND:
            if self.main_hand == equippable_entity:
                self.main_hand = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.main_hand:
                    results.append({'dequipped': self.main_hand})

                self.main_hand = equippable_entity
                results.append({'equipped': equippable_entity})
                
        elif slot == EquipmentSlots.OFF_HAND:
            if self.off_hand == equippable_entity:
                self.off_hand = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.off_hand:
                    results.append({'dequipped': self.off_hand})

                self.off_hand = equippable_entity
                results.append({'equipped': equippable_entity})

        elif slot == EquipmentSlots.HEAD:
            if self.head == equippable_entity:
                self.head = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.head:
                    results.append({'dequipped': self.off_hand})

                self.head = equippable_entity
                results.append({'equipped': equippable_entity})

        elif slot == EquipmentSlots.BODY:
            if self.body == equippable_entity:
                self.body = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.body:
                    results.append({'dequipped': self.off_hand})

                self.body = equippable_entity
                results.append({'equipped': equippable_entity})

        elif slot == EquipmentSlots.RING_A:
            if self.ring_a == equippable_entity:
                self.ring_a = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.ring_a:
                    results.append({'dequipped': self.off_hand})

                self.ring_a = equippable_entity
                results.append({'equipped': equippable_entity})

        elif slot == EquipmentSlots.RING_B:
            if self.ring_b == equippable_entity:
                self.ring_b = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.ring_b:
                    results.append({'dequipped': self.off_hand})

                self.ring_b = equippable_entity
                results.append({'equipped': equippable_entity})

        return results
