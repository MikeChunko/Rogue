# File name: render.py
# Author: Michael Chunko
# Python Version: 3.7

# This file contains the functions used to render the screen

import tcod
from engine import colors


# TODO add render priority (should be pickups < monsters < player)

def render_all(con, panel, message_log, entities, game_map, fov_map, fov_recalculate, screen_width, screen_height,
               bar_width, panel_height, panel_y, ignore_fov=False):
    """ Render every part of the game. """
    # Draw the map
    draw_map(con, game_map, fov_map, fov_recalculate, ignore_fov)

    # Draw all entities
    for entity in entities:
        draw_entity(con, entity, fov_map, ignore_fov)

    tcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

    # Setup the bottom panel
    tcod.console_set_default_background(panel, tcod.black)
    tcod.console_clear(panel)

    # Print game messages to the bottom panel
    render_messages(panel, message_log)

    # Draw the player stats to the bottom panel
    render_bar(panel, 1, 1, bar_width, "HP", entities[0].hp, entities[0].max_hp, tcod.darker_red, tcod.darkest_red)
    render_bar(panel, 1, 3, bar_width, "LVL: {0}".format(entities[0].level), entities[0].xp, entities[0].max_xp,
               tcod.darker_green, tcod.darkest_green)

    # Draw the player inventory to the bottom panel
    render_inventory(panel, entities[0].inventory)

    tcod.console_blit(panel, 0, 0, screen_width, panel_height, 0, 0, panel_y)


def clear_all(con, entities):
    """ Clear the rendered entities by inserting a blank character in their place.
        This prepares the console for the next frame to be rendered. """
    for entity in entities:
        clear_entity(con, entity)


def draw_map(con, game_map, fov_map, fov_recalculate, ignore_fov=False):
    """ Render the map elements (wall, floor) and their proper state (seen/unseen in/not in fov). """
    if fov_recalculate:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = tcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight

                # The tile is in the FOV
                if ignore_fov or visible:
                    # Update the tile to be seen
                    game_map.tiles[x][y].seen = True
                    if wall:
                        tcod.console_set_char_background(con, x, y, colors.get("light wall"), tcod.BKGND_SET)
                    else:
                        tcod.console_set_char_background(con, x, y, colors.get("light ground"), tcod.BKGND_SET)
                else:
                    if not game_map.tiles[x][y].seen:
                        tcod.console_set_char_background(con, x, y, colors.get("unseen"), tcod.BKGND_SET)
                    elif wall:
                        tcod.console_set_char_background(con, x, y, colors.get("dark wall"), tcod.BKGND_SET)
                    else:
                        tcod.console_set_char_background(con, x, y, colors.get("dark ground"), tcod.BKGND_SET)


def draw_entity(con, entity, fov_map, ignore_fov=False):
    """ Render the entity, checking to make sure that it is in the player's fov. """
    if ignore_fov or tcod.map_is_in_fov(fov_map, entity.x, entity.y):
        tcod.console_set_default_foreground(con, entity.color)
        tcod.console_put_char(con, entity.x, entity.y, entity.char, tcod.BKGND_NONE)


def clear_entity(con, entity):
    """ Clear a given entity, replacing it with a blank character. """
    tcod.console_put_char(con, entity.x, entity.y, ' ', tcod.BKGND_NONE)


def render_bar(panel, x, y, total_width, name, value, maximum, foreground_color, background_color):
    """ Render a bar (HP, XP, etc.). """
    bar_width = int((value / maximum) * total_width)

    # Going to be honest, don't know why it has to be done this way
    tcod.console_set_default_background(panel, background_color)
    tcod.console_rect(panel, x, y, total_width, 1, False, tcod.BKGND_SCREEN)
    tcod.console_set_default_background(panel, foreground_color)

    if bar_width > 0:
        tcod.console_rect(panel, x, y, bar_width, 1, False, tcod.BKGND_SCREEN)

    tcod.console_set_default_foreground(panel, tcod.white)
    tcod.console_print_ex(panel, int(x + total_width / 2), y, tcod.BKGND_NONE, tcod.CENTER,
                          "{0}: {1}/{2}".format(name, value, maximum))


def render_messages(panel, message_log):
    """ Render the messages in the message log. """
    y = 1
    for message in message_log.messages:
        tcod.console_set_default_foreground(panel, message.color)
        tcod.console_print_ex(panel, message_log.x, y, tcod.BKGND_NONE, tcod.LEFT, message.text)
        y += 1


def render_inventory(panel, inventory):
    """ Render the player's inventory and its contents. """
    # Draw "INVENTORY" directly above the inventory
    tcod.console_print_ex(panel, 70, 1, tcod.BKGND_NONE, tcod.LEFT, "INVENTORY:")

    # Render each item's symbol
    dx = 0
    for item in inventory:
        if item is None:
            tcod.console_print_ex(panel, 70 + dx, 2, tcod.BKGND_NONE, tcod.LEFT, "  | ")
        else:
            tcod.console_print_ex(panel, 70 + dx, 2, tcod.BKGND_NONE, tcod.LEFT, item.char + " | ")
        dx += 4
