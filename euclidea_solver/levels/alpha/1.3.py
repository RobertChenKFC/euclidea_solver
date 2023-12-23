import random
from math import cos, pi
from euclidea_solver.canvas import Canvas
from euclidea_solver.solution import Solution
from euclidea_solver.solver import Solver
from euclidea_solver.entity.point import THRESH, Point


class LevelCreator:
    def __init__(self):
        self.p1 = None
        self.p2 = None

    def __call__(self):
        canvas = Canvas()
        p1 = canvas.get_obj(canvas.create_point(self.p1))
        p2 = canvas.get_obj(canvas.create_point(self.p2))

        m = 0.5 * (p1 + p2)
        targets = [m]

        return canvas, targets


def main():
    level_creator = LevelCreator()
    solver = Solver(level_creator)
    insts = solver.solve()

    level_creator.p1 = Point(0, 0)
    level_creator.p2 = Point(10, 0)
    solution = Solution(level_creator, insts=insts)
    solution.gen_pdf("1.3")


if __name__ == "__main__":
    main()
