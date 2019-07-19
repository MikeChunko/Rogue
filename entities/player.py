# File name: player.py
# Author: Michael Chunko
# Python Version: 3.7

# This file contains the attacker subclass representing the player character
from entities.attacker import Attacker
import tcod
from game_states import GameStates


class Player(Attacker):
    def __init__(self, hp, defense, power, max_xp, level, tiles, x=1, y=1, char='#', color=tcod.white, name="none",
                 blocks=True):
        Attacker.__init__(self, hp, defense, power, 0, tiles, x, y, char, color, name, blocks, moves=True)
        self.inventory = []
        self.inventory_size = 5
        for i in range(0, self.inventory_size):
            self.inventory.append(None)

        self.max_xp = max_xp
        self.xp = 0
        self.level = level

    def attack(self, target):
        if isinstance(target, Attacker):
            damage = self.power - target.defense

            results = [{"damaged": [target.name, damage]}]
            results.extend(target.take_damage(damage))
            return results
        return []

    def add_xp(self, dxp):
        """ Gain experience. """
        self.xp += dxp

        # Level up
        if self.xp > self.max_xp:
            self.xp -= self.max_xp
            self.max_xp += 5
            self.level += 1

    def kill(self, tiles):
        """ Do any necessary preparations to kill off the player and present the game over screen. """
        if self.blocks:
            tiles[self.x][self.y].blocked = False

        self.char = "%"
        self.color = tcod.Color(150, 0, 0)

        # Ensures the player never sees a negative HP value
        self.hp = 0

        return GameStates.GAME_OVER
