import numpy as np

from common import Status


class SimplexBasic:

    # maximum number of iterations
    max_iter = 1_000
    print_iter = True
    
    def __init__(self, A, b, c, s):
        """
        A: matrix of coefficients of the constraints
        b: vector of right-hand side values
        c: vector of coefficients of the objective function
        s: vector of indices of the initial basic feasible variables
        """
        self.A = np.array(A)
        self.b = np.array(b)
        self.c = np.array(c)
        self.m = len(A)
        self.n = len(A[0])
        self._basic_vars = s
        self._nonbasic_vars = [i for i in range(self.n) if i not in s]
        self.status = None  # optimal or unbounded
        self._iter = 0
        self._check()
        
    def _check(self):
        # Check if the instance is valid
        # A is full rank
        assert np.linalg.matrix_rank(self.A) == self.m, "A is not full rank"
        # b is a vector of length m and non-negative
        assert len(self.b) == self.m, "b is not of length m"
        assert np.all(self.b >= 0), "b is not non-negative"
        # c is a vector of length n
        assert len(self.c) == self.n, "c is not of length n"
        # s is a vector of length m
        assert len(self._basic_vars) == self.m, "s is not of length m"
        # Basic matrix is invertible
        assert np.linalg.matrix_rank(self._B) == self.m, "s is not a basic feasible solution"
        
    @property
    def _B(self):
        # Basic matrix
        return self.A[:, self._basic_vars]
    
    @property
    def _N(self):
        # Non-basic matrix
        return self.A[:, self._nonbasic_vars]

    @property
    def _x(self):
        # Solution vector
        x = np.zeros(self.n)
        x[self._basic_vars] = np.linalg.inv(self._B) @ self.b
        return x

    @property
    def _cB(self):
        # Basic cost vector
        return self.c[self._basic_vars]

    @property
    def _cN(self):
        # Non-basic cost vector
        return self.c[self._nonbasic_vars]
    
    @property
    def _xB(self):
        # Basic solution vector
        return self._x[self._basic_vars]

    @property
    def _xN(self):
        # Non-basic solution vector
        return self._x[self._nonbasic_vars]

    def _reduced_costs(self):
        # Calculate the reduced costs
        mu = np.zeros(self.n)
        mu[self._nonbasic_vars] = self._cN - self._cB @ np.linalg.inv(self._B) @ self._N
        return mu
    
    def _is_optimal(self):
        # Check if the current solution is optimal
        mu = self._reduced_costs()
        return np.all(mu >= 0)

    def _find_entering_var(self):
        # Find the entering variable
        mu = self._reduced_costs()
        return int(np.argmin(mu))
    
    def _find_leaving_var(self, j):
        # Find the leaving variable
        # j is the index of the entering variable
        b_tilde = self._xB
        A_tilde = np.zeros((self.m, self.n))
        A_tilde[:, self._nonbasic_vars] = np.linalg.inv(self._B) @ self._N
        # A_tilde_j is the j-th column of A_tilde
        A_tilde_j = A_tilde[:, j]
        ratio = np.zeros(self.m)
        for i in range(self.m):
            if A_tilde_j[i] > 0:
                ratio[i] = b_tilde[i] / A_tilde_j[i]
            else:
                ratio[i] = np.inf

        if np.all(ratio == np.inf):
            return None  # Unbounded

        i_index = int(np.argmin(ratio))
        return self._basic_vars[i_index]

    def _update(self, i, j):
        """
        Update the basic and non-basic variables.
        1. remove i from self._basic_vars and add j to self._basic_vars
        2. remove j from self._nonbasic_vars and add i to self._nonbasic_vars
        Args:
        i: leaving variable
        j: entering variable
        """
        i_idx = self._basic_vars.index(i)
        self._basic_vars[i_idx] = j
        j_idx = self._nonbasic_vars.index(j)  
        self._nonbasic_vars[j_idx] = i

    def _print_iteration(self, enable=True):
        if not enable:
            return
        print(f"Iteration {self._iter}:")
        print(f"Reduced costs: {self._reduced_costs()}")
        print(f"Basic variables: {self._basic_vars}")
        print(f"Non-basic variables: {self._nonbasic_vars}")
        print(f"Solution vector: {self._x}")
        print(f"Objective value: {self.objective}")
        print("------------------------")

    def solve(self):
        # Iterate until the solution is optimal,
        # or the maximum number of iterations is reached

        self._print_iteration(self.print_iter)
        while not self._is_optimal():
            self._iter += 1
            if self._iter > self.max_iter:
                self.status = Status.MAX_ITER
                return
            entering_var = self._find_entering_var()
            leaving_var = self._find_leaving_var(entering_var)
            if leaving_var is None:
                self.status = Status.UNBOUNDED
                return

            self._update(leaving_var, entering_var)
            self._print_iteration(self.print_iter)
            
        self.status = Status.OPTIMAL

        return self

    @property
    def solution(self):
        return self._x

    @property
    def objective(self):
        return self._cB @ self._xB


if __name__ == '__main__':
    # example
    A = [
        [3, 1, 1, 0, 0], 
        [1, 2, 0, 1, 0], 
        [1, 0, 0, 0, 1]
    ]
    b = [120, 160, 35]
    c = [-7, -6, 0, 0, 0]
    s = [2, 3, 4]

    simplex = SimplexBasic(A, b, c, s)
    simplex.solve()
    print(f"status = {simplex.status}")