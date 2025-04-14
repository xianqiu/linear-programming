---
weight: 481
title: "内点法"
description: ""
icon: "article"
date: "2025-04-14T10:43:11+08:00"
lastmod: "2025-04-14T10:43:11+08:00"
draft: false
toc: true
---

本文讲一下 [内点法](../algorithm) 的实现。前面讲到的内点法也称为 **原始对偶内点法（Primal Dual Interior Point Method）**，它同时考虑原问题和对偶问题的可行解，好处是可以加快收敛。

实现之前先明确几点假设。第一，问题是最小化问题。第二，系数矩阵 `A` 是满秩矩阵。第三，存在最优解。也就是说，问题可行且最优目标函数值有界。

### 接口

定义一个类 `PDInteriorPoint` ，它的输入是 `A, b, c` 。方法 `solve` 用来求解线性规划问题，结果和状态保存在成员变量中。

```python
import numpy as np


class PDInteriorPoint:

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

讲一下实现的思路。首先是初始化。

```python
import numpy as np


class PDInteriorPoint:

    def __init__(self, A, b, c):
        """
        Args:
        A: matrix of coefficients of the constraints
        b: vector of right-hand side values
        c: vector of coefficients of the objective function
        """
        self.A = np.array(A)
        self.b = np.array(b)
        self.c = np.array(c)
        self.n = len(c)
        self.m = len(b)
        self.objective = None
        self.solution = None
        self.status = None
        # Initialize the primal and dual variables
        self._x = np.ones(self.n)
        self._y = np.ones(self.m)
        self._s = np.ones(self.n)
        # Initialize the centering parameter
        self._mu = self._x @ self._s / self.n
        # Scaling parameter of mu
        self._alpha = 0.1
```

定义如下几个方法：

* `_is_optimal`：判断是否达到最优条件。
* `_newton_direction:` 计算牛顿方向。
* `_update`: 根据牛顿方向更新变量。

```python
class PDInteriorPoint:
    
    # ...

    def _is_optimal(self):
    		""" Check if the primal and dual variables are optimal.
    		"""
        return False

    def _newton_direction(self):
    	  """
    	  Compute the Newton direction.
        """
        return dx, dy, ds

    def _update(self, dx, dy, ds):
        """
        Update solution w.r.t. Newton direction.
        """
        pass
```

利用这几个函数实现 `solve`。

```python
class PDInteriorPoint:

    # ...

    def solve(self):  
    
        while not self._is_optimal():
            # Update the centering parameter
            self._mu = self._mu * self._alpha
            # Compute the Newton direction
            dx, dy, ds = self._newton_direction()
            # Update the primal and dual variables
            self._update(dx, dy, ds)
        
        # Set solution
        self.objective = self.c @ self._x
        self.solution = self._x
        self.status = "OPTIMAL"
```

### 代码

相关代码在 [`codes/interior-point-method`](https://github.com/xianqiu/linear-programming/tree/main/codes/interior-point-method) 文件夹。

* [primal_dual.py](https://github.com/xianqiu/linear-programming/blob/main/codes/interior-point-method/primal_dual.py) 原始对偶内点法实现
* [test_primal_dual.py](https://github.com/xianqiu/linear-programming/blob/main/codes/interior-point-method/test_primal_dual.py) 测试代码
  * [interior.json](https://github.com/xianqiu/linear-programming/blob/main/codes/interior-point-method/interior.json)  测试用例