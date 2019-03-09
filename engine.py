# File name: engine.py
# Author: Michael Chunko
# Python Version: 3.7

# This file contains the main engine of the game

from input_handling import *
from render import *
from map_objects.game_map import *
from fov_functions import *

# Maximum supported values: Actual monitor width or height // 10
screen_width, screen_height = 100, 70
map_width, map_height = screen_width, screen_height

max_room_size, min_room_size = 25, 5
max_rooms = 15

# Minimum and maximum NPCs that can be generated per room
min_npcs, max_npcs = 1, 5

# Permissive FOV algorithm
fov_algorithm = 0
fov_light_walls = True
fov_radius = 30

colors = {
    "dark wall": tcod.Color(80, 30, 5),
    "dark ground": tcod.Color(40, 20, 5),
    "light wall": tcod.Color(100, 50, 10),
    "light ground": tcod.Color(60, 25, 10),
    "unseen": tcod.Color(25, 25, 40),
    "goblin": tcod.Color(10, 150, 10),
    "orc": tcod.Color(10, 130, 80),
}

max_fps = 30


def main():
    # Limit the FPS
    tcod.sys_set_fps(max_fps)

    # Set the font to be used
    tcod.console_set_custom_font('terminal8x8_gs_as.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_ASCII_INCOL)

    # Create the screen
    tcod.console_init_root(screen_width, screen_height, 'Rogue', False)

    con = tcod.console_new(screen_width, screen_height)

    # Generate the tile map
    game_map = GameMap(map_width, map_height)

    # Initialize entities
    player = Entity(game_map.tiles, screen_width // 2, screen_height // 2, '@', tcod.white)
    entities = [player]

    # Generate the rest of the game map
    game_map.make_map(max_rooms, min_room_size, max_room_size, map_width, map_height, player)
    game_map.create_npcs(min_npcs, max_npcs, entities, colors)

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
                player.move(game_map.tiles, dx, dy)
                fov_recalculate = True

        if exit:
            return True

        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())


if __name__ == "__main__":
    main()
