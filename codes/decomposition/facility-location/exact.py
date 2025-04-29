from ortools.linear_solver import pywraplp
import numpy as np


class FacilityLocationExact:

    """
    Exact solution of the facility location problem.
    Args:
    f: facility open costs
    C: connection costs

    The problem is:
    min sum(f[i] * y[i]) + sum(C[i][j] * x[i][j])
    s.t. sum(x[i][j]) = 1, for all j
         sum(x[i][j]) <= y[i], for all i
         x[i][j] >= 0, for all i, j
         y[i] in {0, 1}, for all i, j
    """

    timeout = 30  # in seconds
    
    def __init__(self, f, C):
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
        solver = pywraplp.Solver.CreateSolver('CBC')
        solver.set_time_limit(self.timeout * 1000)
        # Decision variables.
        m = len(self.f)
        n = len(self.C[0])
        x = [[solver.NumVar(0, 1, f"x-{i}-{j}") for j in range(n)] for i in range(m)]
        y = [solver.IntVar(0, 1, f"y-{i}") for i in range(m)]
        # Constraints
        # sum(x[i][j]) = 1 for all j
        for j in range(n):
            ct = solver.Constraint(1, 1, f"ct-{j}")
            for i in range(m):
                ct.SetCoefficient(x[i][j], 1)
        # x[i][j] <= y[i] for all i
        for i in range(m):
            for j in range(n):
                ct = solver.Constraint(-1, 0, f"ct-{i}-{j}")
                ct.SetCoefficient(x[i][j], 1)
                ct.SetCoefficient(y[i], -1)

        # Objective function
        # min sum(f[i] * y[i] + C[i][j] * x[i][j]) for all i, j
        obj = solver.Objective()
        for i in range(m):
            obj.SetCoefficient(y[i], float(self.f[i]))
            for j in range(n):
                obj.SetCoefficient(x[i][j], float(self.C[i][j]))

        obj.SetMinimization()

        # Solve
        status = solver.Solve()
        if status == solver.OPTIMAL:
            self.x = np.array([[x[i][j].solution_value() for j in range(n)] 
                                for i in range(m)]).reshape(m, n)
            self.y = np.array([y[i].solution_value() for i in range(m)])
            self.objective = solver.Objective().Value()
            self.status = "OPTIMAL"
        else:
            self.status = "UNKNOWN"
        
        return self

    def print_solution(self):

        if self.status == "UNKNOWN":
            print("Solution is unknown")
            return
        
        open_facilities = np.where(self.y == 1)[0]
        connections = {
            int(i): np.where(self.x[i] == 1)[0].tolist() 
            for i in open_facilities
        }
        print("-" * 50)
        print(f"Solution: {self.status}")
        print(f"|-- Objective: {self.objective}")
        print(f"|-- Open facilities: {open_facilities}")
        print(f"|-- Connections")
        for i in connections:
            print(f"    |-- Facility {i}: {connections[i]}")
        print("-" * 50)


if __name__ == '__main__':
    _m = 20
    _n = 200
    f = np.random.randint(10, 100, _m)
    C = np.random.randint(1, 20, (_m, _n))
    fl = FacilityLocationExact(f, C)
    fl.solve().print_solution()
    
    