# File name: tile.py
# Author: Michael Chunko
# Python Version: 3.7

# This file contains the class representing a tile on a map


class Tile:
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked

        # By default, a blocked tile also blocks sight
        if block_sight is None:
            self.block_sight = blocked
        else:
            self.block_sight = blocked
