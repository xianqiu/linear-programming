---
weight: 620
title: "线性规划建模技巧"
description: ""
icon: "article"
date: "2025-03-22T17:39:17+08:00"
lastmod: "2025-03-22T17:39:17+08:00"
draft: false
toc: true
katex: true
---


本文介绍一些常用的线性规划建模技巧。主要是变量和约束的处理方法。


### 绝对值变量

看这个例子， $|x_j|$ 在目标函数中，并且 $x_j$ 没有非负要求。

{{<katex>}}
$$
\begin{aligned}
\min~ & \sum_j c_j |x_j| \\
\text{s.t. } & a_{ij}x_j \geq b_i, \quad \forall i\\
\end{aligned}
$$
{{</katex>}}

这样的形式不好直接求解。需要把绝对值符号去掉，并且保证变量是非负的。

先定义记号。给定任意的 $x$，令
{{<katex>}}
$$
x^+ = \max\{0,x\}, \quad x^- = -\min\{0, x\}
$$
因此  $x^+, x^-\geq 0$，且
$$
|x| = x^+ + x^-
$$
{{</katex>}}

引入变量 $x_j^+, x_j^- \geq 0$。上面的问题可以写成这样。

{{<katex>}}
$$
\begin{aligned}
\min ~  & \sum_j c_j(x^+_j + x^-_j) \\
\text{s.t. } & \sum_j a_{ij}(x^+_j + x^-_j)  \geq b_i, \quad \forall i\\
& x^+_j, x^-_j \geq 0,\quad \forall j
\end{aligned}
$$
{{</katex>}}

### 平方目标

有些时候目标函数不是线性的。比如线性回归中，目标是平方和误差。

$$
\min f(x) = \sum_i x_i^2
$$

用它的导数去近似

$$
\min f(x) = \sum_i |x_i|
$$

再用绝对值技巧，把它转化成标准形式。

或者用导数的最大值去近似

$$
\min f(x) = \max_j |x_j|
$$

这种情况下，优化目标是最小化一个最大化函数。处理方法下面讲。

### 最小最大目标

考虑下面的问题，目标是最小化是一个最大化函数。这样的目标称为 **最小最大目标（Minimax Objective）**。

{{<katex>}}
$$
\begin{aligned}
\min & \max_k \sum_k c_{kj}x_j\\
\text{s.t. } & \sum_j a_{ij}x_j \geq b_i, \quad \forall i\\
& x_j \geq 0,\quad \forall j
\end{aligned}
$$
{{</katex>}}

为了方便理解这个目标。举个例子，假设 $k=1, 2, 3$，$j=1,2$。那么优化目标就是这样。

{{<katex>}}
$$
\min ~ \max \{c_{11}x_1 + c_{12}x_2, ~ c_{21}x_1 + c_{22}x_2, ~c_{31}x_1 + c_{32}x_2\}
$$
{{</katex>}}

引入新的变量

$$
z := \max_k \sum_k c_{kj}x_j
$$

因此，每一个求和项 $c_{kj}x_j$ 都不超过 $z$。这样一来，目标可以写成 $k$ 个约束

$$
\sum_k c_{kj}x_j \leq z,\quad \forall k
$$

我们得到

{{<katex>}}
$$
\begin{aligned}
\min~ & z \\
\text{s.t. } & \sum_j a_{ij}x_j \geq b_i, \quad \forall i\\
& \sum_k c_{kj}x_j \leq z,\quad \forall k\\
& x_j \geq 0,\quad \forall j
\end{aligned}
$$
{{</katex>}}

### 分数目标

这个例子的目标函数是分数形式。

{{<katex>}}
$$
\begin{aligned}
\min~ & \left(\sum_j c_jx_j +\alpha\right) \div \left(\sum_j d_jx_j +\beta \right) \\[6pt]
\text{s.t. } & \sum_j a_{ij}x_j \geq b_i, \quad \forall i\\
& x_j \geq 0,\quad \forall j
\end{aligned}
$$
{{</katex>}}

引入新的变量

$$
t = \frac{1}{\sum_j d_jx_j +\beta}
$$

目标函数可以写成

$$
\min ~ \sum_j c_jx_j t +\alpha t
$$

由于 $t > 0$，把约束条件两边乘以 $t$ 得到

$$
\sum_j a_{ij}x_jt \geq b_i t, \quad \forall i
$$

再引入新的变量

$$
y_j = x_jt,\quad \forall j
$$

那么

$$
t = \frac{1}{\sum_j d_jx_j +\beta} \Leftrightarrow \sum_j d_jy_j +\beta t = 1
$$

原问题可以写成

{{<katex>}}
$$
\begin{aligned}
\min~ & \sum_j y_j t +\alpha t\\
\text{s.t. } & \sum_j a_{ij} y_j \geq b_it, \quad \forall i\\
& \sum_j d_jy_j +\beta t = 1\\
& t > 0,~ x_j \geq 0,\quad \forall j\\
\end{aligned}
$$
{{</katex>}}

为了求解方便，需要把 $t$ 松弛为 $t\geq 0$。只要原问题的最优解满足 $t>0$，那么这个问题的最优解就跟原问题的最优解本质上是一样的，即 $x_i  = y_i /  t$。

