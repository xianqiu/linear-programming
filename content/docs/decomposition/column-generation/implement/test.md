---
weight: 784
title: "规模测试"
description: ""
icon: "article"
date: "2025-04-22T11:44:56+08:00"
lastmod: "2025-04-22T11:44:56+08:00"
draft: false
toc: true
---

前面讲到直接求解的方法，不适合解大规模问题。那多大的规模，算大规模问题。

回顾 [下料问题](cutting-stock#例子) 的例子，`L` 是原材料长度，`s` 是需求长度，`d` 是需求数量。

* `L = 1000`

* `s = [450, 360, 310, 140]`

* `d = [97, 610, 395, 211]`

我们有 `m=4`。

它的可行矩阵 `A` 代表所有的可行切割。它的维度是 `m×n`，其中  `n` 是可行切割的数量。当 `m` 增加时，`n` 随着 `m` 呈指数增长。下面简单估计一下 `n` 的增长。

### 规模

原材料长度除以需求长度，然后向下取整，得到的结果就是一根原材料能满足的需求数量。例如 `L=1000`，`s[0]=450`，那么 `1000÷450` 的整数部分就是 `2`。

对每个需求长度计算这个数值，于是得到列向量的上界`ub = [2, 2, 3, 7]`。再把 `ub` 中的分量相乘作为 `n` 的估计。在这个例子中 `n ≈ 2×2×3×7=84`。这个估计是 `n` 的一个上界，不同的例子结果也不同。因此，我们主要关注它的量级，而不是具体的数值。

接下来，我们随机生成一些例子，然后计算 `m` 和 `n` 之间的关系。

{{<table "table-responsive table-striped">}}
| m  | n  ||m|n|
| ---- | ---- |-|-|-|
| `5`    |  623    |\|| `13`    |  16941470    |
| `6`    |  2378   |\| |`14`    |  33159642    |
| `7`    |  7310   |\| |`15`    |  182363748    |
| `8`    |  27246   |\| |`16`    |  1675940581    |
| `9`    |  63470    |\||`17`    |  2842892536    |
| `10`    |  301749   |\| |`18`    |  9438043514    |
| `11`    |  727795    |\|| `19`    |  68510658781    |
| `12`    |  3439389    |\||`20`    |  81802185661    |

{{</table>}}

从表格中看到，当 `m = 8`时，`n` 是已经是万级。当 `m = 20` 时，`n` 是百亿级。

接下来我们试试求解。

### 求解

#### 小例子

随机生成 `100` 个  `m=8` 的小例子。限制求解时间 `timeout = 1` 秒。

然后分别用三个算法求解。

* `CutStockExact`：直接求解整数规划，得到精确解。如果求出整数规划问题的最优解，则认为求解成功，否则求解失败。
* `CutStockApprox`：直接求解松弛问题，然后得到近似解。如果求出松弛问题的最优解，则认为求解成功，否则求解失败。
* `CutStockApproxCG`：用列生成求解松弛问题，然后得到近似解。如果求出松弛问题的最优解，则认为求解成功，否则求解失败。

注意：即使列生成 `CutStockApproxCG` 使求解失败，它也能返回原问题的一个可行解。

下表是三种方法的求解时间和成功数量的结果。

{{<table  "table-responsive table-striped-columns">}}
|Method|Solved Num.|Mean Time|
|-|-|-|
|`CutStockExact`|94 | 0.3|
|`CutStockApprox`|94 | 0.26|
|`CutStockApproxCG`|68 | 0.37|
{{</table>}}

从上表可以看到，直接求解的方法大概能够应对 `m <= 8` 的例子。因为是直接求解，前两种方法的计算效率比列生成要高。因此当问题规模小时，没必要用列生成的方法。

接下来考虑大规模的例子。

#### 大例子

随机生成 `100` 个  `m=20` 的大例子。因为例子比较大，把限制求解时间设置为 `timeout = 10` 秒。 

下面是计算结果。

{{<table  "table-responsive table-striped-columns">}}
|Method|Solved Num.|Mean Time|
|-|-|-|
|`CutStockApproxCG`|51 | 5.37|
{{</table>}}

这种情况下，直接求解没法解。列生成的方法就有价值了。其中 51 个例子求出了松弛问题的最优解，其余的例子也能得到可行解。

### 代码

相关代码在 [`codes/decomposition/cutting-stock`](https://github.com/xianqiu/linear-programming/tree/main/codes/decomposition/cutting-stock) 文件夹。

* [test_runtime.py](https://github.com/xianqiu/linear-programming/blob/main/codes/decomposition/cutting-stock/test_runtime.py) 测试代码
  * [column_generation.py](https://github.com/xianqiu/linear-programming/blob/main/codes/decomposition/cutting-stock/column_generation.py) 列生成算法
  * [approximate.py](https://github.com/xianqiu/linear-programming/blob/main/codes/decomposition/cutting-stock/approximate.py) 近似解算法
  * [exact.py](https://github.com/xianqiu/linear-programming/blob/main/codes/decomposition/cutting-stock/exact.py) 精确解算法






