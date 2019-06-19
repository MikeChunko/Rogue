# File name: pickup.py
# Author: Michael Chunko
# Python Version: 3.7

# This file contains the class representing items that can be picked up

from entities.entity import Entity
import tcod


class Pickup(Entity):
    def __init__(self, tiles, x=1, y=1, char='-', color=tcod.white, name="item", blocks=False, moves=False,
                 deletes=False):
        Entity.__init__(self, tiles, x, y, char, color, name, blocks, moves)
        self.deletes = deletes

    def use(self, entities):
        """ Performs the use action for the item. """
        message = "You used the {0}. It didn't do much of anything".format(self.name)
        return [{"pickup_used": [message, self]}]

    def delete(self, player):
        """ Remove the item from the player inventory. """
        for i in range(0, player.inventory_size):
            if player.inventory[i] == self:
                player.inventory[i] = None
                break

    def take_turn(self, entities, fov_map, game_map):
        """ Checks if the player is on top of it and, if so, performs the code to obtain the item. """
        result = []

        # The player is on the same tile as the item
        if entities[0].x == self.x and entities[0].y == self.y:

            # Find the index of the first open space in the player inventory
            i = 0
            while i < entities[0].inventory_size and entities[0].inventory[i] is not None:
                i += 1

            if i >= entities[0].inventory_size:
                result = [{"pickup_failed": [self.name]}]
            else:
                result = [{"pickup_success": [self.name, self]}]
                entities[0].inventory[i] = self

        return result
