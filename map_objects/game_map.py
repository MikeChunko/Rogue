# File name: game_map.py
# Author: Michael Chunko
# Python Version: 3.7

# This file contains the class representing the array of tiles that is the game map

from map_objects.tile import *
from map_objects.rectangle import Rectangle
from entities.attacker import Attacker
from entities.entity import get_entity_at_location
from random import randint

# Known Issue: if you somehow get out of the map, the game crashes

rooms = []

monster_stats = {
    "orc": (8, 1, 3),
    "goblin": (3, 0, 1)
}


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

    def make_map(self, max_rooms, min_room_size, max_room_size, map_width, map_height, entities):
        """ Procedurally generate a map consisting of rooms and tunnels connecting them. """
        player = entities[0]
        room_count = 0

        for r in range(max_rooms):
            width = randint(min_room_size, max_room_size)
            height = randint(min_room_size, max_room_size)

            # Make sure that the starting coordinates aren't outside the map
            x = randint(0, map_width - width - 1)
            y = randint(0, map_height - height - 1)

            new_room = Rectangle(x, y, width, height)

            for other in rooms:
                # End if new_room intersects with any rooms
                if new_room.intersect(other):
                    break
            else:
                self.create_room(new_room)
                new_x, new_y = new_room.center()

                if room_count == 0:
                    # Place the player in the center of the first room
                    player.move_to(self.tiles, new_x, new_y)
                else:
                    # Not the first room
                    prev_x, prev_y = rooms[-1].center()

                    if randint(0, 1) == 1:
                        self.create_tunnel(prev_x, new_x, prev_y, 'h', entities)
                        self.create_tunnel(prev_y, new_y, new_x, 'v', entities)
                    else:
                        self.create_tunnel(prev_y, new_y, prev_x, 'v', entities)
                        self.create_tunnel(prev_x, new_x, new_y, 'h', entities)

                rooms.append(new_room)
                room_count += 1

    def create_room(self, room):
        """ Make the tiles in room unblocked and see-through.
            The "+ 1" is because (x1, y1) should be a wall. """
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_tunnel(self, start, end, location, direction, entities):
        """ Make a "tunnel" of tiles 1-thick that are unblocked and see-through.
            Input location: The x/y coordinate to make the tunnel at
            Input direction: h = horizontal
                             v = vertical. """
        if direction == "h":
            for x in range(min(start, end), max(start, end) + 1):
                if get_entity_at_location(x, location, entities) == -1:
                    self.tiles[x][location].blocked = False
                    self.tiles[x][location].block_sight = False
        elif direction == "v":
            for y in range(min(start, end), max(start, end) + 1):
                if get_entity_at_location(location, y, entities) == -1:
                    self.tiles[location][y].blocked = False
                    self.tiles[location][y].block_sight = False

    def create_npcs(self, min_npcs, max_npcs, entities, colors):
        for room in rooms:
            for i in range(0, randint(min_npcs, max_npcs)):
                x = y = 0

                # Don't spawn on a blocked tile or on a player
                while self.tiles[x][y].blocked:
                    x = randint(room.x1 + 1, room.x2 - 1)
                    y = randint(room.y1 + 1, room.y2 - 1)

                # 80% chance to spawn a goblin, otherwise spawn an orc
                # TODO change later
                if randint(0, 100) < 80:
                    hp, defense, power = monster_stats.get("goblin")
                    entities.append(
                        Attacker(hp, defense, power, self.tiles, x, y, "g", colors.get("goblin"), "goblin", True, True))
                else:
                    hp, defense, power = monster_stats.get("orc")
                    entities.append(
                        Attacker(hp, defense, power, self.tiles, x, y, "O", colors.get("orc"), "orc", True, True))

    def is_blocked(self, x, y):
        return self.tiles[x][y].blocked
