---
weight: 581
title: "分支定界"
description: ""
icon: "article"
date: "2025-04-16T11:49:51+08:00"
lastmod: "2025-04-16T11:49:51+08:00"
draft: false
toc: true
katex: true
---

讲一下分支定界法的实现思路。考虑这样的整数规划问题。

{{<katex>}}
$$
\begin{aligned}
\max~ & c^Tx \\
& Ax \leq b\\
& x\geq 0\\
& x\in \mathbb{Z}^n
\end{aligned}
$$
{{</katex>}}

其中 $c\in \mathbb{R}^n, b\in\mathbb{R}^m, A\in\mathbb{R}^{m\times n}$。

### 接口

定义三个类 

* `Node`：代表搜索树的一个节点。一个节点就是一个线性规划实例。
* `LPSolver`：线性规划问题求解器。
* `BranchAndBound`：分支定界法的实现类。

`Node` 定义如下。

```python
class Node(object):

    """ Linear Program (LP) instance.
        The instance is defined as:
            max c^T x
            s.t. Ax <= b
                 x >= 0
        where:
            c: n-dim vector
            A: m x n matrix
            b: m-dim vecto
    """

    def __init__(self, A, b, c):
        self.A = A
        self.b = b
        self.c = c
        self.solution = None
        self.objective = None
```

`LPSolver` 用来求解 `Node` 对象，并把结果保存在对象中。

```python
class LPSolver:

    """ Solve the given linear program.
    """

    def __init__(self, node):
        """
        Args:
            node: Node object, The LP instance.
        """
        self.node = node
        self.status = None

    def solve(self):
        """ Solve the instance and save the result to 
        node.objective and node.solution.
        """
        # self.node.solution = ...
        # self.node.objective = ...
        pass
```

`BranchAndBound` 定义如下。方法 `solve` 用来求解，结果保存在成员变量中。

```python
class BranchAndBound:
    
    """ Branch and bound algorithm for maximization problem.
    """
    
    def __init__(self, A, b, c):
        """
        Args:
            c: n-dim vector
            A: m x n matrix
            b: m-dim vector
        """
        # Instance
        self.A = A
        self.b = b
        self.c = c
        # Solution
        self.solution = None
        self.objective = None
        self.status = None

    def solve(self):
        """ Solve the problem.
        """
        pass
```

### 实现

实现 `LPSolver.solve` 只要调求解器就可以了。这里用 [OR-Tools](https://developers.google.com/optimization) 来求解。使用方法请参考官方教程，这里不重复讲。

接下来讲 `BranchAndBound`。

首先是初始化。定义根节点 `self.root`，这是搜索的起点。用 `self._best_solution` 和 `self._best_objective` 保存搜索结果，记录“最好的”可行解。

```python
class BranchAndBound:
    
    """ Branch and bound algorithm.
    """
    
    def __init__(self, A, b, c):
        """
        Args:
            c: n-dim vector
            A: m x n matrix
            b: m-dim vector
        """
        self.A = A
        self.b = b
        self.c = c
        self.root = Node(A, b, c)
        # Best search result
        self._best_solution = None
        self._best_objective = -np.inf
        # Final Solution
        self.solution = None
        self.objective = None
        self.status = None
```

接下来就是搜索过程。定义如下方法。

* `_branch(node)`：给定当前节点 `node`，生成它的两个子节点。
* `_search(node)`：递归的方式进行搜索，即深度优先搜索。其中用到 `_branch` 进行分支操作。

```python
class BranchAndBound:
    
    """ Branch and bound algorithm.
    """

    def _branch(self, node):
        """ Branch the node.
        """
        # node1 = Node(A1, b1, node.c)
        # node2 = Node(A2, b2, node.c)
        # return node1, node2
        pass


    def _search(self, node):
        """ Depth first search.
        """
        pass
```

最后是 `solve` 方法。调用 `_search`，再把结果写入成员变量。

```python

class BranchAndBound:

    # ...

    def solve(self):
        """ Solve the problem.
        """
        self._search(self.root)
        if self._best_solution is not None:
            self.solution = self._best_solution
            self.objective = self._best_objective
            self.status = 'OPTIMAL'
```

### 代码

相关代码在 [`codes/integer-programming`](https://github.com/xianqiu/linear-programming/tree/main/codes/integer-programming) 文件夹。

* [branchbound.py](https://github.com/xianqiu/linear-programming/blob/main/codes/integer-programming/branchbound.py) 分支定界法实现

* [test_branchbound.py](https://github.com/xianqiu/linear-programming/blob/main/codes/integer-programming/test_branchbound.py) 测试代码
  * [integer.json](https://github.com/xianqiu/linear-programming/blob/main/codes/integer-programming/integer.json)   测试用例