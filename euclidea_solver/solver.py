from timeit import default_timer
from euclidea_solver.entity.line import Line
from euclidea_solver.entity.circle import Circle
from euclidea_solver.solution import (
    Solution, CreatePoint, CreatePointOnLine, CreatePointOnCircle,
    CreateLine, CreateCircle
)

class Solver:
    def __init__(self, canvas_creator, verifier):
        self._solution = Solution(canvas_creator, verifier)
        self._candidates = []
        self._used_insts = set()

        canvas = canvas_creator()
        for p in canvas.get_points().values():
            for q in canvas.get_points().values():
                if p != q:
                    if p < q:
                        l1 = Line(canvas.get_obj(p), canvas.get_obj(q))
                        for l2 in canvas.get_lines():
                            if l1.is_close_to(l2):
                                self._used_insts.add(CreateLine(p, q))
                    c1 = Circle(canvas.get_obj(p), canvas.get_obj(q))
                    for c2 in canvas.get_circles():
                        if c1.is_close_to(c2):
                            self._used_insts.add(CreateCircle(p, q))

        self._num_trials = 0

    def _try_inst(self, inst, depth, allow_repeats=False, verbose=True):
        if not allow_repeats:
            if inst in self._used_insts:
                return
            self._used_insts.add(inst)

        self._solution.add(inst)
        self._solve_until_depth(depth - 1, verbose=verbose)
        self._solution.pop()
        if not allow_repeats:
            self._used_insts.remove(inst)

    def _solve_until_depth(self, depth, verbose=True):
        self._num_trials += 1
        if verbose and self._num_trials % 1000 == 0:
            print(f"Tried {self._num_trials} solutions...")

        solution = self._solution
        if solution.verify(additional_verifications=0):
            self._candidates.append(list(solution.get_insts()))
        if depth == 0:
            return

        canvas = solution.get_canvas()
        # DEBUG
        # self._try_inst(
        #     CreatePoint(), depth, allow_repeats=True, verbose=verbose
        # )
        # for line in canvas.get_lines().values():
        #     self._try_inst(
        #         CreatePointOnLine(line), depth, allow_repeats=True,
        #         verbose=verbose
        #     )
        # for circle in canvas.get_circles().values():
        #     self._try_inst(
        #         CreatePointOnCircle(circle), depth, allow_repeats=True,
        #         verbose=verbose
        #     )

        # TODO: possible optimization: we only allow creating lines and circles
        #       in order, where each instruction is ordered by the pair of
        #       points used to construct this line/circle.
        # TODO: another possible optimization: create all possible lines and
        #       circles, check if this yields the solution, if so then remove
        #       unnecessary lines and circles. Have to figure out how to figure
        #       out which lines and circles are necessary for the solution, and
        #       how to remove the unnecessary lines and circles in the most
        #       efficient way.

        for p1 in canvas.get_points().values():
            for p2 in canvas.get_points().values():
                if p1 != p2:
                    if p1 < p2:
                        # CreateLine(a, b) is the same as CreateLine(b, a), so
                        # we only try CreateLine(min(a, b), max(a, b))
                        self._try_inst(
                            CreateLine(p1, p2), depth, verbose=verbose
                        )
                    self._try_inst(CreateCircle(p1, p2), depth, verbose=verbose)

    def solve(self, verbose=True):
        self._num_trials = 0
        tic = default_timer()

        depth = 1
        while True:
            if verbose:
                print(f"Trying depth = {depth}")

            self._candidates = []
            self._solution.clear()
            self._solve_until_depth(depth)

            best_insts = None
            for insts in self._candidates:
                self._solution.clear()
                good_insts = True
                for inst in insts:
                    # Similar to the check in Solution.verify
                    # TODO: find a better way to check this
                    try:
                        self._solution.add(inst)
                    except:
                        good_insts = False
                        break
                if good_insts and self._solution.verify():
                    cost = sum(inst.cost() for inst in insts)
                    if best_insts is None or cost < best_cost:
                        best_insts = insts
                        best_cost = cost

            if best_insts is not None:
                # TODO: this is not necessarily the best solution; figure
                #       out how to search for the best solution
                if verbose:
                    toc = default_timer()
                    duration = toc - tic
                    
                    print(
                        f"Found {cost}E solution in {duration:.2f} seconds "
                        f"after {self._num_trials} tries:"
                    )
                    self._solution.clear()
                    for i, inst in enumerate(best_insts):
                        print(f"{i + 1}. ", end="")
                        self._solution.add(inst, verbose=True)

                return best_insts

            depth += 1
