# Rogue
This is a simple roguelike game designed as a way of getting comfortable with programming basic games and using python-tcod library.

# Running It
Currently the only way to run the game is to clone the repository, install [python-libtcod](https://github.com/libtcod/python-tcod),
and execute ```engine.py```.
An executable file may be added later when the game is in a more finished state and has more "game" to it.

# World Guide
This is a work in progress guide to understanding the game.

## Controls
Up, w: Move up\
Left, a: Move to the left\
Down, s: Move down\
Right, d: Move to the right\
1 thru 5: Use the appropriate inventory slot\
Enter: Toggle fullscreen\
Esc: Exit the game\
g: Generate a new level (preserves player stats)\
r: Reset the game

## Entities
@: You!\
%: Dead you!\
g: A goblin; the most basic enemy\
O: An orc; considerably stronger than a goblin\
!: A health potion\
\*: An Armor upgrade


# Licensing
python-libtcod is distributed under the [Simplified 2-clause FreeBSD license](https://github.com/MikeChunko/Rogue/blob/master/LICENSE.txt).
