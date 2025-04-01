---
weight: 15
title: "算法示例"
description: ""
icon: "article"
date: "2025-03-27T13:47:58+08:00"
lastmod: "2025-03-27T13:47:58+08:00"
draft: false
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

引入松弛变量 $x_2, x_4, x_5 \geq 0$。把不等式改写成等式，目标函数改写成最小化。

得到如下标准形式。

{{<katex>}}
$$
\begin{aligned}
& \min~ -7x_1 - 6x_2 + 0 x_3 + 0 x_4 + 0x_5\\
& ~ \begin{matrix}
\text{s.t. } & 3x_1 & + & x_2  & + x_3 &       &       & = &120 \\
& x_1  & + & 2x_2 &       & + x_4 &       & = & 160 \\
& x_1  &   &      &       &       & + x_5 & = & 35
\end{matrix}
\end{aligned}
$$
{{</katex>}}

或者写成矩阵形式。

{{<katex>}}
$$
\begin{aligned}
\min~ &
\begin{bmatrix}
-7 & -6 & 0 & 0 & 0
\end{bmatrix} \begin{bmatrix}
x_1 & x_2 & x_3 & x_4 & x_5
\end{bmatrix}^T \\[6pt]
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
&~~ x =[x_1, x_2, x_3, x_4, x_5]^T \geq \mathbf{0}
\end{aligned}
$$
{{</katex>}}

**注意** 新问题最优目标函数值等于原问题最优目标函数值乘以-1。

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

令 {{<katex>}} $ s=\{3, 4, 5\} $ {{</katex>}}，代表 $A$ 中列的集合。它定义了一个基矩阵 $B$， 包含 $A$ 的第 $3, 4, 5$ 列。即
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

我们有
$$
x_B = B^{-1}b = b \geq \mathbf{0}
$$

因此 
$x = [0, 0, 120, 160, 35]^T$ 是一个基本可行解。

### 迭代

每一步迭代就是计算出基变量和入基变量，然后交换对应的列。

**第 0 步**

先计算入基变量。

需要计算 $\mu_N$，根据公式
$$
\mu_N^T = c_N^T - c_B^T B^{-1} N
$$

因为 $c_B = 0$，所以
{{< katex >}}
$$
\mu_N^T = c_N^T =
\begin{bmatrix}
-7 & - 6
\end{bmatrix}
$$
{{< /katex >}}

$\mu, A, b, c$ 的对应关系如下表所示。

{{< katex >}}
$$
\begin{matrix}
c &   | & -7 & -6 & 0  & 0 & 0 & | & b & |\\
&      & -  & -  & -  & - & - & & -\\ 
&     | & 3 & 1 & 1 & 0 & 0 & | & 120 & |\\
A &   | & 1 & 2 & 0 & 1 & 0 & | & 160 & |\\
&     | & 1 & 0 & 0 & 0 & 1 & | & 35 & |\\
&       & - & - & - & - & - &  & - & \\
\mu & | & \textcolor{blue}{-7} & -6 &  0 & 0 & 0& |
\end{matrix}
$$
{{< /katex >}}

根据 $\mu$ 值选入基变量，即 $\mu_j < 0$ 对应的 $x_j$。在上表中 $\mu_1=-7, \mu_2=-6$，因此选 $x_1$ 或者 $x_2$ 都是可行的。不妨选 $\mu$ 值最小的列，即 $x_1$ 作为入基变量。

接下来根据入基变量，计算对应的出基变量。

① 计算 $\tilde{A}$ 和 $\tilde{b}$。 

$B^{-1}$ 分别左乘 $A$ 和 $b$，我们有

$$
B^{-1}A =
\begin{bmatrix}
B^{-1}B & B^{-1}N 
\end{bmatrix}
=\begin{bmatrix}
\mathbf{I} & \tilde{A}
\end{bmatrix}
$$

$$
B^{-1}b = \tilde{b}
$$

我们可以根据上面的表格做计算。对 $A$ 和 $b$ 分别左乘 $B^{-1}$ 得到

{{< katex >}}
$$
\begin{matrix}
c &       ｜ & -7 & -6 & 0 & 0 & 0 &｜& \tilde{b} & | \\
&           & -  & -  & -  & - & - & & - &\\ 
&         | & 3 & 1 & 1  & 0 & 0 & ｜& 120 & |\\
B^{-1}A & | & 1 & 2 & 0  & 1 & 0 &｜& 160 &| \\
&         | & 1 & 0 & 0  & 0 & 1 & ｜& 35 & |\\
&           & -& - & - & & - &   \\
\mu & | & \textcolor{blue}{-7} & -6 & 0& 0 & 0 & ｜
\end{matrix}
$$
{{< /katex >}}

非基矩阵 $N$ 的列是 $1, 2$，因此 $\tilde{A}$ 就是上表 $B^{-1}A$ 前两列。其余三列是一个单位矩阵。由于 $B^{-1}$ 也是单位矩阵，因此 $B^{-1} A = A$，这一步计算实际上没有变化。

② 计算 $\tilde{a}_j$。因为入基变量是 $x_1$，此时 $j=1$，即

{{< katex >}}
$$
\tilde{a}_1 =\begin{bmatrix}
\tilde{a}_{31} \\
\tilde{a}_{41} \\
\tilde{a}_{51} 
\end{bmatrix} = \begin{bmatrix}
3 \\
1 \\
1 
\end{bmatrix}
$$
{{< /katex >}}
注意：$\tilde{a}_1$ 的行下标 $3,4,5$ 对应基矩阵的列。

③ 计算 $\tilde{b}$ 与 $\tilde{a}_1$ 中每个分量的比值。注意：下面式中 $\div$ 代表向量之间元素逐个相除。

{{< katex >}}
$$
\begin{aligned}
\tilde{b} \div \tilde{a}_1 & = 
\begin{bmatrix}
120 \\
160 \\
35
\end{bmatrix} \div
\begin{bmatrix}
\tilde{a}_{31} \\
\tilde{a}_{41} \\
\tilde{a}_{\textcolor{red}{5}1} 
\end{bmatrix}\\
& = \begin{bmatrix}
120 \\
160 \\
35
\end{bmatrix} \div
\begin{bmatrix}
3\\
1\\
1
\end{bmatrix}
=
\begin{bmatrix}
40\\
160\\
\textcolor{red}{35}
\end{bmatrix}
\end{aligned}
$$
{{< /katex >}}

根据比值选择出基变量。在比值为正的分量中，选择最小值对应的行标。上式中最小正值是第三个分量，因此基矩阵 $B$ 的第三列出基，即 $x_5$ 为出基变量。

综上所述，$x_1$ 入基， $x_5$ 出基。此时基矩阵 $B$ 包含 $A$ 的第 $3,4, 1$ 列，非基矩阵 $N$ 包含 $A$ 的第 $5, 2$ 列， 即
{{< katex >}}
$$
B = 
\begin{bmatrix}
1 & 0 & 3\\
0 & 1 & 1\\
0 & 0 & 1
\end{bmatrix}\quad
N = 
\begin{bmatrix}
0 & 1\\
0 & 2\\
1 & 0
\end{bmatrix}
$$
{{< /katex >}}

**第 1 步**

① 更新 $\tilde{A}, \tilde{b}$。

{{< katex >}}
$$
B^{-1}N = \begin{bmatrix}
1 & 0 & -3\\
0 & 1 & -1\\
0 & 0 & 1
\end{bmatrix}\begin{bmatrix}
0 & 1 \\
0 & 2\\
1 & 0
\end{bmatrix} = \begin{bmatrix}
-3 & 1\\
-1 & 2\\
1 & 0
\end{bmatrix}
$$
{{< /katex >}}

{{< katex >}}
$$
\tilde{b} = B^{-1}b = \begin{bmatrix}
1 & 0 & -3\\
0 & 1 & -1\\
0 & 0 & 1
\end{bmatrix}\begin{bmatrix}
120\\
160\\
35
\end{bmatrix} = \begin{bmatrix}
15\\
125\\
35
\end{bmatrix}
$$
{{< /katex >}}

② 计算 $\mu_N$。
{{< katex >}}
$$
\begin{aligned}
\mu_N^T & = c_N^T - c_B^T B^{-1} N \\
& = 
\begin{bmatrix}
0 & -6
\end{bmatrix} -
\begin{bmatrix}
0 & 0 & -7
\end{bmatrix}
\begin{bmatrix}
-3 & 1\\
-1 & 2\\
1 & 0
\end{bmatrix}\\[6pt]
& =
\begin{bmatrix}
0 & -6
\end{bmatrix} -
\begin{bmatrix}
-7 & 0
\end{bmatrix}\\
& = \begin{bmatrix}
 7 & -6
\end{bmatrix}
\end{aligned}
$$
{{< /katex >}}

③ 更新表格。

{{< katex >}}
$$
\begin{matrix}
c &       ｜ & -7 & -6 & 0 & 0 & 0 &｜& \tilde{b} & | &\\
&           & -  & -  & -  & - & - & & - & \\ 
&         | & 0 & 1 & 1  & 0 & -3 & ｜& 15 & | \\
B^{-1}A & | & 0 & 2 & 0  & 1 & -1 &｜& 125 &| \\
&         | & 1 & 0 & 0  & 0 & 1 & ｜& 35 & |\\
&           & -& - & - & & - &  & - &  \\
\mu & | & 0 & \textcolor{blue}{-6} & 0& 0 & 7 & ｜ 
\end{matrix}
$$
{{< /katex >}}

④ 选择入基变量。$\mu_2 =-6 < 0$，选择 $x_2$ 作为入基变量。

⑤ 计算比值。

{{< katex >}}
$$ 
\begin{aligned}
\tilde{b}\div \tilde{a}_2 & =
\begin{bmatrix}
15\\
125\\
35
\end{bmatrix}
\div
\begin{bmatrix}
\tilde{a}_{\textcolor{red}{3}2}\\
\tilde{a}_{42}\\
\tilde{a}_{12}
\end{bmatrix}\\
& =\begin{bmatrix}
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
\textcolor{red}{15}\\
62.5\\
\infty
\end{bmatrix}
\end{aligned}
$$
{{< /katex >}}

选择最小比值 $15$ 对应的行下标 $3$，即 $x_3$ 作为出基变量。

综上所述，$x_2$ 入基，$x_3$ 出基。此时基矩阵 $B$ 包含 $A$ 的第 $2, 4, 1$ 列，非基矩阵 $N$ 包含 $A$ 的第 $5, 3$ 列， 即
{{< katex >}}
$$
B = 
\begin{bmatrix}
1 & 0 & 3\\
2 & 1 & 1\\
0 & 0 & 1
\end{bmatrix}\quad
N = 
\begin{bmatrix}
0 & 1\\
0 & 0\\
1 & 0
\end{bmatrix}
$$
{{< /katex >}}

**第 2 步**

① 更新 $\tilde{A}, \tilde{b}$。

{{< katex >}}
$$
B^{-1}N = \begin{bmatrix}
1 & 0 & -3\\
-2 & 1 & 5\\
0 & 0 & 1
\end{bmatrix}\begin{bmatrix}
0 & 1 \\
0 & 0\\
1 & 0
\end{bmatrix} = \begin{bmatrix}
-3 & 1\\
5 & -2\\
1 & 0
\end{bmatrix}
$$
{{< /katex >}}

{{< katex >}}
$$
\tilde{b} = B^{-1}b = \begin{bmatrix}
1 & 0 & -3\\
0 & 1 & -1\\
0 & 0 & 1
\end{bmatrix}\begin{bmatrix}
120\\
160\\
35
\end{bmatrix} = \begin{bmatrix}
15\\
95\\
35
\end{bmatrix}
$$
{{< /katex >}}

② 计算 $\mu_N$。
{{< katex >}}
$$
\begin{aligned}
\mu_N^T & = c_N^T - c_B^T B^{-1} N \\
& = 
\begin{bmatrix}
0 & 0
\end{bmatrix} -
\begin{bmatrix}
-6 & 0 & -7
\end{bmatrix}
\begin{bmatrix}
-3 & 1\\
5 & -2\\
1 & 0
\end{bmatrix}\\[6pt]
& =
\begin{bmatrix}
0 & 0
\end{bmatrix} -
\begin{bmatrix}
11 & -6
\end{bmatrix}\\
& = \begin{bmatrix}
 -11 & 6
\end{bmatrix}
\end{aligned}
$$
{{< /katex >}}

③ 更新表格。

{{< katex >}}
$$
\begin{matrix}
c &       ｜ & -7 & -6 & 0 & 0 & 0 &｜& \tilde{b} & | &\\
&           & -  & -  & -  & - & - & & - & \\ 
&         | & 0 & 1 & 1  & 0 & -3 & ｜& 15 & | \\
B^{-1}A & | & 0 & 0 & -2  & 1 & 5 &｜& 95 &| \\
&         | & 1 & 0 & 0  & 0 & 1 & ｜& 35 & |\\
&           & -& - & - & & - &  & - &  \\
\mu & | & 0 & 0 & 6& 0 & \textcolor{blue}{-11} & ｜ 
\end{matrix}
$$
{{< /katex >}}

④ 选择入基变量。$\mu_5=-11 < 0$，选择 $x_5$ 作为入基变量。

⑤ 计算比值。

{{< katex >}}
$$ 
\begin{aligned}
\tilde{b}\div \tilde{a}_5 & =
\begin{bmatrix}
15\\
95\\
35
\end{bmatrix}
\div
\begin{bmatrix}
\tilde{a}_{25}\\
\tilde{a}_{\textcolor{red}{4}5}\\
\tilde{a}_{15}
\end{bmatrix}\\
& =\begin{bmatrix}
15\\
95\\
35
\end{bmatrix}\div
\begin{bmatrix}
-3\\
5\\
1
\end{bmatrix}=
\begin{bmatrix}
-5\\
\textcolor{red}{19}\\
35
\end{bmatrix}
\end{aligned}
$$
{{< /katex >}}

选择最小**正**比值 $15$ 对应的行下标 $2$，即 $x_4$ 作为出基变量。

综上所述，$x_5$ 入基，$x_4$ 出基。此时基矩阵 $B$ 包含 $A$ 的第 $2, 5, 1$ 列，非基矩阵 $N$ 包含 $A$ 的第 $4, 3$ 列， 即
{{< katex >}}
$$
B = 
\begin{bmatrix}
1 & 0 & 3\\
2 & 0 & 1\\
0 & 1 & 1
\end{bmatrix}\quad
N = 
\begin{bmatrix}
0 & 1\\
1 & 0\\
0 & 0
\end{bmatrix}
$$
{{< /katex >}}

**第 3 步**

① 更新 $\tilde{A}, \tilde{b}$。

{{< katex >}}
$$
B^{-1}N = \begin{bmatrix}
-0.2 & 0.6 & 0\\
-0.2 & 0.4 & 1\\
0.4 & -0.2 & 0
\end{bmatrix}\begin{bmatrix}
0 & 1 \\
1 & 0\\
0 & 0
\end{bmatrix} = \begin{bmatrix}
0.6 & -0.2\\
0.2 & -0.4\\
-0.2 & 0.4
\end{bmatrix}
$$
{{< /katex >}}

{{< katex >}}
$$
\tilde{b} = B^{-1}b = \begin{bmatrix}
-0.2 & 0.6 & 0\\
-0.2 & 0.4 & 1\\
0.4 & -0.2 & 0
\end{bmatrix}\begin{bmatrix}
120\\
160\\
35
\end{bmatrix} = \begin{bmatrix}
72\\
19\\
16
\end{bmatrix}
$$
{{< /katex >}}

② 计算 $\mu_N$。
{{< katex >}}
$$
\begin{aligned}
\mu_N^T & = c_N^T - c_B^T B^{-1} N \\
& = 
\begin{bmatrix}
0 & 0
\end{bmatrix} -
\begin{bmatrix}
-6 & 0 & -7
\end{bmatrix}
\begin{bmatrix}
0.6 & -0.2\\
0.2 & -0.4\\
-0.2 & 0.4
\end{bmatrix}\\[6pt]
& =
\begin{bmatrix}
0 & 0
\end{bmatrix} -
\begin{bmatrix}
-2.2 & -1.6
\end{bmatrix}\\
& = \begin{bmatrix}
 2.2 & 1.6
\end{bmatrix}
\end{aligned}
$$
{{< /katex >}}

③ 更新表格。

{{< katex >}}
$$
\begin{matrix}
c &       ｜ & -7 & -6 & 0 & 0 & 0 &｜& \tilde{b} & | &\\
&           & -  & -  & -  & - & - & & - & \\ 
&         | & 0 & 1 &  0.6 & -0.2 & 0 & ｜& 72 & | \\
B^{-1}A & | & 0 & 0 &  0.2 & -0.4 & 1 &｜& 19 &| \\
&         | & 1 & 0 & -0.2  & 0.4 & 0 & ｜& 16 & |\\
&           & -& - & - & & - &  & - &  \\
\mu & | & 0 &0 & 1.6& 2.2 & 0 & ｜ 
\end{matrix}
$$
{{< /katex >}}

满足最优条件 $\mu \geq \mathbf{0}$，停止迭代。

## 最优解

最优解对应的基矩阵 $B$ 为 $A$ 的第 $2, 5, 1$ 列，即
$$
{{< katex >}}
B = 
\begin{bmatrix}
1 & 0 & 3\\
2 & 0 & 1\\
0 & 1 & 1
\end{bmatrix}
$$
{{< /katex >}}

我们有 

{{< katex >}}
$$
\begin{aligned}
x_B & = \begin{bmatrix}
x_2\\
x_4\\
x_5
\end{bmatrix}
=B^{-1}b \\[6pt]
& = \begin{bmatrix}
-0.2 & 0.6 & 0\\
-0.2 & 0.4 & 1\\
0.4 & -0.2 & 0
\end{bmatrix}\begin{bmatrix}
120\\
160\\
35
\end{bmatrix}
= \begin{bmatrix}
72\\
19\\
16
\end{bmatrix}
\end{aligned}
$$
{{< /katex >}}

因此，最优解为
$$
x^T = \begin{bmatrix}
16 & 72 & 0 & 0 & 19
\end{bmatrix}
$$

最小化问题的最优目标函数值为
{{< katex >}}
$$
c^Tx = 
\begin{bmatrix}
-7 & -6 & 0 & 0 & 0
\end{bmatrix}
\begin{bmatrix}
16 \\
72 \\ 
0 \\ 
0 \\
19
\end{bmatrix} = -544
$$
{{< /katex >}}

因此，原问题（最大化问题）的最优目标函数值为 
$$
-c^Tx = 544
$$



