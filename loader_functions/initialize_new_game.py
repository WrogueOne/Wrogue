from components.equipment import Equipment
from components.equippable import Equippable
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from components.entity import Entity

from equipment_slots import EquipmentSlots

from game_messages import MessageLog

from game_states import GameStates

from map_utils import GameMap, make_level

from render_functions import RenderOrder

import random

def get_constants():
    window_title = 'WrogueOne'

    screen_width = 100
    screen_height = 60

    map_width = 80
    map_height = 45

    panel_height = 12
    panel_y = screen_height - panel_height
    bar_width = 25

    sidebar_height = screen_height - panel_height
    sidebar_width = 18
    sidebar_x = screen_width - sidebar_width
    sidebar_y = screen_height - 1

    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 2

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30
    
    fov_algorithm = 'BASIC'
    fov_light_walls = True
    fov_radius = 10

    seed = random.seed()

    colors = {
        'dark_wall': (0, 0, 100),
        'dark_ground': (50, 50, 150),
        'light_wall': (130, 110, 50),
        'light_ground': (200, 180, 50),
        
        # grey levels
        'black': (0,0,0),
        'darkest_grey': (31,31,31),
        'darker_grey': (63,63,63),
        'dark_grey': (95,95,95),
        'grey': (127,127,127),
        'light_grey': (159,159,159),
        'lighter_grey': (191,191,191),
        'lightest_grey': (223,223,223),
        'darkest_gray': (31,31,31),
        'darker_gray': (63,63,63),
        'dark_gray': (95,95,95),
        'gray': (127,127,127),
        'light_gray': (159,159,159),
        'lighter_gray': (191,191,191),
        'lightest_gray': (223,223,223),
        'white': (255,255,255),

        # sepia
        'darkest_sepia': (31,24,15),
        'darker_sepia': (63,50,31),
        'dark_sepia': (94,75,47),
        'sepia': (127,101,63),
        'light_sepia': (158,134,100),
        'lighter_sepia': (191,171,143),
        'lightest_sepia': (222,211,195),

        #standard s
        'red': (255,0,0),
        'flame': (255,63,0),
        'orange': (255,127,0),
        'amber': (255,191,0),
        'yellow': (255,255,0),
        'lime': (191,255,0),
        'chartreuse': (127,255,0),
        'green': (0,255,0),
        'sea': (0,255,127),
        'turquoise': (0,255,191),
        'cyan': (0,255,255),
        'sky': (0,191,255),
        'azure': (0,127,255),
        'blue': (0,0,255),
        'han': (63,0,255),
        'violet': (127,0,255),
        'purple': (191,0,255),
        'fuchsia': (255,0,255),
        'magenta': (255,0,191),
        'pink': (255,0,127),
        'crimson': (255,0,63),

        # dark s
        'dark_red': (191,0,0),
        'dark_flame': (191,47,0),
        'dark_orange': (191,95,0),
        'dark_amber': (191,143,0),
        'dark_yellow': (191,191,0),
        'dark_lime': (143,191,0),
        'dark_chartreuse': (95,191,0),
        'dark_green': (0,191,0),
        'dark_sea': (0,191,95),
        'dark_turquoise': (0,191,143),
        'dark_cyan': (0,191,191),
        'dark_sky': (0,143,191),
        'dark_azure': (0,95,191),
        'dark_blue': (0,0,191),
        'dark_han': (47,0,191),
        'dark_violet': (95,0,191),
        'dark_purple': (143,0,191),
        'dark_fuchsia': (191,0,191),
        'dark_magenta': (191,0,143),
        'dark_pink': (191,0,95),
        'dark_crimson': (191,0,47),

        # darker s
        'darker_red': (127,0,0),
        'darker_flame': (127,31,0),
        'darker_orange': (127,63,0),
        'darker_amber': (127,95,0),
        'darker_yellow': (127,127,0),
        'darker_lime': (95,127,0),
        'darker_chartreuse': (63,127,0),
        'darker_green': (0,127,0),
        'darker_sea': (0,127,63),
        'darker_turquoise': (0,127,95),
        'darker_cyan': (0,127,127),
        'darker_sky': (0,95,127),
        'darker_azure': (0,63,127),
        'darker_blue': (0,0,127),
        'darker_han': (31,0,127),
        'darker_violet': (63,0,127),
        'darker_purple': (95,0,127),
        'darker_fuchsia': (127,0,127),
        'darker_magenta': (127,0,95),
        'darker_pink': (127,0,63),
        'darker_crimson': (127,0,31),

        # darkest s
        'darkest_red': (63,0,0),
        'darkest_flame': (63,15,0),
        'darkest_orange': (63,31,0),
        'darkest_amber': (63,47,0),
        'darkest_yellow': (63,63,0),
        'darkest_lime': (47,63,0),
        'darkest_chartreuse': (31,63,0),
        'darkest_green': (0,63,0),
        'darkest_sea': (0,63,31),
        'darkest_turquoise': (0,63,47),
        'darkest_cyan': (0,63,63),
        'darkest_sky': (0,47,63),
        'darkest_azure': (0,31,63),
        'darkest_blue': (0,0,63),
        'darkest_han': (15,0,63),
        'darkest_violet': (31,0,63),
        'darkest_purple': (47,0,63),
        'darkest_fuchsia': (63,0,63),
        'darkest_magenta': (63,0,47),
        'darkest_pink': (63,0,31),
        'darkest_crimson': (63,0,15),

        # light s
        'light_red': (255,114,114),
        'light_flame': (255,149,114),
        'light_orange': (255,184,114),
        'light_amber': (255,219,114),
        'light_yellow': (255,255,114),
        'light_lime': (219,255,114),
        'light_chartreuse': (184,255,114),
        'light_green': (114,255,114),
        'light_sea': (114,255,184),
        'light_turquoise': (114,255,219),
        'light_cyan': (114,255,255),
        'light_sky': (114,219,255),
        'light_azure': (114,184,255),
        'light_blue': (114,114,255),
        'light_han': (149,114,255),
        'light_violet': (184,114,255),
        'light_purple': (219,114,255),
        'light_fuchsia': (255,114,255),
        'light_magenta': (255,114,219),
        'light_pink': (255,114,184),
        'light_crimson': (255,114,149),

        #lighter s
        'lighter_red': (255,165,165),
        'lighter_flame': (255,188,165),
        'lighter_orange': (255,210,165),
        'lighter_amber': (255,232,165),
        'lighter_yellow': (255,255,165),
        'lighter_lime': (232,255,165),
        'lighter_chartreuse': (210,255,165),
        'lighter_green': (165,255,165),
        'lighter_sea': (165,255,210),
        'lighter_turquoise': (165,255,232),
        'lighter_cyan': (165,255,255),
        'lighter_sky': (165,232,255),
        'lighter_azure': (165,210,255),
        'lighter_blue': (165,165,255),
        'lighter_han': (188,165,255),
        'lighter_violet': (210,165,255),
        'lighter_purple': (232,165,255),
        'lighter_fuchsia': (255,165,255),
        'lighter_magenta': (255,165,232),
        'lighter_pink': (255,165,210),
        'lighter_crimson': (255,165,188),

        # lightest s
        'lightest_red': (255,191,191),
        'lightest_flame': (255,207,191),
        'lightest_orange': (255,223,191),
        'lightest_amber': (255,239,191),
        'lightest_yellow': (255,255,191),
        'lightest_lime': (239,255,191),
        'lightest_chartreuse': (223,255,191),
        'lightest_green': (191,255,191),
        'lightest_sea': (191,255,223),
        'lightest_turquoise': (191,255,239),
        'lightest_cyan': (191,255,255),
        'lightest_sky': (191,239,255),
        'lightest_azure': (191,223,255),
        'lightest_blue': (191,191,255),
        'lightest_han': (207,191,255),
        'lightest_violet': (223,191,255),
        'lightest_purple': (239,191,255),
        'lightest_fuchsia': (255,191,255),
        'lightest_magenta': (255,191,239),
        'lightest_pink': (255,191,223),
        'lightest_crimson': (255,191,207),

        # desaturated s
        'desaturated_red': (127,63,63),
        'desaturated_flame': (127,79,63),
        'desaturated_orange': (127,95,63),
        'desaturated_amber': (127,111,63),
        'desaturated_yellow': (127,127,63),
        'desaturated_lime': (111,127,63),
        'desaturated_chartreuse': (95,127,63),
        'desaturated_green': (63,127,63),
        'desaturated_sea': (63,127,95),
        'desaturated_turquoise': (63,127,111),
        'desaturated_cyan': (63,127,127),
        'desaturated_sky': (63,111,127),
        'desaturated_azure': (63,95,127),
        'desaturated_blue': (63,63,127),
        'desaturated_han': (79,63,127),
        'desaturated_violet': (95,63,127),
        'desaturated_purple': (111,63,127),
        'desaturated_fuchsia': (127,63,127),
        'desaturated_magenta': (127,63,111),
        'desaturated_pink': (127,63,95),
        'desaturated_crimson': (127,63,79),

        # metallic
        'brass': (191,151,96),
        'copper': (197,136,124),
        'gold': (229,191,0),
        'silver': (203,203,203),

        # miscellaneous
        'celadon': (172,255,175),
        'peach': (255,159,127)

        }

    constants = {
        'window_title': window_title,
        'screen_width': screen_width,
        'screen_height': screen_height,
        'bar_width': bar_width,
        'panel_height': panel_height,
        'panel_y': panel_y,
        'sidebar_height': sidebar_height,
        'sidebar_width': sidebar_width,
        'sidebar_x': sidebar_x, 
        'sidebar_y': sidebar_y,
        'message_x': message_x,
        'message_width': message_width,
        'message_height': message_height,
        'map_width': map_width,
        'map_height': map_height,
        'room_max_size': room_max_size,
        'room_min_size': room_min_size,
        'max_rooms': max_rooms,
        'fov_algorithm': fov_algorithm,
        'fov_light_walls': fov_light_walls,
        'fov_radius': fov_radius,
        'colors': colors,
        'seed': seed
    }

    return constants

def initialize_game(constants):
    player = Entity(0, 0, '@', (255, 255, 255), 'Player', blocks=True,
                    render_order=RenderOrder.ACTOR,
                    fighter=Fighter(hp=100, defense=0, power=1, regen=1, regen_rate=1),
                    inventory=Inventory(26),
                    level=Level(),
                    equipment=Equipment()
                    )

    entities = [player]
    
    shirt =  (Entity(0, 0, '#', constants['colors'].get('white'), 'Shirt',
                        render_order=RenderOrder.ITEM,
                        equippable=Equippable(EquipmentSlots.BODY, defense_bonus=1)))
    player.inventory.add_item(shirt, constants['colors'])
    player.equipment.toggle_equip(shirt)
    
    dagger = Entity(0, 0, '-', constants['colors'].get('sky'), 'Dagger',
                    equippable=Equippable(EquipmentSlots.MAIN_HAND, power_bonus=2))
    player.inventory.add_item(dagger, constants['colors'])
    player.equipment.toggle_equip(dagger)

    game_map = GameMap(constants['map_width'], constants['map_height'])
    make_level(game_map, constants['max_rooms'], constants['room_min_size'],
             constants['room_max_size'], constants['map_width'], constants['map_height'], player, entities,
             constants['colors'])

    message_log = MessageLog(constants['message_x'], constants['message_width'],
                             constants['message_height'])

    game_state = GameStates.PLAYERS_TURN

    return player, entities, game_map, message_log, game_state
