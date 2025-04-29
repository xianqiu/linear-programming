---
weight: 781
title: "直接求解"
description: ""
icon: "article"
date: "2025-04-29T11:05:17+08:00"
lastmod: "2025-04-29T11:05:17+08:00"
draft: false
toc: true
katex: true
---

直接求解就是解下面的混合整数规划。

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

定义类 `FacilityLocationExact` 用来求解上面的混合整数规划问题。`solve` 方法用来求解，结果保存在成员变量中。

```python

class FacilityLocationExact:

    """
    Exact solution of the facility location problem.
    Args:
    f: facility open costs
    C: connection costs

    The problem is:
    min sum(f[i] * y[i]) + sum(C[i][j] * x[i][j])
    s.t. sum(x[i][j]) = 1, for all j
         sum(x[i][j]) <= y[i], for all i
         x[i][j] >= 0, for all i, j
         y[i] in {0, 1}, for all i, j
    """
    
    def __init__(self, f, C):
        self.f = np.array(f)
        self.C = np.array(C)
        # Solution
        self.x = None
        self.y = None
        self.objective = None
        
    def solve(self):
        """
        Solve the facility location problem.
        """
```

### 实现

在 `solve` 函数中调用 [OR-Tools](https://developers.google.com/optimization) 的整数规划求解器（例如 `CBC`），结果保存在成员变量 `self.x, self.y, self.objective` 中。
细节可以参考代码。

### 代码

相关代码在 [`codes/decomposition/facility-location`](https://github.com/xianqiu/linear-programming/tree/main/codes/decomposition/facility-location) 文件夹。
* [exact.py](https://github.com/xianqiu/linear-programming/blob/main/codes/decomposition/facility-location/exact.py) 求解设施选址问题的整数规划

