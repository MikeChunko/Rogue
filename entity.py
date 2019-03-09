# File name: entity.py
# Author: Michael Chunko
# Python Version: 3.7

# This file contains the class representing entities

import tcod


class Entity:
    def __init__(self, tiles, x=1, y=1, char='#', color=tcod.white):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        tiles[self.x][self.y].blocked = True

    def move(self, tiles, dx, dy):
        tiles[self.x][self.y].blocked = False
        self.x += dx
        self.y += dy
        tiles[self.x][self.y].blocked = True
