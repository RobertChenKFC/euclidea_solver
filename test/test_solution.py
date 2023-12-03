import random
from euclidea_solver.entity.point import THRESH
from euclidea_solver.entity.line import Line
from euclidea_solver.solution import (
    Solution, CreateLine, CreateCircle, CreatePoint,
    CreatePointOnLine, CreatePointOnCircle
)
from euclidea_solver.canvas import Canvas

def test_solution_1():
    random.seed(0)

    def canvas_creator():
        canvas = Canvas()
        canvas.create_point()
        canvas.create_point()
        return canvas

    def verifier(canvas):
        m = (canvas.get_obj(0) + canvas.get_obj(1)) * 0.5
        for p in canvas.get_points():
            if m.is_close_to(p):
                return True
        return False

    solution = Solution(canvas_creator, verifier)
    solution.add(CreateLine(0, 1))
    solution.add(CreateCircle(0, 1))
    solution.add(CreateCircle(1, 0))
    assert not solution.verify()
    solution.add(CreateLine(7, 8))
    assert solution.verify()


def test_solution_2():
    random.seed(0)

    def canvas_creator():
        canvas = Canvas()
        p1 = canvas.create_point()
        p2 = canvas.create_point()
        canvas.create_line(p1, p2)
        return canvas

    def verifier(canvas):
        p = canvas.get_obj(0)
        q = canvas.get_obj(1)
        m = (p + q) * 0.5
        v1 = q - p
        v1 = v1 / v1.mag()
        for l in canvas.get_lines():
            if l.contains(p):
                v2 = l.p2 - l.p1
                if abs(v1.dot(v2)) < THRESH * v2.mag():
                    return True
        return False

    solution = Solution(canvas_creator, verifier)
    solution.add(CreatePoint())
    solution.add(CreateCircle(3, 0))
    solution.add(CreateLine(3, 5))
    assert not solution.verify()
    solution.add(CreateLine(0, 7))
    assert solution.verify()


def test_solution_3():
    random.seed(0)

    def canvas_creator():
        canvas = Canvas()
        canvas.create_point()
        canvas.create_point()
        canvas.create_point()
        return canvas

    def verifier(canvas):
        p = canvas.get_obj(0)
        q = canvas.get_obj(1)

        ms = [(i * p + (3 - i) * q) / 3 for i in range(1, 3)]
        matches = [False] * len(ms)
        for m1 in canvas.get_points():
            for i, m2 in enumerate(ms):
                if m1.is_close_to(m2):
                    matches[i] = True
        return all(matches)

    solution = Solution(canvas_creator, verifier)
    solution.add(CreateLine(0, 2))
    solution.add(CreateCircle(2, 0))
    solution.add(CreateLine(1, 5))
    solution.add(CreateCircle(1, 5))
    solution.add(CreateLine(0, 1))
    solution.add(CreateLine(2, 10))
    assert not solution.verify()
    solution.add(CreateCircle(17, 1))
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
