# File name: player.py
# Author: Michael Chunko
# Python Version: 3.7

# This file contains the attacker subclass representing the player character
from entities.attacker import Attacker
import tcod
from game_states import GameStates


class Player(Attacker):
    def __init__(self, hp, defense, power, tiles, x=1, y=1, char='#', color=tcod.white, name="none", blocks=True):
        Attacker.__init__(self, hp, defense, power, tiles, x, y, char, color, name, blocks, moves=True)

    def attack(self, target):
        damage = self.power - target.defense

        if damage > 0:
            print("You attack {0} for {1} damage, leaving them at {2} hp".format(target.name,
                                                                                 damage, target.hp - damage))
            return target.take_damage(damage)
        else:
            print("You attack {0}, but deal no damage".format(target.name))

    def kill(self, tiles):
        """ Do any necessary preparations to kill off the player and present the game over screen. """
        if self.blocks:
            tiles[self.x][self.y].blocked = False

        print("\n\nYou have died\n\nGAME\nOVER")
        self.char = "%"
        self.color = tcod.Color(150, 0, 0)

        return GameStates.GAME_OVER
