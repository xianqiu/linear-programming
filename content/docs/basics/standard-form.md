---
weight: 10
title: "标准形式"
description: ""
icon: "article"
date: "2025-03-21T19:38:06+08:00"
lastmod: "2025-03-21T19:38:06+08:00"
draft: false
toc: true
katex: true
---

考虑一个线性规划的例子。

{{<katex>}}
$$
\begin{aligned}
\max~ & 7x_1 + 6 x_2\\
\text{s.t.}~ & 3x_1 + x_2 \leq 120 \\
& x_1 + 2x_2 \leq 160 \\
& x_1 \leq 35 \\
\end{aligned}
$$
{{</katex>}}

其中第一行是目标函数，其中 `max`​ 代表优化方向，即最大化目标函数值。接下来是三个约束条件，分别用不等式来描述，其中 `s.t.` 是 `subject to` 的缩写）。

求解这个问题，就要找到满足约束条件的 $x_1,x_2$，使得目标函数值最大。

### 矩阵形式

接下来我们把它写成矩阵的形式。定义列向量 $c$ 和 $x$:
{{<katex>}}
$$
c = \begin{bmatrix}
7\\
6
\end{bmatrix}\quad
x = \begin{bmatrix}
x_1\\
x_2
\end{bmatrix}
$$
{{</katex>}}
那么目标函数可以写成 $c^Tx$。
定义矩阵 $A$ 和 列向量 $b$: 

{{<katex>}}
$$
A = \begin{bmatrix}
3 & 1 \\
1 & 2 \\
1 & 0 
\end{bmatrix}\quad
b = 
\begin{bmatrix}
120\\
160\\
35
\end{bmatrix}
$$
{{</katex>}}
那么约束条件可以写成 $Ax\leq b$。

因此，它可以写成下面的形式。

{{<katex>}}
$$
\begin{aligned}
\max~ & c^Tx \\
\text{s.t. } & Ax\leq b.
\end{aligned}
$$
{{</katex>}}

### 简化问题

在不改变最优解的前提下，我们可以对问题的形式进行简化。

1. 把最大化问题转化成最小化问题。

   假设 $x^*$ 使得 $f(x) = c^Tx$ 最大，那么它就使得 $-f(x) = - c^Tx$ 最小。因此，$\max c^Tx$ 可以转化成 $\min -c^Tx$，而不会改变最优解。

   例：$\max 7x_1 + 6x_2$。它可以写成 $\min -7x_1 - 6x_2$。

2. 把不等式变成等式。

   例： $3x_1+x_2\leq 120$。引入新变量 $x_3$ 当作不等式两边的差值，那么原来的不等式可以写成等式，即
   $$
   3x_1 + x_2 + x_3 = 120
   $$
   这个操作不会改变原问题的最优解。

3. 把等式右边的常数变成非负。

   例：$-3x_1-x_2 = -120$。等式两边同时乘以 $-1$ 即可。

4. 把变量变成非负。

   设 $x \in\mathbb{R}$，引入非负变量 $x^+ = \max(x, 0), x^- = -\min(x, 0)$ 。这样一来，$x$ 可以表示成 $x = x^+ - x^-$。

   例：$x_1+2x_2 = 160$，$x_1,x_2\in \mathbb{R}$。

   引入非负变量 $x_{11}=\max(x_1,0), x_{12}=-\min(x_1,0)$，那么 $x_1=x_{11}+x_{12}$；再令 $x_{21}=\max(x_2,0), x_{22}=-\min(x_2,0)$，那么 $x_2 = x_{21} + x_{22}$。

   代入等式，得到 $x_{11} + x_{12} + 2(x_{21}+x_{22})= 160$。

### 标准形式

综上所述，我们得到线性规划的**标准形式**。
{{<katex>}}
$$
\begin{aligned}
\min~ & c^T x\\
\text{s.t.}~ & Ax=b\\
& x\geq 0
\end{aligned}
$$
{{</katex>}}

其中 $c, x \in \mathbb{R}^n$，$A\in\mathbb{R}^{m\times n}$，$b\in\mathbb{R}^m \geq \mathbf{0}$，$n\geq m$。

注意：如果 $n < m$，可以添加冗余变量使得 $n\geq m$。



如果不用矩阵形式，标准形式也可以写成这样。

{{<katex>}}
$$
\begin{aligned}
\min~ & c_1x_1 + c_2x_2 + ... + c_nx_n\\
\text{s.t. }~ & a_{11}x_1 + a_{12}x_2 + ... + a_{1n}x_n = b_1 \\
& a_{12}x_2 + a_{22}x_2 + ... + a_{2n}x_n = b_2 \\
& \quad \vdots\\
& a_{m1}x_1 + a_{m2}x_2 + ... + a_{mn}x_n = b_m \\
& x_1, ..., x_n \geq 0
\end{aligned}
$$
{{</katex>}}

