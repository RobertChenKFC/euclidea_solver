from euclidea_solver.canvas import Canvas
from euclidea_solver.entity.line import Line
from euclidea_solver.entity.circle import Circle

class Inst:
    def __init__(self, method, *args):
        self._method = method
        self._args = args
        self._idx = None

    def _idx_str(self):
        return f" {self._idx}" if self._idx is not None else ""

    def __call__(self, canvas):
        self._idx = self._method(canvas, *self._args)
        return self._idx

    def cost(self):
        return 1

    def __hash__(self):
        return hash((id(self._method), *self._args))


    def __eq__(self, inst):
        return (
            self._method == inst._method and
            len(self._args) == len(inst._args) and
            all(arg1 == arg2 for arg1, arg2 in zip(self._args, inst._args))
        )


class PointInst(Inst):
    def cost(self):
        return 0


class CreatePoint(PointInst):
    def __init__(self):
        super().__init__(Canvas.create_point)

    def __str__(self):
        return f"Create point{self._idx_str()}"


class CreatePointOnLine(PointInst):
    def __init__(self, line):
        self._line = line
        super().__init__(Canvas.create_point_on_line, line)

    def __str__(self):
        return f"Create point{self._idx_str()} on line {self._line}"


class CreatePointOnCircle(PointInst):
    def __init__(self, circle):
        self._circle = circle
        super().__init__(Canvas.create_point_on_circle, circle)

    def __str__(self):
        return (
            f"Create point{self._idx_str()} on circle {self._circle}"
        )


class CreateLine(Inst):
    def __init__(self, p1, p2):
        self._p1 = p1
        self._p2 = p2
        super().__init__(Canvas.create_line, p1, p2)

    def __str__(self):
        return (
            f"Create line{self._idx_str()} through points {self._p1} and "
            f"{self._p2}"
        )


class CreateCircle(Inst):
    def __init__(self, p1, p2):
        self._p1 = p1
        self._p2 = p2
        super().__init__(Canvas.create_circle, p1, p2)

    def __str__(self):
        return (
            f"Create circle{self._idx_str()} with center at point {self._p1} "
            f"and passing through point {self._p2}"
        )


class Solution:
    def __init__(self, canvas_creator, verifier):
        self._canvas_creator = canvas_creator
        self._verifier = verifier
        self.clear()

    def clear(self):
        self._insts = []
        self._canvas = self._canvas_creator()

    def add(self, inst, verbose=False):
        self._insts.append(inst)
        idx = inst(self._canvas)
        if verbose:
            intersections = self._canvas.get_intersections()[idx]
            print(f"{inst}" + (
                ", intersecting with the following objects: "
                if len(intersections) != 0 else ""
            ))
            for obj, ps in intersections.items():
                msg = "- "
                # TODO: refactor this into something more elegant
                if isinstance(obj, Line):
                    msg += f"Line {self._canvas.get_lines()[obj]}"
                elif isinstance(obj, Circle):
                    msg += f"Circle {self._canvas.get_circles()[obj]}"
                msg += f" at Point"
                if len(ps) > 1:
                    msg += "s"
                msg += " " + ", ".join([str(p) for p in ps])
                print(msg)

    def pop(self):
        self._insts.pop()
        self._canvas.undo()

    def get_canvas(self):
        return self._canvas

    def get_insts(self):
        return self._insts

    def verify(self, additional_verifications=10):
        if not self._verifier(self._canvas):
            return False
        for _ in range(additional_verifications):
            canvas = self._canvas_creator()
            for inst in self._insts:
                # If this triggers an error, than that means this set of
                # instructions is not general enough (sometimes cannot be
                # constructed), and thus is not considered a solution
                # TODO: find a better way to check this
                try:
                    inst(canvas)
                except:
                    return False
            if not self._verifier(canvas):
                return False
        return True

