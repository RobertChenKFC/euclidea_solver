from math import sqrt
from euclidea_solver.canvas import Canvas
from euclidea_solver.entity.line import Line
from euclidea_solver.solution import Solution
from euclidea_solver.solver import Solver
from euclidea_solver.entity.point import Point, THRESH


class LevelCreator:
    def __init__(self):
        self.p1 = None
        self.p2 = None

    def __call__(self):
        canvas = Canvas()
        p1 = canvas.create_point(self.p1)
        p2 = canvas.create_point(self.p2)
        canvas.create_line(p1, p2)

        p1 = canvas.get_obj(p1)
        p2 = canvas.get_obj(p2)
        v = p2 - p1
        cost, sint = 1 / 2, sqrt(3) / 2
        p3 = p1 + Point(v.x * cost - v.y * sint, v.x * sint + v.y * cost)
        targets = [Line(p1, p3)]

        return canvas, targets


def main():
    level_creator = LevelCreator()
    solver = Solver(level_creator)
    insts = solver.solve()

    level_creator.p1 = Point(0, 0)
    level_creator.p2 = Point(10, 0)
    solution = Solution(level_creator, insts=insts)
    solution.gen_pdf("1.1")


if __name__ == "__main__":
    main()
