import numpy as np

from simplex_twophase import SimplexTwoPhase
from common import Status


class SimplexSolver:

    # maximum number of iterations
    max_iter = 1_000

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
        # remember the original number of variables
        self.n0 = self.n 
        self._check()
        self._format()
        self._is_maximize = False
        self.objective = None
        self.solution = None
        self.status = None

    def _check(self):
        """
        Check if the instance is valid.
        """
        assert self.A.shape == (self.m, self.n), "A must be a matrix of shape (m, n)"
        assert self.b.shape == (self.m,), "b must be a vector of shape (m,)"
        assert self.c.shape == (self.n,), "c must be a vector of shape (n,)"

    def _format(self):
        """
        Format the instance to be used in the simplex algorithm.
        """
        # 1. b[i] < 0
        indices = np.where(self.b < 0)[0]
        for i in indices:
            self.A[i, :] = -self.A[i, :]
            self.b[i] = -self.b[i]
        # 2. m > n
        # add slack variables
    
        if self.m > self.n:
            self.A = np.hstack((self.A, np.zeros((self.m, self.m - self.n))))
            self.c = np.hstack((self.c, np.zeros(self.m - self.n)))
            self.m, self.n = self.A.shape

    def maximize(self):
        """
        Solve the linear program as a maximization problem.
        """
        self.c = -self.c
        self._is_maximize = True
        return self

    def solve(self):
        """
        Solve the linear program
        """
        simplex = SimplexTwoPhase(self.A, self.b, self.c)
        simplex.print_info = False
        simplex.solve()

        self.status = simplex.status

        if self.status == Status.OPTIMAL:
            if simplex.solution is not None:
                self.solution = simplex.solution[:self.n0]
            self.objective = simplex.objective
            # For maximization problem
            if self._is_maximize and self.objective is not None:
                self.objective = -self.objective

        elif self.status == Status.UNBOUNDED:
            self.objective = -np.inf
            # For maximization problem
            if self._is_maximize:
                self.objective = np.inf
                
        return self


if __name__ == '__main__':

    # example: maximization problem
    # 1. m > n; 
    # 2. with redundant rows
    # 3. with b[i] < 0
    A = [
        [3, 1, 1, 0, 0],
        [-1, -2, 0, -1, 0],
        [1, 2, 0, 1, 0],
        [-1, 0, 0, 0, -1],
        [1, 2, 0, 1, 0],  # redundant row
        [-1, 0, 0, 0, -1]  # redundant row
    ]
    b = [3, -4, 4, -1, 4, -1]  
    c = [1, 1, 0, 0, 0]
    
    simplex = SimplexSolver(A, b, c).maximize()
    simplex.solve()
    print(simplex.solution)
    print(simplex.objective)
    print(simplex.status)

    