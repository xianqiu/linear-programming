---
weight: 20
title: "处理退化"
description: ""
icon: "article"
date: "2025-03-27T13:55:23+08:00"
lastmod: "2025-03-27T13:55:23+08:00"
draft: false
toc: true
---

为了避免单纯形算法出现循环。在适当的条件下，采用[字典序最小测试比](../degeneracy)的方法选择出基列，可以保证单纯形算法在有限步内收敛。本文讲一下实现的思路。

### 接口

定义一个新的类 `SimplexDegen`，它可以求解退化实例。当然，也可以求解普通实例。它跟以前的算法 `SimplexBasic` 相比，只改变选择出基列的策略，而算法的其他部分没有改变。

因此， `SimplexDegen` 只需要继承 `SimplexBasic`，并且重写选择出基策略的部份（如下所示）。

```python
from typing import override


class SimplexDegen(SimplexBasic):

    @override
    def _find_leaving_var(self, j):
        pass
```

### 实现

讲一下实现的思路。

简单回顾一下字典序最小测试比。首先计算 $I_0$，这一步就是原先的最小测试比。如果 $I_0$ 只包含一个元素，那么它就是出基列，这跟以前一样。如果 $I_0$ 包含多个元素，那么按照前面描述的方法计算 $I_1, I_2, ...$，直到 $I_k$，停止的条件是它只包含一个元素。

因此，我们定义两个函数，一个是 `_I0` ；另一个是 `_I_next` 用递归的方式计算 $I_k$。

```python
class SimplexDegen(SimplexBasic):

    def _I0(self, j):
        """
        Minimum Ratio Test.
        I0 = {i | tilde_b / tilde_a_ij is minimized, and tilde_a_ij > 0}
        Args:
        j: entering variable
        """
        pass

    def _I_next(self, j, I, k):
        """
        Given I_k, find I_{k+1}, I_{k+2}, ... until it contains only one element.
        I_{k+1} = {i | a_ik / a_ij is minimized and i in I_k}
        Args:
        j: entering variable
        I: I_k
        k: k-th column of A
        """
        pass

```



有了这两个函数，就很容易实现 `_find_leaving_var`。

```python
from typing import override

import numpy as np

from simplex_basic import SimplexBasic


class SimplexDegen(SimplexBasic):

    @override
    def _find_leaving_var(self, j):
        I0 = self._I0(j)
        if len(I0) == 0:
            return None  # Unbounded
        I_final = self._I_next(j, I0, 0)
        i_index = int(I_final[0])
        return self._basic_vars[i_index]

    def _I0(self, j):
        """
        Minimum Ratio Test.
        I0 = {i | tilde_b / tilde_a_ij is minimized, and tilde_a_ij > 0}
        Args:
        j: entering variable
        """
        pass

    def _I_next(self, j, I, k):
        """
        Given I_k, find I_{k+1}, I_{k+2}, ... until it contains only one element.
        I_{k+1} = {i | a_ik / a_ij is minimized and i in I_k}
        Args:
        j: entering variable
        I: I_k
        k: k-th column of A
        """
        pass
```

另外，`_I0` 本质上跟以前没区别。关键是实现 `_I_next`，算法细节已经介绍，代码见下面的链接。

### 代码

相关代码在 [`codes/simplex-algorithms`](https://github.com/xianqiu/linear-programming/tree/main/codes/simplex-algorithms) 文件夹。

* [simplex_degen.py](https://github.com/xianqiu/linear-programming/blob/main/codes/simplex-algorithms/simplex_degen.py) 字典序最小测试比的实现
* [simplex_basic.py](https://github.com/xianqiu/linear-programming/blob/main/codes/simplex-algorithms/simplex_basic.py) 单纯形算法的实现
* [common.py](https://github.com/xianqiu/linear-programming/blob/main/codes/simplex-algorithms/common.py) 定义解的状态，例如 `OPTIMAL`, `UNBOUNDED`
* [test_simplex_degen.py](https://github.com/xianqiu/linear-programming/blob/main/codes/simplex-algorithms/test_simplex_degen.py) 测试代码
* [test-data/cycle.json](https://github.com/xianqiu/linear-programming/blob/main/codes/simplex-algorithms/test-data/cycle.json) 测试用例
* [test-data/degen.json](https://github.com/xianqiu/linear-programming/blob/main/codes/simplex-algorithms/test-data/degen.json)  测试用例

### 注意

我们实现 ` SimplexDegen` 类时用到了**继承**，好处是可以少一些代码。但是，它引入了新的依赖关系，从而增加了代码的**耦合性**。

简单来说，其父类 `SimplexBasic` 的任何变化，可能会影响到 `SimplexDegen`。此外，如果我想修改子类 ` SimplexDegen`，也有必要了解其父类的实现。这种耦合性的增加，会降低代码的可维护性。个人觉得，不是必要的话，就不要使用继承。