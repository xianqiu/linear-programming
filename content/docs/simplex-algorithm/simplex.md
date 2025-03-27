---
weight: 10
title: "单纯形算法"
description: ""
icon: "article"
date: "2025-03-21T19:35:16+08:00"
lastmod: "2025-03-21T19:35:16+08:00"
draft: false
toc: true
katex: true
---

考虑线性规划问题的标准形式。

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

这个问题还可以这样描述。

找到一个点 {{<katex>}}$x\in P:={\{x| Ax=b, x\geq 0\}}${{</katex>}}，使得目标函数 $f(x):=c^Tx$ 最小化。从几何的角度来看，$P$ 是一个多面体，$x$ 是多面体的一个顶点。

单纯形算法的思路就是，从多面体的某一个顶点开始，然后沿着目标函数减少的方向，迭代到另一个顶点，直到目标函数值无法降低。那么对应的顶点就是最优解。

### 分块矩阵

先把原问题中的矩阵和向量用分块的方式表达。令 $B$ 和 $N$ 分别代表基矩阵和非基矩阵。$A$ 可以写成下面的形式。

{{<katex>}}
$$
A = [B \quad N]
$$
{{</katex>}}

相应地，$x$ 和 $c$ 可以写成
{{<katex>}}
$$
x = \begin{bmatrix}
x_B \\
x_N
\end{bmatrix}\quad
c = \begin{bmatrix} c_B \\
c_N\end{bmatrix}
$$
{{</katex>}}


### 目标函数

用分块矩阵的形式来表示目标函数。

{{<katex>}}
$$
\begin{aligned}
f(x) & = c^Tx \\
& = \begin{bmatrix}
c_B^T & c_N^T
\end{bmatrix}\begin{bmatrix}
x_B\\
x_N
\end{bmatrix}\\
& = c_B^Tx_B + c_N^T x_N \\
\end{aligned}
$$
{{</katex>}}

根据约束条件 $Ax=b$，我们可以计算 $x_B$。

{{<katex>}}
$$
\begin{aligned}
Ax & = \begin{bmatrix}
B & N
\end{bmatrix}\begin{bmatrix}
x_B\\
x_N
\end{bmatrix}\\
& = B x_B + N x_N \\
& = b
\end{aligned}
$$
{{</katex>}}

因此 

$$
x_B = B^{-1}b - B^{-1}N x_N
$$

把 $x_B$ 代入目标函数得到

{{<katex>}}
$$
f(x) = c_B^T B^{-1}b + (c_N^T - c_B^T B^{-1}N) x_N
$$
{{</katex>}}


### 缩减成本

对 $f(x)$ 关于 $x_N$ 求导数
{{<katex>}}
$$
\nabla f(x) = (c_N^T - c_B^T B^{-1}N)^T
$$
{{</katex>}}

令 $\mu := \nabla f(x)$，即
{{<katex>}}
$$
\mu^T = c_N^T - c_B^T B^{-1}N
$$
{{</katex>}}

它表示 $f(x)$ 关于 $x_N$ 的变化率，称为**缩减成本 (Reduced Cost)**。换句话说，$x_j$ 增加一个单位，那么函数值改变 $\mu_j$，$\forall j=m+1, ...,n$。

因此，如果存在 $j$ 使得 $\mu_j < 0$，那么 $x_j$ 增加一个单位，目标函数值就减少 $-\mu_j$。但是要注意，$x_j$ 的值不能任意改变，因为要保证可行性，即满足条件 {{<katex>}}$Ax=b$ {{</katex>}} 和 {{<katex>}}$x\geq 0${{</katex>}}。

下面我们描述如何保证可行性。

### 出基入基

根据前面的计算，我们知道 $x$ 可以表示成下面的形式。
{{<katex>}}
$$
x = \begin{bmatrix}
x_B\\
x_N
\end{bmatrix}=
\begin{bmatrix}
B^{-1}b - B^{-1}N x_N\\
x_N
\end{bmatrix}
$$
{{</katex>}}

可以验证 $Ax=b$。因此，只需要保证等式最右边是非负的，那么 $x$ 就是可行的。即

{{<katex>}}
$$
\begin{aligned}
& B^{-1}b - B^{-1}N x_N \geq 0, \\
& x_N\geq 0
\end{aligned}
$$
{{</katex>}}

为了简化描述，引入两个记号

{{<katex>}}
$$
\tilde{b} := B^{-1}b = \begin{bmatrix}
\tilde{b}_1\\
\tilde{b}_2\\
\vdots\\
\tilde{b}_m
\end{bmatrix}
$$
{{</katex>}}

{{<katex>}}
$$
\tilde{A} := B^{-1}N = \begin{bmatrix}
\tilde{a}_{1, m+1}, \tilde{a}_{1, m+2}, ..., \tilde{a}_{1, n}\\
\tilde{a}_{2, m+1}, \tilde{a}_{2, m+1}, ..., \tilde{a}_{2, n}\\
\vdots\\
\tilde{a}_{m, n}, \tilde{a}_{m, m+1}, ..., \tilde{a}_{m, n}
\end{bmatrix}
$$
{{</katex>}}

这样一来，上述两个条件可以写成

{{<katex>}}
$$x=
\begin{bmatrix}
\tilde{b} - \tilde{A} x_N \\
x_N
\end{bmatrix}
\geq\mathbf{0}
$$
{{</katex>}}

再把它写成分量的形式

{{<katex>}}
$$x=
\begin{bmatrix}
\tilde{b}_1 - \sum_{k=m+1}^n \tilde{a}_{1,k}x_k \\
\vdots\\
\tilde{b}_m - \sum_{k=m+1}^n \tilde{a}_{m,k}x_k \\[6pt]
x_{m+1}\\
\vdots\\
x_{n}
\end{bmatrix}
\geq\mathbf{0}
$$
{{</katex>}}

接下来要以一个基本可行解为起点，沿着目标函数值下降的方向迭代。为了简化符号，仍然用 $x$ 来表示这个起点。那么在上面的式子中，$x_j=0$，$\forall j = m+1, ...,n$。

迭代的方向通过计算 $\mu$ 得到。如果当前 $x$ 不是最优解，那么存在某个 $j$ 使得 $\mu_j < 0$。换句话说，这表示目标函数值可以进一步降低。

把 $x_j$ 增加 $\delta$，其中 $\delta > 0$，即 $x_j := x_j + \delta$，我们有

{{<katex>}}
$$x=
\begin{bmatrix}
\tilde{b}_1 - \sum_{k=m+1}^n \tilde{a}_{1,k}x_k  - \tilde{a}_{1,j}\delta \\
\vdots\\
\tilde{b}_m - \sum_{k=m+1}^n \tilde{a}_{m,k}x_k - \tilde{a}_{m, j}\delta\\[6pt]
x_{m+1}\\
\vdots\\
x_j+\delta\mu_j\\
\vdots\\
x_{n}
\end{bmatrix}
$$
{{</katex>}}

根据前面的假设，起点 $x$ 是一个基本可行解。那么 $x_j=0$，$\forall j=m+1, ..., n$。

于是上式可以写成
{{<katex>}}
$$x=
\begin{bmatrix}
\tilde{b}_1  - \tilde{a}_{1,j}\delta \\
\vdots\\
\tilde{b}_m - \tilde{a}_{m, j}\delta \\[6pt]
0\\
\vdots\\
\delta\\
\vdots\\
0
\end{bmatrix}
$$
{{</katex>}}

要保证可行性，只需要上式每个分量非负，即
{{<katex>}}
$$
\tilde{b}_i  - \tilde{a}_{i,j}\delta \geq 0,\quad \forall i = 1, 2, ...,m
$$
{{</katex>}}

如果 $\tilde{a}_{i,j} < 0$，$\forall i=1, 2, ...,m$，那么 $\delta$ 可以无穷大，目标函数值就是负无穷，因而问题没有最优解。

假设原问题有最优解。那么存在 $i$ 使得 $\tilde{a}_{i,j} > 0$。注意到起点是基本可行解，那么 $x_B =  B^{-1}b \geq 0$。注意，这里 $x_B$ 中的 $x$ 指的是起点。因此，$\tilde{b}_i \geq 0$。

于是，$\delta$ 可以按如下公式取值。

{{<katex>}}
$$
\delta = \min \left\{ \frac{\tilde{b}_i}{\tilde{a}_{i,j}} \text{ and } \tilde{a}_{i,j} > 0, \quad i=1,2,\ldots, m \right\}
$$
{{</katex>}}

容易验证，上式 $x$ 中的每个分量都非负，因此迭代后的解也是可行的。

回顾这个迭代过程。已知 $\mu_j < 0$，于是把 $x_j$ 的值增加到 $\delta$。假设原问题有界。因而存在某个某个下标 $i$ ，使得 $\tilde{a}_{i,j} > 0$ 且

{{<katex>}}
$$
\delta = \frac{\tilde{b}_i}{\tilde{a}_{i,j}}
$$
{{</katex>}}

于是
{{<katex>}}
$$
x_i  = \tilde{b}_i  - \tilde{a}_{i,j}\delta  = 0
$$
{{</katex>}}

这意味着 $x_j$ 从之前的非基变量变成了基变量（简称**入基变量**），而 $x_i$ 从之前的基变量变成了基变量（简称**出基变量**）。这个迭代过程，就是从一个基本可行解，移动到了令一个基本可行解，并且使得目标函数值降低。

### 算法描述

先明确算法的输入与输出。

* **输入** 根据线形规划的标准形式，$A\in\mathbb{R}^{m\times n}, b\in\mathbb{R}^m_+, c\in\mathbb{R}^n$ 定义一个线性规划问题。注意：$A$ 是满秩矩阵，即 $A$ 的秩是 $m$，且 $n\geq m$。

  此外，单纯形算法需要一个起点 $s$。它是一个基本可行解，即 $A$ 中 $m$ 个线性无关的列向量。因此可以用列标的集合来表示 $s$，例如 {{<katex>}}$s=\{1, 2, ..., m\}${{</katex>}} 代表 $A$ 的前 $m$ 列。

* **输出** 返回最优解或者判断无界，即最优目标函数值是负无穷。注意，由于存在初始解，那么可行区域非空，不存在无解的情况。

接下来描述单纯形算法。

**第 0 步：初始化**

输入线性规划问题的参数 $A, b, c$ 和起点 $s$。根据起点 $s$ 计算对应的基矩阵 $B$ 和非基矩阵 $N$。

令 $A=[a_1, a_2, ..., a_n]$，其中 $a_j$ 代表 $A$ 的列向量。我们有

{{<katex>}}
$$
\begin{aligned}
& B = [a_j]  \quad  j\in s \\
& N = [a_j] \quad j \not\in s
\end{aligned}
$$
{{</katex>}}

**第 1 步：判断最优性**

计算 $\mu^T = c_N^T - c_B^T B^{-1}N$。注意：$\mu$ 和 $c_N$ 的下标与 $N$ 的列标对应；$c_B$ 的下标与 $B$ 的列标对应。

如果 $\mu \geq 0$，则满足最优性条件，并返回当前解 $x$。

**第 2 步：入基和出基**

计算出基变量的下标 $i$ 和入基变量的下标 $j$；或者返回无界，即最优目标函数值为负无穷。

① 计算入基变量下标 $j$。在 $\mu$ 中找到一个分量 $j$ 使得 $\mu_j < 0$ 即可。

② 判断最优目标函数值是否有界。

计算 $\tilde{b} = B^{-1}b$ 和 $\tilde{A}=B^{-1}N$。注意：$\tilde{A}$ 的列标与 $N$ 的列标对应。

考虑 $\tilde{A}$ 的第 $j$ 列，记作 $\tilde{a}_j$，即

{{<katex>}}
$$
\tilde{a}_j = \begin{bmatrix}
\tilde{a}_{1, j}\\
\tilde{a}_{2, j}\\
\vdots\\
\tilde{a}_{m, j}
\end{bmatrix}
$$
{{</katex>}}

如果 $\tilde{a}_j \leq 0$，则返回无界。

③ 计算出基变量的下标。

{{<katex>}}
$$
i = \arg\min_k \left\{ \frac{\tilde{b}_k}{\tilde{a}_{k,j}}\text{ and } \tilde{a}_{k,j} > 0, \quad k=1,2,\ldots, m \right\}
$$
{{</katex>}}

**第 3 步：更新**

更新变量值
{{<katex>}}
$$
x_i = 0, \quad x_j = \frac{\tilde{b}_i}{\tilde{a}_{j,j}}
$$
{{</katex>}}
其中 $i$ 和 $j$ 是上一步计算的出基变量和入基变量的下标。

更新更新基矩阵 $B$ 和 非基矩阵 $N$。即，把 $a_j$ 和 $a_i$ 交换位置。

回到第 1 步。

