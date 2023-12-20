from math import cos, pi
from euclidea_solver.canvas import Canvas
from euclidea_solver.solution import Solution
from euclidea_solver.solver import Solver
from euclidea_solver.entity.point import Point, THRESH


class CanvasCreator:
    def __init__(self):
        self.p1 = None
        self.p2 = None

    def __call__(self):
        canvas = Canvas()
        p1 = canvas.create_point(self.p1)
        p2 = canvas.create_point(self.p2)
        canvas.create_line(p1, p2)
        return canvas


def verifier(canvas):
    p1 = canvas.get_obj(0)
    p2 = canvas.get_obj(1)
    v1 = p2 - p1
    v1 = v1 / v1.mag()
    for line in canvas.get_lines():
        if line.contains(p1):
            v2 = line.p1 - line.p2
            v2 = v2 / v2.mag()
            if (abs(v1.dot(v2)) - 0.5) < THRESH:
                return True


def main():
    canvas_creator = CanvasCreator()
    solver = Solver(canvas_creator, verifier)
    insts = solver.solve()

    canvas_creator.p1 = Point(0, 0)
    canvas_creator.p2 = Point(10, 0)
    solution = Solution(canvas_creator, verifier, insts=insts)
    with open("1.1.tex", "w") as outfile:
        outfile.write(solution.gen_latex("Level 1.1"))


if __name__ == "__main__":
    main()
