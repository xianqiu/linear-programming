from typing import override
import time

from ortools.linear_solver import pywraplp
import numpy as np

from exact import FacilityLocationExact


class _MasterProblem:

    """
    Master problem for the facility location problem.
    Args:
    f: facility open costs
    C: connection costs
    The master problem is:

    min sum(f[i] * y[i]) + z
    s.t. sum(y[i]) >= 1
         sum(alpha[j]) + sum(y[i]beta[i][j]) <= z, for all alpha, beta
    
    Note: alpha, beta are parameters.
    """

    timeout = 10  # seconds

    def __init__(self, f, C):
        self.f = f
        self.C = C
        # Solution
        self.y = None
        self.objective = None
        self.status = None
        # Solver
        self._solver = None
        self._y_var = None
        self._z_var = None
        self._formulate()

    def _decision_variables(self):
        m = len(self.f)
        self._y_var = [self._solver.IntVar(0, 1, f"y-{i}") for i in range(m)]
        self._z_var = self._solver.NumVar(0, self._solver.infinity(), "z")

    def _constraints(self):
        # sum(y[i]) >= 1
        ct = self._solver.Constraint(1, self._solver.infinity(), "ct-feasibility")
        for y in self._y_var:
            ct.SetCoefficient(y, 1)

    def _objective(self):
        """
        Objective function.
        """
        # min sum(f[i] * y[i]) + z
        obj = self._solver.Objective()
        m = len(self._y_var)
        for i in range(m):
            obj.SetCoefficient(self._y_var[i], float(self.f[i]))
        obj.SetCoefficient(self._z_var, 1)
        obj.SetMinimization()

        return obj

    def _formulate(self):
        """
        Formulate the master problem.
        """
        self._solver = pywraplp.Solver.CreateSolver("CBC")
        self._solver.set_time_limit(self.timeout * 1000)
        self._decision_variables()
        self._constraints()
        self._objective()

    def solve(self):
        """
        Solve the master problem.
        """
        status = self._solver.Solve()
        if status == pywraplp.Solver.OPTIMAL:
            self.status = "OPTIMAL"
            self.y = np.array([y.solution_value() for y in self._y_var])
            self.objective = self._solver.Objective().Value()
        else:
            self.status = "UNKNOWN"
        return self

    def add_constraint(self, alpha, beta):
        """
        Add the following constraint:
            sum(alpha[j]) <= z + sum(beta[i][j] * y[i])
        """
        ct = self._solver.Constraint(sum(alpha), self._solver.infinity())
        ct.SetCoefficient(self._z_var, 1)
        m = len(self._y_var)
        for i in range(m):
            ct.SetCoefficient(self._y_var[i], sum(beta[i]))
       

class _Subproblem:

    """
    Subproblem for the facility location problem.
    Args:
    C: connection costs
    y: solution of the master problem

    The subproblem is:
    
    max sum(alpha[j]) - sum(beta[i][j] * y[i]) 
        s.t. alpha[j] + beta[i][j] <= C[i][j], for all i, j
             beta[i][j] >= 0, for all i, j
    Note: 
    1. alpha, beta are decision variables.
    2. y is parameter.
    """

    timeout = 10  # seconds

    def __init__(self, C, y):
        self.C = np.array(C)
        self.y = np.array(y)
        self.m, self.n = self.C.shape
        # Solution
        self.alpha = None
        self.beta = None
        self.objective = None
        self.status = None
        # Solver
        self._solver = None
        self._alpha_var = None
        self._beta_var = None
        self._cts = []
        self._obj = None
        self._formulate()

    def _decision_variables(self):
        inf = self._solver.infinity()
        self._alpha_var = [self._solver.NumVar(-inf, inf, f"alpha-{j}") 
                    for j in range(self.n)]
        self._beta_var = [[self._solver.NumVar(0, inf, f"beta-{i}-{j}") for j in range(self.n)] 
                for i in range(self.m)]
    
    def _constraints(self):
        # alpha[j] - beta[i][j] <= C[i][j] for all i, j
        inf = self._solver.infinity()
        for i in range(self.m):
            ct_row = []
            for j in range(self.n):
                ct = self._solver.Constraint(-inf, float(self.C[i][j]), f"ct-{i}-{j}")
                ct.SetCoefficient(self._alpha_var[j], 1)
                ct.SetCoefficient(self._beta_var[i][j], -1)
                ct_row.append(ct)
            self._cts.append(ct_row)

    def _objective(self):
        # max sum(alpha[j]) - sum(beta[i][j] * y[i])
        self._obj = self._solver.Objective()
        for j in range(self.n):
            self._obj.SetCoefficient(self._alpha_var[j], 1)
        for i in range(self.m):
            for j in range(self.n):
                self._obj.SetCoefficient(self._beta_var[i][j], -self.y[i])  
        self._obj.SetMaximization()

    def _formulate(self):
        """
        Formulate the subproblem.
        """
        self._solver = pywraplp.Solver.CreateSolver("GLOP")
        self._solver.set_time_limit(self.timeout * 1000)
        self._decision_variables()
        self._constraints()
        self._objective()
        
    def solve(self):
        """
        Solve the sub problem.
        """
        status = self._solver.Solve()
        # Save solution
        if status == pywraplp.Solver.OPTIMAL:
            self.status = "OPTIMAL"
            self.alpha = np.array([self._alpha_var[j].solution_value() for j in range(self.n)])
            self.beta = np.array([[self._beta_var[i][j].solution_value() for j in range(self.n)]
                                    for i in range(self.m)])
            self.objective = self._obj.Value()
        else:
            print(f"sub: {status}")
            self.status = "UNKNOWN"

        return self
    
    @property
    def x(self):
        """
        Return the dual solution.
        """
        return np.array([[self._cts[i][j].dual_value()
                    for j in range(self.n)]
                    for i in range(self.m)])


class _BendersProcess:
    """
    Benders decomposition for the facility location problem.
    """

    timeout = 30
    print_info = True

    def __init__(self, f, C):
        self._start = time.time()
        self.f = np.array(f)
        self.C = np.array(C)
        # Solution
        self.x = None
        self.y = None
        self.objective = None
        self.status = None

    def solve(self):
        """
        Solve the facility location problem.
        """
        # Initialization
        master = _MasterProblem(self.f, self.C)
        master.solve()
        lb = master.objective
        ub = np.inf
        iteration = 0

        while True:
            
            # 1. Solve the subproblem
            sub = _Subproblem(self.C, master.y)
            sub.solve()
            if sub.objective is None:
                self.status = "UNKNOWN"
                print(">> Sub Unsolved.")
                break

            # update upper bound
            ub = min(ub, self.f @ np.array(master.y) + sub.objective)
            # Check the gap
            if (ub - lb)/ub < 1e-6:
                break

            # 2. Generate row
            master.add_constraint(sub.alpha, sub.beta)
            
            # 3. Solve the master problem
            master.solve()
            if master.objective is None:
                self.status = "UNKNOWN"
                print(">> Master Unsolved.")
                break
            # update lower bound
            lb = master.objective

            if time.time() - self._start > self.timeout:
                self.status = "TIMEOUT"
                break 

            # Print iteration
            if self.print_info:
                print(f"[iter {iteration}] LB = {lb:.2f}, UB = {ub:.2f}, Gap = {ub-lb:.2f}")
            iteration += 1
            
        # Save solution
        self.y = master.y
        self.x = sub.x
        self.objective = ub
        if self.status is None:
            self.status = "OPTIMAL"

        return self
        

class FacilityLocationBenders(FacilityLocationExact):
    
    """
    Benders decomposition for the facility location problem.
    """

    timeout = 30
    print_info = True

    def __init__(self, f, C):
        self._start = time.time()
        super().__init__(f, C)
    
    @override
    def solve(self):
        """
        Solve the facility location problem.
        """
        bp = _BendersProcess(self.f, self.C)
        bp.timeout = self.timeout
        bp.print_info = self.print_info
        bp.solve()
        self.x = bp.x
        self.y = bp.y
        self.objective = bp.objective
        self.status = bp.status

        return self


if __name__ == "__main__":
    _m = 20
    _n = 200
    f = np.random.randint(10, 100, _m)
    C = np.random.randint(1, 20, (_m, _n))
    fl = FacilityLocationBenders(f, C)
    fl.solve().print_solution()
