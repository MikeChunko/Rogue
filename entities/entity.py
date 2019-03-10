# File name: entity.py
# Author: Michael Chunko
# Python Version: 3.7

# This file contains the class representing entities

import math
import tcod


class Entity:
    def __init__(self, tiles, x=1, y=1, char='#', color=tcod.white, name="none", blocks=True, moves=True):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        if self.blocks:
            tiles[self.x][self.y].blocked = True
        self.moves = moves

    def move(self, tiles, dx, dy):
        self.x += dx
        self.y += dy
        if self.blocks:
            tiles[self.x - dx][self.y - dy].blocked = False
            tiles[self.x][self.y].blocked = True

    def move_to(self, tiles, new_x, new_y):
        if self.blocks:
            tiles[self.x][self.y].blocked = False
            tiles[new_x][new_y].blocked = True
        self.x = new_x
        self.y = new_y

    def move_towards(self, target_x, target_y, game_map):
        distance = math.sqrt((target_x - self.x) ** 2 + (target_y - self.y) ** 2)
        dx = int(round((target_x - self.x) / distance))
        dy = int(round((target_y - self.y) / distance))

        if not game_map.is_blocked(self.x + dx, self.y) and not game_map.is_blocked(self.x, self.y + dy):
            if dx > dy:
                self.move(game_map.tiles, dx, 0)
            else:
                self.move(game_map.tiles, 0, dy)
        elif not game_map.is_blocked(self.x + dx, self.y):
            self.move(game_map.tiles, dx, 0)
        elif not game_map.is_blocked(self.x, self.y + dy):
            self.move(game_map.tiles, 0, dy)

    def take_turn(self, entities, fov_map, game_map):
        """ The entity takes their turn in the game. """
        player = entities[0]
        if self.moves and (tcod.map_is_in_fov(fov_map, self.x, self.y) or self.distance_to(player) <= 5):
            self.move_towards(player.x, player.y, game_map)
        else:
            print(self.name + " does nothing")

    def distance_to(self, other):
        return math.sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)


def get_entity_at_location(x, y, entities):
    """ Return the entity at the given x, y coordinates.
        Return -1 if there is no entity at these coordinates."""
    for entity in entities:
        if entity.x == x and entity.y == y:
            return entity

    return -1


def entity_turn(entities, fov_map, game_map):
    """ Make all entities in entities take their turn. """
    # Player should not run take turn
    for enty in entities[1:]:
        enty.take_turn(entities, fov_map, game_map)