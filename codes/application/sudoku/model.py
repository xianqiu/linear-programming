from ortools.linear_solver import pywraplp
import numpy as np


class SudokuModel(object):

    def __init__(self, a):
        """
        :param a: a[i][j][p][q][n] = 1 if n is in cell [i][j][p][q] else 0
        """
        self._a = a  # model input
        self.x = None  # solution 
        self._solver = pywraplp.Solver.CreateSolver("CBC")
        # self._solver = pywraplp.Solver('SudokuModel',
        #                               pywraplp.Solver.BOP_INTEGER_PROGRAMMING)
        self._x_var = None  # decision variables
        
    def _decision_variables(self):
        self._x_var = np.empty((3, 3, 3, 3, 9)).tolist()
        for i in range(3):
            for j in range(3):
                for p in range(3):
                    for q in range(3):
                        for n in range(9):
                            # Constraint set 1: Do not change existed numbers
                            # x[i][j][p][q][n] >= a[i][j][p][q][n]
                            self._x_var[i][j][p][q][n] \
                                = self._solver.IntVar(self._a[i][j][p][q][n], 1,
                                                      'x[%d][%d][%d][%d][%d]' % (i, j, p, q, n))

    def _constraints(self):
        # Constraint set 2: One number in each cell
        # sum(x[i][j][p][q][n]) = 1, over n
        for i in range(3):
            for j in range(3):
                for p in range(3):
                    for q in range(3):
                        ct = self._solver.Constraint(1, 1)
                        for n in range(9):
                            ct.SetCoefficient(self._x_var[i][j][p][q][n], 1)
        # Constraint set 3: Each block contains number 1-9
        # sum(x[i][j][p][q][n]) = 1, over p, q
        for i in range(3):
            for j in range(3):
                for n in range(9):
                    ct = self._solver.Constraint(1, 1)
                    for p in range(3):
                        for q in range(3):
                            ct.SetCoefficient(self._x_var[i][j][p][q][n], 1)
        # Constraint set 4: Each row contains number 1-9
        # sum(x[i][j][p][q][n]) = 1, over j, q
        for i in range(3):
            for p in range(3):
                for n in range(9):
                    ct = self._solver.Constraint(1, 1)
                    for j in range(3):
                        for q in range(3):
                            ct.SetCoefficient(self._x_var[i][j][p][q][n], 1)
        # Constraint set 5: Each column contains number 1-9
        # sum(x[i][j][p][q][n]) = 1, over i, p
        for j in range(3):
            for q in range(3):
                for n in range(9):
                    ct = self._solver.Constraint(1, 1)
                    for i in range(3):
                        for p in range(3):
                            ct.SetCoefficient(self._x_var[i][j][p][q][n], 1)

    def solve(self):
        self._decision_variables()
        self._constraints()
        status = self._solver.Solve()
        if status == pywraplp.Solver.OPTIMAL or pywraplp.Solver.FEASIBLE:    
            self._get_solution()

    def _get_solution(self):
        self.x = np.zeros((3, 3, 3, 3, 9)).astype(int)
        for i in range(3):
            for j in range(3):
                for p in range(3):
                    for q in range(3):
                        for n in range(9):
                            self.x[i][j][p][q][n] = self._x_var[i][j][p][q][n].solution_value()
                              


if __name__ == '__main__':
    
    a = np.zeros((3, 3, 3, 3, 9))

    # Block[0][0]
    a[0][0][0][1][1] = 1 
    a[0][0][2][0][0] = 1
    # Block[0][1]
    a[0][1][0][1][2] = 1
    # Block[0][2]
    a[0][2][0][1][8] = 1
    a[0][2][2][0][6] = 1
    # Block[1][0]
    a[1][0][1][0][4] = 1
    a[1][0][2][2][6] = 1
    # Block[1][1]
    a[1][1][0][1][3] = 1
    a[1][1][1][1][5] = 1
    # Block[1][2]
    a[1][2][0][1][5] = 1
    a[1][2][0][2][1] = 1
    # Block[2][0]
    a[2][0][0][2][8] = 1
    a[2][0][1][1][3] = 1
    # Block[2][1]
    a[2][1][0][0][6] = 1
    a[2][1][0][2][0] = 1
    a[2][1][2][0][4] = 1
    # Block[2][2]
    a[2][2][1][1][1] = 1

    sm = SudokuModel(a)
    sm.solve()
    print(f"Solution:\n {sm.x}")
    