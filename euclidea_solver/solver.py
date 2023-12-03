from timeit import default_timer
from euclidea_solver.solution import (
    Solution, CreatePoint, CreatePointOnLine, CreatePointOnCircle,
    CreateLine, CreateCircle
)

class Solver:
    def __init__(self, canvas_creator, verifier):
        self._solution = Solution(canvas_creator, verifier)
        self._candidates = []
        self._used_insts = set()
        self._num_trials = 0

    def _try_inst(self, inst, depth, allow_repeats=False):
        if not allow_repeats:
            if inst in self._used_insts:
                return
            self._used_insts.add(inst)

        self._solution.add(inst)
        self._solve_until_depth(depth - 1)
        self._solution.pop()
        if not allow_repeats:
            self._used_insts.remove(inst)

    def _solve_until_depth(self, depth):
        self._num_trials += 1

        solution = self._solution
        if solution.verify(additional_verifications=0):
            self._candidates.append(list(solution.get_insts()))
        if depth == 0:
            return

        canvas = solution.get_canvas()
        self._try_inst(CreatePoint(), depth, allow_repeats=True)
        for line in canvas.get_lines().values():
            self._try_inst(
                CreatePointOnLine(line), depth, allow_repeats=True
            )
        for circle in canvas.get_circles().values():
            self._try_inst(
                CreatePointOnCircle(circle), depth, allow_repeats=True
            )

        for p1 in canvas.get_points().values():
            for p2 in canvas.get_points().values():
                if p1 != p2:
                    if p1 < p2:
                        # CreateLine(a, b) is the same as CreateLine(b, a), so
                        # we only try CreateLine(min(a, b), max(a, b))
                        self._try_inst(CreateLine(p1, p2), depth)
                    self._try_inst(CreateCircle(p1, p2), depth)

    def solve(self, verbose=True):
        self._num_trials = 0
        tic = default_timer()

        depth = 1
        while True:
            self._candidates = []
            self._solution.clear()
            self._solve_until_depth(depth)

            best_solution = None
            for insts in self._candidates:
                self._solution.clear()
                good_solution = True
                for inst in insts:
                    # Similar to the check in Solution.verify
                    # TODO: find a better way to check this
                    try:
                        self._solution.add(inst)
                    except:
                        good_solution = False
                        break
                if good_solution and self._solution.verify():
                    cost = sum(inst.cost() for inst in insts)
                    if best_solution is None or cost < best_cost:
                        best_solution = insts
                        best_cost = cost

            if best_solution is not None:
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
                    for i, inst in enumerate(best_solution):
                        print(f"{i + 1}. ", end="")
                        self._solution.add(inst, verbose=True)

                return best_solution

            depth += 1

