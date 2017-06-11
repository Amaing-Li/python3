import math


# since no base classes are specified, Point is a direct subclass of object
class Point:
    def __init__(self, x=0, y=0):  # the first argument is an object reference to the object itself(called this in C++ an java)
        self.x = x  # all object attributes must be qualified by self
        self.y = y


def distance_from_origin(self):
    return math.hypot(self.x, self.y)


def __eq__(self, other):
    return self.x == other.x and self.y == other.y


def __repr__(self):
    return "Point({0.x!r}, {0.y!r})".format(self)


def __str__(self):
    return "({0.x!r}, {0.y!r})".format(self)










