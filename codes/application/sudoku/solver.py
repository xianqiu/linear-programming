import numpy as np

from model import SudokuModel


class SudokuSolver:

    def __init__(self, board):
        """
        :param board: a 9x9 array of integers in 0-9, 0 for empty cells
        """
        self.board = np.array(board).astype(int)
        self.status = None

    def _to_model_input(self):
        """
        Convert the board to model input
        :return: a[i][j][p][q][n] = 1 if n is in cell [i][j][p][q] else 0
        """
        a = np.zeros((3, 3, 3, 3, 9))
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    a[i//3][j//3][i%3][j%3][int(self.board[i][j])-1] = 1
        return a

    def _to_solution(self, x):
        """
        Convert the model solution to a 9x9 array of integers in 1-9
        :param x: model solution (same format as model input a)
        :return: 9x9 array of integers in 1-9
        """
        board = np.zeros((9, 9)).astype(int)
        for i in range(3):
            for j in range(3):
                for p in range(3):
                    for q in range(3):
                        board[i*3+p][j*3+q] = np.argmax(x[i][j][p][q]) + 1
        return board

    def solve(self):
        """
        Solve the Sudoku puzzle
        """
        a = self._to_model_input()
        model = SudokuModel(a)
        model.solve()
        if model.x is not None:
            self.board = self._to_solution(model.x)
            self.status = "SOLVED"
        else:
            self.status = "INFEASIBLE"


if __name__ == '__main__':

    board = [
        [0, 2, 0, 0, 3, 0, 0, 9, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 7, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 6, 2],
        [5, 0, 0, 0, 6, 0, 0, 0, 0],
        [0, 0, 7, 0, 0, 0, 0, 0, 0],
        [0, 0, 9, 7, 0, 1, 0, 0, 0],
        [0, 4, 0, 0, 0, 0, 0, 2, 0],
        [0, 0, 0, 5, 0, 0, 0, 0, 0]
    ]
    
    solver = SudokuSolver(board)
    solver.solve()
    print(f"Status: {solver.status}")
    print(f"Solution:\n {solver.board}")