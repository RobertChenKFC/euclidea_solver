from math import tau, sin, cos
from random import random
from itertools import chain
from euclidea_solver.entity.point import Point, RAND_RANGE, THRESH_SQ, THRESH
from euclidea_solver.entity.line import Line
from euclidea_solver.entity.circle import Circle

class Canvas:
    def __init__(self):
        self._objs = []
        self._points = dict()
        self._lines = dict()
        self._circles = dict()
        self._intersections = dict()
        self._undo_stack = []

    def get_num_objs(self):
        return len(self._objs)

    def get_obj(self, idx):
        return self._objs[idx]

    def get_points(self):
        return self._points

    def get_lines(self):
        return self._lines

    def get_circles(self):
        return self._circles

    def _add_obj(self, obj, objs):
        objs[obj] = idx = len(self._objs)
        self._objs.append(obj)
        if isinstance(obj, Point):
            self._intersections[idx] = dict()
        else:
            intersections = dict()
            for obj2 in chain(self._lines.keys(), self._circles.keys()):
                ps = [self._add_point(p) for p in obj.intersect(obj2)]
                if len(ps) > 0:
                    intersections[obj2] = ps
            self._intersections[idx] = intersections
        return idx

    def _create_undo_point(self):
        self._undo_stack.append(len(self._objs))

    def _add_point(self, p):
        for q, idx in self._points.items():
            if p.is_close_to(q):
                return idx
        return self._add_obj(p, self._points)

    def create_point(self):
        self._create_undo_point()
        p = Point()
        cur_len = len(self._objs)
        while (idx := self._add_point(p)) < cur_len:
            p = Point()
        return idx

    def create_point_on_line(self, line_idx):
        self._create_undo_point()
        line = self._objs[line_idx]
        assert isinstance(line, Line)
        p, vec = line.p1, line.p2 - line.p1
        t = random() * RAND_RANGE
        cur_len = len(self._objs)
        while (idx := self._add_point(p + t * vec)) < cur_len:
            t = random() * RAND_RANGE
        return idx

    def create_point_on_circle(self, circle_idx):
        self._create_undo_point()
        circle = self._objs[circle_idx]
        assert isinstance(circle, Circle)
        p, r = circle.p1, circle.r()
        t = random() * tau
        cur_len = len(self._objs)
        while (
            idx := self._add_point(Point(p.x + r * cos(t), p.y + r * sin(t)))
        ) < cur_len:
            t = random() * tau
        return idx

    def create_line(self, p1_idx, p2_idx):
        self._create_undo_point()
        p1 = self._objs[p1_idx]
        p2 = self._objs[p2_idx]
        assert isinstance(p1, Point)
        assert isinstance(p2, Point)
        l1 = Line(p1, p2)
        for l2, idx in self._lines.items():
            if l1.is_close_to(l2):
                return idx
        return self._add_obj(l1, self._lines)

    def create_circle(self, p1_idx, p2_idx):
        self._create_undo_point()
        p1 = self._objs[p1_idx]
        p2 = self._objs[p2_idx]
        assert isinstance(p1, Point)
        assert isinstance(p2, Point)
        c1 = Circle(p1, p2)
        for c2, idx in self._circles.items():
            if c1.is_close_to(c2):
                return idx
        return self._add_obj(c1, self._circles)

    def get_intersections(self):
        return self._intersections

    def undo(self):
        if len(self._undo_stack) > 0:
            length = self._undo_stack.pop()
            for i in range(len(self._objs) - 1, length - 1, -1):
                obj = self._objs.pop()
                # TODO: refactor this to make this more elegant
                for objs, cls in [
                    (self._points, Point), (self._lines, Line),
                    (self._circles, Circle)
                ]:
                    if isinstance(obj, cls):
                        del objs[obj]
                        break
