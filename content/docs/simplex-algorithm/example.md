---
weight: 15
title: "算法示例"
description: ""
icon: "article"
date: "2025-03-27T13:47:58+08:00"
lastmod: "2025-03-27T13:47:58+08:00"
draft: true
toc: true
katex: true
---

为了更好理解[单纯形算法](simplex)，我们看一个具体的例子。

{{<katex>}}
$$
\begin{aligned}
\max ~ & 7x_1 + 6x_2 \\
\text{s.t. } & 3x_1 + x_2 \leq 120\\
& x_1 + 2x_2 \leq 160 \\
& x_1 \leq 35 \\
& x_1, x_2 \geq 0
\end{aligned}
$$
{{</katex>}}

这是一个最大化问题，而且约束是不等式。接下来把它转化成标准形式。

### 标准形式

引入松弛变量 $x_2, x_4, x_5 \geq 0$。把不等式改写成等式，目标函数改写成最小化，得到如下标准形式。

{{<katex>}}
$$
\begin{aligned}
& \min~ -7x_1 - 6x_2 + 0 x_3 + 0 x_4 + 0x_5\\
& \begin{matrix}
& 3x_1 & + & x_2  & + x_3 &       &       & = &120 \\
& x_1  & + & 2x_2 &       & + x_4 &       & = & 160 \\
& x_1  &   &      &       &       & + x_5 & = & 35
\end{matrix}
\end{aligned}
$$
{{</katex>}}

矩阵形式就是这样。

{{<katex>}}
$$
\begin{aligned}
\min~ &
\begin{bmatrix}
-7 & -6 & 0 & 0 & 0
\end{bmatrix}\cdot \begin{bmatrix}
x_1\\
\vdots\\
x_5
\end{bmatrix} \\[6pt]
\text{s.t. } & \begin{bmatrix}
3  &  1 & 1 & 0 & 0 \\
1  &  2 & 0 & 1 & 0 \\
1  &  0 & 0 & 0 & 1
\end{bmatrix}
\begin{bmatrix}
x_1\\
\vdots\\
x_5
\end{bmatrix} 
=
\begin{bmatrix}
120\\
160\\
35
\end{bmatrix}\\[18pt]
&~~ x^T =[x_1, x_2, x_3, x_4, x_5] \geq \mathbf{0}
\end{aligned}
$$
{{</katex>}}

注意：新问题的最优目标函数值等于原问题最优目标函数值乘以-1。

### 初始点

单纯形算法的输入是 $A,b,c,s$。已知
{{<katex>}}
$$
A = \begin{bmatrix}
3  &  1 & 1 & 0 & 0 \\
1  &  2 & 0 & 1 & 0 \\
1  &  0 & 0 & 0 & 1
\end{bmatrix}
\quad
b = \begin{bmatrix}
120\\
160\\
35
\end{bmatrix}
\quad 
c = \begin{bmatrix}
-7\\ 
-6\\
0\\
0\\
0
\end{bmatrix}
$$
{{</katex>}}

$s$ 代表初始可行解。它是 $A$ 中列下标的集合，长度为 $m=3$。在这个例子中，取 
{{<katex>}}
$$
s=\{2, 3, 4\}
$$
{{</katex>}}

注意：从 0 开始计数。$s$ 包含 $A$ 的后三列。对应的基矩阵
{{<katex>}}
$$
B=
\begin{bmatrix}
1 & 0 & 0 \\
0 & 1 & 0 \\
0 & 0 & 1
\end{bmatrix}
$$
{{</katex>}}
它是一个单位矩阵，它的逆矩阵等于自身。

我们有
$$
x_B = B^{-1}b = b \geq \mathbf{0}
$$

因此 
$x = [0, 0, 120, 160, 35]^T$ 是一个基本可行解。

### 迭代

**第 0 步**

**第 1 步**

**第 2 步**

**第 3 步**
