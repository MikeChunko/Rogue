# File name: render.py
# Author: Michael Chunko
# Python Version: 3.7

# This file contains the functions used to render the screen

import tcod
from engine import colors


def render_all(con, entities, game_map, screen_width, screen_height):
    for y in range(game_map.height):
        for x in range(game_map.width):
            if game_map.tiles[x][y].blocked:
                tcod.console_set_char_background(con, x, y, colors.get("dark wall"), tcod.BKGND_SET)
            else:
                tcod.console_set_char_background(con, x, y, colors.get("dark ground"), tcod.BKGND_SET)

    for entity in entities:
        draw_entity(con, entity)

    tcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity):
    tcod.console_set_default_foreground(con, entity.color)
    tcod.console_put_char(con, entity.x, entity.y, entity.char, tcod.BKGND_NONE)


def clear_entity(con, entity):
    tcod.console_put_char(con, entity.x, entity.y, ' ', tcod.BKGND_NONE)
