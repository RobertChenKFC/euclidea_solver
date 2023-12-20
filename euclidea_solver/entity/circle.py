from math import sqrt
from euclidea_solver.entity.point import Point, THRESH, THRESH_SQ

class Circle:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __hash__(self):
        return id(self)

    def get_coords(self):
        return self.p1.x, self.p1.y, self.p2.x, self.p2.y

    def __str__(self):
        return f"Circle({self.p1}, {self.p1.dist(self.p2)})"

    __repr__ = __str__

    def r_sq(self):
        return (self.p1 - self.p2).mag_sq()

    def r(self):
        return (self.p1 - self.p2).mag()

    def intersect(self, obj):
        from euclidea_solver.entity.line import Line

        if isinstance(obj, Line):
            return obj.intersect(self)
        elif isinstance(obj, Circle):
            x1, y1 = self.p1.get_coords()
            x3, y3 = obj.p1.get_coords()
            r1_sq, r2_sq = self.r_sq(), obj.r_sq()
            if x1 == x3 and y1 == y3:
                return []
            rhs = (x1 * x1 - x3 * x3 + y1 * y1 - y3 * y3 - r1_sq + r2_sq) / 2
            if x1 == x3:
                p = Point(0, rhs / (y1 - y3))
            else:
                p = Point(rhs / (x1 - x3), 0)
            return Line(p, p + Point(y3 - y1, x1 - x3)).intersect(self)
        else:
            return []

    def is_close_to(self, c):
        # TODO: difference of squares can probably be replaced with expression
        #       that only requires one square root
        return (
            self.p1.dist_sq(c.p1) < THRESH_SQ and
            abs(self.r() - c.r()) < THRESH
        )

    def contains(self, p):
        # TODO: same optimization as Circle.is_close_to probably applies here
        return abs(self.p1.dist(p) - self.r()) < THRESH

    def gen_latex(self, top_left, bottom_right, label, color="black"):
        x, y, r = self.p1.x, self.p1.y, self.r()
        return f"""
        \\draw[color={color}] ({x}, {y}) circle ({r});
        \\draw[color={color}] ({x + r / sqrt(2)}, {y + r / sqrt(2)})
            node[above right] {{{label}}};
        """

    def get_bounds(self):
        r = self.r()
        v = Point(r, r)
        return self.p1 - v, self.p1 + v