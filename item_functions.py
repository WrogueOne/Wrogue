from components.entity import get_blocking_entities_at_location

from components.ai import ConfusedMonster, FrozenMonster

from game_messages import Message

from random import randint, shuffle
import random

def summon_monsters(*args, **kwargs):
    summoner = args[0]
    colors = args[1]

    entities = kwargs.get('entities')
    game_map = kwargs.get('game_map')
    
    results = []

    open_cells = []
    for dx in range(-2, 2):
        for dy in range(-2, 2):
            if game_map.walkable[summoner.x + dx][summoner.y + dy]:
                open_cells.append([[summoner.x + dx], [summoner.y + dy]])

    shuffle(open_cells)
    (x, y) = open_cells.pop()

    results.append({'consumed': True, 're_render': True,
                    'message': Message('This scroll isnt fully functional yet.', colors.get('light_yellow'))})
    return results

def bless_item(*args, **kwargs):
    user = args[0]
    colors = args[1]

    results = []

    items = []

    for item in user.inventory.items:
        items.append(item)

    blessed_item = random.choice(items)

    results.append({'consumed': True,
                    'message': Message('Your {0} glows with a bright blue light'.format(blessed_item.name), colors.get('cyan'))})

    blessed_item.name = 'Blessed ' + blessed_item.name
    
    return results    

def boost_attribute(*args, **kwargs):
    user = args[0]
    colors = args[1]
    attribute = kwargs.get('attribute')
    amount = kwargs.get('amount')

    results = []

    if attribute == 'power':
        user.fighter.base_power += amount
        results.append({'consumed': True,
                        'message': Message('You feel stronger', colors.get('violet'))})
    elif attribute == 'dodge':
        user.fighter.base_dodge += amount
        results.append({'consumed': True,
                        'message': Message('Your reflexes improve', colors.get('violet'))})
    elif attribute == 'regen':
        user.fighter.base_regen += amount
        results.append({'consumed': True,
                        'message': Message('Your blood races', colors.get('violet'))})
    elif attribute == 'regen_rate':
        user.fighter.base_regen_rate+= amount
        results.append({'consumed': True,
                        'message': Message('You experience a short hot flash', colors.get('violet'))})
    elif attribute == 'accuracy':
        user.fighter.base_accuracy += amount
        results.append({'consumed': True,
                        'message': Message('Your eyesight sharpens', colors.get('violet'))})
    elif attribute == 'hp':
        user.fighter.base_max_hp += amount
        results.append({'consumed': True,
                        'message': Message('You feel healthier', colors.get('violet'))})
    elif attribute == 'defense':
        user.fighter.base_defense += amount
        results.append({'consumed': True,
                        'message': Message('You skin thickens', colors.get('violet'))})
    else:
        results.append({'consumed': False,
                        'message': Message('You drink the potion...  Nothing happens', colors.get('violet'))})

    return results

def heal(*args, **kwargs):
    entity = args[0]
    colors = args[1]
    amount = kwargs.get('amount')

    results = []
    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({'consumed': False, 'message': Message('You are already at full health, why not save this for later',
                                                              colors.get('yellow'))})
    else:
        entity.fighter.heal(amount)
        results.append({'consumed': True, 'message': Message('Your wounds start to feel better!', colors.get('green'))})
    return results

def cure_poison(*args, **kwargs):
    entity = args[0]
    colors = args[1]

    results = []
    if entity.fighter.is_poisoned == False:
        results.append({'consumed': False, 'message': Message('You are not currently poisoned, why not save this for later',
                                                    colors.get('yellow'))})
    else:
        entity.fighter.is_poisoned = False
        results.append({'consumed': True, 'message': Message('You feel a cool rush pass through your body', colors.get('green'))})

    return results

def cure_sickness(*args, **kwargs):
    entity = args[0]
    colors = args[1]

    results = []
    if entity.fighter.is_sick == False:
        results.append({'consumed': False, 'message': Message('You are not currently ill, why not save this for later',
                                                    colors.get('yellow'))})
    else:
        entity.fighter.is_sick = False
        results.append({'consumed': True, 'message': Message('That disgusting cough cleared right up!', colors.get('green'))})

    return results

def cast_confuse(*args, **kwargs):
    colors = args[1]
    entities = kwargs.get('entities')
    game_map = kwargs.get('game_map')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')
    duration = kwargs.get('duration')

    results = []

    if not game_map.fov[target_x, target_y]:
        results.append({'consumed': False, 'message': Message('You cannot target a tile outside your field of view.',
                                                              colors.get('yellow'))})
        return results

    for entity in entities:
        if entity.x == target_x and entity.y == target_y and entity.ai:
            confused_ai = ConfusedMonster(entity.ai, duration)

            confused_ai.owner = entity
            entity.ai = confused_ai

            results.append({'consumed': True, 'message': Message('The eyes of the {0} look vacant, as he starts to stumble around!'.format(entity.name),
                                                                 colors.get('light_green'))})

            break
    else:
        results.append({'consumed': False, 'message': Message('There is no targetable enemy at that location.',
                                                              colors.get('yellow'))})

    return results

def cast_lightning(*args, **kwargs):
    caster = args[0]
    colors = args[1]
    entities = kwargs.get('entities')
    game_map = kwargs.get('game_map')
    damage = kwargs.get('damage')
    maximum_range = kwargs.get('maximum_range')

    results = []

    target = None
    closest_distance = maximum_range + 1

    for entity in entities:
        if entity.fighter and entity != caster and game_map.fov[entity.x, entity.y]:
            distance = caster.distance_to(entity)

            if distance < closest_distance:
                target = entity
                closest_distance = distance

    if target:
        results.append({'consumed': True, 'target': target, 'message': Message('A lighting bolt strikes the {0} with a loud thunder! The damage is {1}'.format(target.name, damage))})
        results.extend(target.fighter.take_damage(damage))
    else:
        results.append({'consumed': False, 'target': None, 'message': Message('No enemy is close enough to strike.', colors.get('red'))})

    return results

def cast_teleport(*args, **kwargs):
    caster = args[0]
    colors = args[1]
    entities = kwargs.get('entities')
    game_map = kwargs.get('game_map')

    results = []
    teleported = False

    while teleported == False:
        x = randint(1, game_map.width - 1)
        y = randint(1, game_map.height - 1)

        if game_map.walkable[x, y] == True:
            caster.x = x
            caster.y = y
            teleported = True
            results.append({'consumed': True, 're_render': True, 'message': Message(
                'Your mind and body are wrenched through time and space', colors.get('light_green'))})
        else:
            continue

    return results

def cast_magic_map(*args, **kwargs):
    colors = args[1]
    game_map = kwargs.get('game_map')

    results = []

    if game_map.dungeon_level % 5 != 0:
        for x, y in game_map:
            if game_map.fov[x, y]:
                game_map.explored[x][y] = True
            elif game_map.transparent [x, y]:
                game_map.explored[x][y] = True
        results.append({'consumed': True, 're_render': True, 'message': Message(
                    'A map of a dungeon forms in your mind', colors.get('sepia'))})
        return results

    else:
        results.append({'consumed': True, 'message': Message(
                    'The scroll turns to dust', colors.get('sepia'))})

    return results
    
def cast_fireball(*args, **kwargs):
    colors = args[1]
    entities = kwargs.get('entities')
    game_map = kwargs.get('game_map')
    damage = kwargs.get('damage')
    radius = kwargs.get('radius')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not game_map.fov[target_x, target_y]:
        results.append({'consumed': False, 'message': Message('You cannot target a tile outside your field of view.',
                                                              colors.get('yellow'))})
        return results

    results.append({'consumed': True,
                    'message': Message('The fireball explodes, burning everything within {0} tiles!'.format(radius),
                                       colors.get('orange'))})

    for entity in entities:
        if entity.distance(target_x, target_y) <= radius and entity.fighter:
            results.append({'message': Message('The {0} gets burned for {1} hit points.'.format(entity.name, damage),
                                               colors.get('orange'))})
            results.extend(entity.fighter.take_damage(damage))

    return results

def cast_blizzard(*args, **kwargs):
    colors = args[1]
    entities = kwargs.get('entities')
    game_map = kwargs.get('game_map')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')
    duration = kwargs.get('duration')

    results = []

    if not game_map.fov[target_x, target_y]:
        results.append({'consumed': False, 'message': Message('You cannot target a tile outside your field of view.',
                                                              colors.get('yellow'))})
        return results

    for entity in entities:
        if entity.x == target_x and entity.y == target_y and entity.ai:
            frozen_ai = FrozenMonster(entity.ai, duration)

            frozen_ai.owner = entity
            entity.ai = frozen_ai

            results.append({'consumed': True, 'message': Message('The blizard freezes the {0} inside a block of ice!'.format(entity.name),
                                                                 colors.get('light_cyan'))})

            break
    else:
        results.append({'consumed': False, 'message': Message('There is no targetable enemy at that location.',
                                                              colors.get('yellow'))})

    return results
