from euclidea_solver.solver import Solver
from euclidea_solver.canvas import Canvas
from euclidea_solver.solution import Solution
from euclidea_solver.entity.point import THRESH


def test_solver():
    def canvas_creator():
        canvas = Canvas()
        canvas.create_point()
        canvas.create_point()
        return canvas

    def verifier(canvas):
        p = canvas.get_obj(0)
        q = canvas.get_obj(1)
        m = (p + q) * 0.5
        v1 = q - p
        v1 = v1 / v1.mag()
        for l in canvas.get_lines():
            if l.contains(m):
                v2 = l.p1 - l.p2
                if abs(v1.dot(v2)) < THRESH * v2.mag():
                    return True
        return False

    solver = Solver(canvas_creator, verifier)
    insts = solver.solve()

    solution = Solution(canvas_creator, verifier)
    for inst in insts:
        solution.add(inst)
    assert solution.verify()

