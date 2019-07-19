# File name: attacker.py
# Author: Michael Chunko
# Python Version: 3.7

# This file contains the entity subclass representing those capable of attacking
from entities.entity import Entity
import tcod


class Attacker(Entity):
    def __init__(self, hp, defense, power, xp, tiles, x=1, y=1, char='#', color=tcod.white, name="none", blocks=True,
                 moves=True):
        Entity.__init__(self, tiles, x, y, char, color, name, blocks, moves)
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
        self.xp = xp

    def take_turn(self, entities, fov_map, game_map):
        """ The entity takes their turn in the game. """
        result = {}
        player = entities[0]
        distance = self.distance_to(player)
        if distance <= 1:
            result = self.attack(player)
        elif self.moves and (tcod.map_is_in_fov(fov_map, self.x, self.y) or distance <= 7):
            self.move_towards(player.x, player.y, game_map)

        return result

    def take_damage(self, damage):
        self.hp -= damage

        if self.hp <= 0:
            return [{"dead": self}]

        return []

    def attack(self, target):
        damage = self.power - target.defense

        if damage < 0:
            damage = 0

        results = [{"damaged": [self.name, damage]}]
        results.extend(target.take_damage(damage))
        return results

    def __repr__(self):
        return "{0}: hp = {1}, defense = {2}, power = {3}".format(self.name, self.hp, self.defense, self.power)
