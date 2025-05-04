from generator import SodukuGenerator
from solver import SudokuSolver


def check_board(board):
    """
    Check if the board is valid.
    :param board: a 9x9 numpy array
    :return: True if the board is valid, False otherwise
    """
    # Check rows
    for i in range(9):
        row = board[i][board[i]!= 0]
        if len(row) != 9:
            return False
    # Check columns
    for i in range(9):
        col = board[:, i][board[:, i]!= 0]
        if len(col) != 9:
            return False
    # Check blocks
    for i in range(3):
        for j in range(3):
            if len(set(board[i*3:i*3+3, j*3:j*3+3].flatten()))!= 9:
                return False
    return True


def test_one():
    """ 
    Test the solver with one instance.
    Return:
        True if the solver can solve the board, False otherwise.
    """
    board = SodukuGenerator().generate()
    solver = SudokuSolver(board)
    solver.solve()
    if solver.status == "SOLVED":
        assert check_board(solver.board), "The board is not valid"
        return True
    else:
        return False


def tests():
    n = 100
    count = 0
    for _ in range(n):
        print(f"[Test] Solving instance {count+1}/{n}")
        if test_one():
            count += 1
    print(f"[Test Passed] Solved {count}/{n} instances.")


if __name__ == '__main__':
    tests()
    