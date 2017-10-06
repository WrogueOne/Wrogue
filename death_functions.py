from game_messages import Message

from game_states import GameStates

from render_functions import RenderOrder

from random import randint

from items import generate_dropped_items

from components.ai import NaturalMonster

def kill_player(player, colors):
    player.char = '%'
    player.color = colors.get('dark_red')

    return Message('You died!', colors.get('red')), GameStates.PLAYER_DEAD

def kill_monster(monster, colors, entities):
    death_message = Message('{0} is dead!'.format(monster.name.capitalize()), colors.get('orange'))

    chance_corpse = randint(0, 100)
    chance_item = randint(0, 100)
    
    if monster.ai != NaturalMonster():
        if chance_item >= 80:
            generate_dropped_items(monster, colors, entities)
        else:
            pass

    if chance_corpse >= 80:
        monster.char = '%'
        monster.blocks = False
        monster.fighter = None
        monster.ai = None
        monster.name = 'Remains of ' + monster.name
        monster.render_order = RenderOrder.CORPSE
    else:
        entities.remove(monster)

    return death_message
