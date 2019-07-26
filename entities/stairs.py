# File name: stairs.py
# Author: Michael Chunko
# Python Version: 3.7

# This file contains the entity subclass representing stairs used for advancing to the next floor
from entities.entity import Entity
import tcod


class Stairs(Entity):
    def __init__(self, floor, tiles, x=1, y=1, char='/', color=tcod.gray, name="none", blocks=True,
                 moves=True):
        Entity.__init__(self, tiles, x, y, char, color, name, blocks, moves)
        self.floor = floor

    def next_floor(self):
        return [{"next_floor": self.floor}]

    # Ensures the stairs do not move
    def take_turn(self, entities, fov_map, game_map):
        pass
