import numpy as np


class PDInteriorPoint:

    """
    Primal-Dual Interior Point Method.
    Solve the following problem:
    --------------
    min c^T x
    s.t. Ax = b
         x >= 0
    --------------
    Note:
    1. A is full rank
    2. Bounded and feasible
    """

    max_iter = 100
    print_iter = True

    def __init__(self, A, b, c):
        """
        Args:
        A: matrix of coefficients of the constraints
        b: vector of right-hand side values
        c: vector of coefficients of the objective function
        """
        self.A = np.array(A)
        self.b = np.array(b)
        self.c = np.array(c)
        self.n = len(c)
        self.m = len(b)
        self._check()
        self.objective = None
        self.solution = None
        self.status = None
        # Initialize the primal and dual variables
        self._x = np.ones(self.n)
        self._y = np.ones(self.m)
        self._s = np.ones(self.n)
        # Small number for numerical stability
        self._epesilon = 1e-8
        # Centering parameter
        self._mu = self._x @ self._s / self.n
        # Scaling parameter of mu
        self._alpha = 0.1
        # Iteration number
        self._iter = 0
        
    def _check(self):
        if len(self.A) != self.m:
            raise ValueError("A and b must have the same number of rows")
        if len(self.A[0]) != self.n:
            raise ValueError("A and c must have the same number of columns")
        # A is full rank
        if np.linalg.matrix_rank(self.A) != self.m:
            raise ValueError("A is not full rank")
    
    def _is_optimal(self):
        # Check if the primal and dual variables are optimal
        r1 = np.linalg.norm(self.A @ self._x - self.b)
        r2 = np.linalg.norm(self.c - self.A.T @ self._y - self._s)
        r3 = abs(self._x @ self._s)
        r = max(r1, r2, r3)
        
        if r < self._epesilon:
            return True
        return False

    def _newton_direction(self):
        # Compute the Newton direction
        X = np.diag(self._x)
        S = np.diag(self._s)
        J = np.block([
            [self.A, np.zeros((self.m, self.m)), np.zeros((self.m, self.n))],
            [np.zeros((self.n, self.n)), self.A.T, np.eye(self.n)],
            [S, np.zeros((self.n, self.m)), X]
        ])
        
        r = np.block([
            self.b - self.A @ self._x,
            self.c - self.A.T @ self._y - self._s,
            self._mu * np.ones(self.n) - X @ S @ np.ones(self.n)
        ])
        # Solve the linear system J @ delta = r
        delta = np.linalg.solve(J, r)
        dx = delta[0: self.n]
        dy = delta[self.n: self.n + self.m]
        ds = delta[self.n + self.m: ]

        return dx, dy, ds

    def _update(self, dx, dy, ds):
        # step size
        alpha_p = 1
        alpha_d = 1
        r = 0.99

        for j in range(self.n):
            if dx[j] < -self._epesilon:
                alpha_p = min(alpha_p, r * (-self._x[j] / dx[j]))
            if ds[j] < -self._epesilon:
                alpha_d = min(alpha_d, r * (-self._s[j] / ds[j]))
            
        # Update the primal and dual variables
        self._x = self._x + alpha_p * dx
        self._y = self._y + alpha_d * dy
        self._s = self._s + alpha_d * ds

    def _print_iteration(self, enable=True):
        if not enable:
            return
        print(f"Iteration {self._iter}:")
        print(f"|-- Primal Solution: x = {self._x}")
        print(f"|-- Primal Objective Value: {self._x @ self.c}")    
        print(f"|-- Dual Solution: y = {self._y}, s = {self._s}")
        print(f"|-- Dual Objective Value: {self._y @ self.b}")
        print(f"|-- Primal Feasibility: r = {np.linalg.norm(self.A @ self._x - self.b)}")
        print(f"|-- Dual Feasibility: r = {np.linalg.norm(self.c - self.A.T @ self._y - self._s)}")
        print(f"|-- Duality Gap: {abs(self._x @ self._s)}")
        print(f"|-- Centering Parameter: mu = {self._mu}")
        print("------------------------")

    def solve(self):    

        while not self._is_optimal():
            self._print_iteration(self.print_iter)
            # Update the centering parameter
            self._mu = self._mu * self._alpha
            # Compute the Newton direction
            dx, dy, ds = self._newton_direction()
            # Update the primal and dual variables
            self._update(dx, dy, ds)
            self._iter += 1
            if self._iter > self.max_iter:
                self.status = "MAX_ITER"
                break

        self.objective = self.c @ self._x
        self.solution = self._x
        self.status = "OPTIMAL"


if __name__ == "__main__":
    
    # example
    A = [
        [3, 1, 1, 0, 0], 
        [1, 2, 0, 1, 0], 
        [1, 0, 0, 0, 1]
    ]
    b = [120, 160, 35]
    c = [-7, -6, 0, 0, 0]
    s = [2, 3, 4]

    pd = PDInteriorPoint(A, b, c)
    pd.solve()

    print("Objective:", pd.objective)
    print("Solution:", pd.solution)
    print("Status:", pd.status)