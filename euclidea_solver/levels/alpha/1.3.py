from math import cos, pi
from euclidea_solver.canvas import Canvas
from euclidea_solver.solver import Solver
from euclidea_solver.entity.point import THRESH

def canvas_creator():
    canvas = Canvas()
    canvas.create_point()
    canvas.create_point()
    return canvas


def verifier(canvas):
    p1 = canvas.get_obj(0)
    p2 = canvas.get_obj(1)
    m = (p1 + p2) * 0.5
    for p in canvas.get_points():
        if m.is_close_to(p):
            return True
    return False


def main():
    solver = Solver(canvas_creator, verifier)
    solver.solve()


if __name__ == "__main__":
    main()
