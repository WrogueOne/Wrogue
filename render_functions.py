from enum import Enum

from game_states import GameStates

from menus import character_screen, inventory_menu, level_up_menu

class RenderOrder(Enum):
    STAIRS = 1
    TRAP = 2
    CORPSE = 3
    ITEM = 4
    ACTOR = 5

def get_names_under_mouse(mouse_coordinates, entities, game_map):
    x, y = mouse_coordinates

    names = [entity.name for entity in entities
             if entity.x == x and entity.y == y and game_map.fov[entity.x, entity.y]]
    names = ', '.join(names)

    return names.capitalize()

def get_names_under_player(player_coordinates, entities, game_map):
    x, y = player_coordinates

    names = [entity.name for entity in entities
             if entity.x == x and entity.y == y and game_map.fov[entity.x, entity.y]]
    if 'Player' in names:
        names.remove('Player')
    else:
        pass
    names = ', '.join(names)

    return names.capitalize()

def render_all(con, panel, sidebar, entities, player, game_map, fov_recompute, root_console, message_log, screen_width,
               screen_height, bar_width, panel_height, panel_y, sidebar_height, sidebar_width,
               sidebar_x, sidebar_y, mouse_coordinates, colors, game_state):

    render_dungeon(con, game_map, fov_recompute, colors)

    render_entities(con, entities, game_map, root_console, screen_width, screen_height)

    render_panel(panel, player, root_console, message_log, screen_width, bar_width, panel_height, panel_y, colors)

    render_sidebar(sidebar, entities, player, game_map, mouse_coordinates,
                   sidebar_x, sidebar_y, sidebar_width, sidebar_height,
                   root_console, colors)

    render_game_state_menus(con, root_console, player, screen_width, screen_height, game_state)

def render_dungeon(con, game_map, fov_recompute, colors):        
        if fov_recompute:
            for x, y in game_map:
                wall = not game_map.transparent[x, y]

                if game_map.fov[x, y]:
                    if wall:
                        con.draw_char(x, y, None, fg=None, bg=colors.get('light_wall'))
                    else:
                        con.draw_char(x, y, None, fg=None, bg=colors.get('light_ground'))

                    game_map.explored[x][y] = True
                elif game_map.explored[x][y]:
                    if wall:
                        con.draw_char(x, y, None, fg=None, bg=colors.get('dark_wall'))
                    else:
                        con.draw_char(x, y, None, fg=None, bg=colors.get('dark_ground'))

def render_entities(con, entities, game_map, root_console, screen_width, screen_height):
    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)

    for entity in entities_in_render_order:
        draw_entity(con, entity, game_map)
    root_console.blit(con, 0, 0, screen_width, screen_height, 0, 0)

def render_panel(panel, player, root_console, message_log, screen_width, bar_width, panel_height, panel_y, colors):
    panel.clear(fg=colors.get('white'), bg=colors.get('black'))
    panel.draw_frame(message_log.x, 0, None, None, '-', fg=colors.get('red'), bg=None)
    y = 1
    for message in message_log.messages:
        panel.draw_str(message_log.x + 1, y, message.text, bg=None, fg=message.color)
        y += 1
    panel.draw_frame(0, 0, message_log.x, None, '-', fg=colors.get('light_gray'), bg=None)
    panel_title_color = colors.get('white')
    player_status_text = 'HP'
    if player.fighter.is_sick == True:
        panel_title_color = colors.get('cyan')
        player_status_text = '! SICK !'
    if player.fighter.is_poisoned == True:
        panel_title_color = colors.get('green')
        player_status_text = '! POISONED !'
    panel.draw_str(1, 1, '       Player Info', fg=panel_title_color, bg=None)
    render_bar(panel, 1, 2, bar_width, player_status_text, player.fighter.hp, player.fighter.max_hp,
               colors.get('light_red'), colors.get('darker_red'), colors.get('white'))
    panel.draw_str(1, 4, 'Exp Level:  {0}'.format(player.level.current_level), fg=colors.get('white'), bg=None)
    panel.draw_str(1, 5, 'Pwr: {0}({1})'.format(player.fighter.power, player.fighter.base_power), fg=colors.get('white'), bg=None)
    panel.draw_str(1, 6, 'Acc: {0}({1})'.format(player.fighter.accuracy, player.fighter.base_accuracy), fg=colors.get('white'), bg=None)
    panel.draw_str(1, 7, 'Def: {0}({1})'.format(player.fighter.defense, player.fighter.base_defense), fg=colors.get('white'), bg=None)
    panel.draw_str(1, 8, 'Dod: {0}({1})'.format(player.fighter.dodge, player.fighter.base_dodge), fg=colors.get('white'), bg=None)
    root_console.blit(panel, 0, panel_y, screen_width, panel_height, 0, 0)

def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color, string_color):
    # Render a bar (HP, experience, etc). first calculate the width of the bar
    bar_width = int(float(value) / maximum * total_width)

    # Render the background first
    panel.draw_rect(x, y, total_width, 1, None, bg=back_color)

    # Now render the bar on top
    if bar_width > 0:
        panel.draw_rect(x, y, bar_width, 1, None, bg=bar_color)

    # Finally, some centered text with the values
    text = name + ': ' + str(value) + '/' + str(maximum)
    x_centered = x + int((total_width-len(text)) / 2)

    panel.draw_str(x_centered, y, text, fg=string_color, bg=None)

def render_sidebar(sidebar, entities, player, game_map, mouse_coordinates, sidebar_x, sidebar_y, sidebar_width, sidebar_height,
                   root_console, colors):

    sidebar.clear(fg=colors.get('white'), bg=colors.get('black'))
    sidebar.draw_frame(0, 0, None, None, '-', fg=colors.get('light_gray'), bg=None)
    sidebar_title_color = colors.get('white')
    sidebar.draw_str(1, 1, '  Dungeon Info', fg=sidebar_title_color, bg=None)
    sidebar.draw_str(1, 2, '    Level: {0}'.format(game_map.dungeon_level), fg=colors.get('white'), bg=None)
    if len(get_names_under_player((player.x, player.y), entities, game_map)) >= 2:
        sidebar.draw_str(1, 3, get_names_under_player((player.x, player.y), entities, game_map))
    elif len(get_names_under_player((player.x, player.y), entities, game_map)) >= 2:
        sidebar.draw_str(1, 3, 'A pile of junk')
    else:
        sidebar.draw_str(1, 3, get_names_under_mouse(mouse_coordinates, entities, game_map))
    root_console.blit(sidebar, sidebar_x, 0, sidebar_width, sidebar_height, 0, 0)
    
def render_game_state_menus(con, root_console, player, screen_width, screen_height, game_state):
    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        if game_state == GameStates.SHOW_INVENTORY:
            inventory_title = 'Press the key next to an item to use it, or Esc to cancel.\n'
        else:
            inventory_title = 'Press the key next to an item to drop it, or Esc to cancel.\n'

        inventory_menu(con, root_console, inventory_title, player, 50, screen_width, screen_height)

    elif game_state == GameStates.LEVEL_UP:
        level_up_menu(con, root_console, 'Level up! Choose a stat to raise:', player, 40, screen_width,
                      screen_height)

    elif game_state == GameStates.CHARACTER_SCREEN:
        character_screen(root_console, player, 30, 10, screen_width, screen_height)    

def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)

def draw_entity(con, entity, game_map):
    if game_map.fov[entity.x, entity.y] or (entity.stairs and game_map.explored[entity.x][entity.y]):
        con.draw_char(entity.x, entity.y, entity.char, entity.color, bg=None)

def clear_entity(con, entity):
    # erase the character that represents this object
    con.draw_char(entity.x, entity.y, ' ', entity.color, bg=None)
