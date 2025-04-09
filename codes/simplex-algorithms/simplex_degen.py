from typing import override

import numpy as np

from simplex_basic import SimplexBasic


class SimplexDegen(SimplexBasic):

    @override
    def _find_leaving_var(self, j):
        I0 = self._I0(j)
        if len(I0) == 0:
            return None  # Unbounded
        I_final = self._I_next(j, I0, 0)
        i_index = int(I_final[0])
        return self._basic_vars[i_index]

    def _I0(self, j):
        """
        Minimum Ratio Test.
        I0 = {i | tilde_b / tilde_a_ij is minimized, and tilde_a_ij > 0}
        Args:
        j: entering variable
        """
        b_tilde = self._xB
        A_tilde = np.zeros((self.m, self.n))
        A_tilde[:, self._nonbasic_vars] = np.linalg.inv(self._B) @ self._N
        # A_tilde_j is the j-th column of A_tilde
        A_tilde_j = A_tilde[:, j]
        ratio = np.zeros(self.m)
        for i in range(self.m):
            if A_tilde_j[i] > 0:
                # use abs(b_tilde[i]) instead of b_tilde[i] to avoid negative b_tilde[i]
                # because floating error may cause negative b_tilde[i], e.g. -1e-16
                ratio[i] = abs(b_tilde[i]) / A_tilde_j[i]
            else:
                ratio[i] = np.inf

        if np.all(ratio == np.inf):
            return []  # Unbounded
        
        min_ratio = np.min(ratio)
        I0 = np.where(ratio == min_ratio)[0]
        I0 = [int(i) for i in I0]
        
        return I0

    def _I_next(self, j, I, k):
        """
        Given I_k, find I_{k+1}, I_{k+2}, ... until it contains only one element.
        I_{k+1} = {i | a_ik / a_ij is minimized and i in I_k}
        Args:
        j: entering variable
        I: I_k
        k: k-th column of A
        """
        if len(I) <= 1:
            return I
        tilde_a_k = np.linalg.inv(self._B) @ self.A[:, k]
        tilde_a_j = np.linalg.inv(self._B) @ self.A[:, j]
        ratio = np.full((self.m,), np.inf)
        for i in I:
            if abs(tilde_a_j[i]) > 1e-6:
                ratio[i] = tilde_a_k[i] / tilde_a_j[i]
                
        min_ratio = np.min(ratio)
        I1 = np.where(ratio == min_ratio)[0]
        I1 = [int(i) for i in I1]
        return self._I_next(j, I1, k+1)


if __name__ == "__main__":
    # example
    A = [[0.5, -5.5, -2.5, 9, 1, 0, 0],
         [0.5, -1.5, -0.5, 1, 0, 1, 0],
         [1, 0, 0, 0, 0, 0, 1]]
    b = [0, 0, 1]
    c = [-10, 57, 9, 24, 0, 0, 0]
    s = [0, 5, 6]

    simplex = SimplexDegen(A, b, c, s)
    simplex.solve()
    print(f"status = {simplex.status}")
