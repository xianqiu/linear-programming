---
weight: 782
title: "行生成"
description: ""
icon: "article"
date: "2025-04-29T11:05:28+08:00"
lastmod: "2025-04-29T11:05:28+08:00"
draft: false
toc: true
katex: true
---

讲一下 [行生成](../benders) 方法的实现。用来求解如下的设施选址问题。

{{<katex>}}
$$
\begin{aligned}
\min ~  & \sum_{i=1}^m f_iy_i + \sum_{i=1}^m\sum_{j=1}^n c_{ij}x_{ij}\\[6pt]
\text{s.t. } & \sum_{i=1}^m x_{ij} = 1, \quad \forall j\\[6pt]
& x_{ij}\leq y_i, \quad \forall i, j\\[6pt]
& x_{i,j}\geq 0,~ y_i \in \set{0,1}, \quad \forall i, j
\end{aligned}
$$
{{</katex>}}

### 接口

定义一个类 `FacilityLocationBenders` 用来求解设施选址问题。它的接口跟 [直接求解](exact#接口) 方法的接口一样。为了让代码看起来简洁一点，`FacilityLocationBenders` 可以直接继承 `FacilityLocationExact` 类。

```python

class FacilityLocationBenders(FacilityLocationExact):
    
    """
    Benders decomposition for the facility location problem.
    """

    def __init__(self, f, C):
        self._start = time.time()
        super().__init__(f, C)
    
    @override
    def solve(self):
        """
        Solve the facility location problem.
        """
        pass
```

`solve` 方法用来求解，结果保存在成员变量 `self.x, self.y, self.solution` 中。

### 实现

定义如下三个类

* `_MasterProblem`：用来求解主问题。 
* `_SubProblem`：用来求解子问题。
* `_BendersProcess`：行生成的算法过程。过程中调用 `_MasterProblem` 求解主问题，以及 `_SubProblem`求解子问题。

类名前加下划线 `_` 的目的是声明它是一个内部的实现类。强调它不是为了给用户调用。

#### 主问题

求解主问题的类 `_MasterProblem` 的定义如下。

```python

class _MasterProblem:

    """
    Master problem for the facility location problem.
    Args:
    f: facility open costs
    C: connection costs
    The master problem is:

    min sum(f[i] * y[i]) + z
    s.t. sum(y[i]) >= 1
         sum(alpha[j]) + sum(y[i]beta[i][j]) <= z, for all alpha, beta
    
    Note: alpha, beta are parameters.
    """

    def __init__(self, f, C):
        self.f = f
        self.C = C
        # Solution
        self.y = None
        self.objective = None
        self.status = None

    def solve(self):
        """
        Solve the master problem.
        """
        pass
    
    def add_constraint(self, alpha, beta):
        """
        Add the following constraint:
            sum(alpha[j]) <= z + sum(beta[i][j] * y[i])
        """
```

`solve` 方法进行求解，调用整数规划求解器实现。`add_constraint` 方法增加约束，其中参数 `alpha, beta` 来自子问题的解。

#### 子问题

求解子问题的类 `_SubProblem` 的定义如下。

```python

class _Subproblem:

    """
    Subproblem for the facility location problem.
    Args:
    C: connection costs
    y: solution of the master problem

    The subproblem is:
    
    max sum(alpha[j]) - sum(beta[i][j] * y[i]) 
        s.t. alpha[j] + beta[i][j] <= C[i][j], for all i, j
             beta[i][j] >= 0, for all i, j
    Note: 
    1. alpha, beta are decision variables.
    2. y is parameter.
    """

    def __init__(self, C, y):
        self.C = np.array(C)
        self.y = np.array(y)
        # Solution
        self.alpha = None
        self.beta = None
        self.objective = None
        
    def solve(self):
        """
        Solve the sub problem.
        """
        pass
    
    @property
    def x(self):
        """
        Return the dual solution.
        """
        pass
```
方法 `solve` 用来求解，调用线性规划求解器实现。注意，子问题解出的是 `alpha, beta` 值，而原问题的解是关于 `x, y`，其中 `y` 来自主问题，而 `x` 来自子问题。方法 `_Subproblem.x` 返回 `x` 值，它是子问题的对偶变量值。

### 行生成

假设 `_BendersProcess` 已经实现。就可以用它求解设施选址问题，然后把结果按照接口的要求输出。

```python
class FacilityLocationBenders(FacilityLocationExact):
    
    """
    Benders decomposition for the facility location problem.
    """

    def __init__(self, f, C):
        super().__init__(f, C)
    
    @override
    def solve(self):
        """
        Solve the facility location problem.
        """
        bp = _BendersProcess(self.f, self.C)
        bp.timeout = self.timeout
        bp.print_info = self.print_info
        bp.solve()
        self.x = bp.x
        self.y = bp.y
        self.objective = bp.objective
        self.status = bp.status

        return self
```

最后，还需要增加一个计时功能。当计算时间超过阈值时算法停止。此时输出当前的解。这也是间接求解方法的好处。在迭代的过程中，可以随时停止。

### 代码

相关代码在 [`codes/decomposition/facility-location`](https://github.com/xianqiu/linear-programming/tree/main/codes/decomposition/facility-location) 文件夹。
* [benders.py](https://github.com/xianqiu/linear-programming/blob/main/codes/decomposition/facility-location/benders.py) 行生成方法
	* [exact.py](https://github.com/xianqiu/linear-programming/blob/main/codes/decomposition/facility-location/exact.py) 直接求解