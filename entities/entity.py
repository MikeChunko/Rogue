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
        """ Move the entity to the location (x + dx, x + dy). """
        self.x += dx
        self.y += dy
        if self.blocks:
            tiles[self.x - dx][self.y - dy].blocked = False
            tiles[self.x][self.y].blocked = True

    def move_to(self, tiles, new_x, new_y):
        """ Move the entity directly to the location (new_x, new_y). """
        if self.blocks:
            tiles[self.x][self.y].blocked = False
            tiles[new_x][new_y].blocked = True
        self.x = new_x
        self.y = new_y

    def move_towards(self, target_x, target_y, game_map):
        """ Move the entity 1 tile towards the target. """
        distance = math.sqrt((target_x - self.x) ** 2 + (target_y - self.y) ** 2)
        dx = round((target_x - self.x) / distance)
        dy = round((target_y - self.y) / distance)

        if dx == 0:
            if target_x - self.x > 0:
                dx = 1
            elif target_x - self.x < 0:
                dx = -1

        if dy == 0:
            if target_y - self.y > 0:
                dy = 1
            elif target_y - self.y < 0:
                dy = -1

        if not game_map.is_blocked(self.x + dx, self.y) and not game_map.is_blocked(self.x, self.y + dy):
            if dx > dy:
                self.move(game_map.tiles, dx, 0)
            else:
                self.move(game_map.tiles, 0, dy)
        elif not game_map.is_blocked(self.x + dx, self.y):
            self.move(game_map.tiles, dx, 0)
        elif not game_map.is_blocked(self.x, self.y + dy):
            self.move(game_map.tiles, 0, dy)

    def kill(self, tiles):
        """ Do any necessary preparations to cleanly remove the entity from the game. """
        if self.blocks:
            tiles[self.x][self.y].blocked = False

    def take_turn(self, entities, fov_map, game_map):
        """ The entity takes their turn in the game. """
        player = entities[0]
        if self.moves and (tcod.map_is_in_fov(fov_map, self.x, self.y) or self.distance_to(player) <= 5):
            self.move_towards(player.x, player.y, game_map)

    def distance_to(self, other):
        return math.sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)

    def __repr__(self):
        return "{0}: x = {1}, y = {2}".format(self.name, self.x, self.y)


def get_entity_at_location(x, y, entities):
    """ Return the entity at the given x, y coordinates.
        Return -1 if there is no entity at these coordinates."""
    for entity in entities:
        if entity.x == x and entity.y == y:
            return entity

    return -1


def entity_turn(entities, fov_map, game_map):
    """ Make all entities in entities take their turn. """
    turn_results = []

    # Player turn should not be calculated
    for enty in entities[1:]:
        result = enty.take_turn(entities, fov_map, game_map)

        if result is not None:
            turn_results.extend(result)

    return turn_results
