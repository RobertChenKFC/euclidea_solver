from euclidea_solver.entity.line import Line
from euclidea_solver.solver import Solver
from euclidea_solver.canvas import Canvas
from euclidea_solver.solution import Solution
from euclidea_solver.entity.point import THRESH, Point


def test_solver():
    def level_creator():
        canvas = Canvas()
        p1 = canvas.get_obj(canvas.create_point())
        p2 = canvas.get_obj(canvas.create_point())

        m1 = 0.5 * (p1 + p2)
        v = p2 - p1
        m2 = m1 + Point(-v.y, v.x)
        l = Line(m1, m2)
        targets = [l]

        return canvas, targets

    solver = Solver(level_creator)
    insts = solver.solve()

    solution = Solution(level_creator)
    for inst in insts:
        solution.add(inst)
    assert solution.verify()
