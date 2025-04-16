---
weight: 420
title: "割平面法"
description: ""
icon: "article"
date: "2025-03-22T17:12:29+08:00"
lastmod: "2025-03-22T17:12:29+08:00"
draft: false
toc: true
katex: true
---

考虑如下的整数规划问题。

{{<katex>}}
$$
\begin{aligned}
\max~ & c^Tx \\
& Ax = b\\
& x\geq 0\\
& x\in \mathbb{Z}^n
\end{aligned}
$$
{{</katex>}}

其中 $A\in\mathbb{R}^{m\times n}, b\in\mathbb{R}^m, c\in \mathbb{R}^n$。

对应的线性规划问题称为它的**松弛问题**。割平面法就是对松弛问题求解。如果最优解不是整数解，就增加新的约束，直到获得整数解。

从几何角度来看，等式可以看成超平面。一个不等式相当于把一个空间切分成两半，然后取其中一半。这样一来，可以通过增加约束，切掉非整数解。

{{< figure src="cut.gif" width="200px" class="text-center">}}

这样的不等式也称为 **割平面（Cutting Plane）**。

### 割平面

介绍一种构造割平面的方法，称为 **Gomory-Chvátal Cut**，简称 GC 割。

回顾[单纯形算法](../simplex-method/simplex)，我们可以把约束条件用分块矩阵表示。令 $B$ 和 $N$ 代表基矩阵和非基矩阵，$x_B, x_N$ 代表对应的基变量和非基变量。约束条件可以写成

{{<katex>}}
$$
x_B + B^{-1}Nx_N = B^{-1}b
$$
{{</katex>}}

令 $\tilde{b} = B^{-1}b$。令 $J$ 代表非基变量的下标。再把 $B^{-1}N$ 写成列向量的形式。

{{<katex>}}
$$
B^{-1}N = [\tilde{a}_{j} ], \quad j\in J
$$
{{</katex>}}

我们有

{{<katex>}}
$$
x_B + \sum_{j\in J}\tilde{a}_{j} x_j = \tilde{b}
$$
{{</katex>}}

把上式中 $\tilde{a}_j$ 向下取整，我们有
{{<katex>}}
$$
x_B + \sum_{j\in J} \lfloor \tilde{a}_j \rfloor x_j \leq \tilde{b}
$$
{{</katex>}}

由于 $x$ 是可行解，那么它的分量都是整数。因此，不等式的左边是整数向量。那么，对不等式右边的向量 $\bar{b}$ 进行取整，不等式依然成立。

我们得到

{{<katex>}}
$$
x_B + \sum_{j\in J} \lfloor \tilde{a}_j \rfloor x_j \leq \lfloor\bar{b}\rfloor
$$
{{</katex>}}

由于 $x_B=  \tilde{b} - \sum_{j\in J}\tilde{a}_{j} x_j$，代入上式得到 **GC 割**。
{{<katex>}}
$$
\sum_{j\in J}(\bar{a}_j-\lfloor \tilde{a}_j\rfloor) x_j \geq \tilde{b} - \lfloor\tilde{b}\rfloor
$$
{{</katex>}}

### 例子

{{<katex>}}
$$
\begin{aligned}
\max~ & 4x_1+5x_2\\
\text{s.t. } & x_1+4x_2 \leq 10\\
& 3x_1-4x_2 \leq 6\\
& x_1, x_2 \in \mathbb{Z}_+
\end{aligned}
$$
{{</katex>}}

它的松弛问题如下

{{<katex>}}
$$
\begin{aligned}
\max~ & 4x_1+5x_2\\
\text{s.t. } & x_1+4x_2 \leq 10\\
& 3x_1-4x_2 \leq 6\\
& x_1, x_2 \geq 0
\end{aligned}
$$
{{</katex>}}

先引入松弛变量 $x_3, x_4$，把上面的不等式写成等式形式。

{{<katex>}}
$$
\begin{aligned}
\max~ & 4x_1+5x_2\\
\text{s.t. } & x_1+4x_2 + x_3 = 10\\
& 3x_1-4x_2 + x_4 = 6\\
& x_1, x_2, x_3, x_4 \geq 0
\end{aligned}
$$
{{</katex>}}

它的最优解为 $x_1=4, x_2=1.5$。

{{<katex>}}
$$
\begin{aligned}
& B^{-1}N = \begin{bmatrix}
\tilde{a}_3 & \tilde{a}_4
\end{bmatrix} = 
\begin{bmatrix}
-0.0625 & 0.1875\\
0.25 & 0.25
\end{bmatrix}\\[6pt]
& \tilde{b} = B^{-1}b = 
\begin{bmatrix}
1.5\\
4
\end{bmatrix}
\end{aligned}
$$
{{</katex>}}

接下来对向量进行取整，并计算它们的差值。

{{<katex>}}
$$
\begin{aligned}
& \tilde{a}_3 -\lfloor\tilde{a}_3\rfloor = 
\begin{bmatrix}
-0.0625\\
0.25
\end{bmatrix} 
- \begin{bmatrix}
-1\\
0
\end{bmatrix}=\begin{bmatrix}
0.9375\\
0.25
\end{bmatrix}\\[6pt]
& \tilde{a}_4 -\lfloor\tilde{a}_4\rfloor = 
\begin{bmatrix}
0.1875\\
0.25
\end{bmatrix} 
- \begin{bmatrix}
0\\
0
\end{bmatrix}=\begin{bmatrix}
0.1875\\
0.25
\end{bmatrix}\\[6pt]
& \tilde{b} -\lfloor\tilde{b}\rfloor = 
\begin{bmatrix}
1.5\\
4
\end{bmatrix} 
- \begin{bmatrix}
1\\
4
\end{bmatrix}=\begin{bmatrix}
0.5\\
0
\end{bmatrix}
\end{aligned}
$$
{{</katex>}}

再把结果代入下面的不等式。

{{<katex>}}
$$
(\tilde{a}_3-\lfloor \tilde{a}_3\rfloor) x_3 + (\tilde{a}_4-\lfloor \tilde{a}_4 \rfloor ) x_4 \geq \tilde{b}-\lfloor \tilde{b} \rfloor
$$
{{</katex>}}

我们得到

{{<katex>}}
$$
\begin{bmatrix}
0.9375\\
0.25
\end{bmatrix}x_3 + 
\begin{bmatrix}
0.1875\\
0.25
\end{bmatrix}x_4
\geq \begin{bmatrix}
0.5\\
0
\end{bmatrix}
$$
{{</katex>}}

即

{{<katex>}}
$$
\begin{aligned}
& 0.9375x_3 + 0.1875 x_4 \geq 0.5\\
& 0.25 x_3 + 0.25 x_4 \geq 0 \\
\end{aligned}
$$
{{</katex>}}

把它们添加到松弛问题中，然后重复上面的步骤，直到得到整数解。

### 算法描述

简要描述算法步骤。

**第 0 步：初始化**

考虑如下松弛问题。

{{<katex>}}
$$
\begin{aligned}
\max~ & c^Tx \\
& Ax = b\\
& x\geq \mathbf{0}\\
\end{aligned}
$$
{{</katex>}}

**第 1 步：求解**

求解松弛问题。如果得到整数解，它就是最优解。算法停止，并返回最优解。否则执行下一步。

**第 2 步：生成割平面**

生成割平面，把它添加到松弛问题中。再执行第 1 步。
