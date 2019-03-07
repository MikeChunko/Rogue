# File name: engine.py
# Author: Michael Chunko
# Python Version: 3.7

# This file contains the main engine of the game

import tcod
from input_handling import *
from entity import *
from render import *
from map_objects.game_map import *

screen_width = 80
screen_height = 50
map_width = 80
map_height = 50

max_room_size = 12
min_room_size = 5
max_rooms = 10

colors = {
    "dark wall": tcod.Color(0, 100, 0),
    "dark ground": tcod.Color(50, 150, 50)
}


def main():
    # Initialize entities
    player = Entity(screen_width // 2, screen_height // 2, '@', tcod.white)
    npc = Entity(color=tcod.red)
    entities = [npc, player]

    # Set the font to be used
    tcod.console_set_custom_font('terminal8x8_gs_as.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_ASCII_INCOL)

    # Create the screen
    tcod.console_init_root(screen_width, screen_height, 'Rogue', False)

    con = tcod.console_new(screen_width, screen_height)

    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, min_room_size, max_room_size, map_width, map_height, player)

    key = tcod.Key()
    mouse = tcod.Mouse()

    # Game loop
    while not tcod.console_is_window_closed():
        # Update key and mouse with the user inputs
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)

        tcod.console_set_default_foreground(con, tcod.white)

        # Print the entities
        render_all(con, entities, game_map, screen_width, screen_height)

        # Apply the updates on screen
        tcod.console_flush()

        # Clear the entities in preparation for updates
        clear_all(con, entities)

        # Handle key presses
        action = handle_keys(key)

        move = action.get("move")
        exit = action.get("exit")
        fullscreen = action.get("fullscreen")

        if move:
            dx, dy = move
            if not game_map.is_blocked(player.x + dx, player.y + dy):
                player.move(dx, dy)

        if exit:
            return True

        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())


if __name__ == "__main__":
    main()
