---
weight: 10
title: "基础算法"
description: ""
icon: "article"
date: "2025-03-27T13:55:12+08:00"
lastmod: "2025-03-27T13:55:12+08:00"
draft: false
toc: true
---

本文用 Python 实现一个基本的[单纯形算法](../simplex)。主要是讲实现的思路，代码地址在文末。


### 接口

首先是定义接口，就是明确输入和输出。

定义一个类 `SimplexBasic`，它的初始化函数 `__init__`  的参数就是单纯形算法的输入。

```python

class SimplexBasic:
    
    def __init__(self, A, b, c, s):
        """
        A: matrix of coefficients of the constraints
        b: vector of right-hand side values
        c: vector of coefficients of the objective function
        s: vector of indices of the initial basic feasible variables
        """
        pass
```

接下来定义函数  `solve` 计算最优解。

```python

class SimplexBasic:

    # ...
        
    def solve(self):
        # solve the problem
        pass
```

由于计算结果不只是解向量，还有目标函数值，基本矩阵等多种信息。为了简单起见，`solve` 只做求解，它不直接返回结果。

为了得到最优解，可以定义两个函数  `solution` 返回和 `objective`，如下所示。

```python

class SimplexBasic:

    # ...
    
    @property
    def solution(self):
        # returns the solution vector
        pass

    @property
    def objective(self):
        # returns the objective function value
        pass
```

总结一下，接口就是这样。

```python

class SimplexBasic:
    
    def __init__(self, A, b, c, s):
        """
        A: matrix of coefficients of the constraints
        b: vector of right-hand side values
        c: vector of coefficients of the objective function
        s: vector of indices of the initial basic feasible variables
        """
        pass
        
    def solve(self):
        # solve the problem
        pass
        
    @property
    def solution(self):
        # returns the solution vector
        pass

    @property
    def objective(self):
        # returns the objective function value
        pass
```

假设函数的功能已经实现。我们就可以这样调用。

```python

# example
A = [[3, 1, 1, 0, 0], 
    [1, 2, 0, 1, 0], 
    [1, 0, 0, 0, 1]]
b = [120, 160, 35]
c = [-7, -6, 0, 0, 0]
s = [2, 3, 4]


if __name__ == '__main__':

    simplex = SimplexBasic(A, b, c, s)
    simplex.solve()
    print(f"objective value: {simplex.objective}")
    print(f"solution vector: {simplex.solution}")
```

接下来就是去实现上面的函数。

### 实现

首先是初始化 `__init__` 函数。用成员变量保存输入参数。`_basic_vars` 是基矩阵对应的列标；`_nonbasic_vars` 是非基矩阵对应的列标。

```python
class SimplexBasic:

    def __init__(self, A, b, c, s):
        """
        A: matrix of coefficients of the constraints
        b: vector of right-hand side values
        c: vector of coefficients of the objective function
        s: vector of indices of the initial basic feasible variables
        """
        self.A = np.array(A)
        self.b = np.array(b)
        self.c = np.array(c)
        self.s = s
        self.m = len(A)
        self.n = len(A[0])
        self._basic_vars = s
        self._nonbasic_vars = [i for i in range(self.n) if i not in s]
```

根据 `_basic_vars` 可以计算出基矩阵 `_B`。

```python
class SimplexBasic:

    # ...

    @property
    def _B(self):
        # Basic matrix
        return self.A[:, self._basic_vars]
```

于是得到基本解 `_x`。

```python
class SimplexBasic:

    # ...

    @property
    def _x(self):
        # Solution vector
        x = np.zeros(self.n)
        x[self._basic_vars] = np.linalg.inv(self._B) @ self.b
        return x
        
    @property
    def solution(self):
        return self._x
```
这样一来，`solution` 函数就实现了。

类似地，下面的方法实现了 `objective` 函数。

```python
class SimplexBasic:

    # ...
    
    @property
    def _xB(self):
        # Basic solution vector
        return self._x[self._basic_vars]

    @property
    def _cB(self):
        # Basic cost vector
        return self.c[self._basic_vars]

    @property
    def objective(self):
        return self._cB @ self._xB
```

接下来考虑 `solve` 函数。迭代的思路如下。

```python

class SimplexBasic:

    # ...

    def solve(self):
        while not self._is_optimal():
            # iteration
            # 1. find j, the entering column
            entering_var = self._find_entering_var()
            # 2. givin j, find i, the leaving column 
            #    if unbounded, let i = None
            leaving_var = self._find_leaving_var(entering_var)
            if leaving_var is None:
                # unbounded
                return
            # 3. update: exchange i and j
            self._update(leaving_var, entering_var)
```

其中

* `_is_optimal` 判断是否最优；
* `_find_entering_var` 计算入基变量的下标；
* `_find_leaving_var` 计算出基变量的下标；
* `_update` 执行入基和出基操作。

这四个函数如何实现，这里不展开。具体可以参考[单纯形算法](../simplex)中的细节。

### 代码

相关代码在 [`codes/simplex-algorithms`](https://github.com/xianqiu/linear-programming/tree/main/codes/simplex-algorithms) 文件夹。

* [common.py](https://github.com/xianqiu/linear-programming/blob/main/codes/simplex-algorithms/common.py) 定义解的状态，例如 `OPTIMAL`, `UNBOUNDED`
* [simplex_basic.py](https://github.com/xianqiu/linear-programming/blob/main/codes/simplex-algorithms/simplex_basic.py) 算法的实现
* [test-data/basic.json](https://github.com/xianqiu/linear-programming/blob/main/codes/simplex-algorithms/test-data/basic.json)  测试用例
* [test_simplex_basic.py](https://github.com/xianqiu/linear-programming/blob/main/codes/simplex-algorithms/test_simplex_basic.py) 测试代码
