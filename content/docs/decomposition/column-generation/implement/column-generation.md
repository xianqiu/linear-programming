---
weight: 783
title: "列生成"
description: ""
icon: "article"
date: "2025-04-22T11:44:22+08:00"
lastmod: "2025-04-22T11:44:22+08:00"
draft: false
toc: true
---

本文讲一下如何用列生成方法求解下料问题。

### 思路

回顾 [近似解](solve#近似解) 求解步骤，分三个步骤：

1. 求解松弛问题 
2. 向下取整数
3. 满足剩余需求

列生成方法是用来求第一步的解松弛问题。它定义了两个问题。

1. 主问题
2. 子问题

列生成用迭代的方式求解主问题和子问题，直到满足停止条件。

### 接口

定义类 `CutStockApproxCG` 用来求解下料问题。它的接口跟 [精确解](exact) 和 [近似解](approximate) 的接口是一样的。为了让代码看起来简洁一点，可以直接继承 `CutStockApprox` 类。

```python
from typing import override


class CutStockApproxCG(CutStockApprox):

    """ Use column generation method to get the approximate solution 
    of the cutting stock problem.
    """

    def __init__(self, L, s, d):
        super().__init__(L, s, d)

    @override
    def solve(self):
        pass
```

方法 `solve` 用来求解。结果保存在成员变量中，其中 `self.count` 表示需要的总的原材料数量，`self.cuts` 是用到的切割方式，`self.x` 代表切割方式对应的原材料数量。因此 `self.count = sum(self.x)` 。

### 实现

注意 `CutStockApproxCG` 继承了 `CutStockApprox`，它的求解步骤依赖下面三个方法。

* `_solve_relax` 求解它的松弛问题（线性规划问题），得到一个分数解。
* `_round_down` 对分数解向下取整，得到一个整数解，并计算未被满足的需求。
* `_greedy_satisfy` 用贪心的策略满足剩下的需求，从而得到近似解。

而列生成只需要改变 `_solve_relax` 的实现。

```python
class CutStockApproxCG(CutStockApprox):

    # ...
    
    @override
    def _solve_relax(self):
        # Use column generation to solve the relaxed problem.
        pass
```

### 松弛解

为了实现 `_solve_relax`，定义如下三个类。

* `_MasterProblem`：求解主问题，得到松弛问题的一个可行解。
* `_SubProblem`：求解子问题，得到一个可行切割。
* `_CutStockRelaxCG`：列生成算法的实现，调用 `_MasterProblem` 和 `_SubProblem` 求解主问题和子问题。
 
类名前加下划线 `_` 的目的是声明它是一个内部的实现类。强调它不是为了给用户调用。

下面分别介绍这三个模块。

#### 主问题

`_MasterProblem` 求解主问题，接口如下。

```python
class _MasterProblem:

    """
    Master problem:
        min sum(x_j)
        s.t. Ax >= d
             x >= 0
        where 
        A: matrix of feasible cuts
        x: number of cuts used
        d: demand vector
    """
    
    def __init__(self, d):
        """
        d: list of demand sizes
        """
        self.d = d
        self.A = np.eye(len(d))
        self.solution = None
        self.objective = None
        self.p = None  # shadow price

    def solve(self):
        # Solve the master problem.
        pass
```

初始化函数 `__init__` 的输入只需要参数 `d`，因为主问题处世户的时候矩阵 `A` 是一个单位矩阵。

`solve` 方法求解主问题，调用线性规划求解器即可。结果保存在成员变量 `self.solution` 和 `self.objective`，以及 `self.p`。注意 `self.p` 是影子价格，也称为对偶变量值，它是子问题的输入。在单纯形算法求解器中，它会顺便计算这个值。


#### 子问题

`_SubProblem` 求解子问题，接口如下。

```python
class _SubProblem:

    """
    Subproblem:
        min sum(p_j * y_j)
        s.t. sum(s_j * y_j) <= L
             y_j >= 0
             y_j integer
        where
            L: raw size
            s: stock sizes
            p: price vector (shadow price of the master problem)
    """
    
    def __init__(self, L, s, p):
        self.L = L
        self.s = s
        self.p = p
        self.solution = None
        self.objective = None

    def solve(self):
        # Solve the subproblem.
```

方法 `solve`求解子问题，调用整数规划求解器实现。结果保存在成员变量 `self.solution` 和 `self.objective`。其中 `self.solution` 就是生成的列。`1-self.objective` 就是 `self.solution` 对应的缩减成本（Reduced Cost）。

### 列生成

`_CutStockRelaxCG` 求解松弛问题。通过调用 `_MasterProblem` 和 `_SubProblem` 实现整个求解过程。

```python
class _CutStockRelaxCG:
    """ Use column generation method to solve the relaxed problem, 
    i.e. the linear program problem of the form:
        min sum(x_j)
        s.t. Ax >= d
             x >= 0
        where
        A: initialized by identity matrix (A is not input)
        x: number of cuts used
        d: demand vector
    """
    
    def __init__(self, L, s, d):
        """
        L: raw size
        s: list of stock sizes
        d: list of demand sizes
        """
        self.L = L
        self.s = s
        self.d = d
        # solution
        self.x = None  # number of cuts used
        self.cuts = None  # cuts used
        self.count = None  # number of raw stock needed

    def solve(self):
        """
        Solve the relaxed problem.
        """
        master = _MasterProblem(self.d)
        while True:
            # 1. Solve the master problem
            master.solve()
            # 2. Solve the subproblem
            sub = _SubProblem(self.L, self.s, master.p)
            sub.solve()
            if sub.objective <= 1:
                # Stop if the optimal solution is found
                break
            # 3. Add new column
            master.add_column(sub.solution)

        # set solution
        solution = np.array(master.solution)
        self.x = solution[solution > 1e-6]
        self.cuts = master.A[:, solution > 1e-6]
        self.count = sum(self.x)
```

需要注意的是，在上面的实现中，没有考虑求解时间。当问题规模较大时，需要限制求解时间。如果超时，则返回当前的解。详情请参考代码。

### 代码

相关代码在 [`codes/decomposition/cutting-stock`](https://github.com/xianqiu/linear-programming/tree/main/codes/decomposition/cutting-stock) 文件夹。

* [column_generation.py](https://github.com/xianqiu/linear-programming/blob/main/codes/decomposition/cutting-stock/column_generation.py) 列生成算法
	* [approximate.py](https://github.com/xianqiu/linear-programming/blob/main/codes/decomposition/cutting-stock/approximate.py) 近似解算法
  * [exact.py](https://github.com/xianqiu/linear-programming/blob/main/codes/decomposition/cutting-stock/exact.py) 精确解算法
* [test_cutstock.py](https://github.com/xianqiu/linear-programming/blob/main/codes/decomposition/cutting-stock/test_cutstock.py) 测试代码