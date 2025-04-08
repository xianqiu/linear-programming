---
weight: 40
title: "两阶段法"
description: ""
icon: "article"
date: "2025-03-27T13:48:18+08:00"
lastmod: "2025-03-27T13:48:18+08:00"
draft: false
toc: true
katex: true
---

单纯形算法需要一个基本可行解作为迭代的起点。在一些简单的例子中，可以通过观察发现起点。但是面对复杂的问题，发现起点并不直观。我们需要一个算法，可以自动计算起点。

本文介绍**两阶段单纯形算法 (Two-phase Simplex Algorithm)**，可以端到端求解线性规划问题。它的思路是这样的。

1. 把原问题转化成一个新问题（**一阶段问题**），使得新问题的一个基本可行解是显而易见的。
2. 用单纯形算法求解第一阶段问题，得到它的最优解。
3. 把第一阶段问题的最优解，转化成原问题（**二阶段问题**）的一个基本可行解，于是得到迭代的起点。
4. 把这个起点作为输入，再次用单纯形算法求解原问题，于是得到原问题的最优解。

### 一阶段问题

考虑标准的线性规划问题
{{<katex>}}
$$
\begin{aligned}
\min~ & c^T x\\ 
\text{s.t.}~ & Ax=b\\
& x\geq 0
\end{aligned}
$$
{{</katex>}}
其中 $c, x \in \mathbb{R}^n$，$A\in\mathbb{R}^{m\times n}$，$b\in\mathbb{R}^m\geq \mathbf{0}$，$n\geq m$。


令 $I_m$ 表示 $m$ 维单位矩阵，$e = (1, 1, \ldots, 1)^T \in \mathbb{R}^n$。引入辅助变量 $y \in \mathbb{R}^m$。

定义如下问题，即一阶段问题。

{{<katex>}}
$$
\begin{aligned}
\min~ & e^T y\\ 
\text{s.t.}~ & Ax + I_m y =b\\
& x, y\geq 0
\end{aligned}
$$
{{</katex>}}

可以证明，原问题有可行解等价于新问题的最优目标函数值为零。不妨假设原问题存在可行解。这样一来，可以通过求解第一阶段问题，从而得到原问题的可行解。

具体来说，我们这样做。注意到 $I_m$ 是一个基矩阵。以 $I_m$ 为起点，用单纯形算法求解一阶段问题。假设 $z^T = [x^T~ y^T]$ 是最优解。那么 $y=\mathbf{0}$，于是 $A x = b$，因此 $x$ 就是原问题的可行解。

### 基本可行解

问题来了，怎么判断 $x$ 是不是原问题的基本可行解。如果不是，怎么把它转换成基本可行解。为了方便描述，先定义一些记号，即用分块矩阵的形式表示一阶段问题的约束与变量。

令 $B$ 和 $N$ 分别代表其基矩阵和非基矩阵，于是 $z$ 也可以写成

{{<katex>}}
$$
z = \begin{bmatrix}
z_B\\
z_N
\end{bmatrix}
$$
{{</katex>}}

考虑到 $z_B, z_N$ 有可能包含 $x$ 和 $y$ 中的分量，令

{{<katex>}}
$$
z_B = \begin{bmatrix}
x_B\\
y_B
\end{bmatrix}, \quad
z_N = \begin{bmatrix}
x_N\\
y_N
\end{bmatrix}
$$
{{</katex>}}
其中 $x_B, y_B$ 是 $x, y$ 的基变量，$x_N, y_N$ 是 $x, y$ 的非基变量。于是，$z$ 可以进一步写成

{{<katex>}}
$$
z = \begin{bmatrix}
z_B \\
z_N 
\end{bmatrix} = \begin{bmatrix}
x_B\\
y_B\\
x_N\\
y_N
\end{bmatrix}
$$
{{</katex>}}

约束条件可以写成这样

{{< katex >}}
$$
\begin{bmatrix}
B  & N
\end{bmatrix}
\begin{bmatrix}
x\\
y
\end{bmatrix}=b
$$
{{< /katex >}}

用 $B^{-1}$ 左乘上式，我们得到

{{< katex >}}
$$
\begin{bmatrix}
I_m  & B^{-1}N
\end{bmatrix}
\begin{bmatrix}
x\\
y
\end{bmatrix}=B^{-1}b
$$
{{< /katex >}}

接下来把系数矩阵 $[I_k \quad  B^{-1}N]$ 的列与变量的列对应起来，可以写成如下形式。

{{< katex >}}
$$
\begin{matrix}
｜& x_B & y_B & x_N & y_N & ｜ & \tilde{b} &| \\
  & -   & -   & -  & -    & & -\\
| & I_k & \mathbf{0} & R_1  & R_3 & | & \tilde{b}_1 & | \\
| & \mathbf{0} & I_{m-k} & R_2  & R_4 & | & \tilde{b}_2 &| \\
\end{matrix}
$$
{{< /katex >}}

其中

{{< katex >}}
$$
B^{-1}N = \begin{bmatrix}
R_1 & R_3\\
R_2 & R_4
\end{bmatrix}
\quad
\tilde{b} := B^{-1}b =
\begin{bmatrix}
\tilde{b}_1\\
\tilde{b}_2
\end{bmatrix}
$$
{{< /katex >}}

由于 $z$ 是通过单纯形算法得到的最优解，它也是基本可行解。我们有

{{<katex>}}
$$
z_N = \begin{bmatrix}
x_N\\
y_N\\
\end{bmatrix}=\begin{bmatrix}
\mathbf{0}\\
\mathbf{0}
\end{bmatrix}
$$
{{</katex>}}

原问题存在可行解，那么最优解 $z$ 的分量 $y=\mathbf{0}$，于是

{{<katex>}}
$$
\tilde{b}_2 = I_{m-k}y_B + R_2 x_N + R_4 y_N = \mathbf{0}
$$
{{</katex>}}

我们得到下表。

{{< katex >}}
$$
\begin{matrix}
｜& x_B & y_B & x_N & y_N & ｜ & \tilde{b} &| \\
  & -   & -   & -  & -    & & -\\
| & I_k & \mathbf{0} & R_1  & R_3 & | & \tilde{b}_1 & | \\
| & \mathbf{0} & I_{m-k} & R_2  & R_4 & | & \mathbf{0} &| \\
\end{matrix}
$$
{{< /katex >}}

其中 $x_B$ 对应 $I_k$，也就是说它对应了 $A$ 的 $k$ 个基列。如果 $k=m$，这 $m$ 个基列就是 $A$ 的基矩阵，也就是说 $x$ 是一个基本可行解。

如果 $k< m$，那么 $x$ 不是一个基本可行解。在这种情况下，可以选择 $m-k$ 个列入基，相应的列出基，使得这 $m$ 个列线性无关，从而得到 $A$ 的一个基矩阵 $B$。如果 $x_B=B^{-1}b \geq 0$，那么 $x^T=[x_B^T, \mathbf{0}^T]$ 就是原问题的基本可行解。

为了保证可行性，入基和出基的过程中，需要保证一阶段问题的解 $z^T = [x^T~ y^T]$ 是最优的。即 $y=\mathbf{0}$ 时，我们有 $Ax=b$ 且 $x\geq \mathbf{0}$。

### 入基和出基

本节描述如何得到原问题的一个基本可行解。通过入基和出基的操作实现。入基列应该来自 $x_N$ 对应的列。因为目标函数值只跟 $y$ 有关，$x_N$ 对应的列入基不会改变目标函数值。

注意到上表中最右边一列的第三行，它是 $\tilde{b}_2 =\mathbf{0}$。根据 [最小比测试](degeneracy#最小比测试)，出基列可以是 $y_B$ 对应的任意列，因为其比值都是 $0$。

总结一下。如果从 $x_N$ 对应的列中任选一列入基，再从 $y_B$ 对应的列中任选一列出基，对应的解仍然是一阶段问题的最优解。那么，对应的 $x$ 也是原问题的可行解。

我们重复这样的操作，直到 $x_B$ 的维度为 $m$，也就是说得到原问题的基本可行解；或者到某一步发现原问题的系数矩阵不满秩（见下文）。

接下来描述出基和入基的详细步骤。

从这张表开始。

{{< katex >}}
$$
\begin{matrix}
｜& x_B & y_B & x_N & y_N & ｜ & \tilde{b} &| \\
  & -   & -   & -  & -    & & -\\
| & I_k & \mathbf{0} & R_1  & R_3 & | & \tilde{b}_1 & | \\
| & \mathbf{0} & I_{m-k} & R_2  & R_4 & | & \mathbf{0} &| \\
\end{matrix}
$$
{{< /katex >}}

为了方便描述，定义一些记号。

令 $\text{col}(y_B, i)$ 代表 $y_B$ 第 $i$ 个分量对应的列。例如 $\text{col}(y_B, 1)$ 就是 
{{< katex >}}
$$
\begin{bmatrix}
\mathbf{0}\\
I_{m-k}
\end{bmatrix}
$$ 
{{< /katex >}}

的第一列，即

{{< katex >}}
$$
\text{col}(y_B, 1) = e_{k+1} = [0, ..., 1, ..., 0]^T
$$
{{< /katex >}}

其中 $e_{k+1}$ 中第 $k+1$ 个分量为 $1$，其余分量为 $0$。

令 $\text{col}(x_N, j)$ 代表 $x_N$ 第 $j$ 个分量对应的列。例如 $\text{col}(X_N, 1)$ 就是 

{{< katex >}}
$$
\begin{bmatrix}
R_1\\
R_2
\end{bmatrix}
$$ 
{{< /katex >}}

的第一列。

接下来要让 $y_B$ 的列出基，$x_N$ 的列入基。

从 $i=1$ 开始。出基列为 $\text{col}(y_B, 1)$。入基列从 $\text{col}(X_N, 1)$ 开始找，直到某一列 $\text{col}(X_N, j)$，它的第 $k+1$ 个分量不等于 $0$，那么它就是出基列。

例如 $k=3$, $m=6$，那么

{{< katex >}}
$$
\text{col}(y_B, 1) = 
\begin{bmatrix}
0\\
0\\
0\\
\textcolor{blue}{1}\\
0\\
0\\
\end{bmatrix}
$$
{{< /katex >}}

假设

{{< katex >}}
$$
\begin{bmatrix}
R_1\\
R_2
\end{bmatrix}
=\begin{bmatrix}
1 & -6 & 0\\
4 & 0 & 6\\
0 & 0 & 3\\
0 & \textcolor{blue}{2} & -1\\
0 & 0 & 0\\
-1 & 0 & -1
\end{bmatrix}
$$
{{< /katex >}}

那么入基列为 $\text{col}(X_N, 2)$。

注意，这样的列有可能不存在。接下来讨论。

此时 $i=2$。 出基列为 $\text{col}(y_B, 2)$。接着上面的例子。

{{< katex >}}
$$
\text{col}(y_B, 2) = 
\begin{bmatrix}
0\\
0\\
0\\
0\\
\textcolor{blue}{1}\\
0\\
\end{bmatrix}
\quad 
\begin{bmatrix}
R_1\\
R_2
\end{bmatrix}
=\begin{bmatrix}
1 & -6 & 0\\
4 & 0 & 6\\
0 & 0 & 3\\
0 & 2 & -1\\
\textcolor{red}{0} & \textcolor{red}{0} & \textcolor{red}{0}\\
-1 & 0 & -1
\end{bmatrix}
$$
{{< /katex >}}

此时 $x_N$ 对应的列都不满足条件。说明这一行对应的约束条件是冗余的。从原问题中删除这一行约束即可。

继续上述步骤 $i=3, 4, ... m-k$，要么找到符合条件的入基列，要么删除冗余的约束。

通过这一系列入基和出基操作，最后得到 $x_B$。它对应的 $x^T = [x_B^T \quad \mathbf{0}^T]$ 就是原问题的基本可行解。

### 二阶段问题

令 $x_B = [x_{j_1}, x_{j_2}, ..., x_{j_s}]^T $，其中 $s\leq m$。如果 $s\leq m$，则代表在上述入基和出基过程中删除了 $m-s$ 个冗余的约束。

令 $i_1, i_s, ..., i_s$ 代表保留的行。

此时原问题等价与如下 **二阶段问题**

{{< katex >}}
$$
\begin{aligned}
\min~ & \sum_{j=1}^n c_jx_j\\
\text{s.t. } & a_{{i_1}1}x_1 + a_{{i_1}1}x_2 ... +  a_{{i_1}1}x_n = b_1\\
& a_{{i_2}1}x_1 + a_{{i_1}1}x_2 ... +  a_{{i_1}1}x_n = b_2\\
& \cdots\\
& a_{{i_s}1}x_1 + a_{{i_1}1}x_2 ... +  a_{{i_1}1}x_n = b_s\\
& x_1, x_2, ..., x_n \geq 0
\end{aligned}
$$
{{< /katex >}}

写成矩阵形式如下

{{< katex >}}
$$
\begin{aligned}
\min~ & c^Tx\\
\text{s.t. } & A'x = b'\\
& x \geq 0
\end{aligned}
$$
{{< /katex >}}

其中
{{< katex >}}
$$
A' = \begin{bmatrix}
a_{{i_1}1} & a_{{i_1}2} & ... & a_{{i_1}n}\\
a_{{i_2}1} & a_{{i_2}2} & ... & a_{{i_2}n}\\
\vdots &\vdots & & \vdots \\
a_{{i_s}1} & a_{{i_s}2} & ... & a_{{i_s}n}\\
\end{bmatrix}
\quad 
b'=\begin{bmatrix}
b_{i_1}\\
b_{i_2}\\
\vdots\\
b_{i_s}
\end{bmatrix}
$$
{{< /katex >}}
令 $A_2$ 代表上面约束条件的系数矩阵。

令 {{<katex >}} $a'_j$ {{</katex>}} 代表 {{<katex>}} $A'$ {{</katex >}} 的第 $j$ 列。那么

{{< katex >}}
$$
\begin{aligned}
B' & = 
\begin{bmatrix}
a'_{j_1} & a'_{j_2} & ... & a'_{j_s}
\end{bmatrix}\\[6pt]
& = 
\begin{bmatrix}
a_{{i_1}{j_1}} & a_{{i_1}{j_2}} & ... & a_{{i_1}{j_s}}\\
a_{{i_2}{j_1}} & a_{{i_2}{j_2}} & ... & a_{{i_2}{j_s}}\\
\vdots &\vdots & & \vdots \\
a_{{i_s}{j_1}} & a_{{i_s}{j_2}} & ... & a_{{i_s}{j_s}}
\end{bmatrix}
\end{aligned}
$$
{{</katex >}}

是二阶段问题的基矩阵。

把 {{<katex >}}$B'${{</katex >}} 作为起点，用单纯形算法计算二阶段问题的最优解。即可得到原问题的最优解以及最优目标函数值。

