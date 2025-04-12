---
weight: 320
title: "处理退化"
description: ""
icon: "article"
date: "2025-03-27T13:42:05+08:00"
lastmod: "2025-03-27T13:42:05+08:00"
draft: false
toc: true
katex: true
---

先看一个例子。

{{<katex>}}
$$
\begin{aligned}
\max~ & x_1 + x_2 + x_3\\
\text{s.t. } & x_1 + x_2 \leq 1\\
& -x_2 + x_3 \leq  0\\
& x_1,x_2,x_3 \geq 0
\end{aligned}
$$
{{</katex>}}

根据 $-x_2 + x_3 \leq 0$ 和 $x_3\geq 0$，可以得到 $x_2\geq 0$。因此，上面约束条件中 $x_2\geq 0$ 是冗余的。这种冗余性，可能会影响单纯形算法的求解效率。

接下来求解这个例子，看看它有什么特点。

### 什么是退化

把它写成标准形式。

{{<katex>}}
$$
\begin{aligned}
\min~ & -x_1 - x_2 - x_3\\
\text{s.t. } & x_1 + x_2 + x_4 = 1\\
& -x_2 + x_3 + x_5 = 0\\
& x_1,x_2,x_3,x_4,x_5 \geq 0
\end{aligned}
$$
{{</katex>}}

迭代步骤如下所示（ [example_degeneracy.py](https://github.com/xianqiu/linear-programming/blob/main/codes/simplex-algorithms/example_degeneracy.py)）。

{{< table  "table-striped-columns">}}
|STEP | OBJ | x | Reduced Costs |
|-|-|-|-|
|0 | 0| [0, 0, 0, **1**, **0**] | [-1, -1, -1, **0**, **0**]|
|1 | -1| [**1**, 0, 0, **0**, 0] | [**0**, 0, -1, **1**, 0]|
|2 | -1| [**1**, 0, **0**, 0, 0] | [**0**, -1, 0, **1**, 1]|
|3 | -2| [0, **1**, **1**, 0, 0] | [1, **0**, **0**, 2, 1]|
{{< /table >}}

其中 OBJ 代表当前 STEP 的目标函数值。x 代表当前 STEP 的基本可行解。x 中粗体的分量代表基变量值。REDUCED COSTS 中粗体的分量的下标与基变量下标对应。

从上面的计算，我们看到第 0-2 步，这三个基本可行解中都存在基变量值为 0 的情况。例如 STEP = 2 时，基变量 $x_3=0$。

这种情况称为**退化（Degeneracy）**。 即，线性规划问题的一个基本可行解，其基变量 $x_B$ 中存在分量值为 0。注意到 $x_B = B^{-1}b$，因此迭代过程中如果 $B^{-1}b$ 存在 0 分量，也意味着问题是退化的。

如上面的例子所示。从第 1 步到第 2 步的迭代，目标函数值并没有降低。说明着这一步是冗余的。在实际应用中，如果存在较多这样的冗余点，不仅会降低算法的效率，而且可能导致循环，即算法不收敛。

### 循环的例子

看下面这个例子，它会让算法陷入**循环（Cycling）**。

{{<katex>}}
$$
\begin{aligned}
\min~ & -10x_1 + 57 x_2 + 9 x_3 + 24 x_4\\
\text{s.t. } & 0.5 x_1 - 5.5 x_2 -2.5x_3 + 9 x_4 + x_5 = 0\\
& 0.5x_1 -1.5x_2 -0.5x_3 +x_4 +x_6 = 0\\
& x_1 + x_7 = 1\\
& x_1,x_2,x_3,x_4,x_5,x_6, x_7 \geq 0
\end{aligned}
$$
{{</katex>}}

迭代步骤如下所示（ [example_degeneracy.py](https://github.com/xianqiu/linear-programming/blob/main/codes/simplex-algorithms/example_degeneracy.py)）。

{{< table  "table-striped-columns">}}
|STEP |Basic Columns |x| OBJ | Reduced Costs |
|-|-|-|-|-|
|0 | [0, 5, 6] | [0, 0, 0, 0, 0, 0, 1] | 0 | [0, -53, -41, 204, 20, 0, 0]|
|1 | [0, 1, 6] | [0, 0, 0, 0, 0, 0, 1] | 0 | [0, 0, -14.5, 98, 6.75, 13.25, 0]|
|2 | [2, 1, 6] | [0, 0, 0, 0, 0, 0, 1] | 0 | [29, 0, 0, -18, -15, 93, 0]|
|3 | [2, 3, 6] | [0, 0, 0, 0, 0, 0, 1] | 0 | [20, 9, 0, 0, -10.5, 70.5, 0]|
|4 | [4, 3, 6] | [0, 0, 0, 0, 0, 0, 1] | 0 | [-22, 93, 21, 0, 0, -24, 0]|
|5 | [4, 5, 6] | [0, 0, 0, 0, 0, 0, 1] | 0 | [-10, 57, 9, 24, 0, 0, 0]|
|6 | [0, 5, 6]| [0, 0, 0, 0, 0, 0, 1] | 0 | [0, -53, -41, 204, 20, 0, 0]|
{{< /table >}}

其中 BASIC COLUMNS 代表基矩阵 $B$ 的列（从 0 开始计数）。

从上面的迭代过程可以看到，在第 6 步的时候，回到了第 0 步的起点 [0, 5, 6]。这个迭代过程会无限循环下去。为了解决循环问题，需要给单纯形算法打个补丁。

### 最小比测试

回顾单纯形算法中如何计算出基变量。已知入基列 $j$，需要计算对应的出基列 $i$。

① 计算 $\tilde{a}_j$，它是 $\tilde{A}$ 中下标为 $j$ 的列。

$$
\tilde{A} := B^{-1}N
$$

例如
{{<katex>}}
$$
\tilde{A} = 
\begin{bmatrix}
\tilde{a}_2 & \tilde{a}_5
\end{bmatrix} 
= \begin{bmatrix}
1 & -3\\
2 & -1\\
0 & 1
\end{bmatrix}
$$
{{</katex>}}

其中 $\tilde{a}$ 的下标 $2, 5$ 对应非基矩阵 $N$ 的列。

② 计算 $ \tilde{b}$ 和 $\tilde{a}_j$ 的**比值（Ratio）**，记作 $r$。

{{<katex>}}
$$
\begin{aligned}
& \tilde{b}:= B^{-1}b\\
& r :=\tilde{b} \div \tilde{a}_j
\end{aligned}
$$
{{</katex>}}
其中 $\div$ 代表分量逐个相除。

例如
{{<katex>}}
$$
\tilde{b} = 
\begin{bmatrix}
\tilde{b}_1\\
\tilde{b}_3\\
\tilde{b}_4
\end{bmatrix}=
\begin{bmatrix}
15\\
125\\
35
\end{bmatrix}
$$
{{</katex>}}
其中 $\tilde{b}$ 的下标 $1, 3, 4$ 对应基矩阵 $B$ 的列。

如果入基变量为 $x_2$，即 $j=2$，那么计算 $\tilde{b}$ 与 $\tilde{a}_2$ 的比值
{{<katex>}}
$$
\begin{aligned}
r &= \tilde{b}\div \tilde{a}_2 =
\begin{bmatrix}
\tilde{b}_1\\
\tilde{b}_3\\
\tilde{b}_4
\end{bmatrix}
\div
\begin{bmatrix}
\tilde{a}_{12}\\
\tilde{a}_{32}\\
\tilde{a}_{42}
\end{bmatrix}\\[6pt]
& = 
\begin{bmatrix}
15\\
125\\
35
\end{bmatrix}\div
\begin{bmatrix}
1\\
2\\
0
\end{bmatrix}=
\begin{bmatrix}
15\\
62.5\\
\infty
\end{bmatrix}
\end{aligned}
$$
{{</katex>}}

③ 计算 $I_0$，即 $r$ 中最小比值的下标集合。

例如

{{<katex>}}
$$
r = 
\begin{bmatrix}
r_{\textcolor{red}{1}} \\
r_3\\
r_4
\end{bmatrix} = \begin{bmatrix}
\textcolor{red}{15}\\
62.5\\
\infty
\end{bmatrix}
$$
{{</katex>}}

在这个例子中

{{<katex>}}
$$
I_0 = \{1\}
$$
{{</katex>}}

在 $I_0$ 中任意选择一个下标，作为出基的列标。在这个例子中，$i=1$ 就是出基列。这个计算过程（即选择最小比对应的列），称为**最小比测试 Minimum Ratio Test**。

如果例子是非退化的，$\tilde{b}$ 的分量始终为正，对应的 $I_0$ 只包含一个元素。因此，每一步迭代是唯一的，而且目标函数值降低。这意味着，不会出现循环。


如果例子是退化的，那么会 $\tilde{b}$ 存在分量为 0 的情况。

例如 $\tilde{b} = [0, 0, 35]^T$，$\tilde{a}_2=[1, 2, 0]^T$。

计算它们的比值

{{<katex>}}
$$
r = \begin{bmatrix}
r_{\textcolor{red}{1}}\\
r_{\textcolor{red}{3}}\\
r_4
\end{bmatrix}
=
\begin{bmatrix}
\textcolor{red}{0}\\
\textcolor{red}{0}\\
\infty
\end{bmatrix}
$$
{{</katex>}}

我们有

{{<katex>}}
$$
I_0 = \{1, 3\}
$$
{{</katex>}}

此时无论选择 $1$ 还是 $3$ 作为出基列，都不会改变目标函数值。因此，当前迭代步骤是冗余的。当存在多个冗余点时，就可能产生循环。


### 字典序测试

为了避免循环，本节介绍一个方法，即**字典序最小比测试（Lexicographic Minimum Ratio Test）**。

已知入基列 $j$，需要计算对应的出基列 $i$。

计算 $I_0$。如果 $I_0$ 只包含一个元素，那么这一步就是上面的最小比测试。如果 $I_0$ 包含多个元素，按照下面的方式接着计算 $I_1$。

① 计算 $\tilde{a}_1$，其中 $\tilde{a}_1 = B^{-1}a_1$，$a_1$ 为 $A$ 中的第 $1$ 列，与 $I_1$ 的下标 $1$ 对应。

例如 
{{<katex>}}
$$
A = \begin{bmatrix}
0.5 & -5.5 & -2.5 & 9 & 1 & 0 & 0\\
0.5 & -1.5 & -0.5 & 1 & 0 & 1 & 0\\
1 & 0 & 0 & 0 & 0 & 0 & 1
\end{bmatrix}
$$
{{</katex>}}

{{<katex>}}
$$
B= \begin{bmatrix}
0.5 & -5.5 & 0\\
0.5 & -1.5 & 0\\
1 & 0  & 1
\end{bmatrix}
$$
{{</katex>}}

那么

{{<katex>}}
$$
\tilde{a}_1= B^{-1}a_1=\begin{bmatrix}
-0.75 & 2.75 & 0\\
-0.25 & 0.25 & 0\\
0.75& -2.75  & 1
\end{bmatrix}\begin{bmatrix}
0.5\\
0.5\\
1
\end{bmatrix}=
\begin{bmatrix}
1\\
0\\
0
\end{bmatrix}
$$
{{</katex>}}

② 计算 $\tilde{a}_j$，其中 $j$ 是已知的入基列。

例如 $j=3$，我们有

{{<katex>}}
$$
\tilde{a}_3= B^{-1}a_3=\begin{bmatrix}
-0.75 & 2.75 & 0\\
-0.25 & 0.25 & 0\\
0.75& -2.75  & 1
\end{bmatrix}\begin{bmatrix}
-2.5\\
-0.5\\
0
\end{bmatrix}=
\begin{bmatrix}
0.5\\
0.5\\
-0.5
\end{bmatrix}
$$
{{</katex>}}

③ 计算 $\tilde{a}_1$ 与 $\tilde{a}_j$ 的比值 $r_1$，只计算 $I_0$ 中的分量，即

{{<katex>}}
$$
r_1 = \begin{bmatrix}\frac{\tilde{a}_{i1}}{\tilde{a}_{ij}}\end{bmatrix}, \quad i\in I_0
$$
{{</katex>}}

例如 {{<katex>}} $ I_0 = \{1, 2\}$ {{</katex>}}，那么

{{<katex>}}
$$
r_1 = \begin{bmatrix}
r_{11}\\
r_{\textcolor{red}{2}1}
\end{bmatrix}=
\begin{bmatrix}
1\\
0
\end{bmatrix}\div
\begin{bmatrix}
0.5\\
0.5
\end{bmatrix}=
\begin{bmatrix}
2\\
\textcolor{red}{0}
\end{bmatrix}
$$
{{</katex>}}

④ 得到 $I_1$，即最小比值对应的下标。
{{<katex>}}
$$
I_1 = \{i | \min r_{i1}, ~i\in I_0\}
$$
{{</katex>}}

例如
{{<katex>}}
$$
r_1 = \begin{bmatrix}
r_{11}\\
r_{\textcolor{red}{2}1}
\end{bmatrix}=
\begin{bmatrix}
2\\
\textcolor{red}{0}
\end{bmatrix}
$$
{{</katex>}}

那么， {{<katex>}}$I_1=\{2\}${{</katex>}}。此时 $I_1$ 只包含一个元素，那么 $i=2$ 就是出基列。

如果 $I_1$ 包含多个元素，按照上面的方法，继续计算 $I_2, I_3, ... I_k$，直到 $I_k$ 只包含一个元素。可以证明，这样的 $I_k$ 是存在的。

**注意** 对任意的 $k\geq 1$，计算 $I_k$ 时，其比值  {{<katex>}}$r_k := \tilde{a}_k \div \tilde{a}_j$  {{</katex>}} 只计算 $I_{k-1}$ 中的下标对应的分量。

可以证明，当满足下面的条件：

1. $A$ 包含单位矩阵 $I_m$，且迭代的起点对应的基矩阵 $B=I_m$。
2. 选择入基变量的策略在算法中的每一步中都保持一致性。例如我们前面介绍的方法，每一步选择最小 $\mu$ 值对应的变量。

使用字典序最小比测试计算出基列，可以保证单纯形算法在有限步内收敛。换句话说，它可以避免循环。

