# File name: attacker.py
# Author: Michael Chunko
# Python Version: 3.7

# This file contains the entity subclass representing those capable of attacking
from entities.entity import Entity
import tcod


class Attacker(Entity):
    def __init__(self, hp, defense, power, tiles, x=1, y=1, char='#', color=tcod.white, name="none", blocks=True,
                 moves=True):
        Entity.__init__(self, tiles, x, y, char, color, name, blocks, moves)
        self.hp = hp
        self.defense = defense
        self.power = power

    def take_turn(self, entities, fov_map, game_map):
        """ The entity takes their turn in the game. """
        player = entities[0]
        distance = self.distance_to(player)
        if distance <= 1:
            self.attack(player)
        elif self.moves and (tcod.map_is_in_fov(fov_map, self.x, self.y) or distance <= 7):
            self.move_towards(player.x, player.y, game_map)

    def attack(self, target):
        print(target.name + " is attacked by a vicious " + self.name)
