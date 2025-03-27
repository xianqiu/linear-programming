---
weight: 30
title: "基本可行解"
description: ""
icon: "article"
date: "2025-03-25T13:30:41+08:00"
lastmod: "2025-03-25T13:30:41+08:00"
draft: false
toc: true
katex: true
---

线性规划的约束条件定义了可行区域。如下图所示，可行区域是连续的，其中可行解有无穷多个。那么最优解适否存在。如果存在，如何找到它呢。因此，有必要研究一下最优解的性质。

{{< figure src="vertex.png" width="300px" class="text-center">}}

可以证明如下结论。

{{< alert context="info" text="**定理** 最优解是可行区域的一个顶点。" />}}

注意，顶点的数量是有限的。这样一来，最优解一定存在。可以枚举所有顶点，找到目标函数值最优的顶点。当然，枚举的效率太低，需要设计更好的算法。

但是，有一个概念没讲清楚。那就是，什么是顶点。从几何视角来看，顶点不难理解。接下里，需要从代数角度进行定义，这样才方便计算。

### 标准形

考虑线性规划的标准形式：

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

### 基矩阵

注意 $A$ 是一个 $m$ 行 $n$ 列的矩阵，可以把它看成 $n$ 个 $m$ 维的列向量。
$$
A = [a_1, a_2, ..., a_n]
$$
其中 $a_j \in \mathbb{R}^m$，$j=1,2,...n$。

接下来把 $A$ 拆成两个部分：
$$
A = [B \quad N]
$$
其中 $B$ 包含前 $m$ 列，因此 $B$ 是一个方阵，即 $B\in \mathbb{R}^{m\times m}$；而 $N$ 包含剩下的 $n-m$ 列，因此 $N \in \mathbb{R}^{m \times (n-m)}$。

假设 $A$ 是满秩矩阵，由于 $m\leq n$，那么它的秩是 $m$。考虑 $A$ 的列向量，它有一组**基 (Basis)**，即 $m$ 个线性无关的列向量。

如果 $B$ 不满秩，就把这组基换到前 $m$ 列，因此 $B$ 也是满秩的，或者说可逆的。我们称 $B$ 为**基矩阵 (Basic Matrix)**，称 $N$ 为**非基矩阵 (Non-basic Matrix)**。


### 基变量

相应地，把 $x$ 拆成两个部分，即
{{<katex>}}
$$
x = \begin{bmatrix}
x_B \\
x_N
\end{bmatrix}
$$
{{</katex>}}

其中 

{{<katex>}}
$$
x_B = \begin{bmatrix}
x_1 \\
\vdots\\
x_m
\end{bmatrix}\quad
x_N = \begin{bmatrix}
x_{m+1} \\
\vdots\\
x_n
\end{bmatrix}
$$
{{</katex>}}

把 $x_B$ 对应的变量称为**基变量**， $x_N$ 对应的变量称为**非基变量**。


### 例子

需要注意， $x_B$ 的下标与 $B$ 中的列一一对应。同理，$x_N$ 的下标与 $N$ 中的列一一对应。

举例说明。

{{<katex>}}
$$
A = \begin{bmatrix}
1 & 0 & 0 & 4 & 0\\
0 & 2 & 0 & 0 & 5\\
0 & 0 & 3 & 0 & 0\\
\end{bmatrix}\quad

x = \begin{bmatrix}
x_1\\
x_2\\
\vdots\\
x_5
\end{bmatrix}
$$
{{</katex>}}

接下来划分 $B$ 和 $N$。

从 $A$ 的列中，任选三个线性无关的列作为 $B$。例如，选最后三列。

{{<katex>}}
$$
B = \begin{bmatrix}
3 & 0 & 0\\
0 & 4 & 0 \\
0 & 0 & 5\\
\end{bmatrix}
$$
{{</katex>}}

那么 $N$ 就是剩下的两列。

{{<katex>}}
$$
N = \begin{bmatrix}
1 & 0 \\
0 & 2  \\
0 & 0 \\
\end{bmatrix}
$$
{{</katex>}}

对应的 $x_B$ 和 $x_N$ 如下：

{{<katex>}}
$$
x_B = \begin{bmatrix}
x_3 \\
x_4\\
x_5
\end{bmatrix}\quad
x_N = \begin{bmatrix}
x_1 \\
x_2
\end{bmatrix}
$$
{{</katex>}}

### 基本解

考虑约束条件。把 $Ax=b$ 用分块矩阵来表示。

{{<katex>}}
$$
\begin{aligned}
A x & = 
[B \quad N]
\begin{bmatrix}
x_B\\
x_N
\end{bmatrix}\\
& = Bx_B + N x_N\\
& = b
\end{aligned}
$$
{{</katex>}}

即
$$
Bx_B + N x_N = b
$$
由于 $B$ 可逆，我们得到
$$
x_B = B^{-1}b - B^{-1}Nx_N
$$

令 $x_N = \mathbf{0}$，那么 $x_B = B^{-1}b$，于是
{{<katex>}}
$$
z:= \begin{bmatrix}
x_B\\
x_N
\end{bmatrix} = \begin{bmatrix}
B^{-1}b\\
\mathbf{0}
\end{bmatrix}
$$
{{</katex>}}

满足方程 $Az = b$。那么 $z$ 就称为**基本解 (Basic Solution)**。

### 基本可行解

如果基本解 $z\geq \mathbb{0}$，那么它就是 **基本可行解 (Basic Feasible Solution)**。

可以证明，**可行区域的顶点就是基本可行解**。这两个概念是等价的。也就是说，要在基本可行解中找最优解。