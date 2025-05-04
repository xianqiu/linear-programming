import json
import re

import requests


def test_generate():
    url = "http://localhost:8000/generate"
    response = requests.get(url)
    content = response.json()
    print("-" * 50)
    print("[Test Generate]")
    print(f"|-- URL = {url}")
    print(f"|-- Response = {content}")
    return content


def test_solve(board=None):
    url = "http://localhost:8000/solve"
    headers = {"Content-Type": "application/json"}
    if board is None:
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
    response = requests.post(url, headers=headers, 
                            data=json.dumps({"board": board}))
    content = response.json()
    print("-" * 50)
    print("[Test Generate]")
    print(f"|-- URL = {url}")
    print(f"|-- status = {content["status"]}")
    print(f"|-- solution = {content["solution"]}")

    return content


def test_generate_and_solve():
    """
    Generate a Sudoku puzzle and solve it.
    """
    board = test_generate()["board"]
    test_solve(board)


def test():
    test_generate()
    test_solve()
    test_generate_and_solve()


if __name__ == "__main__":
    test()
    