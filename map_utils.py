from tdl.map import Map

from random import randint, shuffle
import random

from components.entity import Entity
from components.fighter import Fighter
from components.item import Item
from components.dungeon_features import Stairs

from game_messages import Message

from random_utils import from_dungeon_level

from render_functions import RenderOrder

from monsters import generate_monsters, generate_epic_monster
from items import generate_items

from item_functions import cast_magic_map, cast_teleport

class GameMap(Map):
    def __init__(self, width, height, dungeon_level=1):
        super().__init__(width, height)
        self.explored = [[False for y in range(height)] for x in range(width)]
        self.visited = [[False for y in range(height)] for x in range(width)]

        self.dungeon_level = dungeon_level

class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return (center_x, center_y)

    def intersect(self, other):
        # returns true if this rectangle intersects with another one
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

def create_room(game_map, room):
    # go through the tiles in the rectangle and make them passable
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            game_map.walkable[x, y] = True
            game_map.transparent[x, y] = True

def create_h_tunnel(game_map, x1, x2, y):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        game_map.walkable[x, y] = True
        game_map.transparent[x, y] = True

def create_v_tunnel(game_map, y1, y2, x):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        game_map.walkable[x, y] = True
        game_map.transparent[x, y] = True

def place_entities(room, entities, dungeon_level, colors, level_type, open_cells=None):

    if level_type == 'standard':
        max_monsters_per_room = from_dungeon_level([[2, 1], [3, 4], [5, 6]], dungeon_level)
        max_items_per_room = from_dungeon_level([[1, 1], [2, 4]], dungeon_level)

        number_of_monsters = randint(0, max_monsters_per_room)
        number_of_items = randint(0, max_items_per_room)

        for i in range(number_of_monsters):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            generate_monsters(x, y, entities, dungeon_level, colors)

        for i in range(number_of_items):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            generate_items(x, y, entities, dungeon_level, colors)

    if level_type == 'maze':
        max_monsters_per_maze = 50
        max_items_per_maze = 10
        shuffle(open_cells)
        
        for i in range(max_monsters_per_maze - 1):
            (x, y) = open_cells.pop()
            generate_monsters(x, y, entities, dungeon_level, colors)

        (x, y) = open_cells.pop
        generate_epic_monster(x, y, entities, colors)

        for i in range(max_items_per_maze):
            (x, y) = open_cells.pop()
            generate_items(x, y, entities, dungeon_level, colors)
        
def make_level(game_map, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, colors):
    level_type = None
    if game_map.dungeon_level % 5 == 0:
        level_type = 'maze'
        make_maze_map(game_map, map_width, map_height, player, entities, colors, level_type)
    else:
        level_type = 'standard'
        make_standard_map(game_map, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, colors,
                          level_type)

def make_maze_map(game_map, map_width, map_height, player, entities, colors, level_type):

    x = randint(5, map_width - 5)
    y = randint(5, map_height - 5)
    history = [(x, y)]
    open_cells = []
    game_map.visited[x][y] = True
    game_map.walkable[x, y] = True
    game_map.transparent[x, y] = True
    player.x = x
    player.y = y

    while history:
        check = []
        if x > 2 and game_map.visited[x-1][y] == False:
            check.append('L')
        if y > 2 and game_map.visited[x][y-1] == False:
            check.append('U')
        if x < map_width - 2 and game_map.visited[x+1][y] == False:
            check.append('R')
        if y < map_height - 2 and game_map.visited[x][y+1] == False:
            check.append('D')

        if len(check):
            history.append([x, y])
            move_direction = random.choice(check)
            if move_direction == 'L':
                game_map.visited[x][y] = True
                game_map.walkable[x, y] = True
                game_map.transparent[x, y] = True
                x -= 1
                if x % 2 == 0 or x % 5 == 0:
                    game_map.visited[x][y-1] = True
                    game_map.visited[x][y+1] = True
            if move_direction == 'U':
                game_map.visited[x][y] = True
                game_map.walkable[x, y] = True
                game_map.transparent[x, y] = True
                y -= 1
                if y % 3 == 0 or y % 7 == 0:
                    game_map.visited[x-1][y] = True
                    game_map.visited[x+1][y] = True
            if move_direction == 'R':
                game_map.visited[x][y] = True
                game_map.walkable[x, y] = True
                game_map.transparent[x, y] = True
                x += 1
                if x % 5 == 0 or x % 11 == 0:
                    game_map.visited[x][y-1] = True
                    game_map.visited[x][y+1] = True
            if move_direction == 'D':
                game_map.visited[x][y] = True
                game_map.walkable[x, y] = True
                game_map.transparent[x, y] = True
                y += 1
                if y % 7 == 0 or y % 13 == 0:
                    game_map.visited[x-1][y] = True
                    game_map.visited[x+1][y] = True

            game_map.visited[x][y] = True
                        
        else:
            (x, y) = history.pop()

    for x, y in game_map:
        if game_map.walkable[x][y]:
            open_cells.append([x, y])

    (stairs_x, stairs_y) = random.choice(open_cells)
        
    down_stairs = Entity(stairs_x, stairs_y, '>', (255, 255, 255), 'Downward Stairs',
                 render_order=RenderOrder.STAIRS,
                 stairs=Stairs(game_map.dungeon_level + 1))
    entities.append(down_stairs)

    # guardian = (Entity(x, y, 'M', colors.get('purple'), 'Guardian Minotaur', blocks=True,
    #                    render_order=RenderOrder.ACTOR,
    #                    fighter=Fighter(hp=80, defense=4, power=8, xp=1000),
    #                    ai=GuardianMonster()))
    # entities.append(guardian)

    room = Rect(0,0,0,0)

    place_entities(room, entities, game_map.dungeon_level, colors, level_type, open_cells)
   
def make_standard_map(game_map, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, colors,
                      level_type):
    rooms = []
    num_rooms = 0

    center_of_last_room_x = None
    center_of_last_room_y = None

    for r in range(max_rooms):

        w = randint(room_min_size, room_max_size)
        h = randint(room_min_size, room_max_size)

        x = randint(0, map_width - w - 1)
        y = randint(0, map_height - h - 1)

        new_room = Rect(x, y, w, h)

        for other_room in rooms:
            if new_room.intersect(other_room):
                break
        else:
            create_room(game_map, new_room)

            (new_x, new_y) = new_room.center()

            center_of_last_room_x = new_x
            center_of_last_room_y = new_y

            if num_rooms == 0:
                player.x = new_x
                player.y = new_y
                if game_map.dungeon_level >= 2:
                    up_stairs = (Entity(player.x, player.y, '<', (255, 255, 255), 'Upward Stairs',
                                       render_order=RenderOrder.STAIRS,
                                       stairs=Stairs(game_map.dungeon_level - 1)
                                       ))
                    entities.append(up_stairs)
            else:
                (prev_x, prev_y) = rooms[num_rooms - 1].center()

                if randint(0, 1) == 1:
                    create_h_tunnel(game_map, prev_x, new_x, prev_y)
                    create_v_tunnel(game_map, prev_y, new_y, new_x)
                else:
                    create_v_tunnel(game_map, prev_y, new_y, prev_x)
                    create_h_tunnel(game_map, prev_x, new_x, new_y)

            place_entities(new_room, entities, game_map.dungeon_level, colors, level_type)
            rooms.append(new_room)
            num_rooms += 1
            
    down_stairs = Entity(center_of_last_room_x, center_of_last_room_y, '>', (255, 255, 255), 'Downward Stairs',
                         render_order=RenderOrder.STAIRS,
                         stairs=Stairs(game_map.dungeon_level + 1))
    entities.append(down_stairs)

def next_floor(player, message_log, dungeon_level, constants):

    game_map = GameMap(constants['map_width'], constants['map_height'], dungeon_level)
    entities = [player]
    
    make_level(game_map, constants['max_rooms'], constants['room_min_size'],
             constants['room_max_size'], constants['map_width'], constants['map_height'], player, entities,
             constants['colors'])

    player.fighter.heal(player.fighter.max_hp // 2)

    message_log.add_message(Message('You take a moment to rest, and recover your strength.',
                                    constants['colors'].get('light_violet')))

    return game_map, entities
