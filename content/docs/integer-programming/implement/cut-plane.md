---
weight: 582
title: "割平面法"
description: ""
icon: "article"
date: "2025-04-16T11:50:41+08:00"
lastmod: "2025-04-16T11:50:41+08:00"
draft: false
toc: true
katex: true
---

讲一下 [割平面法](../cutting-plane) 的实现思路。考虑下面的整数规划问题。

{{<katex>}}
$$
\begin{aligned}
\max~ & c^Tx \\
& Ax \leq b\\
& x\geq \mathbf{0}, ~ x\in \mathbb{Z}^n
\end{aligned}
$$
{{</katex>}}

注意约束条件是不等式。求解的时候，可以引入松弛变量，把不等式改写成等式。

### 接口

定义两个类

* `CutPlane` 实现割平面算法
* `LPSolver` 求解线性规划问题

先看 `CutPlane`， 初始化函数 `__init__` 的输入参数是上面整数规划问题中的参数 `A, b, c`。方法 `solve` 用来求解，结果保存在成员变量中。

```python
import numpy as np


class CutPlane:

    """ Cutting Plane Method.
    """
    
    def __init__(self, A, b, c):
        self.A = np.array(A)
        self.b = np.array(b)
        self.c = np.array(c)
        self.solution = None
        self.objective = None
        self.status = None
        
    def solve(self):
        """ Solve the problem.
        """
        pass
```

`LPSolver` 除了求最优解，还需要返回基矩阵和非基矩阵。具体来说，定义下面这几个方法。

```python

class LPSolver:

    """ Use ortools to solve a linear program instance.
        The instance is defined as:
            max c^T x
            s.t. Ax = b
                 x >= 0
        where:
            c: n-dim vector
            A: m x n matrix
            b: m-dim vecto
    """

    def __init__(self, A, b, c):
        self.A = np.array(A)
        self.b = np.array(b)
        self.c = np.array(c)
        self.m = len(b)
        self.n = len(c)
        self.solution = None
        self.objective = None
        self.status = None

    def solve(self):
        """ Solve the instance.
        """
        pass

    @property
    def basic_vars(self):
        """ Return the basic variables.
        """
        pass

    @property
    def nonbasic_vars(self):
        """ Return the nonbasic variables.
        """
        pass

    @property
    def B(self):
        """
        Return the basis matrix.
        """
        return self.A[:, self.basic_vars]
    
    @property
    def N(self):
        """
        Return the nonbasis matrix.
        """
        return self.A[:, self.nonbasic_vars]
```

### 实现

`LPSolver` 可以调用 [OR-Tools](https://developers.google.com/optimization) 来实现。使用方法请参考官方教程，这里不重复讲。

接下来讲 `CutPlane` 的实现。方法 `_solve_lp`用来解松弛问题，调用 `LPSolver.solve` 就可以了。注意约束是不等式，方法 `_add_slack_variables` 的作用是引入松弛变量，把约束改写成等式。初始化的时候调用该方法。

```python
class CutPlane:

    def __init__(self, A, b, c):
        self.A = np.array(A)
        self.b = np.array(b)
        self.c = np.array(c)
        self.solution = None
        self.objective = None
        self.status = None
        # Number of original variables
        self.n0 = len(c)
        # Reformat A and c
        self._add_slack_variables()
    
    def _add_slack_variables(self):
        """ Add slack variables to the LP instance.
        """
        # Introduce m slack variables
        m = self.A.shape[0]
        # Reformat A
        self.A = np.hstack((self.A, np.eye(m)))
        # Reformat c
        self.c = np.hstack((self.c, np.zeros(m)))

    def _solve_lp(self):
        """ Solve the LP instance.
        """
        lp = LPSolver(self.A, self.b, self.c)
        lp.solve()
        return lp
```

接下来就是生成割平面，定义如下两个方法。

* `_generate_cuts`：生成割平面。
* `_add_cuts`：把割平面添加到原问题中。

```python
class CutPlane:

    # ...

    def _generate_cuts(self, lp):
        """ Generate cuts from the LP instance.

        The cuts are defined as a tuple (F, f) such that
            F x <= f,
        where F is a matrix and f is a vector.
            
        Args:
            lp: LPSolver instance.
        Returns: cuts, a list of tuples (F, f).
        """
        # self._remove_redundant_constraints(lp)
        # F
        ...
        # f
        ...
        #return F, f

    def _add_cuts(self, cuts):
        """ Add cuts to the LP instance.
        Args:
            cuts: a list of tuples (F, f).
        """
```

注意，在生成割平面 `_generate_cuts` 方法中， 如果系数矩阵可能不满秩，需要去掉冗余的行。我们定义方法 `_remove_redundant_constraints` 做这件事。

```python
class CutPlane:
    
    # ...
    
    def _remove_redundant_constraints(self, lp):
        """ Remove redundant constraints from the LP instance.
        """
```

接下来实现 `solve` 方法，也就是算法迭代的流程。

```python
class CutPlane:
    
    # ...
    
    def solve(self):
        """ Solve the problem.
        """
        # Solve the LP instance
        lp = self._solve_lp()
        
        while lp.status == "OPTIMAL" and not self._is_feasible(lp.solution):
            # Generate cuts
            cuts = self._generate_cuts(lp)
            # Add cuts
            self._add_cuts(cuts)
            # Solve the LP instance
            lp = self._solve_lp()

        self.status = lp.status
        
        if self.status == "OPTIMAL":
            self.solution = lp.solution[:self.n0]
            self.objective = lp.objective
```

### 代码

相关代码在 [`codes/integer-programming`](https://github.com/xianqiu/linear-programming/tree/main/codes/integer-programming) 文件夹。

* [cutplane.py](https://github.com/xianqiu/linear-programming/blob/main/codes/integer-programming/cutplane.py) 割平面法实现

* [test_cutplane.py](https://github.com/xianqiu/linear-programming/blob/main/codes/integer-programming/test_cutplane.py) 测试代码
  * [integer.json](https://github.com/xianqiu/linear-programming/blob/main/codes/integer-programming/integer.json)   测试用例