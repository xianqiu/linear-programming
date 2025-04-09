---
weight: 40
title: "求解器"
description: ""
icon: "article"
date: "2025-04-09T13:44:35+08:00"
lastmod: "2025-04-09T13:44:35+08:00"
draft: true
toc: true
katex: true
---

回顾单纯形算法的标准形式。

{{<katex>}}
$$
\begin{aligned}
\min~ & c^T x\\
\text{s.t.}~ & Ax=b\\
& x\geq 0
\end{aligned}
$$
{{</katex>}}

其中 $c, x \in \mathbb{R}^n$，$A\in\mathbb{R}^{m\times n}$，$b\in\mathbb{R}^m \geq \mathbf{0}$，$n\geq m$。

给定一个线性规划问题，可以把它转化成标准形式，然后用单纯形算法求解。为了使用方便，可以让程序自动转换。

本文实现一个基于单纯形算法的求解器。主要目的是把之前已经实现的算法能力进行封装，从而方便的求解线性规划问题。

### 功能

这个求解器以解决非标准形式的线性规划。

具体来说，有如下功能点。

1. 不要求 $m \leq  n$
2. 不要求 $b\geq \mathbf{0}$
3. 支持求解最大化问题
4. 系数矩阵可以不满秩
5. 可以处理退化的实例

前三个功能点就是把问题转换成标准形式。最后两个功能点，两阶段单纯形算法可以解决。

### 接口

定义类 `SimplexSolver`，它的输入是 `A, b, c`。方法 `solve` 用来求解线性规划问题，结果和状态保存在成员变量中。

```python
import numpy as np


class SimplexSolver:

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
        
    def maximize(self):
        """
        Solve the linear program as a maximization problem.
        """
        return self

    def solve(self):
        """
        Solve the linear program. 
        """
        # simplex = SimplexTwoPhase(self.A, self.b, self.c)
        # simplex.solve()
        # set solution
        pass
```

其中 `maximize` 方法用来标记最大化问题。那么求解时，应该把 `c` 变成 `-c`，以及目标函数值乘以 `-1`。

如果接口已经实现，我们就可以这样调用。


```python

if __name__ == '__main__':

    A = [[3, 1, 1, 0, 0], 
         [-1, -2, 0, -1, 0], 
         [1, 0, 0, 0, 1]]
    b = [120, -160, 35]
    c = [7, 6, 0, 0, 0]
    # maximization problem
    simplex = SimplexSolver(A, b, c).maximize()
    simplex.solve()
    print(simplex.solution)
    print(simplex.objective)
    print(simplex.status)
```

### 实现

调用 `solve` 求解之前，应该先把例子转化成标准形式。定义方法 `_format` 实现这个功能，结果保存在成员变量中。让它在初始化 `__init__` 的时候执行。

```python

class SimplexSolver:

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
        self._format()
    
    def _format(self):
        """
        Format the instance to be used in the simplex algorithm.
        """
        # 1. b[i] < 0
        # 2. m > n
        pass

    def solve(self):
        """
        Solve the linear program
        """
        # Solve the instance, e.g. using two-phase method
        # simplex = SimplexTwoPhase(self.A, self.b, self.c)
        # simplex.solve()
        # Set solution and status
        pass
```

### 代码

相关代码在 [`codes/simplex-algorithms`](https://github.com/xianqiu/linear-programming/tree/main/codes/simplex-algorithms) 文件夹。

* [simplex_solver.py](https://github.com/xianqiu/linear-programming/blob/main/codes/simplex-algorithms/simplex_solver.py) 单纯形算法求解器
	* [simplex_twophase.py](https://github.com/xianqiu/linear-programming/blob/main/codes/simplex-algorithms/simplex_twophase.py) 两阶段单纯形算法
  * [simplex_degen.py](https://github.com/xianqiu/linear-programming/blob/main/codes/simplex-algorithms/simplex_degen.py) 可以处理退化例子的单纯形算法
  * [simplex_basic.py](https://github.com/xianqiu/linear-programming/blob/main/codes/simplex-algorithms/simplex_basic.py) 单纯形算法的实现
  * [common.py](https://github.com/xianqiu/linear-programming/blob/main/codes/simplex-algorithms/common.py) 解的状态定义
* [test_simplex_solver.py](https://github.com/xianqiu/linear-programming/blob/main/codes/simplex-algorithms/test_simplex_twophase.py) 测试代码
  * [test-data/solver.json](https://github.com/xianqiu/linear-programming/blob/main/codes/simplex-algorithms/test-data/solver.json) 测试用例
  * [test-data/twophase.json](https://github.com/xianqiu/linear-programming/blob/main/codes/simplex-algorithms/test-data/twophase.json) 测试用例
  * [test-data/cycle.json](https://github.com/xianqiu/linear-programming/blob/main/codes/simplex-algorithms/test-data/cycle.json) 测试用例
  * [test-data/degen.json](https://github.com/xianqiu/linear-programming/blob/main/codes/simplex-algorithms/test-data/degen.json)  测试用例

