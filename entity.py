# File name: entity.py
# Author: Michael Chunko
# Python Version: 3.7

# This file contains the class representing entities

import tcod


class Entity:
    def __init__(self, tiles, x=1, y=1, char='#', color=tcod.white, name="none", blocks=False):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        if self.blocks:
            tiles[self.x][self.y].blocked = True

    def move(self, tiles, dx, dy):
        if self.blocks:
            tiles[self.x][self.y].blocked = False
        self.x += dx
        self.y += dy
        if self.blocks:
            tiles[self.x][self.y].blocked = True


def get_entity_at_location(x, y, entities):
    """ Return the entity at the given x, y coordinates.
        Return -1 if there is no entity at these coordinates."""
    for entity in entities:
        if entity.x == x and entity.y == y:
            return entity

    return -1
