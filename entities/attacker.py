# File name: attacker.py
# Author: Michael Chunko
# Python Version: 3.7

# This file contains the entity subclass representing those capable of attacking
from entities.entity import Entity
import tcod


class Attacker(Entity):
    def __init__(self, hp, defense, power, tiles, x=1, y=1, char='#', color=tcod.white, name="none", blocks=False,
                 moves=True):
        Entity.__init__(tiles, x, y, char, color, name, blocks, moves)
        self.hp = hp
        self.defense = defense
        self.power = power
