# DEBUG
import random
from euclidea_solver.entity.line import Line

from math import cos, pi
from euclidea_solver.canvas import Canvas
from euclidea_solver.solver import Solver
from euclidea_solver.entity.point import Point, THRESH

def canvas_creator():
    # DEBUG
    random.seed(0)

    canvas = Canvas()
    p1 = canvas.get_obj(canvas.create_point())
    p2 = canvas.get_obj(canvas.create_point())
    v = p2 - p1
    v = Point(-v.y, v.x)
    canvas.create_point(p2 + v)
    canvas.create_point(p1 + v)
    for i in range(4):
        canvas.create_line(i, (i + 1) % 4)

    # DEBUG
    """
    n = canvas.get_num_objs()
    print(f"Num objects: {n}")
    for i in range(n):
        print(canvas.get_obj(i))
    """

    return canvas


def verifier(canvas):
    p1 = canvas.get_obj(0)
    p2 = canvas.get_obj(1)
    p3 = canvas.get_obj(2)
    p4 = canvas.get_obj(3)
    m = (p1 + p2 + p3 + p4) * 0.25
    r = (p1 - p2).mag() * 0.5
    for c in canvas.get_circles():
        if m.is_close_to(c.p1) and abs(r - c.r()) < THRESH:
            return True
    return False


def main():
    solver = Solver(canvas_creator, verifier)
    solver.solve()


if __name__ == "__main__":
    main()
