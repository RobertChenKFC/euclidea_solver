from math import sqrt
from random import random

THRESH = 1e-6
THRESH_SQ = 1e-12
RAND_RANGE = 1e3

class Point:
    def __init__(self, x=None, y=None):
        if x is None or y is None:
            self.x = random() * RAND_RANGE
            self.y = random() * RAND_RANGE
        else:
            self.x = x
            self.y = y

    def __hash__(self):
        return id(self)

    def get_coords(self):
        return self.x, self.y

    def dot(self, p):
        return self.x * p.x + self.y * p.y

    def mag_sq(self):
        return self.dot(self)

    def mag(self):
        return sqrt(self.mag_sq())

    def dist_sq(self, p):
        return (self - p).mag_sq()

    def dist(self, p):
        return (self - p).mag()

    def __str__(self):
        return f"Point({self.x}, {self.y})"

    __repr__ = __str__

    def __add__(self, p):
        return Point(self.x + p.x, self.y + p.y)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __sub__(self, p):
        return self + (-p)

    def __mul__(self, m):
        return Point(m * self.x, m * self.y)

    __rmul__ = __mul__

    def __truediv__(self, m):
        return Point(self.x / m, self.y / m)

    def __pow__(self, n):
        return Point(self.x ** n, self.y ** n)

    def is_close_to(self, p):
        return self.dist_sq(p) < THRESH_SQ

    def is_parallel_to(self, p):
        m1, m2 = self.mag(), p.mag()
        if m1 == 0 or m2 == 0:
            return True
        return abs(1 - abs(self.dot(p)) / (m1 * m2)) < THRESH
