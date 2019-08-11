# File name: game_map.py
# Author: Michael Chunko
# Python Version: 3.7

# This file contains functions used in generating the map

from map_objects.rectangle import Rectangle
from entities.attacker import Attacker
from entities.health_potion import HealthPotion
from entities.armor_upgrade import ArmorUpgrade
from entities.stairs import Stairs
from entities.entity import get_entity_at_location
from random import randint

# (hp, defense, power, xp value)
monster_stats = {
    "orc": (5, 1, 2, 3),
    "goblin": (3, 0, 1, 1)
}

rooms = []


def generate_all(game_map, map_width, map_height, max_rooms, min_room_size, max_room_size, min_npcs, max_npcs,
                 colors, entities, floor_number):
    """ Generate the whole game floor, rooms and entities included. """
    rooms.clear()
    make_map(game_map, map_width, map_height, max_rooms, min_room_size, max_room_size, entities)
    create_entities(game_map, min_npcs, max_npcs, entities, colors, floor_number)


def make_map(game_map, map_width, map_height, max_rooms, min_room_size, max_room_size, entities):
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
            create_room(game_map, new_room)
            new_x, new_y = new_room.center()

            if room_count == 0:
                # Place the player in the center of the first room
                player.move_to(game_map.tiles, new_x, new_y)
            else:
                # Not the first room
                prev_x, prev_y = rooms[-1].center()

                if randint(0, 1) == 1:
                    create_tunnel(game_map, prev_x, new_x, prev_y, 'h', entities)
                    create_tunnel(game_map, prev_y, new_y, new_x, 'v', entities)
                else:
                    create_tunnel(game_map, prev_y, new_y, prev_x, 'v', entities)
                    create_tunnel(game_map, prev_x, new_x, new_y, 'h', entities)

            rooms.append(new_room)
            room_count += 1


def create_room(game_map, room):
    """ Make the tiles in a room unblocked and see-through.
        The "+ 1" is because (x_1, y_1) should be a wall. """
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            game_map.tiles[x][y].blocked = False
            game_map.tiles[x][y].block_sight = False


def create_tunnel(game_map, start, end, location, direction, entities):
    """ Make a "tunnel" of tiles 1-thick that are unblocked and see-through.
        Input location: The x/y coordinate to make the tunnel at
        Input direction: h = horizontal
                         v = vertical. """
    if direction == "h":
        for x in range(min(start, end), max(start, end) + 1):
            if get_entity_at_location(x, location, entities) == -1:
                game_map.tiles[x][location].blocked = False
                game_map.tiles[x][location].block_sight = False
    elif direction == "v":
        for y in range(min(start, end), max(start, end) + 1):
            if get_entity_at_location(location, y, entities) == -1:
                game_map.tiles[location][y].blocked = False
                game_map.tiles[location][y].block_sight = False


def create_entities(game_map, min_npcs, max_npcs, entities, colors, floor_number):
    """ Generate [min_npcs, max_npcs] entities in every room.
        The entity may either be an enemy or an item. """
    stairs_generated = False

    for room in rooms:
        for i in range(0, randint(min_npcs, max_npcs)):
            x = y = 0

            # Don't spawn on a blocked tile or on a player
            while game_map.tiles[x][y].blocked:
                x = randint(room.x1 + 1, room.x2 - 1)
                y = randint(room.y1 + 1, room.y2 - 1)

            # Generates the stairs in a room away from the player
            if rooms[0] != room and not stairs_generated:
                entities.append(Stairs(floor_number, game_map.tiles, x, y))
                stairs_generated = True
            else:
                # 80% chance to spawn an enemy, 20% for an item
                random_number = randint(0, 100)
                if random_number < 80:
                    create_enemies(game_map, entities, colors, x, y)
                else:
                    create_items(game_map, entities, x, y)


def create_enemies(game_map, entities, colors, x, y):
    """ Generate an enemy at the given (x, y) coordinate. """
    # 85% chance for a goblin, 15% for an orc
    random_number = randint(0, 100)
    if random_number < 85:  # goblin
        hp, defense, power, xp = monster_stats.get("goblin")
        entities.append(
            Attacker(hp, defense, power, xp, game_map.tiles, x, y, "g", colors.get("goblin"), "goblin"))
    else:  # orc
        hp, defense, power, xp = monster_stats.get("orc")
        entities.append(
            Attacker(hp, defense, power, xp, game_map.tiles, x, y, "O", colors.get("orc"), "orc"))


def create_items(game_map, entities, x, y):
    """ Generate an item at the given (x, y) coordinate. """
    # 95% chance for a HP potion, 5% for an armor upgrade
    random_number = randint(0, 100)
    if random_number < 95:  # HP potion
        entities.append(HealthPotion(game_map.tiles, x, y))
    else:  # armor upgrade
        entities.append(ArmorUpgrade(game_map.tiles, x, y))
