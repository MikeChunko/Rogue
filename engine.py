# File name: engine.py
# Author: Michael Chunko
# Python Version: 3.7

# This file contains the main engine of the game

from input_handling import *
from render import *
from map_objects.game_map import GameMap
from generate import generate_all
from fov_functions import *
from game_states import GameStates
import entities.entity as enty
from entities.attacker import Attacker

# Maximum supported values: Actual monitor width or height // 10
screen_width, screen_height = 100, 70
map_width, map_height = screen_width, screen_height

min_room_size, max_room_size = 10, 25
max_rooms = 15

# Minimum and maximum NPCs that can be generated per room
min_npcs, max_npcs = 1, 6

# Permissive FOV algorithm
fov_algorithm = 0
fov_light_walls = True
fov_radius = 30

colors = {
    "dark wall": tcod.Color(50, 20, 5),
    "dark ground": tcod.Color(30, 15, 5),
    "light wall": tcod.Color(100, 50, 10),
    "light ground": tcod.Color(55, 25, 10),
    "unseen": tcod.Color(20, 20, 30),
    "goblin": tcod.Color(10, 150, 10),
    "orc": tcod.Color(10, 130, 80),
}

entities = []

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

    # Initialize the player and the entities list
    player = Attacker(10, 0, 2, game_map.tiles, screen_width // 2, screen_height // 2, '@', tcod.white, "player", True,
                      False)
    entities.append(player)

    # Generate the rest of the game map
    generate_all(game_map, map_width, map_height, max_rooms, min_room_size, max_room_size, min_npcs, max_npcs, colors,
                 entities)

    # Initialize user input
    key = tcod.Key()
    mouse = tcod.Mouse()

    # Initialize the game state
    game_state = GameStates.PLAYER_TURN

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

        player_turn_results = []

        if move and game_state == GameStates.PLAYER_TURN:
            dx, dy = move
            if not game_map.is_blocked(player.x + dx, player.y + dy):
                player.move(game_map.tiles, dx, dy)
                fov_recalculate = True

            target = enty.get_entity_at_location(player.x + dx, player.y + dy, entities)

            if target != -1:
                player_turn_results.extend(player.attack(target))

            game_state = GameStates.ENEMY_TURN

        if exit:
            return True

        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

        # Handle the player turn results
        for result in player_turn_results:
            dead_entity = result.get("dead")

            if dead_entity:
                print("You have killed the {0}".format(dead_entity.name))
                dead_entity.kill(game_map.tiles)
                entities.remove(dead_entity)

        if game_state == GameStates.ENEMY_TURN:
            enemy_turn_results = enty.entity_turn(entities, fov_map, game_map)
            game_state = GameStates.PLAYER_TURN

            for result in enemy_turn_results:
                dead = result.get("dead")

                if dead:
                    # TODO: Improve player death
                    game_state = GameStates.GAME_OVER
                    print("\n\nYou have died\n\nGAME\nOVER")
                    entities[0].char = "%"
                    entities[0].color = tcod.Color(150, 0, 0)
                    break
            print()


if __name__ == "__main__":
    main()
