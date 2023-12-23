import shutil
import subprocess

from euclidea_solver.canvas import Canvas, CANVAS_BORDER_RATIO
from euclidea_solver.entity.point import Point
from euclidea_solver.entity.line import Line
from euclidea_solver.entity.circle import Circle


class Inst:
    def __init__(self, method, *args, **kwargs):
        self._method = method
        self._args = args
        self._kwargs = kwargs
        self._idx = None
        self._hash = hash((
            id(self._method), *self._args, *sorted(self._kwargs.items())
        ))

    def _idx_str(self):
        return f" {self._idx}" if self._idx is not None else ""

    def __call__(self, canvas):
        self._idx = self._method(canvas, *self._args, **self._kwargs)
        return self._idx

    def cost(self):
        return 1

    def __hash__(self):
        return self._hash

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
    def __init__(self, point=None, exclusion_list=()):
        super().__init__(
            Canvas.create_point, point=point, exclusion_list=exclusion_list
        )

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


class Targets:
    def __init__(self, targets, cls):
        self._targets = [
            target for target in targets if isinstance(target, cls)
        ]
        self._cls = cls
        self.clear_all_matches()

    def all_matched(self):
        return len(self._targets_matched) == len(self._targets)

    def clear_all_matches(self):
        self._target_is_matched = [False] * len(self._targets)
        self._targets_matched = []

    def undo_match(self):
        idx = self._targets_matched.pop()
        self._target_is_matched[idx] = False

    def match_new_obj(self, obj):
        if isinstance(obj, self._cls) and not self.all_matched():
            for idx, target in enumerate(self._targets):
                if target.is_close_to(obj):
                    self._target_is_matched[idx] += 1
                    self._targets_matched.append(idx)
                    return True
        return False


class Solution:
    def __init__(self, level_creator, insts=None):
        self._level_creator = level_creator
        self.clear()

        if insts is not None:
            for inst in insts:
                self.add(inst)

    def clone(self, copy_insts=True):
        return Solution(
            self._level_creator,
            insts=self._insts if copy_insts else None
        )

    def clear(self):
        self._insts = []
        self._canvas, targets = self._level_creator()
        self._target_points = Targets(targets, Point)
        self._target_lines = Targets(targets, Line)
        self._target_circles = Targets(targets, Circle)
        self._all_targets = [
            self._target_points, self._target_lines, self._target_circles
        ]
        self._targets_matched = []

    def add(self, inst, verbose=False, gen_latex=False):
        # Update canvas with instruction
        self._insts.append(inst)
        num_original_objs = self._canvas.get_num_objs()
        new_obj_idx = inst(self._canvas)

        # Check if newly created objects match unmatched targets
        targets_matched = None
        for idx in range(num_original_objs, self._canvas.get_num_objs()):
            for targets in self._all_targets:
                if targets.match_new_obj(self._canvas.get_obj(idx)):
                    targets_matched = targets
                    break
        self._targets_matched.append(targets_matched)

        # Generate the message/latex to display the instruction and the new
        # intersections
        if verbose or gen_latex:
            intersections = self._canvas.get_intersections()[new_obj_idx]
            msg = (
                f"{inst}" + (
                    ", intersecting with the following objects: "
                    if len(intersections) != 0 else ""
                ) + "\n"
            )
            if gen_latex and len(intersections) != 0:
                msg += "\\begin{itemize}\n"
            for obj, ps in intersections.items():
                if verbose:
                    msg += "- "
                else:
                    msg += "\\item "
                # TODO: refactor this into something more elegant
                if isinstance(obj, Line):
                    msg += f"Line {self._canvas.get_lines()[obj]}"
                elif isinstance(obj, Circle):
                    msg += f"Circle {self._canvas.get_circles()[obj]}"
                msg += f" at Point"
                if len(ps) > 1:
                    msg += "s"
                msg += " " + ", ".join([str(p) for p in ps]) + "\n"
            if gen_latex and len(intersections) != 0:
                msg += "\\end{itemize}\n"
            if verbose:
                print(msg, end="")
            elif gen_latex:
                return msg

    def pop(self):
        self._insts.pop()
        self._canvas.undo()
        targets = self._targets_matched.pop()
        if targets is not None:
            targets.undo_match()

    def get_canvas(self):
        return self._canvas

    def get_insts(self):
        return self._insts

    def _all_targets_matched(self):
        for targets in self._all_targets:
            if not targets.all_matched():
                return False
        return True

    def verify(self, additional_verifications=10):
        if not self._all_targets_matched():
            return False
        for _ in range(additional_verifications):
            solution = self.clone()
            if not solution._all_targets_matched():
                return False
        return True

    def gen_latex(self, title):
        canvas, _ = self._level_creator()
        for inst in self._insts:
            inst(canvas)
        top_left, bottom_right = None, None
        for i in range(canvas.get_num_objs()):
            obj = canvas.get_obj(i)
            obj_top_left, obj_bottom_right = obj.get_bounds()
            if top_left is None:
                top_left, bottom_right = obj_top_left, obj_bottom_right
            else:
                top_left = Point(
                    min(top_left.x, obj_top_left.x),
                    min(top_left.y, obj_top_left.y)
                )
                bottom_right = Point(
                    max(bottom_right.x, obj_bottom_right.x),
                    max(bottom_right.y, obj_bottom_right.y)
                )
        top_left *= 1 + CANVAS_BORDER_RATIO
        bottom_right *= 1 + CANVAS_BORDER_RATIO

        latex = ""
        solution = self.clone()
        canvas, _ = self._level_creator()
        for inst in self._insts:
            inst_latex = solution.add(inst, gen_latex=True)
            new_obj_idx = canvas.get_num_objs()
            inst(canvas)
            latex += f"""
            \\item {inst_latex}
            {canvas.gen_latex(top_left, bottom_right, new_obj_idx)}
            """

        return """
        \\documentclass{article}
        \\usepackage[margin=1in]{geometry}
        \\usepackage{tikz}
        \\usepackage{float}

        \\title{%s}
        \\author{}
        \\date{}

        \\begin{document}

        \\maketitle

        \\begin{enumerate}
        %s
        \\end{enumerate}

        \\end{document}
        """ % (title, latex)

    def gen_pdf(self, level):
        latex = self.gen_latex(f"Level {level}")
        with open(f"{level}.tex", "w") as outfile:
            outfile.write(latex)

        pdflatex = shutil.which("pdflatex")
        subprocess.run(
            [pdflatex, f"{level}.tex"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
