# File name: game_map.py
# Author: Michael Chunko
# Python Version: 3.7

# This file contains the class representing the array of tiles that is the game map

from map_objects.tile import *


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.create_tiles()

    def create_tiles(self):
        """ Return a 2d array consisting of width x height Tile objects.
            The Tiles are set to be blocked by default. """
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def is_blocked(self, x, y):
        return self.tiles[x][y].blocked
