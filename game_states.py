# File name: game_states.py
# Author: Michael Chunko
# Python Version: 3.7

# This file contains the class representing the possible game states

from enum import Enum


class GameStates(Enum):
    PLAYER_TURN = 0
    ENEMY_TURN = 1
    GAME_OVER = 2
