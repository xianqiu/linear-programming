---
weight: 420
title: "最优条件"
description: ""
icon: "article"
date: "2025-04-12T09:27:12+08:00"
lastmod: "2025-04-12T09:27:12+08:00"
draft: false
toc: true
katex: true
---

考虑下面这个问题。

{{<katex>}}
$$
\begin{aligned}
\min~ & c^Tx + \mu F(x)\\
\text{s.t. } & Ax = b\\
& x > 0
\end{aligned}
$$
{{</katex>}} 

接下来给出它的最优解条件。理论和相关推导来自凸优化中的 **KKT 条件**，这里不展开。

### 最优条件

设 $x$ 是上述问题的最优解。当且仅当存在对偶变量 $y, s$ 和 $x$ 一起满足如下条件。


1. **原始可行：** $Ax=b$

2. **对偶可行：** $A^Ty + s = c$

3. **互补松弛：** $XSe = \mu e$ 

其中 

{{<katex>}}
$$
\begin{aligned}
X = 
\begin{bmatrix}
x_1 & 0 & \cdots & 0 \\
0 & x_1&  \cdots & 0\\
\vdots & \vdots & \ddots & \vdots\\
0 & 0 & \cdots & x_n 
\end{bmatrix}
\quad
S = 
\begin{bmatrix}
s_1 & 0 & \cdots & 0 \\
0 & s_1&  \cdots & 0\\
\vdots & \vdots & \ddots & \vdots\\
0 & 0 & \cdots & s_n 
\end{bmatrix}
\quad
e = \begin{bmatrix}
1\\
1\\
\vdots \\
1
\end{bmatrix}
\end{aligned}
$$
{{</katex>}}

上面的互补松弛条件也可以写成

$$
x_i s_i = \mu,\quad i =1, 2, ..., n
$$

因为 $\mu > 0$，所以 $x_i > 0$ 且 $s_i > 0$。这说明 $x$ 和 $(y, s)$ 都是内点。

{{<katex>}}
$$
\begin{aligned}
& x\in \mathcal{F}^{\circ}_P =\{x \mid Ax=b, ~ x > 0\}\\
& (y,s) \in \mathcal{F}^{\circ}_D = \{(y,s)\mid A^Ty + s =c, ~ s > 0\}
\end{aligned}
$$
{{</katex>}}


### 方程形式

最优条件也可以写成方程的形式。

{{<katex>}}
$$
F(x,y,s) := \begin{bmatrix}
Ax-b\\
A^Ty + s - c\\
XSe-\mu e
\end{bmatrix}
$$
{{</katex>}}

$x$ 是最优解等价于这个方程有解。

$$
F(x,y,s) = \mathbf{0}
$$

解出这个方程，得到 $x$ 就是上面问题的最优解。

注意到 $F(x,y,s)$ 是一个连续函数且二阶可导，于是可以用牛顿迭代法求解。
