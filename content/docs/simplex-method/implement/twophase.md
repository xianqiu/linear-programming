---
weight: 383
title: "两阶段法"
description: ""
icon: "article"
date: "2025-03-27T13:58:44+08:00"
lastmod: "2025-03-27T13:58:44+08:00"
draft: false
toc: true
---

讲一下 [两阶段单纯形算法](../twophase) 的实现思路。

### 接口

定义类 `SimplexTwoPhase`，它的输入是 `A, b, c`。跟单纯形算法相比，它不再需要指定起点。方法 `solve` 用来求解线性规划问题，结果和状态保存在成员变量中。

```python
import numpy as np


class SimplexTwoPhase:

    def __init__(self, A, b, c):
        """
        A: matrix of coefficients of the constraints
        b: vector of right-hand side values
        c: vector of coefficients of the objective function
        """
        self.A = np.array(A)
        self.b = np.array(b)
        self.c = np.array(c)
        self.objective = None
        self.solution = None
        self.status = None

    def solve(self):
        """
        Solve the linear program.
        """
        pass
```

### 实现

回顾两阶段法，我们把它拆成三个步骤：
1. 求解一阶段问题；
2. 得到基本可行解；
3. 求解二阶段问题。

可以定义三个函数：
* `_solve_phase_one`：返回一阶段问题的解。如果最优目标函数值不等于 0，意味着原问题没有可行解，则返回空。
* `_get_basic_feasible_solution`：输入一阶段问题的解，返回基本可行解对应的基矩阵的列，以及冗余的行。
* `_solve_phase_two`：已知基本可行解以及冗余的行，求解二阶段问题。

```python
class SimplexTwoPhase:
    
    # ...
    
    def _solve_phase_one(self):
        """
        Solve phase one instance. 
        If OPT != 0, then the original problem is infeasible and return None.
        """
        # Format A, b, c, s of phase one instance
        # simplex = SimplexDegen(A, b, c, s)
        # simplex.solve()
        return simplex
        
    def _get_basic_feasible_solution(self, simplex):
        """
        Given phase one solution, get the basic feasible solution of phase two instance.
        Args:
            simplex: SimplexDegen instance of phase one solution
        Returns:
            basic_vars: list of basic variables w.r.t. phase two instance
            redundant_rows: list of redundant rows of the original instance
        """
        
    def _solve_phase_two(self, basic_vars, redundant_rows):
        """
        Solve phase two instance.
        Args:
            basic_vars: list of basic variables w.r.t. phase two instance
            redundant_rows: list of redundant rows of the original instance
        """
        pass
```

利用这三个函数，我们可以实现 `solve`。

```python
class SimplexTwoPhase:

    # ...
    
    def solve(self):
        """
        Solve the linear program.
        """
        # 1. Solve phase one instance
        simplex = self._solve_phase_one()
        
        # In case of infeasible
        if simplex is None:
            self.status = Status.INFEASIBLE
            return
        
        # 2. Get basic feasible solution of phase two instance
        basic_vars, redundant_rows = self._get_basic_feasible_solution(simplex)
        
        # 3. Solve phase two instance
        simplex = self._solve_phase_two(basic_vars, redundant_rows)
        
        # Set the solution
        self.status = simplex.status
        self.objective = simplex.objective
        self.solution = simplex.solution
```

接下来就是上面三个函数的实现。其中 `_solve_phase_one` 和 `_solve_phase_two` 就是调用单纯形算法，实现相对简单。前面我们已经实现了单纯形算法，且能够 [处理退化](degeneracy) 的例子，因此算法能在有限步内收敛。

函数 `_get_basic_feasible_solution` 的实现参照 [两阶段法](.../twophase#入基和出基) 和 [两阶段法示例](../twophase-example)。

### 代码

相关代码在 [`codes/simplex-algorithms`](https://github.com/xianqiu/linear-programming/tree/main/codes/simplex-algorithms) 文件夹。

* [simplex_twophase.py](https://github.com/xianqiu/linear-programming/blob/main/codes/simplex-algorithms/simplex_twophase.py) 两阶段单纯形算法
	* [simplex_degen.py](https://github.com/xianqiu/linear-programming/blob/main/codes/simplex-algorithms/simplex_degen.py) 可以处理退化例子的单纯形算法
	* [simplex_basic.py](https://github.com/xianqiu/linear-programming/blob/main/codes/simplex-algorithms/simplex_basic.py) 单纯形算法的实现
	* [common.py](https://github.com/xianqiu/linear-programming/blob/main/codes/simplex-algorithms/common.py) 解的状态定义
* [test_simplex_twophase.py](https://github.com/xianqiu/linear-programming/blob/main/codes/simplex-algorithms/test_simplex_twophase.py) 测试代码
	* [test-data/twophase.json](https://github.com/xianqiu/linear-programming/blob/main/codes/simplex-algorithms/test-data/twophase.json) 测试用例
	* [test-data/cycle.json](https://github.com/xianqiu/linear-programming/blob/main/codes/simplex-algorithms/test-data/cycle.json) 测试用例
	* [test-data/degen.json](https://github.com/xianqiu/linear-programming/blob/main/codes/simplex-algorithms/test-data/degen.json)  测试用例
