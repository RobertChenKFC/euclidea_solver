# DEBUG
import random

from euclidea_solver.entity.circle import Circle
from euclidea_solver.entity.line import Line

from math import cos, pi
from euclidea_solver.canvas import Canvas
from euclidea_solver.solver import Solver
from euclidea_solver.entity.point import Point, THRESH

class LevelCreator:
    def __init__(self):
        self.p1 = None
        self.p2 = None

    def __call__(self):
        canvas = Canvas()
        p1 = canvas.get_obj(canvas.create_point())
        p2 = canvas.get_obj(canvas.create_point())
        v = p2 - p1
        v = Point(-v.y, v.x)
        p3 = p2 + v
        p4 = p1 + v
        canvas.create_point(p3)
        canvas.create_point(p4)
        for i in range(4):
            canvas.create_line(i, (i + 1) % 4)

        c = Circle((p1 + p2 + p3 + p4) * 0.25, (p2 - p1) * 0.5)
        targets = [c]

        return canvas, targets


def main():
    level_creator = LevelCreator()
    solver = Solver(level_creator)
    solver.solve()


if __name__ == "__main__":
    main()
