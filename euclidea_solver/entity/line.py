from math import sqrt
from euclidea_solver.entity.point import Point, THRESH

class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __hash__(self):
        return id(self)

    def get_coords(self):
        return self.p1.x, self.p1.y, self.p2.x, self.p2.y

    def intersect(self, obj):
        from euclidea_solver.entity.circle import Circle

        if isinstance(obj, Line):
            x1, y1, x2, y2 = self.get_coords()
            x3, y3, x4, y4 = obj.get_coords()
            dx1, dy1 = x2 - x1, y2 - y1
            dx2, dy2 = x4 - x3, y4 - y3
            dx3, dy3 = x3 - x1, y3 - y1
            t = dx1 * dy2 - dx2 * dy1
            if t == 0:
                return []
            t = (dx3 * dy2 - dx2 * dy3) / t
            return [Point(x1 + dx1 * t, y1 + dy1 * t)]
        elif isinstance(obj, Circle):
            x1, y1, x2, y2 = self.get_coords()
            x3, y3, x4, y4 = obj.get_coords()
            dx1, dy1 = x2 - x1, y2 - y1
            dx2, dy2 = x1 - x3, y1 - y3
            a = dx1 * dx1 + dy1 * dy1
            b = 2 * (dx1 * dx2 + dy1 * dy2)
            c = dx2 * dx2 + dy2 * dy2 - obj.r_sq()
            d = b * b - 4 * a * c
            if d < 0:
                return []
            t1, t2 = (-b + sqrt(d)) / (2 * a), (-b - sqrt(d)) / (2 * a)
            return [Point(x1 + dx1 * t, y1 + dy1 * t) for t in [t1, t2]]
        else:
            return []

    def is_close_to(self, l):
        v1 = self.p2 - self.p1
        for v2 in [l.p2 - l.p1, l.p2 - self.p1]:
            if abs(v1.x * v2.y - v2.x * v1.y) >= THRESH * abs(v1.x * v2.x):
                return False
        return True

    def contains(self, p):
        return (p - self.p1).is_parallel_to(p - self.p2)

    def __str__(self):
        return f"Line({self.p1}, {self.p2})"

    __repr__ = __str__
