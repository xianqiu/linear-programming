---
weight: 783
title: "规模测试"
description: ""
icon: "article"
date: "2025-04-29T11:05:44+08:00"
lastmod: "2025-04-29T11:05:44+08:00"
draft: false
toc: true
---

做个简单的测试，比较一下直接求解和行生成这两种解法。从而更好理解两种方法的使用场景。

### 效率

比较两种方法的求解效率。考虑小规模的例子。随机生成 `100` 个 `m=20, n=100` 的例子。变量的数量是 `m*n+m=2020`，约束的数量是 `m*n+n=2100`。

接下来计算两种方法的平均求解时间。限制求解时间 `timeout = 5` 秒。如果在时间限制内求出最优解，则认为求解成功，否则求解失败。


{{<table  "table-responsive table-striped-columns">}}
|Method|Solved Num.|Mean Time|
|-|-|-|
|`FacilityLocationExact`|100 | 0.43 |
|`FacilityLocationBenders`|57 | 3.61|
{{</table>}}

从实验结果可以看到，在小例子中，行生成方法的求解效率非常低。这是符合预期的。在迭代过程中，主问题的行数不断增加，每一次迭代的耗时会越来越长。

### 规模

接下来考虑大规模的例子。随机生成 `m=50, n=6000` 的例子。变量的数量是 `m*n+m=300,050`，约束的数量是 `m*n+n=306,000`。

限制求解时间 `timeout = 5` 秒。在这样的规模下，两种方法都不能求得最优解。但是行生成方法的好处时可以输出近似结果。

```bash
>> [Solving] Method = FacilityLocationBenders
[iter 0] LB = 49.00, UB = 59786.00, Gap = 59737.00
[iter 1] LB = 122.00, UB = 25893.00, Gap = 25771.00
[iter 2] LB = 277.00, UB = 17573.00, Gap = 17296.00
[iter 3] LB = 826.00, UB = 12267.00, Gap = 11441.00
[iter 4] LB = 4693.00, UB = 9642.00, Gap = 4949.00
[iter 5] LB = 6950.00, UB = 9223.00, Gap = 2273.00
[iter 6] LB = 7431.00, UB = 8384.00, Gap = 953.00
[iter 7] LB = 7481.00, UB = 8384.00, Gap = 903.00
[iter 8] LB = 7521.00, UB = 8384.00, Gap = 863.00
[iter 9] LB = 7544.00, UB = 8384.00, Gap = 840.00
[iter 10] LB = 7580.00, UB = 8384.00, Gap = 804.00
[iter 11] LB = 7598.00, UB = 8384.00, Gap = 786.00
[iter 12] LB = 7615.00, UB = 8384.00, Gap = 769.00
>> [Done] TIMEOUT
Elapsed time: 34.95 seconds
Objective: 8384.0
```

### 代码

相关代码在 [`codes/decomposition/facility-location`](https://github.com/xianqiu/linear-programming/tree/main/codes/decomposition/facility-location) 文件夹。

* [test_runtime.py](https://github.com/xianqiu/linear-programming/blob/main/codes/decomposition/facility-location/test_runtime.py) 测试代码
  * [benders.py](https://github.com/xianqiu/linear-programming/blob/main/codes/decomposition/facility-location/benders.py) 行生成方法
  * [exact.py](https://github.com/xianqiu/linear-programming/blob/main/codes/decomposition/facility-location/exact.py) 直接求解
