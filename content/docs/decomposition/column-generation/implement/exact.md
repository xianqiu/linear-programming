---
weight: 781
title: "精确解"
description: ""
icon: "article"
date: "2025-04-22T11:43:09+08:00"
lastmod: "2025-04-22T11:43:09+08:00"
draft: false
toc: true
katex: true
---

求下料问题的精确解，可以直接调用求解器，解下面的整数规划。

{{<katex>}}
$$
\begin{aligned}
\min ~ & e^Tx \\
\text{ s.t. } &  A x = d \\
& x \in \mathbb{N}^n_+
\end{aligned}
$$
{{</katex>}}

其中 $e=[1, 1, ..., 1]^T$，$d=[d_1, d_2, ..., d_m]^T$。

### 接口

定义类 `CutStockExact` 用来解上述整数规划。方法 `solve` 用来求解，结果保存在成员变量中。

其中 `self.count` 表示需要的总的原材料数量，`self.cuts` 是用到的切割方式，`self.x` 代表切割方式对应的原材料数量。因此 `self.count = sum(self.x)` 。


```python
class CutStockExact:

    """
    Exact solution of the cutting stock problem.
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
        # Solution
        self.count = None  # Number of raw stock needed
        self.x = None  # Number of raw stock for each used cut 
        self.cuts = None  # Cuts used
    
    def solve(self):
        """
        Solve the cutting stock problem.
        """
        pass
```

### 实现

首先是计系数矩阵 $A$，它代表所有的可行切割。

定义函数 `enumerate_vectors(ub)`，用它来枚举 `[0, ub]` 之间的所有整数向量，其中 `ub` 是一个列表，代表一个正整数向量。

```python
def enumerate_vectors(ub):
    """
    Enumerate vectors in [0, ub].
    lb: lower bound vector
    ub: upper bound vector
    E.g. ub = [2, 2] 
        => [[0,0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 1], [2, 2]]
    """
    pass
```

实现了这个函数，就可以用它来枚举所有的可行切割。

```python
class CutStockExact:

    # ...

    def _feasible_cuts(self):
        """
        Enumerate all feasible cuts (patterns).
        """
        cuts = []
        ub = [int(self.L / s) for s in self.s]
        # enumerate all vectors in [0, ub]
        # if sum of vector is less than or equal to L, add to cuts
        # except for the zero vector
        for cut in enumerate_vectors(ub)[1: ]:
            if  np.array(cut) @ np.array(self.s) <= self.L:
                cuts.append(cut)

        return cuts

```

从而得到系数矩阵。

```python
class CutStockExact:

    # ...
    
    def __init__(self, L, s, d):
        """
        L: raw size
        s: list of stock sizes
        d: list of demand sizes
        """
        # ...
        # Enumeragte feasible cuts and get matrix A
        self._A = np.array(self._feasible_cuts()).T
```

然后就是调用整数规划求解器进行求解。详情可以参考代码。

### 代码

相关代码在 [`codes/decomposition/cutting-stock`](https://github.com/xianqiu/linear-programming/tree/main/codes/decomposition/cutting-stock) 文件夹。

* [exact.py](https://github.com/xianqiu/linear-programming/blob/main/codes/decomposition/cutting-stock/exact.py) 用整数规划求解下料问题

