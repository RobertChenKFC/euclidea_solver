import random
from euclidea_solver.canvas import Canvas
from euclidea_solver.entity.point import THRESH

def test_canvas_1():
    canvas = Canvas()

    random.seed(0)
    p1 = canvas.create_point()
    assert p1 == 0
    p2 = canvas.create_point()
    assert p2 == 1
    c1 = canvas.create_circle(p1, p2)
    assert c1 == 2
    c2 = canvas.create_circle(p2, p1)
    assert c2 == 3
    l1 = canvas.create_line(p1, p2)
    assert l1 == 6
    l2 = canvas.create_line(4, 5)
    assert l2 == 9

    p = canvas.get_obj(0)
    q = canvas.get_obj(1)
    m = canvas.get_obj(10)
    assert m.dist((p + q) * 0.5) < THRESH

    p3 = canvas.create_point_on_line(l2)
    assert p3 == 11
    m = canvas.get_obj(p3)
    assert abs(p.dist(m) - q.dist(m)) < THRESH

    assert canvas.create_line(7, 8) == l1
    assert canvas.create_circle(1, 8) == c2


def test_canvas_2():
    canvas = Canvas()

    random.seed(0)
    p1 = canvas.create_point()
    assert p1 == 0
    p2 = canvas.create_point()
    assert p2 == 1
    l1 = canvas.create_line(p1, p2)
    assert l1 == 2
    c1 = canvas.create_circle(p1, p2)
    assert c1 == 3
    p3 = canvas.create_point_on_circle(c1)
    assert p3 == 5

    p = canvas.get_obj(p3)
    q = canvas.get_obj(p2)
    r = canvas.get_obj(4)
    v1 = q - p
    v2 = r - p
    assert abs(v1.dot(v2) / (v1.mag() * v2.mag())) < THRESH


def test_undo():
    canvas = Canvas()

    random.seed(0)
    p1 = canvas.create_point()
    p2 = canvas.create_point()
    canvas.create_circle(p1, p2)
    canvas.create_circle(p2, p1)
    canvas.create_line(p1, p2)

    assert len(canvas.get_points()) == 6
    assert len(canvas.get_lines()) == 1
    assert len(canvas.get_circles()) == 2
    assert canvas.get_num_objs() == 9

    canvas.undo()
    assert len(canvas.get_points()) == 4
    assert len(canvas.get_lines()) == 0
    assert len(canvas.get_circles()) == 2
    assert canvas.get_num_objs() == 6

    canvas.undo()
    assert len(canvas.get_points()) == 2
    assert len(canvas.get_lines()) == 0
    assert len(canvas.get_circles()) == 1
    assert canvas.get_num_objs() == 3

    canvas.undo()
    assert len(canvas.get_points()) == 2
    assert len(canvas.get_lines()) == 0
    assert len(canvas.get_circles()) == 0
    assert canvas.get_num_objs() == 2

    canvas.undo()
    assert len(canvas.get_points()) == 1
    assert len(canvas.get_lines()) == 0
    assert len(canvas.get_circles()) == 0
    assert canvas.get_num_objs() == 1

