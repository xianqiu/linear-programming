from typing import override

from ortools.linear_solver import pywraplp
import numpy as np

from exact import CutStockExact


class CutStockApprox(CutStockExact):

    def __init__(self, L, s, d):
        """
        L: raw size
        s: list of stock sizes
        d: list of demand sizes
        """
        super().__init__(L, s, d)

    def _solve_relax(self):
        # Solve the relaxed problem using CLP solver
        solver = pywraplp.Solver.CreateSolver('CLP')
        m, n = self._A.shape
        # Decision variables.
        x = [solver.NumVar(0, solver.infinity(), f"x-{j}") for j in range(n)]
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
            status = "RELAX_OPTIMAL"
        else:
            status = "RELAX_UNSOLVED"
        
        return status

    def _round_down(self):
        # Round down the solution to the nearest integer
        self.x = np.floor(self.x)
        self.count = sum(self.x)
        unsatisfied_demands = self.d - self.cuts @ self.x

        return unsatisfied_demands

    def _greedy_satisfy(self, unsatisfied_demands):
        """
        Greedily satisfy the unsatisfied demands.
        """
        # Find the maximal unsatsified demand
        row_index = np.argmax(unsatisfied_demands)
        max_demand = unsatisfied_demands[row_index]
        # Return if all demands are satisfied
        if max_demand <= 0:
            return
        # Find the cut that can satisfy the maximal demand
        column_index = np.argmax(self.cuts[row_index])
        cut = self.cuts[:, column_index]
        # Satisfy the max demand
        num = np.ceil(max_demand / cut[row_index]) 
        # Update solution
        self.x[column_index] += num
        self.count += num
        # Update unsatisfied demands
        unsatisfied_demands -= num * cut
        self._greedy_satisfy(unsatisfied_demands)

    @override
    def _solve(self):
        """
        Solve the cutting stock problem.
        """
        # 1. Solve the relaxed problem
        self.status = self._solve_relax()
        # 2. Round down the solution to the nearest integer
        unsatisfied_demands = self._round_down()
        # 3. Satisfy the unsatisfied demands
        self._greedy_satisfy(unsatisfied_demands)
        
        return self


if __name__ == '__main__':
    
    L = 1000
    s = [450, 350, 310, 140]
    d = [97, 610, 395, 211]
    
    cs = CutStockApprox(L, s, d)
    cs.solve().print_solution()
    