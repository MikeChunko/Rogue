# Author: Michael Chunko
# Python Version: 3.7

# Represents a rectangle-shaped room


class Rectangle:
    def __init__(self, x, y, width, height):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    def center(self):
        """ Return the (x, y) coordinates corresponding to the center of the rectangle. """
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        return center_x, center_y

    def intersect(self, other):
        """ Return True if the rectangle intersects with other. """
        return self.x1 <= other.x2 and self.x2 >= other.x1 and self.y1 <= other.y2 and self.y2 >= other.y1
