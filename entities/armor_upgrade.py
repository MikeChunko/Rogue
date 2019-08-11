# File name: armor_upgrade.py
# Author: Michael Chunko
# Python Version: 3.7

# This file contains the class representing an armor upgrade pickup

from entities.pickup import Pickup
import tcod


class ArmorUpgrade(Pickup):
    def __init__(self, tiles, x=1, y=1, char='*', color=tcod.light_blue, name="armor upgrade", blocks=False,
                 moves=False, deletes=True, stat_increase=0.5):
        Pickup.__init__(self, tiles, x, y, char, color, name, blocks, moves, deletes)
        self.stat_increase = stat_increase

    def use(self, entities):
        """ Performs the use action for the item. """
        message_1 = "You found a new armor piece"
        message_2 = "Your defense has increase by {0}".format(self.stat_increase)
        entities[0].defense += self.stat_increase

        return [{"upgrade_used": [message_1, message_2, self]}]

    def take_turn(self, entities, fov_map, game_map):
        """ Checks if the player is on top of it and, if so, performs the code to obtain the item. """
        result = []

        # The player is on the same tile as the item
        if entities[0].x == self.x and entities[0].y == self.y:
            result = self.use(entities)

        return result
