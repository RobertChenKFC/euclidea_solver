from math import cos, pi
from euclidea_solver.canvas import Canvas
from euclidea_solver.solver import Solver
from euclidea_solver.entity.point import THRESH

def canvas_creator():
    canvas = Canvas()
    p1 = canvas.create_point()
    p2 = canvas.create_point()
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
    solver = Solver(canvas_creator, verifier)
    solver.solve()


if __name__ == "__main__":
    main()
