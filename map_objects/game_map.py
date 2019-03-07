# File name: game_map.py
# Author: Michael Chunko
# Python Version: 3.7

# This file contains the class representing the array of tiles that is the game map

from map_objects.tile import *
from map_objects.rectangle import Rectangle


# Known Issue: if you somehow get out of the map, the game crashes

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.create_tiles()

    def create_tiles(self):
        """ Return a 2d array consisting of width x height Tile objects.
            The Tiles are set to be blocked by default. """
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]
        tiles[20][20].blocked = True
        return tiles

    def make_map(self):
        room1 = Rectangle(20, 15, 10, 15)
        room2 = Rectangle(35, 15, 10, 15)

        self.create_room(room1)
        self.create_room(room2)

    def create_room(self, room):
        """ Make the tiles in room unblocked and see-through.
            The "+ 1" is because (x1, y1) should be a wall. """
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def is_blocked(self, x, y):
        return self.tiles[x][y].blocked
