---
weight: 420
title: "割平面法"
description: ""
icon: "article"
date: "2025-03-22T17:12:29+08:00"
lastmod: "2025-03-22T17:12:29+08:00"
draft: true
toc: true
---

考虑整数规划问题：
$$
\begin{aligned}
\max~ & c^Tx \\
& Ax = b\\
& x\geq 0\\
& x\in \mathbb{Z}^n
\end{aligned}
$$
其中 $c\in \mathbb{R}^n, b\in\mathbb{R}^m, A\in\mathbb{R}^{m\times n}$。

整数规划要求决策变量 $x$ 是整数。它对应的线性规划问题称为 *松弛问题*。

本文介绍求解整数规划问题的割平面法。它的思路是不断构造新的约束条件，使得原问题的整数解仍然可行，然后求解松弛问题，直到求得整数最优解。新增的约束割掉了可行域的“分数区域”，所以也被称为*割平面*。

![](https://i-blog.csdnimg.cn/blog_migrate/dfdcf1eb4e1321b52b21dfa6d395fd43.gif#pic_center)


## Gomory-Chvátal Cut

下面介绍一种构造割平面的方法，来自Gomory和Chvátal，称之为“GC割”。

回顾单纯形算法（参考[《线性规划：单纯形算法》](https://blog.csdn.net/qx3501332/article/details/118460050)），已知基矩阵 $B$，用 $N$ 代表非基矩阵，约束条件可以写成
$$
x_B + B^{-1}Nx_N = B^{-1}b.
$$
令 $J$ 代表非基变量的下标，$\bar{a}_j$ 代表 $B^{-1}N$ 的列向量，其中 $j\in J$。令  $\bar{b}:= B^{-1}b$，上式可以写成
$$
x_B + \sum_{j\in J}\bar{a}_jx_j = \bar{b}.
$$
把上式左边 $x_j$ 的系数向下取整，我们有
$$
x_B + \sum_{j\in J} \lfloor \bar{a}_j \rfloor x_j \leq \bar{b}.
$$
注意到 $x_j\geq 0$ 且 $x_j$ 是整数，那么对不等式右边 $\bar{b}$ 取整之后，不等式依然成立，即
$$
x_B + \sum_{j\in J} \lfloor \bar{a}_j \rfloor x_j \leq \lfloor\bar{b}\rfloor.
$$
结合前面的等式，我们有
$$
\sum_{j\in J}(\bar{a}_j-\lfloor \bar{a}_j\rfloor) x_j \geq \bar{b} - \lfloor\bar{b}\rfloor.
$$
上面的不等式称为为 **GC割**。

## 割平面法

割平面法求解整数规划的步骤如下：

1. 考虑整数规划问题： $\max\{c^Tx\mid Ax=b, x\in \mathbb{Z}^n_+\}$；
2. 求解松弛问题，得到解 $x^*$；
3. 如果 $x^*$ 是整数解，则结束；
4. 构造GC割，添加到松弛问题中，然后执行第2步。

## 算法实现

我们用Python实现上述算法。先定义输入和输出。

```python
import numpy as np


class CutPlane(object):

    def __init__(self, c, A, b, lb=None, ub=None):
        """
        :param c: n * 1 vector
        :param A: m * n matrix
        :param b: m * 1 vector
        :param lb: list, lower bounds of x, e.g. [0, 0, 1, ...]
        :param ub: list, upper bounds of x, e.g. [None, None, ...], None 代表正无穷
        """
        # 输入
        self._c = np.array(c) * 1.0
        self._A = np.array(A) * 1.0
        self._b = np.array(b) * 1.0
        self._lb = lb
        self._ub = ub
        # 输出
        self._sol = None  # solution
        self._obj_val = None  # objective value
        # 辅助变量
        # ...
```

算法的迭代流程如下所示。

```python
class CutPlane(object):
  
    # 其它函数省略
    # ...

    def solve(self):
        self._init_model()  # 初始化松弛问题
        self._solve_lp()  # 求解松弛问题
        while not self._is_feasible():
            self._add_cuts_batch()  # 添加割平面
            self._solve_lp()
```

主要实现三个函数：

* `CutPlane._init_model()` 初始化松弛问题。
* `CutPlane._solve_lp()` 求解松弛问题。
* `CutPlane._add_cuts_batch()` 添加割平面。

下面看一看这三个函数。

`CutPlane._init_model()` 进行初始化时，需要把不等式 $Ax\leq b$ 转化成 $A'x' = b$ 的形式。

```python
from ortools.linear_solver import pywraplp
import numpy as np


class CutPlane(object):
  
  	# 其它函数省略
    # ...

    def _init_model(self):
        """ 根据输入，初始化模型。
        """
        self._model = pywraplp.Solver.CreateSolver('GLOP')
        # 约束：Ax <= b
        m, n = np.shape(self._A)
        self._x1 = [self._model.NumVar(0, self._model.Infinity(),
                                       'x[%d]' % j) for j in range(n)]
        for i in range(m):
            self._add_cut(self._x1, self._A[i, :], self._b[i])
        # 约束：lb <= x <= ub
        self._init_lb_ub()  # 初始化 self._lb, self._ub，用数组表示
        for j in range(n):
            # x <= ub
            if self._ub[j] is not None:
                self._add_cut([self._x1[j]], [1], self._ub[j])
            # -x <= -lb
            if self._lb[j] is not None:
                self._add_cut([self._x1[j]], [-1], -self._lb[j])
        # 目标
        self._obj = self._model.Objective()
        self._c1 = self._c
        for j in range(n):
            self._obj.SetCoefficient(self._x1[j], self._c1[j])
        self._obj.SetMaximization()
        
    def _add_cut(self, variables, coefficients, ub):
        """ 增加一个割平面
        """
        # 把不等式约束写成等式约束
        # ax <= ub --> ax + y = ub
        ct = self._model.Constraint(ub, ub)
        for x, c in zip(variables, coefficients):
            ct.SetCoefficient(x, c)
        # add slack variable
        slack_var = self._model.NumVar(0, self._model.Infinity(),
                                       'x[%d]' % len(self._x1))
        ct.SetCoefficient(slack_var, 1)
        self._x1.append(slack_var)  # 决策变量
        self._const1.append(ct)  # 约束的集合
```

`CutPlane._solve_lp()` 求解松弛问题，并计算相关的辅助变量，用来生成GC割。

```python
import numpy as np


class CutPlane(object):
  
  	# 其它函数省略
    # ...    
    
    def _solve_lp(self):
        """ 求解松弛问题。
        """
        self._model.Solve()
        # 把问题转换成标准化形式
        self._refactor_cab()
        # 然后计算辅助变量
        # 为下一步计算割平面做准备
        m, n = np.shape(self._A1)
        self._sol1 = [self._x1[j].solution_value() for j in range(n)]
        self._sol = self._sol1[0: len(self._c)]  # 原问题的解
        self._obj_val = self._obj.Value()  # 目标函数值
        self._basic_vars = [j for j in range(n)
                            if self._x1[j].basis_status() == self._model.BASIC]
        self._non_basic_vars = list(set(range(n)) - set(self._basic_vars))
        self._basic_consts = np.array([j for j in range(m)
                                       if self._const1[j].basis_status() == self._model.FIXED_VALUE])
        self._basic_matrix = np.array([[self._A1[i][j]
                                       for j in self._basic_vars]
                                       for i in self._basic_consts])
        self._non_basic_matrix = np.array([[self._A1[i][j]
                                           for j in self._non_basic_vars]
                                           for i in self._basic_consts])
        
    def _refactor_cab(self):
        """ 把问题用标准形表示。
            min c1 * x1
            s.t. A1 * x1 = b1
        """
        m, n = len(self._const1), len(self._x1)
        self._c1 = np.array(self._c.tolist() + [0] * (n - len(self._c1)))
        self._A1 = np.zeros((m, n))
        self._b1 = np.zeros(m)
        for i in range(m):
            for j in range(n):
                self._A1[i][j] = self._const1[i].GetCoefficient(self._x1[j])
            self._b1[i] = self._const1[i].Ub()
```

`CutPlane._add_cuts_batch()` 添加割平面。生成所有割平面，然后批量添加。

```python
import numpy as np


class CutPlane(object):
  
  	# 其它函数省略
    # ...        
  
    def _add_cuts_batch(self):
        """ 计算并添加割平面。
        """
        B_inv = np.linalg.inv(self._basic_matrix)
        N_bar = B_inv @ self._non_basic_matrix
        b1 = [self._b1[i] for i in self._basic_consts]
        b_bar = B_inv @ b1
        # generate cuts
        variables = [self._x1[j] for j in self._non_basic_vars]
        coefficients_batch = np.array([-N_bar[:, j] + np.floor(N_bar[:, j])
                                       for j in range(len(self._non_basic_vars))]).T
        ub_batch = -b_bar + np.floor(b_bar)
        # add all cuts
        for coefficients, ub in zip(coefficients_batch, ub_batch):
            self._add_cut(variables, coefficients, ub)
```

[完整代码](https://github.com/xianqiu/opt-alg-tutorials/blob/master/math-prog/int-prog/cutplane.py)

## 参考文献

[1] Dimitris Bertsimas and Andreas Schulz. *[Integer Programming and Combinatorial Optimization: Cutting Plane Methods I](https://download.csdn.net/download/qx3501332/23011156)*, Lecture notes, MIT, 2009.