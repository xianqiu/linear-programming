import signal

from ortools.linear_solver import pywraplp
import numpy as np


def enumerate_vectors(ub):
    """
    Enumerate vectors in [0, ub].
    lb: lower bound vector
    ub: upper bound vector
    E.g. ub = [2, 2] 
        => [[0,0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 1], [2, 2]]
    """
    def _enumerate_vectors(lb, ub, i, vec, vecs):
        """
        Enumerate vectors in [lb, ub].
        lb: lower bound vector
        ub: upper bound vector
        i: current index
        vec: current vector
        vecs: list of vectors
        """
        if i == len(lb):
            vecs.append(vec)
            return
        for j in range(lb[i], ub[i] + 1):
            _enumerate_vectors(lb, ub, i + 1, vec + [j], vecs)
    vecs = []
    _enumerate_vectors([0] * len(ub), ub, 0, [], vecs)
    return vecs


class CutStockExact:

    """
    Exact solution of the cutting stock problem.
    """

    timeout = 60  # in seconds
    
    def __init__(self, L, s, d):
        """
        L: raw size
        s: list of stock sizes
        d: list of demand sizes
        """
        self.L = L
        self.s = s
        self.d = d
        # feasible cuts (as columns of matrix A)
        self._A = None
        # Solution
        self.count = None  # Number of raw stock needed
        self.x = None  # Number of raw stock for each used cut 
        self.cuts = None  # Cuts used
        self.status = None  # Status of the solver
    
    def _feasible_cuts(self):
        """
        Enumerate all feasible cuts (patterns).
        """
        cuts = []
        ub = [int(self.L / s) for s in self.s]
        # enumerate all vectors in [0, ub]
        # if sum of vector is less than or equal to L, add to cuts
        # except for the zero vector
        for cut in enumerate_vectors(ub)[1: ]:
            if  np.array(cut) @ np.array(self.s) <= self.L:
                cuts.append(cut)

        return cuts

    def _solve(self):
        """
        Solve the integer program using CBC solver.
        """
        solver = pywraplp.Solver.CreateSolver('CBC')
        m, n = self._A.shape
        # Decision variables.
        x = [solver.IntVar(0, solver.infinity(), f"x-{j}") for j in range(n)]
        # Constraints: Ax >= d
        for i in range(m):
            ct = solver.Constraint(float(self.d[i]), solver.infinity(), f"ct-{i}")
            for j in range(n):
                ct.SetCoefficient(x[j], float(self._A[i][j]))
        # Objective function
        obj = solver.Objective()
        for j in range(n):
            obj.SetCoefficient(x[j], 1)

        obj.SetMinimization()
        # Solve
        status = solver.Solve()
        if status == solver.OPTIMAL:
            solution = np.array([x[j].solution_value() for j in range(n)])
            self.x = solution[solution > 0]
            self.cuts = self._A[:, solution > 0]
            self.count = sum(self.x)
            self.status = "OPTIMAL"
        else:
            self.status = "UNKNOWN"
        
    def solve(self):
        """
        Solve the cutting stock problem.
        """
        # Set timeout handler
        def timeout_handler(signum, frame):
            raise Exception("Timeout")
            
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(self.timeout)

        try:
            self._A = np.array(self._feasible_cuts()).T
            self._solve()
            signal.alarm(0) 
        except Exception as e:
            self.status = "TIMEOUT"
        
        return self

    def print_solution(self):
        print("-" * 50)
        print(f"Solution: {self.status}")
        print(f"|-- Objective: {self.count}")
        print(f"|-- Number of cuts: {self.x}")
        print(f"|-- Cuts:\n {self.cuts}")
        print("-" * 50)


if __name__ == '__main__':
    
    L = 1000
    s = [450, 350, 310, 140]
    d = [97, 610, 395, 211]

    cs = CutStockExact(L, s, d)
    cs.solve().print_solution()
    