# Author: Michael Chunko
# Python Version: 3.7

# Represents a rectangle-shaped room

class Rectangle:
    def __init__(self, x, y, width, height):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
