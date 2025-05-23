---
weight: 713
title: "列生成"
description: ""
icon: "article"
date: "2025-03-22T17:07:49+08:00"
lastmod: "2025-03-22T17:07:49+08:00"
draft: false
toc: true
katex: true
---

考虑下料问题的松弛问题。它的变量数量 $n$ 是约束数量  $m$ 的指数关系。

{{<katex>}}
$$
\begin{aligned}
\min ~ & \sum_{j=1}^n x_j \\
\text{ s.t. } &  \sum_{j=1}^n a_{i,j} x_j = d_i, ~i =1,2,...,m  \\
& x_j \geq 0, ~\forall j
\end{aligned}
$$
{{</katex>}}

当 $m$ 比较大时，不适合直接求解。本文用列生成的方法来求解这个问题。

### 主问题

考虑它的矩阵形式。

{{<katex>}}
$$
\begin{aligned}\min~ &e^T x \\
& Ax = d \\
& x \geq 0
\end{aligned}
$$
{{</katex>}}

其中 $e=[1, 1, ..., 1]^T$，$d=[d_1, d_2, ..., d_m]^T$。

系数矩阵 $A$ 的维度是 $m\times n$，其中 $n$ 远大于 $m$。我们知道，线性规划的最优解是一个基本可行解。也就是说，最优解只包含 $A$ 的 $m$ 列。换句话说，$A$ 的大部分列，可能不需要考虑。

基于这样的观察。初始化的时候，我们只考虑 $m$ 列。

{{<katex>}}
$$
A =\begin{bmatrix}
1 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
$$
{{</katex>}}

假设最优解对应的基矩阵是 $B^\*$。如果 $A=B^\*$，直接解这个问题，就得到最优解。否则，我们可以通过计算，得到 $B^*$ 中的列，再把它们添加到 $A$ 中。

说明一下，找到 $B^*$ 的列是可行的。最坏的情况下，可以枚举所有的可行切割，那么一定包含 $B^\*$ 的列。但是这样一来，就等同于直接求解。因此，需要巧妙的方式来计算 $B^\*$ 中的列。

### 子问题

设 $y = [y_1, y_2, ..., y_m]^T$ 代表一个可行切割。我们有

$$
s^T y \leq L
$$

其中 $L$ 是原材料的长度，$s=[s_1, s_2, ..., s_m]^T$ 是每种产品类型的长度需求。在这个例子中 $s = [450, 360, 310, 140]^T$。


如果把 $y$ 添加到主问题的系数矩阵 $A$ 中，我们期望 $y$ 能作为入基列，使得主问题的目标函数值降低。 

回顾[单纯形算法](../../simplex-method/simplex)，目标函数关于非基变量的梯度称为缩减成本（
Reduced Cost），即

$$
\mu^T_N = c^T_N - c^T_B B^{-1} N
$$

其中 $B$ 和 $N$ 对应基本矩阵和非基矩阵；$c_B$ 和 $c_N$ 作为系数，对应基变量和非基变量。

根据这个公式，可以计算 $y$ 对应的缩减成本 $\mu_y$。如果 $\mu_y < 0$ 时，说明目标函数可以下降。因此，我们希望 $y$ 使得缩减成本 $\mu_y$ 越小越好。

下面计算 $\mu_y$。注意 $y$ 是非基列，因此它是 $N$ 的某一列。它对应的非基变量的系数记作 $c_y$。我们有

$$
\mu_y = c_y - c^T_B B^{-1}y
$$

在下料问题中 $c = (1, 1, ..., 1)^T$，我们有 $c_y=1$。于是

$$
\mu_y = 1 - c^T_B B^{-1}y
$$

令 $\lambda^T = c^T_B B^{-1}$，称为影子价格（Shadow Price），或者也叫对偶变量值。上式也可以写成

$$
\mu_y = 1 - \lambda^T y
$$

目标是最小化 $\mu_y$，即

$$
\min~ 1-\lambda^T y ~ \Leftrightarrow~  \max~ \lambda^Ty
$$

这样一来，我们得到下面的子问题。

{{<katex>}}
$$
\begin{aligned}
\max~ & \lambda^T y \\
\text{s.t. } & s^T y \leq L \\
& y \in \mathbb{N}^m
\end{aligned}
$$
{{</katex>}}

解这个子问题，得到的解 $y$ 是一个可行切割。如果最优目标函数值 $\lambda^T y > 1$，于是 $\mu_y < 0$，把它添加到主问题系数矩阵 $A$ 的列然后求解主问题，目标函数值会降低。如果 $\lambda^T y \leq 1$，就说明不存在一个列，使得主问题的目标函数值降低，于是得到最优解。

注意，子问题是一个整数规划问题。一般来说，整数规划问题的求解效率是较低的。但是这里问题的规模不大，变量个数是 $m$，约束个数是 1。

### 算法描述

用 [下料问题](cutting-stock) 中的例子来描述算法的流程。

**第一步，初始化**

初始化系数矩阵

{{<katex>}}
$$
A :=\begin{bmatrix}
1 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
$$
{{</katex>}}

**第二步，求解主问题**

{{<katex>}}
$$
\begin{aligned}\min~ & e^Tx \\
& Ax = d \\
& x \geq 0
\end{aligned}
$$
{{</katex>}}

其中

{{<katex>}}
$$
\begin{aligned}
& e= \begin{bmatrix}1 & 1 & ... & 1\end{bmatrix}^T
\\
& d = \begin{bmatrix}97 &  610 & 395 &  211 \end{bmatrix}
\end{aligned}
$$
{{</katex>}}

注意，$e$ 和 $x$ 的维度与系数矩阵 $A$ 列的数量相同。当 $A$ 增加列时，$e$ 和 $x$ 的维度也要相应地增加。

**第三步，求解子问题**

{{<katex>}}
$$
\begin{aligned}
\max~ & \lambda^T y \\
\text{s.t. } & s^T y \leq L \\
& y \in \mathbb{N}^m
\end{aligned}
$$
{{</katex>}}

其中 $s^T=(450,360,310,140)$，代表四种需求长度；$\lambda=e^T B^{-1}$ 是主问题的对偶变量值。

如果 $\mu_y = 1-\lambda^T y \geq 0$，那么停止迭代。第二步得到的解就是最优解。否则执行下一步。

**第四步，增加一列**

把 $y$ 添加到主问题的列，即

{{<katex>}}
$$
A:= \begin{bmatrix} A & y
\end{bmatrix}
$$
{{</katex>}}

相应地，$e$ 和 $x$ 的维度增加 1。回到 **第二步**。

###  总结

本文以下料问题为例，介绍了列生成方法。它是一种基于单纯形算法的间接求解方法，适合这种指数多个变量的问题。

相比直接求解原问题，列生成可以降低问题规模，让问题变得可解。求解的过程，就是不断求解主问题和子问题，直到满足停止条件。

此外，列生成算法还有一个好处。它在迭代过程中始终得到松弛问题的一个可行解。因此，可以随时停止迭代，不会出现无解的情况。