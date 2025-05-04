---
weight: 830
title: "代码"
description: ""
icon: "article"
date: "2025-04-29T20:50:54+08:00"
lastmod: "2025-04-29T20:50:54+08:00"
draft: false
toc: true
---

我们已经实现了 `SudokuModel` 类，它可以用来解数独游戏。但是用起来有些麻烦。如前文所述，首先需要把问题转换成模型的输入，最后把模型的输出转换成对应的数字。手动操作还容易出错。

为了解决这个麻烦。我们打算给 `SudokuModel` 增加一个功能，即自动转换模型的输入和输出。注意，增加新功能不需要在  `SudokuModel` 类中进行修改，只需要把它封装成一个新的类即可。

### SudokuSolver

定义 `SudokuSolver` 类，作为数独游戏的求解器。它的输入 `board` 是一个 `9*9` 的矩阵。矩阵中的数字代表填入的数字， `0` 代表空格子。


```python
import numpy as np


class SudokuSolver:

    def __init__(self, board):
        """
        :param board: a 9x9 array of integers in 0-9, 0 for empty cells
        """
        self.board = np.array(board).astype(int)
        self.status = None

    def solve(self):
        """
        Solve the Sudoku puzzle
        """
        pass
```
其中 `solve` 方法调用 `SudokuModel` 进行求解，并把结果转换成 `9*9` 矩阵，保存在成员变量 `self.board` 中。`self.status` 是解的状态，表示否有解。

看这个例子。

{{< figure src="sudoku.png" width="320px" class="text-center">}}

可以这样求解。

```python
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
```

接下来讲一下  `SudokuSolver` 的实现。

定义如下两个方法。

* `_to_model_input`：把数独的输入 `9*9` 矩阵转换成模型 `SudokuModel` 的输入 `a`
* `_to_solution`：把模型 `SudokuModel` 的输出转换成数独的输出，即 `9*9` 矩阵。

```python
class SudokuSolver:

    def _to_model_input(self):
        """
        Convert the board to model input
        :return: a[i][j][p][q][n] = 1 if n is in cell [i][j][p][q] else 0
        """
        pass

    def _to_solution(self, x):
        """
        Convert the model solution to a 9x9 array of integers in 1-9
        :param x: model solution (same format as model input a)
        :return: 9x9 array of integers in 1-9
        """
        pass
```

`solve` 就可以这样实现。

```python
class SudokuSolver:

    # ...

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
```

这样一来，我们能够方便地求解数独游戏。

### SudokuGenerator

但是还有一个小问题，数独的例子从哪里来。如果能够自动地生成例子，那就更好了。定义类 `SudokuGenerator` 用来生成数独的例子。

```python
class SodukuGenerator:

    """
    Use SodokuSolver to generate a board with n numbers.
    The generated board is a 9x9 array of integers in 1-9.
    """
    
    def __init__(self):
        self._board = np.zeros((9, 9))
        # Generate n numbers
        self._n = np.random.randint(20, 40)

    def generate(self):
        """
        Generate a sudoku board
        :return: a 9x9 array of integers in 1-9
        """
        # ...
        return self._board
```

其中 `self._n` 表示已知数字的个数。

为了简单起见，可以用  `SudokuModel` 生成。随机选一个 `1-9` 的数字，然后用 `SudokuModel` 求解，如果有解就填入这个数字，无解就换一个数字。重复几次这个操作，目的是得到一个随机的可行解。最后随机选择 `91-n` 个位置，把对应的数字设置为 `0`。

然后用 `SudokuGenerator` 生成数独例子。

```python
if __name__ == '__main__':
    generator = SodukuGenerator()
    board = generator.generate()
    print(board) 
```

### SudokuPuzzle

现在我们有两个类：`SudokuGenerator` 生成数独实例，`SudokuSover` 求解数独实例。为了方便用户使用，把它们封装成一个类 `SudokuPuzzle`。

```python
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
```

这样一来，用户就可以这样使用调用。

```python
if __name__ == "__main__":
    board = SudokuPuzzle.generate()
    print("\n** Sudoku Puzzle **\n", board)
    solution = SudokuPuzzle.solve(board)
    print("\n** Sudoku Solution **\n", solution)
```

总结一下。 `SudokuPuzzle` 就是提供给用户使用的接口类。它有两个方法：`SudokuPuzzle.genearate` 用来生成数独实例，`SudokuSolver.solve` 用来求解数独实例。

此外，为了使用上的方便。还可以把 `SudokuPuzzle` 打包成一个 `Python Package`。这样就可以通过 `pip install <my_package>` 的方式安装相关代码。具体方法可以参考 [Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)。

但是还有一个问题。用户要使用这个包，需要了解 `Python` 编程，因此有一定的使用门槛。为了降低使用门槛，可以把它封装成一个网络服务。这样一来，如果用户不会 `python`，而是熟悉其他语言，例如 `Javascript, Java, C++` 等，可以通过调用网络服务来使用对应的功能。

### 代码

相关代码在文件夹  [`codes/application/sudoku`](https://github.com/xianqiu/linear-programming/tree/main/codes/application/sudoku) 。

* [puzzle.py](https://github.com/xianqiu/linear-programming/tree/main/codes/application/sudoku/puzzle.py) 提供给用户的接口类
  * [solver.py](https://github.com/xianqiu/linear-programming/tree/main/codes/application/sudoku/solver.py) 数独实例的求解器
  * [generator.py](https://github.com/xianqiu/linear-programming/tree/main/codes/application/sudoku/generator.py) 数独实例的生成器
  * [model.py](https://github.com/xianqiu/linear-programming/tree/main/codes/application/sudoku/model.py) 数独整数模型的求解器

