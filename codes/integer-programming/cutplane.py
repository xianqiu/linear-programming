from ortools.linear_solver import pywraplp
import numpy as np


class LPSolver:

    """ Use ortools to solve a linear program instance.
        The instance is defined as:
            max c^T x
            s.t. Ax = b
                 x >= 0
        where:
            c: n-dim vector
            A: m x n matrix
            b: m-dim vecto
    """

    def __init__(self, A, b, c):
        self.A = np.array(A)
        self.b = np.array(b)
        self.c = np.array(c)
        self.m = len(b)
        self.n = len(c)
        self.solution = None
        self.objective = None
        self.status = None
        self._solver = None  # solver
        self._x = None  # decision variables
        self._obj = None  # objective function

    def _formulate(self):
        """ Formulate the LP instance.
        """
        # Create the linear solver with the CLP backend.
        # DO NOT use GLOP, which does not recongize UNBOUNDED case.
        self._solver = pywraplp.Solver.CreateSolver('CLP')
        # Decision variables.
        self._x = [self._solver.NumVar(0, self._solver.infinity(), f"x-{j}") 
                    for j in range(self.n)]
        # Constraints: Ax = b
        for i in range(self.m):
            ct = self._solver.Constraint(float(self.b[i]), float(self.b[i]), f"ct-{i}")
            for j in range(self.n):
                ct.SetCoefficient(self._x[j], float(self.A[i][j]))
        # Objective function
        self._obj = self._solver.Objective()
        for j in range(self.n):
            self._obj.SetCoefficient(self._x[j], float(self.c[j]))
        self._obj.SetMaximization()
    
    @staticmethod
    def _status_to_string(solver_status):
        """ Convert the solver status to string.
        """
        if solver_status == pywraplp.Solver.OPTIMAL:
            return 'OPTIMAL'
        elif solver_status == pywraplp.Solver.UNBOUNDED:
            return 'UNBOUNDED'
        elif solver_status == pywraplp.Solver.INFEASIBLE:
            return 'INFEASIBLE'
        else:
            return 'UNKNOWN'

    def solve(self):
        """ Solve the instance.
        """
        # Formulate the LP instance.
        self._formulate()
        # Solve
        status = self._solver.Solve()
        if status == self._solver.OPTIMAL:
            self.solution = [self._x[j].solution_value() for j in range(self.n)]
            self.objective = self._obj.Value()
        
        self.status = self._status_to_string(status)
        
        return self

    @property
    def basic_vars(self):
        """ Return the basic variables.
        """
        return [j for j in range(self.n) 
                if self._x[j].basis_status() == self._solver.BASIC]

    @property
    def nonbasic_vars(self):
        """ Return the nonbasic variables.
        """
        return [j for j in range(self.n)
                if self._x[j].basis_status() != self._solver.BASIC]

    @property
    def B(self):
        """
        Return the basis matrix.
        """
        return self.A[:, self.basic_vars]
    
    @property
    def N(self):
        """
        Return the nonbasis matrix.
        """
        return self.A[:, self.nonbasic_vars]


class CutPlane:

    """ Cutting Plane Method.
    """

    print_info = True
    max_iter = 1000

    def __init__(self, A, b, c):
        self.A = np.array(A)
        self.b = np.array(b)
        self.c = np.array(c)
        self.solution = None
        self.objective = None
        self.status = None
        self._iter = 0  # iteration counter
        # Number of original variables
        self.n0 = len(c)
        # Reformat A and c
        self._add_slack_variables()
    
    def _add_slack_variables(self):
        """ Add slack variables to the LP instance.
        """
        # Introduce m slack variables
        m = self.A.shape[0]
        # Reformat A
        self.A = np.hstack((self.A, np.eye(m)))
        # Reformat c
        self.c = np.hstack((self.c, np.zeros(m)))

    def _remove_redundant_constraints(self, lp):
        """ Remove redundant constraints from the LP instance.
        """
        m = len(lp.A)
        m0 = len(lp.basic_vars)
        if m > m0:
            # Remove redundant constraints
            lp.A = lp.A[lp.basic_vars, :]
            lp.b = lp.b[lp.basic_vars]
            lp.c = np.hstack((self.c[lp.basic_vars], self.c[lp.nonbasic_vars]))    
            self.A = lp.A
            self.b = lp.b
            self.c = lp.c      

    def _solve_lp(self):
        """ Solve the LP instance.
        """
        lp = LPSolver(self.A, self.b, self.c)
        lp.solve()
        return lp

    def _generate_cuts(self, lp):
        """ Generate cuts from the LP instance.

        The cuts are defined as a tuple (F, f) such that
            F x <= f,
        where F is a matrix and f is a vector.
            
        Args:
            lp: LPSolver instance.
        Returns: cuts, a list of tuples (F, f).
        """
        self._remove_redundant_constraints(lp)
        # F
        A_tilde = np.linalg.inv(lp.B) @ lp.N
        A_tilde_floor = np.floor(A_tilde)
        F_N = A_tilde - A_tilde_floor
        F = np.zeros((len(F_N), self.A.shape[1]))
        F[:, lp.nonbasic_vars] = F_N
        # f
        b_tilde = np.linalg.inv(lp.B) @ lp.b
        b_tilde_floor = np.floor(b_tilde)
        f = b_tilde - b_tilde_floor
        
        return F, f

    def _add_cuts(self, cuts):
        """ Add cuts to the LP instance.
        Args:
            cuts: a list of tuples (F, f).
        """
        F, f = cuts
        # Reformate A
        self.A = np.vstack((self.A, F))
        # Reformate b
        self.b = np.hstack((self.b, f))
      
        # Add slack variables
        # Reformat A
        m, n = self.A.shape
        k = len(F)
        self.A = np.hstack((self.A, np.zeros((m, k))))
        np.fill_diagonal(self.A[m-k:, n:], -1)
        # Reformate c
        self.c = np.hstack((self.c, np.zeros(k)))

    def _is_feasible(self, solution):
        """ Check if the solution is integer.
        """
        if solution is None:
            return False
        for x in solution:
            if not np.isclose(x, np.round(x)):
                return False
        return True

    def _print_iteration(self, lp, enable=True):
        """ Print the iteration.
        """
        if not enable:
            return
        print(f'>> Iteration {self._iter}:')
        print(f'   |-- LP solution: {lp.solution}')
        print(f'   |-- LP objective: {lp.objective}')
        print(f'   |-- LP basic variables: {lp.basic_vars}')
        print(f'   |-- LP nonbasic variables: {lp.nonbasic_vars}')
    
    def solve(self):
        """ Solve the problem.
        """
        # Solve the LP instance
        lp = self._solve_lp()
        while lp.status == "OPTIMAL" and not self._is_feasible(lp.solution):
            self._print_iteration(lp, self.print_info)
            if self._iter == self.max_iter:
                self.status = "MAX_ITER"
                return self
            # Generate cuts
            cuts = self._generate_cuts(lp)
            # Add cuts
            self._add_cuts(cuts)
            # Solve the LP instance
            lp = self._solve_lp()
            # Update iteration counter
            self._iter += 1
        self._print_iteration(lp, self.print_info)
        
        self.status = lp.status
        if self.status == "OPTIMAL":
            self.solution = lp.solution[:self.n0]
            self.objective = lp.objective
        elif self.status == "UNBOUNDED":
            self.objective = np.inf
            
        return self


if __name__ == '__main__':

    A = [[1, 4], 
        [3, -4]]
    b = [10, 6]
    c = [4, 5]

    solver = CutPlane(A, b, c)
    solver.solve()
    print("-"*20)
    print(f"Solution: {solver.solution}")
    print(f"Objective: {solver.objective}")
    print(f"Status: {solver.status}")
    
    