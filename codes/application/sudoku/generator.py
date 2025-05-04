import numpy as np

from solver import SudokuSolver


class SodukuGenerator:

    """
    Use SodokuSolver to generate a board with n numbers.
    The generated board is a 9x9 array of integers in 1-9.
    """
    
    def __init__(self):
        self._board = np.zeros((9, 9))
        # Generate n numbers
        self._n = np.random.randint(20, 40)

    def _candidates(self, i, j):
        """
        Get candidate numbers at position (i, j)
        """
        candidates = set(range(1, 10))
        rows_numbers = set(self._board[i, :])
        cols_numbers = set(self._board[:, j])
        block_numbers = set(self._board[i // 3 * 3: i // 3 * 3 + 3, j // 3 * 3: j // 3 * 3 + 3].flatten())
        candidates = candidates - rows_numbers - cols_numbers - block_numbers
        return list(candidates) 

    @property
    def _empty_positions(self):
        """
        Get empty positions of numbers
        """
        return [(i, j) for j in range(9) for i in range(9) 
                if self._board[i][j] == 0]

    def _fill_one_number(self):
        """
        Fill one number at a time.
        """
        k = np.random.choice(range(len(self._empty_positions)))
        i, j = self._empty_positions[k]
        candidates = self._candidates(i, j)
        np.random.shuffle(candidates)
        for n in candidates:
            self._board[i][j] = n
            board = self._board.copy()
            solver = SudokuSolver(board)
            solver.solve()
            if solver.status == "SOLVED":
                break
            else:
                self._board[i][j] = 0

    def _mask(self, k):
        """
        Mask k numbers from the board.
        """
        positions = [(i, j) for j in range(9) for i in range(9)]
        np.random.shuffle(positions)
        for i, j in positions[:k]:
            self._board[i][j] = 0

    def generate(self):
        """
        Generate a sudoku board
        :return: a 9x9 array of integers in 1-9
        """
        for _ in range(8):
            self._fill_one_number()
        solver = SudokuSolver(self._board)
        solver.solve()
        self._board = solver.board
        # Mask numbers from the board
        self._mask(81 - self._n)

        return self._board


if __name__ == '__main__':
    generator = SodukuGenerator()
    board = generator.generate()
    print(board)  
    