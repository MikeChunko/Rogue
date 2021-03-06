# File name: engine.py
# Author: Michael Chunko
# Python Version: 3.7

# This file contains the main engine of the game
from game_messages import MessageLog, Message
from input_handling import *
from render import *
from map_objects.game_map import GameMap
from generate import generate_all
from fov_functions import *
from game_states import GameStates
import entities.entity as enty
from entities.player import Player

# Maximum supported values: Actual monitor width or height // 10
screen_width, screen_height = 100, 70

bar_width = 20
panel_height = 7
panel_y = screen_height - panel_height

map_width, map_height = screen_width, screen_height - panel_height

message_x = bar_width + 2
message_width = screen_width - bar_width + 2
message_height = panel_height - 1

min_room_size, max_room_size = 10, 25
max_rooms = 15

# Minimum and maximum NPCs that can be generated per room
min_npcs, max_npcs = 1, 5

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
    "hp potion": tcod.Color(200, 10, 55),
    "stairs": tcod.gray,
    "player": tcod.white
}

# [hp, defense, power, max starting xp, starting level]
player_stats = [10, 0, 2, 10, 1]

entities = []

max_fps = 30

# Starts the game with several debug features when True
debug = True


def main():
    # Limit the FPS
    tcod.sys_set_fps(max_fps)

    # Set the font to be used
    tcod.console_set_custom_font('terminal8x8_gs_as.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_ASCII_INCOL)

    # Create the screen
    tcod.console_init_root(screen_width, screen_height, 'Rogue', False)

    con = tcod.console_new(screen_width, screen_height)
    panel = tcod.console_new(screen_width, screen_height)

    # Generate the tile map
    game_map = GameMap(map_width, map_height)

    # Initialize the player and the entities list
    player = Player(player_stats[0], player_stats[1], player_stats[2], player_stats[3], player_stats[4], game_map.tiles,
                    screen_width // 2, screen_height // 2, '@', colors.get("player"), "player", True)
    entities.append(player)

    # Represents the current dungeon floor
    floor_number = 1

    # Generate the rest of the game map
    generate_all(game_map, map_width, map_height, max_rooms, min_room_size, max_room_size, min_npcs, max_npcs, colors,
                 entities, floor_number)

    # Initialize user input
    key = tcod.Key()
    mouse = tcod.Mouse()

    # Initialize the game state
    game_state = GameStates.PLAYER_TURN

    # Initialize the message log
    message_log = MessageLog(message_x, message_width, message_height)

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
        render_all(con, panel, message_log, entities, game_map, fov_map, fov_recalculate, screen_width, screen_height,
                   bar_width,
                   panel_height, panel_y, debug)
        fov_recalculate = False

        # Apply the updates on screen
        tcod.console_flush()

        # Clear the entities in preparation for updates
        clear_all(con, entities)

        # Handle key presses
        action = handle_keys(key)

        move = action.get("move")
        use = action.get("use")
        exit = action.get("exit")
        fullscreen = action.get("fullscreen")
        reset = action.get("reset")
        regenerate = action.get("regenerate")

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

        if use and game_state == GameStates.PLAYER_TURN:
            if player.inventory[use - 1] is not None:
                player_turn_results.extend(player.inventory[use - 1].use(entities))

        if exit:
            return True

        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

        if reset:  # Reset the game
            player, game_state, regen_values = reset_map(game_map, map_width, map_height, max_rooms, min_room_size,
                                                         max_room_size, min_npcs, max_npcs, colors, entities, message_x,
                                                         message_width, message_height)
            game_map, fov_recalculate, fov_map, message_log = regen_values

        if regenerate and debug:  # Properly generate a new game map
            game_map, fov_recalculate, fov_map, message_log = regenerate_map(player, map_width, map_height, max_rooms,
                                                                             min_room_size, max_room_size, min_npcs,
                                                                             max_npcs, colors, entities, floor_number,
                                                                             message_x, message_width, message_height)

        # Handle the player turn results
        for result in player_turn_results:
            dead_attacker = result.get("dead")

            if dead_attacker:
                message_log.add_message(Message("You have killed the {0}".format(dead_attacker.name)))
                dead_attacker.kill(game_map.tiles)

                message_log.add_message(Message("{0} XP granted".format(dead_attacker.xp)))
                level_up = player.add_xp(dead_attacker.xp).get("level up")

                if level_up:
                    message_log.add_message(Message("You reached level {0}".format(level_up[0])))
                    message_log.add_message(Message(level_up[1]))
                entities.remove(dead_attacker)

            damaged_entity = result.get("damaged")

            if damaged_entity:
                message_log.add_message(
                    Message("You attacked the {0} for {1} damage".format(damaged_entity[0], damaged_entity[1])))

            pickup_used = result.get("pickup_used")

            if pickup_used:
                message_log.add_message(Message(pickup_used[0]))
                if pickup_used[1].deletes:
                    pickup_used[1].delete(player)

            next_floor = result.get("next_floor")

            if next_floor:
                message_log.add_message(Message("You have advanced to floor {0}".format(next_floor + 1)))
                floor_number += 1
                game_map, fov_recalculate, fov_map, null = regenerate_map(player, map_width, map_height,
                                                                          max_rooms, min_room_size,
                                                                          max_room_size, min_npcs, max_npcs,
                                                                          colors, entities, floor_number,
                                                                          message_x, message_width,
                                                                          message_height, preserve_messages=True)

        # Enemy turn (really every entity that is not the player)
        if game_state == GameStates.ENEMY_TURN:
            enemy_turn_results = enty.entity_turn(entities, fov_map, game_map)
            game_state = GameStates.PLAYER_TURN

            # Handle the entity turn results
            for result in enemy_turn_results:
                dead = result.get("dead")

                if dead:
                    game_state = player.kill(game_map.tiles)
                    message_log.add_message(Message("You have died"))
                    message_log.add_message(Message("GAME OVER"))
                    break

                damaged_entity = result.get("damaged")

                if damaged_entity:
                    message_log.add_message(
                        Message("The {0} attacked you for {1} damage".format(damaged_entity[0], damaged_entity[1])))

                pickup_failed = result.get("pickup_failed")

                if pickup_failed:
                    message_log.add_message(
                        Message("You cannot pick up the {0} since your inventory is full".format(pickup_failed[0])))

                pickup_success = result.get("pickup_success")

                if pickup_success:
                    message_log.add_message(Message("You picked up the {0}".format(pickup_success[0])))
                    pickup_success[1].kill(game_map.tiles)
                    entities.remove(pickup_success[1])

                upgrade_used = result.get("upgrade_used")

                if upgrade_used:
                    message_log.add_message(Message(upgrade_used[0]))
                    message_log.add_message(Message(upgrade_used[1]))
                    upgrade_used[2].kill(game_map.tiles)
                    entities.remove(upgrade_used[2])


def reset_map(game_map, map_width, map_height, max_rooms, min_room_size, max_room_size, min_npcs,
              max_npcs, colors, entities, message_x, message_width, message_height):
    """ Fully resets the game as a whole without closing the window. """
    floor_number = 1
    player = Player(player_stats[0], player_stats[1], player_stats[2], player_stats[3], player_stats[4], game_map.tiles,
                    screen_width // 2, screen_height // 2, '@', colors.get("player"), "player", True)
    return player, GameStates.PLAYER_TURN, regenerate_map(player, map_width, map_height, max_rooms, min_room_size,
                                                          max_room_size, min_npcs, max_npcs, colors, entities,
                                                          floor_number, message_x, message_width, message_height)


def regenerate_map(player, map_width, map_height, max_rooms, min_room_size, max_room_size, min_npcs,
                   max_npcs, colors, entities, floor_number, message_x, message_width, message_height,
                   preserve_messages=False):
    """ Fully resets the game map without closing the window. """
    # Reinitialize the tile map
    game_map = GameMap(map_width, map_height)

    # Remove all entities except the player
    entities.clear()
    entities.append(player)

    # Generate a new game map
    generate_all(game_map, map_width, map_height, max_rooms, min_room_size, max_room_size, min_npcs, max_npcs,
                 colors, entities, floor_number)

    # Reset the message log
    if not preserve_messages:
        message_log = MessageLog(message_x, message_width, message_height)
    else:
        message_log = None

    # Set up the fov_map for the new game map and recalculate it
    fov_recalculate = True
    fov_map = initialize_fov(game_map)

    return game_map, fov_recalculate, fov_map, message_log


if __name__ == "__main__":
    main()
