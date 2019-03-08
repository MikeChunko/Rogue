# File name: engine.py
# Author: Michael Chunko
# Python Version: 3.7

# This file contains the main engine of the game

from input_handling import *
from entity import *
from render import *
from map_objects.game_map import *
from fov_functions import *

screen_width, screen_height = 100, 70
map_width, map_height = screen_width, screen_height

max_room_size = 25
min_room_size = 5
max_rooms = 10

# Permissive FOV algorithm
fov_algorithm = 0
fov_light_walls = True
fov_radius = 30

colors = {
    "dark wall": tcod.Color(35, 70, 35),
    "dark ground": tcod.Color(30, 60, 30),
    "light wall": tcod.Color(0, 100, 0),
    "light ground": tcod.Color(50, 150, 50),
    "unseen": tcod.Color(30, 30, 60)
}


def main():
    # Initialize entities
    player = Entity(screen_width // 2, screen_height // 2, '@', tcod.white)
    npc = Entity(color=tcod.red)
    entities = [npc, player]

    tcod.sys_set_fps(30)

    # Set the font to be used
    tcod.console_set_custom_font('terminal8x8_gs_as.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_ASCII_INCOL)

    # Create the screen
    tcod.console_init_root(screen_width, screen_height, 'Rogue', False)

    con = tcod.console_new(screen_width, screen_height)

    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, min_room_size, max_room_size, map_width, map_height, player)
    game_map.create_npcs(min_npcs=10, max_npcs=20, entities=entities)

    key = tcod.Key()
    mouse = tcod.Mouse()

    # Determine whether or not the FOV needs to be recalculated
    fov_recalculate = True
    fov_map = initialize_fov(game_map)

    # Game loop
    while not tcod.console_is_window_closed():
        # Update key and mouse with the user inputs
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)

        if fov_recalculate:
            calculate_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

        # Render everything
        render_all(con, entities, game_map, fov_map, fov_recalculate, screen_width, screen_height)
        fov_recalculate = False

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
                fov_recalculate = True

        if exit:
            return True

        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())


if __name__ == "__main__":
    main()
