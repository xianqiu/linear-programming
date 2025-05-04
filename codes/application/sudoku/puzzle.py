from generator import SodukuGenerator
from solver import SudokuSolver


class SudokuPuzzle:
    
    @staticmethod
    def genearate():
        return SodukuGenerator().generate()

    @staticmethod
    def solve(board):
        solver = SudokuSolver(board)
        solver.solve()
        if solver.status == "SOLVED":
            return solver.board
        return None


if __name__ == "__main__":
    board = SudokuPuzzle.genearate()
    print("\n** Sudoku Puzzle **\n", board)
    solution = SudokuPuzzle.solve(board)
    print("\n** Sudoku Solution **\n", solution)
    