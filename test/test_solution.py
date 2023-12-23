import random
from euclidea_solver.entity.point import THRESH, Point
from euclidea_solver.entity.line import Line
from euclidea_solver.solution import (
    Solution, CreateLine, CreateCircle, CreatePoint,
    CreatePointOnLine, CreatePointOnCircle
)
from euclidea_solver.canvas import Canvas


def test_solution_1():
    random.seed(0)

    def level_creator():
        canvas = Canvas()
        p1 = canvas.get_obj(canvas.create_point())
        p2 = canvas.get_obj(canvas.create_point())

        m = 0.5 * (p1 + p2)
        targets = [m]

        return canvas, targets

    solution = Solution(level_creator)
    solution.add(CreateLine(0, 1))
    solution.add(CreateCircle(0, 1))
    solution.add(CreateCircle(1, 0))
    assert not solution.verify()
    solution.add(CreateLine(7, 8))
    assert solution.verify()


def test_solution_2():
    random.seed(0)

    def level_creator():
        canvas = Canvas()
        p1 = canvas.create_point()
        p2 = canvas.create_point()
        canvas.create_line(p1, p2)

        p1 = canvas.get_obj(p1)
        p2 = canvas.get_obj(p2)
        v = p2 - p1
        p3 = p1 + Point(-v.y, v.x)
        l = Line(p1, p3)
        targets = [l]

        return canvas, targets

    solution = Solution(level_creator)
    solution.add(CreatePoint(exclusion_list=(2,)))
    solution.add(CreateCircle(3, 0))
    solution.add(CreateLine(3, 5))
    assert not solution.verify()
    solution.add(CreateLine(0, 7))
    assert solution.verify()


def test_solution_3():
    random.seed(0)

    def level_creator():
        canvas = Canvas()
        p1 = canvas.create_point()
        p2 = canvas.create_point()

        p1 = canvas.get_obj(p1)
        p2 = canvas.get_obj(p2)
        targets = [(i * p1 + (3 - i) * p2) / 3 for i in range(1, 3)]

        return canvas, targets

    solution = Solution(level_creator)
    solution.add(CreateLine(0, 1), verbose=True)
    solution.add(CreatePoint(exclusion_list=(2,)), verbose=True)
    solution.add(CreateCircle(3, 0), verbose=True)
    solution.add(CreateLine(0, 3), verbose=True)
    solution.add(CreateLine(1, 7), verbose=True)
    solution.add(CreateCircle(1, 7), verbose=True)
    solution.add(CreateLine(3, 14), verbose=True)
    assert not solution.verify()
    solution.add(CreateCircle(17, 1), verbose=True)
    assert solution.verify()


def test_inst():
    insts = set()

    insts.add(CreatePoint())
    assert CreatePoint() in insts

    insts.add(CreatePointOnLine(0))
    insts.add(CreatePointOnLine(1))
    insts.add(CreatePointOnCircle(2))
    assert CreatePointOnLine(0) in insts
    assert CreatePointOnLine(1) in insts
    assert CreatePointOnLine(2) not in insts
    assert CreatePointOnCircle(0) not in insts
    assert CreatePointOnCircle(1) not in insts
    assert CreatePointOnCircle(2) in insts

    insts.add(CreateLine(3, 4))
    insts.add(CreateCircle(5, 6))
    assert CreateLine(3, 4) in insts
    assert CreateLine(4, 3) not in insts
    assert CreateLine(5, 6) not in insts
    assert CreateCircle(3, 4) not in insts
    assert CreateCircle(5, 6) in insts
    assert CreateCircle(6, 5) not in insts
