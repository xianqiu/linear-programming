---
weight: 782
title: "近似解"
description: ""
icon: "article"
date: "2025-04-22T11:43:19+08:00"
lastmod: "2025-04-22T11:43:19+08:00"
draft: fasle
toc: true
---

下料问题求 [近似解](solve#近似解) 的思路是这样的，先求它的线性规划问题得到一个分数解，然后把这个分数解向下取整，从而得到整数解。这样一来，有一些需求可能不被满足。最后，用简单粗暴的办法，去满足剩下的需求，从而得到一个可行解。

### 接口

定义 `CutStockApprox` 用来近似求解下料问题。它的接口跟 [精确算法的接口](exact/#接口) 是一样的。为了让代码看起来简洁一点，可以直接继承 `CutStockExact` 类。

注意，继承的好处是可以少些一点重复代码。但是它增加了代码的耦合度。在大型项目或者多人合作的项目中，应该要慎继承。在很多情况下，允许一些重复代码不见得是个坏事。

```python
from typing import override


class CutStockApprox(CutStockExact):

    def __init__(self, L, s, d):
        """
        L: raw size
        s: list of stock sizes
        d: list of demand sizes
        """
        super().__init__(L, s, d)
        
    @override
    def solve(self)
        # Get the approximate solution.
        pass
```

### 实现

定义如下三个函数

* `_solve_relax` 求解它的松弛问题（线性规划问题），得到一个分数解。
* `_round_down` 对分数解向下取整，得到一个整数解，并计算未被满足的需求。
* `_greedy_satisfy` 用贪心的策略满足剩下的需求，从而得到近似解。

```python

class CutStockApprox(CutStockExact):

    # ...

    def _solve_relax(self):
        # Solve the relaxed problem using CLP solver
        pass

    def _round_down(self):
        # Round down the solution to the nearest integer
        self.x = np.floor(self.x)
        self.count = sum(self.x)
        unsatisfied_demands = self.d - self.cuts @ self.x

        return unsatisfied_demands

    def _greedy_satisfy(self, unsatisfied_demands):
        """
        Greedily satisfy the unsatisfied demands.
        """
        pass
```

接下来就可以实现 `solve` 方法。

```python

class CutStockApprox(CutStockExact):

    # ...

    @override
    def solve(self):
        # 1. Solve the relaxed problem
        self._solve_relax()
        # 2. Round down the solution to the nearest integer
        unsatisfied_demands = self._round_down()
        # 3. Satisfy the unsatisfied demands
        self._greedy_satisfy(unsatisfied_demands)
```

### 代码

相关代码在 [`codes/decomposition/cutting-stock`](https://github.com/xianqiu/linear-programming/tree/main/codes/decomposition/cutting-stock) 文件夹。

* [approximate.py](https://github.com/xianqiu/linear-programming/blob/main/codes/decomposition/cutting-stock/approximate.py) 近似解算法
	* [exact.py](https://github.com/xianqiu/linear-programming/blob/main/codes/decomposition/cutting-stock/exact.py) 精确解算法


