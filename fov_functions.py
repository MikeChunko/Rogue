# File name: fov_functions
# Author: Michael Chunko
# Python Version: 3.7

# This file contains various functions used in implementing field of view for the player

import tcod


def initialize_fov(game_map):
    fov_map = tcod.map_new(game_map.width, game_map.height)

    for x in range(game_map.width):
        for y in range(game_map.height):
            tcod.map_set_properties(fov_map, x, y, not game_map.tiles[x][y].block_sight,
                                    not game_map.tiles[x][y].blocked)

    return fov_map


def calculate_fov(fov_map, x, y, radius, light_walls=True, algorithm=0):
    tcod.map_compute_fov(fov_map, x, y, radius, light_walls, algorithm)
