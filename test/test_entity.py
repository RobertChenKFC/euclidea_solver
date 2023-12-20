import random
from euclidea_solver.entity.point import Point, THRESH
from euclidea_solver.entity.line import Line
from euclidea_solver.entity.circle import Circle

def test_lines_intersect():
    l1 = Line(Point(-2.7, -3.18), Point(-0.08, -0.66))
    l2 = Line(Point(-2.28, 0.12), Point(0.34, -4.06))
    points = l1.intersect(l2)
    assert len(points) == 1
    p = points[0]
    assert p.dist(Point(-1.1475223880597, -1.6867772587444)) < THRESH


def are_same_set_of_points(s1, s2):
    if len(s1) != len(s2):
        return False
    s = set(range(len(s2)))
    for p in s1:
        ok = False
        for j in s:
            q = s2[j]
            if p.dist(q) < THRESH:
                s.remove(j)
                ok = True
                break
        if not ok:
            return False
    return True
            

def test_line_circle_intersect():
    c = Circle(Point(-1.6, -2.08), Point(-0.34, -0.3))
    l = Line(Point(-0.82, 1.2), Point(-3.46, -4.82))
    points = l.intersect(c)

    assert len(points) == 2
    p1 = Point(-1.3104944068425, 0.0815241177305)
    p2 = Point(-2.993919941688, -3.7571962306673)
    assert are_same_set_of_points(points, [p1, p2])


def test_circles_intersect():
    c1 = Circle(Point(-4.14, 0.44), Point(-2.06, 0.48))
    c2 = Circle(Point(-2.26, 3.12), Point(-3.62, 1.6))
    points = c1.intersect(c2)

    assert len(points) == 2
    p1 = Point(-4.2091235208001, 2.5192359026508)
    p2 = Point(-2.1614049951748, 1.0827766384062)
    assert are_same_set_of_points(points, [p1, p2])


def test_parallel():
    random.seed(0)

    p = Point()
    q = Point(-p.y, p.x)
    for _ in range(10):
        m = random.random() * 100 - 50
        assert p.is_parallel_to(p * m)
        assert not p.is_parallel_to(q * m)

def test_close_lines():
    p = Point(84.4421851525048, 75.79544029403024)
    q = Point(134.34595041723873, 33.41041322460994)
    v = q - p
    v = Point(-v.y, v.x)
    r = p + v
    l1 = Line(p, q)
    l2 = Line(q, p)
    l3 = Line(p, r)
    assert l1.is_close_to(l2)
    assert l2.is_close_to(l1)
    assert not l1.is_close_to(l3)
    assert not l3.is_close_to(l1)
