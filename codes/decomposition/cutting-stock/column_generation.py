from typing import override
import time

from ortools.linear_solver import pywraplp
import numpy as np

from approximate import CutStockApprox


class _MasterProblem:

    """
    Master problem:
        min sum(x_j)
        s.t. Ax >= d
             x >= 0
        where 
        A: matrix of feasible cuts
        x: number of cuts used
        d: demand vector
    """
    
    def __init__(self, d):
        """
        d: list of demand sizes
        """
        self.d = d
        self.A = np.eye(len(d))
        self.solution = None
        self.objective = None
        self.p = None  # shadow price

    def solve(self):
        m, n = self.A.shape
        solver = pywraplp.Solver.CreateSolver('CLP')
        # Decision variables.
        x = [solver.NumVar(0, solver.infinity(), f"x-{j}") for j in range(n)]
        # Constraints: Ax >= d
        cts = []
        for i in range(m):
            ct = solver.Constraint(float(self.d[i]), solver.infinity(), f"ct-{i}")
            cts.append(ct)
            for j in range(n):
                ct.SetCoefficient(x[j], float(self.A[i][j]))
        # Objective function
        obj = solver.Objective()
        for j in range(n):
            obj.SetCoefficient(x[j], 1)

        obj.SetMinimization()

        status = solver.Solve()
        if status == solver.OPTIMAL:
            self.solution = np.array([x[j].solution_value() for j in range(n)])
            self.objective = obj.Value()
            # Get shadow price
            self.p = [cts[i].dual_value() for i in range(m)]

    def add_column(self, cut):
        cut = np.array(cut).reshape(-1, 1)
        self.A = np.hstack([self.A, cut])


class _SubProblem:

    """
    Subproblem:
        min sum(p_j * y_j)
        s.t. sum(s_j * y_j) <= L
             y_j >= 0
             y_j integer
        where
            L: raw size
            s: stock sizes
            p: price vector (shadow price of the master problem)
    """
    
    def __init__(self, L, s, p):
        self.L = L
        self.s = s
        self.p = p
        self.solution = None
        self.objective = None

    def solve(self):
        solver = pywraplp.Solver.CreateSolver('SCIP')
        n = len(self.p)
        # Decision variables.
        y = [solver.IntVar(0, solver.infinity(), f"y-{j}") for j in range(n)]
        # Constraint: sum(s_j * y_j) <= L
        ct = solver.Constraint(0, self.L, "ct-0")
        for j in range(n):
            ct.SetCoefficient(y[j], float(self.s[j]))
        # Objective function
        obj = solver.Objective()
        for j in range(n):
            obj.SetCoefficient(y[j], float(self.p[j]))
        obj.SetMaximization()
        self.status = solver.Solve()
        if self.status == solver.OPTIMAL:
            self.solution = np.array([y[j].solution_value() for j in range(n)]) 
            self.objective = obj.Value()


class _CutStockRelaxCG:

    timeout = 60  # in seconds

    """ Use column generation method to solve the relaxed problem, 
    i.e. the linear program problem of the form:
        min sum(x_j)
        s.t. Ax >= d
             x >= 0
        where
        A: initialized by identity matrix (A is not input)
        x: number of cuts used
        d: demand vector
    """
    
    def __init__(self, L, s, d):
        """
        L: raw size
        s: list of stock sizes
        d: list of demand sizes
        """
        self._start = time.time()
        self.L = L
        self.s = s
        self.d = d
        # solution
        self.x = None  # number of cuts used
        self.cuts = None  # cuts used
        self.count = None  # number of raw stock needed
        self.status = None  # status of the solver

    def solve(self):
        """
        Solve the relaxed problem.
        """
        master = _MasterProblem(self.d)
        while True:
            # 1. Solve the master problem
            master.solve()
            # 2. Solve the subproblem
            sub = _SubProblem(self.L, self.s, master.p)
            sub.solve()
            if sub.objective <= 1:
                # Stop if the optimal solution is found
                break
            # Check timeout
            if time.time() - self._start > self.timeout:
                self.status = "TIMEOUT"
                break
            # 3. Add new column
            master.add_column(sub.solution)

        # set solution
        solution = np.array(master.solution)
        self.x = solution[solution > 1e-6]
        self.cuts = master.A[:, solution > 1e-6]
        self.count = sum(self.x)
        
        if self.status is None:
            self.status = "OPTIMAL"

        return self

    def print_solution(self):
        print("-" * 50)
        print(f"Solution: {self.status}")
        print(f"|-- Objective: {self.count}")
        print(f"|-- Number of cuts: {self.x}")
        print(f"|-- Cuts:\n {self.cuts}")
        print("-" * 50)
        

class CutStockApproxCG(CutStockApprox):

    """ Use column generation method to get the approximate solution 
    of the cutting stock problem.
    """

    def __init__(self, L, s, d):
        super().__init__(L, s, d)
        self.timeout -= 1
        if self.timeout < 0:
            self.timeout = 0

    @override
    def _solve_relax(self):
        cg = _CutStockRelaxCG(self.L, self.s, self.d)
        cg.timeout = self.timeout
        cg.solve()
        self.x = cg.x
        self.cuts = cg.cuts
        self.count = cg.count

        if cg.status == "OPTIMAL":
            status = "RELAX_OPTIMAL"
        elif cg.status == "TIMEOUT":
            status = "RELAX_TIMEOUT"

        return status

    @override
    def solve(self):
        import signal
        signal.alarm(0)
        self._solve()
        return self


if __name__ == '__main__':

    L = 1000
    s = [450, 350, 310, 140]
    d = [97, 610, 395, 211]

    cs = CutStockApproxCG(L, s, d)
    cs.solve().print_solution()
    

    