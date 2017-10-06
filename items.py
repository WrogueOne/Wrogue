from random import randint

from components.equipment import EquipmentSlots
from components.equippable import Equippable
from components.item import Item
from components.entity import Entity

from item_functions import cast_confuse, cast_fireball, cast_lightning, cast_blizzard
from item_functions import cast_teleport, cast_magic_map
from item_functions import heal, boost_attribute, bless_item
from item_functions import cure_poison, cure_sickness
from item_functions import summon_monsters

from random_utils import from_dungeon_level, random_choice_from_dict

from render_functions import RenderOrder

from game_messages import Message

def generate_dropped_items(entity, colors, entities):

    x = entity.x
    y = entity.y

    item_chances = {
        'gold': 25,
        'rock': 15,
        'stick': 10,
        'string': 15,
        'turkey_leg': 3,
        'severed_toe': 7
        }

    item_choice = random_choice_from_dict(item_chances)

    droppable_items = {
        'gold': (Entity(x, y, '$', colors.get('yellow'), 'Gold', render_order=RenderOrder.ITEM,
                      item=Item(use_function=None))),
        'rock': (Entity(x, y, '*', colors.get('dark_gray'), 'Rock', render_order=RenderOrder.ITEM,
                      item=Item(use_function=None))),
        'stick': (Entity(x, y, '/', colors.get('sepia'), 'Stick', render_order=RenderOrder.ITEM,
                      item=Item(use_function=None))),
        'string': (Entity(x, y, '~', colors.get('gray'), 'String', render_order=RenderOrder.ITEM,
                      item=Item(use_function=None))),
        'turkey_leg': (Entity(x, y, '!', colors.get('dark_sepia'), 'Turkey Leg', render_order=RenderOrder.ITEM,
                      item=Item(use_function=None))),
        'severed_toe': (Entity(x, y, '`', colors.get('darkest_red'), 'Severed Toe', render_order=RenderOrder.ITEM,
                      item=Item(use_function=None)))
        }

    item = droppable_items.get(item_choice)
    entities.append(item)

def generate_items(x, y, entities, dungeon_level, colors):

    item_chances = {
        'short_sword': 10,
        'long_sword': from_dungeon_level([[5, 3], [15, 6], [25, 10]], dungeon_level),
        'broad_sword': from_dungeon_level([[5, 5], [15, 12], [25, 20]], dungeon_level),
        'hand_axe': 5,
        'battle_axe': from_dungeon_level([[5, 6], [15, 15], [25, 25]], dungeon_level),
        'club': 15,
        'mace': from_dungeon_level([[10, 3], [15, 5], [25, 8]], dungeon_level),
        'warhammer': from_dungeon_level([[10, 6], [15, 10], [25, 20]], dungeon_level),
        'cap': 15,
        'helm': from_dungeon_level([[10, 3], [15, 5], [25, 10]], dungeon_level),
        'shirt': 20,
        'leather_armor': from_dungeon_level([[10, 3], [15, 5], [25, 10]], dungeon_level),
        'chain_mail': from_dungeon_level([[10, 6], [15, 10], [25, 20]], dungeon_level),
        'buckler': 10,
        'medium_shield': from_dungeon_level([[5, 3], [15, 6], [25, 10]], dungeon_level),
        'large_shield': from_dungeon_level([[5, 6], [15, 12], [25, 20]], dungeon_level),
        'ring_of_power': from_dungeon_level([[1, 1], [2, 5], [5, 10]], dungeon_level),
        'ring_of_accuracy': from_dungeon_level([[1, 1], [2, 5], [5, 10]], dungeon_level),
        'ring_of_defense': from_dungeon_level([[1, 1], [2, 5], [5, 10]], dungeon_level),
        'ring_of_dodge': from_dungeon_level([[1, 1], [2, 5], [5, 10]], dungeon_level),
        'ring_of_regeneration': from_dungeon_level([[1, 1], [2, 5], [5, 10]], dungeon_level),
        'ring_of_healing': from_dungeon_level([[1, 1], [2, 5], [5, 10]], dungeon_level),
        'healing_potion': 35,
        'extra_healing_potion': from_dungeon_level([[5, 3], [15, 10], [25, 15]], dungeon_level),
        'boost_power_potion': 1,
        'boost_regen_potion': 1,
        'boost_accuracy_potion': 1,
        'boost_dodge_potion': 1,
        'boost_regen_rate_potion': 1,
        'boost_hp_potion': 1,
        'antidote':  5,
        'vaccine': 5,
        'lightning_scroll': from_dungeon_level([[10, 4]], dungeon_level),
        'fireball_scroll': from_dungeon_level([[10, 6]], dungeon_level),
        'confusion_scroll': from_dungeon_level([[15, 2]], dungeon_level),
        'blizzard_scroll': from_dungeon_level([[5, 5]], dungeon_level),
        'magic_map_scroll': 5,
        'teleport_scroll': 2,
        'summoning_scroll': 5,
        'bless_scroll': 2
    }
    
    if not any([entity for entity in entities if entity.x == x and entity.y == y]):
        item_choice = random_choice_from_dict(item_chances)
    else:
        item_choice = 'healing_potion'

    items = {
        'short_sword': (Entity(x, y, '/', colors.get('gray'), 'Short Sword',
                               render_order=RenderOrder.ITEM,
                               equippable=Equippable(EquipmentSlots.MAIN_HAND, power_bonus=3))),
        'long_sword': (Entity(x, y, '/', colors.get('dark_gray'), 'Long Sword',
                               render_order=RenderOrder.ITEM,
                               equippable=Equippable(EquipmentSlots.MAIN_HAND, power_bonus=4, defense_bonus=1))),
        'broad_sword':  (Entity(x, y, '/', colors.get('darker_gray'), 'Broad Sword',
                               render_order=RenderOrder.ITEM,
                               equippable=Equippable(EquipmentSlots.MAIN_HAND, power_bonus=5, defense_bonus=1))),
        'hand_axe': (Entity(x, y, '/', colors.get('red'), 'Hand Axe',
                            render_order=RenderOrder.ITEM,
                            equippable=Equippable(EquipmentSlots.MAIN_HAND, power_bonus=4))),
        'battle_axe': (Entity(x, y, '/', colors.get('sky'), 'Battle Axe',
                               render_order=RenderOrder.ITEM,
                               equippable=Equippable(EquipmentSlots.MAIN_HAND, power_bonus=6))),
        'club': (Entity(x, y, '|', colors.get('sepia'), 'Club',
                        render_order=RenderOrder.ITEM,
                        equippable=Equippable(EquipmentSlots.MAIN_HAND, power_bonus=2, accuracy_bonus=1))),
        'mace': (Entity(x, y, '|', colors.get('gray'), 'Mace',
                        render_order=RenderOrder.ITEM,
                        equippable=Equippable(EquipmentSlots.MAIN_HAND, power_bonus=4, accuracy_bonus=1))),
        'warhammer': (Entity(x, y, '/', colors.get('darker_gray'), 'Warhammer',
                               render_order=RenderOrder.ITEM,
                               equippable=Equippable(EquipmentSlots.MAIN_HAND, power_bonus=5, accuracy_bonus=1))),
        'cap':  (Entity(x, y, ']', colors.get('white'), 'Cap',
                        render_order=RenderOrder.ITEM,
                        equippable=Equippable(EquipmentSlots.HEAD, defense_bonus=1))),
        'helm':  (Entity(x, y, ']', colors.get('gray'), 'Helm',
                        render_order=RenderOrder.ITEM,
                        equippable=Equippable(EquipmentSlots.HEAD, defense_bonus=2))),
        'shirt':  (Entity(x, y, '#', colors.get('white'), 'Shirt',
                        render_order=RenderOrder.ITEM,
                        equippable=Equippable(EquipmentSlots.BODY, defense_bonus=1))),
        'leather_armor':  (Entity(x, y, ']', colors.get('sepia'), 'Leather Armor',
                        render_order=RenderOrder.ITEM,
                        equippable=Equippable(EquipmentSlots.BODY, defense_bonus=3))),
        'chain_mail':  (Entity(x, y, ']', colors.get('gray'), 'Chain Mail',
                        render_order=RenderOrder.ITEM,
                        equippable=Equippable(EquipmentSlots.BODY, defense_bonus=5))),
        'buckler':  (Entity(x, y, ')', colors.get('sepia'), 'Buckler',
                        render_order=RenderOrder.ITEM,
                        equippable=Equippable(EquipmentSlots.OFF_HAND, defense_bonus=1))),
        'medium_shield':  (Entity(x, y, ')', colors.get('gray'), 'Medium Shield',
                        render_order=RenderOrder.ITEM,
                        equippable=Equippable(EquipmentSlots.OFF_HAND, defense_bonus=2))),
        'large_shield':  (Entity(x, y, ')', colors.get('dark_gray'), 'Large Shield',
                        render_order=RenderOrder.ITEM,
                        equippable=Equippable(EquipmentSlots.OFF_HAND, defense_bonus=4))),
        'ring_of_power':  (Entity(x, y, '=', colors.get('red'), 'Ring of Power',
                        render_order=RenderOrder.ITEM,
                        equippable=Equippable(EquipmentSlots.RING_A, power_bonus=1))),
        'ring_of_accuracy':  (Entity(x, y, '=', colors.get('yellow'), 'Ring of Accuracy',
                        render_order=RenderOrder.ITEM,
                        equippable=Equippable(EquipmentSlots.RING_A, accuracy_bonus=1))),
        'ring_of_defense':  (Entity(x, y, '=', colors.get('blue'), 'Ring of Defense',
                        render_order=RenderOrder.ITEM,
                        equippable=Equippable(EquipmentSlots.RING_B, defense_bonus=1))),
        'ring_of_dodge':  (Entity(x, y, '=', colors.get('light_blue'), 'Ring of Dodge',
                        render_order=RenderOrder.ITEM,
                        equippable=Equippable(EquipmentSlots.RING_B, dodge_bonus=1))),
        'ring_of_regeneration':  (Entity(x, y, '=', colors.get('green'), 'Ring of Regeneration',
                        render_order=RenderOrder.ITEM,
                        equippable=Equippable(EquipmentSlots.RING_A, regen_bonus=1))),
        'ring_of_healing':  (Entity(x, y, '=', colors.get('white'), 'Ring of Healing',
                        render_order=RenderOrder.ITEM,
                        equippable=Equippable(EquipmentSlots.RING_A, regen_rate_bonus=10))),
        'healing_potion': (Entity(x, y, '!', colors.get('light_violet'), 'Healing Potion',
                                  render_order=RenderOrder.ITEM,
                                  item=Item(use_function=heal, amount=20))),
        'extra_healing_potion': (Entity(x, y, '!', colors.get('violet'), 'Extra-Healing Potion',
                                        render_order=RenderOrder.ITEM,
                                        item=Item(use_function=heal, amount=50))),
        'boost_power_potion': (Entity(x, y, '!', colors.get('red'), 'Potion of Power',
                                        render_order=RenderOrder.ITEM,
                                        item=Item(use_function=boost_attribute, attribute='power', amount=1))),
        'boost_regen_potion': (Entity(x, y, '!', colors.get('green'), 'Potion of Regeneration',
                                        render_order=RenderOrder.ITEM,
                                        item=Item(use_function=boost_attribute, attribute='regen', amount=1))),
        'boost_accuracy_potion': (Entity(x, y, '!', colors.get('yellow'), 'Potion of Accuracy',
                                        render_order=RenderOrder.ITEM,
                                        item=Item(use_function=boost_attribute, attribute='accuracy', amount=1))),
        'boost_dodge_potion': (Entity(x, y, '!', colors.get('light_blue'), 'Potion of Dexterity',
                                        render_order=RenderOrder.ITEM,
                                        item=Item(use_function=boost_attribute, attribute='dodge', amount=1))),
        'boost_regen_rate_potion': (Entity(x, y, '!', colors.get('white'), 'Potion of Enhanced Healing',
                                        render_order=RenderOrder.ITEM,
                                        item=Item(use_function=boost_attribute, attribute='regen_rate', amount=10))),
        'boost_hp_potion': (Entity(x, y, '!', colors.get('light_green'), 'Potion of Improved Health',
                                        render_order=RenderOrder.ITEM,
                                        item=Item(use_function=boost_attribute, attribute='max_hp', amount=10))),
        'boost_defense_potion': (Entity(x, y, '!', colors.get('blue'), 'Potion of Defense',
                                        render_order=RenderOrder.ITEM,
                                        item=Item(use_function=boost_attribute, attribute='defense', amount=1))),
        'antidote': (Entity(x, y, '!', colors.get('light_flame'), 'Antidote',
                                  render_order=RenderOrder.ITEM,
                                  item=Item(use_function=cure_poison))),
        'vaccine': (Entity(x, y, '!', colors.get('dark_flame'), 'Vaccine',
                                  render_order=RenderOrder.ITEM,
                                  item=Item(use_function=cure_sickness))),
        'fireball_scroll': (Entity(x, y, '?', colors.get('red'), 'Fireball Scroll',
                                   render_order=RenderOrder.ITEM,
                                   item=Item(use_function=cast_fireball, targeting=True, targeting_message=Message(
                                  'Left-click a target tile for the fireball, or right-click to cancel.', colors.get('light_cyan')),
                                        damage=25, radius=3))),
        'confusion_scroll': (Entity(x, y, '?', colors.get('light_pink'), 'Confusion Scroll',
                                    render_order=RenderOrder.ITEM,
                                    item=Item(use_function=cast_confuse, targeting=True, targeting_message=Message(
                                  'Left-click an enemy to confuse it, or right-click to cancel.', colors.get('light_cyan')),
                                        duration=10))),
        'blizzard_scroll': (Entity(x, y, '?', colors.get('light_blue'), 'Blizzard Scroll',
                                   render_order=RenderOrder.ITEM,
                                   item=Item(use_function=cast_blizzard, targeting=True, targeting_message=Message(
                                  'Left-click an enemy for the blizzard, or right-click to cancel.', colors.get('light_cyan')),
                                        duration=5))),
        'lightning_scroll': (Entity(x, y, '?', colors.get('yellow'), 'Lightning Scroll',
                                    render_order=RenderOrder.ITEM,
                                    item=Item(use_function=cast_lightning, damage=20, maximum_range=5))),
        'magic_map_scroll': (Entity(x, y, '?', colors.get('sepia'), 'Magic Map',
                                    render_order=RenderOrder.ITEM,
                                    item=Item(use_function=cast_magic_map))),
        'teleport_scroll': (Entity(x, y, '?', colors.get('light_green'), 'Teleport Scroll',
                                   render_order=RenderOrder.ITEM,
                                   item=Item(use_function=cast_teleport))),
        'bless_scroll': (Entity(x, y, '?', colors.get('white'), 'Scroll of Blessing',
                                   render_order=RenderOrder.ITEM,
                                   item=Item(use_function=bless_item))),
        'summoning_scroll': (Entity(x, y, '?', colors.get('light_yellow'), 'Scroll of Summoning',
                                   render_order=RenderOrder.ITEM,
                                   item=Item(use_function=summon_monsters)))
        }

    item = items.get(item_choice)
    entities.append(item)
