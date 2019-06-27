# File name: health_potion.py
# Author: Michael Chunko
# Python Version: 3.7

# This file contains the class representing the health potion item

from entities.pickup import Pickup
import tcod


class HealthPotion(Pickup):
    def __init__(self, tiles, x=1, y=1, char='!', color=tcod.red, name="health potion", blocks=False, moves=False,
                 deletes=True, heal_amount=5):
        Pickup.__init__(self, tiles, x, y, char, color, name, blocks, moves, deletes)
        self.heal_amount = heal_amount

    def use(self, entities):
        """ Performs the use action for the item. """
        message = "You used the {0}. It healed for {1} HP".format(self.name, self.heal_amount)
        entities[0].hp += self.heal_amount
        if entities[0].hp > entities[0].max_hp:
            entities[0].hp = entities[0].max_hp

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
