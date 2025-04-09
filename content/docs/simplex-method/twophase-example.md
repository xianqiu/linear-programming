---
weight: 50
title: "两阶段法示例"
description: ""
icon: "article"
date: "2025-04-08T09:53:00+08:00"
lastmod: "2025-04-08T09:53:00+08:00"
draft: false
toc: true
katex: true
---

考虑如下问题

{{<katex>}}
$$
\begin{aligned}
\min~ & -7x_1 - 6x_2\\
\text{s.t. } & 3x_1 + x_2 + x_3 = 120\\
& x_1 + 2x_2 + x_4 = 160\\
& x_1 + 2x_2 + x_4 = 160\\
& x_1 + x_5 = 35\\
& x_1, x_2, x_3, x_4, x_5 \geq 0
\end{aligned}
$$
{{</katex>}}

注意第二个等式和第三个等式是一样的，因此有一个冗余约束。暂时不需要删除它，因为两阶段单纯形法求解时，可以识别冗余约束。

### 一阶段问题

引入辅助变量 $y_1, y_2, y_3, y_4 \geq 0$，得到如下一阶段问题。

{{<katex>}}
$$
\begin{aligned}
\min~ & y_1 + y_2 + y_3\\
\text{s.t. } & 3x_1 + x_2 + x_3 + y_1 = 120\\
& x_1 + 2x_2 + x_4 + y_2 = 160\\
& x_1 + 2x_2 + x_4 + y_3 = 160\\
& x_1 + x_5 + y_4 = 35\\
& x_1, x_2, x_3, x_4, x_5 \geq 0\\
& y_1, y_2, y_3, y_4 \geq 0
\end{aligned}
$$
{{</katex>}}

写成矩阵形式就是
{{<katex>}}
$$
\begin{aligned}
\min~ & e^Ty\\
\text{s.t. } & Ax+ I_4y=b\\
& x, y \geq 0
\end{aligned}
$$
{{</katex>}}

其中

{{<katex>}}
$$
A = 
\begin{bmatrix}
3 & 1 & 1 & 0 & 0\\
1 & 2 & 0 & 1 & 0\\
1 & 2 & 0 & 1 & 0\\
1 & 0 & 0 & 0 & 1
\end{bmatrix}
\quad

I_4 = 
\begin{bmatrix}
1 & 0 & 0 & 0\\
0 & 1 & 0 & 0\\
0 & 0 & 1 & 0\\
0 & 0 & 0 & 1
\end{bmatrix}
$$
{{</katex>}}

{{<katex>}}
$$
b = 
\begin{bmatrix}
120\\
160\\
160\\
35
\end{bmatrix}
\quad
e = \begin{bmatrix}
1\\
1\\
1\\
1
\end{bmatrix}
\quad
x= 
\begin{bmatrix}
x_1\\
x_2\\
x_3\\
x_4\\
x_5
\end{bmatrix}
\quad
y = 
\begin{bmatrix}
y_1\\
y_2\\
y_3\\
y_4
\end{bmatrix}
$$
{{</katex>}}

### 一阶段求解

以单位矩阵 $I_4$ 为起点，用单纯形算法求解一阶段问题。得到最优解如下。

{{<katex>}}
$$
\begin{matrix}
| & \textcolor{blue}{x_1} & \textcolor{blue}{x_2} & x_3 & x_4 & \textcolor{blue}{x_5} & y_1 & \textcolor{blue}{y_2} & y_3 & y_4 & |\\
& -   & -   & -   & -   & -   & -   & -   & -    & - \\
| & \textcolor{blue}{16} & \textcolor{blue}{72} & 0 & 0 & \textcolor{blue}{19} & 0 & \textcolor{blue}{0} & 0 & 0 & |\\
\end{matrix}
$$
{{</katex>}}

其中蓝色分量代表基本解。由于 $y=\mathbf{0}$，最优目标函数值为 0，因此 $x$ 是原问题的可行解。

最优解对应的基矩阵 $B$ 如下

{{<katex>}}
$$
\begin{matrix}
x_2 & y_2 & x_5 & x_1\\
-   & -   & -   & -\\
1 & 0 & 0 & 3\\
2 & 1 & 0 & 1\\
2 & 0 & 0 & 1\\
0 & 0 & 1 & 1
\end{matrix}
$$
{{</katex>}}

最优解对应的非基矩阵 $N$ 如下

{{<katex>}}
$$
\begin{matrix}
y_4 & y_1 & x_3 & x_4 & y_3\\
-   & -   & -   & - & -\\
0 & 1 & 1 & 0 & 0 \\
0 & 0 & 0 & 1 & 0\\
0 & 0 & 0 & 1 & 1\\
1 & 0 & 0 & 0 & 0
\end{matrix}
$$
{{</katex>}}

用 $B^{-1}$ 左乘 $[B~ N]$ 得到

{{<katex>}}
$$
\begin{matrix}
& | & x_2 & y_2 & x_5 & x_1 & |\\
--- & & -   & -   & -   & - & \\
B^{-1}B & | & 1 & 0 & 0 & 0 & |\\
& | & 0 & 1 & 0 & 0 & |\\
& | & 0 & 0 & 1 & 0 & |\\
& | & 0 & 0 & 0 & 1 & |
\end{matrix}
$$
{{</katex>}}

{{<katex>}}
$$
\begin{matrix}
&| & y_4 & y_1 & x_3 & x_4 & y_3 & |\\
---& & -   & -   & -   & - & - & \\
B^{-1}N & |& 0 & -0.2 & -0.2 & 0.6 & 0.6 & | \\
& | & 0 & 0 & 0 & 0 & -1 & |\\
& | & 1 & -0.4 & -0.4 & 0.2 & 0.2 &|\\
& | & 0 & 0.4 & 0.4 & -0.2 & -0.2 & |
\end{matrix}
$$
{{</katex>}}

把这两张表合并在一起

{{<katex>}}
$$
\begin{matrix}
| & \textcolor{blue}{x_1} & \textcolor{blue}{x_2} & x_3 & x_4 & \textcolor{blue}{x_5} & y_1 & \textcolor{blue}{y_2} & y_3 & y_4 & |\\
  & -   & -   & -   & -   & -   & -   &   - & -   &  -  & \\
| & 0 & 0 & -0.2 & 0.6 & 0 & -0.2 & 0 & 0.6 & 0 & |\\
| & 0 & 1 & 0 & 0 & 0 & 0 & 1 & -1 & 0 & |\\
| & 0 & 0 & -0.4 & 0.2 & 1 & -0.4 & 0 & 0.2 & 1 & |\\
| & 1 & 0 & 0.4 & -0.2 & 0 & 0.4 & 0 & -0.2 & 0 & |
\end{matrix}
$$
{{</katex>}}

接下来通过入基和出基操作，得到二阶段问题的基本可行解。

### 基本可行解

出基列来自 $y_B$，即

{{<katex>}}
$$
\begin{matrix}
\textcolor{blue}{y_2}\\
-\\
0\\
1\\
0\\
0
\end{matrix}
$$
{{</katex>}}

这里只有一列，那么出基列就是 $y_2$ 对应的列。

入基列来自 $x_N$，即

{{<katex>}}
$$
\begin{matrix}
| & x_3 & x_4 & |\\
& - & - &\\
| & -0.2 & 0.6 & | \\
| &0 & 0 & |\\
| &-0.4 & 0.2 & |\\
| &0.4 & -0.2 & |
\end{matrix}
$$
{{</katex>}}

入基列满足线性无关的条件就可以。注意 $y_2$ 对应的列中，它的第二个分量非零，那么从 $x_N$ 对应的列中，找到第二个分量非零的列即可。

如下图所示，我们看第二行。

{{<katex>}}
$$
\begin{matrix}
y_2 & | & x_3 & x_4 & |\\
-   &   & -   & -   & \\
0 & | & -0.2 & 0.6 & | \\
\textcolor{red}{1} & | &\textcolor{red}{0} & \textcolor{red}{0} & |\\
0 & | &-0.4 & 0.2 & |\\
0 & | &0.4 & -0.2 & |
\end{matrix}
$$
{{</katex>}}

从 $x_3$ 和 $x_4$ 这两列都不满足条件。因此这一行是冗余的。记录冗余的行标，接下来在原问题中删除对应的行。

于是，约束的数量从4变成了3。这意味着原问题基矩阵的维度是3。我们现在已经有一个维度为3的基向量 $[x_1, x_2, x_5]^T$，因此 $x$ 就是原问题的基本可行解。

### 二阶段问题

二阶段问题是原问题删除冗余约束后的问题。
{{<katex>}}
$$
\begin{aligned}
\min~ & -7x_1 - 6x_2\\
\text{s.t. } & 3x_1 + x_2 + x_3 = 120\\
& x_1 + 2x_2 + x_4 = 160\\
& x_1 + x_5 = 35\\
& x_1, x_2, x_3, x_4, x_5 \geq 0
\end{aligned}
$$
{{</katex>}}

其系数矩阵为

{{<katex>}}
$$
A = \begin{bmatrix}
3 & 1 & 1 & 0 & 0\\
1 & 2 & 0 & 1 & 0\\
1 & 0 & 0 & 0 & 1
\end{bmatrix}
$$
{{</katex>}}

根据上一步的计算，我们得到了基本可行解，其中 $x_1, x_2, x_5$ 是它的基变量。它对应的基矩阵

{{<katex>}}
$$
B' =
\begin{bmatrix}
3 & 1 & 0 \\
1 & 2 & 0 \\
1 & 0 & 1 
\end{bmatrix}
$$
{{</katex>}}

就是单纯形算法的起点。

用单纯行算法进行求解，于是得到原问题的最优解。

{{<katex>}}
$$
\begin{matrix}
\textcolor{blue}{x_1} & \textcolor{blue}{x_2} & x_3 & x_4 & \textcolor{blue}{x_5} \\
 - & -   & -   & -   & - \\
\textcolor{blue}{16} & \textcolor{blue}{72} & 0 & 0 & \textcolor{blue}{19}\\
\end{matrix}
$$
{{</katex>}}

在这个例子中，二阶段问题的起点已经是最优解。其最优目标函数值为

$$
-7x_1 - 6x_2 = -544
$$
