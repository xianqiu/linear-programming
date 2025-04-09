import numpy as np

from simplex_degen import SimplexDegen
from common import Status


class SimplexTwoPhase:

    # maximum number of iterations
    max_iter = 1_000
    print_info = True

    def __init__(self, A, b, c):
        """
        A: matrix of coefficients of the constraints
        b: vector of right-hand side values
        c: vector of coefficients of the objective function
        """
        self.A = np.array(A)
        self.b = np.array(b)
        self.c = np.array(c)
        self.m, self.n = self.A.shape
        self.status = None
        self.objective = None
        self.solution = None

    def _solve_phase_one(self):
        """
        Solve phase one instance.
        """
        
        # Format phase one instance
        A = np.hstack((self.A, np.eye(self.m)))
        b = self.b
        c = np.hstack((np.zeros(self.n), np.ones(self.m)))
        # initial basic feasible solution is the identity matrix
        s = list(range(self.n, self.n + self.m))  
        
        # Solve phase one instance
        simplex = SimplexDegen(A, b, c, s)
        simplex.max_iter = self.max_iter
        simplex.print_iter = False
        simplex.solve()

        # Check feasibility
        if simplex.objective > 1e-6:
            return None

        return simplex

    def _get_basic_feasible_solution(self, simplex):
        """
        Given phase one solution, get the basic feasible solution of phase two instance.
        Args:
            simplex: SimplexDegen instance of phase one solution
        Returns:
            basic_vars: list of basic variables w.r.t. phase two instance
            redundant_rows: list of redundant rows of the original instance
        """

        basic_vars = [i for i in range(self.n) if i in simplex._basic_vars]
        redundant_rows = []
        k = len(basic_vars)
        if k == self.m:
            return basic_vars, redundant_rows

        nonbasic_vars = [i for i in range(self.n) if i in simplex._nonbasic_vars]
        # B^{-1}N columns w.r.t nonbasic variables
        nonbasic_columns = np.linalg.inv(simplex._B) @ self.A[:, nonbasic_vars]

        # Given leaving variables, find entering variables 
        # and add them to basic_vars
        index_leaving_vars = [i for i in range(self.m) if simplex._basic_vars[i] >= self.n]
        for i in index_leaving_vars:
            entering_var = None
            for j in range(self.m - k):
                if abs(nonbasic_columns[i][j]) > 1e-6:
                    entering_var = nonbasic_vars[j]
                    basic_vars.append(entering_var)
                    np.delete(nonbasic_columns, j, axis=1)
                    break
            if entering_var is None:
                # the row is redundant
                redundant_rows.append(i)

        return basic_vars, redundant_rows
    
    def _solve_phase_two(self, basic_vars, redundant_rows):
        """
        Solve phase two instance.
        Args:
            basic_vars: list of basic variables w.r.t. phase two instance
            redundant_rows: list of redundant rows of the original instance
        """
        # Format phase two instance
        A = np.delete(self.A, redundant_rows, axis=0)
        b = np.delete(self.b, redundant_rows)
        c = self.c
        s = basic_vars
        # Solve phase two instance
        simplex = SimplexDegen(A, b, c, s)
        simplex.max_iter = self.max_iter
        simplex.print_iter = False
        simplex.solve()

        return simplex

    def _print_phase(self, simplex, phase, enable=True):
        """
        Print the solution of the phase instance.
        Args:
            simplex: SimplexBasic instance of the phase instance
            phase: phase number
        """
        if not enable:
            return
        print("")    
        print(f"==== Phase {phase} ====")
        if simplex is None:
            print("|-- INFEASIBLE")
            return
        print(f"|-- Instance: ")
        print(f"    |-- A: {simplex.A}")
        print(f"    |-- b: {simplex.b}")
        print(f"    |-- c: {simplex.c}")
        print(f"|-- Solution: {simplex.solution}")
        print(f"|-- Basic variables: {simplex._basic_vars}")
        print(f"|-- Objective: {simplex.objective}")
        print(f"|-- Status: {simplex.status}")

    def _print_values(self, enable=True, **kwargs):   
        """
        Print the basic_vars and redundant_rows.
        """
        if not enable:
            return
        print("")
        print("==== Phase 2 Input ====")
        for key, value in kwargs.items():
            print(f"|-- {key}: {value}")
    
    def solve(self):
        """
        Solve the linear program
        """
        # Solve phase one instance
        simplex = self._solve_phase_one()
        self._print_phase(simplex, 1, enable=self.print_info)
        if simplex is None:
            self.status = Status.INFEASIBLE
            return
        # Get basic feasible solution of phase two instance
        basic_vars, redundant_rows = self._get_basic_feasible_solution(simplex)
        self._print_values(enable=self.print_info, 
                                    basic_vars=basic_vars, 
                                    redundant_rows=redundant_rows)
        # Solve phase two instance
        simplex = self._solve_phase_two(basic_vars, redundant_rows)
        self._print_phase(simplex, 2, enable=self.print_info)
        # Set the solution
        self.status = simplex.status
        self.objective = simplex.objective
        self.solution = simplex.solution


if __name__ == '__main__':
    # example
    A = [
        [3, 1, 1, 0, 0],
        [1, 2, 0, 1, 0],
        [1, 2, 0, 1, 0], 
        [1, 0, 0, 0, 1]
    ]
    b = [120, 160, 160, 35]
    c = [-7, -6, 0, 0, 0]
    simplex = SimplexTwoPhase(A, b, c)
    simplex.solve()
